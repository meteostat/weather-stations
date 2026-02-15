"""Active command - Update active flags based on inventory data."""

import click
import meteostat as ms

from janitor.utils import get_station_files, read_station, write_station


def get_active_station_ids() -> set:
    """Get set of station IDs that have inventory data from Meteostat."""
    df = ms.stations.query()
    return set(df.index.tolist())


@click.command()
def active():
    """Update active flags based on the latest inventory database."""
    click.echo("Fetching inventory data from Meteostat...")

    # Get active station IDs from Meteostat
    active_ids = get_active_station_ids()
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
