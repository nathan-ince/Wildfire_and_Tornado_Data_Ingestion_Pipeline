import pandas as pd

def validate_string_max_length(
    df: pd.DataFrame,
    name: str,
    n: int
) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = df[name].notna() & (df[name].str.strip().str.len() <= n)
    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["reason"] = f"invalid value :: field name = {name}"
    return df_accepted, df_rejected

def validate_string_exact_length(
    df: pd.DataFrame,
    name: str,
    n: int
) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = df[name].notna() & (df[name].str.strip().str.len() == n)
    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["reason"] = f"invalid value :: field name = {name}"
    return df_accepted, df_rejected