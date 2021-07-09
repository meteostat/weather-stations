"""
Perform basic QA check
"""

from meteostat import Stations as Inventory
import stations


valid = Inventory().fetch().index

def qa_check(data: dict) -> dict:
    """
    Find invalid data & delete
    """

    if data and (
        len(data['id']) != 5 or
        data['location']['latitude'] < -90 or
        data['location']['longitude'] < -180 or
        data['location']['latitude'] > 90 or
        data['location']['longitude'] > 180 or
        (data['identifiers']['wmo'] is None and data['id'] not in valid)
    ):

        stations.delete(data['id'])

stations.apply(qa_check)
