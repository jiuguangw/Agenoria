#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the  MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

from matplotlib.dates import MonthLocator, DateFormatter
import numpy as np


def enumerate_labels(date_num):
    hour_labels = []
    for num in range(0, 24):
        label = str(num) + ':00'
        hour_labels.append(label)

    week_labels = []
    for num in range(0, int(round(date_num / 7))):
        label = str(num)
        week_labels.append(label)

    return hour_labels, week_labels


def format_24h_week_plot(ax, date_num, title):
    # Figure settings
    TITLE_FONT_SIZE = 25
    AXIS_FONT_SIZE = 15
    TITLE_HEIGHT_ADJUST = 1.05

    # Create the tick labels
    hour_labels, week_labels = enumerate_labels(date_num)

    # Set title and axis labels
    ax.set_title(title, fontsize=TITLE_FONT_SIZE, y=TITLE_HEIGHT_ADJUST)
    ax.set_xlabel('Age (weeks)', fontsize=AXIS_FONT_SIZE)
    ax.set_ylabel('Time of Day', fontsize=AXIS_FONT_SIZE)

    # Format y axis - clock time
    ax.set_ylim(0, 24)
    ax.yaxis.set_ticks(np.arange(0, 24, 1))
    ax.set_yticklabels(hour_labels)
    ax.invert_yaxis()

    # Format x axis - bottom, week number
    ax.set_xlim(1, date_num)
    ax.xaxis.set_ticks(np.arange(1, date_num, 7))
    ax.set_xticklabels(week_labels)


def format_growth_chart_plot(plot_object):
    # Figure settings
    TITLE_FONT_SIZE = 14
    AXIS_FONT_SIZE = 10

    # Change label sizes
    plot_object.title.set_size(TITLE_FONT_SIZE)
    plot_object.xaxis.label.set_size(AXIS_FONT_SIZE)
    plot_object.yaxis.label.set_size(AXIS_FONT_SIZE)
    plot_object.tick_params(labelsize=AXIS_FONT_SIZE)


def format_monthly_plot(plot_object, xlim_left, xlim_right):
    # Figure settings
    TITLE_FONT_SIZE = 10
    AXIS_FONT_SIZE = 8

    # Axis label
    plot_object.set_xlabel('Date')

    # Change x-axis left and right limits
    plot_object.set_xlim(xlim_left, xlim_right)

    # Change label sizes
    plot_object.title.set_size(TITLE_FONT_SIZE)
    plot_object.xaxis.label.set_size(AXIS_FONT_SIZE)
    plot_object.yaxis.label.set_size(AXIS_FONT_SIZE)
    plot_object.tick_params(labelsize=AXIS_FONT_SIZE)

    # Change tick spacing
    plot_object.set_xticks(plot_object.get_xticks()[::1])
    plot_object.xaxis.set_major_locator(
        MonthLocator(range(1, 13), bymonthday=1, interval=1))
    plot_object.xaxis.set_major_formatter(DateFormatter("%b"))


def export_figure(figure, dim_x, dim_y, output_filename):
    # Export
    figure.subplots_adjust(wspace=0.2, hspace=0.5)
    figure.set_size_inches(dim_x, dim_y)
    figure.savefig(output_filename, bbox_inches='tight')
    figure.clf()
