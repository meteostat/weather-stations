"""
Set active flag
"""

import requests
import stations


def check_status(url):
    """
    Check if HTTP status code equals 404
    """
    try:
        response = requests.head(url)
        return response.status_code == 404
    except requests.RequestException:
        return False


def set_active(data: dict, _) -> dict:
    """
    Update active flag
    """
    if data:

        urls = [
            f'https://bulk.meteostat.net/v2/hourly/{data["id"]}.csv.gz',
            f'https://bulk.meteostat.net/v2/daily/{data["id"]}.csv.gz',
        ]

        not_found = list(map(check_status, urls))

        items = list(data.items())
        items.insert(1, ("active", False if all(not_found) else True))

        return dict(items)


stations.apply(set_active, threads=1)
