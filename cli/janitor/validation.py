"""Station validation using JSON schema."""

import json
from pathlib import Path

import jsonschema

from janitor.utils import get_station_id_from_path, read_station


def get_schema() -> dict:
    """Load the station JSON schema."""
    schema_path = Path(__file__).parent.parent / "station_schema.json"
    with open(schema_path, encoding="utf-8") as f:
        return json.load(f)


def validate_station(file_path: Path) -> tuple[bool, list[str]]:
    """
    Validate a station file against the JSON schema.

    Args:
        file_path: Path to the station JSON file

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    try:
        data = read_station(file_path)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]
    except Exception as e:
        return False, [f"Error reading file: {e}"]

    # Validate JSON schema
    schema = get_schema()
    validator = jsonschema.Draft7Validator(schema)

    schema_errors = list(validator.iter_errors(data))
    if schema_errors:
        for error in schema_errors:
            if error.path:
                path = ".".join(str(p) for p in error.path)
                errors.append(f"{path}: {error.message}")
            else:
                errors.append(error.message)

    # Additional validation: ID must match filename
    expected_id = get_station_id_from_path(file_path)
    if data.get("id") != expected_id:
        errors.append(
            f"ID mismatch: file name is {expected_id} but ID in file is {data.get('id')}"
        )

    return len(errors) == 0, errors
