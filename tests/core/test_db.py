from unittest.mock import MagicMock
from project.core import db

def test_build_engine(monkeypatch):
    mock_create_engine = MagicMock()
    monkeypatch.setattr(db, "create_engine", mock_create_engine)

    db.build_engine()

    mock_create_engine.assert_called_once()