import logging

from pydantic.main import BaseModel

from project.helpers.enums import AbstractStringEnum, PostgresDataType, PyArrowDataType

logger = logging.getLogger(__name__)

class Config(BaseModel):
  internal: Internal
  class Internal(BaseModel):
    tables: Tables
    class Tables(BaseModel):
      accepted: str
      rejected: str
    fields: list[Field]
    class Field(BaseModel):
      name: str
      ptype: PostgresDataType
      dtype: PyArrowDataType
      nullable: bool
      unique: bool
  external: External
  class External(BaseModel):
    sources: list[Source]
    class Source(BaseModel):
      path: str
      format: Format
      class Format(AbstractStringEnum):
        CSV = "csv"
        JSON = "json"
      fields: list[Field]
      class Field(BaseModel):
        source_name: str
        source_dtype: PyArrowDataType
        target_name: str

__all__ = ["Config"]
