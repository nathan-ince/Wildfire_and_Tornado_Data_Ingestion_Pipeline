import matplotlib.pyplot as plt
import seaborn as sns
from project.visualization.queries import tornado_counts_by_state, wildfire_counts_by_state, tornado_most_events_by_month, tornado_average_fatalities_by_magnitude, wildfire_counts_by_cause, wildfire_most_events_by_month
import calendar


STATE_NAME_TO_ABBR = {
    "California": "CA",
    "Oregon": "OR",
    "Texas": "TX",
}

MONTH_NAME_ABBR = {
    
}



def plot_tornado_and_wildfire_per_month(engine):
    df_tornado = tornado_most_events_by_month(engine)
    

    df_tornado["month_abbr"] = df_tornado["month"].apply(lambda m: calendar.month_abbr[int(m)])

    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(12, 8))


    sns.lineplot(data=df_tornado, x="month_abbr", y="tornado_count", marker="o", label="Tornadoes")



    plt.xlabel("Month") 
    plt.ylabel("Number of Events") 
    plt.title("Tornadoes vs Wildfires")
    plt.show()



def plot_tornado_most_events_by_month(engine):
    df = tornado_most_events_by_month(engine)
    df["month_name"] = df["month"].apply(lambda change_month: calendar.month_name[int(change_month)])

    plt.figure(figsize=(12, 8))

    plt.plot(df["month_name"], df["tornado_count"], marker="o", color="darkgray")

    plt.ylabel("Number of Tornado Events") 
    plt.title("Tornado Events by Month")
    plt.show()














def plot_tornado_and_wildfire_most_events_by_month(engine):
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