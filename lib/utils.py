"""
Useful utilities

The code is licensed under the MIT license.
"""

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
