import pandas as pd

from project.utils.compute_record_hash_series import (
    compute_record_hash_series_include,
    compute_record_hash_series_exclude,
)


def test_compute_record_hash_series_include():
    df = pd.DataFrame({
        "a": [1, 2],
        "b": ["x", "y"],
    })

    result = compute_record_hash_series_include(df, ["a", "b"])


    assert len(result) == 2


    assert isinstance(result.iloc[0], str)
    assert isinstance(result.iloc[1], str)


    assert result.iloc[0] != result.iloc[1]


def test_compute_record_hash_series_exclude():
    df = pd.DataFrame({
        "a": [1, 1],
        "b": ["x", "y"],
    })


    result = compute_record_hash_series_exclude(df, excluded_fields=["b"])


    assert result.iloc[0] == result.iloc[1]


def test_compute_empty_dataframe():
    df = pd.DataFrame()

    result = compute_record_hash_series_exclude(df)

    assert result.empty is True