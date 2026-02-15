import pandas as pd

from project.transform.dedupe import dedupe_keep_first

def test_dedupe_keep_first():
    df = pd.DataFrame({
        "id": [1, 1, 2, 3, 3], 
        "val": ["a", "a", "b", "c", "c"]
        })

    accepted, rejected = dedupe_keep_first(df)

    assert accepted.to_dict() == [
        {"id": 1, "val": "a"},
        {"id": 2, "val": "b"},
        {"id": 3, "val": "c"}
        ]

    assert rejected.to_dict() == [
        {"id": 1, "val": "a"},
        {"id": 3, "val": "c"},
    ]

    assert rejected["reason"].eq("duplicate record").all()

