"""
Perform basic QA check
"""

import stations


def qa_check(data: dict) -> dict:

    if data and (
        len(data['id']) != 5 or
        data['location']['latitude'] < -90 or
        data['location']['longitude'] < -180 or
        data['location']['latitude'] > 90 or
        data['location']['longitude'] > 180
    ):

        stations.delete(data['id'])

    return None

stations.apply(qa_check)
