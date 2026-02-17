import pytest
from types import SimpleNamespace
import project.read.read_config as config_mod

def make_config(target_names, source_names_list):
    target = SimpleNamespace(
        fields=[SimpleNamespace(name=n) for n in target_names]
    )
    sources = [
        SimpleNamespace(
            mapping={f"k{i}": SimpleNamespace(name=n) for i, n in enumerate(names)}
        )
        for names in source_names_list
    ]
    return SimpleNamespace(target=target, sources=sources)

def test_read_config_valid(monkeypatch):
    monkeypatch.setattr(config_mod, "read_from_yaml", lambda path: {"anything": "ok"})

    good = make_config(["a", "b"], [["a", "b"]])
    monkeypatch.setattr(config_mod.Config, "model_validate", lambda content: good)

    result = config_mod.read_config_from_yaml("fake.yaml")
    assert result is good

def test_read_config_invalid(monkeypatch):
    monkeypatch.setattr(config_mod, "read_from_yaml", lambda path: {"anything": "ok"})

    bad = make_config(["a", "b"], [["a", "c"]])
    monkeypatch.setattr(config_mod.Config, "model_validate", lambda content: bad)

    with pytest.raises(config_mod.ReadConfigFromYamlError):
        config_mod.read_config_from_yaml("fake.yaml")