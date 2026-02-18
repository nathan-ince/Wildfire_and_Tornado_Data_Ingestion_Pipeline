import logging

from typing import Any, TypeIs, TypeVar

from ..errors import AbstractError

logger = logging.getLogger(__name__)

T = TypeVar("T")

def verify_is_instance_of(
  entity,
  target_types: type[T] | tuple[type[T], ...],
  entity_name: str | None = None,
  track_entity_name: bool = False,
  track_entity_value: bool = True,
  track_entity_source_type: bool = True,
  track_entity_target_type: bool = True,
  extra_mapped_arguments: dict[str, Any] | None = None,
  log_error: bool = True
) -> TypeIs[T]:
  if isinstance(entity, target_types): return True
  kwargs = {}
  if track_entity_name: kwargs["entity_name"] = entity_name
  if track_entity_value: kwargs["entity_value"] = entity
  if track_entity_source_type: kwargs["entity_source_type"] = type(entity).__name__
  if track_entity_target_type:
    if isinstance(target_types, type): kwargs["entity_target_type"] = target_types.__name__
    else: kwargs["entity_target_type"] = tuple(ttype.__name__ for ttype in target_types)
  if extra_mapped_arguments: kwargs.update(extra_mapped_arguments)
  error = AbstractError("failed to verify entity", "entity type is invalid", **kwargs)
  if log_error: logger.error(error.message, extra=error.kwargs)
  raise error

__all__ = ["verify_is_instance_of"]
