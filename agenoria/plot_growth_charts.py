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
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from matplotlib.ticker import MaxNLocator
from pandas.plotting import register_matplotlib_converters
import matplotlib.ticker as ticker


CDC_SEX = 1    # 1 for Boy, 2 for Girl
BIRTHDAY = dt.datetime(2018, 11, 21, 0, 0, 0)
TITLE_FONT_SIZE = 14
AXIS_FONT_SIZE = 10
LINE_ALPHA = 0.4


def parse_glow_data(glow_file):
    # Import file
    data = pd.read_csv(glow_file)

    # Convert to datetime
    data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m/%d')

    # Compute age
    data['Age'] = (data['Date'] - BIRTHDAY) / np.timedelta64(1, 'M')

    # Get date and height columns
    data_height = data[data['Height(cm)'].notnull()][[
        'Date', 'Age', 'Height(cm)']]
    data_head = data[data['Head Circ.(cm)'].notnull()][[
        'Date', 'Age', 'Head Circ.(cm)']]

    return data_height, data_head


def parse_hatch_data(hatch_file):
    # Import file
    data = pd.read_csv(hatch_file)

    # Keep date only, remove time
    hatch_dates = data['Start Time'].astype(str).str[0: 10]
    # Convert to datetime
    data['Start Time'] = pd.to_datetime(hatch_dates, format='%m/%d/%Y')

    # Sort and remove duplicates
    data = data.sort_values(by=['Start Time'], ascending=True)
    data = data.drop_duplicates(subset=['Start Time'], keep=False)

    # Reindex and add missing days
    idx = pd.date_range(
        start=data['Start Time'].min(), end=data['Start Time'].max())
    data = data.set_index('Start Time').reindex(
        idx).rename_axis('Start Time').reset_index()

    # Compute Age
    data['Age'] = (data['Start Time'] - BIRTHDAY) / \
        np.timedelta64(1, 'M')

    # Compute diff
    data['ROC'] = data['Amount'].diff()
    # Fill empty rows with 0
    data['ROC'] = data['ROC'].fillna(0)

    # Compute average on a rolling window
    ROC_WINDOW = 14
    data['Weight Average RoC'] = data['ROC'].rolling(window=ROC_WINDOW).mean()

    # Convert to oz
    data['Weight Average RoC'] = data['Weight Average RoC'] * 35.274

    # data.to_csv('test.csv')

    return data


def plot_weight_roc(file_hatch, plot_object):
    hatch_data = parse_hatch_data(file_hatch)

    plot_object.plot(hatch_data['Age'],
                     hatch_data['Weight Average RoC'], color='red', linewidth=2)

    # Labels
    plot_object.set_title('Average Daily Weight Gain vs. Age',
                          fontsize=TITLE_FONT_SIZE)
    plot_object.set_xlabel('Age (months)', fontsize=AXIS_FONT_SIZE)
    plot_object.set_ylabel('Average Daily Weight Gain (oz)',
                           fontsize=AXIS_FONT_SIZE)

    plot_object.set_xlim(0, 12)
    plot_object.set_ylim(-0.5, 1)
    plot_object.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plot_object.yaxis.set_major_locator(ticker.MultipleLocator(0.2))


def plot_weight_age(file_hatch, file_wtageinf, plot_object):
    # Import data
    data = pd.read_csv(file_wtageinf)
    hatch_data = parse_hatch_data(file_hatch)

    # Extract by sex
    data = data.loc[data['Sex'] == CDC_SEX]

    # Plot percentile lines
    plot_object.plot(data['Agemos'], data['P3'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P5'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P10'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P25'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P50'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P75'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P90'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P95'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P97'], alpha=LINE_ALPHA)
    plot_object.plot(hatch_data['Age'],
                     hatch_data['Amount'], color='red', linewidth=2)

    # Labels
    plot_object.set_title('Weight vs. Age',
                          fontsize=TITLE_FONT_SIZE)
    plot_object.set_xlabel('Age (months)', fontsize=AXIS_FONT_SIZE)
    plot_object.set_ylabel('Weight (kg)', fontsize=AXIS_FONT_SIZE)

    plot_object.set_xlim(0, 12)
    plot_object.set_ylim(3, 10)
    plot_object.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plot_object.yaxis.set_major_locator(ticker.MultipleLocator(1))


def plot_weight_percentile(file_hatch, plot_object):
    hatch_data = parse_hatch_data(file_hatch)

    plot_object.plot(hatch_data['Age'],
                     hatch_data['Percentile'] * 100, color='red')
    plot_object.set_title('Weight Percentile vs. Age',
                          fontsize=TITLE_FONT_SIZE)
    plot_object.set_ylabel(
        'Weight Percentile (%)', fontsize=AXIS_FONT_SIZE)
    plot_object.set_xlabel('Age (months)', fontsize=AXIS_FONT_SIZE)

    plot_object.set_xlim(0, 12)
    plot_object.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plot_object.set_ylim(25, 80)


def plot_length_age(file_glow, file_lenageinf, plot_object):
    # Import data
    data = pd.read_csv(file_lenageinf)
    data_height, data_head = parse_glow_data(file_glow)

    # Extract by sex
    data = data.loc[data['Sex'] == CDC_SEX]

    # Plot percentile lines
    plot_object.plot(data['Agemos'], data['P3'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P5'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P10'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P25'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P50'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P75'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P90'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P95'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P97'], alpha=LINE_ALPHA)
    plot_object.plot(data_height['Age'],
                     data_height['Height(cm)'], color='red', linewidth=2)

    # Labels
    plot_object.set_title('Length vs. Age',
                          fontsize=TITLE_FONT_SIZE)
    plot_object.set_xlabel('Age (months)', fontsize=AXIS_FONT_SIZE)
    plot_object.set_ylabel('Length (cm)', fontsize=AXIS_FONT_SIZE)

    plot_object.set_xlim(0, 12)
    plot_object.set_ylim(53, 80)
    plot_object.xaxis.set_major_locator(ticker.MultipleLocator(1))


def plot_head_circumference_age(file_glow, file_hcageinf, plot_object):
    # Import data
    data = pd.read_csv(file_hcageinf)
    data_height, data_head = parse_glow_data(file_glow)

    # Extract by sex
    data = data.loc[data['Sex'] == CDC_SEX]

    # Plot percentile lines
    plot_object.plot(data['Agemos'], data['P3'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P5'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P10'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P25'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P50'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P75'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P90'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P95'], alpha=LINE_ALPHA)
    plot_object.plot(data['Agemos'], data['P97'], alpha=LINE_ALPHA)
    plot_object.plot(data_head['Age'],
                     data_head['Head Circ.(cm)'], color='red', linewidth=2)

    # Labels
    plot_object.set_title(
        'Head Circumference vs. Age', fontsize=TITLE_FONT_SIZE)
    plot_object.set_xlabel('Age (months)', fontsize=AXIS_FONT_SIZE)
    plot_object.set_ylabel('Head Circumference (cm)', fontsize=AXIS_FONT_SIZE)

    plot_object.set_xlim(0, 12)
    plot_object.set_ylim(35, 48)
    plot_object.xaxis.set_major_locator(ticker.MultipleLocator(1))


def plot_weight_length(file_hatch, file_glow, file_wtleninf, plot_object):
    # Import data
    data = pd.read_csv(file_wtleninf)
    data_height, data_head = parse_glow_data(file_glow)
    hatch_data = parse_hatch_data(file_hatch)

    weight_length = []

    # Search for weight on given date
    for index, row in data_height.iterrows():
        date = row['Date']
        match = hatch_data.loc[hatch_data['Start Time'] == date]
        weight = float(match['Amount'].values)
        if (not np.isnan(weight)):
            weight_length.append([row['Date'],
                                  row['Age'], row['Height(cm)'], weight])

    data_weight_length = pd.DataFrame(
        weight_length, columns=['Date', 'Age', 'Height(cm)', 'Weight'])

    # Extract by sex
    data = data.loc[data['Sex'] == CDC_SEX]

    # Plot percentile lines
    plot_object.plot(data['Length'], data['P3'], alpha=LINE_ALPHA)
    plot_object.plot(data['Length'], data['P5'], alpha=LINE_ALPHA)
    plot_object.plot(data['Length'], data['P10'], alpha=LINE_ALPHA)
    plot_object.plot(data['Length'], data['P25'], alpha=LINE_ALPHA)
    plot_object.plot(data['Length'], data['P50'], alpha=LINE_ALPHA)
    plot_object.plot(data['Length'], data['P75'], alpha=LINE_ALPHA)
    plot_object.plot(data['Length'], data['P90'], alpha=LINE_ALPHA)
    plot_object.plot(data['Length'], data['P95'], alpha=LINE_ALPHA)
    plot_object.plot(data['Length'], data['P97'], alpha=LINE_ALPHA)
    plot_object.plot(data_weight_length['Height(cm)'],
                     data_weight_length['Weight'], color='red', linewidth=2)
    # Labels
    plot_object.set_title('Weight vs. Length',
                          fontsize=TITLE_FONT_SIZE)
    plot_object.set_xlabel('Length (cm)', fontsize=AXIS_FONT_SIZE)
    plot_object.set_ylabel('Weight (kg)', fontsize=AXIS_FONT_SIZE)

    plot_object.set_xlim(53, 80)
    plot_object.set_ylim(3.5, 10)
    plot_object.xaxis.set_major_locator(ticker.MultipleLocator(5))


def plot_growth_charts(file_hatch, file_glow, file_output, file_wtageinf,
                       file_lenageinf, file_hcageinf, file_wtleninf):

    register_matplotlib_converters()

    # Settings

    title_font_size = 10
    axis_font_size = 8
    alpha_value = 0.3

    sns.set(style="darkgrid")
    f, axarr = plt.subplots(2, 3)

    # Chart 1 - Weight / Age
    plot_weight_age(file_hatch, file_wtageinf, axarr[0, 0])

    # Chart 2 - Weight Percentile / Age
    plot_weight_percentile(file_hatch, axarr[0, 1])

    # Chart 2 - Weight Rate of Change / Age
    plot_weight_roc(file_hatch, axarr[0, 2])

    # Chart 4 - Length / Age
    plot_length_age(file_glow, file_lenageinf, axarr[1, 0])

    # Chart 5 - Head Circumference / Age
    plot_head_circumference_age(file_glow, file_hcageinf, axarr[1, 1])

    # Chart 6 - Weight / Length
    plot_weight_length(file_hatch, file_glow, file_wtleninf, axarr[1, 2])

    # Export
    f.subplots_adjust(wspace=0.25, hspace=0.35)
    f.set_size_inches(17, 11)  # Tabloid size
    f.savefig(file_output, bbox_inches='tight')
    f.clf()
