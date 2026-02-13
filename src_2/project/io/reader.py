import logging
import pandas as pd

from pandas import DataFrame
from pathlib import Path

from project.core.settings import REPO_ROOT
from project.helpers.errors import AbstractError
from project.models.config import Config

logger = logging.getLogger(__name__)

class ReadDataWithPandasError(AbstractError): pass

ATTEMPT_MESSAGE = "reading data with pandas"
SUCCESS_MESSAGE = "read data with pandas"
FAILURE_MESSAGE = "failed to read data with pandas"

def read_data_with_pandas(config: Config, source_index: int) -> DataFrame:
  """
  ### **Throws**

  `ReadDataWithPandasError`
  """
  source = config.sources[source_index]

  resolved_path = source.path
  p = Path(source.path)
  if not p.is_absolute():
    p = REPO_ROOT / p
  resolved_path = str(p)

  kwargs = {
    "source_index": source_index,
    "source_name": source.name,
    "source_path": resolved_path,
    "source_format": source.format
  }

  logger.info(ATTEMPT_MESSAGE, extra=kwargs)
  try:
    match source.format:
      case "csv":
        logger.debug("matched source format", extra={"format": source.format})
        data = pd.read_csv(
          resolved_path,
          dtype_backend="pyarrow",
          engine="pyarrow",
          usecols=tuple(source.mapping.keys()),
          dtype={mapping[0]: mapping[1].type for mapping in source.mapping.items()},
          delimiter=source.options.delimiter
        )
        logger.info(SUCCESS_MESSAGE, extra=kwargs)
        return data

      case "json":
        logger.debug("matched source format", extra={"format": source.format})
        data = pd.read_json(
          resolved_path,
          dtype_backend="pyarrow",
          dtype={mapping[0]: mapping[1].type for mapping in source.mapping.items()}
        )
        logger.info(SUCCESS_MESSAGE, extra=kwargs)
        return data

      case _:
        raise ValueError(f"unsupported source format: {source.format}")

  except Exception as err:
    error = ReadDataWithPandasError(FAILURE_MESSAGE, cause=type(err).__name__)
    logger.error(error.message, extra={**error.kwargs, **kwargs})
    raise error from err