import project.core.log_config as log_config
from unittest.mock import MagicMock

def test_configure_logging(monkeypatch, tmp_path):
    fake_settings = MagicMock()
    fake_settings.log_directory_path = tmp_path
    fake_settings.app_log_file_name = "app.log"
    fake_settings.tests_log_file_name = "tests.log"

    monkeypatch.setattr(log_config, "get_settings", lambda: fake_settings)

    log_config.configure_logging()