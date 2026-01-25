"""Tests for CLI commands."""

import sqlite3
import tempfile
from pathlib import Path

from click.testing import CliRunner
from janitor.cli import cli


def test_sync_command():
    """Test the sync command."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        result = runner.invoke(cli, ["sync", "-o", str(db_path)])

        assert result.exit_code == 0
        assert "Database created" in result.output
        assert db_path.exists()

        # Verify database structure
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]
        assert "stations" in tables
        assert "names" in tables
        assert "identifiers" in tables
        conn.close()


def test_query_command():
    """Test the query command."""
    runner = CliRunner()

    # First create a database
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        runner.invoke(cli, ["sync", "-o", str(db_path)])

        # Query it
        result = runner.invoke(
            cli, ["query", "SELECT COUNT(*) as count FROM stations", "-db", str(db_path)]
        )

        assert result.exit_code == 0
        assert "count" in result.output


def test_check_command():
    """Test the check command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["check"])

    # Should run without error
    assert result.exit_code == 0
    assert "Validating" in result.output


def test_import_command_unknown_source():
    """Test import command with unknown source."""
    runner = CliRunner()
    result = runner.invoke(cli, ["import", "-s", "nonexistent"])

    assert result.exit_code != 0
    assert "not found" in result.output


def test_import_command_gsa():
    """Test import command with GSA source."""
    runner = CliRunner()
    result = runner.invoke(cli, ["import", "-s", "gsa"])

    assert result.exit_code == 0
    assert "placeholder" in result.output.lower()
