"""
Perform basic QA check
"""

import os
import stations


def qa_check(data: dict, file_path: str) -> dict:
    """
    Find invalid data & fix or delete
    """

    # Get ID from file name
    STATION_ID = file_path[-10:-5]
    # Make sure IDs are aligned
    if data and (
        data['id'] != STATION_ID
    ):
        data['id'] = STATION_ID
        return data

    if data and (
        len(data["id"]) != 5
        or data["location"]["latitude"] < -90
        or data["location"]["longitude"] < -180
        or data["location"]["latitude"] > 90
        or data["location"]["longitude"] > 180
    ):

        stations.delete(data["id"])


stations.apply(qa_check)
