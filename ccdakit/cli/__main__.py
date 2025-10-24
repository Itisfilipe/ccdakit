"""Main CLI entry point for ccdakit."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console


# Create the main Typer app
app = typer.Typer(
    name="ccdakit",
    help="CLI tool for working with HL7 C-CDA clinical documents",
    add_completion=False,
)

console = Console()


@app.command()
def validate(
    file_path: Path = typer.Argument(..., help="Path to the C-CDA XML file to validate"),
    xsd: bool = typer.Option(True, help="Run XSD schema validation"),
    schematron: bool = typer.Option(True, help="Run Schematron validation"),
    output_format: str = typer.Option("text", help="Output format: text, json, or html"),
) -> None:
    """Validate a C-CDA document using XSD and/or Schematron rules."""
    from ccdakit.cli.commands.validate import validate_command

    validate_command(file_path, xsd=xsd, schematron=schematron, output_format=output_format)


@app.command()
def generate(
    document_type: str = typer.Argument(
        ..., help="Document type to generate (e.g., ccd, discharge-summary)"
    ),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    sections: Optional[str] = typer.Option(
        None, help="Comma-separated list of sections to include"
    ),
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="Interactive mode with prompts"
    ),
) -> None:
    """Generate a sample C-CDA document for testing."""
    from ccdakit.cli.commands.generate import generate_command

    generate_command(document_type, output=output, sections=sections, interactive=interactive)


@app.command()
def convert(
    file_path: Path = typer.Argument(..., help="Path to the C-CDA XML file to convert"),
    to: str = typer.Option("html", help="Target format (currently only 'html')"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    template: str = typer.Option(
        "minimal", help="XSLT template: 'minimal' (custom) or 'official' (HL7 CDA-core-xsl)"
    ),
) -> None:
    """Convert a C-CDA XML document to human-readable HTML using XSLT transformation."""
    from ccdakit.cli.commands.convert import convert_command

    convert_command(file_path, to=to, output=output, template=template)


@app.command()
def compare(
    file1: Path = typer.Argument(..., help="First C-CDA XML file"),
    file2: Path = typer.Argument(..., help="Second C-CDA XML file"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file path for comparison report"
    ),
    format: str = typer.Option("text", help="Output format: text or html"),
) -> None:
    """Compare two C-CDA documents and highlight differences."""
    from ccdakit.cli.commands.compare import compare_command

    compare_command(file1, file2, output=output, format=format)


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", help="Host to bind the server to"),
    port: int = typer.Option(8000, help="Port to bind the server to"),
    debug: bool = typer.Option(False, help="Run in debug mode"),
) -> None:
    """Start the web UI server for interactive C-CDA operations."""
    from ccdakit.cli.commands.serve import serve_command

    serve_command(host=host, port=port, debug=debug)


@app.command()
def from_json(
    input_file: Path = typer.Argument(..., help="Path to JSON file containing C-CDA data"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    pretty: bool = typer.Option(True, help="Pretty-print the XML output"),
) -> None:
    """Convert JSON/dictionary data to a C-CDA XML document."""
    from ccdakit.cli.commands.from_json import from_json_command

    from_json_command(input_file, output=output, pretty=pretty)


@app.command()
def list_sections(
    category: Optional[str] = typer.Option(None, help="Filter by category: core, extended, specialized, hospital"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show template IDs and additional details"),
) -> None:
    """List all available C-CDA section builders."""
    from ccdakit.cli.commands.list_sections import list_sections_command

    list_sections_command(category=category, verbose=verbose)


@app.command()
def download_schemas(
    schema_type: str = typer.Option("all", help="Type of schemas: xsd, schematron, or all"),
    output_dir: Optional[Path] = typer.Option(None, help="Custom directory for schemas"),
    force: bool = typer.Option(False, "--force", "-f", help="Force re-download even if schemas exist"),
) -> None:
    """Download XSD and/or Schematron schema files for validation."""
    from ccdakit.cli.commands.download_schemas import download_schemas_command

    download_schemas_command(schema_type=schema_type, output_dir=output_dir, force=force)


@app.command()
def version() -> None:
    """Show the ccdakit version."""
    import ccdakit

    console.print(f"[bold cyan]ccdakit[/bold cyan] version [green]{ccdakit.__version__}[/green]")


if __name__ == "__main__":
    app()
