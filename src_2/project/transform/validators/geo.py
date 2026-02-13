import pandas as pd

def validate_latitude(
    df: pd.DataFrame,
    name: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = df[name].notna() & df[name].between(-90, 90)
    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["reason"] = f"invalid value :: field name = {name}"
    return df_accepted, df_rejected

def validate_longitude(
    df: pd.DataFrame,
    name: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = df[name].notna() & df[name].between(-180, 180)
    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["reason"] = f"invalid value :: field name = {name}"
    return df_accepted, df_rejected