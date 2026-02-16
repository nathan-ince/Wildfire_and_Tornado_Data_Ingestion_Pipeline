import pytest
from pathlib import Path
from pydantic import ValidationError
import project.core.settings as settings_module


def set_env(monkeypatch, tmp_path):
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "mydb")
    monkeypatch.setenv("DB_USERNAME", "user")
    monkeypatch.setenv("DB_PASSWORD", "pass")
    monkeypatch.setenv("SQL_STATEMENTS_PATH", str(tmp_path / "sql"))
    monkeypatch.setenv("LOG_DIRECTORY_PATH", str(tmp_path / "logs"))
    monkeypatch.setenv("APP_LOG_FILE_NAME", "app.log")
    monkeypatch.setenv("TESTS_LOG_FILE_NAME", "tests.log")


def test_get_settings_valid(monkeypatch, tmp_path):
    set_env(monkeypatch, tmp_path)
    settings_module.get_settings.cache_clear()

    s = settings_module.get_settings()

    assert s.db_host == "localhost"
    assert s.db_port == "5432"
    assert s.log_directory_path == Path(tmp_path / "logs")
    assert s.app_log_file_name == "app.log"


def test_get_settings_invalid_missing_required(monkeypatch, tmp_path):
    set_env(monkeypatch, tmp_path)
    monkeypatch.delenv("DB_HOST")
    settings_module.get_settings.cache_clear()

    with pytest.raises(ValidationError):
        settings_module.get_settings()