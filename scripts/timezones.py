"""
Add missing time zones
"""

import time
import urllib.request
import json
import stations

# Number of threads
stations.threads = 1

# API key
API_KEY = ''

def find_timezone(data: dict) -> dict:

    if data and not data['timezone']:

        url: str = f''

        with urllib.request.urlopen(url) as response:
            tzdata = json.loads(response.read().decode())

        time.sleep(1)

        if tzdata['status'] == 'OK':
            data['timezone'] = tzdata['zoneName']

        return data

stations.apply(find_timezone)
