import pandas as pd

from project.models.config import Config
from project.transform.columns import rename_columns


def test_rename_columns_selects_and_renames():
    config = Config.model_validate({
        "name": "test",
        "version": "0.0",
        "target": {
            "tables": {
                "accepted_final": "accepted_tbl_final",
                "accepted_stage": "accepted_tbl_stage",
                "rejected_final": "rejected_tbl_final",
                "rejected_stage": "rejected_tbl_stage"
            },
            "merge_accepted": "ma.sql",
            "merge_rejected": "mr.sql",
            "fields": []
        },
        "sources": [
            {
                "name": "tornado_usa",
                "path": "unused.json",
                "format": "json",
                "options": None,
                "mapping": {
                    "Year": {"name": "year", "type": "int"},
                    "State": {"name": "state", "type": "string"},
                }
            }
        ]
    })

    df = pd.DataFrame({
        "Year": [2020],
        "State": ["NC"],
        "Extra": ["ignore me"], 
    })

    out = rename_columns(config, source_index=0, df=df)

    assert list(out.columns) == ["year", "state"]
    assert out["year"].tolist() == [2020]
    assert out["state"].tolist() == ["NC"]