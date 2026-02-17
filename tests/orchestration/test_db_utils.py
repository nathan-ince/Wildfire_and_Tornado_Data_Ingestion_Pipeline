import pytest
from uuid import uuid4
from datetime import datetime, timezone
from unittest.mock import MagicMock

import project.orchestration.db_utils as dbu
from project.orchestration.types import Status


@pytest.fixture
def fake_db(monkeypatch):
    connection = MagicMock()

    engine = MagicMock()
    engine.begin.return_value.__enter__.return_value = connection
    engine.begin.return_value.__exit__.return_value = False

    monkeypatch.setattr(dbu, "get_engine", lambda: engine)
    monkeypatch.setattr(dbu, "read_sql_statement", lambda filename: "SQL_TEXT")

    return connection


def test_initialize_main_process(fake_db):
    main_id = uuid4()
    ts = datetime(2026, 2, 15, tzinfo=timezone.utc)
    name = "tornado_usa"

    dbu.initialize_main_process(name, main_id, ts)

    stmt, params = fake_db.execute.call_args[0]
    assert stmt == "SQL_TEXT"
    assert params["id"] == main_id
    assert params["name"] == name
    assert params["status"] == Status.Running.value
    assert params["start_timestamp"] == ts


def test_initialize_main_process_error(fake_db):
    fake_db.execute.side_effect = RuntimeError("db down")

    main_id = uuid4()
    ts = datetime(2026, 2, 15, tzinfo=timezone.utc)

    with pytest.raises(dbu.InitializeMainProcessError):
        dbu.initialize_main_process("tornado_usa", main_id, ts)