"""Compare command implementation."""

import sys
from pathlib import Path
from typing import Optional

from lxml import etree
from rich.console import Console
from rich.table import Table


console = Console()

# XML namespaces
NAMESPACES = {"cda": "urn:hl7-org:v3"}


def compare_command(
    file1: Path,
    file2: Path,
    output: Optional[Path] = None,
    format: str = "text",
) -> None:
    """
    Compare two C-CDA documents.

    Args:
        file1: First C-CDA XML file
        file2: Second C-CDA XML file
        output: Output file path for comparison report
        format: Output format (text or html)
    """
    # Validate files exist
    for file_path in [file1, file2]:
        if not file_path.exists():
            console.print(f"[red]Error:[/red] File not found: {file_path}")
            sys.exit(1)

    console.print("[cyan]Comparing:[/cyan]")
    console.print(f"  File 1: {file1.name}")
    console.print(f"  File 2: {file2.name}")

    # Parse both documents
    try:
        tree1 = etree.parse(str(file1))
        tree2 = etree.parse(str(file2))
    except etree.XMLSyntaxError as e:
        console.print(f"[red]Error parsing XML:[/red] {e}")
        sys.exit(1)

    # Extract data from both documents
    data1 = _extract_comparison_data(tree1.getroot())
    data2 = _extract_comparison_data(tree2.getroot())

    # Compare the documents
    comparison = _compare_documents(data1, data2)

    # Output comparison
    if format == "text":
        _output_text_comparison(comparison, file1, file2)
    elif format == "html":
        html_content = _generate_comparison_html(comparison, file1, file2)
        if output is None:
            output = Path(f"comparison_{file1.stem}_vs_{file2.stem}.html")
        output.write_text(html_content)
        console.print(f"\n[green]✓[/green] Comparison saved to: {output.absolute()}")
    else:
        console.print(f"[red]Error:[/red] Unsupported format: {format}")
        sys.exit(1)


def _extract_comparison_data(root: etree._Element) -> dict:
    """Extract data for comparison."""
    # Patient info
    patient_role = root.find(".//cda:recordTarget/cda:patientRole", NAMESPACES)
    patient = patient_role.find(".//cda:patient", NAMESPACES) if patient_role else None

    patient_data = {}
    if patient is not None:
        name_elem = patient.find(".//cda:name", NAMESPACES)
        if name_elem is not None:
            given = _get_text(name_elem, ".//cda:given")
            family = _get_text(name_elem, ".//cda:family")
            patient_data["name"] = f"{given} {family}".strip()

        patient_data["gender"] = _get_text(patient, ".//cda:administrativeGenderCode/@displayName")
        patient_data["birth_date"] = _get_text(patient, ".//cda:birthTime/@value")

    # Document metadata
    doc_data = {
        "title": _get_text(root, ".//cda:title"),
        "effective_time": _get_text(root, ".//cda:effectiveTime/@value"),
    }

    # Sections
    sections = {}
    component = root.find(".//cda:component/cda:structuredBody", NAMESPACES)
    if component is not None:
        for section in component.findall(".//cda:section", NAMESPACES):
            title = _get_text(section, ".//cda:title")
            code = _get_text(section, ".//cda:code/@code")
            entry_count = len(section.findall(".//cda:entry", NAMESPACES))
            sections[title or code] = {
                "code": code,
                "entry_count": entry_count,
            }

    return {
        "patient": patient_data,
        "document": doc_data,
        "sections": sections,
    }


def _compare_documents(data1: dict, data2: dict) -> dict:
    """Compare two document data structures."""
    comparison = {
        "patient_differences": [],
        "document_differences": [],
        "section_differences": [],
        "sections_only_in_1": [],
        "sections_only_in_2": [],
        "common_sections": [],
    }

    # Compare patient data
    for key in set(data1["patient"].keys()) | set(data2["patient"].keys()):
        val1 = data1["patient"].get(key, "N/A")
        val2 = data2["patient"].get(key, "N/A")
        if val1 != val2:
            comparison["patient_differences"].append(
                {
                    "field": key,
                    "file1": val1,
                    "file2": val2,
                }
            )

    # Compare document metadata
    for key in set(data1["document"].keys()) | set(data2["document"].keys()):
        val1 = data1["document"].get(key, "N/A")
        val2 = data2["document"].get(key, "N/A")
        if val1 != val2:
            comparison["document_differences"].append(
                {
                    "field": key,
                    "file1": val1,
                    "file2": val2,
                }
            )

    # Compare sections
    sections1 = set(data1["sections"].keys())
    sections2 = set(data2["sections"].keys())

    comparison["sections_only_in_1"] = list(sections1 - sections2)
    comparison["sections_only_in_2"] = list(sections2 - sections1)
    common = sections1 & sections2

    for section_name in common:
        s1 = data1["sections"][section_name]
        s2 = data2["sections"][section_name]

        if s1["entry_count"] != s2["entry_count"]:
            comparison["section_differences"].append(
                {
                    "section": section_name,
                    "file1_entries": s1["entry_count"],
                    "file2_entries": s2["entry_count"],
                }
            )
        else:
            comparison["common_sections"].append(section_name)

    return comparison


def _output_text_comparison(comparison: dict, file1: Path, file2: Path) -> None:
    """Output comparison in text format."""
    console.print("\n" + "=" * 80)
    console.print("[bold]Document Comparison Report[/bold]")
    console.print("=" * 80)

    # Patient differences
    if comparison["patient_differences"]:
        console.print("\n[bold red]Patient Demographic Differences:[/bold red]")
        table = Table(show_header=True, header_style="bold")
        table.add_column("Field", width=20)
        table.add_column(f"File 1: {file1.name}", width=30)
        table.add_column(f"File 2: {file2.name}", width=30)

        for diff in comparison["patient_differences"]:
            table.add_row(diff["field"], str(diff["file1"]), str(diff["file2"]))

        console.print(table)
    else:
        console.print("\n[green]✓ Patient demographics are identical[/green]")

    # Document differences
    if comparison["document_differences"]:
        console.print("\n[bold red]Document Metadata Differences:[/bold red]")
        table = Table(show_header=True, header_style="bold")
        table.add_column("Field", width=20)
        table.add_column(f"File 1: {file1.name}", width=30)
        table.add_column(f"File 2: {file2.name}", width=30)

        for diff in comparison["document_differences"]:
            table.add_row(diff["field"], str(diff["file1"]), str(diff["file2"]))

        console.print(table)

    # Sections only in file 1
    if comparison["sections_only_in_1"]:
        console.print(f"\n[bold yellow]Sections only in {file1.name}:[/bold yellow]")
        for section in comparison["sections_only_in_1"]:
            console.print(f"  • {section}")

    # Sections only in file 2
    if comparison["sections_only_in_2"]:
        console.print(f"\n[bold yellow]Sections only in {file2.name}:[/bold yellow]")
        for section in comparison["sections_only_in_2"]:
            console.print(f"  • {section}")

    # Section differences
    if comparison["section_differences"]:
        console.print("\n[bold yellow]Sections with Different Entry Counts:[/bold yellow]")
        table = Table(show_header=True, header_style="bold")
        table.add_column("Section", width=40)
        table.add_column("File 1 Entries", width=15)
        table.add_column("File 2 Entries", width=15)

        for diff in comparison["section_differences"]:
            table.add_row(
                diff["section"],
                str(diff["file1_entries"]),
                str(diff["file2_entries"]),
            )

        console.print(table)

    # Common sections
    if comparison["common_sections"]:
        console.print(
            f"\n[green]✓ {len(comparison['common_sections'])} sections are identical[/green]"
        )

    # Summary
    console.print("\n" + "=" * 80)
    total_diffs = (
        len(comparison["patient_differences"])
        + len(comparison["document_differences"])
        + len(comparison["sections_only_in_1"])
        + len(comparison["sections_only_in_2"])
        + len(comparison["section_differences"])
    )

    if total_diffs == 0:
        console.print("[bold green]Documents are structurally identical![/bold green]")
    else:
        console.print(f"[bold yellow]Found {total_diffs} differences[/bold yellow]")

    console.print("=" * 80 + "\n")


def _generate_comparison_html(comparison: dict, file1: Path, file2: Path) -> str:
    """Generate HTML comparison report."""
    from jinja2 import Template

    html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Document Comparison Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
        h1 { color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
        h2 { color: #555; margin-top: 30px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #007bff; color: white; }
        .diff-row { background: #fff3cd; }
        .success { color: #28a745; }
        .warning { color: #ffc107; }
        .error { color: #dc3545; }
        ul { list-style: none; padding: 0; }
        li { padding: 8px; margin: 4px 0; background: #f8f9fa; border-left: 3px solid #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Document Comparison Report</h1>
        <p><strong>File 1:</strong> {{ file1 }}</p>
        <p><strong>File 2:</strong> {{ file2 }}</p>

        {% if comparison.patient_differences %}
        <h2 class="error">Patient Demographic Differences</h2>
        <table>
            <tr><th>Field</th><th>File 1</th><th>File 2</th></tr>
            {% for diff in comparison.patient_differences %}
            <tr class="diff-row">
                <td>{{ diff.field }}</td>
                <td>{{ diff.file1 }}</td>
                <td>{{ diff.file2 }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <h2 class="success">✓ Patient demographics are identical</h2>
        {% endif %}

        {% if comparison.sections_only_in_1 %}
        <h2 class="warning">Sections only in {{ file1 }}</h2>
        <ul>
            {% for section in comparison.sections_only_in_1 %}
            <li>{{ section }}</li>
            {% endfor %}
        </ul>
        {% endif %}

        {% if comparison.sections_only_in_2 %}
        <h2 class="warning">Sections only in {{ file2 }}</h2>
        <ul>
            {% for section in comparison.sections_only_in_2 %}
            <li>{{ section }}</li>
            {% endfor %}
        </ul>
        {% endif %}

        {% if comparison.section_differences %}
        <h2 class="warning">Sections with Different Entry Counts</h2>
        <table>
            <tr><th>Section</th><th>File 1 Entries</th><th>File 2 Entries</th></tr>
            {% for diff in comparison.section_differences %}
            <tr class="diff-row">
                <td>{{ diff.section }}</td>
                <td>{{ diff.file1_entries }}</td>
                <td>{{ diff.file2_entries }}</td>
            </tr>
            {% endfor %}
        </table>
        {% endif %}
    </div>
</body>
</html>
    """

    template = Template(html_template)
    return template.render(
        comparison=comparison,
        file1=file1.name,
        file2=file2.name,
    )


def _get_text(element, xpath: str) -> str:
    """Safely get text from XPath."""
    if element is None:
        return ""

    try:
        result = element.xpath(xpath, namespaces=NAMESPACES)
        if result:
            return str(result[0]) if result[0] else ""
    except Exception:
        # Silently ignore XPath errors and return empty string
        return ""

    return ""
