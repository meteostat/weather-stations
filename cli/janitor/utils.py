"""Utility functions for the Janitor CLI."""

import json
from pathlib import Path
from typing import Iterator


def get_repo_root() -> Path:
    """Get the repository root directory."""
    # Start from current file and go up to find the repo root
    current = Path(__file__).resolve()
    while current.parent != current:
        if (current / ".git").exists():
            return current
        current = current.parent
    # If .git not found, assume we're in the cli directory
    return Path(__file__).resolve().parent.parent.parent


def get_stations_dir() -> Path:
    """Get the stations directory path."""
    return get_repo_root() / "stations"


def get_station_files() -> Iterator[Path]:
    """Iterate over all station JSON files."""
    stations_dir = get_stations_dir()
    if stations_dir.exists():
        for file_path in sorted(stations_dir.glob("*.json")):
            yield file_path


def read_station(file_path: Path) -> dict:
    """Read and parse a station JSON file."""
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def write_station(file_path: Path, data: dict) -> None:
    """Write station data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_station_id_from_path(file_path: Path) -> str:
    """Extract station ID from file path."""
    return file_path.stem
