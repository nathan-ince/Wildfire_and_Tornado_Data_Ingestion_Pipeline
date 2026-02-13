def dedupe_tornado(df):
    keys = ["date", "state", "magnitude", "latitude_start", "longitude_start", "length_miles", "width_yards"]
    duplicates = df.duplicated(subset=keys, keep="first")

    accepted = df[~duplicates].copy()
    rejected = df[duplicates].copy()
    rejected["reason"] = "Duplicate record"

    return accepted, rejected

__all__ = ["dedupe_tornado"]