import pandas as pd
import pytest

from project.transform.validators.strings import validate_string_max_length, validate_string_exact_length


def to_py_list(values) -> list:
    s = pd.Series(values)
    return s.astype(object).where(s.notna(), None).tolist()


@pytest.mark.parametrize(
    "column, values, n, expected_valid, expected_invalid",
    [
        # Wildfire
        ("month", ["December", "DecembJanFebruary", "", pd.NA], 9, ["December"], ["DecembJanFebruary", "", pd.NA]),
    ],
)
def test_validate_string_max_length(column, values, n, expected_valid, expected_invalid):
    df = pd.DataFrame({column: values})
    accepted, rejected = validate_string_max_length(df, column, n)

    assert to_py_list(accepted[column]) == to_py_list(expected_valid)
    assert to_py_list(rejected[column]) == to_py_list(expected_invalid)
    assert rejected["reason"].eq(f"invalid value :: field name = {column}").all()


@pytest.mark.parametrize(
    "column, values, n, expected_valid, expected_invalid",
    [
        # Tornado
        ("state", ["NC", "B", "", pd.NA], 2, ["NC"], ["B", "", pd.NA]),
    ],
)
def test_validate_string_exact_length(column, values, n, expected_valid, expected_invalid):
    df = pd.DataFrame({column: values})
    accepted, rejected = validate_string_exact_length(df, column, n)

    assert to_py_list(accepted[column]) == to_py_list(expected_valid)
    assert to_py_list(rejected[column]) == to_py_list(expected_invalid)
    assert rejected["reason"].eq(f"invalid value :: field name = {column}").all()