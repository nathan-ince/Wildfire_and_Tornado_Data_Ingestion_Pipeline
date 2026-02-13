import sys

from pathlib import Path
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated

class Settings(BaseSettings):
  db_host: Annotated[str, Field(alias="DB_HOST")]
  db_port: Annotated[str, Field(alias="DB_PORT")]
  db_name: Annotated[str, Field(alias="DB_NAME")]
  db_username: Annotated[str, Field(alias="DB_USERNAME")]
  db_password: Annotated[str, Field(alias="DB_PASSWORD")]
  sql_statements_path: Annotated[str, Field(alias="SQL_STATEMENTS_PATH")]
  log_directory_path: Annotated[Path, Field(alias="LOG_DIRECTORY_PATH")]
  app_log_file_name: Annotated[str, Field(alias="APP_LOG_FILE_NAME")]
  tests_log_file_name: Annotated[str, Field(alias="TESTS_LOG_FILE_NAME")]

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    env_ignore_empty=True,
    case_sensitive=True,
    extra="ignore",
  )

try:
  settings = Settings.model_validate({})
except ValidationError as exception:
  print("Error Processing Environment")
  for error in exception.errors():
    print(f"[{error['loc']}] [{error['msg']}]")
  sys.exit(1)
except Exception as exception:
  print("Error Processing Environment", exception, sep="\n")
  sys.exit(1)

__all__ = ["settings"]
