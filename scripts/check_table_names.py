import logging

from psycopg2 import OperationalError
from sqlalchemy import inspect
from sqlalchemy.exc import MultipleResultsFound, NoResultFound, SQLAlchemyError
from sqlalchemy.sql import text

from project.core import dbengine, configure_logging

logger = logging.getLogger(__name__)
inspector = inspect(dbengine)

def check_table_names():
  select_version_statement = text("SELECT version();")
  with dbengine.connect() as db:
    try:
      result = db.execute(select_version_statement)
      version = result.scalar_one()
      logger.info("Postgres Version = %s", version)
      logger.info("Table Names = %s", inspector.get_table_names(schema="public"))
    except NoResultFound:
      logger.debug("No Result Found")
      logger.debug("There should be one and only one result.")
    except MultipleResultsFound:
      logger.debug("Multiple Results Found")
      logger.debug("There should be one and only one result.")
    except SQLAlchemyError:
      logger.error("Unknown SQL Alchemy Error")
    except Exception:
      logger.error("Unknown Error")

__all__ = ["check_table_names"]

if __name__ == "__main__":
  configure_logging()
  check_table_names()
