"""Check command - Validate station files."""

import click

from janitor.utils import get_station_files
from janitor.validation import validate_station


@click.command()
@click.option(
    "--delete",
    "-d",
    is_flag=True,
    help="Delete stations that fail validation",
)
def check(delete):
    """Validate all station files against the JSON schema."""
    click.echo("Validating station files...")

    invalid_count = 0
    deleted_count = 0
    total_count = 0

    for file_path in get_station_files():
        total_count += 1
        is_valid, errors = validate_station(file_path)

        if not is_valid:
            invalid_count += 1
            click.echo(f"\n✗ {file_path.name}:")
            for error in errors:
                click.echo(f"  - {error}")

            if delete:
                file_path.unlink()
                deleted_count += 1
                click.echo("  → Deleted")

    click.echo(f"\n{'='*60}")
    click.echo(f"Total stations: {total_count}")
    click.echo(f"Invalid stations: {invalid_count}")
    if delete:
        click.echo(f"Deleted stations: {deleted_count}")

    if invalid_count == 0:
        click.echo("✓ All station files are valid!")
    elif not delete:
        click.echo("\nUse --delete (-d) flag to delete invalid stations")
