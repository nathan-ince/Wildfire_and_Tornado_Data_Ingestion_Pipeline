import pandas as pd
from typing import Literal

def validate_int_between(df: pd.DataFrame, name: str, left: int, right: int, inclusive: Literal["both", "neither", "left", "right"] = "both",) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = df[name].notna() & df[name].between(left, right, inclusive)
    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["reason"] = f"invalid value :: field name = {name}"
    return df_accepted, df_rejected

def validate_non_negative(df: pd.DataFrame, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = df[name].notna() & df[name].ge(0)
    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["reason"] = f"invalid value :: field name = {name}"
    return df_accepted, df_rejected