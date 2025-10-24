"""CLI command for converting JSON/dictionary data to C-CDA documents."""

import json
import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

logger = logging.getLogger(__name__)
console = Console()


def from_json_command(
    input_file: Path,
    output: Optional[Path] = None,
    pretty: bool = True,
) -> None:
    """Convert JSON/dictionary data to a C-CDA XML document.

    Args:
        input_file: Path to JSON file containing C-CDA data
        output: Output file path (prints to stdout if not specified)
        pretty: Pretty-print the XML output
    """
    from ccdakit.utils.converters import DictToCCDAConverter

    try:
        # Read JSON file
        with open(input_file, "r") as f:
            data = json.load(f)

        # Convert to C-CDA
        converter = DictToCCDAConverter()
        document = converter.from_dict(data)

        # Generate XML
        xml_string = document.to_xml_string(pretty=pretty)

        # Output
        if output:
            output.write_text(xml_string)
            console.print(f"[green]✓[/green] C-CDA document written to: {output}")
        else:
            console.print(xml_string)

    except FileNotFoundError:
        console.print(f"[red]Error:[/red] File not found: {input_file}", err=True)
        raise typer.Exit(1)
    except json.JSONDecodeError as e:
        console.print(f"[red]Error:[/red] Invalid JSON: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}", err=True)
        logger.exception("Failed to convert JSON to C-CDA")
        raise typer.Exit(1)
