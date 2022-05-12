"""
█▀▄▀█ █▀▀ ▀█▀ █▀▀ █▀█ █▀ ▀█▀ ▄▀█ ▀█▀
█░▀░█ ██▄ ░█░ ██▄ █▄█ ▄█ ░█░ █▀█ ░█░

The code is licensed under the MIT license.
"""

import os

__appname__ = 'stations'
__version__ = '0.0.2'

# Path of the weather stations directory
stations_path: str = os.path.expanduser(
    "~") + os.sep + 'Meteostat' + os.sep + 'weather-stations' + os.sep + 'stations'

from .utils import create_station_dict, merge_dicts, get_distance
from .generators import generate_uid
from .checks import find_duplicate
from .mutations import create, update, delete, apply
