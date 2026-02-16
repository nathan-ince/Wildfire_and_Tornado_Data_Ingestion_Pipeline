from functools import lru_cache
from pathlib import Path
from sqlalchemy import text

from project.core.settings import get_settings

@lru_cache
def read_sql_statement(filename: str):
  settings = get_settings()
  path = Path(settings.sql_statements_path) / Path(filename)
  return text(path.read_text())