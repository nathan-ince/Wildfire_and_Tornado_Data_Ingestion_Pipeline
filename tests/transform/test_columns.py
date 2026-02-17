import pandas as pd
from unittest.mock import MagicMock

from project.transform.columns import rename_columns


def test_rename_columns():
    config = MagicMock()

    year_field = MagicMock()
    year_field.name = "year"

    state_field = MagicMock()
    state_field.name = "state"

    source = MagicMock()
    source.mapping = {
        "Year": year_field,
        "State": state_field,
    }
    config.sources = [source]

    df = pd.DataFrame(
        {
            "Year": [2020],
            "State": ["NC"],
            "Extra": ["ignore me"],
        }
    )

    renamed_df = rename_columns(config, source_index=0, df=df)

    assert list(renamed_df.columns) == ["year", "state"]
    assert renamed_df["year"].tolist() == [2020]
    assert renamed_df["state"].tolist() == ["NC"]