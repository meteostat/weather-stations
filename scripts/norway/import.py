"""
Import weather stations from met.no Frost
"""

import os
from urllib import request
import json
from string import capwords
from meteostat import Stations
from stations import find_duplicate, generate_uid, create, update


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
    + "norway"
    + os.sep
    + "stations.json"
)

# Create Stations instance
stations = Stations()

# returns JSON object as
# a dictionary
with open(JSON_FILE) as file:
    inventory = json.load(file)

for station in inventory:
    # Check if sensor system
    if station["@type"] == "SensorSystem":
        data = {
            "name": {
                "en": station["shortName"] if "shortName" in station else station["name"]
            },
            "country": station["countryCode"],
            "identifiers": {
                "national": station["id"]
            },
            "location": {
                "latitude": station["geometry"]["coordinates"][0],
                "longitude": station["geometry"]["coordinates"][1],
                "elevation": station['masl']
            }
        }

        # Add IDs
        if "wmoId" in station:
            data['identifiers']['wmo'] = f"0{str(station['wmoId'])}" if len(station["wmoId"]) == 4 else str(station["wmoId"])
        if "icaoCodes" in station:
            data['identifiers']['icao'] = stations["icaoCodes"][0]

        # Get potential duplicate
        duplicate = find_duplicate(data, stations)

        # Update or create
        if duplicate:
            data["id"] = duplicate["id"]
            update(data)
        else:
            data["id"] = generate_uid()
            create(data)
