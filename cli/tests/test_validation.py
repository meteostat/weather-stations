"""Tests for validation module."""

import json
import tempfile
from pathlib import Path

from janitor.validation import validate_station


def test_valid_station():
    """Test validation of a valid station file."""
    valid_station = {
        "id": "TEST1",
        "active": True,
        "name": {"en": "Test Station"},
        "country": "US",
        "region": "CA",
        "identifiers": {"wmo": "12345"},
        "location": {"latitude": 37.7749, "longitude": -122.4194, "elevation": 10},
        "timezone": "America/Los_Angeles",
    }

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        # Use TEST1.json as filename
        temp_path = Path(f.name)
        temp_path = temp_path.parent / "TEST1.json"
        json.dump(valid_station, temp_path.open("w"))

    try:
        is_valid, errors = validate_station(temp_path)
        assert is_valid, f"Expected valid station, got errors: {errors}"
        assert len(errors) == 0
    finally:
        if temp_path.exists():
            temp_path.unlink()


def test_invalid_station_missing_required():
    """Test validation fails for missing required fields."""
    invalid_station = {
        "id": "TEST2",
        "name": {"en": "Test Station"},
        # Missing: active, country, identifiers, location, timezone
    }

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        temp_path = Path(f.name)
        temp_path = temp_path.parent / "TEST2.json"
        json.dump(invalid_station, temp_path.open("w"))

    try:
        is_valid, errors = validate_station(temp_path)
        assert not is_valid
        assert len(errors) > 0
    finally:
        if temp_path.exists():
            temp_path.unlink()


def test_invalid_latitude():
    """Test validation fails for invalid latitude."""
    invalid_station = {
        "id": "TEST3",
        "active": True,
        "name": {"en": "Test Station"},
        "country": "US",
        "region": None,
        "identifiers": {},
        "location": {"latitude": 95.0, "longitude": 0.0, "elevation": 0},  # Invalid!
        "timezone": "UTC",
    }

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        temp_path = Path(f.name)
        temp_path = temp_path.parent / "TEST3.json"
        json.dump(invalid_station, temp_path.open("w"))

    try:
        is_valid, errors = validate_station(temp_path)
        assert not is_valid
        assert any("latitude" in str(e).lower() for e in errors)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def test_id_filename_mismatch():
    """Test validation fails when ID doesn't match filename."""
    station = {
        "id": "WRONG",
        "active": True,
        "name": {"en": "Test Station"},
        "country": "US",
        "region": None,
        "identifiers": {},
        "location": {"latitude": 0.0, "longitude": 0.0, "elevation": 0},
        "timezone": "UTC",
    }

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        temp_path = Path(f.name)
        temp_path = temp_path.parent / "TEST4.json"
        json.dump(station, temp_path.open("w"))

    try:
        is_valid, errors = validate_station(temp_path)
        assert not is_valid
        assert any("mismatch" in str(e).lower() for e in errors)
    finally:
        if temp_path.exists():
            temp_path.unlink()
