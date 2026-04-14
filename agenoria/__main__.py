# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import multiprocessing
import timeit
from collections.abc import Callable
from multiprocessing import Process
from pathlib import Path

from config import param as config

from .plot_24h_viz import (
    plot_diapers_24h_viz,
    plot_feeding_24h_viz,
    plot_sleep_24h_viz,
)
from .plot_diaper_charts import plot_diaper_charts
from .plot_feeding_stats_charts import plot_feeding_stats_charts
from .plot_growth_charts import plot_growth_charts
from .plot_medical_charts import plot_medical_charts
from .plot_sleep_stats_charts import plot_sleep_stats_charts

PLOT_TASKS: tuple[tuple[str, Callable[[], None]], ...] = (
    ("build_daily_diaper_charts", plot_diaper_charts),
    ("build_daily_sleep_stats_charts", plot_sleep_stats_charts),
    ("build_daily_feeding_stats_charts", plot_feeding_stats_charts),
    ("build_growth_charts", plot_growth_charts),
    ("build_medical_charts", plot_medical_charts),
    ("build_sleep_viz", plot_sleep_24h_viz),
    ("build_feeding_viz", plot_feeding_24h_viz),
    ("build_diaper_viz", plot_diapers_24h_viz),
)


def get_enabled_plot_tasks() -> list[Callable[[], None]]:
    return [plot_fn for config_key, plot_fn in PLOT_TASKS if config["output_data"][config_key]]


def main() -> None:
    # Create a timer
    start = timeit.default_timer()

    # Create the output directory
    Path(config["output_data"]["output_directory"]).mkdir(
        parents=True,
        exist_ok=True,
    )

    # Spin off multi-process plotting
    procs = [Process(target=plot_task) for plot_task in get_enabled_plot_tasks()]
    for proc in procs:
        proc.start()

    # Complete the processes
    for proc in procs:
        proc.join()

    # Stop the clock
    stop = timeit.default_timer()

    print("Time elapsed: ", stop - start, " seconds")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
