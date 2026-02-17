################################################################################################

import logging
import yaml

from pathlib import Path
from yaml import YAMLError

################################################################################################

from project.models import PipelineConfigurationSettings as Config

from ..constants import CONFIG_FILE_PATH

################################################################################################

logger = logging.getLogger(__name__)

################################################################################################

class LoadConfigurationError(Exception):
  def __init__(self, reason: str = "N/A", path: str | Path = "N/A"):
    self.message = f"load configuration error :: reason = {reason} :: path = {path}"
    self.reason = reason
    self.path = path
    super().__init__(self.message)

################################################################################################

def load_configuration() -> Config:
  """
  ### **Throws**

  `LoadConfigurationError` - if an error occurs
  """
  logger.info("loading configuration settings")
  try:
    with open(file=CONFIG_FILE_PATH, mode="r") as file:
      content = yaml.safe_load(file)
      settings = Config(**content)
      logger.info("configuration settings have been loaded")
      return settings
  except FileNotFoundError as e:
    logger.warning("failed to load configuration settings")
    exception = LoadConfigurationError(reason=f"FileNotFoundError = {type(e).__name__}", path=CONFIG_FILE_PATH)
    logger.error(exception.message)
    raise exception from e
  except IsADirectoryError as e:
    logger.warning("failed to load configuration settings")
    exception = LoadConfigurationError(reason=f"IsADirectoryError = {type(e).__name__}", path=CONFIG_FILE_PATH)
    logger.error(exception.message)
    raise exception from e
  except PermissionError as e:
    logger.warning("failed to load configuration settings")
    exception = LoadConfigurationError(reason=f"PermissionError = {type(e).__name__}", path=CONFIG_FILE_PATH)
    logger.error(exception.message)
    raise exception from e
  except OSError as e:
    logger.warning("failed to load configuration settings")
    exception = LoadConfigurationError(reason=f"OSError = {type(e).__name__}", path=CONFIG_FILE_PATH)
    logger.error(exception.message)
    raise exception from e
  except YAMLError as e:
    logger.warning("failed to load configuration settings")
    exception = LoadConfigurationError(reason=f"YAMLError = {type(e).__name__}", path=CONFIG_FILE_PATH)
    logger.error(exception.message)
    raise exception from e
  except Exception as e:
    logger.warning("failed to load configuration settings")
    exception = LoadConfigurationError(reason=f"Exception = {type(e).__name__}", path=CONFIG_FILE_PATH)
    logger.error(exception.message)
    raise exception from e

################################################################################################

__all__ = ["load_configuration", "LoadConfigurationError"]

################################################################################################
