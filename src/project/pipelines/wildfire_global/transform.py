import logging
import pandas as pd

from project.models.config import Config
from project.transform.columns import rename_columns
from project.transform.chain import validate_chain
from project.transform.dedupe import dedupe_keep_first

from project.pipelines.wildfire_global import validators

from project.utils.compute_record_hash_series import compute_record_hash_series_exclude

logger = logging.getLogger(__name__)

def transform(config: Config, source_index: int, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    logger.info("transforming data")
    df = rename_columns(config, source_index, df)

    df_accepted, df_rejected = validate_chain(
        df,
        (
            validators.validate_country,
            validators.validate_year,
            validators.validate_month,
            validators.validate_region,
            validators.validate_fires_count,
            validators.validate_burned_area_hectares,
            validators.validate_cause,
            validators.validate_temperature_celsius,
            validators.validate_humidity_percent,
            validators.validate_wind_speed_kmh
        ),
    )

    df_accepted = df_accepted[~df_accepted.duplicated(keep="first")]

    # batch process id has not been been appended to either dataframe yet
    df_accepted_hash_series = compute_record_hash_series_exclude(df_accepted)
    df_rejected_hash_series = compute_record_hash_series_exclude(df_rejected, ["reason"])

    df_accepted = df_accepted.copy()
    df_rejected = df_rejected.copy()

    df_accepted["content_hash"] = df_accepted_hash_series
    df_rejected["content_hash"] = df_rejected_hash_series

    logger.info("transformed data")
    return df_accepted, df_rejected
