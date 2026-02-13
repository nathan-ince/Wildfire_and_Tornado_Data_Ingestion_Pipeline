import logging
import yaml

from ..errors import AbstractError

logger = logging.getLogger(__name__)

ATTEMPT_MESSAGE = "loading content from yaml"
SUCCESS_MESSAGE = "loaded content from yaml"
FAILURE_MESSAGE = "failed to load content from yaml"

class LoadFromYamlError(AbstractError): pass

def load_from_yaml(path: str, log: bool = False):
  """
  ### **Description**

  This function will load the content of a `yaml` file and return it as `Any`.

  ---

  ### **Parameters**

  `path` :: `str` - the path of the `yaml` file

  ---

  ### **Returns**

  `Any` - the content of the `yaml` file

  ### **Throws**

  `LoadFromYamlError`
  """
  if log: logger.info(ATTEMPT_MESSAGE, extra={"path": path})
  try:
    with open(path, mode="r") as file: content = yaml.safe_load(file)
    if log: logger.info(SUCCESS_MESSAGE, extra={"path": path})
    return content
  except FileNotFoundError as err:
    error = LoadFromYamlError(FAILURE_MESSAGE, cause=type(err).__name__, path=path)
    if log: logger.error(error.message, extra=error.kwargs)
    raise error from err
  except Exception as err:
    error = LoadFromYamlError(FAILURE_MESSAGE, cause=type(err).__name__, path=path)
    if log: logger.error(error.message, extra=error.kwargs)
    raise error from err

__all__ = ["load_from_yaml", "LoadFromYamlError"]
