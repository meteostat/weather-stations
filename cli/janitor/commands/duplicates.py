"""Duplicates command - Find potential duplicate stations."""

import click

from janitor.database import query_database
from janitor.utils import get_repo_root


@click.command()
@click.option(
    "--distance",
    "-d",
    type=float,
    default=10.0,
    help="Maximum distance in km to consider as duplicate (default: 10.0)",
)
def duplicates(distance):
    """List potential duplicate stations based on proximity and identifiers."""
    db_path = get_repo_root() / "stations.db"

    if not db_path.exists():
        click.echo(
            "Database not found. Please run 'janitor sync' first.", err=True
        )
        raise click.Abort()

    click.echo("Searching for potential duplicates...")

    # Find duplicates by identifiers
    identifier_duplicates = find_identifier_duplicates(db_path)

    # Find duplicates by proximity
    proximity_duplicates = find_proximity_duplicates(db_path, distance)

    # Display results
    if identifier_duplicates:
        click.echo("\n" + "=" * 60)
        click.echo("DUPLICATES BY IDENTIFIER")
        click.echo("=" * 60)

        for key, value, stations in identifier_duplicates:
            click.echo(f"\n{key.upper()}: {value}")
            for station in stations:
                click.echo(f"  - {station}")

    if proximity_duplicates:
        click.echo("\n" + "=" * 60)
        click.echo(f"DUPLICATES BY PROXIMITY (<{distance} km)")
        click.echo("=" * 60)

        for s1_id, s2_id, dist in proximity_duplicates:
            click.echo(f"\n{s1_id} ↔ {s2_id}: {dist:.2f} km")

    if not identifier_duplicates and not proximity_duplicates:
        click.echo("✓ No potential duplicates found!")


def find_identifier_duplicates(db_path):
    """Find stations sharing the same identifier."""
    query = """
        SELECT key, value, GROUP_CONCAT(station) as stations
        FROM identifiers
        GROUP BY key, value
        HAVING COUNT(*) > 1
        ORDER BY key, value
    """
    results = query_database(query, db_path)

    duplicates = []
    for row in results:
        stations = row["stations"].split(",")
        duplicates.append((row["key"], row["value"], stations))

    return duplicates


def find_proximity_duplicates(db_path, max_distance_km):
    """Find stations within specified distance of each other."""
    # Get all stations
    query = "SELECT id, latitude, longitude FROM stations"
    stations = query_database(query, db_path)

    duplicates = []

    # Compare each pair
    for i, s1 in enumerate(stations):
        for s2 in stations[i + 1 :]:
            dist = calculate_distance(
                s1["latitude"],
                s1["longitude"],
                s2["latitude"],
                s2["longitude"],
            )

            if dist <= max_distance_km:
                duplicates.append((s1["id"], s2["id"], dist))

    return sorted(duplicates, key=lambda x: x[2])


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km using Haversine formula."""
    import math

    # Earth radius in km
    R = 6371.0

    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
