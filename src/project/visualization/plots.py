import matplotlib.pyplot as plt
import seaborn as sns
from project.visualization.queries import tornado_most_events_by_month, tornado_average_fatalities_by_magnitude, wildfire_counts_by_cause
import calendar


def plot_tornado_most_events_per_month_and_year(engine):
    df_tornado = tornado_most_events_by_month(engine)

    df_tornado["month_abbr"] = df_tornado["month"].apply(lambda m: calendar.month_abbr[int(m)])

    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(12, 8))

    sns.lineplot(data=df_tornado, x="month_abbr", y="tornado_count", marker="o", label="Tornadoes")

    plt.xlabel("Month") 
    plt.ylabel("Number of Events") 
    plt.title("Tornadoes vs Wildfires")
    plt.tight_layout()
    plt.show()


def plot_tornado_average_fatalities_by_magnitude(engine):
    df = tornado_average_fatalities_by_magnitude(engine)

    fatality_colors = {
    "0": "#F6C7C3",  
    "1": "#EFA39D",
    "2": "#E0665C",
    "3": "#C51C0D",  
    "4": "#8F140A",
    "5": "#580C05"   
}

    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(12, 8))

    sns.barplot(data=df, x="magnitude", y="average_fatalities", palette=fatality_colors, label="Tornadoes")

    plt.xlabel("Tornado Magnitude")
    plt.ylabel("Average Fatalities") 
    plt.title("Average Tornado Fatalities by Magnitude")
    plt.tight_layout()
    plt.show()


def plot_wildfire_counts_by_cause(engine):
    df = wildfire_counts_by_cause(engine)

    cause_colors = {
    "Lightning": "#F4D03F",
    "Human": "#D35400",
    "Deforestation": "#27AE60",
    "Unknown": "#7F8C8D",
    "Climate Change": "#3498DB"
}

    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(12, 8))

    sns.barplot(data=df, x="cause", y="wildfire_count", palette=cause_colors, label="Wildfires")

    plt.xlabel("Wildfire Cause")
    plt.ylabel("Number of Wildfires") 
    plt.title("Wildfire Counts by Cause")
    plt.tight_layout()
    plt.show()