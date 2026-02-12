from project.utils.clean import clean_wildfire
from project.utils.clean import clean_tornado_usa

from project.utils.dedupe import dedupe_wildfire
from project.utils.dedupe import dedupe_tornado

from project.utils.validate import validate_wildfire
from project.utils.validate import validate_tornado_usa

PIPELINES = {
    "wildfire": {
        "clean": clean_wildfire,
        "dedupe": dedupe_wildfire,
        "validate": validate_wildfire
    },
    "tornado": {
        "clean": clean_tornado_usa,
        "dedupe": dedupe_tornado,
        "validate": validate_tornado_usa
    },
}

def pick_pipeline(config_path: str) -> dict:
    name = config_path.lower()
    if "wildfire" in name:
        return PIPELINES["wildfire"]
    if "tornado" in name:
        return PIPELINES["tornado"]
    raise ValueError(f"Unknown config type: {config_path}")

__all__ = ["pick_pipeline"]
