################################################################################################

import logging

from pandas import DataFrame

################################################################################################

from project.errors.abstract import AbstractError
from project.models import PipelineConfigurationSettings as Config

from ..constants import CONFIG_FILE_PATH

################################################################################################

logger = logging.getLogger(__name__)

################################################################################################

class FieldNameConfigurationError(AbstractError): pass

################################################################################################

def validate_field_name_configuration(
  data: DataFrame,
  config: Config,
  source_index: int
):
  """
  ### **Throws**

  `FieldNameConfigurationError`
  """
  try:
    source = config.external.sources[source_index]
    internal_field_set = set(config.internal.table.fields.list)
    external_field_map = source.table.fields.map
    for external_field in list(data.columns):
      if external_field not in external_field_map:
        logger.warning("invalid field configuration")
        exception = FieldNameConfigurationError("external configuration error :: an external field could not be resolved to a key in the external field map")
        logger.error(exception.message)
        logger.debug("pipeline name = %s", config.name)
        logger.debug("config file path = %s", CONFIG_FILE_PATH)
        logger.debug("source index = %s", source_index)
        logger.debug("source format = %s", source.format.value)
        logger.debug("source path = %s", source.path)
        raise exception
      if external_field_map[external_field] not in internal_field_set:
        logger.warning("invalid field configuration")
        exception = FieldNameConfigurationError("internal configuration error :: a key in the external field map could not be found in the internal field set")
        logger.error(exception.message)
        logger.debug("pipeline name = %s", config.name)
        logger.debug("config file path = %s", CONFIG_FILE_PATH)
        logger.debug("source index = %s", source_index)
        logger.debug("source format = %s", source.format.value)
        logger.debug("source path = %s", source.path)
        raise exception
  except FieldNameConfigurationError: raise
  except Exception as e:
    exception = FieldNameConfigurationError("unknown error", f"name = {type(e).__name__}")
    logger.error(exception.message)
    raise exception from e

################################################################################################

__all__ = ["validate_field_name_configuration", "FieldNameConfigurationError"]

################################################################################################
