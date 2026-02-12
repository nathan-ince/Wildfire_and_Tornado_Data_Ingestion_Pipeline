import logging

from typing import Literal

from pydantic.main import BaseModel

logger = logging.getLogger(__name__)

class SourceField(BaseModel):
  name: str
  type: str

class SourceBase(BaseModel):
  name: str
  path: str
  mapping: dict[str, SourceField]

class SourceCSV(SourceBase):
  format: Literal["csv"]
  options: CsvOptions
  class CsvOptions(BaseModel):
    delimiter: str

class SourceJSON(SourceBase):
  format: Literal["json"]
  options: None = None

Source = SourceCSV | SourceJSON

class Config(BaseModel):
  version: str
  target: Target
  class Target(BaseModel):
    tables: Tables
    class Tables(BaseModel):
      accepted: str
      rejected: str
    fields: list[Field]
    class Field(BaseModel):
      name: str
      type: str
      nullable: bool = False
      unique: bool = False
  sources: list[SourceCSV | SourceJSON]

__all__ = ["Config", "Source"]
