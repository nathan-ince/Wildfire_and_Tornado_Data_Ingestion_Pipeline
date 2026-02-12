import logging

from project.core import configure_logging
from project.groups import tornado_usa, wildfire_global

logger = logging.getLogger(__name__)

if __name__ == "__main__":
  configure_logging()
  # tornado_usa.start()
  wildfire_global.start()
