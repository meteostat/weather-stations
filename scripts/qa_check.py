"""
Perform basic QA check
"""

import stations


def qa_check(data: dict) -> dict:
    """
    Find invalid data & delete
    """

    if data and (
        data["country"] == 'AU' and
        data["identifiers"]["national"] is not None
    ):
        data["identifiers"].pop("national")
        stations.update(data)


stations.apply(qa_check)
