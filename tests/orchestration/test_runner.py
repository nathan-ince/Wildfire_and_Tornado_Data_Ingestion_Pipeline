import pandas as pd
from uuid import UUID

import project.orchestration.runner as runner
from project.orchestration.types import Status


class _Source:
    def __init__(self, name="s1", path="p", fmt="csv"):
        self.name = name
        self.path = path
        self.format = fmt
        self.mapping = {}
        self.options = None

class _Config:
    def __init__(self, source_count: int):
        self.sources = [_Source(name=f"s{i}") for i in range(source_count)]


def _fixed_uuid(i: int) -> UUID:
    return UUID(f"00000000-0000-0000-0000-{i:012d}")


def _fixed_ts(i: int):
    return f"ts{i}"


def test_run_main_process_config_read_fails_finalizes_failure(monkeypatch):
    calls = {"finalize_main": []}

    uuid_counter = {"i": 1}
    ts_counter = {"i": 1}
    monkeypatch.setattr(runner, "generate_random_uuid", lambda: _fixed_uuid(uuid_counter.setdefault("i", 1) or 1))
    def next_uuid():
        i = uuid_counter["i"]
        uuid_counter["i"] += 1
        return _fixed_uuid(i)
    monkeypatch.setattr(runner, "generate_random_uuid", next_uuid)

    def next_ts():
        i = ts_counter["i"]
        ts_counter["i"] += 1
        return _fixed_ts(i)
    monkeypatch.setattr(runner, "generate_timestamp", next_ts)


    monkeypatch.setattr(runner, "initialize_main_process", lambda **kwargs: None)


    def fail_read_config(_path: str):
        raise runner.ReadConfigFromYamlError("bad config", cause="YAMLError", path=_path)
    monkeypatch.setattr(runner, "read_config_from_yaml", fail_read_config)


    def fake_finalize_main_process(**kwargs):
        calls["finalize_main"].append(kwargs)
    monkeypatch.setattr(runner, "finalize_main_process", fake_finalize_main_process)

    runner.run_main_process("config.yaml", transform_data=lambda *a: (pd.DataFrame(), pd.DataFrame()))

    assert len(calls["finalize_main"]) == 1
    assert calls["finalize_main"][0]["main_process_status"] is Status.Failure


def test_run_main_process_all_batches_success_finalizes_success(monkeypatch):
    calls = {"finalize_main": [], "finalize_batch": []}


    uuid_counter = {"i": 1}
    ts_counter = {"i": 1}

    def next_uuid():
        i = uuid_counter["i"]
        uuid_counter["i"] += 1
        return _fixed_uuid(i)
    monkeypatch.setattr(runner, "generate_random_uuid", next_uuid)

    def next_ts():
        i = ts_counter["i"]
        ts_counter["i"] += 1
        return _fixed_ts(i)
    monkeypatch.setattr(runner, "generate_timestamp", next_ts)

    monkeypatch.setattr(runner, "initialize_main_process", lambda **kwargs: None)
    monkeypatch.setattr(runner, "read_config_from_yaml", lambda _path: _Config(source_count=2))

    monkeypatch.setattr(runner, "initialize_batch_process", lambda **kwargs: None)
    monkeypatch.setattr(runner, "read_data_with_pandas", lambda config, source_index: pd.DataFrame({"x": [1]}))

    def transform_ok(config, source_index, df):
        return pd.DataFrame({"ok": [1]}), pd.DataFrame({"bad": []})


    monkeypatch.setattr(runner, "load_to_postgres", lambda config, a, r: None)

    def fake_finalize_batch_process(**kwargs):
        calls["finalize_batch"].append(kwargs)
    monkeypatch.setattr(runner, "finalize_batch_process", fake_finalize_batch_process)

    def fake_finalize_main_process(**kwargs):
        calls["finalize_main"].append(kwargs)
    monkeypatch.setattr(runner, "finalize_main_process", fake_finalize_main_process)

    runner.run_main_process("config.yaml", transform_data=transform_ok)


    assert len(calls["finalize_batch"]) == 2
    assert all(c["batch_process_status"] is Status.Success for c in calls["finalize_batch"])


    assert len(calls["finalize_main"]) == 1
    assert calls["finalize_main"][0]["main_process_status"] is Status.Success


def test_run_main_process_one_batch_fails_finalizes_warning(monkeypatch):
    calls = {"finalize_main": [], "finalize_batch": []}

    uuid_counter = {"i": 1}
    ts_counter = {"i": 1}

    def next_uuid():
        i = uuid_counter["i"]
        uuid_counter["i"] += 1
        return _fixed_uuid(i)
    monkeypatch.setattr(runner, "generate_random_uuid", next_uuid)

    def next_ts():
        i = ts_counter["i"]
        ts_counter["i"] += 1
        return _fixed_ts(i)
    monkeypatch.setattr(runner, "generate_timestamp", next_ts)

    monkeypatch.setattr(runner, "initialize_main_process", lambda **kwargs: None)
    monkeypatch.setattr(runner, "read_config_from_yaml", lambda _path: _Config(source_count=2))
    monkeypatch.setattr(runner, "initialize_batch_process", lambda **kwargs: None)
    monkeypatch.setattr(runner, "read_data_with_pandas", lambda config, source_index: pd.DataFrame({"x": [1]}))


    def load_maybe_fail(config, df_a, df_r):

        batch_id = df_a["batch_process_id"].iloc[0]
        if str(batch_id).endswith("000000000003"):
            raise RuntimeError("db write failed")
    monkeypatch.setattr(runner, "load_to_postgres", load_maybe_fail)

    def transform_ok(config, source_index, df):
        return pd.DataFrame({"ok": [1]}), pd.DataFrame({"bad": []})

    def fake_finalize_batch_process(**kwargs):
        calls["finalize_batch"].append(kwargs)
    monkeypatch.setattr(runner, "finalize_batch_process", fake_finalize_batch_process)

    def fake_finalize_main_process(**kwargs):
        calls["finalize_main"].append(kwargs)
    monkeypatch.setattr(runner, "finalize_main_process", fake_finalize_main_process)

    runner.run_main_process("config.yaml", transform_data=transform_ok)


    statuses = [c["batch_process_status"] for c in calls["finalize_batch"]]
    assert Status.Success in statuses
    assert Status.Failure in statuses


    assert len(calls["finalize_main"]) == 1
    assert calls["finalize_main"][0]["main_process_status"] is Status.Warning