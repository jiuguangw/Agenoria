import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from matplotlib.ticker import MaxNLocator

import matplotlib.dates as dt


def enumerate_labels():
    hour_labels = []
    for num in range(0, 24):
        label = str(num) + ':00'
        hour_labels.append(label)

    week_labels = []
    for num in range(0, 52):
        label = 'Wk ' + str(num)
        week_labels.append(label)

    months_labels = []
    for num in range(0, 12):
        label = 'Month ' + str(num)
        months_labels.append(label)

    return hour_labels, week_labels, months_labels


def format_axis(ax, ax2, date_num, title):
        # Figure settings
    TITLE_FONT_SIZE = 25
    AXIS_FONT_SIZE = 15
    TITLE_HEIGHT_ADJUST = 1.05

    hour_labels, week_labels, months_labels = enumerate_labels()

    ax.set_title(title, fontsize=TITLE_FONT_SIZE, y=TITLE_HEIGHT_ADJUST)
    ax.set_xlabel('Age', fontsize=AXIS_FONT_SIZE)
    ax.set_ylabel('Time of Day', fontsize=AXIS_FONT_SIZE)

    # Format y axis - clock time
    ax.set_ylim(0, 24)
    ax.yaxis.set_ticks(np.arange(0, 24, 1))
    ax.set_yticklabels(hour_labels)
    ax.invert_yaxis()

    # Format x axis - bottom, week number
    ax.set_xlim(1, date_num)
    ax.xaxis.set_ticks(np.arange(1, date_num, 7))
    ax.set_xticklabels(week_labels)

    # Format x axis - top, month number. Todo: bug here
    ax2.set_xlim(1, date_num)
    ax2.xaxis.set_ticks(np.arange(1, date_num, 30))
    ax2.set_xticklabels(months_labels)


def get_feeding_data(filename):
     # Import data
    data = pd.read_csv(filename)

    # Convert the date columns into datetime
    data['start_time_label'] = pd.to_datetime(
        data['start_time_label'], format='%Y/%m/%d %H:%M:%S')

    # Get start and end dates
    start_date = data['start_time_label'].iloc[-1].date()
    end_date = data['start_time_label'].iloc[0].date()

    return data, start_date, end_date


def get_sleep_data(filename):
     # Import data
    data = pd.read_csv(filename)

    # Convert the date columns into datetime
    data['start_time_label'] = pd.to_datetime(
        data['start_time_label'], format='%Y/%m/%d %H:%M:%S')
    data['end_time_label'] = pd.to_datetime(
        data['end_time_label'], format='%Y/%m/%d %H:%M:%S')

    # Separate sleep and diaper data
    data_sleep = data.loc[data['key'] == "sleep"]

    # Get start and end dates
    start_date = data_sleep['start_time_label'].iloc[-1].date()
    end_date = data_sleep['start_time_label'].iloc[0].date()

    return data_sleep, start_date, end_date


def plot_sleep(figure):
    # Import and extract sleep data
    data_sleep, start_date, end_date = get_sleep_data(
        'data/glow_sleep_diaper_sleep.csv')

    # Plot setup
    ax = figure.add_subplot(111)
    ax2 = ax.twiny()

    date_num = 1
    offset = 0
    BAR_SIZE = 1

    # Loop through the start-end dates
    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        date_key = data_sleep['start_time_label'].dt.normalize().isin(
            np.array([current_date]).astype('datetime64[ns]'))
        rows_on_date = data_sleep[date_key]

        # Plot offset from previous day, with offset as duration from midnight
        if (offset != 0):
            ax.broken_barh([(date_num, BAR_SIZE)], [0, offset])
            offset = 0

        # Loop through each row under current day, plot each session
        for index, row in rows_on_date.iterrows():
            # Start and end timestamp
            start_timestamp = row['start_time_label']
            end_timestamp = row['end_time_label']

            # Convert start timestamp to decimal hours
            start_hour = start_timestamp.hour + start_timestamp.minute / 60

            # if the session's end time extends to next day, calculate offset
            if(end_timestamp.date() > start_timestamp.date()):
                # Set end time to 24:00
                end_hour = 24

                # Calculate offset from midnight - end time
                offset = end_timestamp.hour + end_timestamp.minute / 60
            else:  # For same day sessions, end time is standard
                end_hour = end_timestamp.hour + end_timestamp.minute / 60

            # Calculate duration
            duration = end_hour - start_hour

            # Draw
            ax.broken_barh([(date_num, BAR_SIZE)], [start_hour, duration])
        # Increment date
        date_num += 1

    # Format plot
    format_axis(ax, ax2, date_num, 'Sleep')


def plot_feeding(figure):
    # Import and extract feeding data
    data_feeding, start_date, end_date = get_feeding_data(
        'data/glow_daily_feeding.csv')

    # Plot setup
    ax = figure.add_subplot(111)
    ax2 = ax.twiny()
    date_num = 1

    # Loop through the start-end dates
    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        date_key = data_feeding['start_time_label'].dt.normalize().isin(
            np.array([current_date]).astype('datetime64[ns]'))
        rows_on_date = data_feeding[date_key]

        # Loop through each row under current day, plot each session
        for index, row in rows_on_date.iterrows():
            # Start and end timestamp
            start_timestamp = row['start_time_label']

            # Convert start timestamp to decimal hours
            start_hour = start_timestamp.hour + start_timestamp.minute / 60

            # Draw
            ax.plot(date_num, start_hour, marker='o', color='r')

        # Increment date
        date_num += 1

    # Format plot
    format_axis(ax, ax2, date_num, 'Feeding')


def main():
    # Plot settings
    sns.set(style="darkgrid")

    sleep_figure = plt.figure()
    plot_sleep(sleep_figure)
    sleep_figure.set_size_inches(18, 12)
    sleep_figure.savefig("Baby_Stats_sleep.pdf", bbox_inches='tight')
    sleep_figure.clf()

    feeding_figure = plt.figure()
    plot_feeding(feeding_figure)
    feeding_figure.set_size_inches(18, 12)
    feeding_figure.savefig("Baby_Stats_feeding.pdf", bbox_inches='tight')
    feeding_figure.clf()


main()
