import project.read.read_sql as read_sql
from unittest.mock import MagicMock
from sqlalchemy.sql.elements import TextClause


def test_read_sql_statement(tmp_path, monkeypatch):
    sql_dir = tmp_path / "sql"
    sql_dir.mkdir()
    (sql_dir / "test.sql").write_text("SELECT 1;")

    fake_settings = MagicMock()
    fake_settings.sql_statements_path = sql_dir

    monkeypatch.setattr(read_sql, "get_settings", lambda: fake_settings)
    read_sql.read_sql_statement.cache_clear()

    result = read_sql.read_sql_statement("test.sql")

    assert isinstance(result, TextClause)
    assert str(result) == "SELECT 1;"