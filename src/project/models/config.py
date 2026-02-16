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
  name: str
  version: str
  target: Target
  class Target(BaseModel):
    tables: Tables
    merge_accepted: str
    merge_rejected: str
    class Tables(BaseModel):
      accepted_final: str
      accepted_stage: str
      rejected_final: str
      rejected_stage: str
    fields: list[Field]
    class Field(BaseModel):
      name: str
      type: str
      nullable: bool = False
      unique: bool = False
  sources: list[SourceCSV | SourceJSON]
