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

# Config file
config_file = 'config.json'


procs = []

proc = Process(target=agenoria.plot_diaper_charts, args=(config_file,))
procs.append(proc)
proc.start()

proc = Process(target=agenoria.plot_sleep_feeding_charts, args=(config_file,))
procs.append(proc)
proc.start()

proc = Process(target=agenoria.plot_growth_charts, args=(config_file,))
procs.append(proc)
proc.start()

proc = Process(target=agenoria.plot_medical_charts, args=(config_file,))
procs.append(proc)
proc.start()

proc = Process(target=agenoria.plot_sleep_24h_viz, args=(config_file,))
procs.append(proc)
proc.start()

proc = Process(target=agenoria.plot_feeding_24h_viz, args=(config_file,))
procs.append(proc)
proc.start()

proc = Process(target=agenoria.plot_diapers_24h_viz, args=(config_file,))
procs.append(proc)
proc.start()

# complete the processes
for proc in procs:
    proc.join()

# Stop the clock
stop = timeit.default_timer()

print('Time elapsed: ', stop - start, ' seconds')
