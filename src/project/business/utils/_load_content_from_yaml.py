import logging
import yaml

from project.helpers.errors import AbstractError

logger = logging.getLogger(__name__)

ATTEMPT_MESSAGE = "loading content from yaml"
SUCCESS_MESSAGE = "successfully loaded content from yaml"
FAILURE_MESSAGE = "failed to load content from yaml"

class LoadContentFromYamlError(AbstractError): pass

def load_content_from_yaml(path: str):
  """
  ### **Description**

  This function will load the content of a `yaml` file and return it.

  ---

  ### **Parameters**

  `path` :: `str` - the path of the `yaml` file

  ---

  ### **Throws**

  `LoadContentFromYamlError`
  """
  try:
    logger.info(ATTEMPT_MESSAGE, extra={"path": path})
    with open(path, mode="r") as file: content = yaml.safe_load(file)
    logger.info(SUCCESS_MESSAGE, extra={"path": path})
    return content
  except FileNotFoundError as e:
    error = LoadContentFromYamlError(FAILURE_MESSAGE, "file not found", path=path)
    logger.error(error.message, extra=error.kwargs)
    raise error from e
  except Exception as e:
    error = LoadContentFromYamlError(FAILURE_MESSAGE, path=path, error_name=type(e).__name__)
    logger.error(error.message, extra=error.kwargs)
    raise error from e

__all__ = ["load_content_from_yaml", "LoadContentFromYamlError"]
