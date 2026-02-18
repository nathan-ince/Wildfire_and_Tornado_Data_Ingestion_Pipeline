from functools import lru_cache
from sqlalchemy.engine import Engine, create_engine
from project.core.settings import get_settings

def build_engine() -> Engine:
    s = get_settings()
    url = f"postgresql+psycopg2://{s.db_username}:{s.db_password}@{s.db_host}:{s.db_port}/{s.db_name}"
    return create_engine(url, pool_pre_ping=True, future=True)

@lru_cache
def get_engine() -> Engine:
    return build_engine()