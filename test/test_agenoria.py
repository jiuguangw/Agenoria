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
    # Config file
    config_file = 'config.json'
    config = agenoria.parse_json_config(config_file)

    # Plot
    agenoria.plot_daily_charts(config_file)

    # Get the file size of the output PDF
    file_size = os.path.getsize(config['output_daily_charts'])

    # Check the size is greater than 40 KB
    assert file_size > 40 * 1024, "Test failed - daily charts"


def test_24h_viz():
    # Config file
    config_file = 'config.json'
    config = agenoria.parse_json_config(config_file)

    # Plot
    agenoria.plot_24h_viz(config_file)

    # Get the file size of the output PDF
    file_size_sleep = os.path.getsize(config['output_sleep_viz'])
    file_size_feeding = os.path.getsize(config['output_feeding_viz'])
    file_size_diaper = os.path.getsize(config['output_diaper_viz'])

    # Check the size is greater than 40 KB
    assert file_size_sleep > 100 * 1024, "Test failed - sleep viz"
    assert file_size_feeding > 300 * 1024, "Test failed - feeding viz"
    assert file_size_diaper > 300 * 1024, "Test failed - diaper viz"


def test_growth_charts():
    # Config file
    config_file = 'config.json'
    config = agenoria.parse_json_config(config_file)

    # Plot
    agenoria.plot_growth_charts(config_file)

    # Get the file size of the output PDF
    file_size = os.path.getsize(config['output_growth'])

    # Check the size is greater than 40 KB
    assert file_size > 30 * 1024, "Test failed - growth charts"
