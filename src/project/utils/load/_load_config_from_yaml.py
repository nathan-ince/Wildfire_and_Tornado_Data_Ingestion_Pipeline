import logging
import yaml

from pydantic import ValidationError

from project.errors import AbstractError
from project.models import Config

logger = logging.getLogger(__name__)

class LoadConfigFromYamlError(AbstractError): pass

def load_config_from_yaml(path: str) -> Config:
  """
  ### **Description**

  This function will load the content of a `YAML` file into a `Config` object.

  ---

  ### **Parameters**

  `path` :: `str` - the path of the configuration file

  ---

  ### **Throws**

  `LoadConfigFromYamlError`
  """
  logger.info("loading config from yaml", extra={"path": path})
  try:
    with open(path, mode="r") as file:
      content = yaml.safe_load(file)
      result = Config(**content)
      logger.info("successfully loaded config from yaml", extra={"path": path})
      return result
  except ValidationError as e:
    error = LoadConfigFromYamlError("failed to load config from YAML", "pydantic validation error")
    logger.error(error.message, extra={
      "path": path,
      "error_count": e.error_count(),
      "error_messages": e.errors()
    })
    raise error from e
  except Exception as e:
    error = LoadConfigFromYamlError("failed to load config from YAML", "unknown exception")
    logger.error(error.message, extra={
      "path": path,
      "error_class": type(e).__name__,
      "error_args": e.args
    })
    raise error from e
  return

__all__ = ["load_config_from_yaml", "LoadConfigFromYamlError"]
