import pandas as pd
import pytest

from project.transform.validators.strings import validate_string_max_length, validate_string_exact_length


@pytest.mark.parametrize(
    "column, values, n, expected_valid, expected_invalid",
    [
        # Wildfire
        ("month", ["December", "DecembJanFebruary", "", None], 9, ["December"], ["DecembJanFebruary", "", None]),
    ],
)
def test_validate_string_max_length(column, values, n, expected_valid, expected_invalid):
    df = pd.DataFrame({column: values})
    accepted, rejected = validate_string_max_length(df, column, n)

    assert accepted[column].tolist() == expected_valid
    assert rejected[column].tolist() == expected_invalid
    assert rejected["reason"].eq(f"invalid value :: field name = {column}").all()


@pytest.mark.parametrize(
    "column, values, n, expected_valid, expected_invalid",
    [
        # Tornado
        ("state", ["NC", "B", "", None], 2, ["NC"], ["B", "", None]),
    ],
)
def test_validate_string_exact_length(column, values, n, expected_valid, expected_invalid):
    df = pd.DataFrame({column: values})
    accepted, rejected = validate_string_exact_length(df, column, n)

    assert accepted[column].tolist() == expected_valid
    assert rejected[column].tolist() == expected_invalid
    assert rejected["reason"].eq(f"invalid value :: field name = {column}").all()