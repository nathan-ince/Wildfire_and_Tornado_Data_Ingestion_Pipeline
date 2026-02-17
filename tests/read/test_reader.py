import pandas as pd
import pytest
from unittest.mock import MagicMock

import project.read.read_data as reader_module


def make_config(fmt: str):
    field = MagicMock()
    field.type = "int64"

    options = MagicMock()
    options.delimiter = ","

    source = MagicMock()
    source.name = "src"
    source.path = "file"
    source.format = fmt
    source.mapping = {"a": field}
    source.options = options

    config = MagicMock()
    config.sources = [source]
    return config


@pytest.mark.parametrize(
    "fmt, pandas_function",
    [
        ("csv", "read_csv"),
        ("json", "read_json"),
    ],
)
def test_read_data(monkeypatch, fmt, pandas_function):
    df = pd.DataFrame({"a": [1]})

    pandas_reader_mock = MagicMock(return_value=df)
    monkeypatch.setattr(reader_module.pd, pandas_function, pandas_reader_mock)

    config = make_config(fmt)
    result = reader_module.read_data_with_pandas(config, 0)

    assert result is df
    assert pandas_reader_mock.call_count == 1


def test_read_data_invalid():
    config = make_config("xml")

    with pytest.raises(reader_module.ReadDataWithPandasError) as excinfo:
        reader_module.read_data_with_pandas(config, 0)

    assert excinfo.value.kwargs["cause"] == "ValueError"