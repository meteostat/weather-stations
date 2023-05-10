"""
Import weather stations from DWD
"""

import os
import json
import traceback
import pandas as pd
from string import capwords
from meteostat import Stations
from stations import find_duplicate, generate_uid, create, update, get_distance

# Map Bundesland string to ISO code
REGION_CODES = {
    'Baden-Württemberg': 'BW',
    'Bayern': 'BY',
 'Berlin': 'BE',
 'Brandenburg': 'BB',
 'Bremen': 'HB',
 'Hamburg': 'HH',
 'Hessen': 'HE',
 'Mecklenburg-Vorpommern': 'MV',
 'Niedersachsen': 'NI',
 'Nordrhein-Westfalen': 'NW',
 'Rheinland-Pfalz':	'RP',
 'Saarland': 'SL',
 'Sachsen': 'SN',
 'Sachsen-Anhalt': 'ST',
 'Schleswig-Holstein': 'SH',
 'Thüringen': 'TH'
}

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
    + "germany"
    + os.sep
    + "stations_not_in_mstat.json"
)

# Create Stations instance
stations = Stations()

inventory = pd.read_json(JSON_FILE, dtype={'Stations_id':'object'})
new_stations_count =0 # Number of new stations
dupes = [] # List of duplicates
for index, row in inventory.iterrows():
    try:
        data = {
            "name": {
                "en": capwords(row["Stationsname"])
            },
            "country": "DE",
            "region": REGION_CODES[row["Bundesland"]] if row["Bundesland"] in REGION_CODES.keys() else None,
            "identifiers": {"national": row["Stations_id"]},
            "location": {
                "latitude": row["geoBreite"],
                "longitude": row["geoLaenge"],
                "elevation": row["Stationshoehe"],
            },
            "timezone": "Europe/Berlin"
        }

        # Get potential duplicate
        duplicate = find_duplicate(data, stations)
        # Update or create
        if duplicate:
            print(duplicate)
            dupes.append({
                'new_entry': json.dumps(data),
                'dupe': {'id': duplicate['id'], 'name': duplicate['name'], 'lat': duplicate['latitude'], 'long': duplicate['longitude']}
            })
        else:
            data["id"] = generate_uid()
            create(data)
            new_stations_count += 1

    except BaseException as e:
        print(traceback.format_exc())
        print(e)
        break
print(f"Created {new_stations_count} new stations")
print(f"Detected {len(dupes)} potential duplicates")

# Persist duplicates for future reference
with open('duplicate_stations.json', "w+") as dupe_file:
    json.dump(dupes, dupe_file)