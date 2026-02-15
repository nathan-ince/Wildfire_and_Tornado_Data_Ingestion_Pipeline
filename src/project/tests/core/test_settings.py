import pytest
from pydantic import ValidationError
from pathlib import Path
import project.core.settings as settings_module

def test_load_settings_success(monkeypatch, tmp_path):
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "mydb")
    monkeypatch.setenv("DB_USERNAME", "user")
    monkeypatch.setenv("DB_PASSWORD", "pass")
    monkeypatch.setenv("SQL_STATEMENTS_PATH", str(tmp_path / "sql"))
    monkeypatch.setenv("LOG_DIRECTORY_PATH", str(tmp_path / "logs"))
    monkeypatch.setenv("APP_LOG_FILE_NAME", "app.log")
    monkeypatch.setenv("TESTS_LOG_FILE_NAME", "tests.log")

    s = settings_module.get_settings()

    assert s.db_host == "localhost"
    assert s.log_directory_path == Path(tmp_path / "logs")
    assert s.app_log_file_name == "app.log"


def test_load_settings_failed(monkeypatch):
    for key in [
        "DB_HOST","DB_PORT","DB_NAME","DB_USERNAME","DB_PASSWORD",
        "SQL_STATEMENTS_PATH","LOG_DIRECTORY_PATH","APP_LOG_FILE_NAME","TESTS_LOG_FILE_NAME",
    ]:
        monkeypatch.delenv(key, raising=False)

    with pytest.raises(ValidationError):
        settings_module.load_settings()