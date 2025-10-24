"""Validate command implementation."""

import json
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ccdakit.core.validation import ValidationLevel, ValidationResult
from ccdakit.validators import SchematronValidator, XSDValidator
from ccdakit.validators.utils import get_default_schema_path


console = Console()


def validate_command(
    file_path: Path,
    xsd: bool = True,
    schematron: bool = True,
    output_format: str = "text",
) -> None:
    """
    Validate a C-CDA document.

    Args:
        file_path: Path to the C-CDA XML file
        xsd: Whether to run XSD validation
        schematron: Whether to run Schematron validation
        output_format: Output format (text, json, html)
    """
    # Validate file exists
    if not file_path.exists():
        console.print(f"[red]Error:[/red] File not found: {file_path}")
        sys.exit(1)

    if not file_path.is_file():
        console.print(f"[red]Error:[/red] Not a file: {file_path}")
        sys.exit(1)

    # Show validation banner
    console.print(
        Panel.fit(
            f"[bold cyan]Validating:[/bold cyan] {file_path.name}",
            border_style="cyan",
        )
    )

    # Store all results
    all_results = {}

    # Run XSD validation
    if xsd:
        console.print("\n[bold]Running XSD Schema Validation...[/bold]")
        xsd_result = _run_xsd_validation(file_path)
        all_results["xsd"] = xsd_result

        if output_format == "text":
            _print_validation_result(xsd_result, "XSD")

    # Run Schematron validation
    if schematron:
        console.print("\n[bold]Running Schematron Validation...[/bold]")
        schematron_result = _run_schematron_validation(file_path)
        all_results["schematron"] = schematron_result

        if output_format == "text":
            _print_validation_result(schematron_result, "Schematron")

    # Output in requested format
    if output_format == "json":
        _output_json(all_results)
    elif output_format == "html":
        _output_html(all_results, file_path)

    # Print summary
    _print_summary(all_results)

    # Exit with error code if validation failed
    if any(not result.is_valid for result in all_results.values()):
        sys.exit(1)


def _run_xsd_validation(file_path: Path) -> ValidationResult:
    """Run XSD validation with automatic schema download."""
    try:
        from ccdakit.validators.xsd_downloader import XSDDownloader

        # Check if schemas are installed
        downloader = XSDDownloader()

        if not downloader.is_installed():
            console.print(
                "[yellow]XSD schemas not found. Attempting automatic download...[/yellow]"
            )
            success, message = downloader.download_schemas()

            if not success:
                console.print(f"[red]Error:[/red] {message}")
                result = ValidationResult()
                result.errors.append(
                    type(
                        "ValidationIssue",
                        (),
                        {
                            "level": ValidationLevel.ERROR,
                            "message": f"XSD schemas not available: {message}. XSD validation cannot be performed. Run 'ccdakit download-schemas --schema-type xsd' to install schemas.",
                            "location": None,
                            "code": "SCHEMA_NOT_FOUND",
                        },
                    )()
                )
                return result
            else:
                console.print(f"[green]{message}[/green]")

        # Get schema path
        schema_path = get_default_schema_path()
        if schema_path is None:
            # get_default_schema_path returns the full path to CDA.xsd
            # If it's None, construct it from downloader directory
            schema_path = downloader.target_dir / "CDA.xsd"

        if not schema_path.exists():
            console.print("[red]Error:[/red] CDA.xsd not found after download attempt.")
            result = ValidationResult()
            result.errors.append(
                type(
                    "ValidationIssue",
                    (),
                    {
                        "level": ValidationLevel.ERROR,
                        "message": f"CDA.xsd not found at {schema_path}. XSD validation cannot be performed. Run 'ccdakit download-schemas --schema-type xsd' to install schemas.",
                        "location": None,
                        "code": "SCHEMA_NOT_FOUND",
                    },
                )()
            )
            return result

        validator = XSDValidator(schema_path)
        return validator.validate(file_path)

    except Exception as e:
        console.print(f"[red]XSD Validation Error:[/red] {e}")
        result = ValidationResult()
        result.errors.append(
            type(
                "ValidationIssue",
                (),
                {
                    "level": ValidationLevel.ERROR,
                    "message": str(e),
                    "location": None,
                    "code": "VALIDATION_FAILED",
                },
            )()
        )
        return result


def _run_schematron_validation(file_path: Path) -> ValidationResult:
    """Run Schematron validation."""
    try:
        # Use default schematron (auto-downloads if needed)
        validator = SchematronValidator()
        return validator.validate(file_path)

    except Exception as e:
        console.print(f"[red]Schematron Validation Error:[/red] {e}")
        result = ValidationResult()
        result.errors.append(
            type(
                "ValidationIssue",
                (),
                {
                    "level": ValidationLevel.ERROR,
                    "message": str(e),
                    "location": None,
                    "code": "VALIDATION_FAILED",
                },
            )()
        )
        return result


def _print_validation_result(result: ValidationResult, validator_name: str) -> None:
    """Print validation result in a nice table format."""
    if result.is_valid and not result.has_warnings:
        console.print(f"[green]✓[/green] {validator_name} validation passed!")
        return

    # Create table for issues
    table = Table(show_header=True, header_style="bold")
    table.add_column("Level", style="bold", width=10)
    table.add_column("Location", style="dim", width=30)
    table.add_column("Message", width=70)
    table.add_column("Code", style="dim", width=20)

    # Add errors
    for error in result.errors:
        table.add_row(
            "[red]ERROR[/red]",
            error.location or "",
            error.message,
            error.code or "",
        )

    # Add warnings
    for warning in result.warnings:
        table.add_row(
            "[yellow]WARNING[/yellow]",
            warning.location or "",
            warning.message,
            warning.code or "",
        )

    console.print(table)


def _output_json(results: dict) -> None:
    """Output results as JSON."""
    output = {}
    for validator_name, result in results.items():
        output[validator_name] = result.to_dict()

    console.print(json.dumps(output, indent=2))


def _output_html(results: dict, file_path: Path) -> None:
    """Output results as HTML."""
    from jinja2 import Template

    # Simple HTML template
    template_str = """
<!DOCTYPE html>
<html>
<head>
    <title>Validation Report - {{ filename }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
        h1 { color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
        h2 { color: #555; margin-top: 30px; }
        .summary { display: flex; gap: 20px; margin: 20px 0; }
        .summary-box { flex: 1; padding: 20px; border-radius: 5px; text-align: center; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .warning { background: #fff3cd; color: #856404; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #007bff; color: white; }
        .error-row { background: #f8d7da; }
        .warning-row { background: #fff3cd; }
        .badge { padding: 4px 8px; border-radius: 3px; font-weight: bold; }
        .badge-error { background: #dc3545; color: white; }
        .badge-warning { background: #ffc107; color: black; }
    </style>
</head>
<body>
    <div class="container">
        <h1>C-CDA Validation Report</h1>
        <p><strong>File:</strong> {{ filename }}</p>

        <div class="summary">
            {% for name, result in results.items() %}
            <div class="summary-box {{ 'success' if result.is_valid else 'error' }}">
                <h3>{{ name.upper() }}</h3>
                <p>{{ 'PASSED' if result.is_valid else 'FAILED' }}</p>
                <p>{{ result.error_count }} errors, {{ result.warning_count }} warnings</p>
            </div>
            {% endfor %}
        </div>

        {% for name, result in results.items() %}
        <h2>{{ name.upper() }} Validation</h2>

        {% if result.errors or result.warnings %}
        <table>
            <thead>
                <tr>
                    <th>Level</th>
                    <th>Location</th>
                    <th>Message</th>
                    <th>Code</th>
                </tr>
            </thead>
            <tbody>
                {% for error in result.errors %}
                <tr class="error-row">
                    <td><span class="badge badge-error">ERROR</span></td>
                    <td>{{ error }}</td>
                    <td>{{ error }}</td>
                    <td>{{ error }}</td>
                </tr>
                {% endfor %}
                {% for warning in result.warnings %}
                <tr class="warning-row">
                    <td><span class="badge badge-warning">WARNING</span></td>
                    <td>{{ warning }}</td>
                    <td>{{ warning }}</td>
                    <td>{{ warning }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <p style="color: green;">✓ All checks passed!</p>
        {% endif %}
        {% endfor %}
    </div>
</body>
</html>
    """

    template = Template(template_str)
    html_output = template.render(
        filename=file_path.name,
        results={name: result.to_dict() for name, result in results.items()},
    )

    # Write to file
    output_path = file_path.parent / f"{file_path.stem}_validation_report.html"
    output_path.write_text(html_output)

    console.print(f"\n[green]HTML report saved to:[/green] {output_path}")


def _print_summary(results: dict) -> None:
    """Print validation summary."""
    console.print("\n" + "=" * 60)
    console.print("[bold]Validation Summary[/bold]")
    console.print("=" * 60)

    total_errors = sum(len(r.errors) for r in results.values())
    total_warnings = sum(len(r.warnings) for r in results.values())

    for name, result in results.items():
        status = "[green]PASSED[/green]" if result.is_valid else "[red]FAILED[/red]"
        console.print(f"{name.upper()}: {status}")
        console.print(f"  Errors: {len(result.errors)}, Warnings: {len(result.warnings)}")

    console.print("\n" + "=" * 60)
    if total_errors == 0:
        console.print("[green bold]✓ Document is valid![/green bold]")
    else:
        console.print(f"[red bold]✗ Validation failed with {total_errors} error(s)[/red bold]")

    if total_warnings > 0:
        console.print(f"[yellow]⚠ {total_warnings} warning(s) found[/yellow]")

    console.print("=" * 60 + "\n")
