from sqlalchemy import text
from sqlalchemy.engine import Engine
import pandas as pd

def tornado_counts_by_state(engine: Engine) -> pd.DataFrame:
    query = text("""
        SELECT state, COUNT(*) AS tornado_count
        FROM tornado_usa_accepted_final
        GROUP BY state
    """)
    return pd.read_sql(query, engine)


def wildfire_counts_by_state(engine: Engine) -> pd.DataFrame:
    query = text("""
        SELECT region as state, COUNT(*) AS wildfire_count
        FROM wildfire_global_accepted_final
        WHERE country = 'Usa'
        GROUP BY region
    """)
    return pd.read_sql(query, engine)