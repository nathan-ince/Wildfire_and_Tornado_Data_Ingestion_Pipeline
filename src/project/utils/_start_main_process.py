import logging

from pandas import DataFrame
from typing import Callable, TypeAlias

from project.errors import MainProcessError
from project.helpers.utils import generate_random_uuid, generate_timestamp
from project.models import Config

from ._load_config_from_yaml import load_config_from_yaml
from ._load_data_with_pandas import load_data_with_pandas
from ._stored_data_in_postgres import store_data_in_postgres

logger = logging.getLogger(__name__)

TransformFunction: TypeAlias = Callable[[Config, int, DataFrame], tuple[DataFrame, DataFrame]]

def start_main_process(config_path: str, transform_data: TransformFunction):
  """
  ### **Throws**

  `MainProcessError`
  """
  main_process_id = generate_random_uuid()
  main_process_start_timestamp = generate_timestamp()
  logger.info("starting main process", extra={"main_process_id": str(main_process_id)})
  try:
    config = load_config_from_yaml(config_path)
    any_batch_errors: bool = False
    for source_index in range(len(config.sources)):
      batch_process_id = generate_random_uuid()
      batch_process_start_timestamp = generate_timestamp()
      logger.info("starting batch process %s/%s", source_index + 1, len(config.sources), extra={"batch_process_id": str(batch_process_id)})
      try:
        df_raw = load_data_with_pandas(config, source_index)
        df_accepted, df_rejected = transform_data(config, source_index, df_raw)
        store_data_in_postgres(config, df_accepted, df_rejected)
        # batch_process_final_timestamp = generate_timestamp()
        logger.info("successfully completed batch process %s/%s", source_index + 1, len(config.sources), extra={"batch_process_id": str(batch_process_id)})
      except Exception as err:
        any_batch_errors = True
        batch_process_final_timestamp = generate_timestamp()
        logger.error("batch process %s/%s failed", source_index + 1, len(config.sources), extra={
          "cause": type(err).__name__,
          "config_path": config_path,
          "source_index": source_index,
          "source_name": config.sources[source_index].name,
          "batch_process_id": str(batch_process_id),
          "batch_process_start_timestamp": str(batch_process_start_timestamp),
          "batch_process_final_timestamp": str(batch_process_final_timestamp),
        })
        continue
    main_process_final_timestamp = generate_timestamp()
    if any_batch_errors is False: logger.info("successfully completed main process", extra={"main_process_id": str(main_process_id)})
    else: logger.warning("partially successful main process", extra={"main_process_id": str(main_process_id)})
  except Exception as err:
    main_process_final_timestamp = generate_timestamp()
    error = MainProcessError(
      "main process failed",
      cause=type(err).__name__,
      config_path=config_path,
      main_process_id=str(main_process_id),
      main_process_start_timestamp=str(main_process_start_timestamp),
      main_process_final_timestamp=str(main_process_final_timestamp),
    )
    logger.error(error.message, extra=error.kwargs)
    raise error from err

__all__ = ["start_main_process"]
