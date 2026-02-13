# from functools import lru_cache
from pathlib import Path
from sqlalchemy import text

# @lru_cache
def load_sql_from_file(filename: str):
  path = Path("sql/statements") / Path(filename)
  return text(path.read_text())

__all__ = ["load_sql_from_file"]
