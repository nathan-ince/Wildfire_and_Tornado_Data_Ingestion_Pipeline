from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Annotated
from functools import lru_cache

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

@lru_cache
def get_settings() -> Settings:
    return Settings.model_validate({})
