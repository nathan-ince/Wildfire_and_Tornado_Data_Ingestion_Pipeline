from pydantic import BaseModel
from ._abstract_enums import AbstractStringEnum

class Config(BaseModel):
  accepted: str
  rejected: str
  sources: list[Source]
  class Source(BaseModel):
    path: str
    format: Format
    class Format(AbstractStringEnum):
      CSV = "csv"
      JSON = "json"
    columns: dict[str, str]

__all__ = ["Config"]
