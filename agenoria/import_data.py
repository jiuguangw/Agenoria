#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import pandas as pd
import warnings
from data_cache import pandas_cache


@pandas_cache
def import_data(config):
    # Suppress HDF warnings
    warnings.simplefilter(
        action='ignore', category=pd.errors.PerformanceWarning)

    # Import diaper data
    diaper_data = pd.read_csv(
        config['data_diaper'], parse_dates=['Diaper time'])
    # Sort by date and time
    diaper_data = diaper_data.sort_values(by=['Diaper time'], ascending=False)
    # Make a new column with date component only
    diaper_data['Date'] = diaper_data['Diaper time'].dt.normalize()

    # Import sleep data
    sleep_data = pd.read_csv(config['data_sleep'], parse_dates=[
                             'Begin time', 'End time'])
    # Make a new column with date component only
    sleep_data['Date'] = sleep_data['Begin time'].dt.normalize()

    # Import bottle data
    feeding_bottle_data = pd.read_csv(
        config['data_feed_bottle'], parse_dates=['Time of feeding'])
    # Make a new column with date component only
    feeding_bottle_data['Date'] = feeding_bottle_data['Time of feeding'].dt.normalize()

    # Import solid data
    feeding_solid_data = pd.read_csv(
        config['data_feed_solid'], parse_dates=['Time of feeding'])
    # Make a new column with date component only
    feeding_solid_data['Date'] = feeding_solid_data['Time of feeding'].dt.normalize()

    # Import misc data
    misc_data = pd.read_csv(config['data_misc'], parse_dates=['Date'])
    misc_data.fillna(0, inplace=True)
    misc_data = misc_data.set_index(misc_data['Date'])

    return diaper_data, sleep_data, feeding_bottle_data, feeding_solid_data, misc_data
