import pandas as pd

from project.transform.chain import validate_chain


def test_validate_chain():
    df = pd.DataFrame({"x": [1, 2, 3, 4]})

    def reject_even_numbers(df):
        accepted = df[df["x"] % 2 != 0]
        rejected = df[df["x"] % 2 == 0].copy()
        rejected["rejected_reason"] = "even"
        return accepted, rejected

    def reject_numbers_greater_than_two(df):
        accepted = df[df["x"] <= 2]
        rejected = df[df["x"] > 2].copy()
        rejected["rejected_reason"] = "greater-than-two"
        return accepted, rejected

    accepted, rejected = validate_chain(df,(reject_even_numbers, reject_numbers_greater_than_two))

    assert accepted["x"].tolist() == [1]
    assert len(rejected) == 3