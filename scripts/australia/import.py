"""
Import weather stations from bom.gov.au
"""

import os
from urllib import request
import json
from meteostat import Stations
from stations import find_duplicate, generate_uid, create, update

# Base path of bom.gov.au JSON files
BASE = "http://www.bom.gov.au/fwo/"

# Path of the JSON file
JSON_FILE = (
    os.path.expanduser("~")
    + os.sep
    + "Meteostat"
    + os.sep
    + "weather-stations"
    + os.sep
    + "scripts"
    + os.sep
    + "australia"
    + os.sep
    + "stations.json"
)

# Request headers for bom.gov.au
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Host": "www.bom.gov.au",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
}

# Create Stations instance
stations = Stations()

# returns JSON object as
# a dictionary
with open(JSON_FILE) as file:
    inventory = json.load(file)

for station in inventory[248:]:
    # Get meta data
    try:
        req = request.Request(
            BASE + station,
            headers=HEADERS,
        )
        # Get JSON data
        with request.urlopen(req) as raw:
            meta = json.loads(raw.read().decode())["observations"]["data"][0]
        # Get elevation
        elevation = json.loads(
            request.urlopen(
                'https://api.open-elevation.com/api/v1/lookup?'
                + f'locations={meta["lat"]},{meta["lon"]}'
            )
            .read()
            .decode("utf-8")
        )["results"][0]["elevation"]
        # Collect meta data
        data = {
            "name": {"en": meta["name"]},
            "country": "AU",
            "identifiers": {
                "wmo": str(meta["wmo"]) if meta["wmo"] else None,
                "national": station[-10:-5],
            },
            "location": {
                "latitude": meta["lat"],
                "longitude": meta["lon"],
                "elevation": None if elevation is None else int(elevation),
            },
        }
        # Get potential duplicate
        duplicate = find_duplicate(data, stations)

        # Update or create
        if duplicate:
            data["id"] = duplicate["id"]
            data["location"].pop("elevation")
            update(data)
        else:
            data["id"] = generate_uid()
            create(data)

    except BaseException:
        pass
