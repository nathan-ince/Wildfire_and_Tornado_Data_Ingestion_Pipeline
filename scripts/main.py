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

from project.core.settings import get_settings
from project.core import configure_logging
from project.core.db import get_engine
from project.pipelines.tornado_usa.pipeline import start as start_tornado_usa
from project.pipelines.wildfire_global.pipeline import start as start_wildfire_global
from project.visualization.plots import plot_tornado_and_wildfire_per_state

if __name__ == "__main__":
    try:
        get_settings()
    except ValidationError as e:
        print("Invalid environment configuration")
        for err in e.errors():
            print(f"{err['loc']}: {err['msg']}")
        sys.exit(1)

    configure_logging()
    start_tornado_usa()
    start_wildfire_global()

    engine = get_engine()
    plot_tornado_and_wildfire_per_state(engine)