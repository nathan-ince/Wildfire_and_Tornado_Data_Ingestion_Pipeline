import logging

from project.core import configure_logging
from project.pipelines.tornado_usa.pipeline import start as start_tornado_usa
from project.pipelines.wildfire_global.pipeline import start as start_wildfire_global

logger = logging.getLogger(__name__)

if __name__ == "__main__":
  configure_logging()
  start_tornado_usa()
  start_wildfire_global()
