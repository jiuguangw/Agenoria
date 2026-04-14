# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import ticker
from matplotlib.axes import Axes

from config import growth_data
from config import hatch_data as hatch_weight_data
from config import param as config

from .plot_settings import export_figure, format_growth_chart_plot

LINE_ALPHA = 0.4
ROC_WINDOW = 14


def compute_age(date: pd.Series, birthday: pd.Timestamp) -> pd.Series:
    return (date - birthday) / np.timedelta64(4, "W")


def parse_glow_data(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    parsed = data.copy()

    # Compute age
    parsed["Age"] = compute_age(
        parsed["Date"],
        pd.Timestamp(config["info"]["birthday"]),
    )

    # Get date and height columns
    data_height = parsed[parsed["Height(cm)"].notna()][["Date", "Age", "Height(cm)"]]
    data_head = parsed[parsed["Head Circ.(cm)"].notna()][["Date", "Age", "Head Circ.(cm)"]]

    return data_height, data_head


def parse_hatch_data(data: pd.DataFrame) -> pd.DataFrame:
    parsed = data.copy()

    # Keep date only, remove time. Hatch invalid format: redundant AM/PM
    hatch_dates = parsed["Start Time"].astype(str).str[0:10]
    # Convert to datetime
    parsed["Start Time"] = pd.to_datetime(hatch_dates, format="%m/%d/%Y")

    # Sort and remove duplicates
    parsed = parsed.sort_values(by=["Start Time"], ascending=True)
    parsed = parsed.drop_duplicates(subset=["Start Time"], keep=False)

    # Reindex and add missing days
    idx = pd.date_range(
        start=parsed["Start Time"].min(),
        end=parsed["Start Time"].max(),
    )
    parsed = parsed.set_index("Start Time").reindex(idx).rename_axis("Start Time").reset_index()

    # Compute Age
    parsed["Age"] = compute_age(
        parsed["Start Time"],
        pd.Timestamp(config["info"]["birthday"]),
    )

    # Compute diff
    parsed["ROC"] = parsed["Amount"].diff()
    # Fill empty rows with 0
    parsed["ROC"] = parsed["ROC"].fillna(0)

    # Compute average on a rolling window
    parsed["Weight Average RoC"] = parsed["ROC"].rolling(window=ROC_WINDOW).mean()

    # Convert to oz
    parsed["Weight Average RoC"] = parsed["Weight Average RoC"] * 35.274

    return parsed


def plot_growth_curves(
    curve_file: str,
    index: str,
    plot_object: Axes,
) -> None:
    # Import growth curves data file
    data_raw = pd.read_csv(curve_file)

    # Extract by sex
    sex = 1 if (config["info"]["gender"] == "boy") else 2
    data = data_raw.loc[data_raw["Sex"] == sex]

    # Plot percentile lines
    for percentile in ("P3", "P5", "P10", "P25", "P50", "P75", "P90", "P95", "P97"):
        plot_object.plot(data[index], data[percentile], alpha=LINE_ALPHA)


def plot_weight_length(
    plot_object: Axes,
    data_height: pd.DataFrame,
    hatch_data: pd.DataFrame,
) -> None:
    data_weight_length = (
        data_height.merge(
            hatch_data[["Start Time", "Amount"]],
            left_on="Date",
            right_on="Start Time",
            how="left",
        )
        .dropna(subset=["Amount"])
        .rename(columns={"Amount": "Weight"})
    )

    # Plot data
    plot_object.plot(
        data_weight_length["Height(cm)"],
        data_weight_length["Weight"],
    )
    # Labels
    plot_object.set_title("Weight vs. Length")
    plot_object.set_xlabel("Length (cm)")
    plot_object.set_ylabel("Weight (kg)")
    plot_object.set_xlim(53, 90)
    plot_object.set_ylim(3.5, 12)
    plot_object.xaxis.set_major_locator(ticker.MultipleLocator(5))
    format_growth_chart_plot(plot_object)


def plot_growth_charts() -> None:
    # Settings
    sns.set(style="darkgrid")
    plt.rcParams["lines.linewidth"] = 2
    fig, axarr = plt.subplots(2, 3)

    # Import data
    data_height, data_head = parse_glow_data(growth_data)
    hatch_data = parse_hatch_data(hatch_weight_data)

    # Start & end date - one year or full
    start_date = 0
    if config["output_format"]["output_year_one_only"]:
        end_date = 12
    else:
        end_date = hatch_data["Age"].iloc[-1]

    # Chart 1 - Weight / Age
    plot_growth_curves(
        config["input_data"]["growth_curve_weight"],
        "Agemos",
        axarr[0, 0],
    )
    axarr[0, 0].plot(hatch_data["Age"], hatch_data["Amount"])
    axarr[0, 0].set_title("Weight vs. Age")
    axarr[0, 0].set_xlabel("Age (months)")
    axarr[0, 0].set_ylabel("Weight (kg)")
    axarr[0, 0].set_xlim(start_date, end_date)
    axarr[0, 0].set_ylim(3, 12)
    axarr[0, 0].xaxis.set_major_locator(ticker.MultipleLocator(1))
    axarr[0, 0].yaxis.set_major_locator(ticker.MultipleLocator(1))
    format_growth_chart_plot(axarr[0, 0])

    # Chart 2 - Weight Percentile / Age
    axarr[0, 1].plot(hatch_data["Age"], hatch_data["Percentile"] * 100)
    axarr[0, 1].set_title("Weight Percentile vs. Age")
    axarr[0, 1].set_ylabel("Weight Percentile (%)")
    axarr[0, 1].set_xlabel("Age (months)")

    axarr[0, 1].set_xlim(start_date, end_date)
    axarr[0, 1].xaxis.set_major_locator(ticker.MultipleLocator(1))
    axarr[0, 1].autoscale(enable=True, axis="y", tight=True)
    format_growth_chart_plot(axarr[0, 1])

    # Chart 2 - Weight Rate of Change / Age
    axarr[0, 2].plot(hatch_data["Age"], hatch_data["Weight Average RoC"])
    axarr[0, 2].set_title("Average Daily Weight Gain vs. Age")
    axarr[0, 2].set_xlabel("Age (months)")
    axarr[0, 2].set_ylabel("Average Daily Weight Gain (oz)")
    axarr[0, 2].set_xlim(start_date, end_date)
    axarr[0, 2].autoscale(enable=True, axis="y", tight=True)
    axarr[0, 2].xaxis.set_major_locator(ticker.MultipleLocator(1))
    axarr[0, 2].yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    format_growth_chart_plot(axarr[0, 2])

    # Chart 4 - Length / Age
    plot_growth_curves(
        config["input_data"]["growth_curve_length"],
        "Agemos",
        axarr[1, 0],
    )
    axarr[1, 0].plot(data_height["Age"], data_height["Height(cm)"])
    axarr[1, 0].set_title("Length vs. Age")
    axarr[1, 0].set_xlabel("Age (months)")
    axarr[1, 0].set_ylabel("Length (cm)")
    axarr[1, 0].set_xlim(start_date, end_date)
    axarr[1, 0].set_ylim(53, 80)
    axarr[1, 0].xaxis.set_major_locator(ticker.MultipleLocator(1))
    format_growth_chart_plot(axarr[1, 0])

    # Chart 5 - Head Circumference / Age
    plot_growth_curves(
        config["input_data"]["growth_curve_head"],
        "Agemos",
        axarr[1, 1],
    )
    axarr[1, 1].plot(data_head["Age"], data_head["Head Circ.(cm)"])
    axarr[1, 1].set_title("Head Circumference vs. Age")
    axarr[1, 1].set_xlabel("Age (months)")
    axarr[1, 1].set_ylabel("Head Circumference (cm)")
    axarr[1, 1].set_xlim(start_date, end_date)
    axarr[1, 1].set_ylim(35, 48)
    axarr[1, 1].xaxis.set_major_locator(ticker.MultipleLocator(1))
    format_growth_chart_plot(axarr[1, 1])

    # Chart 6 - Weight / Length
    plot_growth_curves(
        config["input_data"]["growth_curve_weight_length"],
        "Length",
        axarr[1, 2],
    )
    plot_weight_length(axarr[1, 2], data_height, hatch_data)

    # Export
    fig.subplots_adjust(wspace=0.25, hspace=0.35)
    export_figure(fig, config["output_data"]["output_growth_charts"])
