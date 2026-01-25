"""Database operations for weather stations."""

import json
import sqlite3
from pathlib import Path
from typing import Optional

from janitor.utils import get_repo_root, get_station_files, read_station


def create_database(db_path: Optional[Path] = None) -> Path:
    """
    Create a SQLite database from all active stations.

    Args:
        db_path: Path to the database file. If None, uses stations.db in repo root.

    Returns:
        Path to the created database file.
    """
    if db_path is None:
        db_path = get_repo_root() / "stations.db"

    # Remove existing database
    if db_path.exists():
        db_path.unlink()

    # Get tables SQL
    tables_sql_path = get_repo_root() / "tables.sql"
    with open(tables_sql_path, encoding="utf-8") as f:
        tables_sql = f.read()

    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.executescript(tables_sql)

    # Process all station files
    for file_path in get_station_files():
        try:
            data = read_station(file_path)

            # Skip inactive stations
            if not data.get("active", False):
                continue

            # Insert into stations table
            cursor.execute(
                """INSERT INTO `stations` VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    data["id"],
                    data["country"],
                    data.get("region"),
                    data["location"]["latitude"],
                    data["location"]["longitude"],
                    data["location"]["elevation"],
                    data["timezone"],
                ),
            )

            # Insert into names table
            for lang, name in data["name"].items():
                cursor.execute(
                    """INSERT INTO `names` VALUES (?, ?, ?)""",
                    (data["id"], lang, name),
                )

            # Insert into identifiers table
            for key, value in data.get("identifiers", {}).items():
                cursor.execute(
                    """INSERT INTO `identifiers` VALUES (?, ?, ?)""",
                    (data["id"], key, value),
                )

        except (json.JSONDecodeError, KeyError):
            # Skip invalid files
            continue

    # Commit and close
    conn.commit()
    conn.close()

    return db_path


def query_database(query_str: str, db_path: Optional[Path] = None) -> list:
    """
    Execute a SQL query on the stations database.

    Args:
        query_str: SQL query to execute
        db_path: Path to the database file. If None, uses stations.db in repo root.

    Returns:
        List of rows returned by the query.
    """
    if db_path is None:
        db_path = get_repo_root() / "stations.db"

    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    cursor = conn.cursor()

    try:
        cursor.execute(query_str)
        results = [dict(row) for row in cursor.fetchall()]
        return results
    finally:
        conn.close()
