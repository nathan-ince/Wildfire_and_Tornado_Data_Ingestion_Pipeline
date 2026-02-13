from functools import lru_cache
from pathlib import Path
from sqlalchemy import text

from project.core import settings

@lru_cache
def load_stmt_from_sql(filename: str):
  path = Path(settings.sql_statements_path) / Path(filename)
  return text(path.read_text())

__all__ = ["load_stmt_from_sql"]
