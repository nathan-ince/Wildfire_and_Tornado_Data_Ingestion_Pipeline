# import logging

# from project.core import configure_logging
# from project.pipelines.tornado_usa.pipeline import start as start_tornado_usa
# from project.pipelines.wildfire_global.pipeline import start as start_wildfire_global

# logger = logging.getLogger(__name__)

# if __name__ == "__main__":
#   configure_logging()
#   start_tornado_usa()
#   start_wildfire_global()

from pydantic import ValidationError
import sys

from src.project.core.settings import get_settings
from src.project.core import configure_logging
from src.project.pipelines.tornado_usa.pipeline import start as start_tornado_usa
from src.project.pipelines.wildfire_global.pipeline import start as start_wildfire_global

if __name__ == "__main__":
    try:
        get_settings()  # validate config early
    except ValidationError as e:
        print("Invalid environment configuration")
        for err in e.errors():
            print(f"{err['loc']}: {err['msg']}")
        sys.exit(1)

    configure_logging()
    start_tornado_usa()
    start_wildfire_global()