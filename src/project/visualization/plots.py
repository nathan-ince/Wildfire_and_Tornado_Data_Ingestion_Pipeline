import matplotlib.pyplot as plt
from project.visualization.queries import tornado_counts_by_state, wildfire_counts_by_state, tornado_most_events_by_state, wildfire_most_events_by_state, tornado_most_events_by_month, tornado_average_fatalities_by_magnitude

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


def plot_tornado_most_events_by_state(engine):
    df = tornado_most_events_by_state(engine)

    plt.bar(df["state"], df["tornado_count"])

    plt.xlabel("State")
    plt.ylabel("Number of Tornado Events") 
    plt.title("Top 3 States by Tornado Events")
    plt.show()


def plot_wildfire_most_events_by_state(engine):
    df = wildfire_most_events_by_state(engine)

    plt.bar(df["state"], df["wildfire_count"])

    plt.xlabel("State")
    plt.ylabel("Number of Tornado Events") 
    plt.title("Top 3 States by Wildfire Events")
    plt.show()


def plot_tornado_most_events_by_month(engine):
    df = tornado_most_events_by_month(engine)

    plt.bar(df["month"], df["tornado_count"])

    plt.xlabel("Month")
    plt.ylabel("Number of Tornado Events") 
    plt.title("Top 3 Months by Tornado Events")
    plt.show()


def plot_tornado_average_fatalities_by_magnitude(engine):
    df = tornado_average_fatalities_by_magnitude(engine)

    plt.bar(df["magnitude"], df["average_fatalities"])

    plt.xlabel("Tornado Magnitude")
    plt.ylabel("Average Fatalities") 
    plt.title("Average Tornado Fatalities by Magnitude")
    plt.show()