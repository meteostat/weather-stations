"""Query command - Execute SQL queries on the stations database."""

import json

import click
import meteostat as ms


@click.command()
@click.argument("query_str")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Output format",
)
def query(query_str, format):
    """Execute a SQL query on the stations database.

    Example: janitor query "SELECT * FROM stations LIMIT 10"
    """
    try:
        df = ms.stations.query(query_str)

        if df.empty:
            click.echo("No results found.")
            return

        df = df.reset_index()
        results = df.to_dict("records")

        if format == "json":
            click.echo(json.dumps(results, indent=2))
        else:
            # Table format
            if results:
                # Print header
                headers = list(results[0].keys())
                col_widths = {
                    col: max(len(col), max(len(str(row[col])) for row in results))
                    for col in headers
                }

                header_line = " | ".join(
                    col.ljust(col_widths[col]) for col in headers
                )
                click.echo(header_line)
                click.echo("-" * len(header_line))

                # Print rows
                for row in results:
                    click.echo(
                        " | ".join(
                            str(row[col]).ljust(col_widths[col]) for col in headers
                        )
                    )

                click.echo(f"\n{len(results)} row(s) returned")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort() from e
