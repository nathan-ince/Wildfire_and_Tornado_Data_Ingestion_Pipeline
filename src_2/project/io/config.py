import logging
from pathlib import Path

from pydantic import ValidationError

from project.core.settings import REPO_ROOT
from project.helpers.errors import AbstractError
from project.helpers.yaml_reader import read_from_yaml, ReadFromYamlError
from project.models.config import Config

logger = logging.getLogger(__name__)

ATTEMPT_MESSAGE = "reading config from yaml"
SUCCESS_MESSAGE = "read config from yaml"
FAILURE_MESSAGE = "failed to read config from yaml"

class ReadConfigFromYamlError(AbstractError): pass

def read_config_from_yaml(path: str) -> Config:
  resolved_path = path
  try:
    p = Path(path)
    if not p.is_absolute():
      p = REPO_ROOT / p
    resolved_path = str(p)

    logger.info(ATTEMPT_MESSAGE, extra={"path": resolved_path})

    content = read_from_yaml(resolved_path)
    config = Config.model_validate(content)

    target_field_name_set = set(field.name for field in config.target.fields)
    sources = config.sources
    for source_index in range(len(sources)):
      source = sources[source_index]
      source_mapping_field_name_set = set(mapping[1].name for mapping in source.mapping.items())
      if source_mapping_field_name_set != target_field_name_set:
        error = ReadConfigFromYamlError(
          FAILURE_MESSAGE,
          reason="source mapping field name set and target field name set do not match",
          path=resolved_path,
          source_index=source_index,
        )
        logger.error(error.message, extra=error.kwargs)
        raise error

    logger.info(SUCCESS_MESSAGE, extra={"path": resolved_path})
    return config

  except ReadConfigFromYamlError:
    raise
  except ReadFromYamlError as err:
    error = ReadConfigFromYamlError(FAILURE_MESSAGE, cause=type(err).__name__, path=resolved_path)
    logger.error(error.message, extra=error.kwargs)
    raise error from err
  except ValidationError as err:
    error = ReadConfigFromYamlError(
      FAILURE_MESSAGE,
      cause=type(err).__name__,
      path=resolved_path,
      error_count=err.error_count(),
    )
    logger.error(error.message, extra=error.kwargs)
    raise error from err
  except Exception as err:
    error = ReadConfigFromYamlError(FAILURE_MESSAGE, cause=type(err).__name__, path=resolved_path)
    logger.error(error.message, extra=error.kwargs)
    raise error from err