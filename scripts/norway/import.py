"""
Import weather stations from met.no Frost
"""

import os
import json
from string import capwords
from meteostat import Stations
from stations import find_duplicate, generate_uid, create, update, get_distance


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
    if (
        station["@type"] == "SensorSystem"
        and "masl" in station
        and "geometry" in station
        and station["countryCode"] == "NO"
    ):
        data = {
            "name": {
                "en": capwords(station["shortName"])
                if "shortName" in station
                else capwords(station["name"])
            },
            "country": station["countryCode"],
            "identifiers": {"national": station["id"]},
            "location": {
                "latitude": round(station["geometry"]["coordinates"][1], 3),
                "longitude": round(station["geometry"]["coordinates"][0], 3),
                "elevation": station["masl"],
            },
        }

        # Add WMO identifier
        if "wmoId" in station:
            data["identifiers"]["wmo"] = (
                f"0{str(station['wmoId'])}"
                if len(str(station["wmoId"])) == 4
                else str(station["wmoId"])
            )

        # Get potential duplicate
        duplicate = find_duplicate(data, stations)

        # Update or create
        if (
            duplicate
            and get_distance(
                station["geometry"]["coordinates"][1],
                station["geometry"]["coordinates"][0],
                duplicate["latitude"],
                duplicate["longitude"],
            )
            <= 1000
            and abs(station["masl"] - duplicate["elevation"]) <= 25
        ):
            update(
                {
                    "id": duplicate["id"],
                    "identifiers": {"national": data["identifiers"]["national"]},
                }
            )
        elif duplicate is None:
            data["id"] = generate_uid()
            create(data)
