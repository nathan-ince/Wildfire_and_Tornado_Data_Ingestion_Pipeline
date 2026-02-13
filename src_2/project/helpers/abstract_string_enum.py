import logging

from typing import Any, Self

from project.helpers.errors import AbstractError

from project.helpers.abstract_enum import AbstractEnum

logger = logging.getLogger(__name__)

class AbstractStringEnum(str, AbstractEnum):

  @classmethod
  def get_value_tuple(cls) -> tuple[str, ...]:
    return tuple(x.value for x in cls)
  
  @classmethod
  def get_value_set(cls) -> set[str]:
    return set(x.value for x in cls)
  
  @classmethod
  def define(
    cls,
    entity,
    entity_name: str | None = None,
    track_class_name: bool = True,
    track_entity_name: bool = False,
    track_entity_value: bool = True,
    track_entity_source_type: bool = True,
    track_entity_target_type: bool = True,
    track_valid_values: bool = True,
    extra_kwargs: dict[str, Any] | None = None,
    log_error: bool = True
  ) -> Self:
    if not isinstance(entity, str):
      kwargs = {}
      if track_class_name: kwargs["class_name"] = cls.__name__
      if track_entity_name: kwargs["entity_name"] = entity_name
      if track_entity_source_type: kwargs["entity_source_type"] = type(entity).__name__
      if track_entity_target_type: kwargs["entity_target_type"] = str.__name__
      if extra_kwargs: kwargs.update(extra_kwargs)
      error = AbstractError("failed to define entity as class", "entity type is invalid", **kwargs)
      if log_error: logger.error(error.message, extra=error.kwargs)
      raise error
    if not entity in cls.get_value_set():
      kwargs = {}
      if track_class_name: kwargs["class_name"] = cls.__name__
      if track_entity_name: kwargs["entity_name"] = entity_name
      if track_entity_value: kwargs["entity_value"] = entity
      if track_valid_values: kwargs["valid_values"] = cls.get_value_set()
      if extra_kwargs: kwargs.update(extra_kwargs)
      error = AbstractError("failed to define entity as class", "entity value is invalid", **kwargs)
      if log_error: logger.error(error.message, extra=error.kwargs)
      raise error
    return cls(entity)

__all__ = ["AbstractStringEnum"]
