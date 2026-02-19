from sqlalchemy import text
from sqlalchemy.engine import Engine
import pandas as pd


def tornado_most_events_by_month(engine: Engine) -> pd.DataFrame:
    query = text("""
        SELECT year, month, COUNT(*) AS tornado_count
        FROM tornado_usa_accepted_final
        GROUP BY year, month
        ORDER BY year, month
    """)
    return pd.read_sql(query, engine)


def tornado_average_fatalities_by_magnitude(engine: Engine) -> pd.DataFrame:
    query = text("""
        SELECT magnitude, AVG(fatality_count) AS average_fatalities
        FROM tornado_usa_accepted_final
        GROUP BY magnitude
        ORDER BY magnitude
    """)
    return pd.read_sql(query, engine)


def wildfire_counts_by_cause(engine: Engine) -> pd.DataFrame:
    query = text("""
        SELECT cause, COUNT(*) AS wildfire_count
        FROM wildfire_global_accepted_final
        GROUP BY cause
        ORDER BY wildfire_count
    """)
    return pd.read_sql(query, engine)

def wildfire_count_by_month(engine: Engine) -> pd.DataFrame:
    query = text("SELECT count(*) FROM wildfire_global_accepted_final GROUP BY month")
    return pd.read_sql_query(query, engine)

def tornado_count_by_month(engine: Engine) -> pd.DataFrame:
    query = text("SELECT count(*) FROM tornado_usa_accepted_final GROUP BY month")
    return pd.read_sql_query(query, engine)
