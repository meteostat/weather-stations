"""
Generic Helpers

The code is licensed under the MIT license.
"""

from meteostat import Stations
from stations import merge_dicts, station_template

def find_duplicate(station: dict):
    """
    Check if a (similar) station already exists
    """

    # Merge station data with template
    station = merge_dicts(station, station_template)

    # Get all weather df
    stations = Stations()
    df = stations.fetch()

    # Get key fields
    wmo = station['identifiers']['wmo']
    icao = station['identifiers']['icao']
    lat = station['location']['latitude']
    lon = station['location']['longitude']

    # First, check for Meteostat ID
    if station['id'] in df.index:
        return df.loc[[station['id']]].reset_index().to_dict('records')[0]

    # Now, check for WMO ID
    if wmo and (df['wmo'] == wmo).any():
        return df[df['wmo'] == wmo].reset_index().to_dict('records')[0]

    # Now, check for ICAO ID
    if icao and (df['icao'] == icao).any():
        return df[df['icao'] == icao].reset_index().to_dict('records')[0]

    # Last, check for proximity
    stations = stations.nearby(lat, lon, 500)
    if stations.count() > 0:
        return stations.fetch(1).reset_index().to_dict('records')[0]

    # No duplicates
    return None
