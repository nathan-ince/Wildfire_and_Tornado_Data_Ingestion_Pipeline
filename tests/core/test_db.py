from unittest.mock import MagicMock
from project.core import db

def test_build_engine(monkeypatch):
    fake_settings = MagicMock()
    fake_settings.db_host = "localhost"
    fake_settings.db_port = "5432"
    fake_settings.db_name = "mydb"
    fake_settings.db_username = "user"
    fake_settings.db_password = "pass"

    monkeypatch.setattr(db, "get_settings", lambda: fake_settings)

    mock_engine = MagicMock()
    monkeypatch.setattr(db, "create_engine", mock_engine)

    db.build_engine()

    assert mock_engine.call_count == 1