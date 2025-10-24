"""CLI command for downloading XSD and Schematron schema files."""

import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

logger = logging.getLogger(__name__)
console = Console()


def download_schemas_command(
    schema_type: str = "all",
    output_dir: Optional[Path] = None,
    force: bool = False,
) -> None:
    """Download XSD and/or Schematron schema files for validation.

    Args:
        schema_type: Type of schemas to download: 'xsd', 'schematron', or 'all'
        output_dir: Custom directory for schemas (uses default if not specified)
        force: Force re-download even if schemas already exist
    """
    from ccdakit.validators.schematron_downloader import SchematronDownloader
    from ccdakit.validators.xsd_downloader import XSDDownloader

    schema_type = schema_type.lower()
    if schema_type not in ["xsd", "schematron", "all"]:
        console.print(f"[red]Error:[/red] Invalid schema type: {schema_type}")
        console.print("Valid options: xsd, schematron, all")
        raise typer.Exit(1)

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Download XSD schemas
            if schema_type in ["xsd", "all"]:
                task = progress.add_task("Downloading XSD schemas...", total=None)
                xsd_downloader = XSDDownloader(schema_dir=output_dir)

                if force or not xsd_downloader.is_downloaded():
                    xsd_path = xsd_downloader.download()
                    progress.update(task, description="[green]✓ XSD schemas downloaded")
                    console.print(f"[green]✓[/green] XSD schemas: {xsd_path}")
                else:
                    progress.update(task, description="[yellow]XSD schemas already exist (use --force to re-download)")
                    console.print(f"[yellow]→[/yellow] XSD schemas already exist at: {xsd_downloader.schema_path}")

            # Download Schematron schemas
            if schema_type in ["schematron", "all"]:
                task = progress.add_task("Downloading Schematron schemas...", total=None)
                schematron_downloader = SchematronDownloader(schema_dir=output_dir)

                if force or not schematron_downloader.is_downloaded():
                    schematron_path = schematron_downloader.download()
                    progress.update(task, description="[green]✓ Schematron schemas downloaded and cleaned")
                    console.print(f"[green]✓[/green] Schematron schemas: {schematron_path}")
                else:
                    progress.update(task, description="[yellow]Schematron schemas already exist (use --force to re-download)")
                    console.print(f"[yellow]→[/yellow] Schematron schemas already exist at: {schematron_downloader.schema_dir}")

        console.print("\n[green]Schema download complete![/green]")

    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to download schemas: {e}", err=True)
        logger.exception("Schema download failed")
        raise typer.Exit(1)
