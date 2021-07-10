"""
Add missing time zones
"""

import time
import urllib.request
import json
import stations

# API key
API_KEY = ''

def find_timezone(data: dict) -> dict:
    """
    Find time zone for weather station
    """

    if data and data['country'] == 'CA':

        url: str = f'http://api.timezonedb.com/v2.1/get-time-zone?key={API_KEY}\
        format=json&by=position&lat={data["location"]["latitude"]}&\
        lng={data["location"]["longitude"]}'

        with urllib.request.urlopen(url) as response:
            tzdata = json.loads(response.read().decode())

        time.sleep(1.1)

        if tzdata['status'] == 'OK':
            data['timezone'] = tzdata['zoneName']
            return data

stations.apply(find_timezone, threads=1)
