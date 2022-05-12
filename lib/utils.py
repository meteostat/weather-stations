"""
Useful utilities

The code is licensed under the MIT license.
"""

import numpy as np


def create_station_dict(data: dict) -> dict:
    """
    Deep merge two dicts
    """

    result = {
        "id": data.get("id", None),
        "name": data.get("name", {"en": None}),
        "country": data.get("country", None),
        "region": data.get("region", None),
        "identifiers": data.get("identifiers", {}),
        "location": {
            "latitude": data["location"].get("latitude", None)
            if "location" in data
            else None,
            "longitude": data["location"].get("longitude", None)
            if "location" in data
            else None,
            "elevation": data["location"].get("elevation", None)
            if "location" in data
            else None,
        },
        "timezone": data.get("timezone", None),
    }

    return result


def merge_dicts(source: dict, destination: dict) -> None:
    """
    Deep merge two dicts

    CAUTION: This changes destination, pass a copy
    if you want to re-use the destination dict
    """

    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            merge_dicts(value, node)
        else:
            destination[key] = value


def get_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between weather station and geo point
    """
    # Earth radius in meters
    radius = 6371000

    # Degress to radian
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])

    # Deltas
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Calculate distance
    arch = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    arch_sin = 2 * np.arcsin(np.sqrt(arch))

    return radius * arch_sin
