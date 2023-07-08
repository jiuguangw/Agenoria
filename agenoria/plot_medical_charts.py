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
from pandas.plotting import register_matplotlib_converters

from config import misc_data
from config import param as config

from .plot_settings import export_figure, format_monthly_plot


def plot_daycare_days(plot_object: plt.figure, data: pd.DataFrame) -> None:
    # Group and compute sum by month. BMS gives 1st of month
    daycare_monthly = data["Daycare"].resample("BMS").sum()

    # Plot
    plot_object.plot(daycare_monthly.index, daycare_monthly)
    plot_object.set_title("Number of Days in Daycare by Months")
    plot_object.set_ylabel("Number of Days")
    plot_object.yaxis.set_ticks(np.arange(0, 21, 2))
    format_monthly_plot(
        plot_object, daycare_monthly.index[0], daycare_monthly.index[-1]
    )


def plot_days_between_vomit(
    plot_object: plt.figure, data: pd.DataFrame
) -> None:
    # Look up vomit days and compute gaps
    vomit_days = data.loc[data["Vomit"] == 1]
    days_since_last_vomit = vomit_days["Date"].diff() / np.timedelta64(1, "D")

    # Plots
    plot_object.plot(vomit_days["Date"], days_since_last_vomit)
    plot_object.set_title("Days Since Last Vomit")
    plot_object.set_xlabel("Date")
    plot_object.set_ylabel("Days Since Last Vomit")
    format_monthly_plot(plot_object, vomit_days.index[0], vomit_days.index[-1])


def plot_doctor_visit_monthly(
    plot_object: plt.figure, data: pd.DataFrame
) -> None:
    # Group and compute sum by month. BMS gives 1st of month
    doctor_monthly = data["Doctor"].resample("BMS").sum()

    # Plot
    plot_object.plot(doctor_monthly.index, doctor_monthly)
    plot_object.set_title("Total Number of Doctor Visits by Months")
    plot_object.set_ylabel("Total Number of Doctor Visits")
    plot_object.yaxis.set_ticks(np.arange(0, 5, 1))
    format_monthly_plot(
        plot_object, doctor_monthly.index[0], doctor_monthly.index[-1]
    )


def plot_monthly_vomit(plot_object: plt.figure, data: pd.DataFrame) -> None:
    # Group and compute sum by month. BMS gives 1st of month
    vomit_monthly = data["Vomit"].resample("BMS").sum()

    # Plot
    plot_object.plot(vomit_monthly.index, vomit_monthly)
    plot_object.set_title("Total Number of Vomits by Months")
    plot_object.set_ylabel("Total Number of Vomits")
    format_monthly_plot(
        plot_object, vomit_monthly.index[0], vomit_monthly.index[-1]
    )


def plot_medical_charts() -> None:
    register_matplotlib_converters()

    # Style
    sns.set(style="darkgrid")
    fig, axarr = plt.subplots(2, 3)

    # Chart 1 - Total Vomit Per Month
    plot_monthly_vomit(axarr[0, 0], misc_data)

    # Chart 2 - Days Between Vomit
    plot_days_between_vomit(axarr[0, 1], misc_data)

    # Chart 3 - Days in Daycare
    plot_daycare_days(axarr[0, 2], misc_data)

    # Chart 4 - Doctor Visits
    plot_doctor_visit_monthly(axarr[1, 0], misc_data)

    # Export
    fig.subplots_adjust(wspace=0.25, hspace=0.35)
    export_figure(fig, config["output_data"]["output_medical_charts"])
