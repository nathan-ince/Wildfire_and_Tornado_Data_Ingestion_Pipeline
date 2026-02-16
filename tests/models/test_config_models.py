import pytest
from pydantic import ValidationError

from project.models.config import Config


def _valid_base_config():
    return {
        "name": "my-pipeline",
        "version": "1.0",
        "target": {
            "tables": {"accepted": "accepted_tbl", "rejected": "rejected_tbl"},
            "fields": [
                {"name": "a", "type": "int64", "nullable": False, "unique": False},
                {"name": "b", "type": "string", "nullable": True, "unique": False},
            ],
        },
        "sources": [],
    }


def test_config_parses_with_csv_and_json_sources():
    data = _valid_base_config()
    data["sources"] = [
        {
            "name": "src_csv",
            "path": "data.csv",
            "format": "csv",
            "options": {"delimiter": ","},
            "mapping": {
                "col_a": {"name": "a", "type": "int64"},
                "col_b": {"name": "b", "type": "string"},
            },
        },
        {
            "name": "src_json",
            "path": "data.json",
            "format": "json",
            "options": None,
            "mapping": {
                "col_a": {"name": "a", "type": "int64"},
                "col_b": {"name": "b", "type": "string"},
            },
        },
    ]

    test_config = Config.model_validate(data)

    assert test_config.name == "my-pipeline"
    assert test_config.sources[0].format == "csv"
    assert test_config.sources[0].options.delimiter == ","
    assert test_config.sources[1].format == "json"
    assert test_config.sources[1].options is None


def test_source_rejects_unknown_format():
    data = _valid_base_config()
    data["sources"] = [
        {
            "name": "src_bad",
            "path": "data.txt",
            "format": "txt",  # invalid
            "options": None,
            "mapping": {"col_a": {"name": "a", "type": "int64"}},
        }
    ]

    with pytest.raises(ValidationError):
        Config.model_validate(data)


def test_csv_source_requires_delimiter():
    data = _valid_base_config()
    data["sources"] = [
        {
            "name": "src_csv",
            "path": "data.csv",
            "format": "csv",
            "options": {},  # missing delimiter
            "mapping": {"col_a": {"name": "a", "type": "int64"}},
        }
    ]

    with pytest.raises(ValidationError):
        Config.model_validate(data)