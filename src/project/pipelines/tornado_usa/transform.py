import logging
import pandas as pd

from project.models.config import Config
from project.transform.columns import rename_columns
from project.transform.chain import validate_chain
from project.transform.dedupe import dedupe_keep_first

from project.pipelines.tornado_usa import validators

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

    df_accepted, df_dupes = dedupe_keep_first(df_accepted)
    df_rejected = pd.concat([df_rejected, df_dupes], ignore_index=True)

    logger.info("transformed data")
    return df_accepted, df_rejected