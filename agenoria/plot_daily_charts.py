#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the  MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.dates import MonthLocator, DateFormatter
from pandas.plotting import register_matplotlib_converters
from .parse_config import parse_json_config

DEBUG = False

# Cold Formula
# DEBUG_START_DATE = dt.datetime(2019, 7, 14, 0, 0, 0)
# DEBUG_END_DATE = dt.datetime(2019, 7, 25, 0, 0, 0)

# AOM 2019
# DEBUG_START_DATE = dt.datetime(2019, 8, 6, 0, 0, 0)
# DEBUG_END_DATE = dt.datetime(2019, 8, 18, 0, 0, 0)

# Weight loss (daycare)
DEBUG_START_DATE = dt.datetime(2019, 8, 17, 0, 0, 0)
DEBUG_END_DATE = dt.datetime(2019, 9, 27, 0, 0, 0)

# Settings
TITLE_FONT_SIZE = 10
AXIS_FONT_SIZE = 8
ALPHA_VALUE = 0.3

config = []


def format_plot(date_data, plot_object):
    axis_font_size = 8

    plot_object.set_xlim(date_data.iloc[0],
                         date_data.iloc[-1])

    if(DEBUG):
        plot_object.tick_params(labelsize=axis_font_size)
        plot_object.set_xticks(plot_object.get_xticks()[::1])
        plot_object.xaxis.set_major_formatter(DateFormatter("%m/%d"))
    else:
        plot_object.tick_params(labelsize=axis_font_size)
        plot_object.set_xticks(plot_object.get_xticks()[::1])
        plot_object.xaxis.set_major_locator(
            MonthLocator(range(1, 13), bymonthday=1, interval=1))
        plot_object.xaxis.set_major_formatter(DateFormatter("%b"))


def parse_glow_diaper_data(file_name):
    # Import file
    data_diaper = pd.read_csv(file_name)

    # Convert date column to datetime
    data_diaper['Diaper time'] = pd.to_datetime(
        data_diaper['Diaper time'], format='%m/%d/%Y %I:%M:%S %p')

    # Find first and last entry in column
    start_date = data_diaper['Diaper time'].iloc[-1].date()
    end_date = data_diaper['Diaper time'].iloc[0].date()

    if (DEBUG):
        start_date = DEBUG_START_DATE
        end_date = DEBUG_END_DATE

    # Final data
    diaper_data_list = []
    total_diaper_count = 0

    # Diaper
    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        date_key = data_diaper['Diaper time'].dt.normalize().isin(
            np.array([current_date]).astype('datetime64[ns]'))
        rows_on_date = data_diaper[date_key]

        # Compute total diaper count
        total_diaper_count += rows_on_date['In the diaper'].count()

        # Separate pees and poops
        total_pee_count = 0
        total_poop_count = 0
        for index, diaper_event in rows_on_date.iterrows():
            key = diaper_event['In the diaper']
            if (key == 'pee'):  # Pee only
                total_pee_count += 1
            elif (key == 'poo'):
                total_poop_count += 1
            else:
                total_pee_count += 1
                total_poop_count += 1

        # Put stats in a list
        diaper_data_list.append(
            [current_date, total_diaper_count, total_pee_count, total_poop_count])

        # Convert list to dataframe
        daily_diaper_data = pd.DataFrame(
            diaper_data_list, columns=['date', 'total_diaper_count', 'pee_count', 'poop_count'])

    return daily_diaper_data


def parse_glow_sleep_data(file_name):
    # Import file
    data_sleep = pd.read_csv(file_name)

    # Convert date column to datetime
    data_sleep['Begin time'] = pd.to_datetime(
        data_sleep['Begin time'], format='%m/%d/%Y %I:%M:%S %p')
    data_sleep['End time'] = pd.to_datetime(
        data_sleep['End time'], format='%m/%d/%Y %I:%M:%S %p')

    # Find first and last entry in column
    start_date = data_sleep['Begin time'].iloc[-1].date()
    end_date = data_sleep['Begin time'].iloc[0].date()

    if (DEBUG):
        start_date = DEBUG_START_DATE
        end_date = DEBUG_END_DATE

    sleep_data_list = []
    offset = 0

    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        date_key = data_sleep['Begin time'].dt.normalize().isin(
            np.array([current_date]).astype('datetime64[ns]'))
        rows_on_date = data_sleep[date_key]

        # For some reason raw sleep data is not sorted by time
        rows_on_date = rows_on_date.sort_values(
            ['Begin time'], ascending=False)

        # Compute number of nap sessions
        nap_sessions_on_date = 0

        for index, sleep_session in rows_on_date.iterrows():
            timestamp = sleep_session['Begin time']
            time7am = timestamp.replace(
                hour=7, minute=0, second=0, microsecond=0)
            time7pm = timestamp.replace(
                hour=19, minute=0, second=0, microsecond=0)
            if (timestamp > time7am) and (timestamp < time7pm):
                nap_sessions_on_date += 1

        # Total sleep

        # Get duration for each row, then sum
        elapsed_time = rows_on_date['End time'] - \
            rows_on_date['Begin time']
        total_sleep_duration = elapsed_time.sum().total_seconds()

        # Add offset from previous day
        total_sleep_duration += offset

        # Get the first row in the block
        start_last = rows_on_date['Begin time'].iloc[0]
        end_last = rows_on_date['End time'].iloc[0]

        # Catch session that extend past midnight
        if(end_last.date() > start_last.date()):  # if extends to next day
            midnight = end_last.replace(
                hour=0, minute=0, second=0, microsecond=0)

            # Subtract duration from today's total
            offset = (end_last - midnight).total_seconds()
            total_sleep_duration -= offset
            # Keep the offset to add to tomorrow's total
        else:
            offset = 0

        # Convert to hours
        total_sleep_duration = total_sleep_duration // 3600

        # Longest session
        longest_session = elapsed_time.max().total_seconds() // 3600

        # Longest awake duration

        # Remove all sleep sessions less than two minutes
        SLEEP_THRESHOLD = dt.timedelta(minutes=2)
        sleep_filtered = rows_on_date[elapsed_time > SLEEP_THRESHOLD]

        # Compute awake time - begin (current time) -  end (next row)
        end_time_shifted = sleep_filtered['End time'].shift(-1)
        awake_duration = sleep_filtered['Begin time'] - end_time_shifted
        max_awake_duration = awake_duration.max().total_seconds() // 3600

        # Put stats in a list
        sleep_data_list.append(
            [current_date, nap_sessions_on_date, total_sleep_duration, longest_session, max_awake_duration])

    # Convert list to dataframe
    daily_sleep_data = pd.DataFrame(
        sleep_data_list, columns=['date', 'total_naps', 'total_sleep_duration', 'longest_session', 'max_awake_duration'])

    return daily_sleep_data


def parse_glow_feeding_data(file_name, key_amount):
    # Import file
    data = pd.read_csv(file_name)

    # Convert date column to datetime
    data['Time of feeding'] = pd.to_datetime(
        data['Time of feeding'], format='%m/%d/%Y %I:%M:%S %p')

    # Find first and last entry in column
    start_date = data['Time of feeding'].iloc[-1].date()
    end_date = data['Time of feeding'].iloc[0].date()

    if (DEBUG):
        start_date = DEBUG_START_DATE
        end_date = DEBUG_END_DATE

    # Final data
    feeding_data_list = []

    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        date_key = data['Time of feeding'].dt.normalize().isin(
            np.array([current_date]).astype('datetime64[ns]'))
        rows_on_date = data[date_key]

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


def combine_bottle_solid(glow_bottle_data, glow_solid_data):
    # Compute the difference in size between bottle and solids
    size_missing = glow_bottle_data['date'].size - glow_solid_data['date'].size

    # Create rows of zero
    zero_data = pd.DataFrame(0, index=np.arange(size_missing), columns=['sum'])

    # Append it to the front of the solid data
    solid_new = pd.concat(
        [zero_data['sum'], glow_solid_data['sum']], axis=0, ignore_index=True)

    # Convert bottle feeding from mL to oz and add the solids
    combined = glow_bottle_data['sum'] / 29.5735 + solid_new

    # Return combined data
    return combined


def plot_daily_charts(config_file):
    # Matplotlib converters
    register_matplotlib_converters()

    # Style
    sns.set(style="darkgrid")
    f, axarr = plt.subplots(4, 3)

    # Import data
    global config
    config = parse_json_config(config_file)

    # Parse data
    glow_bottle_data = parse_glow_feeding_data(
        config['data_feed_bottle'], 'Amount(ml)')
    glow_solid_data = parse_glow_feeding_data(
        config['data_feed_solid'], 'Amount')
    daily_diaper_data = parse_glow_diaper_data(config['data_diaper'])
    daily_sleep_data = parse_glow_sleep_data(config['data_sleep'])
    glow_combined_feeding_data = combine_bottle_solid(
        glow_bottle_data, glow_solid_data)

    # Chart 1 - Eat: Daily, Average Consumed Per Day(mL)
    axarr[0, 0].plot(glow_bottle_data['date'],
                     glow_bottle_data['mean'])
    axarr[0, 0].fill_between(
        glow_bottle_data['date'].values, glow_bottle_data['mean'],
        glow_bottle_data['max'], alpha=ALPHA_VALUE)
    axarr[0, 0].fill_between(
        glow_bottle_data['date'].values, glow_bottle_data['mean'],
        glow_bottle_data['min'], alpha=ALPHA_VALUE)
    axarr[0, 0].set_title('Eat: Daily Volume Per Session (mL)',
                          fontsize=TITLE_FONT_SIZE)
    axarr[0, 0].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[0, 0].set_ylabel(
        'Average Volume Per Session (mL)', fontsize=AXIS_FONT_SIZE)
    axarr[0, 0].yaxis.set_ticks(np.arange(0, 280, 30))
    format_plot(glow_bottle_data['date'], axarr[0, 0])

    # Chart 2 - Eat: Daily Number of Feeding Sessions Per Day
    axarr[0, 1].plot(glow_bottle_data['date'],
                     glow_bottle_data['sessions'])
    axarr[0, 1].set_title('Eat: Daily Number of Feeding Sessions',
                          fontsize=TITLE_FONT_SIZE)
    axarr[0, 1].set_xlabel('Time', fontsize=AXIS_FONT_SIZE)
    axarr[0, 1].set_ylabel('Number of Feeding Sessions',
                           fontsize=AXIS_FONT_SIZE)
    axarr[0, 1].yaxis.set_ticks(np.arange(4, 15, 2))
    format_plot(glow_bottle_data['date'], axarr[0, 1])

    # Chart 3 - Eat: Daily, Daily Total Volume (mL)
    axarr[0, 2].plot(glow_bottle_data['date'],
                     glow_bottle_data['sum'])
    axarr[0, 2].set_title('Eat: Daily Total Volume (mL)',
                          fontsize=TITLE_FONT_SIZE)
    axarr[0, 2].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[0, 2].set_ylabel('Daily Total (mL)', fontsize=AXIS_FONT_SIZE)
    axarr[0, 2].yaxis.set_ticks(np.arange(0, 1200, 200))
    format_plot(glow_bottle_data['date'], axarr[0, 2])

    # Chart 4 - Eat: Daily Total Solid Feeding (oz)
    axarr[1, 0].plot(glow_solid_data['date'],
                     glow_solid_data['sum'])
    axarr[1, 0].set_title('Eat: Daily Total Solid Feeding (oz)',
                          fontsize=TITLE_FONT_SIZE)
    axarr[1, 0].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[1, 0].set_ylabel(
        'Daily Total Solid Feeding (oz)', fontsize=AXIS_FONT_SIZE)
    format_plot(glow_bottle_data['date'], axarr[1, 0])

    # Chart 5 - Eat: Daily Total Bottle + Solid
    axarr[1, 1].plot(glow_bottle_data['date'],
                     glow_combined_feeding_data)
    axarr[1, 1].set_title('Eat: Daily Total Bottle + Solid (oz)',
                          fontsize=TITLE_FONT_SIZE)
    axarr[1, 1].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[1, 1].set_ylabel(
        'Daily Total Bottle + Solid (oz)', fontsize=AXIS_FONT_SIZE)
    format_plot(glow_bottle_data['date'], axarr[1, 1])

    # Chart 6 - Sleep: Daily Total Naps (7:00-19:00)
    axarr[1, 2].plot(daily_sleep_data['date'],
                     daily_sleep_data['total_naps'])
    axarr[1, 2].set_title('Sleep: Daily Total Naps (7:00-19:00)',
                          fontsize=TITLE_FONT_SIZE)
    axarr[1, 2].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[1, 2].set_ylabel(
        'Total Naps', fontsize=AXIS_FONT_SIZE)
    axarr[1, 2].yaxis.set_ticks(np.arange(0, 16, 2))
    format_plot(daily_sleep_data['date'], axarr[1, 2])

    # Chart 7 - Sleep: Daily Longest Duration of Uninterrupted Sleep (Hours)
    axarr[2, 0].plot(daily_sleep_data['date'],
                     daily_sleep_data['longest_session'])
    axarr[2, 0].set_title('Sleep: Daily Longest Sleep Duration (Hr)',
                          fontsize=TITLE_FONT_SIZE)
    axarr[2, 0].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[2, 0].set_ylabel(
        'Longest Sleep Duration (Hr)', fontsize=AXIS_FONT_SIZE)
    axarr[2, 0].yaxis.set_ticks(np.arange(0, 13, 2))
    format_plot(daily_sleep_data['date'], axarr[2, 0])

    # Chart 8 - Sleep: Daily Total Sleep (Hours)
    axarr[2, 1].plot(daily_sleep_data['date'],
                     daily_sleep_data['total_sleep_duration'])
    axarr[2, 1].set_title('Sleep: Daily Total Sleep (Hr)',
                          fontsize=TITLE_FONT_SIZE)
    axarr[2, 1].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[2, 1].set_ylabel(
        'Total Sleep (Hr)', fontsize=AXIS_FONT_SIZE)
    axarr[2, 1].yaxis.set_ticks(np.arange(11, 21, 2))
    format_plot(daily_sleep_data['date'], axarr[2, 1])

    # Chart 9 - Daily Maximum Awake Duration (Hr)
    axarr[2, 2].plot(daily_sleep_data['date'],
                     daily_sleep_data['max_awake_duration'])
    axarr[2, 2].set_title('Daily Maximum Awake Duration (Hr)',
                          fontsize=TITLE_FONT_SIZE)
    axarr[2, 2].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[2, 2].set_ylabel(
        'Maximum Awake Duration (Hr)', fontsize=AXIS_FONT_SIZE)
    format_plot(daily_sleep_data['date'], axarr[2, 2])

    # Chart 10 - Diaper: Total Diapers (Cumulative)
    axarr[3, 0].plot(daily_diaper_data['date'],
                     daily_diaper_data['total_diaper_count'])
    axarr[3, 0].set_title('Diaper: Total Diapers (Cumulative)',
                          fontsize=TITLE_FONT_SIZE)
    axarr[3, 0].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[3, 0].set_ylabel(
        'Total Diapers', fontsize=AXIS_FONT_SIZE)
    format_plot(daily_diaper_data['date'], axarr[3, 0])

    # Chart 11 - Diaper: Daily Total Pees
    axarr[3, 1].plot(daily_diaper_data['date'],
                     daily_diaper_data['pee_count'])
    axarr[3, 1].set_title('Diaper: Daily Total Pees',
                          fontsize=TITLE_FONT_SIZE)
    axarr[3, 1].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[3, 1].set_ylabel(
        'Total Pees', fontsize=AXIS_FONT_SIZE)
    axarr[3, 1].yaxis.set_ticks(np.arange(2, 20, 2))
    format_plot(daily_diaper_data['date'], axarr[3, 1])

    # Chart 12 - Diaper: Daily Total Poops
    axarr[3, 2].plot(daily_diaper_data['date'],
                     daily_diaper_data['poop_count'])
    axarr[3, 2].set_title('Diaper: Daily Total Poops',
                          fontsize=TITLE_FONT_SIZE)
    axarr[3, 2].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[3, 2].set_ylabel(
        'Total Poops', fontsize=AXIS_FONT_SIZE)
    axarr[3, 2].yaxis.set_ticks(np.arange(0, 11, 2))
    format_plot(daily_diaper_data['date'], axarr[3, 2])

    # Export

    f.subplots_adjust(wspace=0.2, hspace=0.5)
    # if (DEBUG):
    #     f.set_size_inches(11, 8.5)  # US Letter
    # else:
    f.set_size_inches(config['output_dim_x'], config['output_dim_y'])
    f.savefig(config['output_daily_charts'], bbox_inches='tight')
    f.clf()
