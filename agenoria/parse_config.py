# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import pandas as pd


def get_daytime_index(data: pd.Series) -> pd.DataFrame:
    return (data.dt.hour >= 7) & (data.dt.hour < 20)


def get_nighttime_index(data: pd.Series) -> pd.DataFrame:
    return (data.dt.hour < 7) | (data.dt.hour >= 21)
