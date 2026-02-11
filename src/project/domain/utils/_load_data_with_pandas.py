import logging
import pandas as pd

from pandas import DataFrame

from project.helpers.errors import AbstractError

from ..models import Config

logger = logging.getLogger(__name__)

class LoadDataWithPandasError(AbstractError): pass

ATTEMPT_MESSAGE = "loading data with pandas"
SUCCESS_MESSAGE = "successfully loaded data with pandas"
FAILURE_MESSAGE = "failed to load data with pandas"

def load_data_with_pandas(config: Config, source_index: int) -> DataFrame:
  """
  ### **Throws**

  `LoadDataWithPandasError`
  """
  source = config.external.sources[source_index]
  source_path = source.path
  source_format = source.format
  kwargs = {
    "source_index": source_index,
    "source_path": source_path,
    "source_format": source_format
  }
  logger.info(ATTEMPT_MESSAGE, extra=kwargs)
  try:
    field_dtype_map = {field.source_name: field.source_dtype for field in source.fields}
    match source_format:
      case Config.External.Source.Format.CSV:
        logger.debug("matched source format", extra={"format": source_format})
        field_name_tuple = tuple(field.source_name for field in source.fields)
        data = pd.read_csv(source_path, dtype_backend="pyarrow", engine="pyarrow", usecols=field_name_tuple, dtype={**field_dtype_map})
        logger.info(SUCCESS_MESSAGE, extra=kwargs)
        return data
      case Config.External.Source.Format.JSON:
        logger.debug("matched source format", extra={"format": source_format})
        data = pd.read_json(source_path, dtype_backend="pyarrow", dtype={**field_dtype_map})
        logger.info(SUCCESS_MESSAGE, extra=kwargs)
        return data
  except Exception as err:
    error = LoadDataWithPandasError(FAILURE_MESSAGE, cause=type(err).__name__)
    logger.error(error.message, extra={**error.kwargs, **kwargs})
    raise error from err

__all__ = ["load_data_with_pandas", "LoadDataWithPandasError"]
