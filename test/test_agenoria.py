# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the  MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.


from pathlib import Path

import agenoria
from config import param as config

# pylint: disable=no-member


def get_filename(output_filename: str) -> str:
    return (
        config["output_data"]["output_directory"]
        + "/"
        + output_filename
        + config["output_format"]["format"]
    )


def test_diaper_charts() -> None:
    # Plot
    agenoria.plot_diaper_charts()

    # File
    path = get_filename(config["output_data"]["output_daily_diaper_charts"])

    # Get the file size of the output PDF
    file_size = Path(path).stat().st_size

    # Check the size is greater than 40 KB
    assert file_size > 20 * 1024, "Test failed - diaper charts"


def test_sleep_stats_charts() -> None:
    # Plot
    agenoria.plot_sleep_stats_charts()

    # File
    path = get_filename(
        config["output_data"]["output_daily_sleep_stats_charts"],
    )

    # Get the file size of the output PDF
    file_size = Path(path).stat().st_size

    # Check the size is greater than 40 KB
    assert file_size > 30 * 1024, "Test failed - diaper charts"


def test_feeding_stats_charts() -> None:
    # Plot
    agenoria.plot_feeding_stats_charts()

    # File
    path = get_filename(
        config["output_data"]["output_daily_feeding_stats_charts"],
    )

    # Get the file size of the output PDF
    file_size = Path(path).stat().st_size

    # Check the size is greater than 40 KB
    assert file_size > 40 * 1024, "Test failed - diaper charts"


def test_24h_viz() -> None:
    # Plot
    agenoria.plot_sleep_24h_viz()
    agenoria.plot_feeding_24h_viz()
    agenoria.plot_diapers_24h_viz()

    # Get the file size of the output PDF
    file_size_sleep = (
        Path(get_filename(config["output_data"]["output_sleep_viz"]))
        .stat()
        .st_size
    )
    file_size_feeding = (
        Path(get_filename(config["output_data"]["output_feeding_viz"]))
        .stat()
        .st_size
    )
    file_size_diaper = (
        Path(get_filename(config["output_data"]["output_diaper_viz"]))
        .stat()
        .st_size
    )

    # Check the size is greater than 40 KB
    assert file_size_sleep > 90 * 1024, "Test failed - sleep viz"
    assert file_size_feeding > 20 * 1024, "Test failed - feeding viz"
    assert file_size_diaper > 25 * 1024, "Test failed - diaper viz"


def test_growth_charts() -> None:
    # Plot
    agenoria.plot_growth_charts()

    # File
    path = get_filename(config["output_data"]["output_growth_charts"])

    # Get the file size of the output PDF
    file_size = Path(path).stat().st_size

    # Check the size is greater than 40 KB
    assert file_size > 10 * 1024, "Test failed - growth charts"


def test_medical_charts() -> None:
    # Plot
    agenoria.plot_medical_charts()

    # File
    path = get_filename(config["output_data"]["output_medical_charts"])

    # Get the file size of the output PDF
    file_size = Path(path).stat().st_size

    # Check the size is greater than 40 KB
    assert file_size > 10 * 1024, "Test failed - medical charts"
