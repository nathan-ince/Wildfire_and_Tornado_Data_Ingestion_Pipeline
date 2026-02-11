import logging

import pandas as pd

from dataclasses import dataclass

from project.helpers.enums import PyArrowDataType
from project.helpers.errors import AbstractError

from ...models import Config
from ...utils import (
  load_config_from_yaml, LoadConfigFromYamlError,
  load_data_with_pandas, LoadDataWithPandasError
)

class IngestError(AbstractError): pass

logger = logging.getLogger(__name__)

NAME = "tornado_usa"
CONFIG_FILE_PATH = "config/tornado_usa.yaml"
ATTEMPT_MESSAGE = f"ingesting {NAME}"
SUCCESS_MESSAGE = f"successfully ingested {NAME}"
FAILURE_MESSAGE = f"failed to ingest {NAME}"

KWARGS = {
  "ingest_name": NAME,
  "config_file_path": CONFIG_FILE_PATH
}

def clean(data: pd.DataFrame):
  data["state"] = data["state"].str.strip().str.upper()
  data["date"] = data["date"].combine_first(
    pd.to_datetime(data[["year", "month", "day"]], errors="coerce").astype(PyArrowDataType.date32.value)
  )

@dataclass
class DedupeResult:
  duplicate_count: int
  accepted_data: pd.DataFrame
  rejected_data: pd.DataFrame

def dedupe(data: pd.DataFrame) -> DedupeResult:
  duplicate_mask = data.duplicated(keep=False)
  count = duplicate_mask.sum() # In Python, True = 1 and False = 0
  accepted = data[~duplicate_mask].copy()
  rejected = data[duplicate_mask].copy()
  rejected["reason"] = "duplicate record"
  return DedupeResult(count, accepted, rejected)

def ingest():
  logger.info(ATTEMPT_MESSAGE, extra=KWARGS)
  try:
    config = load_config_from_yaml(CONFIG_FILE_PATH)
    sources = config.external.sources
    source_count = len(sources)
    for source_index in range(source_count):
      data = load_data_with_pandas(config, source_index)
      source = sources[source_index]
      field_source_name_list = list(field.source_name for field in source.fields)
      field_source_target_name_map = dict({field.source_name: field.target_name for field in source.fields})
      data = data[field_source_name_list].copy()
      data = data[field_source_name_list].rename(columns=field_source_target_name_map)
      clean(data)
      dedupe_result = dedupe(data)
      print(data.info())
      print(dedupe_result)
  except Exception as err:
    error = IngestError(FAILURE_MESSAGE, cause=type(err).__name__)
    logger.error(error.message, extra={**error.kwargs, **KWARGS})
    raise error from err

__all__ = ["ingest", "IngestError"]
