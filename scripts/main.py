from dotenv import load_dotenv
load_dotenv()


from pydantic import ValidationError
import sys


from project.core.settings import get_settings
from project.core import configure_logging
from project.core.db import get_engine
from project.pipelines.tornado_usa.pipeline import start as start_tornado_usa
from project.pipelines.wildfire_global.pipeline import start as start_wildfire_global
from project.visualization.plots import plot_tornado_most_events_per_month_and_year, plot_tornado_average_fatalities_by_magnitude, plot_wildfire_counts_by_cause, plot_counts_by_month

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

    # engine = get_engine()
    # plot_tornado_most_events_per_month_and_year(engine)
    # plot_tornado_average_fatalities_by_magnitude(engine)
    # plot_wildfire_counts_by_cause(engine)
    # plot_counts_by_month(engine)