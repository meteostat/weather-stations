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

# Path of the CSV file
CSV_FILE = (
    os.path.expanduser("~")
    + os.sep
    + "Meteostat"
    + os.sep
    + "weather-stations"
    + os.sep
    + "scripts"
    + os.sep
    + "canada"
    + os.sep
    + "stations.csv"
)

CSV_FILE = "C:\\Users\\SIDDHARTH-PC\\Desktop\\tmp\\weather-stations\\scripts\\germany\\stations_not_in_mstat.json"
# Create Stations instance
stations = Stations()

# inventory = pd.read_csv(CSV_FILE, header=0 , encoding='utf-8', dtype={'Stations_id':'object'})
inventory = pd.read_json(CSV_FILE, dtype={'Stations_id':'object'})
nu =0
upd =0
dupes = []
for index, row in inventory.iterrows():
    try:
        data = {
            "name": {
                "en": capwords(row["Stationsname"])
            },
            "country": "DE",
            "identifiers": {"national": row["Stations_id"]},
            "location": {
                "latitude": row["geoBreite"],
                "longitude": row["geoLaenge"],
                "elevation": row["Stationshoehe"],
            },
        }

        # # Add WMO identifier
        # if "wmoId" in row:
        #     data["identifiers"]["wmo"] = (
        #         f"0{str(row['wmoId'])}"
        #         if len(str(row["wmoId"])) == 4
        #         else str(row["wmoId"])
        #     )

        # Get potential duplicate
        duplicate = find_duplicate(data, stations)
        # Update or create
        if duplicate:
            print(duplicate)
            dupes.append({
                'new_entry': json.dumps(data),
                'dupe': {'id': duplicate['id'], 'name': duplicate['name'], 'lat': duplicate['latitude'], 'long': duplicate['longitude']}
            })
            update(
                {
                    "id": duplicate["id"],
                    "identifiers": {"national": data["identifiers"]["national"]},
                }
            )
            upd += 1 
        else:
            data["id"] = generate_uid()
            create(data)
            nu += 1

    except BaseException as e:
        print(traceback.format_exc())
        print(e)
        break
print(f"Created {nu} new stations")
print(f"Updated {upd} existing stations")
print(len(dupes))
# print(dupes)
with open('duplicate_stations.json', "w+") as dupe_file:
    json.dump(dupes, dupe_file)