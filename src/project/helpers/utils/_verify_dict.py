import logging

from typing import Any, TypeIs, TypeVar

from ..errors import AbstractError

logger = logging.getLogger(__name__)

K = TypeVar("K")
V = TypeVar("V")

def verify_dict(
  entity,
  entity_name: str | None = None,
  track_entity_name: bool = False,
  track_entity_value: bool = True,
  track_entity_source_type: bool = True,
  track_entity_target_type: bool = True,
  verify_dict_keys: bool = False,
  verify_dict_cells: bool = False,
  dict_keys_target_type: type[K] | tuple[type[K], ...] | None = None,
  dict_cells_target_type: type[V] | tuple[type[V], ...] | None = None,
  track_dict_key: bool = True,
  track_dict_key_source_type: bool = True,
  track_dict_key_target_type: bool = True,
  track_dict_cell: bool = True,
  track_dict_cell_source_type: bool = True,
  track_dict_cell_target_type: bool = True,
  extra_mapped_arguments: dict[str, Any] | None = None,
  log_error: bool = True
) -> TypeIs[dict[K, V]]:
  if not isinstance(entity, dict):
    kwargs = {}
    if track_entity_name: kwargs["entity_name"] = entity_name
    if track_entity_source_type: kwargs["entity_source_type"] = type(entity).__name__
    if track_entity_target_type: kwargs["entity_target_type"] = dict.__name__
    if extra_mapped_arguments: kwargs.update(extra_mapped_arguments)
    error = AbstractError("failed to verify entity", "entity type is invalid", **kwargs)
    if log_error: logger.error(error.message, extra=error.kwargs)
    raise error
  if verify_dict_keys:
    if dict_keys_target_type is None:
      kwargs = {}
      if track_entity_name: kwargs["entity_name"] = entity_name
      if track_entity_value: kwargs["entity_value"] = entity
      error = AbstractError("failed to verify dict", "verify_dict_keys is True but dict_keys_target_type is None", **kwargs)
      if log_error: logger.error(error.message, extra=error.kwargs)
      raise error
    for key in entity.keys():
      if not isinstance(key, dict_keys_target_type):
        kwargs = {}
        if track_entity_name: kwargs["entity_name"] = entity_name
        if track_entity_value: kwargs["entity_value"] = entity
        if track_dict_key: kwargs["dict_key"] = key
        if track_dict_key_source_type: kwargs["dict_key_source_type"] = type(key).__name__
        if track_dict_key_target_type:
          if isinstance(dict_keys_target_type, type): kwargs["dict_key_target_type"] = dict_keys_target_type.__name__
          else: kwargs["dict_key_target_type"] = tuple(ttype.__name__ for ttype in dict_keys_target_type)
        if extra_mapped_arguments: kwargs.update(extra_mapped_arguments)
        error = AbstractError("failed to verify dict", "dict key type is invalid", **kwargs)
        if log_error: logger.error(error.message, extra=error.kwargs)
        raise error
  if verify_dict_cells:
    if dict_cells_target_type is None:
      kwargs = {}
      if track_entity_name: kwargs["entity_name"] = entity_name
      if track_entity_value: kwargs["entity_value"] = entity
      error = AbstractError("failed to verify dict", "verify_dict_cells is True but dict_cells_target_type is None", **kwargs)
      if log_error: logger.error(error.message, extra=error.kwargs)
      raise error
    for cell in entity.values():
      if not isinstance(cell, dict_cells_target_type):
        kwargs = {}
        if track_entity_name: kwargs["entity_name"] = entity_name
        if track_entity_value: kwargs["entity_value"] = entity
        if track_dict_cell: kwargs["dict_cell"] = cell
        if track_dict_cell_source_type: kwargs["dict_cell_source_type"] = type(cell).__name__
        if track_dict_cell_target_type:
          if isinstance(dict_cells_target_type, type): kwargs["dict_cell_target_type"] = dict_cells_target_type.__name__
          else: kwargs["dict_cell_target_type"] = tuple(ttype.__name__ for ttype in dict_cells_target_type)
        if extra_mapped_arguments: kwargs.update(extra_mapped_arguments)
        error = AbstractError("failed to verify dict", "dict cell type is invalid", **kwargs)
        if log_error: logger.error(error.message, extra=error.kwargs)
        raise error
  return True

__all__ = ["verify_dict"]
