#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import datetime as dt
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from .parse_config import parse_json_config, get_daytime_index
from .plot_settings import format_monthly_plot, export_figure

# Debug option
DEBUG = False
DEBUG_START_DATE = dt.datetime(2019, 8, 17, 0, 0, 0)
DEBUG_END_DATE = dt.datetime(2019, 9, 27, 0, 0, 0)

ALPHA_VALUE = 0.3

# Parameters from JSON
config = []


def parse_glow_sleep_data(file_name):
    # Import file
    data_sleep = pd.read_csv(file_name, parse_dates=['Begin time', 'End time'])

    # Make a new column with date component only
    data_sleep['Date'] = data_sleep['Begin time'].dt.normalize()

    # Find first and last entry in column
    start_date = data_sleep['Date'].iloc[-1]
    end_date = data_sleep['Date'].iloc[0]

    if (DEBUG):
        start_date = DEBUG_START_DATE
        end_date = DEBUG_END_DATE

    sleep_data_list = []
    offset = 0

    # For some reason raw sleep data is not sorted by time
    data_sleep = data_sleep.sort_values(['Begin time'], ascending=False)

    # Label each daytime nap session
    nap_index = get_daytime_index(data_sleep['Begin time'])
    data_sleep.loc[nap_index, 'daytime_nap'] = 1

    # Get duration for each row, then convert to hours
    data_sleep['duration'] = data_sleep['End time'] - data_sleep['Begin time']
    data_sleep['duration'] = data_sleep['duration'] / np.timedelta64(1, 'h')

    # Find the index of session that extend into the next day
    index = data_sleep['End time'].dt.normalize() > data_sleep['Date']

    # Compute the offset duration to be plotted the next day
    sleep_offset = data_sleep.loc[index, 'End time']
    data_sleep.loc[index, 'offset'] = sleep_offset.dt.hour + \
        sleep_offset.dt.minute / 60

    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        rows_on_date = data_sleep[data_sleep['Date'].isin([current_date])]

        # Compute number of nap sessions
        nap_sessions_on_date = rows_on_date['daytime_nap'].count()

        # Get total sleep duration
        total_sleep_duration = rows_on_date['duration'].sum()

        # Add offset from previous day
        total_sleep_duration += offset

        # Catch session that extend past midnight, subtract from duration
        offset = rows_on_date['offset'].sum()
        total_sleep_duration -= offset

        # Longest session
        longest_session = rows_on_date['duration'].max()

        # Remove all sleep sessions less than two minutes
        SLEEP_THRESHOLD = 0.0333333  # two minutes -> hours
        filtered = rows_on_date[rows_on_date['duration'] > SLEEP_THRESHOLD]

        # Compute longest awake time - begin (current time) -  end (next row)
        end_time_shifted = filtered['End time'].shift(-1)
        awake_duration = filtered['Begin time'] - end_time_shifted
        max_awake_duration = awake_duration.max() / np.timedelta64(1, 'h')

        # Put stats in a list
        sleep_data_list.append(
            [current_date, nap_sessions_on_date, total_sleep_duration,
             longest_session, max_awake_duration])

    # Convert list to dataframe
    data_sleep_daily = pd.DataFrame(
        sleep_data_list, columns=['date', 'total_naps', 'total_sleep_duration',
                                  'longest_session', 'max_awake_duration'])

    return data_sleep_daily


def plot_sleep_stats_charts(config_file):
    # Matplotlib converters
    register_matplotlib_converters()

    # Style
    sns.set(style="darkgrid")
    f, axarr = plt.subplots(2, 2)

    # Import data
    global config
    config = parse_json_config(config_file)

    # Parse data
    data_sleep_daily = parse_glow_sleep_data(config['data_sleep'])

    # Start date
    xlim_left = data_sleep_daily['date'].iloc[0]
    # End date - one year or full
    if (config["output_year_one_only"]):
        xlim_right = xlim_left + relativedelta(years=1)
    else:
        xlim_right = data_sleep_daily['date'].iloc[-1]

    # Chart 1 - Sleep: Daily Total Naps (7:00-19:00)
    axarr[0, 0].plot(data_sleep_daily['date'], data_sleep_daily['total_naps'])
    axarr[0, 0].set_title('Sleep: Daily Total Naps (7:00-19:00)')
    axarr[0, 0].set_ylabel('Total Naps')
    format_monthly_plot(axarr[0, 0], xlim_left, xlim_right)

    # Chart 2 - Sleep: Daily Longest Duration of Uninterrupted Sleep (Hours)
    axarr[0, 1].plot(data_sleep_daily['date'],
                     data_sleep_daily['longest_session'])
    axarr[0, 1].set_title('Sleep: Daily Longest Sleep Duration (Hr)')
    axarr[0, 1].set_ylabel('Longest Sleep Duration (Hr)')
    format_monthly_plot(axarr[0, 1], xlim_left, xlim_right)

    # Chart 3 - Sleep: Daily Total Sleep (Hours)
    axarr[1, 0].plot(data_sleep_daily['date'],
                     data_sleep_daily['total_sleep_duration'])
    axarr[1, 0].set_title('Sleep: Daily Total Sleep (Hr)')
    axarr[1, 0].set_ylabel('Total Sleep (Hr)')
    format_monthly_plot(axarr[1, 0], xlim_left, xlim_right)

    # Chart 4 - Daily Maximum Awake Duration (Hr)
    axarr[1, 1].plot(data_sleep_daily['date'],
                     data_sleep_daily['max_awake_duration'])
    axarr[1, 1].set_title('Daily Maximum Awake Duration (Hr)')
    axarr[1, 1].set_ylabel('Maximum Awake Duration (Hr)')
    format_monthly_plot(axarr[1, 1], xlim_left, xlim_right)

    # Export
    f.subplots_adjust(wspace=0.2, hspace=0.35)
    export_figure(f, config['output_dim_x'], config['output_dim_y'],
                  config['output_daily_sleep_stats_charts'])
