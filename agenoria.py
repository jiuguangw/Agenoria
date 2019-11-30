#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the  MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import agenoria

# Plot daily charts

file_bottle = 'data/zw/glow_feed_bottle.csv'
file_solid = 'data/zw/glow_feed_solid.csv'
file_diaper = 'data/zw/glow_diaper.csv'
file_sleep = 'data/zw/glow_sleep.csv'

output_daily_charts = 'build/Agenoria_Daily_Charts.pdf'

agenoria.plot_daily_charts(file_bottle, file_solid, file_diaper,
                           file_sleep, output_daily_charts)

# Plot 24h viz

file_sleep = 'data/zw/glow_sleep.csv'
file_feeding = 'data/zw/glow_feed_bottle.csv'
file_diaper = 'data/zw/glow_diaper.csv'

output_sleep_viz = 'build/Agenoria_Sleep_Viz.pdf'
output_feeding_viz = 'build/Agenoria_Feeding_Viz.pdf'
output_diaper_viz = 'build/Agenoria_Diaper_Viz.pdf'

agenoria.plot_24h_viz(file_sleep, file_feeding, file_diaper,
                      output_sleep_viz, output_feeding_viz, output_diaper_viz)

# Plot growth charts

file_hatch = 'data/zw/hatch.csv'
file_glow = 'data/zw/glow_growth.csv'
file_output = 'build/Agenoria_Growth_Charts.pdf'

file_wtageinf = 'data/cdc_growth_curves/wtageinf.csv'
file_lenageinf = 'data/cdc_growth_curves/lenageinf.csv'
file_hcageinf = 'data/cdc_growth_curves/hcageinf.csv'
file_wtleninf = 'data/cdc_growth_curves/wtleninf.csv'

agenoria.plot_growth_charts(file_hatch, file_glow, file_output,
                            file_wtageinf, file_lenageinf, file_hcageinf, file_wtleninf)
