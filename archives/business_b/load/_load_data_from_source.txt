import logging
import pandas as pd

from pandas import DataFrame

from project.errors.abstract import AbstractError
from project.models import Config

logger = logging.getLogger(__name__)

class LoadDataFromSourceError(AbstractError): pass

def load_data_from_source(source_format: Config.Source.Format, source_path: str) -> DataFrame:
  """
  ### **Throws**

  `LoadDataFromSourceError`
  """
  logger.info("loading data from source", extra={"format": source_format, "path": source_path})
  try:
    match source_format:
      case Config.Source.Format.CSV:
        logger.debug("successfully matched source format %s", source_format, extra={"format": source_format})
        data = pd.read_csv(source_path, dtype_backend="pyarrow", engine="pyarrow")
        logger.info("successfully loaded data", extra={"path": source_path})
        return data
      case Config.Source.Format.JSON:
        logger.debug("successfully matched source format %s", source_format, extra={"format": source_format})
        data = pd.read_json(source_path, dtype_backend="pyarrow")
        logger.info("successfully loaded data from source", extra={"path": source_path})
        return data
  except Exception as e:
    error = LoadDataFromSourceError("failed to load data from source", "unknown exception")
    logger.error(error.message, extra={"format": source_format, "path": source_path})
    raise error from e

__all__ = ["load_data_from_source", "LoadDataFromSourceError"]
