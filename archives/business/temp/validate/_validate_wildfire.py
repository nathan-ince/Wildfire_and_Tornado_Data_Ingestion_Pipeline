import pandas as pd

def validate_wildfire(df):
    valid_rows = []
    rejected_rows = []

    for _, row in df.iterrows():
        errors = []

        # required fields
        if pd.isna(row["country"]) or str(row["country"]).strip() == "":
            errors.append("country missing")

        if pd.isna(row["year"]):
            errors.append("year missing")

        if pd.isna(row["month"]) or str(row["month"]).strip() == "":
            errors.append("month missing")

        if pd.isna(row["recorded_fires_count"]):
            errors.append("recorded_fires_count missing")


        if pd.isna(row["region"]) or str(row["region"]).strip() == "":
            errors.append("region missing")

        if pd.isna(row["cause"]) or str(row["cause"]).strip() == "":
            errors.append("cause missing")


        if not pd.isna(row["recorded_fires_count"]) and row["recorded_fires_count"] < 0:
            errors.append("recorded_fires_count negative")

        if not pd.isna(row["burned_area_hectares"]) and row["burned_area_hectares"] < 0:
            errors.append("burned_area_hectares negative")

        if not pd.isna(row["humidity_percent"]) and (row["humidity_percent"] < 0 or row["humidity_percent"] > 100):
            errors.append("humidity_percent invalid")

        if errors:
            reject_row = row.to_dict()
            reject_row["reason"] = "; ".join(errors)
            rejected_rows.append(reject_row)
        else:
            valid_rows.append(row.to_dict())

    accepted_df = pd.DataFrame(valid_rows)
    rejected_df = pd.DataFrame(rejected_rows)

    return accepted_df, rejected_df

__all__ = ["validate_wildfire"]