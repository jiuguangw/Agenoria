#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the  MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def enumerate_labels():
    hour_labels = []
    for num in range(0, 24):
        label = str(num) + ':00'
        hour_labels.append(label)

    week_labels = []
    for num in range(0, 53):
        label = str(num)
        week_labels.append(label)

    return hour_labels, week_labels


def format_axis(ax, date_num, title):
    # Figure settings
    TITLE_FONT_SIZE = 25
    AXIS_FONT_SIZE = 15
    TITLE_HEIGHT_ADJUST = 1.05

    hour_labels, week_labels = enumerate_labels()

    ax.set_title(title, fontsize=TITLE_FONT_SIZE, y=TITLE_HEIGHT_ADJUST)
    ax.set_xlabel('Age (weeks)', fontsize=AXIS_FONT_SIZE)
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


def get_feeding_data(filename):
    # Import data
    data_feeding = pd.read_csv(filename)

    # Convert the date columns into datetime
    data_feeding['Time of feeding'] = pd.to_datetime(
        data_feeding['Time of feeding'], format='%m/%d/%Y %I:%M:%S %p')

    # Get start and end dates
    start_date = data_feeding['Time of feeding'].iloc[-1].date()
    end_date = data_feeding['Time of feeding'].iloc[0].date()

    return data_feeding, start_date, end_date


def get_diaper_data(filename):
    # Import data
    data_diaper = pd.read_csv(filename)

    # Convert the date columns into datetime
    data_diaper['Diaper time'] = pd.to_datetime(
        data_diaper['Diaper time'], format='%m/%d/%Y %I:%M:%S %p')

    # Get start and end dates
    start_date = data_diaper['Diaper time'].iloc[-1].date()
    end_date = data_diaper['Diaper time'].iloc[0].date()

    return data_diaper, start_date, end_date


def get_sleep_data(filename):
    # Import data
    data_sleep = pd.read_csv(filename)

    # Convert the date columns into datetime
    data_sleep['Begin time'] = pd.to_datetime(
        data_sleep['Begin time'], format='%m/%d/%Y %I:%M:%S %p')
    data_sleep['End time'] = pd.to_datetime(
        data_sleep['End time'], format='%m/%d/%Y %I:%M:%S %p')

    # Get start and end dates
    start_date = data_sleep['Begin time'].iloc[-1].date()
    end_date = data_sleep['Begin time'].iloc[0].date()

    return data_sleep, start_date, end_date


def plot_sleep(file_sleep, figure):
    # Import and extract sleep data
    data_sleep, start_date, end_date = get_sleep_data(file_sleep)

    # Plot setup
    ax = figure.add_subplot(111)

    date_num = 1
    offset = 0
    BAR_SIZE = 1

    # Loop through the start-end dates
    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        date_key = data_sleep['Begin time'].dt.normalize().isin(
            np.array([current_date]).astype('datetime64[ns]'))
        rows_on_date = data_sleep[date_key]

        # Plot offset from previous day, with offset as duration from midnight
        if (offset != 0):
            ax.broken_barh([(date_num, BAR_SIZE)], [0, offset])
            offset = 0

        # Loop through each row under current day, plot each session
        for index, row in rows_on_date.iterrows():
            # Start and end timestamp
            start_timestamp = row['Begin time']
            end_timestamp = row['End time']

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
    format_axis(ax, date_num, 'Sleep')


def plot_feeding(file_feeding, figure):
    # Import and extract feeding data
    data_feeding, start_date, end_date = get_feeding_data(file_feeding)

    # Plot setup
    ax = figure.add_subplot(111)
    date_num = 1

    # Loop through the start-end dates
    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        date_key = data_feeding['Time of feeding'].dt.normalize().isin(
            np.array([current_date]).astype('datetime64[ns]'))
        rows_on_date = data_feeding[date_key]

        # Loop through each row under current day, plot each session
        for index, row in rows_on_date.iterrows():
            # Start and end timestamp
            start_timestamp = row['Time of feeding']

            # Convert start timestamp to decimal hours
            start_hour = start_timestamp.hour + start_timestamp.minute / 60

            # Draw
            ax.plot(date_num, start_hour, marker='o', color='r')

        # Increment date
        date_num += 1

    # Format plot
    format_axis(ax, date_num, 'Feeding')


def plot_diapers(file_diaper, figure):
    # Import and extract feeding data
    data_diaper, start_date, end_date = get_diaper_data(file_diaper)

    # Plot setup
    ax = figure.add_subplot(111)
    date_num = 1

    # Loop through the start-end dates
    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        date_key = data_diaper['Diaper time'].dt.normalize().isin(
            np.array([current_date]).astype('datetime64[ns]'))
        rows_on_date = data_diaper[date_key]

        # Loop through each row under current day, plot each diaper
        for index, row in rows_on_date.iterrows():
            # Start and end timestamp
            start_timestamp = row['Diaper time']
            color = row['Color']

            # Convert start timestamp to decimal hours
            start_hour = start_timestamp.hour + start_timestamp.minute / 60

            # Draw
            if (color == 'yellow'):  # poop, yello
                ax.plot(date_num, start_hour, marker='o', color='b')
            elif (color == 'green'):  # poop, green
                ax.plot(date_num, start_hour, marker='o', color='g')
            elif (color == 'brown'):  # poop, brown
                ax.plot(date_num, start_hour, marker='o', color='m')
            elif (pd.isnull(color)):  # pee only, yellow
                ax.plot(date_num, start_hour, marker='o', color='y')
            else:  # poop, other colors
                ax.plot(date_num, start_hour, marker='o', color='r')

        # Increment date
        date_num += 1

    # Format plot
    format_axis(ax, date_num, 'Diapers')


def plot_24h_viz(file_sleep, file_feeding, file_diaper, output_sleep_viz, output_feeding_viz, output_diaper_viz):
    # Plot settings
    sns.set(style="darkgrid")

    sleep_figure = plt.figure()
    plot_sleep(file_sleep, sleep_figure)
    sleep_figure.set_size_inches(17, 11)
    sleep_figure.savefig(output_sleep_viz, bbox_inches='tight')
    sleep_figure.clf()

    feeding_figure = plt.figure()
    plot_feeding(file_feeding, feeding_figure)
    feeding_figure.set_size_inches(17, 11)
    feeding_figure.savefig(output_feeding_viz, bbox_inches='tight')
    feeding_figure.clf()

    diaper_figure = plt.figure()
    plot_diapers(file_diaper, diaper_figure)
    diaper_figure.set_size_inches(17, 11)
    diaper_figure.savefig(output_diaper_viz, bbox_inches='tight')
    diaper_figure.clf()
