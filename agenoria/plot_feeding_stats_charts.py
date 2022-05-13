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
from .parse_config import parse_json_config, get_daytime_index, get_nighttime_index
from .plot_settings import mmm_plot, format_monthly_plot, export_figure

# Debug option
DEBUG = False
DEBUG_START_DATE = dt.datetime(2019, 8, 17, 0, 0, 0)
DEBUG_END_DATE = dt.datetime(2019, 9, 27, 0, 0, 0)

ALPHA_VALUE = 0.3

# Parameters from JSON
config = []


def export_feeding_text(feeding_data, key_amount, label):
    print(label + ': ', end='')
    for index, row in feeding_data.iterrows():
        print(row['Time of feeding'].strftime('%I:%M%p').lower(), end='')
        print(': ' + str(int(row[key_amount])) + ' mL; ', end='')
    print('\n', end='')


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

        # For some reason raw feeding data is not sorted by time
        rows_on_date = rows_on_date.sort_values(
            ['Time of feeding'], ascending=True)

        # Compute statistics
        sum_on_date = rows_on_date[key_amount].sum()
        mean_on_date = rows_on_date[key_amount].mean()
        max_on_date = rows_on_date[key_amount].max()
        min_on_date = rows_on_date[key_amount].min()
        sessions_on_date = rows_on_date[key_amount].count()

        # Daytime feedings
        daytime_index = get_daytime_index(rows_on_date['Time of feeding'])
        daytime_feeding = rows_on_date[daytime_index]
        daytime_sum = daytime_feeding[key_amount].sum()

        # Daytime time between feedings
        time_between_feeding = daytime_feeding['Time of feeding'].diff()
        min2hour = np.timedelta64(1, 'h')
        time_between_feeding_max = time_between_feeding.max() / min2hour
        time_between_feeding_mean = time_between_feeding.mean() / min2hour
        time_between_feeding_min = time_between_feeding.min() / min2hour

        # Nighttime feeding
        nighttime_index = get_nighttime_index(rows_on_date['Time of feeding'])
        nighttime_feeding = rows_on_date[nighttime_index]
        nighttime_sum = nighttime_feeding[key_amount].sum()

        # Print
        if (DEBUG):
            print(current_date.date())
            export_feeding_text(daytime_feeding, key_amount, 'Daytime')
            export_feeding_text(nighttime_feeding, key_amount, 'Nighttime')
            print('Total volume:', int(sum_on_date), 'mL')
            print('\n', end='')

        # Put stats in a list
        feeding_data_list.append([current_date, sum_on_date,
                                  mean_on_date, min_on_date, max_on_date,
                                  sessions_on_date, time_between_feeding_max,
                                  time_between_feeding_mean,
                                  time_between_feeding_min,
                                  daytime_sum, nighttime_sum])

    # Convert list to dataframe
    daily_data_new = pd.DataFrame(feeding_data_list, columns=[
        'date', 'sum', 'mean', 'min', 'max', 'sessions',
        'time gap max', 'time gap mean', 'time gap min',
        'daytime sum', 'nighttime sum'])

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


def plot_feeding_stats_charts(config_file):
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
    data_feeding_combined = combine_bottle_solid(data_bottle, data_solid)

    # Start date
    xlim_left = data_bottle['date'].iloc[0]
    # End date - one year or full
    if (config["output_year_one_only"]):
        xlim_right = xlim_left + relativedelta(years=1)
    else:
        xlim_right = data_bottle['date'].iloc[-1]

    # Chart 1 - Eat: Daily, Average Consumed Per Day(mL)
    mmm_plot(axarr[0, 0], data_bottle['date'], data_bottle['mean'],
             data_bottle['min'], data_bottle['max'], ALPHA_VALUE)
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

    # Chart 4 - Eat: Daytime Volume
    axarr[1, 0].plot(data_bottle['date'], data_bottle['daytime sum'],)
    axarr[1, 0].set_title('Eat: Daily Total Daytime Volume (mL)')
    axarr[1, 0].set_ylabel('Eat: Daily Total Daytime Volume (mL)')
    format_monthly_plot(axarr[1, 0], xlim_left, xlim_right)

    # Chart 5 - Eat: Nighttime Volume
    axarr[1, 1].plot(data_bottle['date'], data_bottle['nighttime sum'],)
    axarr[1, 1].set_title('Eat: Daily Total Nighttime Volume (mL)')
    axarr[1, 1].set_ylabel('Eat: Daily Total Nighttime Volume (mL)')
    format_monthly_plot(axarr[1, 1], xlim_left, xlim_right)

    # Chart 6 - Eat: Daily Total Solid Feeding (oz)
    axarr[1, 2].plot(data_solid['date'], data_solid['sum'])
    axarr[1, 2].set_title('Eat: Daily Total Solid Feeding (oz)')
    axarr[1, 2].set_ylabel('Daily Total Solid Feeding (oz)')
    format_monthly_plot(axarr[1, 2], xlim_left, xlim_right)

    # Chart 7 - Eat: Daily Total Bottle + Solid
    axarr[2, 0].plot(data_bottle['date'], data_feeding_combined)
    axarr[2, 0].set_title('Eat: Daily Total Bottle + Solid (oz)')
    axarr[2, 0].set_ylabel('Daily Total Bottle + Solid (oz)')
    format_monthly_plot(axarr[2, 0], xlim_left, xlim_right)

    # Chart 8 - Eat: Average Time Between Feedings
    mmm_plot(axarr[2, 1], data_bottle['date'], data_bottle['time gap mean'],
             data_bottle['time gap min'],
             data_bottle['time gap max'], ALPHA_VALUE)
    axarr[2, 1].set_title('Eat: Average Daytime Bottle Feeding Time Gap (Hr)')
    axarr[2, 1].set_ylabel('Eat: Average Daytime Bottle Feeding Time Gap (Hr)')
    format_monthly_plot(axarr[2, 1], xlim_left, xlim_right)

    # Export
    f.subplots_adjust(wspace=0.2, hspace=0.35)
    export_figure(f, config['output_dim_x'], config['output_dim_y'],
                  config['output_daily_feeding_stats_charts'])
