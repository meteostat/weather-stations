"""
Update all weather stations

The code is licensed under the MIT license.
"""

import os
import json
from multiprocessing.pool import ThreadPool
from stations import stations_path, merge_dicts, station_template


def create(data: dict) -> None:
    """
    Write a new weather station into a JSON file
    """

    # Get file path
    file = stations_path + os.sep + data['id'] + '.json'

    # Merge with template
    data = merge_dicts(data, station_template)

    # Write into file
    with open(file, 'w') as f:
        f.write(json.dumps(data, indent=4, default=str, ensure_ascii=False))
        f.close()

def update(data: dict) -> None:
    """
    Update an existing weather station
    """

    # Get file path
    file = stations_path + os.sep + data['id'] + '.json'

    # Read file and parse JSON
    with open(file, 'r') as f:
        state: dict = json.load(f)

    # Deep merge
    data = merge_dicts(data, state)

    # Write into file
    with open(file, 'w') as f:
        f.write(json.dumps(data, indent=4, default=str, ensure_ascii=False))
        f.close()

def delete(station: str) -> None:
    """
    Delete a weather station
    """

    file = stations_path + os.sep + station + '.json'
    os.remove(file)

def apply(function, threads=12) -> None:
    """
    Apply function to all weather stations
    """

    def _update(file: str) -> None:
        # Read file and parse JSON
        with open(file, 'r') as f:
            data: dict = json.load(f)

        # Apply your logic
        data = function(data)

        # Persist changes
        if data:
            with open(file, 'w') as f:
                f.write(json.dumps(data, indent=4, default=str, ensure_ascii=False))
                f.close()

    # List of files
    files = []

    # Go through all files
    for dirpath, dirnames, filenames in os.walk(stations_path):
        for filename in [f for f in filenames if f.endswith('.json')]:
            # Write station data
            files.append(os.path.join(dirpath, filename))

    # Multi-thread processing
    if threads > 1:
        with ThreadPool(threads) as pool:
            # Process datasets in pool
            pool.map(_update, files)
            # Wait for Pool to finish
            pool.close()
            pool.join()
    else:
        for file in files:
            _update(file)
