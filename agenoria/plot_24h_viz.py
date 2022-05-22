#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import matplotlib.pyplot as plt
import matplotlib.patches as plot_patches
import pandas as pd
import numpy as np
import seaborn as sns
from .parse_config import parse_json_config
from .plot_settings import format_24h_week_plot_vertical
from .plot_settings import format_24h_week_plot_horizontal
from .plot_settings import export_figure

config = []


def get_end_date(data, first_year_only):
    end_date = 0

    if (first_year_only):
        end_date = 365
    else:
        end_date = data.iloc[0]

    return end_date


def parse_raw_data(data, key):
    # Get start and end dates
    start_date = data['Date'].iloc[-1]

    # Convert timesteamp to decimal hour
    data['timestamp_hour'] = data[key[0]].dt.hour + \
        data[key[0]].dt.minute / 60

    # Convert date to day number
    data['day_number'] = (data['Date'] - start_date).dt.days + 1

    return data


def plot_sleep_24h_viz(config, sleep_data):
    # Import and extract sleep data
    data = parse_raw_data(sleep_data, ['Begin time', 'End time'])

    # Convert end time timestamp to decimal hours
    data['end_timestamp_hour'] = data['End time'].dt.hour + \
        data['End time'].dt.minute / 60

    # Compute duration in decimal hours
    data['duration'] = data['end_timestamp_hour'] - data['timestamp_hour']

    # Find the index of session that extend into the next day
    index = data['End time'].dt.normalize() > data['Date']

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
        [(row['day_number'] + 1, BAR_SIZE)], [0, row['offset']]), axis=1)

    # Loop through each row and plot the duration
    data.apply(lambda row: ax.broken_barh(
        [(row['day_number'], BAR_SIZE)],
        [row['timestamp_hour'], row['duration']]), axis=1)

    # End date - one year or full
    end_date = get_end_date(data['day_number'], config["output_year_one_only"])

    # Format plot - vertical or horizontal
    if (config["output_sleep_viz_orientation"] == "vertical"):
        format_24h_week_plot_vertical(ax, end_date, 'Sleep')
    else:
        format_24h_week_plot_horizontal(ax, end_date, 'Sleep')

    # Export figure
    export_figure(figure, config['output_dim_x'], config['output_dim_y'],
                  config['output_sleep_viz'])


def plot_feeding_24h_viz(config, feeding_bottle_data, feeding_solid_data):
    # Import and extract feeding data
    data_bottle = parse_raw_data(feeding_bottle_data, ['Time of feeding'])
    data_solid = parse_raw_data(feeding_solid_data, ['Time of feeding'])

    # Plot setup
    sns.set(style="darkgrid")
    figure = plt.figure()
    ax = figure.add_subplot(111)

    # Compute offset from birthday
    offset = data_solid['Date'].iloc[-1] - config['birthday']
    offset = int(offset / np.timedelta64(1, 'D'))   # Convert to day in int

    # Plot
    ax.scatter(data_bottle['day_number'], data_bottle['timestamp_hour'],
               s=25, c='r')
    ax.scatter(data_solid['day_number'] + offset, data_solid['timestamp_hour'],
               s=25, c='b')

    # Legend
    red_patch = plot_patches.Patch(color='r', label='Bottle Feeding')
    blue_patch = plot_patches.Patch(color='b', label='Solid Feeding')
    plt.legend(handles=[red_patch, blue_patch])

    # End date - one year or full
    end_date = get_end_date(
        data_bottle['day_number'], config["output_year_one_only"])

    # Format plot
    format_24h_week_plot_horizontal(ax, end_date, 'Feeding')

    # Export figure
    export_figure(figure, config['output_dim_x'], config['output_dim_y'],
                  config['output_feeding_viz'])


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


def plot_diapers_24h_viz(config, diaper_data):
    # Import and extract feeding data
    data = parse_raw_data(diaper_data, ['Diaper time'])

    # Go through poop colors and map to matplotlib color keys
    data['Color key'] = data['Color'].apply(map_poop_color)

    # Plot setup
    sns.set(style="darkgrid")
    figure = plt.figure()
    ax = figure.add_subplot(111)

    # Plot
    ax.scatter(data['day_number'], data['timestamp_hour'],
               s=25, c=data['Color key'])

    # Legend
    blue_patch = plot_patches.Patch(color='b', label='Poop, Yellow')
    green_patch = plot_patches.Patch(color='g', label='Poop, Green')
    brown_patch = plot_patches.Patch(color='m', label='Poop, Brown')
    red_patch = plot_patches.Patch(color='r', label='Poop, Others')
    yellow_patch = plot_patches.Patch(color='y', label='Pee')
    plt.legend(handles=[blue_patch, green_patch, brown_patch,
                        red_patch, yellow_patch])

    # End date - one year or full
    end_date = get_end_date(data['day_number'], config["output_year_one_only"])

    # Format plot
    format_24h_week_plot_horizontal(ax, end_date, 'Diapers')

    # Export figure
    export_figure(figure, config['output_dim_x'], config['output_dim_y'],
                  config['output_diaper_viz'])
