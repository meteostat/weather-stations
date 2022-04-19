"""
Generic Helpers

The code is licensed under the MIT license.
"""

from meteostat import Stations
from stations import merge_dicts, station_template

def find_duplicate(station: dict, stations = Stations()):
    """
    Check if a (similar) station already exists
    """

    # Merge station data with template
    station = merge_dicts(station, station_template)

    # Get all weather df
    df = stations.fetch()

    # Get key fields
    wmo = station['identifiers']['wmo'] if 'wmo' in station['identifiers'] else None
    icao = station['identifiers']['icao'] if 'icao' in station['identifiers'] else None
    lat = station['location']['latitude']
    lon = station['location']['longitude']

    # First, check for Meteostat ID
    if station['id'] and station['id'] in df.index:
        return df.loc[[station['id']]].reset_index().to_dict('records')[0]

    # Now, check for WMO ID
    if wmo and (df['wmo'] == wmo).any():
        return df[df['wmo'] == wmo].reset_index().to_dict('records')[0]

    # Now, check for ICAO ID
    if icao and (df['icao'] == icao).any():
        return df[df['icao'] == icao].reset_index().to_dict('records')[0]

    # Last, check for proximity
    stations = stations.nearby(lat, lon, 3000)
    if stations.count() > 0:
        result = stations.fetch(1).reset_index().to_dict('records')[0]
        return result if abs(result['elevation'] - station['location']['elevation']) <= 10 else None

    # No duplicates
    return None
