def dedupe_wildfire(df):
    keys = ["country", "year", "month", "region", "cause"]
    duplicates = df.duplicated(subset=keys, keep="first")

    accepted = df[~duplicates].copy()
    rejected = df[duplicates].copy()
    rejected["reason"] = "Duplicate record"

    return accepted, rejected

__all__ = ["dedupe_wildfire"]