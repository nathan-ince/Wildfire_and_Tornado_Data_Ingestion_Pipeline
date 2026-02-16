import project.core.log_config as log_config
from unittest.mock import MagicMock

def test_configure_logging(monkeypatch, tmp_path):
    settings = MagicMock()
    settings.log_directory_path = tmp_path
    settings.app_log_file_name = "app.log"
    settings.tests_log_file_name = "tests.log"

    monkeypatch.setattr(log_config, "get_settings", MagicMock(return_value=settings))

    log_config.configure_logging()