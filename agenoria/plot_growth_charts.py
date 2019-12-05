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
from pandas.plotting import register_matplotlib_converters
import matplotlib.ticker as ticker


TITLE_FONT_SIZE = 14
AXIS_FONT_SIZE = 10
LINE_ALPHA = 0.4


def compute_age(date, birthday):
    age = (date - birthday) / np.timedelta64(1, 'M')
    return age


def parse_glow_data(glow_file, birthday):
    # Import file
    data = pd.read_csv(glow_file)

    # Convert to datetime
    data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m/%d')

    # Compute age
    data['Age'] = compute_age(data['Date'], birthday)

    # Get date and height columns
    data_height = data[data['Height(cm)'].notnull()][[
        'Date', 'Age', 'Height(cm)']]
    data_head = data[data['Head Circ.(cm)'].notnull()][[
        'Date', 'Age', 'Head Circ.(cm)']]

    return data_height, data_head


def parse_hatch_data(hatch_file, birthday):
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
    data['Age'] = compute_age(data['Start Time'], birthday)

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


def plot_growth_curves(curve_file, sex, index, plot_object):
    # Import growth curves data file
    data_raw = pd.read_csv(curve_file)

    # Extract by sex
    data = data_raw.loc[data_raw['Sex'] == sex]

    # Plot percentile lines
    plot_object.plot(data[index], data['P3'], alpha=LINE_ALPHA)
    plot_object.plot(data[index], data['P5'], alpha=LINE_ALPHA)
    plot_object.plot(data[index], data['P10'], alpha=LINE_ALPHA)
    plot_object.plot(data[index], data['P25'], alpha=LINE_ALPHA)
    plot_object.plot(data[index], data['P50'], alpha=LINE_ALPHA)
    plot_object.plot(data[index], data['P75'], alpha=LINE_ALPHA)
    plot_object.plot(data[index], data['P90'], alpha=LINE_ALPHA)
    plot_object.plot(data[index], data['P95'], alpha=LINE_ALPHA)
    plot_object.plot(data[index], data['P97'], alpha=LINE_ALPHA)


def plot_weight_roc(file_hatch, birthday, plot_object):
    hatch_data = parse_hatch_data(file_hatch, birthday)

    plot_object.plot(hatch_data['Age'],
                     hatch_data['Weight Average RoC'], color='red', linewidth=2)

    # Labels
    plot_object.set_title('Average Daily Weight Gain vs. Age',
                          fontsize=TITLE_FONT_SIZE)
    plot_object.set_xlabel('Age (months)', fontsize=AXIS_FONT_SIZE)
    plot_object.set_ylabel('Average Daily Weight Gain (oz)',
                           fontsize=AXIS_FONT_SIZE)
    plot_object.set_xlim(hatch_data['Age'].iloc[0], hatch_data['Age'].iloc[-1])
    plot_object.set_ylim(-0.5, 1)
    plot_object.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plot_object.yaxis.set_major_locator(ticker.MultipleLocator(0.2))


def plot_weight_age(file_hatch, sex, birthday, file_wtageinf, plot_object):
    # Plot growth curves
    index = 'Agemos'
    plot_growth_curves(file_wtageinf, sex, index, plot_object)

    # Import data
    hatch_data = parse_hatch_data(file_hatch, birthday)

    # Plot data
    plot_object.plot(hatch_data['Age'],
                     hatch_data['Amount'], color='red', linewidth=2)

    # Labels
    plot_object.set_title('Weight vs. Age',
                          fontsize=TITLE_FONT_SIZE)
    plot_object.set_xlabel('Age (months)', fontsize=AXIS_FONT_SIZE)
    plot_object.set_ylabel('Weight (kg)', fontsize=AXIS_FONT_SIZE)
    plot_object.set_xlim(hatch_data['Age'].iloc[0], hatch_data['Age'].iloc[-1])
    plot_object.set_ylim(3, 10)
    plot_object.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plot_object.yaxis.set_major_locator(ticker.MultipleLocator(1))


def plot_weight_percentile(file_hatch, birthday, plot_object):
    hatch_data = parse_hatch_data(file_hatch, birthday)

    plot_object.plot(hatch_data['Age'],
                     hatch_data['Percentile'] * 100, color='red')
    plot_object.set_title('Weight Percentile vs. Age',
                          fontsize=TITLE_FONT_SIZE)
    plot_object.set_ylabel(
        'Weight Percentile (%)', fontsize=AXIS_FONT_SIZE)
    plot_object.set_xlabel('Age (months)', fontsize=AXIS_FONT_SIZE)

    plot_object.set_xlim(hatch_data['Age'].iloc[0], hatch_data['Age'].iloc[-1])
    plot_object.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plot_object.set_ylim(25, 80)


def plot_length_age(file_glow, sex, birthday, file_lenageinf, plot_object):
    # Plot growth curves
    index = 'Agemos'
    plot_growth_curves(file_lenageinf, sex, index, plot_object)

    # Import data
    data_height, data_head = parse_glow_data(file_glow, birthday)

    # Plot data
    plot_object.plot(data_height['Age'],
                     data_height['Height(cm)'], color='red', linewidth=2)

    # Labels
    plot_object.set_title('Length vs. Age',
                          fontsize=TITLE_FONT_SIZE)
    plot_object.set_xlabel('Age (months)', fontsize=AXIS_FONT_SIZE)
    plot_object.set_ylabel('Length (cm)', fontsize=AXIS_FONT_SIZE)
    plot_object.set_xlim(
        data_height['Age'].iloc[-1], data_height['Age'].iloc[0])
    plot_object.set_ylim(53, 80)
    plot_object.xaxis.set_major_locator(ticker.MultipleLocator(1))


def plot_head_circumference_age(file_glow, sex, birthday, file_hcageinf, plot_object):
    # Plot growth curves
    index = "Agemos"
    plot_growth_curves(file_hcageinf, sex, index, plot_object)

    # Import data
    data_height, data_head = parse_glow_data(file_glow, birthday)

    # Plot data
    plot_object.plot(data_head['Age'],
                     data_head['Head Circ.(cm)'], color='red', linewidth=2)

    # Labels
    plot_object.set_title(
        'Head Circumference vs. Age', fontsize=TITLE_FONT_SIZE)
    plot_object.set_xlabel('Age (months)', fontsize=AXIS_FONT_SIZE)
    plot_object.set_ylabel('Head Circumference (cm)', fontsize=AXIS_FONT_SIZE)

    plot_object.set_xlim(data_head['Age'].iloc[-1], data_head['Age'].iloc[0])
    plot_object.set_ylim(35, 48)
    plot_object.xaxis.set_major_locator(ticker.MultipleLocator(1))


def plot_weight_length(file_hatch, file_glow, sex, birthday, file_wtleninf, plot_object):
    # Plot growth curves
    index = 'Length'
    plot_growth_curves(file_wtleninf, sex, index, plot_object)

    # Import data
    data_height, data_head = parse_glow_data(file_glow, birthday)
    hatch_data = parse_hatch_data(file_hatch, birthday)

    weight_length = []

    # Search for weight on given date
    for index, row in data_height.iterrows():
        date = row['Date']
        match = hatch_data.loc[hatch_data['Start Time'] == date]
        weight = float(match['Amount'].values)
        if (not np.isnan(weight)):
            weight_length.append([row['Date'],
                                  row['Age'], row['Height(cm)'], weight])

    # Assemble into dataframe
    data_weight_length = pd.DataFrame(
        weight_length, columns=['Date', 'Age', 'Height(cm)', 'Weight'])

    # Plot data
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


def plot_growth_charts(file_hatch, file_glow, file_output, sex, birthday, file_wtageinf,
                       file_lenageinf, file_hcageinf, file_wtleninf):

    register_matplotlib_converters()

    # Settings
    sns.set(style="darkgrid")
    f, axarr = plt.subplots(2, 3)

    # Convert birthday tuple into datetime
    birthday_date = dt.datetime(birthday[0], birthday[1], birthday[2], 0, 0, 0)

    # Chart 1 - Weight / Age
    plot_weight_age(file_hatch, sex, birthday_date, file_wtageinf, axarr[0, 0])

    # Chart 2 - Weight Percentile / Age
    plot_weight_percentile(file_hatch, birthday_date, axarr[0, 1])

    # Chart 2 - Weight Rate of Change / Age
    plot_weight_roc(file_hatch, birthday_date, axarr[0, 2])

    # Chart 4 - Length / Age
    plot_length_age(file_glow, sex, birthday_date, file_lenageinf, axarr[1, 0])

    # Chart 5 - Head Circumference / Age
    plot_head_circumference_age(
        file_glow, sex, birthday_date, file_hcageinf, axarr[1, 1])

    # Chart 6 - Weight / Length
    plot_weight_length(file_hatch, file_glow, sex,
                       birthday_date, file_wtleninf, axarr[1, 2])

    # Export
    f.subplots_adjust(wspace=0.25, hspace=0.35)
    f.set_size_inches(17, 11)  # Tabloid size
    f.savefig(file_output, bbox_inches='tight')
    f.clf()
