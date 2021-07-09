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

    if data and not data['timezone']:

        url: str = '' # Add URL of API provider

        with urllib.request.urlopen(url) as response:
            tzdata = json.loads(response.read().decode())

        time.sleep(1.1)

        if tzdata['status'] == 'OK':
            data['timezone'] = tzdata['zoneName']

        return data

stations.apply(find_timezone, threads=1)
