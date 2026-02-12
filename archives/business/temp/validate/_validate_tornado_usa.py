import pandas as pd

def validate_tornado_usa(df):
    valid_rows = []
    rejected_rows = []

    for _, row in df.iterrows():
        errors = []

        # required fields
        if pd.isna(row["year"]):
            errors.append("year missing")

        if pd.isna(row["month"]) or row["month"] < 1 or row["month"] > 12:
            errors.append("month invalid")

        if pd.isna(row["day"]) or row["day"] < 1 or row["day"] > 31:
            errors.append("day invalid")

        if pd.isna(row["state"]) or len(row["state"]) != 2:
            errors.append("state invalid")

        if pd.isna(row["magnitude"]) or row["magnitude"] < 0:
            errors.append("magnitude invalid")

        # non-negative counts
        if not pd.isna(row["injury_count"]) and row["injury_count"] < 0:
            errors.append("injury_count negative")

        if not pd.isna(row["fatality_count"]) and row["fatality_count"] < 0:
            errors.append("fatality_count negative")


        if not pd.isna(row["latitude_start"]) and abs(row["latitude_start"]) > 90:
            errors.append("latitude_start invalid")

        if not pd.isna(row["longitude_start"]) and abs(row["longitude_start"]) > 180:
            errors.append("longitude_start invalid")

        if errors:
            reject_row = row.to_dict()
            reject_row["reason"] = "; ".join(errors)
            rejected_rows.append(reject_row)
        else:
            valid_rows.append(row.to_dict())

    accepted_df = pd.DataFrame(valid_rows)
    rejected_df = pd.DataFrame(rejected_rows)

    return accepted_df, rejected_df

__all__ = ["validate_tornado_usa"]