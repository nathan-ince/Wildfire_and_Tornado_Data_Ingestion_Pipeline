import pandas as pd
from unittest.mock import MagicMock
from project.load import postgres_loader


class DummyConfig:
    class Target:
        class Tables:
            accepted = "accepted_table"
            rejected = "rejected_table"
        tables = Tables()
    target = Target()


def test_load_to_postgres_valid(monkeypatch):
    monkeypatch.setattr(postgres_loader, "get_engine", MagicMock(return_value=MagicMock()))

    calls = []

    def fake_to_sql(self, *, name, con, if_exists, index):
        calls.append(name)

    monkeypatch.setattr(pd.DataFrame, "to_sql", fake_to_sql)

    config = DummyConfig()
    df_accepted = pd.DataFrame({"a": [1]})
    df_rejected = pd.DataFrame({"a": [2]})

    postgres_loader.load_to_postgres(config, df_accepted, df_rejected)

    assert calls == ["accepted_table", "rejected_table"]


def test_load_to_postgres_invalid(monkeypatch):
    monkeypatch.setattr(postgres_loader, "get_engine", MagicMock(return_value=MagicMock()))

    def fake_to_sql(*args, **kwargs):
        raise AssertionError("to_sql should not be called for empty dfs")

    monkeypatch.setattr(pd.DataFrame, "to_sql", fake_to_sql)

    config = DummyConfig()
    df_accepted = pd.DataFrame({"a": []})
    df_rejected = pd.DataFrame({"a": []})

    postgres_loader.load_to_postgres(config, df_accepted, df_rejected)