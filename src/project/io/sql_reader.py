from functools import lru_cache
from pathlib import Path
from sqlalchemy import text

from project.core import settings

@lru_cache
def read_sql_statement(filename: str):
  path = Path(settings.sql_statements_path) / Path(filename)
  return text(path.read_text())


# @lru_cache
# def read_sql_statement(filename: str):
#   base = Path(settings.sql_statements_path)

#   # make relative paths relative to repo root (not current working dir)
#   if not base.is_absolute():
#     base = REPO_ROOT / base

#   path = base / filename
#   return text(path.read_text(encoding="utf-8"))
