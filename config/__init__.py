# Copyright 2019 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of Agenoria and is released under the MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import sys
import warnings
from pathlib import Path

import pandas as pd

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    import tomli as tomllib

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = ROOT_DIR / "config/config_zyw.toml"


def _resolve_config_path() -> Path:
    if "pytest" in sys.argv[0]:
        return DEFAULT_CONFIG_PATH

    # Parse command line argument for TOML configuration file.
    # Pytest and other runners pass flags as argv[1], so only treat argv[1]
    # as config when it is a TOML path.
    if len(sys.argv) > 1:
        candidate = Path(sys.argv[1])
        if candidate.suffix == ".toml":
            return candidate if candidate.is_absolute() else ROOT_DIR / candidate

    warnings.warn(
        "No configuration file supplied. Using config_zyw.toml...",
        stacklevel=2,
    )
    return DEFAULT_CONFIG_PATH


def _resolve_data_path(configured_path: str) -> Path:
    path = Path(configured_path)
    return path if path.is_absolute() else ROOT_DIR / path


def _read_input_csv(config_key: str, **kwargs: object) -> pd.DataFrame:
    return pd.read_csv(_resolve_data_path(param["input_data"][config_key]), **kwargs)


path = _resolve_config_path()

# Import configuration
with path.open(mode="rb") as fp:
    param = tomllib.load(fp)

# Import diaper data
diaper_data = _read_input_csv("data_diaper")
diaper_data["Diaper time"] = pd.to_datetime(
    diaper_data["Diaper time"],
    format="%m/%d/%Y %I:%M:%S %p",
)

# Sort by date and time
diaper_data = diaper_data.sort_values(by=["Diaper time"], ascending=False)
# Make a new column with date component only
diaper_data["Date"] = diaper_data["Diaper time"].dt.normalize()

# Import sleep data
sleep_data = _read_input_csv("data_sleep")
sleep_data["Begin time"] = pd.to_datetime(
    sleep_data["Begin time"],
    format="%m/%d/%Y %I:%M:%S %p",
)
sleep_data["End time"] = pd.to_datetime(
    sleep_data["End time"],
    format="%m/%d/%Y %I:%M:%S %p",
)

# Make a new column with date component only
sleep_data["Date"] = sleep_data["Begin time"].dt.normalize()

# Import bottle data
feeding_bottle_data = _read_input_csv("data_feed_bottle")
feeding_bottle_data["Time of feeding"] = pd.to_datetime(
    feeding_bottle_data["Time of feeding"],
    format="%m/%d/%Y %I:%M:%S %p",
)

# Make a new column with date component only
feeding_bottle_data["Date"] = feeding_bottle_data["Time of feeding"].dt.normalize()

# Import solid data
feeding_solid_data = _read_input_csv("data_feed_solid")
feeding_solid_data["Time of feeding"] = pd.to_datetime(
    feeding_solid_data["Time of feeding"],
    format="%m/%d/%Y %I:%M:%S %p",
)

# Make a new column with date component only
feeding_solid_data["Date"] = feeding_solid_data["Time of feeding"].dt.normalize()

# Import growth data
growth_data = _read_input_csv("data_growth")
growth_data["Date"] = pd.to_datetime(growth_data["Date"], format="%Y/%m/%d")

hatch_data = _read_input_csv("data_weight")

# Import misc data
misc_data = _read_input_csv("data_misc", parse_dates=["Date"])
misc_data["Date"] = pd.to_datetime(misc_data["Date"], format="%m/%d/%Y")
misc_data = misc_data.fillna(0).set_index(misc_data["Date"])
