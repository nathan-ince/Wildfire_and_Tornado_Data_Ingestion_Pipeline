import pytest

from project.helpers.abstract_string_enum import AbstractStringEnum
from project.helpers.errors import AbstractError


class Color(AbstractStringEnum):
    RED = "red"
    BLUE = "blue"


def test_define_valid_value_returns_enum():
    result = Color.define("red", log_error=False)
    assert result is Color.RED


def test_define_non_string_raises_abstract_error():
    with pytest.raises(AbstractError):
        Color.define(123, log_error=False)


def test_define_invalid_string_raises_abstract_error():
    with pytest.raises(AbstractError):
        Color.define("green", log_error=False)