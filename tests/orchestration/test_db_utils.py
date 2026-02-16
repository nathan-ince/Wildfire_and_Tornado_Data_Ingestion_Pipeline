import pytest
from uuid import uuid4
from datetime import datetime, timezone

import project.orchestration.db_utils as dbu
from project.orchestration.types import Status


class _FakeConnection:
    def __init__(self, should_raise: Exception | None = None):
        self.should_raise = should_raise
        self.calls = []  # (stmt, params)

    def execute(self, stmt, params):
        if self.should_raise:
            raise self.should_raise
        self.calls.append((stmt, params))


class _BeginCtx:
    def __init__(self, conn: _FakeConnection):
        self.conn = conn

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeEngine:
    def __init__(self, conn: _FakeConnection):
        self._conn = conn

    def begin(self):
        return _BeginCtx(self._conn)


def test_initialize_main_process_executes_statement(monkeypatch):
    monkeypatch.setattr(dbu, "INITIALIZE_MAIN_PROCESS", "INIT_MAIN_SQL")

    conn = _FakeConnection()
    engine = _FakeEngine(conn)
    monkeypatch.setattr(dbu, "get_engine", lambda: engine)

    main_id = uuid4()
    ts = datetime(2026, 2, 15, tzinfo=timezone.utc)

    dbu.initialize_main_process(main_id, ts)

    assert len(conn.calls) == 1
    stmt, params = conn.calls[0]
    assert stmt == "INIT_MAIN_SQL"
    assert params["id"] == main_id
    assert params["status"] == Status.Running.value
    assert params["start_timestamp"] == ts


def test_initialize_main_process_wraps_errors(monkeypatch):
    monkeypatch.setattr(dbu, "INITIALIZE_MAIN_PROCESS", "INIT_MAIN_SQL")

    conn = _FakeConnection(should_raise=RuntimeError("db down"))
    engine = _FakeEngine(conn)
    monkeypatch.setattr(dbu, "get_engine", lambda: engine)

    main_id = uuid4()
    ts = datetime(2026, 2, 15, tzinfo=timezone.utc)

    with pytest.raises(dbu.InitializeMainProcessError):
        dbu.initialize_main_process(main_id, ts)


def test_finalize_batch_process_executes_statement(monkeypatch):
    monkeypatch.setattr(dbu, "FINALIZE_BATCH_PROCESS", "FIN_BATCH_SQL")

    conn = _FakeConnection()
    engine = _FakeEngine(conn)
    monkeypatch.setattr(dbu, "get_engine", lambda: engine)

    batch_id = uuid4()
    ts = datetime(2026, 2, 15, tzinfo=timezone.utc)

    dbu.finalize_batch_process(batch_id, Status.Success, ts)

    assert len(conn.calls) == 1
    stmt, params = conn.calls[0]
    assert stmt == "FIN_BATCH_SQL"
    assert params["id"] == batch_id
    assert params["status"] == Status.Success.value
    assert params["final_timestamp"] == ts


def test_finalize_batch_process_wraps_errors(monkeypatch):
    monkeypatch.setattr(dbu, "FINALIZE_BATCH_PROCESS", "FIN_BATCH_SQL")

    conn = _FakeConnection(should_raise=ValueError("bad sql"))
    engine = _FakeEngine(conn)
    monkeypatch.setattr(dbu, "get_engine", lambda: engine)

    batch_id = uuid4()
    ts = datetime(2026, 2, 15, tzinfo=timezone.utc)

    with pytest.raises(dbu.FinalizeBatchProcessError):
        dbu.finalize_batch_process(batch_id, Status.Failure, ts)