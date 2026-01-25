"""Main CLI entry point."""

import click

from janitor.commands.active import active
from janitor.commands.check import check
from janitor.commands.duplicates import duplicates
from janitor.commands.import_cmd import import_cmd
from janitor.commands.query import query
from janitor.commands.sync import sync


@click.group()
@click.version_option()
def cli():
    """Janitor - Weather station management tool."""
    pass


cli.add_command(sync)
cli.add_command(duplicates)
cli.add_command(active)
cli.add_command(check)
cli.add_command(import_cmd, name="import")
cli.add_command(query)


if __name__ == "__main__":
    cli()
