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

    # Create the tick labels
    hour_labels, week_labels = enumerate_labels(date_num)

    # Set title and axis labels
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
    data = pd.read_csv(filename, parse_dates=key)

    # Make a new column data date component only
    data['Date'] = data[key[0]].dt.normalize()

    # Get start and end dates
    start_date = data['Date'].iloc[-1]
    end_date = data['Date'].iloc[0]

    # Convert timesteamp to decimal hour
    data['timestamp_hour'] = data[key[0]].dt.hour + \
        data[key[0]].dt.minute / 60

    # Convert date to day number
    data['day_number'] = (data['Date'] - start_date).dt.days + 1

    return data


def plot_sleep_24h_viz(config_file):
    # Parse config file
    config = parse_json_config(config_file)

    # Import and extract sleep data
    data = parse_raw_data(config['data_sleep'], ['Begin time', 'End time'])

    # Convert end time timestamp to decimal hours
    data['end_timestamp_hour'] = data['End time'].dt.hour + \
        data['End time'].dt.minute / 60

    # Compute duration in decimal hours
    data['duration'] = data['end_timestamp_hour'] - data['timestamp_hour']

    # Find the index of session that extend into the next day
    index = data['End time'].dt.normalize() > data['Begin time'].dt.normalize()

    # Compute the offset duration to be plotted the next day
    data.loc[index, 'offset'] = data['end_timestamp_hour']

    # Compute the current day duration, cut off to midnight
    data.loc[index, 'duration'] = 24 - data['timestamp_hour']

    # Plot setup
    sns.set(style="darkgrid")
    figure = plt.figure()
    ax = figure.add_subplot(111)
    BAR_SIZE = 1

    # Find sessions with offsets and plot the offset with day_number+1
    data.loc[index].apply(lambda row: ax.broken_barh(
        [(row['day_number']+1, BAR_SIZE)], [0, row['offset']]), axis=1)

    # Loop through each row and plot the duration
    data.apply(lambda row: ax.broken_barh(
        [(row['day_number'], BAR_SIZE)],
        [row['timestamp_hour'], row['duration']]), axis=1)

    # Format plot
    format_axis(ax, data['day_number'].iloc[0], 'Sleep')

    # Export figure
    figure.set_size_inches(config['output_dim_x'], config['output_dim_y'])
    figure.savefig(config['output_sleep_viz'], bbox_inches='tight')
    figure.clf()


def plot_feeding_24h_viz(config_file):
    # Parse config file
    config = parse_json_config(config_file)

    # Import and extract feeding data
    data = parse_raw_data(
        config['data_feed_bottle'], ['Time of feeding'])

    # Plot setup
    sns.set(style="darkgrid")
    figure = plt.figure()
    ax = figure.add_subplot(111)

    # Loop through each row and plot
    data.apply(lambda row: ax.plot(row['day_number'], row['timestamp_hour'],
                                   marker='o', color='r'), axis=1)

    # Format plot
    format_axis(ax, data['day_number'].iloc[0], 'Feeding')

    # Export figure
    figure.set_size_inches(config['output_dim_x'], config['output_dim_y'])
    figure.savefig(config['output_feeding_viz'], bbox_inches='tight')
    figure.clf()


def map_poop_color(color):
    # Matplotlib key
    key = ''

    # Map from Glow color to matplotlib color key
    if (color == 'yellow'):  # poop, yello
        key = 'b'
    elif (color == 'green'):  # poop, green
        key = 'g'
    elif (color == 'brown'):  # poop, brown
        key = 'm'
    elif (pd.isnull(color)):  # pee only, yellow
        key = 'y'
    else:  # poop, other colors
        key = 'r'

    return key


def plot_diapers_24h_viz(config_file):
    # Parse config file
    config = parse_json_config(config_file)

    # Import and extract feeding data
    data = parse_raw_data(
        config['data_diaper'], ['Diaper time'])

    # Go through poop colors and map to matplotlib color keys
    data['Color key'] = data['Color'].apply(map_poop_color)

    # Plot setup
    sns.set(style="darkgrid")
    figure = plt.figure()
    ax = figure.add_subplot(111)

    # Loop through each row under current day, plot each diaper
    data.apply(lambda row: ax.plot(row['day_number'], row['timestamp_hour'],
                                   marker='o', color=row['Color key']), axis=1)

    # Format plot
    format_axis(ax, data['day_number'].iloc[0], 'Diapers')

    # Export figure
    figure.set_size_inches(config['output_dim_x'], config['output_dim_y'])
    figure.savefig(config['output_diaper_viz'], bbox_inches='tight')
    figure.clf()
