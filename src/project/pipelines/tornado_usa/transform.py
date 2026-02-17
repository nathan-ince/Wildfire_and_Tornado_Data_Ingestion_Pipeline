import logging
import pandas as pd

from project.models.config import Config
from project.transform.columns import rename_columns
from project.transform.chain import validate_chain

from project.pipelines.tornado_usa import validators

from project.utils.compute_record_hash_series import compute_record_hash_series_exclude

logger = logging.getLogger(__name__)

def transform(config: Config, source_index: int, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    logger.info("transforming data")
    df = rename_columns(config, source_index, df)

    df_accepted, df_rejected = validate_chain(
        df,
        (
            validators.validate_year,
            validators.validate_month,
            validators.validate_day,
            validators.validate_date,
            validators.validate_state,
            validators.validate_magnitude,
            validators.validate_injury_count,
            validators.validate_fatality_count,
            validators.validate_latitude_start,
            validators.validate_longitude_start,
            validators.validate_latitude_end,
            validators.validate_longitude_end,
            validators.validate_length_miles,
            validators.validate_width_yards,
            validators.validate_year_month_day_date,
        ),
    )

    # dedupe
    df_accepted = df_accepted[~df_accepted.duplicated(keep=False)]

    # batch process id has not been been appended to either dataframe yet
    df_accepted_hash_series = compute_record_hash_series_exclude(df_accepted)
    df_rejected_hash_series = compute_record_hash_series_exclude(df_rejected, ["rejected_reason"])

    df_accepted = df_accepted.copy()
    df_rejected = df_rejected.copy()

    df_accepted["content_hash"] = df_accepted_hash_series
    df_rejected["content_hash"] = df_rejected_hash_series

    logger.info("transformed data")
    return df_accepted, df_rejected
