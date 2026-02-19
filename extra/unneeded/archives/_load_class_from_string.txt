################################################################################################

import logging

from importlib import import_module

################################################################################################

logger = logging.getLogger(__name__)

################################################################################################

def load_class_from_string(path: str) -> type:
  """
  ### **Description**

  This function will attemtpt to load a class from a string.

  ---

  ### **Parameters**

  `path` :: `str` - the path of the class to be loaded
  
    - should be separated with dots, so it should have a format that resembles `module.module.module.class`

  ---

  ### **Returns**

  `type` - the class

  ---

  ### **Splits**

  `module_name` - the first part of the path (everything before the last dot)

  `class_name` - the last part of the path (everything after the last dot)

  ---

  ### **Throws**

  `ImportError` - if the module `module_name` cannot be imported

  `AttributeError` - if the module `module_name` was imported but the attribute `class_name` does not exist in the module

  `TypeError` - if the module `module_name` was imported and the attribute `class_name` exists in the module but is not a class
  
  """
  module_name, class_name = path.rsplit(".", 1)
  try:
    module = import_module(module_name)
  except ImportError as e:
    logger.error("Error importing module %s derived from path %s", module_name, path)
    raise ImportError(f"Cannot load class from path {path}") from e
  try:
    clazz = getattr(module, class_name)
  except AttributeError as e:
    logger.error("Error getting class %s from module %s", class_name, module_name)
    raise AttributeError(f"Cannot load class from path {path}") from e
  if not isinstance(clazz, type):
    logger.error("attribute %s from module %s is not a class", class_name, module_name)
    raise TypeError(f"Cannot load class from path {path}")
  return clazz

################################################################################################

__all__ = ["load_class_from_string"]

################################################################################################
