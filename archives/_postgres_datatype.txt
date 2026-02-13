from ._abstract_string_enum import AbstractStringEnum

# this can be extended when needed
class PostgresDataType(AbstractStringEnum):
  bigint = "bigint"
  date = "date"
  double_precision = "double precision"
  integer = "integer"
  real = "real"
  smallint = "smallint"
  text = "text"

__all__ = ["PostgresDataType"]
