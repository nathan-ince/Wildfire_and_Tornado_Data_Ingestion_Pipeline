from project.core import db

def test_build_engine(monkeypatch):
    captured = {}

    def fake_create_engine(url, **kwargs):
        captured["url"] = url
        captured["kwargs"] = kwargs
        return "ENGINE"

    monkeypatch.setattr(db, "create_engine", fake_create_engine)

    engine = db.build_engine()

    assert engine == "ENGINE"
    assert captured["url"].startswith("postgresql+psycopg2://")
    assert captured["kwargs"]["pool_pre_ping"] is True
    assert captured["kwargs"]["future"] is True


def test_get_engine(monkeypatch):
    monkeypatch.setattr(db, "build_engine", lambda: "ENGINE")

    engine = db.get_engine()

    assert engine == "ENGINE"