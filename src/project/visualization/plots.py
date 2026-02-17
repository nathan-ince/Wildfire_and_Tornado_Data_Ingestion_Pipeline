import matplotlib.pyplot as plt
from project.visualization.queries import tornado_counts_by_state, wildfire_counts_by_state

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