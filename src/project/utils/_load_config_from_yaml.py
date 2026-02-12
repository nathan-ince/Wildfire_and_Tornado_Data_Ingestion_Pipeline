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
    config = Config.model_validate(content)
    target_field_name_set = set(field.name for field in config.target.fields)
    sources = config.sources
    for source_index in range(len(sources)):
      source = sources[source_index]
      source_mapping_field_name_set = set(mapping[1].name for mapping in source.mapping.items())
      if source_mapping_field_name_set != target_field_name_set:
        error = LoadConfigFromYamlError(FAILURE_MESSAGE, reason="source mapping field name set and target field name set do not match", path=path, source_index=source_index)
        logger.error(error.message, extra=error.kwargs)
        raise error
    logger.info(SUCCESS_MESSAGE, extra={"path": path})
    return config
  except LoadConfigFromYamlError: raise
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
