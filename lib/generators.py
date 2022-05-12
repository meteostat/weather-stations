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

        id = x = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(5)
        )

        if private:
            id = "$" + id[1:]

        url = f"https://github.com/meteostat/weather-df/blob/master/df/{id}.json"

        try:
            response = request.urlopen(url)
        except error.HTTPError:
            return id
