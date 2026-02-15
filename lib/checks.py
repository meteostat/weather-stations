"""
Generic Helpers

The code is licensed under the MIT license.
"""

import meteostat as ms
from stations import create_station_dict


def find_duplicate(station: dict):
    """
    Check if a (similar) station already exists
    """

    # Merge station data with template
    station = create_station_dict(station)

    # Get all weather stations
    df = ms.stations.query()

    # Get key fields
    wmo = station["identifiers"]["wmo"] if "wmo" in station["identifiers"] else None
    icao = station["identifiers"]["icao"] if "icao" in station["identifiers"] else None
    lat = station["location"]["latitude"]
    lon = station["location"]["longitude"]

    # First, check for Meteostat ID
    if station["id"] and station["id"] in df.index:
        return df.loc[[station["id"]]].reset_index().to_dict("records")[0]

    # Now, check for WMO ID
    if wmo and (df["wmo"] == wmo).any():
        return df[df["wmo"] == wmo].reset_index().to_dict("records")[0]

    # Now, check for ICAO ID
    if icao and (df["icao"] == icao).any():
        return df[df["icao"] == icao].reset_index().to_dict("records")[0]

    # Last, check for proximity
    nearby_df = ms.stations.query(lat=lat, lon=lon, radius=10000)
    if len(nearby_df) > 0:
        result = nearby_df.head(1).reset_index().to_dict("records")[0]
        return (
            result
            if abs(result["elevation"] - station["location"]["elevation"]) <= 50
            else None
        )

    # No duplicates
    return None
