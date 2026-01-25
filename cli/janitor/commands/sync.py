"""Sync command - Create SQLite database from active stations."""

import click

from janitor.database import create_database


@click.command()
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output path for the database file (default: stations.db in repo root)",
)
def sync(output):
    """Create a SQLite database from all active stations."""
    from pathlib import Path

    db_path = Path(output) if output else None

    click.echo("Creating database from active stations...")
    result_path = create_database(db_path)
    click.echo(f"✓ Database created: {result_path}")
