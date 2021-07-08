"""
█▀▄▀█ █▀▀ ▀█▀ █▀▀ █▀█ █▀ ▀█▀ ▄▀█ ▀█▀
█░▀░█ ██▄ ░█░ ██▄ █▄█ ▄█ ░█░ █▀█ ░█░

The code is licensed under the MIT license.
"""

import os

__appname__ = 'stations'
__version__ = '0.0.1'

# Path of the weather stations directory
stations_path: str = os.path.expanduser(
    "~") + os.sep + 'Meteostat' + os.sep + 'weather-stations' + os.sep + 'stations'

# Number of threads for multi-thread processing
threads: int = 12

from .utils import merge_dicts
from .templates import station_template
from .generators import generate_uid
from .checks import find_duplicate
from .mutations import create, update, apply
