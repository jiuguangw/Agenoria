#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the  MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import agenoria
import os


def get_data():
    # Create the output directory
    if not os.path.exists('build'):
        os.makedirs('build')

    # Parse JSON config file
    config_file = 'config_zyw.json'
    config = agenoria.parse_json_config(config_file)

    # Import data
    diaper_data, sleep_data, feeding_bottle_data, feeding_solid_data, misc_data, growth_data, hatch_data = agenoria.import_data(
        config)

    return config, diaper_data, sleep_data, feeding_bottle_data, feeding_solid_data, misc_data, growth_data, hatch_data


def test_diaper_charts():
    # Setup
    config, diaper_data, _, _, _, _, _, _ = get_data()

    # Plot
    agenoria.plot_diaper_charts(config, diaper_data)

    # Get the file size of the output PDF
    file_size = os.path.getsize(config['output_daily_diaper_charts'])

    # Check the size is greater than 40 KB
    assert file_size > 20 * 1024, "Test failed - diaper charts"


def test_sleep_stats_charts():
    # Setup
    config, _, sleep_data, _, _, _, _, _ = get_data()

    # Plot
    agenoria.plot_sleep_stats_charts(config, sleep_data)

    # Get the file size of the output PDF
    file_size = os.path.getsize(config['output_daily_sleep_stats_charts'])

    # Check the size is greater than 40 KB
    assert file_size > 30 * 1024, "Test failed - diaper charts"


def test_feeding_stats_charts():
    # Setup
    config, _, _, feeding_bottle_data, feeding_solid_data, _, _, _ = get_data()

    # Plot
    agenoria.plot_feeding_stats_charts(
        config, feeding_bottle_data, feeding_solid_data)

    # Get the file size of the output PDF
    file_size = os.path.getsize(config['output_daily_feeding_stats_charts'])

    # Check the size is greater than 40 KB
    assert file_size > 40 * 1024, "Test failed - diaper charts"


def test_24h_viz():
    # Setup
    config, diaper_data, sleep_data, feeding_bottle_data, feeding_solid_data, _, _, _ = get_data()

    # Plot
    agenoria.plot_sleep_24h_viz(config, sleep_data)
    agenoria.plot_feeding_24h_viz(
        config, feeding_bottle_data, feeding_solid_data)
    agenoria.plot_diapers_24h_viz(config, diaper_data)

    # Get the file size of the output PDF
    file_size_sleep = os.path.getsize(config['output_sleep_viz'])
    file_size_feeding = os.path.getsize(config['output_feeding_viz'])
    file_size_diaper = os.path.getsize(config['output_diaper_viz'])

    # Check the size is greater than 40 KB
    assert file_size_sleep > 100 * 1024, "Test failed - sleep viz"
    assert file_size_feeding > 25 * 1024, "Test failed - feeding viz"
    assert file_size_diaper > 25 * 1024, "Test failed - diaper viz"


def test_growth_charts():
    # Setup
    config, _, _, _, _, _, growth_data, hatch_data = get_data()

    # Plot
    agenoria.plot_growth_charts(config, growth_data, hatch_data)

    # Get the file size of the output PDF
    file_size = os.path.getsize(config['output_growth'])

    # Check the size is greater than 40 KB
    assert file_size > 30 * 1024, "Test failed - growth charts"


def test_medical_charts():
    # Setup
    config, _, _, _, _, misc_data, _, _ = get_data()

    # Plot
    agenoria.plot_medical_charts(config, misc_data)

    # Get the file size of the output PDF
    file_size = os.path.getsize(config['output_medical_charts'])

    # Check the size is greater than 40 KB
    assert file_size > 10 * 1024, "Test failed - medical charts"
