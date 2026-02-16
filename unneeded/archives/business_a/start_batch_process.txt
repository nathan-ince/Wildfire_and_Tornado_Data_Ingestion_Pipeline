################################################################################################

from logging import getLogger
from pandas import DataFrame
from pandera.errors import SchemaErrors
from typing import cast
from uuid import UUID, uuid4

################################################################################################

from project.errors.abstract import AbstractError

from project.models import PipelineConfigurationSettings as Config

from project.sql import (
  insert_batch_process, InsertBatchProcessError,
  update_batch_process, UpdateBatchProcessError
)

from project.utils import generate_timestamp

from ..schemas.internal import schema

from .load_external_data import load_external_data, LoadExternalDataError
from .validate_field_name_configuration import validate_field_name_configuration, FieldNameConfigurationError

################################################################################################

logger = getLogger(__name__)

################################################################################################

class ProcessBatchDataError(AbstractError): pass

def process_batch_data(data: DataFrame, config: Config, source_index: int, batch_process_id: str):
  try:
    validate_field_name_configuration(data, config, source_index)
    source = config.external.sources[source_index]
    data = data[list(source.table.fields.map.keys())].rename(columns=source.table.fields.map)
    required_field_name_list = ["a", "b", "c"]
    mask_present = data[required_field_name_list].notna().all(axis=1)
    data_present = data[mask_present].copy()
    data_absent = data[~mask_present].copy()
    # need to validate/coerce data types
    # some columns are null in the externally and I don't want them to be null internally
  except FieldNameConfigurationError as e:
    logger.warning("failed to process batch data")
    exception = ProcessBatchDataError("field name configuration error")
    logger.error(exception.message)
    raise exception from e
  except Exception as e:
    logger.warning("failed to process batch data")
    exception = ProcessBatchDataError("unknown error", name=type(e).__class__)
    logger.error(exception.message)
    raise exception from e

################################################################################################

def start_batch_process(config: Config, source_index: int, main_process_id: UUID) -> None:
  logger.info("starting batch process")
  batch_process_start_timestamp = generate_timestamp()
  logger.info("batch process started at %s", batch_process_start_timestamp)
  batch_process_id = uuid4()
  logger.debug("batch_process_id = %s", batch_process_id)
  source = config.external.sources[source_index]
  try: insert_batch_process(main_process_id, batch_process_id, source_index, source.path, batch_process_start_timestamp)
  except InsertBatchProcessError:
    batch_process_final_timestamp = generate_timestamp()
    logger.warning("batch process aborted at %s", batch_process_final_timestamp)
    return
  try: raw_data = load_external_data(config, source)
  except LoadExternalDataError:
    batch_process_final_timestamp = generate_timestamp()
    logger.warning("batch process aborted at %s", batch_process_final_timestamp)
    return
  try: raw_data = raw_data[list(source.table.fields.map.keys())].rename(columns=source.table.fields.map)
  except Exception:
    batch_process_final_timestamp = generate_timestamp()
    logger.warning("batch process aborted at %s", batch_process_final_timestamp)
    return
  print(raw_data.info())
  batch_process_final_timestamp = generate_timestamp()
  logger.info("batch process completed at %s", batch_process_final_timestamp)
  return
  # try:
  #   valid_data = schema.validate(raw_data, lazy=True).copy()
  #   valid_data["batch_process_id"] = batch_process_id
  #   valid_data["record_index"] = batch_process_id
  #   print("VALID TABLE DATA", valid_data.head(100))
  #   batch_process_final_timestamp = generate_timestamp()
  #   logger.info("batch process completed at %s", batch_process_final_timestamp)
  #   return
  # except SchemaErrors as e:
  #   failure_data = cast(DataFrame, e.failure_cases)
  #   rejected_index_list = failure_data["index"].dropna().astype(int).unique().tolist()
  #   candidate_valid_data = raw_data.drop(index=rejected_index_list).copy()
  #   try: accepted_data = schema.validate(candidate_valid_data).copy()
  #   except Exception:
  #     logger.error("this branch should never be entered")
  #     batch_process_final_timestamp = generate_timestamp()
  #     logger.warning("batch process aborted at %s", batch_process_final_timestamp)
  #     return
  #   accepted_data["batch_process_id"] = batch_process_id
  #   accepted_data["record_index"] = batch_process_id
  #   print("ACCEPTED TABLE DATA", accepted_data.head(100))
  #   rejected_data = raw_data.loc[rejected_index_list].copy()
  #   rejected_data["batch_process_id"] = batch_process_id
  #   rejected_data["record_index"] = rejected_data.index
  #   print("REJECTED TABLE DATA", rejected_data.head(100))
  #   batch_process_final_timestamp = generate_timestamp()
  #   logger.info("batch process completed at %s", batch_process_final_timestamp)
  #   return
  # except Exception:
    # batch_process_final_timestamp = generate_timestamp()
    # logger.warning("batch process aborted at %s", batch_process_final_timestamp)
    # return

################################################################################################

__all__ = ["start_batch_process"]

################################################################################################
