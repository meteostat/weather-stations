"""Import command - Import stations from external sources."""

import importlib
import sys
from pathlib import Path

import click


@click.command()
@click.option(
    "--source",
    "-s",
    required=True,
    help="Data source name (maps to import script in cli/janitor/importers/)",
)
def import_cmd(source):
    """Import or update stations from a data source.

    The --source argument maps to an import script in cli/janitor/importers/.
    For example, --source gsa will look for cli/janitor/importers/gsa.py
    """
    importers_dir = Path(__file__).parent.parent / "importers"

    if not importers_dir.exists():
        importers_dir.mkdir(parents=True)

    importer_file = importers_dir / f"{source}.py"

    if not importer_file.exists():
        click.echo(f"Error: Importer '{source}' not found at {importer_file}", err=True)
        click.echo("\nAvailable importers:")

        if importers_dir.exists():
            available = [
                f.stem for f in importers_dir.glob("*.py") if f.stem != "__init__"
            ]
            if available:
                for imp in available:
                    click.echo(f"  - {imp}")
            else:
                click.echo("  (none)")

        raise click.Abort()

    click.echo(f"Running importer: {source}")

    # Add importers directory to Python path
    sys.path.insert(0, str(importers_dir.parent))

    try:
        # Import the module
        module = importlib.import_module(f"importers.{source}")

        # Look for a run() or main() function
        if hasattr(module, "run"):
            module.run()
        elif hasattr(module, "main"):
            module.main()
        else:
            click.echo(
                f"Error: Importer '{source}' must have a run() or main() function",
                err=True,
            )
            raise click.Abort()

        click.echo(f"✓ Import from '{source}' completed")

    except Exception as e:
        click.echo(f"Error running importer: {e}", err=True)
        raise
    finally:
        sys.path.pop(0)
