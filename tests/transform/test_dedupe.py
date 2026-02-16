import pandas as pd
from project.transform.dedupe import dedupe_keep_first

def test_dedupe_keep_first():
    df = pd.DataFrame({
        "id": [1, 1, 2, 3, 3],
        "val": ["a", "a", "b", "c", "c"]
    })

    accepted, rejected = dedupe_keep_first(df)

    assert accepted.reset_index(drop=True).to_dict(orient="records") == [
        {"id": 1, "val": "a"},
        {"id": 2, "val": "b"},
        {"id": 3, "val": "c"},
    ]

    assert rejected.reset_index(drop=True).to_dict(orient="records") == [
        {"id": 1, "val": "a", "reason": "duplicate record"},
        {"id": 3, "val": "c", "reason": "duplicate record"},
    ]