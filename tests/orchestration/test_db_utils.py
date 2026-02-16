import pytest
from uuid import uuid4
from datetime import datetime, timezone
from unittest.mock import MagicMock

import project.orchestration.db_utils as dbu
from project.orchestration.types import Status


@pytest.fixture
def mock_engine():
    engine = MagicMock()
    connection = MagicMock()

    # engine.begin() returns a context manager
    ctx = MagicMock()
    ctx.__enter__.return_value = connection
    ctx.__exit__.return_value = False
    engine.begin.return_value = ctx

    return engine, connection


def test_initialize_main_process_executes_statement(monkeypatch, mock_engine):
    engine, connection = mock_engine

    monkeypatch.setattr(dbu, "get_engine", MagicMock(return_value=engine))
    monkeypatch.setattr(dbu, "read_sql_statement", MagicMock(return_value="INIT_MAIN_SQL"))

    main_id = uuid4()
    ts = datetime(2026, 2, 15, tzinfo=timezone.utc)

    dbu.initialize_main_process(main_id, ts)

    connection.execute.assert_called_once()
    stmt, params = connection.execute.call_args[0]

    assert stmt == "INIT_MAIN_SQL"
    assert params["id"] == main_id
    assert params["status"] == Status.Running.value
    assert params["start_timestamp"] == ts


def test_initialize_main_process_wraps_errors(monkeypatch, mock_engine):
    engine, connection = mock_engine

    monkeypatch.setattr(dbu, "get_engine", MagicMock(return_value=engine))
    monkeypatch.setattr(dbu, "read_sql_statement", MagicMock(return_value="INIT_MAIN_SQL"))

    connection.execute.side_effect = RuntimeError("db down")

    main_id = uuid4()
    ts = datetime(2026, 2, 15, tzinfo=timezone.utc)

    with pytest.raises(dbu.InitializeMainProcessError):
        dbu.initialize_main_process(main_id, ts)


def test_finalize_batch_process_executes_statement(monkeypatch, mock_engine):
    engine, connection = mock_engine

    monkeypatch.setattr(dbu, "get_engine", MagicMock(return_value=engine))
    monkeypatch.setattr(dbu, "read_sql_statement", MagicMock(return_value="FIN_BATCH_SQL"))

    batch_id = uuid4()
    ts = datetime(2026, 2, 15, tzinfo=timezone.utc)

    dbu.finalize_batch_process(batch_id, Status.Success, ts)

    connection.execute.assert_called_once()
    stmt, params = connection.execute.call_args[0]

    assert stmt == "FIN_BATCH_SQL"
    assert params["id"] == batch_id
    assert params["status"] == Status.Success.value
    assert params["final_timestamp"] == ts


def test_finalize_batch_process_wraps_errors(monkeypatch, mock_engine):
    engine, connection = mock_engine

    monkeypatch.setattr(dbu, "get_engine", MagicMock(return_value=engine))
    monkeypatch.setattr(dbu, "read_sql_statement", MagicMock(return_value="FIN_BATCH_SQL"))

    connection.execute.side_effect = ValueError("bad sql")

    batch_id = uuid4()
    ts = datetime(2026, 2, 15, tzinfo=timezone.utc)

    with pytest.raises(dbu.FinalizeBatchProcessError):
        dbu.finalize_batch_process(batch_id, Status.Failure, ts)