import pandas as pd
import pytest

import project.io.reader as reader_mod


class _Field:
    def __init__(self, typ: str):
        self.type = typ

class _Options:
    def __init__(self, delimiter: str = ","):
        self.delimiter = delimiter

class _Source:
    def __init__(self, fmt: str):
        self.name = "src"
        self.path = "file"
        self.format = fmt
        self.mapping = {"a": _Field("int64")}
        self.options = _Options()

class _Config:
    def __init__(self, fmt: str):
        self.sources = [_Source(fmt)]


def test_read_data_csv(monkeypatch):
    df = pd.DataFrame({"a": [1]})

    def fake_read_csv(*args, **kwargs):
        return df

    monkeypatch.setattr(reader_mod.pd, "read_csv", fake_read_csv)

    test_config = _Config("csv")
    result = reader_mod.read_data_with_pandas(test_config, 0)

    assert result is df


def test_read_data_json(monkeypatch):
    df = pd.DataFrame({"a": [1]})

    def fake_read_json(*args, **kwargs):
        return df

    monkeypatch.setattr(reader_mod.pd, "read_json", fake_read_json)

    test_config = _Config("json")
    result = reader_mod.read_data_with_pandas(test_config, 0)

    assert result is df


def test_read_data_invalid():
    test_config = _Config("xml")

    with pytest.raises(reader_mod.ReadDataWithPandasError) as excinfo:
        reader_mod.read_data_with_pandas(test_config, 0)

    assert excinfo.value.kwargs["cause"] == "ValueError"