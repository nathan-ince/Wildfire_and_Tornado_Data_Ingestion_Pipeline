def check_is_type(source_value, target_type: type):
  return type(source_value) is target_type

def check_in_types(source_value, target_types: tuple[type, ...]):
  return type(source_value) in target_types

def check_is_instance_of(source_value, target_types: type | tuple[type, ...]):
  return isinstance(source_value, target_types)

__all__ = [
  "check_is_type",
  "check_in_types",
  "check_is_instance_of"
]
