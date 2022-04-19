"""
Useful utilities

The code is licensed under the MIT license.
"""

import numpy as np


def merge_dicts(source, destination):
    """
    Deep merge two dicts
    """

    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            merge_dicts(value, node)
        else:
            destination[key] = value

    return destination

def get_distance(lat1, lon1, lat2, lon2):
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
    arch = np.sin(dlat / 2)**2 + np.cos(lat1) * \
        np.cos(lat2) * np.sin(dlon / 2)**2
    arch_sin = 2 * np.arcsin(np.sqrt(arch))

    return radius * arch_sin