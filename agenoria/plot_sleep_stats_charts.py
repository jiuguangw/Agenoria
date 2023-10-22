# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from dateutil.relativedelta import relativedelta
from pandas.plotting import register_matplotlib_converters

from config import param as config
from config import sleep_data

from .parse_config import get_daytime_index
from .plot_settings import export_figure, format_monthly_plot

ALPHA_VALUE = 0.3
SLEEP_THRESHOLD = 0.0333333  # two minutes -> hours


def parse_glow_sleep_data(data_sleep: pd.DataFrame) -> pd.DataFrame:
    # Find first and last entry in column
    start_date = data_sleep["Date"].iloc[-1]
    end_date = data_sleep["Date"].iloc[0]

    if config["debug"]["debug_mode"]:
        start_date = config["debug"]["debug_start_date"]
        end_date = config["debug"]["debug_end_date"]

    sleep_data_list = []
    offset = 0

    # For some reason raw sleep data is not sorted by time
    data_sleep = data_sleep.sort_values(["Begin time"], ascending=False)

    # Get duration for each row, then convert to hours
    data_sleep["duration"] = data_sleep["End time"] - data_sleep["Begin time"]
    data_sleep["duration"] = data_sleep["duration"] / np.timedelta64(1, "h")

    # Find the index of session that extend into the next day
    index = data_sleep["End time"].dt.normalize() > data_sleep["Date"]

    # Compute the offset duration to be plotted the next day
    sleep_offset = data_sleep.loc[index, "End time"]
    data_sleep.loc[index, "offset"] = (
        sleep_offset.dt.hour + sleep_offset.dt.minute / 60
    )

    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        rows_on_date = data_sleep[data_sleep["Date"].isin([current_date])]

        # Remove all sleep sessions less than two minutes
        filtered = rows_on_date[rows_on_date["duration"] > SLEEP_THRESHOLD]

        # Get total sleep duration
        total_sleep_duration = filtered["duration"].sum()

        # Add offset from previous day
        total_sleep_duration += offset

        # Catch session that extend past midnight, subtract from duration
        offset = rows_on_date["offset"].sum()
        total_sleep_duration -= offset

        # Longest session
        longest_session = rows_on_date["duration"].max()

        # Compute longest awake time - begin (current time) -  end (next row)
        end_time_shifted = filtered["End time"].shift(-1)
        awake_duration = filtered["Begin time"] - end_time_shifted
        max_awake_duration = awake_duration.max() / np.timedelta64(1, "h")

        # Remove session that extends into other days
        filtered2 = filtered[
            filtered["End time"].dt.normalize() == current_date
        ]

        # Nap sessions must begin and end within the defined window
        nap_index1 = get_daytime_index(filtered2["Begin time"])
        nap_index2 = get_daytime_index(filtered2["End time"])
        nap_rows = filtered2[nap_index1 & nap_index2]

        # Compute stats on nap sessions
        nap_sessions_on_date = len(nap_rows.index)
        nap_duration_on_date = nap_rows["duration"].sum()

        # Total nighttime duration
        nighttime_duration = total_sleep_duration - nap_duration_on_date

        # Put stats in a list
        sleep_data_list.append(
            [
                current_date,
                nap_sessions_on_date,
                total_sleep_duration,
                nap_duration_on_date,
                nighttime_duration,
                longest_session,
                max_awake_duration,
            ],
        )

    # Convert list to dataframe
    return pd.DataFrame(
        sleep_data_list,
        columns=[
            "date",
            "total_naps",
            "total_sleep_duration",
            "total_nap_duration",
            "total_nighttime_duration",
            "longest_session",
            "max_awake_duration",
        ],
    )


def plot_sleep_stats_charts() -> None:
    # Matplotlib converters
    register_matplotlib_converters()

    # Style
    sns.set(style="darkgrid")
    fig, axarr = plt.subplots(2, 3)

    # Parse data
    data_sleep_daily = parse_glow_sleep_data(sleep_data)

    # Start date
    xlim_left = data_sleep_daily["date"].iloc[0]
    # End date - one year or full
    if config["output_format"]["output_year_one_only"]:
        xlim_right = xlim_left + relativedelta(years=1)
    else:
        xlim_right = data_sleep_daily["date"].iloc[-1]

    # Chart 1 - Sleep: Daily Total Naps (7:00-19:00)
    axarr[0, 0].plot(data_sleep_daily["date"], data_sleep_daily["total_naps"])
    axarr[0, 0].set_title("Sleep: Daily Total Naps (7:00-19:00)")
    axarr[0, 0].set_ylabel("Total Naps")
    format_monthly_plot(axarr[0, 0], xlim_left, xlim_right)

    # Chart 2 - Sleep: Daily Longest Duration of Uninterrupted Sleep (Hours)
    axarr[0, 1].plot(
        data_sleep_daily["date"],
        data_sleep_daily["longest_session"],
    )
    axarr[0, 1].set_title("Sleep: Daily Longest Sleep Duration (Hr)")
    axarr[0, 1].set_ylabel("Longest Sleep Duration (Hr)")
    format_monthly_plot(axarr[0, 1], xlim_left, xlim_right)

    # Chart 3 - Sleep: Daily Total Sleep (Hours)
    axarr[0, 2].plot(
        data_sleep_daily["date"],
        data_sleep_daily["total_sleep_duration"],
    )
    axarr[0, 2].set_title("Sleep: Daily Total Sleep (Hr)")
    axarr[0, 2].set_ylabel("Total Sleep (Hr)")
    format_monthly_plot(axarr[0, 2], xlim_left, xlim_right)

    # Chart 4 - Sleep: Daily Daytime Sleep (Hours)
    axarr[1, 0].plot(
        data_sleep_daily["date"],
        data_sleep_daily["total_nap_duration"],
    )
    axarr[1, 0].set_title("Sleep: Daily Total Daytime Sleep (Hr)")
    axarr[1, 0].set_ylabel("Total Sleep (Hr)")
    format_monthly_plot(axarr[1, 0], xlim_left, xlim_right)

    # Chart 5 - Sleep: Daily Nighttime Sleep (Hours)
    axarr[1, 1].plot(
        data_sleep_daily["date"],
        data_sleep_daily["total_nighttime_duration"],
    )
    axarr[1, 1].set_title("Sleep: Daily Total Nighttime Sleep (Hr)")
    axarr[1, 1].set_ylabel("Total Sleep (Hr)")
    format_monthly_plot(axarr[1, 1], xlim_left, xlim_right)

    # Chart 6 - Daily Maximum Awake Duration (Hr)
    axarr[1, 2].plot(
        data_sleep_daily["date"],
        data_sleep_daily["max_awake_duration"],
    )
    axarr[1, 2].set_title("Daily Maximum Awake Duration (Hr)")
    axarr[1, 2].set_ylabel("Maximum Awake Duration (Hr)")
    format_monthly_plot(axarr[1, 2], xlim_left, xlim_right)

    # Export
    fig.subplots_adjust(wspace=0.2, hspace=0.35)
    export_figure(
        fig,
        config["output_data"]["output_daily_sleep_stats_charts"],
    )
