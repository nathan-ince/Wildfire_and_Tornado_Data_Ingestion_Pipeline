# from sqlalchemy.engine import Engine, create_engine
# from .settings import settings

# def build_engine() -> Engine:
#   host = settings.db_host
#   port = settings.db_port
#   name = settings.db_name
#   username = settings.db_username
#   password = settings.db_password
#   url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{name}"
#   return create_engine(url, pool_pre_ping=True, future=True)

# dbengine = build_engine()

from sqlalchemy.engine import Engine, create_engine
from project.core.settings import settings

def build_engine() -> Engine:
    url = (
        f"postgresql+psycopg2://{settings.db_username}:{settings.db_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )
    return create_engine(url, pool_pre_ping=True, future=True)

def get_engine() -> Engine:
    return build_engine()