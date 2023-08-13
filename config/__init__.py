#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import pathlib
import sys
import warnings

import pandas as pd
import tomli

# Parse command line argument for toml configuration file
if len(sys.argv) > 1 and "pytest" in sys.argv[0]:
    path = pathlib.Path(__file__).parents[1] / "config/config_zyw.toml"
elif len(sys.argv) > 1:
    path = pathlib.Path(__file__).parents[1] / sys.argv[1]
else:
    warnings.warn("No configuration file supplied. Using config_zyw.toml...")
    path = pathlib.Path(__file__).parents[1] / "config/config_zyw.toml"

# Import configuration
with path.open(mode="rb") as fp:
    param = tomli.load(fp)

# Import diaper data
diaper_data = pd.read_csv(param["input_data"]["data_diaper"])
diaper_data["Diaper time"] = pd.to_datetime(
    diaper_data["Diaper time"], format="%m/%d/%Y %I:%M:%S %p"
)

# Sort by date and time
diaper_data = diaper_data.sort_values(by=["Diaper time"], ascending=False)
# Make a new column with date component only
diaper_data["Date"] = diaper_data["Diaper time"].dt.normalize()

# Import sleep data
sleep_data = pd.read_csv(param["input_data"]["data_sleep"])
sleep_data["Begin time"] = pd.to_datetime(
    sleep_data["Begin time"], format="%m/%d/%Y %I:%M:%S %p"
)
sleep_data["End time"] = pd.to_datetime(
    sleep_data["End time"], format="%m/%d/%Y %I:%M:%S %p"
)

# Make a new column with date component only
sleep_data["Date"] = sleep_data["Begin time"].dt.normalize()

# Import bottle data
feeding_bottle_data = pd.read_csv(param["input_data"]["data_feed_bottle"])
feeding_bottle_data["Time of feeding"] = pd.to_datetime(
    feeding_bottle_data["Time of feeding"], format="%m/%d/%Y %I:%M:%S %p"
)

# Make a new column with date component only
feeding_bottle_data["Date"] = feeding_bottle_data[
    "Time of feeding"
].dt.normalize()

# Import solid data
feeding_solid_data = pd.read_csv(param["input_data"]["data_feed_solid"])
feeding_solid_data["Time of feeding"] = pd.to_datetime(
    feeding_solid_data["Time of feeding"], format="%m/%d/%Y %I:%M:%S %p"
)

# Make a new column with date component only
feeding_solid_data["Date"] = feeding_solid_data[
    "Time of feeding"
].dt.normalize()

# Import growth data
growth_data = pd.read_csv(param["input_data"]["data_growth"])
growth_data["Date"] = pd.to_datetime(growth_data["Date"], format="%Y/%m/%d")

hatch_data = pd.read_csv(param["input_data"]["data_weight"])

# Import misc data
misc_data = pd.read_csv(param["input_data"]["data_misc"], parse_dates=["Date"])
misc_data["Date"] = pd.to_datetime(misc_data["Date"], format="%m/%d/%Y")

misc_data.fillna(0, inplace=True)
misc_data = misc_data.set_index(misc_data["Date"])
