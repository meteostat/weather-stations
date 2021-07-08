from string import capwords
import pandas as pd
from stations import find_duplicate, generate_uid, create, update


# Min. last year to prevent inactive stations from being imported
MIN_LAST_YEAR = 2010

def province_code(name: str) -> str:
    """
    Convert province name to code
    """

    if name == 'ALBERTA':
        return 'AB'
    elif name == 'BRITISH COLUMBIA':
        return 'BC'
    elif name == 'MANITOBA':
        return 'MB'
    elif name == 'NEW BRUNSWICK':
        return 'NB'
    elif name == 'NEWFOUNDLAND':
        return 'NL'
    elif name == 'NOVA SCOTIA':
        return 'NS'
    elif name == 'ONTARIO':
        return 'ON'
    elif name == 'PRINCE EDWARD ISLAND':
        return 'PE'
    elif name == 'QUEBEC':
        return 'QC'
    elif name == 'SASKATCHEWAN':
        return 'SK'
    else:
        return None

# Read Canadian station inventory
# (should be updated before importing)
# https://drive.google.com/drive/folders/1WJCDEU34c60IfOnG4rv5EPZ4IhhW9vZH
inventory = pd.read_csv(
    './stations.csv',
    usecols=[0, 1, 3, 4, 6, 7, 10, 12],
    header=0,
    names=['name', 'province', 'id', 'wmo', 'latitude', 'longitude', 'elevation', 'last_year'],
    dtype={
        'wmo': 'string'
    })

# Process all stations
for index, row in inventory.iterrows():

    if not pd.isna(row['last_year']) and int(row['last_year']) >= MIN_LAST_YEAR:

        # Collect meta data
        data = {
            'name': {
                'en': capwords(row['name'])
            },
            'country': 'CA',
            'region': province_code(str(row['province'])),
            'identifiers': {
                'national': str(row['id']),
                'wmo': None if pd.isna(row['wmo']) else str(row['wmo'])
            },
            'location': {
                'latitude': float(row['latitude']),
                'longitude': float(row['longitude']),
                'elevation': None if pd.isna(row['elevation']) else int(round(row['elevation']))
            }
        }

        # Get potential duplicate station
        duplicate = find_duplicate(data)

        # Check if duplicate found
        if isinstance(duplicate, dict):
            if 'distance' in duplicate and duplicate['distance'] > 50:
                continue
            data['id'] = duplicate['id']
            update(data)
        else:
            data['id'] = generate_uid()
            create(data)
