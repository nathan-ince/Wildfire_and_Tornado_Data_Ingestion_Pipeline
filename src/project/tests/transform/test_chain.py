import pandas as pd

from project.transform.chain import validate_chain


def test_validate_chain_applies_all_validators_and_collects_rejections():
    df = pd.DataFrame({
        "x": [1, -1, 2, -2],
    })

    def keep_positive(df):
        accepted = df[df["x"] > 0]
        rejected = df[df["x"] <= 0].copy()
        rejected["reason"] = "non-positive"
        return accepted, rejected

    def keep_less_than_two(df):
        accepted = df[df["x"] < 2]
        rejected = df[df["x"] >= 2].copy()
        rejected["reason"] = "too-large"
        return accepted, rejected

    accepted, rejected = validate_chain(df, (keep_positive, keep_less_than_two))

    assert accepted["x"].tolist() == [1]
    assert rejected["x"].tolist() == [-1, -2, 2]
    assert len(rejected) == 3