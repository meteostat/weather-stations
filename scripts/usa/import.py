"""
Import national weather stations from NOAA (weather.gov)
"""

from urllib.request import urlopen
import json
import pandas as pd
from meteostat import Stations
from stations import find_duplicate, generate_uid, create, update, get_distance

FILE_URL = 'https://w1.weather.gov/xml/current_obs/index.xml'

inventory = pd.read_xml(FILE_URL, xpath="station")

# Create Stations instance
stations = Stations()

# US States
US_STATES = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

# Process all stations
for index, row in inventory.iterrows():

    if row['state'] in US_STATES:

        # Get elevation
        lat = float(row['latitude'])
        lon = float(row['longitude'])
        details = json.loads(urlopen(
            f"https://api.weather.gov/stations/{row['station_id']}/observations/latest"
        ).read().decode("utf-8"))
        elevation = details["properties"]["elevation"]["value"]

        # Collect meta data
        data = {
            'name': {
                'en': row['station_name']
            },
            'country': 'US',
            'region': row['state'],
            'identifiers': {
                'national': str(row['station_id']),
                'icao': str(row['station_id']) if len(str(row['station_id'])) == 4 else None,
            },
            'location': {
                'latitude': lat,
                'longitude': lon,
                'elevation': None if elevation == None else int(elevation)
            }
        }

        # Get potential duplicate
        duplicate = find_duplicate(data, stations)

        # Clean data
        del data['identifiers']['icao']

        # Peform basic quality check
        if duplicate and get_distance(lat, lon, duplicate['latitude'], duplicate['longitude']) <= 5000 and abs(elevation - duplicate['elevation']) <= 25:
            del data['name']['en']
            data['id'] = duplicate['id']
            update(data)
        else:
            data['id'] = generate_uid()
            create(data)
            exit()