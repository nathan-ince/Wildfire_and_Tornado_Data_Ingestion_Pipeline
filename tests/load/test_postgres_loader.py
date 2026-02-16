import pandas as pd

from project.load.postgres_loader import load_to_postgres


class DummyConfig:
    class Target:
        class Tables:
            accepted = "accepted_table"
            rejected = "rejected_table"
        tables = Tables()
    target = Target()


def test_load_to_postgres_valid(monkeypatch):
    calls = []

    def fake_to_sql(self, *, name, con, if_exists, index):
        calls.append(name)

    monkeypatch.setattr(pd.DataFrame, "to_sql", fake_to_sql)

    config = DummyConfig()
    df_accepted = pd.DataFrame({"a": [1]})
    df_rejected = pd.DataFrame({"a": [2]})

    load_to_postgres(config, df_accepted, df_rejected)

    assert calls == ["accepted_table", "rejected_table"]


def test_load_to_postgres_invalid(monkeypatch):
    def fake_to_sql(*args, **kwargs):
        raise AssertionError("to_sql should not be called for empty dfs")

    monkeypatch.setattr(pd.DataFrame, "to_sql", fake_to_sql)

    config = DummyConfig()
    df_accepted = pd.DataFrame({"a": []})
    df_rejected = pd.DataFrame({"a": []})

    load_to_postgres(config, df_accepted, df_rejected)