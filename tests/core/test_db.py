from unittest.mock import MagicMock
from project.core import db

def test_build_engine(monkeypatch):
    fake_settings = MagicMock()
    fake_settings.db_host = "localhost"
    fake_settings.db_port = "5432"
    fake_settings.db_name = "mydb"
    fake_settings.db_username = "user"
    fake_settings.db_password = "pass"

    monkeypatch.setattr(db, "get_settings", MagicMock(return_value=fake_settings))
    monkeypatch.setattr(db, "create_engine", MagicMock())

    db.build_engine()

    db.create_engine.assert_called_once()