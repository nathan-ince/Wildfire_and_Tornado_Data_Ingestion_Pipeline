import project.read.read_sql as read_sql
from types import SimpleNamespace
from sqlalchemy.sql.elements import TextClause

def test_read_sql_statement_returns_text_clause(tmp_path, monkeypatch):
    sql_dir = tmp_path / "sql"
    sql_dir.mkdir()
    (sql_dir / "test.sql").write_text("SELECT 1;")

    monkeypatch.setattr(read_sql, "get_settings", lambda: SimpleNamespace(sql_statements_path=str(sql_dir)))

    read_sql.read_sql_statement.cache_clear()
    result = read_sql.read_sql_statement("test.sql")

    assert isinstance(result, TextClause)
    assert str(result) == "SELECT 1;"