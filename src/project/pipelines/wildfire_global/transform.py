import logging
import pandas as pd

from project.models.config import Config
from project.transform.columns import rename_columns
from project.transform.chain import validate_chain
from project.transform.dedupe import dedupe_keep_first

from project.pipelines.wildfire_global import validators

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

    df_accepted, df_dupes = dedupe_keep_first(df_accepted)
    df_rejected = pd.concat([df_rejected, df_dupes], ignore_index=True)

    logger.info("transformed data")
    return df_accepted, df_rejected