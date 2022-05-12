"""
Generate a unique identifier

The code is licensed under the MIT license.
"""

import random
import string
from urllib import request, error


def generate_uid(private: bool = False) -> str:
    """
    Generate a unique station identifier
    """

    while True:

        uid = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(5)
        )

        if private:
            uid = "$" + uid[1:]

        url = f"https://github.com/meteostat/weather-stations/blob/master/stations/{uid}.json"

        try:
            # pylint: disable=consider-using-with
            request.urlopen(url)
        except error.HTTPError:
            return uid
