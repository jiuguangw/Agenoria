#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import agenoria
import os
import timeit
from multiprocessing import Process

# Create a timer
start = timeit.default_timer()

# Create the output directory
if not os.path.exists('build'):
    os.makedirs('build')

# Parse JSON config file
config_file = 'config_zyw.json'
config = agenoria.parse_json_config(config_file)

# Import data
diaper_data, sleep_data, feeding_bottle_data, feeding_solid_data, misc_data = agenoria.import_data(
    config)

# Spin off multi-process plotting
procs = []

proc = Process(target=agenoria.plot_diaper_charts,
               args=(config, diaper_data, ))
procs.append(proc)
proc.start()

proc = Process(target=agenoria.plot_sleep_stats_charts,
               args=(config, sleep_data, ))
procs.append(proc)
proc.start()

proc = Process(target=agenoria.plot_feeding_stats_charts, args=(
    config, feeding_bottle_data, feeding_solid_data, ))
procs.append(proc)
proc.start()

proc = Process(target=agenoria.plot_growth_charts, args=(config,))
procs.append(proc)
proc.start()

proc = Process(target=agenoria.plot_medical_charts, args=(config, misc_data, ))
procs.append(proc)
proc.start()

proc = Process(target=agenoria.plot_sleep_24h_viz, args=(config, sleep_data, ))
procs.append(proc)
proc.start()

proc = Process(target=agenoria.plot_feeding_24h_viz, args=(
    config, feeding_bottle_data, feeding_solid_data, ))
procs.append(proc)
proc.start()

proc = Process(target=agenoria.plot_diapers_24h_viz,
               args=(config, diaper_data, ))
procs.append(proc)
proc.start()

# Complete the processes
for proc in procs:
    proc.join()

# Stop the clock
stop = timeit.default_timer()

print('Time elapsed: ', stop - start, ' seconds')
