import project.core.log_config as log_config

def test_configure_logging_does_not_crash(monkeypatch, tmp_path):

    class FakeSettings:
        log_directory_path = tmp_path
        app_log_file_name = "app.log"

    monkeypatch.setattr(log_config, "settings", FakeSettings)

    log_config.configure_logging()