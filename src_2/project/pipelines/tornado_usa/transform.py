import logging
import pandas as pd

from project.models.config import Config
from project.transform.columns import rename_columns
from project.transform.chain import validate_chain
from project.transform.dedupe import dedupe_keep_first

from .validators import (
    validate_year,
    validate_month,
    validate_day,
    validate_date,
    validate_state,
    validate_magnitude,
    validate_injury_count,
    validate_fatality_count,
    validate_latitude_start,
    validate_longitude_start,
    validate_latitude_end,
    validate_longitude_end,
    validate_length_miles,
    validate_width_yards,
    validate_year_month_day_date,
)

logger = logging.getLogger(__name__)

def transform(config: Config, source_index: int, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    logger.info("transforming data")
    df = rename_columns(config, source_index, df)

    df_accepted, df_rejected = validate_chain(
        df,
        (
            validate_year,
            validate_month,
            validate_day,
            validate_date,
            validate_state,
            validate_magnitude,
            validate_injury_count,
            validate_fatality_count,
            validate_latitude_start,
            validate_longitude_start,
            validate_latitude_end,
            validate_longitude_end,
            validate_length_miles,
            validate_width_yards,
            validate_year_month_day_date,  # intentionally after individual checks
        ),
    )

    df_accepted, df_dupes = dedupe_keep_first(df_accepted)
    df_rejected = pd.concat([df_rejected, df_dupes], ignore_index=True)

    logger.info("transformed data")
    return df_accepted, df_rejected