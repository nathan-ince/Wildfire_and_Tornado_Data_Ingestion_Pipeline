import logging
import pandas as pd

from project.models.config import Config
from project.transform.columns import rename_columns
from project.transform.chain import validate_chain
from project.transform.dedupe import dedupe_keep_first

from .validators import (
    validate_country,
    validate_year,
    validate_month,
    validate_region,
    validate_fires_count,
    validate_burned_area_hectares,
    validate_cause,
    validate_temperature_celsius,
    validate_humidity_percent,
    validate_wind_speed_kmh,
)

logger = logging.getLogger(__name__)

def transform(config: Config, source_index: int, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    logger.info("transforming data")
    df = rename_columns(config, source_index, df)

    df_accepted, df_rejected = validate_chain(
        df,
        (
            validate_country,
            validate_year,
            validate_month,
            validate_region,
            validate_fires_count,
            validate_burned_area_hectares,
            validate_cause,
            validate_temperature_celsius,
            validate_humidity_percent,
            validate_wind_speed_kmh,
        ),
    )

    df_accepted, df_dupes = dedupe_keep_first(df_accepted)
    df_rejected = pd.concat([df_rejected, df_dupes], ignore_index=True)

    logger.info("transformed data")
    return df_accepted, df_rejected