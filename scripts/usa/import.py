"""
Import national weather stations from NOAA (weather.gov)
"""

from urllib.request import urlopen
import json
from string import capwords
import pandas as pd
from meteostat import Stations
from stations import find_duplicate, generate_uid, create, update, get_distance

FILE_URL = "https://w1.weather.gov/xml/current_obs/index.xml"

inventory = pd.read_xml(FILE_URL, xpath="station")

# Create Stations instance
stations = Stations()

# US States
US_STATES = [
    "AK",
    "AL",
    "AR",
    "AZ",
    "CA",
    "CO",
    "CT",
    "DC",
    "DE",
    "FL",
    "GA",
    "HI",
    "IA",
    "ID",
    "IL",
    "IN",
    "KS",
    "KY",
    "LA",
    "MA",
    "MD",
    "ME",
    "MI",
    "MN",
    "MO",
    "MS",
    "MT",
    "NC",
    "ND",
    "NE",
    "NH",
    "NJ",
    "NM",
    "NV",
    "NY",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VA",
    "VT",
    "WA",
    "WI",
    "WV",
    "WY",
]

# Process all stations
for index, row in inventory.iterrows():

    if row["state"] in US_STATES:

        try:

            # Get elevation
            lat = float(row["latitude"])
            lon = float(row["longitude"])
            with urlopen(
                f"https://api.weather.gov/stations/{row['station_id']}/observations/latest"
            ) as conn:
                details = json.loads(
                    conn.read().decode("utf-8")
                )
            elevation = details["properties"]["elevation"]["value"]

            # Collect meta data
            data = {
                "name": {"en": capwords(row["station_name"])},
                "country": "US",
                "region": row["state"],
                "identifiers": {
                    "icao": str(row["station_id"])
                    if len(str(row["station_id"])) == 4
                    else None,
                },
                "location": {
                    "latitude": lat,
                    "longitude": lon,
                    "elevation": None if elevation is None else int(elevation),
                },
            }

            # Get potential duplicate
            duplicate = find_duplicate(data, stations)

            # Peform basic quality check
            if (
                duplicate
                and get_distance(
                    lat, lon, duplicate["latitude"], duplicate["longitude"]
                )
                <= 1000
                and abs(elevation - duplicate["elevation"]) <= 25
            ):
                if data["identifiers"]["icao"]:
                    update(
                        {
                            "id": duplicate["id"],
                            "identifiers": {"icao": data["identifiers"]["icao"]},
                        }
                    )

            elif duplicate is None:
                data["id"] = generate_uid()
                create(data)

        except BaseException:

            pass
