# ################################################################################################

# import logging

# from tests import configure_logging
# from pytest import fixture
# from sqlalchemy.exc import SQLAlchemyError

# from project.core import dbengine

# ################################################################################################

# configure_logging()

# ################################################################################################

# @fixture
# def connection():
#   logger = logging.getLogger(__name__)
#   try:
#     logger.info("Establishing Database Connection")
#     with dbengine.connect() as connection:
#       logger.info("Database Connection Established")
#       yield connection
#   except SQLAlchemyError:
#     logger.error("SQLAlchemyError: Failed to Establish Database Connection")
#     raise
#   except:
#     logger.error("Unknown Error: Failed to Establish Database")
#   finally:
#     logger.info("Database Connection Fixture Destroyed")

# ################################################################################################
