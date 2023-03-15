#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import multiprocessing
import os
import timeit
from multiprocessing import Process

from config import param as config

from .plot_24h_viz import (plot_diapers_24h_viz, plot_feeding_24h_viz,
                           plot_sleep_24h_viz)
from .plot_diaper_charts import plot_diaper_charts
from .plot_feeding_stats_charts import plot_feeding_stats_charts
from .plot_growth_charts import plot_growth_charts
from .plot_medical_charts import plot_medical_charts
from .plot_sleep_stats_charts import plot_sleep_stats_charts


def main() -> None:
    # Create a timer
    start = timeit.default_timer()

    # Create the output directory
    if not os.path.exists(config['output_data']['output_directory']):
        os.makedirs(config['output_data']['output_directory'])

    # Spin off multi-process plotting
    procs = []

    if config['output_data']['build_daily_diaper_charts']:
        proc = Process(target=plot_diaper_charts)
        procs.append(proc)
        proc.start()

    if config['output_data']['build_daily_sleep_stats_charts']:
        proc = Process(target=plot_sleep_stats_charts)
        procs.append(proc)
        proc.start()

    if config['output_data']['build_daily_feeding_stats_charts']:
        proc = Process(target=plot_feeding_stats_charts)
        procs.append(proc)
        proc.start()

    if config['output_data']['build_growth_charts']:
        proc = Process(target=plot_growth_charts)
        procs.append(proc)
        proc.start()

    if config['output_data']['build_medical_charts']:
        proc = Process(target=plot_medical_charts)
        procs.append(proc)
        proc.start()

    if config['output_data']['build_sleep_viz']:
        proc = Process(target=plot_sleep_24h_viz)
        procs.append(proc)
        proc.start()

    if config['output_data']['build_feeding_viz']:
        proc = Process(target=plot_feeding_24h_viz)
        procs.append(proc)
        proc.start()

    if config['output_data']['build_diaper_viz']:
        proc = Process(target=plot_diapers_24h_viz)
        procs.append(proc)
        proc.start()

    # Complete the processes
    for proc in procs:
        proc.join()

    # Stop the clock
    stop = timeit.default_timer()

    print('Time elapsed: ', stop - start, ' seconds')


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
