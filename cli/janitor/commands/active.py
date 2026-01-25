"""Active command - Update active flags based on inventory data."""

import sqlite3
from pathlib import Path

import click
import requests

from janitor.utils import get_repo_root, get_station_files, read_station, write_station


def download_inventory_db(output_path: Path) -> None:
    """Download the inventory database from Meteostat."""
    url = "http://data.meteostat.net/stations.db"
    click.echo(f"Downloading inventory database from {url}...")

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)

        click.echo(f"✓ Downloaded to {output_path}")
    except requests.exceptions.Timeout:
        click.echo(
            "Error: Request timed out after 60 seconds. Please check your internet connection.",
            err=True,
        )
        raise click.Abort() from None
    except requests.exceptions.RequestException as e:
        click.echo(
            f"Error: Failed to download inventory database: {e}",
            err=True,
        )
        raise click.Abort() from None


def get_active_station_ids(db_path: Path) -> set:
    """Get set of station IDs that have inventory data."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to find stations with non-empty inventory
    # The inventory table should have records for stations with data
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    active_ids = set()

    # Check if inventory table exists
    if "inventory" in tables:
        cursor.execute("SELECT DISTINCT station FROM inventory")
        active_ids = {row[0] for row in cursor.fetchall()}

    conn.close()
    return active_ids


@click.command()
def active():
    """Update active flags based on the latest inventory database."""
    # Download the inventory database
    temp_db = get_repo_root() / "inventory_temp.db"

    try:
        download_inventory_db(temp_db)

        # Get active station IDs
        click.echo("Analyzing inventory data...")
        active_ids = get_active_station_ids(temp_db)
        click.echo(f"Found {len(active_ids)} stations with inventory data")

        # Update station files
        updated_count = 0
        for file_path in get_station_files():
            data = read_station(file_path)
            station_id = data["id"]

            # Determine if station should be active
            should_be_active = station_id in active_ids

            # Update if different
            if data.get("active") != should_be_active:
                data["active"] = should_be_active
                write_station(file_path, data)
                updated_count += 1
                status = "activated" if should_be_active else "deactivated"
                click.echo(f"  {station_id}: {status}")

        click.echo(f"\n✓ Updated {updated_count} stations")

    finally:
        # Clean up temporary database
        if temp_db.exists():
            temp_db.unlink()
