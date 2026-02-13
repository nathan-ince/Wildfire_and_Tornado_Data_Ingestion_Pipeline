import logging
import yaml

from project.helpers.errors import AbstractError

logger = logging.getLogger(__name__)

ATTEMPT_MESSAGE = "reading content from yaml"
SUCCESS_MESSAGE = "read content from yaml"
FAILURE_MESSAGE = "failed to read content from yaml"

class ReadFromYamlError(AbstractError): pass

def read_from_yaml(path: str, log: bool = False):
  if log: logger.info(ATTEMPT_MESSAGE, extra={"path": path})
  try:
    with open(path, mode="r") as file: content = yaml.safe_load(file)
    if log: logger.info(SUCCESS_MESSAGE, extra={"path": path})
    return content
  except FileNotFoundError as err:
    error = ReadFromYamlError(FAILURE_MESSAGE, cause=type(err).__name__, path=path)
    if log: logger.error(error.message, extra=error.kwargs)
    raise error from err
  except Exception as err:
    error = ReadFromYamlError(FAILURE_MESSAGE, cause=type(err).__name__, path=path)
    if log: logger.error(error.message, extra=error.kwargs)
    raise error from err
