"""
Utility

Update Weather Stations

The code is licensed under the MIT license.
"""

import os
import json
from multiprocessing.pool import ThreadPool

"""
Configuration
"""
# Path of the weather stations directory
STATIONS_PATH: str = f'{os.path.expanduser("~")}{os.sep}Meteostat{os.sep}weather-stations{os.sep}stations'
# Number of threads for multi-thread processing
THREADS: int = 12

def update(file: str) -> None:
    """
    Function applied to each weather station for update
    """

    # Read file and parse JSON
    with open(file, 'r') as f:
        data: dict = json.load(f)

    # Apply your logic

    # Persist changes
    with open(file, 'w') as f:
        f.write(json.dumps(data, indent=4, default=str, ensure_ascii=False))
        f.close()


"""
Read weather station files
"""
# List of files
files = []

# Go through all files
for dirpath, dirnames, filenames in os.walk(STATIONS_PATH):
    for filename in [f for f in filenames if f.endswith('.json')]:
        # Write station data
        files.append(os.path.join(dirpath, filename))

"""
Create thread pool
"""
with ThreadPool(THREADS) as pool:
    # Process datasets in pool
    pool.map(update, files)
    # Wait for Pool to finish
    pool.close()
    pool.join()
