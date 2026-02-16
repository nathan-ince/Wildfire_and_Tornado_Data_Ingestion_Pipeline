import pytest
from project.read.read_yaml import read_from_yaml, ReadFromYamlError


def test_read_yaml_valid(tmp_path):
    p = tmp_path / "config.yaml"
    p.write_text("name: nate\ncount: 2\n")

    result = read_from_yaml(str(p))

    assert result == {"name": "nate", "count": 2}


def test_read_yaml_file_not_found():
    with pytest.raises(ReadFromYamlError) as excinfo:
        read_from_yaml("does_not_exist.yaml")

    err = excinfo.value
    assert err.kwargs["cause"] == "FileNotFoundError"
    assert err.kwargs["path"] == "does_not_exist.yaml"


def test_read_from_yaml_invalid(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("name: nate: oops\n") 

    with pytest.raises(ReadFromYamlError) as excinfo:
        read_from_yaml(str(p))

    err = excinfo.value
    assert err.kwargs["cause"].endswith("Error")
    assert err.kwargs["path"] == str(p)