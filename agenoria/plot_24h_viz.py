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
from .parse_config import parse_json_config

config = []


def enumerate_labels(date_num):
    hour_labels = []
    for num in range(0, 24):
        label = str(num) + ':00'
        hour_labels.append(label)

    week_labels = []
    for num in range(0, int(round(date_num / 7))):
        label = str(num)
        week_labels.append(label)

    return hour_labels, week_labels


def format_axis(ax, date_num, title):
    # Figure settings
    TITLE_FONT_SIZE = 25
    AXIS_FONT_SIZE = 15
    TITLE_HEIGHT_ADJUST = 1.05

    hour_labels, week_labels = enumerate_labels(date_num)

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


def parse_raw_data(filename, key):
    # Import data
    data = pd.read_csv(filename)

    # Convert the date columns into datetime
    data[key] = pd.to_datetime(
        data[key], format='%m/%d/%Y %I:%M:%S %p')

    # Make a new column data date component only
    data['Date'] = data[key].dt.normalize()

    # Get start and end dates
    start_date = data['Date'].iloc[-1]
    end_date = data['Date'].iloc[0]

    return data, start_date, end_date


def get_sleep_data(filename):
    # Import data
    data_sleep = pd.read_csv(filename)

    # Convert the date columns into datetime
    data_sleep['Begin time'] = pd.to_datetime(
        data_sleep['Begin time'], format='%m/%d/%Y %I:%M:%S %p')
    data_sleep['End time'] = pd.to_datetime(
        data_sleep['End time'], format='%m/%d/%Y %I:%M:%S %p')

    # Make a new column with date component only
    data_sleep['Date'] = data_sleep['Begin time'].dt.normalize()

    # Get start and end dates
    start_date = data_sleep['Date'].iloc[-1]
    end_date = data_sleep['Date'].iloc[0]

    return data_sleep, start_date, end_date


def plot_sleep(figure):
    # Import and extract sleep data
    data_sleep, start_date, end_date = get_sleep_data(config['data_sleep'])

    # Plot setup
    ax = figure.add_subplot(111)

    date_num = 1
    offset = 0
    BAR_SIZE = 1

    # Loop through the start-end dates
    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        rows_on_date = data_sleep[data_sleep['Date'].isin([current_date])]

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


def plot_feeding(figure):
    # Import and extract feeding data
    data_feeding, start_date, end_date = parse_raw_data(
        config['data_feed_bottle'], 'Time of feeding')

    # Plot setup
    ax = figure.add_subplot(111)
    date_num = 1

    # Loop through the start-end dates
    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        rows_on_date = data_feeding[data_feeding['Date'].isin([current_date])]

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


def plot_diapers(figure):
    # Import and extract feeding data
    data_diaper, start_date, end_date = parse_raw_data(
        config['data_diaper'], 'Diaper time')

    # Plot setup
    ax = figure.add_subplot(111)
    date_num = 1

    # Loop through the start-end dates
    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        rows_on_date = data_diaper[data_diaper['Date'].isin([current_date])]

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


def plot_24h_viz(config_file):
    # Import data
    global config
    config = parse_json_config(config_file)

    # Plot settings
    sns.set(style="darkgrid")

    sleep_figure = plt.figure()
    plot_sleep(sleep_figure)
    sleep_figure.set_size_inches(
        config['output_dim_x'], config['output_dim_y'])
    sleep_figure.savefig(config['output_sleep_viz'], bbox_inches='tight')
    sleep_figure.clf()

    feeding_figure = plt.figure()
    plot_feeding(feeding_figure)
    feeding_figure.set_size_inches(
        config['output_dim_x'], config['output_dim_y'])
    feeding_figure.savefig(config['output_feeding_viz'], bbox_inches='tight')
    feeding_figure.clf()

    diaper_figure = plt.figure()
    plot_diapers(diaper_figure)
    diaper_figure.set_size_inches(
        config['output_dim_x'], config['output_dim_y'])
    diaper_figure.savefig(config['output_diaper_viz'], bbox_inches='tight')
    diaper_figure.clf()
