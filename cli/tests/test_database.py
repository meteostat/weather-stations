"""Tests for database operations."""

import sqlite3
import tempfile
from pathlib import Path

from janitor.database import create_database, query_database


def test_create_database():
    """Test database creation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        result = create_database(db_path)

        assert result == db_path
        assert db_path.exists()

        # Verify structure
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check tables exist
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]
        assert "stations" in tables
        assert "names" in tables
        assert "identifiers" in tables

        # Check stations have data
        cursor.execute("SELECT COUNT(*) FROM stations")
        count = cursor.fetchone()[0]
        assert count > 0  # Should have some active stations

        conn.close()


def test_query_database():
    """Test database querying."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        create_database(db_path)

        # Test simple query
        results = query_database("SELECT COUNT(*) as count FROM stations", db_path)
        assert len(results) == 1
        assert "count" in results[0]
        assert results[0]["count"] > 0

        # Test query with conditions
        results = query_database(
            "SELECT id FROM stations WHERE country='US' LIMIT 5", db_path
        )
        assert len(results) <= 5
        for row in results:
            assert "id" in row
