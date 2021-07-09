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
        data['timezone'] is None
    ):

        stations.delete(data['id'])

stations.apply(qa_check)
