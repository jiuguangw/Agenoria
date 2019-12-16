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

# Debug option
DEBUG = False
DEBUG_START_DATE = dt.datetime(2019, 8, 17, 0, 0, 0)
DEBUG_END_DATE = dt.datetime(2019, 9, 27, 0, 0, 0)

# Settings
TITLE_FONT_SIZE = 10
AXIS_FONT_SIZE = 8
ALPHA_VALUE = 0.3

config = []


def format_plot(date_data, plot_object):
    plot_object.set_xlim(date_data.iloc[0],
                         date_data.iloc[-1])

    if(DEBUG):
        plot_object.tick_params(labelsize=AXIS_FONT_SIZE)
        plot_object.set_xticks(plot_object.get_xticks()[::1])
        plot_object.xaxis.set_major_formatter(DateFormatter("%m/%d"))
    else:
        plot_object.tick_params(labelsize=AXIS_FONT_SIZE)
        plot_object.set_xticks(plot_object.get_xticks()[::1])
        plot_object.xaxis.set_major_locator(
            MonthLocator(range(1, 13), bymonthday=1, interval=1))
        plot_object.xaxis.set_major_formatter(DateFormatter("%b"))


def parse_glow_diaper_data(file_name):
    # Import file
    data_diaper = pd.read_csv(file_name, parse_dates=['Diaper time'])

    # Sort by date and time
    data_diaper = data_diaper.sort_values(by=['Diaper time'], ascending=False)

    # Make a new column with date component only
    data_diaper['Date'] = data_diaper['Diaper time'].dt.normalize()

    # Find first and last entry in column
    start_date = data_diaper['Date'].iloc[-1]
    end_date = data_diaper['Date'].iloc[0]

    if (DEBUG):
        start_date = DEBUG_START_DATE
        end_date = DEBUG_END_DATE

    # Final data
    diaper_data_list = []
    cumulative_diaper_count = 0

    # Diaper
    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        rows_on_date = data_diaper[data_diaper['Date'].isin([current_date])]

        # Compute total diaper count
        daily_total_diaper_count = rows_on_date['In the diaper'].count()
        cumulative_diaper_count += rows_on_date['In the diaper'].count()

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

        # Compute poop to total diaper change ratio
        poop_ratio = (total_poop_count / daily_total_diaper_count) * 100

        # Compute diaper day duration
        diaper_final = rows_on_date['Diaper time'].iloc[0]
        diaper_first = rows_on_date['Diaper time'].iloc[-1]
        diaper_day_duration = (
            diaper_final - diaper_first).total_seconds() / 3600

        # Compute average time between diaper changes
        diaper_change_time_avg = diaper_day_duration / daily_total_diaper_count

        # Put stats in a list
        diaper_data_list.append(
            [current_date, daily_total_diaper_count, cumulative_diaper_count,
             total_pee_count, total_poop_count, poop_ratio,
             diaper_change_time_avg])

    # Convert list to dataframe
    daily_diaper_data = pd.DataFrame(
        diaper_data_list, columns=['date', 'daily_total_diaper_count',
                                   'cumulative_diaper_count', 'pee_count',
                                   'poop_count', 'poop_ratio',
                                   'diaper_change_time_avg'])

    return daily_diaper_data


def get_abnormal_days(diaper_data):
    # Constipation monthly - days with zero poop
    constipation_days = diaper_data.loc[diaper_data['poop_count'] == 0]
    constipation_days = constipation_days.set_index(constipation_days['date'])
    constipation_monthly = constipation_days['daily_total_diaper_count'].resample(
        'BMS').count()

    # Diarrhea monthly - days with high percentage of poops
    CUTOFF = 65
    diarrhea_days = diaper_data.loc[diaper_data['poop_ratio'] >= CUTOFF]
    diarrhea_days = diarrhea_days.set_index(diarrhea_days['date'])
    diarrhea_monthly = diarrhea_days['daily_total_diaper_count'].resample(
        'BMS').count()

    return constipation_monthly, diarrhea_monthly


def get_diaper_monthly_data(diaper_data):
    # Reindex
    monthly_data = diaper_data.set_index(diaper_data['date'])

    # Compute monthly total
    diaper_monthly_data = monthly_data['daily_total_diaper_count'].resample(
        'BMS').sum()

    return diaper_monthly_data


def plot_diaper_charts(config_file):
    # Matplotlib converters
    register_matplotlib_converters()

    # Style
    sns.set(style="darkgrid")
    f, axarr = plt.subplots(3, 3)

    # Import data
    global config
    config = parse_json_config(config_file)

    # Parse data
    daily_diaper_data = parse_glow_diaper_data(config['data_diaper'])
    diaper_monthly_data = get_diaper_monthly_data(daily_diaper_data)
    constipation_monthly_data, diarrhea_monthly_data = get_abnormal_days(
        daily_diaper_data)

    # Chart 1 - Diaper: Total Diapers (Cumulative)
    axarr[0, 0].plot(daily_diaper_data['date'],
                     daily_diaper_data['cumulative_diaper_count'])
    axarr[0, 0].set_title('Diaper: Total Diapers (Cumulative)',
                          fontsize=TITLE_FONT_SIZE)
    axarr[0, 0].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[0, 0].set_ylabel(
        'Total Diapers', fontsize=AXIS_FONT_SIZE)
    format_plot(daily_diaper_data['date'], axarr[0, 0])

    # Chart 2 - Diaper: Number of Diapers by Month
    axarr[0, 1].plot(diaper_monthly_data.index,
                     diaper_monthly_data)
    axarr[0, 1].set_title('Diaper: Number of Diapers by Month',
                          fontsize=TITLE_FONT_SIZE)
    axarr[0, 1].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[0, 1].set_ylabel(
        'Number of Diapers by Month', fontsize=AXIS_FONT_SIZE)
    axarr[0, 1].yaxis.set_ticks(np.arange(0, 400, 50))
    format_plot(daily_diaper_data['date'], axarr[0, 1])

    # Chart 3 - Diaper: Daily Total Diaper Count
    axarr[0, 2].plot(daily_diaper_data['date'],
                     daily_diaper_data['daily_total_diaper_count'])
    axarr[0, 2].set_title('Diaper: Number of Diapers by Day',
                          fontsize=TITLE_FONT_SIZE)
    axarr[0, 2].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[0, 2].set_ylabel(
        'Number of Diapers by Day', fontsize=AXIS_FONT_SIZE)
    axarr[0, 2].yaxis.set_ticks(np.arange(0, 20, 2))
    format_plot(daily_diaper_data['date'], axarr[0, 2])

    # Chart 4 - Diaper: Daily Total Pees
    axarr[1, 0].plot(daily_diaper_data['date'],
                     daily_diaper_data['pee_count'])
    axarr[1, 0].set_title('Diaper: Daily Total Pees',
                          fontsize=TITLE_FONT_SIZE)
    axarr[1, 0].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[1, 0].set_ylabel(
        'Total Pees', fontsize=AXIS_FONT_SIZE)
    axarr[1, 0].yaxis.set_ticks(np.arange(2, 20, 2))
    format_plot(daily_diaper_data['date'], axarr[1, 0])

    # Chart 5 - Diaper: Daily Total Poops
    axarr[1, 1].plot(daily_diaper_data['date'],
                     daily_diaper_data['poop_count'])
    axarr[1, 1].set_title('Diaper: Daily Total Poops',
                          fontsize=TITLE_FONT_SIZE)
    axarr[1, 1].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[1, 1].set_ylabel(
        'Total Poops', fontsize=AXIS_FONT_SIZE)
    axarr[1, 1].yaxis.set_ticks(np.arange(0, 11, 2))
    format_plot(daily_diaper_data['date'], axarr[1, 1])

    # Chart 6 - Diaper: Average Time Between Diaper Changes
    axarr[1, 2].plot(daily_diaper_data['date'],
                     daily_diaper_data['diaper_change_time_avg'])
    axarr[1, 2].set_title('Diaper: Average Time Between Diaper Changes (Hours)',
                          fontsize=TITLE_FONT_SIZE)
    axarr[1, 2].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[1, 2].set_ylabel(
        'Average Time Between Diaper Changes (Hours)', fontsize=AXIS_FONT_SIZE)
    axarr[1, 2].yaxis.set_ticks(np.arange(1, 5, 0.5))
    format_plot(daily_diaper_data['date'], axarr[1, 2])

    # Chart 7 - Diaper: Poop Ratio
    axarr[2, 0].plot(daily_diaper_data['date'],
                     daily_diaper_data['poop_ratio'])
    axarr[2, 0].set_title('Diaper: Poop as Percentage of Diaper Changes',
                          fontsize=TITLE_FONT_SIZE)
    axarr[2, 0].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[2, 0].set_ylabel(
        'Poop as Percentage of Diaper Changes', fontsize=AXIS_FONT_SIZE)
    axarr[2, 0].yaxis.set_ticks(np.arange(0, 110, 10))
    format_plot(daily_diaper_data['date'], axarr[2, 0])

    # Chart 8 - Diaper: Constipation
    axarr[2, 1].plot(constipation_monthly_data.index,
                     constipation_monthly_data)
    axarr[2, 1].set_title('Diaper: Number of Constipated Days by Month',
                          fontsize=TITLE_FONT_SIZE)
    axarr[2, 1].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[2, 1].set_ylabel(
        'Number of Constipated Days', fontsize=AXIS_FONT_SIZE)
    format_plot(daily_diaper_data['date'], axarr[2, 1])

    # Chart 9 - Diaper: Diarrhea
    axarr[2, 2].plot(diarrhea_monthly_data.index,
                     diarrhea_monthly_data)
    axarr[2, 2].set_title('Diaper: Number of Diarrhea Days by Month',
                          fontsize=TITLE_FONT_SIZE)
    axarr[2, 2].set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    axarr[2, 2].set_ylabel(
        'Number of Diarrhea Days', fontsize=AXIS_FONT_SIZE)
    axarr[2, 2].yaxis.set_ticks(np.arange(0, 3, 1))
    format_plot(daily_diaper_data['date'], axarr[2, 2])

    # Export
    f.subplots_adjust(wspace=0.2, hspace=0.5)
    if (DEBUG):
        f.set_size_inches(11, 8.5)  # US Letter
    else:
        f.set_size_inches(config['output_dim_x'], config['output_dim_y'])
        f.savefig(config['output_daily_diaper_charts'], bbox_inches='tight')
        f.clf()
