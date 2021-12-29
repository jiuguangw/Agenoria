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
from .parse_config import parse_json_config
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
    nap_index = (data_sleep['Begin time'].dt.hour > 7) & (
        data_sleep['Begin time'].dt.hour < 19)
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


def parse_glow_feeding_data(file_name, key_amount):
    # Import file
    data = pd.read_csv(file_name, parse_dates=['Time of feeding'])

    # Make a new column with date component only
    data['Date'] = data['Time of feeding'].dt.normalize()

    # Find first and last entry in column
    start_date = data['Date'].iloc[-1]
    end_date = data['Date'].iloc[0]

    if (DEBUG):
        start_date = DEBUG_START_DATE
        end_date = DEBUG_END_DATE

    # Final data
    feeding_data_list = []

    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        rows_on_date = data[data['Date'].isin([current_date])]

        # Compute statistics
        sum_on_date = rows_on_date[key_amount].sum()
        mean_on_date = rows_on_date[key_amount].mean()
        max_on_date = rows_on_date[key_amount].max()
        min_on_date = rows_on_date[key_amount].min()
        sessions_on_date = rows_on_date[key_amount].count()

        # Put stats in a list
        feeding_data_list.append([current_date, sum_on_date,
                                  mean_on_date, min_on_date, max_on_date,
                                  sessions_on_date])

    # Convert list to dataframe
    daily_data_new = pd.DataFrame(feeding_data_list, columns=[
        'date', 'sum', 'mean', 'min', 'max', 'sessions'])

    return daily_data_new


def combine_bottle_solid(data_bottle, data_solid):
    # Compute the difference in size between bottle and solids
    size_missing = data_bottle['date'].size - data_solid['date'].size

    # Create rows of zero
    zero_data = pd.DataFrame(0, index=np.arange(size_missing), columns=['sum'])

    # Append it to the front of the solid data
    solid_new = pd.concat(
        [zero_data['sum'], data_solid['sum']], axis=0, ignore_index=True)

    # Convert bottle feeding from mL to oz and add the solids
    combined = data_bottle['sum'] / 29.5735 + solid_new

    # Return combined data
    return combined


def plot_sleep_feeding_charts(config_file):
    # Matplotlib converters
    register_matplotlib_converters()

    # Style
    sns.set(style="darkgrid")
    f, axarr = plt.subplots(3, 3)

    # Import data
    global config
    config = parse_json_config(config_file)

    # Parse data
    data_bottle = parse_glow_feeding_data(
        config['data_feed_bottle'], 'Amount(ml)')
    data_solid = parse_glow_feeding_data(config['data_feed_solid'], 'Amount')
    data_sleep_daily = parse_glow_sleep_data(config['data_sleep'])
    data_feeding_combined = combine_bottle_solid(data_bottle, data_solid)

    # Start date
    xlim_left = data_bottle['date'].iloc[0]
    # End date - one year or full
    if (config["output_year_one_only"]):
        xlim_right = xlim_left + relativedelta(years=1)
    else:
        xlim_right = data_bottle['date'].iloc[-1]

    # Chart 1 - Eat: Daily, Average Consumed Per Day(mL)
    axarr[0, 0].plot(data_bottle['date'], data_bottle['mean'])
    axarr[0, 0].fill_between(data_bottle['date'], data_bottle['max'],
                             data_bottle['mean'], alpha=ALPHA_VALUE)
    axarr[0, 0].fill_between(data_bottle['date'], data_bottle['min'],
                             data_bottle['mean'], alpha=ALPHA_VALUE)
    axarr[0, 0].set_title('Eat: Daily Volume Per Session (mL)')
    axarr[0, 0].set_ylabel('Average Volume Per Session (mL)')
    format_monthly_plot(axarr[0, 0], xlim_left, xlim_right)

    # Chart 2 - Eat: Daily Number of Feeding Sessions Per Day
    axarr[0, 1].plot(data_bottle['date'], data_bottle['sessions'])
    axarr[0, 1].set_title('Eat: Daily Number of Feeding Sessions')
    axarr[0, 1].set_xlabel('Time')
    axarr[0, 1].set_ylabel('Number of Feeding Sessions')
    format_monthly_plot(axarr[0, 1], xlim_left, xlim_right)

    # Chart 3 - Eat: Daily, Daily Total Volume (mL)
    axarr[0, 2].plot(data_bottle['date'], data_bottle['sum'])
    axarr[0, 2].set_title('Eat: Daily Total Volume (mL)')
    axarr[0, 2].set_ylabel('Daily Total (mL)')
    format_monthly_plot(axarr[0, 2], xlim_left, xlim_right)

    # Chart 4 - Eat: Daily Total Solid Feeding (oz)
    axarr[1, 0].plot(data_solid['date'], data_solid['sum'])
    axarr[1, 0].set_title('Eat: Daily Total Solid Feeding (oz)')
    axarr[1, 0].set_ylabel('Daily Total Solid Feeding (oz)')
    format_monthly_plot(axarr[1, 0], xlim_left, xlim_right)

    # Chart 5 - Eat: Daily Total Bottle + Solid
    axarr[1, 1].plot(data_bottle['date'], data_feeding_combined)
    axarr[1, 1].set_title('Eat: Daily Total Bottle + Solid (oz)')
    axarr[1, 1].set_ylabel('Daily Total Bottle + Solid (oz)')
    format_monthly_plot(axarr[1, 1], xlim_left, xlim_right)

    # Chart 6 - Sleep: Daily Total Naps (7:00-19:00)
    axarr[1, 2].plot(data_sleep_daily['date'], data_sleep_daily['total_naps'])
    axarr[1, 2].set_title('Sleep: Daily Total Naps (7:00-19:00)')
    axarr[1, 2].set_ylabel('Total Naps')
    format_monthly_plot(axarr[1, 2], xlim_left, xlim_right)

    # Chart 7 - Sleep: Daily Longest Duration of Uninterrupted Sleep (Hours)
    axarr[2, 0].plot(data_sleep_daily['date'],
                     data_sleep_daily['longest_session'])
    axarr[2, 0].set_title('Sleep: Daily Longest Sleep Duration (Hr)')
    axarr[2, 0].set_ylabel('Longest Sleep Duration (Hr)')
    format_monthly_plot(axarr[2, 0], xlim_left, xlim_right)

    # Chart 8 - Sleep: Daily Total Sleep (Hours)
    axarr[2, 1].plot(data_sleep_daily['date'],
                     data_sleep_daily['total_sleep_duration'])
    axarr[2, 1].set_title('Sleep: Daily Total Sleep (Hr)')
    axarr[2, 1].set_ylabel('Total Sleep (Hr)')
    format_monthly_plot(axarr[2, 1], xlim_left, xlim_right)

    # Chart 9 - Daily Maximum Awake Duration (Hr)
    axarr[2, 2].plot(data_sleep_daily['date'],
                     data_sleep_daily['max_awake_duration'])
    axarr[2, 2].set_title('Daily Maximum Awake Duration (Hr)')
    axarr[2, 2].set_ylabel('Maximum Awake Duration (Hr)')
    format_monthly_plot(axarr[2, 2], xlim_left, xlim_right)

    # Export
    f.subplots_adjust(wspace=0.2, hspace=0.35)
    export_figure(f, config['output_dim_x'], config['output_dim_y'],
                  config['output_daily_sleep_feeding_charts'])
