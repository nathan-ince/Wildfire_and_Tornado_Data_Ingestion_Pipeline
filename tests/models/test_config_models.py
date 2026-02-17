import pytest
from pydantic import ValidationError
from project.models.config import Config


BASE_MAPPING = {
    "col_a": {"name": "a", "type": "int64"},
    "col_b": {"name": "b", "type": "string"},
}


def base_config():
    return {
        "name": "my-pipeline",
        "version": "1.0",
        "target": {
            "tables": {
                "accepted_final": "accepted_tbl_final",
                "accepted_stage": "accepted_tbl_stage",
                "rejected_final": "rejected_tbl_final",
                "rejected_stage": "rejected_tbl_stage",
            },
            "merge_accepted": "ma.sql",
            "merge_rejected": "mr.sql",
            "fields": [
                {"name": "a", "type": "int64"},
                {"name": "b", "type": "string"},
            ],
        },
        "sources": [],
    }


def test_config_csv_and_json():
    data = base_config()
    data["sources"] = [
        {
            "name": "src_csv",
            "path": "data.csv",
            "format": "csv",
            "options": {"delimiter": ","},
            "mapping": BASE_MAPPING,
        },
        {
            "name": "src_json",
            "path": "data.json",
            "format": "json",
            "options": None,
            "mapping": BASE_MAPPING,
        },
    ]

    config = Config.model_validate(data)

    assert config.sources[0].format == "csv"
    assert config.sources[0].options.delimiter == ","
    assert config.sources[1].format == "json"
    assert config.sources[1].options is None


@pytest.mark.parametrize(
    "format, options",
    [
        ("txt", None),          # unknown format
        ("csv", {}),            # csv missing delimiter
    ],
)
def test_source_validation_errors(format, options):
    data = base_config()
    data["sources"] = [
        {
            "name": "src_bad",
            "path": "data.bad",
            "format": format,
            "options": options,
            "mapping": BASE_MAPPING,
        }
    ]

    with pytest.raises(ValidationError):
        Config.model_validate(data)