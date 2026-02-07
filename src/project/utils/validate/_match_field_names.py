import logging

from pandas import DataFrame

from project.errors import AbstractError

logger = logging.getLogger(__name__)

class InvalidFieldNameListError(AbstractError): pass

def match_field_names(
  data: DataFrame,
  internal_field_name_set: set[str],
  external_field_name_map: dict[str, str]
):
  """
  ### **Throws**

  `InvalidFieldNameListError`
  """
  invalid_external_field_name_list: list[str] = list()
  invalid_internal_field_name_list: list[str] = list()
  for external_field_name in list(data.columns):
    if external_field_name not in external_field_name_map:
      logger.warning("a field name from the extracted data could not be resolved to a key in the external field name map", extra={"external_field_name": external_field_name})
      invalid_external_field_name_list.append(external_field_name)
  if len(invalid_external_field_name_list) > 0:
    error = InvalidFieldNameListError("invalid external field names")
    logger.error(error.message, extra={"invalid_external_field_name_list": invalid_external_field_name_list})
    raise error
  for exteral_field_name in list(data.columns):
    if external_field_name_map[exteral_field_name] not in internal_field_name_set:
      logger.warning("a key in the external field name map could not be found in the internal field name set")
      invalid_internal_field_name_list.append(exteral_field_name)
  if len(invalid_internal_field_name_list) > 0:
    error = InvalidFieldNameListError("invalid internal field names")
    logger.error(error.message, extra={"invalid_internal_field_name_list": invalid_internal_field_name_list})
    raise error

__all__ = ["match_field_names"]
