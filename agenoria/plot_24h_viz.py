# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import matplotlib.patches as plot_patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from config import (
    diaper_data,
    feeding_bottle_data,
    feeding_solid_data,
    sleep_data,
)
from config import param as config

from .plot_settings import (
    export_figure,
    format_24h_week_plot_horizontal,
    format_24h_week_plot_vertical,
)

BAR_SIZE = 1


def get_end_date(data: pd.DataFrame, *, first_year_only: bool) -> int:
    # Assign the end date. Either 365 or actual day number.
    return 365 if first_year_only else data.iloc[0]


def parse_raw_data(data: pd.DataFrame, key: list[str]) -> pd.DataFrame:
    # Get start and end dates
    start_date = data["Date"].iloc[-1]

    # Convert timesteamp to decimal hour
    data["timestamp_hour"] = data[key[0]].dt.hour + data[key[0]].dt.minute / 60

    # Convert date to day number
    data["day_number"] = (data["Date"] - start_date).dt.days + 1

    return data


def plot_sleep_24h_viz() -> None:
    # Import and extract sleep data
    data = parse_raw_data(sleep_data, ["Begin time", "End time"])

    # Convert end time timestamp to decimal hours
    data["end_timestamp_hour"] = (
        data["End time"].dt.hour + data["End time"].dt.minute / 60
    )

    # Compute duration in decimal hours
    data["duration"] = data["end_timestamp_hour"] - data["timestamp_hour"]

    # Find the index of session that extend into the next day
    index = data["End time"].dt.normalize() > data["Date"]

    # Compute the offset duration to be plotted the next day
    data.loc[index, "offset"] = data["end_timestamp_hour"]

    # Compute the current day duration, cut off to midnight
    data.loc[index, "duration"] = 24 - data["timestamp_hour"]

    # Plot setup
    sns.set(style="darkgrid")
    figure = plt.figure()
    fig_ax = figure.add_subplot(111)

    # Find sessions with offsets and plot the offset with day_number+1
    data.loc[index].apply(
        lambda row: fig_ax.broken_barh(
            [(row["day_number"] + 1, BAR_SIZE)],
            [0, row["offset"]],
        ),
        axis=1,
    )

    # Loop through each row and plot the duration
    data.apply(
        lambda row: fig_ax.broken_barh(
            [(row["day_number"], BAR_SIZE)],
            [row["timestamp_hour"], row["duration"]],
        ),
        axis=1,
    )

    # End date - one year or full
    end_date = get_end_date(
        data["day_number"],
        first_year_only=config["output_format"]["output_year_one_only"],
    )

    # Format plot - vertical or horizontal
    if config["output_format"]["output_sleep_viz_orientation"] == "vertical":
        format_24h_week_plot_vertical(fig_ax, end_date)
    else:
        format_24h_week_plot_horizontal(fig_ax, end_date, "Sleep")

    # Export figure
    export_figure(figure, config["output_data"]["output_sleep_viz"])


def plot_feeding_24h_viz() -> None:
    # Import and extract feeding data
    data_bottle = parse_raw_data(feeding_bottle_data, ["Time of feeding"])
    data_solid = parse_raw_data(feeding_solid_data, ["Time of feeding"])

    # Plot setup
    sns.set(style="darkgrid")
    figure = plt.figure()
    fig_ax = figure.add_subplot(111)

    # Compute offset from birthday
    offset = data_solid["Date"].iloc[-1] - pd.Timestamp(
        config["info"]["birthday"],
    )
    offset = int(offset / np.timedelta64(1, "D"))  # Convert to day in int

    # Plot
    fig_ax.scatter(
        data_bottle["day_number"],
        data_bottle["timestamp_hour"],
        s=25,
        c="r",
    )
    fig_ax.scatter(
        data_solid["day_number"] + offset,
        data_solid["timestamp_hour"],
        s=25,
        c="b",
    )

    # Legend
    red_patch = plot_patches.Patch(color="r", label="Bottle Feeding")
    blue_patch = plot_patches.Patch(color="b", label="Solid Feeding")
    plt.legend(handles=[red_patch, blue_patch])

    # End date - one year or full
    end_date = get_end_date(
        data_bottle["day_number"],
        first_year_only=config["output_format"]["output_year_one_only"],
    )

    # Format plot
    format_24h_week_plot_horizontal(fig_ax, end_date, "Feeding")

    # Export figure
    export_figure(figure, config["output_data"]["output_feeding_viz"])


def map_poop_color(color: str) -> str:
    # If input is null, then it's pee
    if pd.isna(color):  # pee only, yellow
        return "y"

    # Map from Glow color to matplotlib color key
    color_map = {
        "yellow": "b",  # poop, yellow
        "green": "g",  # poop, green
        "brown": "m",  # poop, brown
        pd.NaT: "y",  # pee only, yellow
    }
    return color_map.get(color, "r")  # poop, other colors


def plot_diapers_24h_viz() -> None:
    # Import and extract feeding data
    data = parse_raw_data(diaper_data, ["Diaper time"])

    # Go through poop colors and map to matplotlib color keys
    data["Color key"] = data["Color"].apply(map_poop_color)

    # Plot setup
    sns.set(style="darkgrid")
    figure = plt.figure()
    fig_ax = figure.add_subplot(111)

    # Plot
    fig_ax.scatter(
        data["day_number"],
        data["timestamp_hour"],
        s=25,
        c=data["Color key"],
    )

    # Legend
    blue_patch = plot_patches.Patch(color="b", label="Poop, Yellow")
    green_patch = plot_patches.Patch(color="g", label="Poop, Green")
    brown_patch = plot_patches.Patch(color="m", label="Poop, Brown")
    red_patch = plot_patches.Patch(color="r", label="Poop, Others")
    yellow_patch = plot_patches.Patch(color="y", label="Pee")
    plt.legend(
        handles=[
            blue_patch,
            green_patch,
            brown_patch,
            red_patch,
            yellow_patch,
        ],
    )

    # End date - one year or full
    end_date = get_end_date(
        data["day_number"],
        first_year_only=config["output_format"]["output_year_one_only"],
    )

    # Format plot
    format_24h_week_plot_horizontal(fig_ax, end_date, "Diapers")

    # Export figure
    export_figure(figure, config["output_data"]["output_diaper_viz"])
