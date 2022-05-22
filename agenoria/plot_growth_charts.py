#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.ticker as ticker
from .parse_config import parse_json_config
from .plot_settings import format_growth_chart_plot, export_figure

# Parameters from JSON
config = []

LINE_ALPHA = 0.4


def compute_age(date, birthday):
    age = (date - birthday) / np.timedelta64(1, 'M')
    return age


def parse_glow_data(glow_file, birthday):
    # Import file
    data = pd.read_csv(glow_file, parse_dates=['Date'])

    # Compute age
    data['Age'] = compute_age(data['Date'], config['birthday'])

    # Get date and height columns
    data_height = data[data['Height(cm)'].notnull()][[
        'Date', 'Age', 'Height(cm)']]
    data_head = data[data['Head Circ.(cm)'].notnull()][[
        'Date', 'Age', 'Head Circ.(cm)']]

    return data_height, data_head


def parse_hatch_data(hatch_file, birthday):
    # Import file
    data = pd.read_csv(hatch_file)

    # Keep date only, remove time. Hatch invalid format: redundant AM/PM
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
    data['Age'] = compute_age(data['Start Time'], config['birthday'])

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


def plot_growth_curves(curve_file, index, plot_object):
    # Import growth curves data file
    data_raw = pd.read_csv(curve_file)

    # Extract by sex
    sex = 1 if (config['gender'] == "boy") else 2
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


def plot_weight_length(plot_object, data_height, data_head, hatch_data):
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
    plot_object.plot(
        data_weight_length['Height(cm)'], data_weight_length['Weight'])
    # Labels
    plot_object.set_title('Weight vs. Length')
    plot_object.set_xlabel('Length (cm)')
    plot_object.set_ylabel('Weight (kg)')
    plot_object.set_xlim(53, 90)
    plot_object.set_ylim(3.5, 12)
    plot_object.xaxis.set_major_locator(ticker.MultipleLocator(5))
    format_growth_chart_plot(plot_object)


def plot_growth_charts(config_data):
    # Import data
    global config
    config = config_data

    # Settings
    sns.set(style="darkgrid")
    plt.rcParams["lines.linewidth"] = 2
    f, axarr = plt.subplots(2, 3)

    # Import data
    data_height, data_head = parse_glow_data(
        config['data_growth'], config['birthday'])
    hatch_data = parse_hatch_data(config['data_weight'], config['birthday'])

    # Start & end date - one year or full
    start_date = 0
    if (config["output_year_one_only"]):
        end_date = 12
    else:
        end_date = hatch_data['Age'].iloc[-1]

    # Chart 1 - Weight / Age
    plot_growth_curves(config['growth_curve_weight'], 'Agemos', axarr[0, 0])
    axarr[0, 0].plot(hatch_data['Age'], hatch_data['Amount'])
    axarr[0, 0].set_title('Weight vs. Age')
    axarr[0, 0].set_xlabel('Age (months)')
    axarr[0, 0].set_ylabel('Weight (kg)')
    axarr[0, 0].set_xlim(start_date, end_date)
    axarr[0, 0].set_ylim(3, 12)
    axarr[0, 0].xaxis.set_major_locator(ticker.MultipleLocator(1))
    axarr[0, 0].yaxis.set_major_locator(ticker.MultipleLocator(1))
    format_growth_chart_plot(axarr[0, 0])

    # Chart 2 - Weight Percentile / Age
    axarr[0, 1].plot(hatch_data['Age'], hatch_data['Percentile'] * 100)
    axarr[0, 1].set_title('Weight Percentile vs. Age')
    axarr[0, 1].set_ylabel('Weight Percentile (%)')
    axarr[0, 1].set_xlabel('Age (months)')

    axarr[0, 1].set_xlim(start_date, end_date)
    axarr[0, 1].xaxis.set_major_locator(ticker.MultipleLocator(1))
    axarr[0, 1].set_ylim(20, 80)
    format_growth_chart_plot(axarr[0, 1])

    # Chart 2 - Weight Rate of Change / Age
    axarr[0, 2].plot(hatch_data['Age'], hatch_data['Weight Average RoC'])
    axarr[0, 2].set_title('Average Daily Weight Gain vs. Age')
    axarr[0, 2].set_xlabel('Age (months)')
    axarr[0, 2].set_ylabel('Average Daily Weight Gain (oz)')
    axarr[0, 2].set_xlim(start_date, end_date)
    axarr[0, 2].set_ylim(-0.5, 1.3)
    axarr[0, 2].xaxis.set_major_locator(ticker.MultipleLocator(1))
    axarr[0, 2].yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    format_growth_chart_plot(axarr[0, 2])

    # Chart 4 - Length / Age
    plot_growth_curves(config['growth_curve_length'], 'Agemos', axarr[1, 0])
    axarr[1, 0].plot(data_height['Age'], data_height['Height(cm)'])
    axarr[1, 0].set_title('Length vs. Age')
    axarr[1, 0].set_xlabel('Age (months)')
    axarr[1, 0].set_ylabel('Length (cm)')
    axarr[1, 0].set_xlim(start_date, end_date)
    axarr[1, 0].set_ylim(53, 80)
    axarr[1, 0].xaxis.set_major_locator(ticker.MultipleLocator(1))
    format_growth_chart_plot(axarr[1, 0])

    # Chart 5 - Head Circumference / Age
    plot_growth_curves(config['growth_curve_head'], 'Agemos', axarr[1, 1])
    axarr[1, 1].plot(data_head['Age'], data_head['Head Circ.(cm)'])
    axarr[1, 1].set_title('Head Circumference vs. Age')
    axarr[1, 1].set_xlabel('Age (months)')
    axarr[1, 1].set_ylabel('Head Circumference (cm)')
    axarr[1, 1].set_xlim(start_date, end_date)
    axarr[1, 1].set_ylim(35, 48)
    axarr[1, 1].xaxis.set_major_locator(ticker.MultipleLocator(1))
    format_growth_chart_plot(axarr[1, 1])

    # Chart 6 - Weight / Length
    plot_growth_curves(
        config['growth_curve_weight_length'], 'Length', axarr[1, 2])
    plot_weight_length(axarr[1, 2], data_height, data_head, hatch_data)

    # Export
    f.subplots_adjust(wspace=0.25, hspace=0.35)
    export_figure(f, config['output_dim_x'], config['output_dim_y'],
                  config['output_growth'])
