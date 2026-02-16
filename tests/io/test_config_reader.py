import pytest
import project.io.config as config_mod


class _Field:
    def __init__(self, name: str):
        self.name = name

class _Target:
    def __init__(self, names):
        self.fields = [_Field(n) for n in names]

class _Source:
    def __init__(self, names):
        self.mapping = {f"k{i}": _Field(n) for i, n in enumerate(names)}

class _Config:
    def __init__(self, target_names, source_names_list):
        self.target = _Target(target_names)
        self.sources = [_Source(names) for names in source_names_list]


def test_read_config_valid(monkeypatch):
    monkeypatch.setattr(config_mod, "read_from_yaml", lambda path: {"anything": "ok"})

    good = _Config(["a", "b"], [["a", "b"]])
    monkeypatch.setattr(config_mod.Config, "model_validate", lambda content: good)

    result = config_mod.read_config_from_yaml("fake.yaml")
    assert result is good


def test_read_config_invalid(monkeypatch):
    monkeypatch.setattr(config_mod, "read_from_yaml", lambda path: {"anything": "ok"})

    bad = _Config(["a", "b"], [["a", "c"]])
    monkeypatch.setattr(config_mod.Config, "model_validate", lambda content: bad)

    with pytest.raises(config_mod.ReadConfigFromYamlError):
        config_mod.read_config_from_yaml("fake.yaml")