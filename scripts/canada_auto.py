"""
Rename weather stations and restore
"""

import os
import json
import urllib.request
from stations import stations_path, generate_uid, create

stations = json.loads('["stations/71033.json","stations/71036.json",\
    "stations/71038.json","stations/71048.json","stations/71051.json",\
    "stations/71056.json","stations/71060.json","stations/71062.json",\
    "stations/71072.json","stations/71073.json","stations/71085.json",\
    "stations/71098.json","stations/71102.json","stations/71105.json",\
    "stations/71106.json","stations/71110.json","stations/71111.json",\
    "stations/71112.json","stations/71127.json","stations/71134.json",\
    "stations/71136.json","stations/71141.json","stations/71142.json",\
    "stations/71151.json","stations/71161.json","stations/71167.json",\
    "stations/71174.json","stations/71175.json","stations/71180.json",\
    "stations/71183.json","stations/71187.json","stations/71193.json",\
    "stations/71196.json","stations/71202.json","stations/71208.json",\
    "stations/71239.json","stations/71247.json","stations/71250.json",\
    "stations/71265.json","stations/71268.json","stations/71271.json",\
    "stations/71272.json","stations/71273.json","stations/71283.json",\
    "stations/71290.json","stations/71292.json","stations/71293.json",\
    "stations/71304.json","stations/71366.json","stations/71369.json",\
    "stations/71398.json","stations/71399.json","stations/71410.json",\
    "stations/71414.json","stations/71436.json","stations/71440.json",\
    "stations/71461.json","stations/71481.json","stations/71483.json",\
    "stations/71488.json","stations/71496.json","stations/71499.json",\
    "stations/71507.json","stations/71513.json","stations/71527.json",\
    "stations/71559.json","stations/71582.json","stations/71584.json",\
    "stations/71587.json","stations/71594.json","stations/71596.json",\
    "stations/71605.json","stations/71608.json","stations/71613.json",\
    "stations/71618.json","stations/71629.json","stations/71632.json",\
    "stations/71634.json","stations/71637.json","stations/71655.json",\
    "stations/71660.json","stations/71675.json","stations/71685.json",\
    "stations/71686.json","stations/71689.json","stations/71691.json",\
    "stations/71697.json","stations/71720.json","stations/71733.json",\
    "stations/71736.json","stations/71748.json","stations/71812.json",\
    "stations/71820.json","stations/71855.json","stations/71856.json",\
    "stations/71857.json","stations/71859.json","stations/71872.json",\
    "stations/71874.json","stations/71884.json","stations/71886.json",\
    "stations/71888.json","stations/71890.json","stations/71895.json",\
    "stations/71903.json","stations/71904.json","stations/71905.json",\
    "stations/71920.json","stations/71931.json","stations/71932.json",\
    "stations/71933.json","stations/71947.json","stations/71954.json",\
    "stations/71956.json","stations/71967.json","stations/71970.json",\
    "stations/71976.json","stations/71981.json","stations/71982.json",\
    "stations/71986.json"]')

for station in stations:

    # Get ID from path
    ms_id = station[9:14]

    # Rename station
    new_id = generate_uid()
    from_path = stations_path + os.sep + ms_id + '.json'
    to_path = stations_path + os.sep + new_id + '.json'
    os.rename(from_path, to_path)
    with open(to_path, 'r') as f:
        state = json.load(f)
    state['id'] = new_id
    state['identifiers']['icao'] = None
    with open(to_path, 'w') as f:
        f.write(json.dumps(state, indent=4, default=str, ensure_ascii=False))
        f.close()

    # Re-create old station
    url = f'https://raw.githubusercontent.com/meteostat/weather-stations/master/stations/{ms_id}.json'
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    data['identifiers']['wmo'] = None
    create(data)
