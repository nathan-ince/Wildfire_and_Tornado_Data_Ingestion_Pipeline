import matplotlib.pyplot as plt
from project.visualization.queries import tornado_counts_by_state, wildfire_counts_by_state, tornado_most_events_by_month, tornado_average_fatalities_by_magnitude, wildfire_counts_by_cause
import calendar


STATE_NAME_TO_ABBR = {
    "California": "CA",
    "Oregon": "OR",
    "Texas": "TX",
}

def plot_tornado_and_wildfire_per_state(engine):
    df_tornado = tornado_counts_by_state(engine)
    df_wildfire = wildfire_counts_by_state(engine)

    df_wildfire["state"] = df_wildfire["state"].map(STATE_NAME_TO_ABBR)
    df = df_tornado.merge(df_wildfire, on="state", how="inner")

    states = df["state"].tolist()

    plt.bar(states, df["tornado_count"], label="Tornadoes")
    plt.bar(
        states,
        df["wildfire_count"],
        bottom=df["tornado_count"],
        label="Wildfires",
    )

    plt.xlabel("State")
    plt.ylabel("Number of Events") 
    plt.title("Tornadoes vs Wildfires by State")

    plt.grid(axis="y")           
    plt.legend()
    plt.show()


def plot_tornado_most_events_by_month(engine):
    df = tornado_most_events_by_month(engine)
    df["month_name"] = df["month"].apply(lambda change_month: calendar.month_name[int(change_month)])

    plt.figure(figsize=(12, 8))

    plt.plot(df["month_name"], df["tornado_count"], marker="o", color="darkgray")

    plt.ylabel("Number of Tornado Events") 
    plt.title("Tornado Events by Month")
    plt.show()


def plot_tornado_average_fatalities_by_magnitude(engine):
    df = tornado_average_fatalities_by_magnitude(engine)

    plt.figure(figsize=(8, 5))

    plt.bar(df["magnitude"], df["average_fatalities"], color="darkred")

    plt.xlabel("Tornado Magnitude")
    plt.ylabel("Average Fatalities") 
    plt.title("Average Tornado Fatalities by Magnitude")
    plt.show()


def plot_wildfire_counts_by_cause(engine):
    df = wildfire_counts_by_cause(engine)

    plt.figure(figsize=(8, 5))

    plt.bar(df["cause"], df["wildfire_count"], color="darkorange")

    plt.xlabel("Wildfire Cause")
    plt.ylabel("Number of Wildfires") 
    plt.title("Wildfire Counts by Cause")
    plt.show()