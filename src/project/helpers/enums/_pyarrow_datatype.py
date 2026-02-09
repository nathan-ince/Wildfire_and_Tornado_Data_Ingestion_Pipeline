from ._abstract_string_enum import AbstractStringEnum

# this can be extended when needed
class PyArrowDataType(AbstractStringEnum):
  date32 = "date32[pyarrow]"
  int8 = "int8[pyarrow]"
  int16 = "int16[pyarrow]"
  int32 = "int32[pyarrow]"
  int64 = "int64[pyarrow]"
  string = "string[pyarrow]"
  uint8 = "uint8[pyarrow]"
  uint16 = "uint16[pyarrow]"
  uint32 = "uint32[pyarrow]"
  uint64 = "uint64[pyarrow]"
  float32 = "float32[pyarrow]"

__all__ = ["PyArrowDataType"]
