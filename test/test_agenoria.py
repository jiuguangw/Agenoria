#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the  MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import agenoria
import os


def test_daily_charts():
    # Plot daily charts

    file_bottle = 'data/zw/glow_feed_bottle.csv'
    file_solid = 'data/zw/glow_feed_solid.csv'
    file_diaper = 'data/zw/glow_diaper.csv'
    file_sleep = 'data/zw/glow_sleep.csv'

    output_daily_charts = 'Agenoria_Daily_Charts.pdf'

    agenoria.plot_daily_charts(file_bottle, file_solid, file_diaper,
                               file_sleep, output_daily_charts)

    # Get the file size of the output PDF
    file_size = os.path.getsize(output_daily_charts)

    # Check the size is greater than 40 KB
    assert file_size > 40 * 1024, "Test failed - daily charts"


def test_24h_viz():
    # Plot 24h viz

    file_sleep = 'data/zw/glow_sleep.csv'
    file_feeding = 'data/zw/glow_feed_bottle.csv'
    file_diaper = 'data/zw/glow_diaper.csv'

    output_sleep_viz = 'Agenoria_Sleep_Viz.pdf'
    output_feeding_viz = 'Agenoria_Feeding_Viz.pdf'
    output_diaper_viz = 'Agenoria_Diaper_Viz.pdf'

    agenoria.plot_24h_viz(file_sleep, file_feeding, file_diaper,
                          output_sleep_viz, output_feeding_viz, output_diaper_viz)

    # Get the file size of the output PDF
    file_size_sleep = os.path.getsize(output_sleep_viz)
    file_size_feeding = os.path.getsize(output_feeding_viz)
    file_size_diaper = os.path.getsize(output_diaper_viz)

    # Check the size is greater than 40 KB
    assert file_size_sleep > 100 * 1024, "Test failed - sleep viz"
    assert file_size_feeding > 300 * 1024, "Test failed - feeding viz"
    assert file_size_diaper > 300 * 1024, "Test failed - diaper viz"


def test_growth_charts():
    # Plot growth charts

    sex = 1    # 1 for Boy, 2 for Girl
    birthday = (2018, 11, 21)  # Birthday Year/Month/Date

    file_hatch = 'data/zw/hatch.csv'
    file_glow = 'data/zw/glow_growth.csv'

    file_wtageinf = 'data/cdc_growth_curves/wtageinf.csv'
    file_lenageinf = 'data/cdc_growth_curves/lenageinf.csv'
    file_hcageinf = 'data/cdc_growth_curves/hcageinf.csv'
    file_wtleninf = 'data/cdc_growth_curves/wtleninf.csv'

    file_output = 'Agenoria_Growth_Charts.pdf'

    agenoria.plot_growth_charts(file_hatch, file_glow, file_output, sex, birthday,
                                file_wtageinf, file_lenageinf, file_hcageinf, file_wtleninf)

    # Get the file size of the output PDF
    file_size = os.path.getsize(file_output)

    # Check the size is greater than 40 KB
    assert file_size > 30 * 1024, "Test failed - growth charts"
