import pytest
from project.io.yaml_reader import read_from_yaml, ReadFromYamlError


def test_read_from_yaml_success(tmp_path):
    p = tmp_path / "config.yaml"
    p.write_text("name: nate\ncount: 2\n")

    result = read_from_yaml(str(p))

    assert result == {"name": "nate", "count": 2}


def test_read_from_yaml_file_not_found_raises():
    with pytest.raises(ReadFromYamlError) as excinfo:
        read_from_yaml("does_not_exist.yaml")

    err = excinfo.value
    assert err.kwargs["cause"] == "FileNotFoundError"
    assert err.kwargs["path"] == "does_not_exist.yaml"


def test_read_from_yaml_invalid_yaml_raises(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("name: nate: oops\n")  # invalid YAML

    with pytest.raises(ReadFromYamlError) as excinfo:
        read_from_yaml(str(p))

    err = excinfo.value
    assert err.kwargs["cause"] == "YAMLError"
    assert err.kwargs["path"] == str(p)