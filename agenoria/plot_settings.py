# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import math
from pathlib import Path

import matplotlib as mpl
import numpy as np
import pandas as pd
from chart_studio import plotly
from matplotlib.dates import DateFormatter, MonthLocator

from config import param as config

# Figure settings
TITLE_HEIGHT_ADJUST = 1.02

TITLE_FONT_SIZE_LG = 25
AXIS_FONT_SIZE_LG = 15
TITLE_FONT_SIZE_MED = 14
AXIS_FONT_SIZE_MED = 10
TITLE_FONT_SIZE_SM = 10
AXIS_FONT_SIZE_SM = 8

ALPHA_VALUE = 0.3


def mmm_plot(
    plot_object: mpl.figure,
    data_date: pd.DataFrame,
    data_mean: pd.DataFrame,
    data_min: pd.DataFrame,
    data_max: pd.DataFrame,
) -> None:
    plot_object.plot(data_date, data_mean)
    plot_object.fill_between(data_date, data_max, data_mean, alpha=ALPHA_VALUE)
    plot_object.fill_between(data_date, data_min, data_mean, alpha=ALPHA_VALUE)


def enumerate_labels(date_num: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    hour_labels = [f"{num}:00" for num in range(24)]
    week_labels = [str(num) for num in range(0, math.ceil(date_num / 7), 2)]

    return hour_labels, week_labels


def format_24h_week_plot_horizontal(
    fig_axis: mpl.figure,
    date_num: int,
    title: str,
) -> None:
    # Create the tick labels
    hour_labels, week_labels = enumerate_labels(date_num)

    # Set title and axis labels
    if config["output_format"]["output_chart_labels_on"]:
        fig_axis.set_title(
            title,
            fontsize=TITLE_FONT_SIZE_LG,
            y=TITLE_HEIGHT_ADJUST,
        )
        fig_axis.set_xlabel("Age (weeks)", fontsize=AXIS_FONT_SIZE_LG)
        fig_axis.set_ylabel("Time of Day", fontsize=AXIS_FONT_SIZE_LG)

    # Format y axis - clock time
    fig_axis.set_ylim(0, 24)
    fig_axis.yaxis.set_ticks(np.arange(0, 24, 1))
    fig_axis.set_yticklabels(hour_labels)
    fig_axis.invert_yaxis()

    # Format x axis - bottom, week number
    fig_axis.set_xlim(1, date_num)
    fig_axis.xaxis.set_ticks(np.arange(1, date_num + 1, 14))
    fig_axis.set_xticklabels(week_labels)


def format_24h_week_plot_vertical(fig_axis: mpl.figure, date_num: int) -> None:
    # Create the tick labels
    hour_labels, week_labels = enumerate_labels(date_num)

    # Set title and axis labels
    fig_axis.set_xlabel(
        "Age (weeks)",
        fontsize=AXIS_FONT_SIZE_LG,
        rotation=180,
    )
    fig_axis.set_ylabel("Time of Day", fontsize=AXIS_FONT_SIZE_LG)

    # Format y axis - clock time
    fig_axis.set_ylim(24, 0)
    fig_axis.yaxis.set_ticks(np.arange(0, 24, 1))
    fig_axis.set_yticklabels(hour_labels, rotation=180)
    fig_axis.invert_yaxis()

    # Format x axis - bottom, week number
    fig_axis.set_xlim(1, date_num)
    fig_axis.xaxis.set_ticks(np.arange(1, date_num + 1, 14))
    fig_axis.set_xticklabels(week_labels, rotation=90)


def format_growth_chart_plot(plot_object: mpl.figure) -> None:
    # Change label sizes
    plot_object.title.set_size(TITLE_FONT_SIZE_MED)
    plot_object.xaxis.label.set_size(AXIS_FONT_SIZE_MED)
    plot_object.yaxis.label.set_size(AXIS_FONT_SIZE_MED)
    plot_object.tick_params(labelsize=AXIS_FONT_SIZE_MED)


def format_monthly_plot(
    plot_object: mpl.figure,
    xlim_left: int,
    xlim_right: int,
) -> None:
    # Axis label
    plot_object.set_xlabel("Date")

    # Change x-axis left and right limits
    plot_object.set_xlim(xlim_left, xlim_right)
    plot_object.autoscale(enable=True, axis="y", tight=True)

    # Change label sizes
    plot_object.title.set_size(TITLE_FONT_SIZE_SM)
    plot_object.xaxis.label.set_size(AXIS_FONT_SIZE_SM)
    plot_object.yaxis.label.set_size(AXIS_FONT_SIZE_SM)
    plot_object.tick_params(labelsize=AXIS_FONT_SIZE_SM)

    # Change tick spacing
    plot_object.set_xticks(plot_object.get_xticks()[::1])
    plot_object.xaxis.set_major_locator(
        MonthLocator(range(1, 13), bymonthday=1, interval=1),
    )
    plot_object.xaxis.set_major_formatter(DateFormatter("%b"))


def export_figure(figure: mpl.figure, output_filename: str) -> None:
    # Create the directory if it didn't exist already
    directory_path = Path(config["output_data"]["output_directory"])
    directory_path.mkdir(parents=True, exist_ok=True)

    # Form the file name
    filename = (
        config["output_data"]["output_directory"]
        + "/"
        + output_filename
        + config["output_format"]["format"]
    )

    # Page settings
    figure.set_size_inches(
        config["output_format"]["output_dim_x"],
        config["output_format"]["output_dim_y"],
    )
    figure.savefig(filename, bbox_inches="tight")

    if config["output_format"]["plotly_on"]:
        plotly.plot_mpl(figure, filename="Agenoria - " + output_filename)

    figure.clf()
