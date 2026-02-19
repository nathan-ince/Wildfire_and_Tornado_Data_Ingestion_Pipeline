import matplotlib.pyplot as plt
import seaborn as sns
from project.visualization.queries import tornado_most_events_by_month, tornado_average_fatalities_by_magnitude, wildfire_counts_by_cause, wildfire_count_by_month, tornado_count_by_month
import calendar
from sqlalchemy import Engine
import pandas as pd

def plot_tornado_most_events_per_month_and_year(engine: Engine):
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


def plot_tornado_average_fatalities_by_magnitude(engine: Engine):
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


def plot_wildfire_counts_by_cause(engine: Engine):
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

month_number_name_map = {
  1: "January",
  2: "February",
  3: "March",
  4: "April",
  5: "May",
  6: "June",
  7: "July",
  8: "August",
  9: "September",
  10: "October",
  11: "November",
  12: "December"
}

month_name_number_map = {
  "January": 1,
  "February": 2,
  "March": 3,
  "April": 4,
  "May": 5,
  "June": 6,
  "July": 7,
  "August": 8,
  "September": 9,
  "October": 10,
  "November": 11,
  "December": 12
}

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def plot_counts_by_month(engine: Engine):
    df_wildfire = wildfire_count_by_month(engine)
    df_tornado = tornado_count_by_month(engine)
    
    df_tornado["month"] = df_tornado["month"].map(month_number_name_map)

    df_wildfire_total = df_wildfire["occurrences"].sum()
    df_wildfire["ratio"] = df_wildfire["occurrences"] / df_wildfire_total

    df_tornado_total = df_tornado["occurrences"].sum()
    df_tornado["ratio"] = df_tornado["occurrences"] / df_tornado_total

    df_wildfire["month"] = pd.Categorical(df_wildfire["month"], categories=month_order, ordered=True)
    df_tornado["month"] = pd.Categorical(df_tornado["month"], categories=month_order, ordered=True)

    colors = {
        "wildfire": "#ff9100",
        "tornado": "#5cdeff"
    }

    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(12, 8))

    print(df_wildfire)

    sns.lineplot(data=df_wildfire, x="month", y="ratio", marker="o", label="Wildfires")
    sns.lineplot(data=df_tornado, x="month", y="ratio", marker="o", label="Tornadoes")

    plt.xlabel("Month") 
    plt.ylabel("Ratio of Events per Month") 
    plt.title("Tornadoes vs Wildfires")
    plt.tight_layout()
    plt.show()
