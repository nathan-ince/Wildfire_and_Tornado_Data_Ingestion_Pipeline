import logging

from pandas import DataFrame
from typing import Callable, TypeAlias

from project.errors import BatchProcessError, MainProcessError
from project.helpers.utils import generate_random_uuid, generate_timestamp
from project.models import Config
from project.postgres.types import Status
from project.postgres.utils import (
  initialize_main_process, InitializeMainProcessError,
  initialize_batch_process, InitializeBatchProcessError,
  finalize_main_process, FinalizeMainProcessError,
  finalize_batch_process, FinalizeBatchProcessError
)

from ._load_config_from_yaml import load_config_from_yaml, LoadConfigFromYamlError
from ._load_data_with_pandas import load_data_with_pandas
from ._stored_data_in_postgres import store_data_in_postgres

logger = logging.getLogger(__name__)

TransformFunction: TypeAlias = Callable[[Config, int, DataFrame], tuple[DataFrame, DataFrame]]

def run_main_process(config_path: str, transform_data: TransformFunction) -> None:
  """
  ### **Parameters**

  `config_path` :: `str` - the path of the config file

  `transform_data` :: `TransformFunction` - a specific type of function 

  ---

  ### **Returns**

  `None`
  """
  logger.info("starting main process")
  main_process_id = generate_random_uuid()
  main_process_start_timestamp = generate_timestamp()
  try:
    initialize_main_process(
      main_process_id=main_process_id,
      main_process_start_timestamp=main_process_start_timestamp
    )
  except InitializeMainProcessError as err:
    main_process_final_timestamp = generate_timestamp()
    error = MainProcessError(
      "aborted main process",
      cause=type(err).__name__,
      main_process_id=str(main_process_id),
      main_process_start_timestamp=str(main_process_start_timestamp),
      main_process_final_timestamp=str(main_process_final_timestamp)
    )
    logger.error(error.message)
    return None
  try:
    config = load_config_from_yaml(config_path)
  except LoadConfigFromYamlError as err:
    main_process_final_timestamp = generate_timestamp()
    error = MainProcessError(
      "aborted main process",
      cause=type(err).__name__,
      main_process_id=str(main_process_id),
      main_process_start_timestamp=str(main_process_start_timestamp),
      main_process_final_timestamp=str(main_process_final_timestamp)
    )
    logger.error(error.message, extra=error.kwargs)
    try:
      finalize_main_process(
        main_process_id=main_process_id,
        main_process_status=Status.Failure,
        main_process_final_timestamp=main_process_final_timestamp
      )
      return None
    except FinalizeMainProcessError: return None
  source_count = len(config.sources)
  batch_process_errors: list[BatchProcessError] = []
  for source_index in range(source_count):
    logger.info("starting batch process %s/%s", source_index + 1, source_count)
    batch_process_id = generate_random_uuid()
    batch_process_start_timestamp = generate_timestamp()
    try:
      initialize_batch_process(
        main_process_id=main_process_id,
        batch_process_id=batch_process_id,
        batch_process_start_timestamp=batch_process_start_timestamp
      )
    except InitializeBatchProcessError as err:
      batch_process_final_timestamp = generate_timestamp()
      error = BatchProcessError(
        f"aborted batch process {source_index + 1}/{source_count}",
        cause=type(err).__name__,
        batch_process_id=str(batch_process_id),
        batch_process_start_timestamp=str(batch_process_start_timestamp),
        batch_process_final_timestamp=str(batch_process_final_timestamp)
      )
      logger.error(error.message, extra=error.kwargs)
      batch_process_errors.append(error)
      continue
    try:
      df_raw = load_data_with_pandas(config, source_index)
      df_accepted, df_rejected = transform_data(config, source_index, df_raw) # where everything unique to each pipeline happens
      df_accepted_copy = df_accepted.copy()
      df_accepted_copy["batch_process_id"] = batch_process_id
      df_rejected_copy = df_rejected.copy()
      df_rejected_copy["batch_process_id"] = batch_process_id
      store_data_in_postgres(config, df_accepted_copy, df_rejected_copy)
      logger.info("completed batch process %s/%s", source_index + 1, source_count)
      batch_process_final_timestamp = generate_timestamp()
      try:
        finalize_batch_process(
          batch_process_id=batch_process_id,
          batch_process_status=Status.Success,
          batch_process_final_timestamp=batch_process_final_timestamp
        )
        continue
      except FinalizeBatchProcessError: continue
    except Exception as err:
      batch_process_final_timestamp = generate_timestamp()
      error = BatchProcessError(
        f"aborted batch process {source_index + 1}/{source_count}",
        cause=type(err).__name__,
        batch_process_id=str(batch_process_id),
        batch_process_start_timestamp=str(batch_process_start_timestamp),
        batch_process_final_timestamp=str(batch_process_final_timestamp)
      )
      logger.error(error.message, extra=error.kwargs)
      batch_process_errors.append(error)
      try:
        finalize_batch_process(
          batch_process_id=batch_process_id,
          batch_process_status=Status.Failure,
          batch_process_final_timestamp=batch_process_final_timestamp
        )
        continue
      except FinalizeBatchProcessError: continue
  main_process_final_timestamp = generate_timestamp()
  logger.info("completed main process")
  batch_process_error_count = len(batch_process_errors)
  if batch_process_error_count == 0:
    logger.info("all sources were processed successfully", extra={"source_count": source_count})
    try:
      finalize_main_process(
        main_process_id=main_process_id,
        main_process_status=Status.Success,
        main_process_final_timestamp=main_process_final_timestamp
      )
    except FinalizeMainProcessError: return None
    else: return None
  else:
    logger.warning("not all sources were processed successfully", extra={"source_count": source_count, "error_count": batch_process_error_count})
    try:
      finalize_main_process(
        main_process_id=main_process_id,
        main_process_status=Status.Warning,
        main_process_final_timestamp=main_process_final_timestamp
      )
    except FinalizeMainProcessError: return None
    else: return None

__all__ = ["run_main_process"]
