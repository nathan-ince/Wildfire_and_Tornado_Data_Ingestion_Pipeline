import pytest
from project.read.read_yaml import read_from_yaml, ReadFromYamlError


def test_read_yaml_valid(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("name: nate and jack\ncount: 2\n")

    result = read_from_yaml(str(path))

    assert result == {"name": "nate and jack", "count": 2}


def test_read_yaml_file_not_found():
    with pytest.raises(ReadFromYamlError) as yaml_error:
        read_from_yaml("does_not_exist.yaml")

    err = yaml_error.value
    assert err.kwargs["cause"] == "FileNotFoundError"
    assert err.kwargs["path"] == "does_not_exist.yaml"


def test_read_from_yaml_invalid(tmp_path):
    p = tmp_path / "invalid.yaml"
    p.write_text("name: nate: invalid data\n") 

    with pytest.raises(ReadFromYamlError) as yaml_error:
        read_from_yaml(str(p))

    err = yaml_error.value
    assert err.kwargs["cause"].endswith("Error")
    assert err.kwargs["path"] == str(p)