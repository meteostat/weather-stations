"""
█▀▄▀█ █▀▀ ▀█▀ █▀▀ █▀█ █▀ ▀█▀ ▄▀█ ▀█▀
█░▀░█ ██▄ ░█░ ██▄ █▄█ ▄█ ░█░ █▀█ ░█░

The code is licensed under the MIT license.
"""

import os
from .mutations import create, update, delete, apply
from .checks import find_duplicate
from .generators import generate_uid
from .utils import create_station_dict, merge_dicts, get_distance

__appname__ = "stations"
__version__ = "0.0.4"

# Path of the weather stations directory
stations_path: str = (
    os.path.expanduser("~")
    + os.sep
    + "Meteostat"
    + os.sep
    + "weather-stations"
    + os.sep
    + "stations"
)
