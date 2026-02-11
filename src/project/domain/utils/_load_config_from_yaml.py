import logging

from pydantic import ValidationError

from project.helpers.errors import AbstractError
from project.helpers.utils import load_from_yaml, LoadFromYamlError

from ..models import Config

logger = logging.getLogger(__name__)

ATTEMPT_MESSAGE = "loading config from yaml"
SUCCESS_MESSAGE = "successfully loaded config from yaml"
FAILURE_MESSAGE = "failed to load config from yaml"

class LoadConfigFromYamlError(AbstractError): pass

def load_config_from_yaml(path: str) -> Config:
  """
  ### **Description**

  This function will load the content of a `yaml` file and return it as `Config`.

  ---

  ### **Parameters**

  `path` :: `str` - the path of the `yaml` file

  ---

  ### **Returns**

  `Config` - the content of the `yaml` file

  ### **Throws**

  `LoadConfigFromYamlError`
  """
  logger.info(ATTEMPT_MESSAGE, extra={"path": path})
  try:
    content = load_from_yaml(path)
    config = Config(**content)
    internal_field_name_set = set(field.name for field in config.internal.fields)
    sources = config.external.sources
    for source_index in range(len(sources)):
      source = sources[source_index]
      external_field_name_set = set(field.target_name for field in source.fields)
      if internal_field_name_set != external_field_name_set:
        error = LoadConfigFromYamlError(FAILURE_MESSAGE, "internal field name and external field name sets do not match", path=path, source_index=source_index)
        logger.error(error.message, extra=error.kwargs)
        raise error
    logger.info(SUCCESS_MESSAGE, extra={"path": path})
    return config
  except LoadFromYamlError as err:
    error = LoadConfigFromYamlError(FAILURE_MESSAGE, cause=type(err).__name__, path=path)
    logger.error(error.message, extra=error.kwargs)
    raise error from err
  except ValidationError as err:
    error = LoadConfigFromYamlError(FAILURE_MESSAGE, cause=type(err).__name__, path=path, error_count=err.error_count())
    logger.error(error.message, extra=error.kwargs)
    raise error from err
  except Exception as err:
    error = LoadConfigFromYamlError(FAILURE_MESSAGE, cause=type(err).__name__, path=path)
    logger.error(error.message, extra=error.kwargs)
    raise error from err

__all__ = ["load_config_from_yaml", "LoadConfigFromYamlError"]
