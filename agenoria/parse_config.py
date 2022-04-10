#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import json
import datetime as dt


def parse_json_config(file_name):
    with open(file_name) as json_file:
        config = json.load(json_file)
        config['birthday'] = dt.datetime.strptime(
            config['birthday'], '%m-%d-%Y')
    return config


def get_daytime_index(data):
    return (data.dt.hour > 7) & (data.dt.hour < 19)
