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
from pandas.plotting import register_matplotlib_converters
from matplotlib.dates import MonthLocator, DateFormatter
from .parse_config import parse_json_config

# Settings
TITLE_FONT_SIZE = 10
AXIS_FONT_SIZE = 8
ALPHA_VALUE = 0.3

config = []


def format_plot(plot_object):
    plot_object.tick_params(labelsize=AXIS_FONT_SIZE)
    plot_object.set_xticks(plot_object.get_xticks()[::1])
    plot_object.xaxis.set_major_locator(
        MonthLocator(range(1, 13), bymonthday=1, interval=1))
    plot_object.xaxis.set_major_formatter(DateFormatter("%b"))


def plot_days_between_vomit(plot_object):
    # Import file
    data = pd.read_csv(config['data_misc'], parse_dates=['Date'])

    # Find first and last entry in column
    start_date = data['Date'].iloc[0].date()
    end_date = data['Date'].iloc[-1].date()

    # Look up vomit days and compute gaps
    vomit_days = data.loc[data['Vomit'] == 1]
    days_since_last_vomit = vomit_days['Date'].diff() / np.timedelta64(1, 'D')

    # Plots
    plot_object.plot(vomit_days['Date'], days_since_last_vomit)
    plot_object.set_title('Days Since Last Vomit',
                          fontsize=TITLE_FONT_SIZE)
    plot_object.set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    plot_object.set_ylabel(
        'Days Since Last Vomit', fontsize=AXIS_FONT_SIZE)
    plot_object.set_xlim(start_date, end_date)
    format_plot(plot_object)


def plot_monthly_vomit(plot_object):
    # Import file
    data = pd.read_csv(config['data_misc'], parse_dates=['Date'])

    # Fill empty cells with 0s
    data.fillna(0, inplace=True)

    # Group and compute sum by month. BMS gives 1st of month
    data = data.set_index(data['Date'])
    vomit_monthly = data['Vomit'].resample('BMS').sum()

    # Bug here - if I don't subtract by one month, label is wrong
    plot_object.plot(vomit_monthly.index, vomit_monthly)
    plot_object.set_title('Total Number of Vomits by Months',
                          fontsize=TITLE_FONT_SIZE)
    plot_object.set_xlabel('Date', fontsize=AXIS_FONT_SIZE)
    plot_object.set_ylabel(
        'Total Number of Vomits', fontsize=AXIS_FONT_SIZE)
    plot_object.set_xlim(vomit_monthly.index[0],
                         vomit_monthly.index[-1])
    format_plot(plot_object)


def plot_medical_charts(config_file):
    register_matplotlib_converters()

    # Style
    sns.set(style="darkgrid")
    f, axarr = plt.subplots(2, 3)

    # Import data
    global config
    config = parse_json_config(config_file)

    # Chart 1 - Total Vomit Per Month
    plot_monthly_vomit(axarr[0, 0])

    # Chart 2 - Days Between Vomit
    plot_days_between_vomit(axarr[0, 1])

    # Export
    f.subplots_adjust(wspace=0.2, hspace=0.5)
    f.set_size_inches(config['output_dim_x'], config['output_dim_y'])
    f.savefig(config['output_medical_charts'], bbox_inches='tight')
    f.clf()
