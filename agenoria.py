#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the  MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import agenoria
import os

# Create the output directory
if not os.path.exists('build'):
    os.makedirs('build')

# Config file
config_file = 'config.json'

# Plot daily charts
agenoria.plot_daily_charts(config_file)

# Plot 24h viz
agenoria.plot_24h_viz(config_file)

# Plot growth charts
agenoria.plot_growth_charts(config_file)

# Plot medical charts
agenoria.plot_medical_charts(config_file)
