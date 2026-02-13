import logging

from typing import Any, TypeIs, TypeVar

from ..errors import AbstractError

logger = logging.getLogger(__name__)

E = TypeVar("E")

def verify_list(
  entity,
  entity_name: str | None = None,
  track_entity_name: bool = False,
  track_entity_value: bool = True,
  track_entity_source_type: bool = True,
  track_entity_target_type: bool = True,
  verify_elements: bool = False,
  elements_target_type: type[E] | tuple[type[E], ...] | None = None,
  track_element_value: bool = True,
  track_element_source_type: bool = True,
  track_element_target_type: bool = True,
  extra_keyword_arguments: dict[str, Any] | None = None,
  log_error: bool = True
) -> TypeIs[list[E]]:
  if not isinstance(entity, list):
    kwargs = {}
    if track_entity_name: kwargs["entity_name"] = entity_name
    if track_entity_source_type: kwargs["entity_source_type"] = type(entity).__name__
    if track_entity_target_type: kwargs["entity_target_type"] = list.__name__
    if extra_keyword_arguments: kwargs.update(extra_keyword_arguments)
    error = AbstractError("failed to verify list", "entity type is invalid", **kwargs)
    if log_error: logger.error(error.message, extra=error.kwargs)
    raise error
  if verify_elements:
    if elements_target_type is None:
      kwargs = {}
      if track_entity_name: kwargs["entity_name"] = entity_name
      if track_entity_value: kwargs["entity_value"] = entity
      if extra_keyword_arguments: kwargs.update(extra_keyword_arguments)
      error = AbstractError("failed to verify list", "verify_elements is True but elements_target_type is None", **kwargs)
      if log_error: logger.error(error.message, extra=error.kwargs)
      raise error
    for element in entity:
      if not isinstance(element, elements_target_type):
        kwargs = {}
        if track_entity_name: kwargs["entity_name"] = entity_name
        if track_entity_value: kwargs["entity_value"] = entity
        if track_element_value: kwargs["element_value"] = element
        if track_element_source_type: kwargs["element_source_type"] = type(element).__name__
        if track_element_target_type:
          if isinstance(elements_target_type, type): kwargs["element_target_type"] = elements_target_type.__name__
          else: kwargs["element_target_type"] = tuple(ttype.__name__ for ttype in elements_target_type)
        if extra_keyword_arguments: kwargs.update(extra_keyword_arguments)
        error = AbstractError("failed to verify list", "element type is invalid", **kwargs)
        if log_error: logger.error(error.message, extra=error.kwargs)
        raise error
  return True

__all__ = ["verify_list"]
