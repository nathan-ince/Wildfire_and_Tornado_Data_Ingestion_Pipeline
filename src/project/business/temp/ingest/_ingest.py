import logging
import pandas as pd

from typing import cast

from project.core import dbengine
from project.utils.load import load_config_from_yaml, load_external_data

from ._pipeline import pick_pipeline

logger = logging.getLogger(__name__)

def ingest(config_path: str) -> None:
    pipeline = pick_pipeline(config_path)

    config = load_config_from_yaml(config_path)
    source_count = len(config.sources)
    for source_index in range(source_count):
        # source
        source = config.sources[source_index]
        logger.info("Ingesting \"%s\"", source.path)
        all_rejected = pd.DataFrame(columns=[*source.columns.values(), "reason"])

        # load
        df = load_external_data(config, source_index)
        logger.info("Read %d rows", len(df))

        # rename
        logger.info("Renaming Columns")
        df = df[list(source.columns.keys())].rename(columns=source.columns)

        # clean
        df = pipeline["clean"](df)
        logger.info("Data cleaned")

        # dedupe
        accepted_after_dedupe, dup_rejects = pipeline["dedupe"](df)
        logger.info("Deduped: %d rows remain", len(accepted_after_dedupe))
        all_rejected = pd.concat([all_rejected, dup_rejects]).copy()

        # validate
        accepted, rejected = pipeline["validate"](accepted_after_dedupe)
        logger.info("Validated: %d accepted, %d rejected", len(accepted), len(rejected))
        all_rejected = pd.concat([all_rejected, rejected]).copy()

        # load accepted
        logger.info("Loaded accepted -> \"%s\"", config.accepted)
        cast(pd.DataFrame, accepted).to_sql(name=config.accepted, con=dbengine, if_exists="delete_rows", index=False)

        # load rejected
        if rejected is not None and not rejected.empty:
            logger.info("Loaded rejected -> \"%s\"", config.rejected)
            cast(pd.DataFrame, all_rejected).to_sql(name=config.rejected, con=dbengine, if_exists="delete_rows", index=False)
        else:
            logger.info("No rejected rows to load")

        logger.info("Finished \"%s\"", config.accepted)

__all__ = ["ingest"]