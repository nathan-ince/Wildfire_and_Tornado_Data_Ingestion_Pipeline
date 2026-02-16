import project.core.log_config as log_config

def test_configure_logging(monkeypatch, tmp_path):

    class FakeSettings:
        log_directory_path = tmp_path
        app_log_file_name = "app.log"
        tests_log_file_name = "tests.log"

    monkeypatch.setattr(log_config, "get_settings", lambda: FakeSettings())

    log_config.configure_logging()