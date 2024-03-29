# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dateutil.relativedelta import relativedelta
from pandas.plotting import register_matplotlib_converters

from config import diaper_data
from config import param as config

from .plot_settings import export_figure, format_monthly_plot

CUTOFF = 65


def count_pee_poop(row: pd.DataFrame) -> tuple[int, int]:
    # Return variables
    pee = 0
    poop = 0

    # Parse
    key = row["In the diaper"]
    if key == "pee":  # Pee only
        pee += 1
    elif key == "poo":
        poop += 1
    elif key == "pee and poo":
        pee += 1
        poop += 1

    return pee, poop


def parse_glow_diaper_data(data_diaper: pd.DataFrame) -> pd.DataFrame:
    # Find first and last entry in column
    start_date = data_diaper["Date"].iloc[-1]
    end_date = data_diaper["Date"].iloc[0]

    if config["debug"]["debug_mode"]:
        start_date = config["debug"]["debug_start_date"]
        end_date = config["debug"]["debug_end_date"]

    # Final data
    diaper_data_list = []
    cumulative_diaper_count = 0

    # Diaper
    for current_date in pd.date_range(start_date, end_date):
        # Get all entires on this date
        rows_on_date = data_diaper[data_diaper["Date"].isin([current_date])]

        # Compute total diaper count
        daily_total_diaper_count = rows_on_date["In the diaper"].count()
        cumulative_diaper_count += rows_on_date["In the diaper"].count()

        # Separate pees and poops
        total_pee_count = 0
        total_poop_count = 0
        for _index, diaper_event in rows_on_date.iterrows():
            pee, poop = count_pee_poop(diaper_event)
            total_pee_count += pee
            total_poop_count += poop

        # Compute poop to total diaper change ratio
        poop_ratio = (total_poop_count / daily_total_diaper_count) * 100

        # Compute diaper day duration
        diaper_final = rows_on_date["Diaper time"].iloc[0]
        diaper_first = rows_on_date["Diaper time"].iloc[-1]
        diaper_day_duration = (
            diaper_final - diaper_first
        ).total_seconds() / 3600

        # Compute average time between diaper changes
        diaper_change_time_avg = diaper_day_duration / daily_total_diaper_count

        # Put stats in a list
        diaper_data_list.append(
            [
                current_date,
                daily_total_diaper_count,
                cumulative_diaper_count,
                total_pee_count,
                total_poop_count,
                poop_ratio,
                diaper_change_time_avg,
            ],
        )

    # Convert list to dataframe
    return pd.DataFrame(
        diaper_data_list,
        columns=[
            "date",
            "daily_total_diaper_count",
            "cumulative_diaper_count",
            "pee_count",
            "poop_count",
            "poop_ratio",
            "diaper_change_time_avg",
        ],
    )


def get_abnormal_days(
    daily_diaper_data: pd.DataFrame,
) -> pd.DataFrame:
    # Constipation monthly - days with zero poop
    constipation_days = daily_diaper_data.loc[
        daily_diaper_data["poop_count"] == 0
    ]
    constipation_days = constipation_days.set_index(constipation_days["date"])
    constipation_monthly = (
        constipation_days["daily_total_diaper_count"].resample("BMS").count()
    )

    # Diarrhea monthly - days with high percentage of poops
    diarrhea_days = daily_diaper_data.loc[
        daily_diaper_data["poop_ratio"] >= CUTOFF
    ]
    diarrhea_days = diarrhea_days.set_index(diarrhea_days["date"])
    diarrhea_monthly = (
        diarrhea_days["daily_total_diaper_count"].resample("BMS").count()
    )

    return constipation_monthly, diarrhea_monthly


def get_diaper_monthly_data(daily_diaper_data: pd.DataFrame) -> pd.DataFrame:
    # Reindex
    monthly_data = daily_diaper_data.set_index(daily_diaper_data["date"])

    # Compute monthly total
    return monthly_data["daily_total_diaper_count"].resample("BMS").sum()


def plot_diaper_charts() -> None:
    # Matplotlib converters
    register_matplotlib_converters()

    # Style
    sns.set(style="darkgrid")
    fig, axarr = plt.subplots(3, 3)

    # Parse data
    daily_diaper_data = parse_glow_diaper_data(diaper_data)
    diaper_monthly_data = get_diaper_monthly_data(daily_diaper_data)
    constipation_monthly_data, diarrhea_monthly_data = get_abnormal_days(
        daily_diaper_data,
    )

    # Start date
    xlim_left = daily_diaper_data["date"].iloc[0]
    # End date - one year or full
    if config["output_format"]["output_year_one_only"]:
        xlim_right = xlim_left + relativedelta(years=1)
    else:
        xlim_right = daily_diaper_data["date"].iloc[-1]

    # Chart 1 - Diaper: Total Diapers (Cumulative)
    axarr[0, 0].plot(
        daily_diaper_data["date"],
        daily_diaper_data["cumulative_diaper_count"],
    )
    axarr[0, 0].set_title("Diaper: Total Diapers (Cumulative)")
    axarr[0, 0].set_ylabel("Total Diapers")
    format_monthly_plot(axarr[0, 0], xlim_left, xlim_right)

    # Chart 2 - Diaper: Number of Diapers by Month
    axarr[0, 1].plot(diaper_monthly_data.index, diaper_monthly_data)
    axarr[0, 1].set_title("Diaper: Number of Diapers by Month")
    axarr[0, 1].set_ylabel("Number of Diapers by Month")
    format_monthly_plot(axarr[0, 1], xlim_left, xlim_right)

    # Chart 3 - Diaper: Daily Total Diaper Count
    axarr[0, 2].plot(
        daily_diaper_data["date"],
        daily_diaper_data["daily_total_diaper_count"],
    )
    axarr[0, 2].set_title("Diaper: Number of Diapers by Day")
    axarr[0, 2].set_ylabel("Number of Diapers by Day")
    format_monthly_plot(axarr[0, 2], xlim_left, xlim_right)

    # Chart 4 - Diaper: Daily Total Pees
    axarr[1, 0].plot(daily_diaper_data["date"], daily_diaper_data["pee_count"])
    axarr[1, 0].set_title("Diaper: Daily Total Pees")
    axarr[1, 0].set_ylabel("Total Pees")
    format_monthly_plot(axarr[1, 0], xlim_left, xlim_right)

    # Chart 5 - Diaper: Daily Total Poops
    axarr[1, 1].plot(
        daily_diaper_data["date"],
        daily_diaper_data["poop_count"],
    )
    axarr[1, 1].set_title("Diaper: Daily Total Poops")
    axarr[1, 1].set_ylabel("Total Poops")
    format_monthly_plot(axarr[1, 1], xlim_left, xlim_right)

    # Chart 6 - Diaper: Average Time Between Diaper Changes
    axarr[1, 2].plot(
        daily_diaper_data["date"],
        daily_diaper_data["diaper_change_time_avg"],
    )
    axarr[1, 2].set_title(
        "Diaper: Average Time Between Diaper Changes (Hours)",
    )
    axarr[1, 2].set_ylabel("Average Time Between Diaper Changes (Hours)")
    format_monthly_plot(axarr[1, 2], xlim_left, xlim_right)

    # Chart 7 - Diaper: Poop Ratio
    axarr[2, 0].plot(
        daily_diaper_data["date"],
        daily_diaper_data["poop_ratio"],
    )
    axarr[2, 0].set_title("Diaper: Poop as Percentage of Diaper Changes")
    axarr[2, 0].set_ylabel("Poop as Percentage of Diaper Changes")
    format_monthly_plot(axarr[2, 0], xlim_left, xlim_right)

    # Chart 8 - Diaper: Constipation
    axarr[2, 1].plot(
        constipation_monthly_data.index,
        constipation_monthly_data,
    )
    axarr[2, 1].set_title("Diaper: Number of Constipated Days by Month")
    axarr[2, 1].set_ylabel("Number of Constipated Days")
    format_monthly_plot(axarr[2, 1], xlim_left, xlim_right)

    # Chart 9 - Diaper: Diarrhea
    axarr[2, 2].plot(diarrhea_monthly_data.index, diarrhea_monthly_data)
    axarr[2, 2].set_title("Diaper: Number of Diarrhea Days by Month")
    axarr[2, 2].set_ylabel("Number of Diarrhea Days")
    format_monthly_plot(axarr[2, 2], xlim_left, xlim_right)

    # Export
    fig.subplots_adjust(wspace=0.2, hspace=0.35)
    export_figure(fig, config["output_data"]["output_daily_diaper_charts"])
