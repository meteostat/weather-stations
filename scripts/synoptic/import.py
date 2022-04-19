"""
Import weather stations from Synoptic
"""

import os
import json
from meteostat import Stations
from stations import find_duplicate, generate_uid, create, update, get_distance

# Path of the JSON file
# https://api.synopticdata.com/v2/stations/metadata?obrange=20210101&complete=1&token={TOKEN}
FILE = os.path.expanduser(
    "~") + os.sep + 'Meteostat' + os.sep + 'weather-stations' \
    + os.sep + 'scripts' + os.sep + 'synoptic' + os.sep + 'stations.json'

with open(FILE) as f:
    data = json.loads(f.read())

# Create Stations instance
stations = Stations()

for station in data['STATION']:
    # Get elevation
    lat = float(station['LATITUDE'])
    lon = float(station['LONGITUDE'])
    elevation = None if station['ELEVATION'] is None else int(round(float(station['ELEVATION']) / 3.2808399))

    # Collect meta data
    data = {
        'name': {
            'en': station['NAME']
        },
        'country': station['COUNTRY'],
        'identifiers': {
            'icao': station['STID'] if len(station['STID']) == 4 else None,
            'synoptic': station['STID']
        },
        'location': {
            'latitude': lat,
            'longitude': lon,
            'elevation': elevation
        },
        'timezone': station['TIMEZONE']
    }

    # Get potential duplicate
    duplicate = find_duplicate(data, stations)

    # Peform basic quality check
    if duplicate and get_distance(lat, lon, duplicate['latitude'], duplicate['longitude']) <= 5000 and abs(elevation - duplicate['elevation']) <= 25 and station['TIMEZONE'] == duplicate['timezone']:
        data['id'] = duplicate['id']
        update(data)
    else:
        data['id'] = generate_uid()
        create(data)
    
    # Print STID
    print(station['STID'])