"""Generate command implementation."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from ccdakit.builders.documents import ContinuityOfCareDocument, DischargeSummary


console = Console()

# Available document types
DOCUMENT_TYPES = {
    "ccd": {"name": "Continuity of Care Document", "class": ContinuityOfCareDocument},
    "discharge-summary": {"name": "Discharge Summary", "class": DischargeSummary},
}

# Available sections - organized by category
AVAILABLE_SECTIONS = [
    # Core Clinical Sections
    ("problems", "Problems Section"),
    ("medications", "Medications Section"),
    ("allergies", "Allergies and Intolerances Section"),
    ("immunizations", "Immunizations Section"),
    ("vital-signs", "Vital Signs Section"),
    ("procedures", "Procedures Section"),
    ("results", "Results Section"),
    ("social-history", "Social History Section"),
    ("encounters", "Encounters Section"),
    # Extended Clinical Sections
    ("goals", "Goals Section"),
    ("functional-status", "Functional Status Section"),
    ("mental-status", "Mental Status Section"),
    ("family-history", "Family History Section"),
    ("health-concerns", "Health Concerns Section"),
    ("health-status-evaluations", "Health Status Evaluations and Outcomes Section"),
    ("past-medical-history", "Past Medical History Section"),
    ("physical-exam", "Physical Exam Section"),
    ("assessment-and-plan", "Assessment and Plan Section"),
    # Specialized/Administrative Sections
    ("plan-of-treatment", "Plan of Treatment Section"),
    ("advance-directives", "Advance Directives Section"),
    ("medical-equipment", "Medical Equipment Section"),
    ("admission-medications", "Admission Medications Section"),
    ("discharge-medications", "Discharge Medications Section"),
    ("hospital-discharge-instructions", "Hospital Discharge Instructions Section"),
    ("payers", "Payers Section"),
    ("nutrition", "Nutrition Section"),
    ("reason-for-visit", "Reason for Visit Section"),
    ("chief-complaint-reason-for-visit", "Chief Complaint and Reason for Visit Section"),
    ("interventions", "Interventions Section"),
    # Hospital and Surgical Sections
    ("admission-diagnosis", "Admission Diagnosis Section"),
    ("discharge-diagnosis", "Discharge Diagnosis Section"),
    ("hospital-course", "Hospital Course Section"),
    ("instructions", "Instructions Section"),
    ("anesthesia", "Anesthesia Section"),
    ("postoperative-diagnosis", "Postoperative Diagnosis Section"),
    ("preoperative-diagnosis", "Preoperative Diagnosis Section"),
    ("complications", "Complications Section"),
    ("discharge-studies", "Hospital Discharge Studies Summary Section"),
    ("medications-administered", "Medications Administered Section"),
]


def generate_command(
    document_type: str,
    output: Path | None = None,
    sections: str | None = None,
    interactive: bool = False,
) -> None:
    """
    Generate a sample C-CDA document.

    Args:
        document_type: Type of document to generate (ccd, discharge-summary)
        output: Output file path
        sections: Comma-separated list of sections to include
        interactive: Whether to use interactive mode
    """
    # Validate document type
    if document_type not in DOCUMENT_TYPES:
        console.print(f"[red]Error:[/red] Unknown document type: {document_type}")
        console.print(f"Available types: {', '.join(DOCUMENT_TYPES.keys())}")
        sys.exit(1)

    # Check if faker is installed
    try:
        import importlib.util

        if importlib.util.find_spec("faker") is None:
            raise ImportError("faker not found")
    except ImportError:
        console.print(
            "[red]Error:[/red] Test data generation requires the 'faker' package.\n"
            "Install it with: [cyan]pip install 'ccdakit[test-data]'[/cyan] or "
            "[cyan]pip install faker>=20.0.0[/cyan]"
        )
        sys.exit(1)

    # Show banner
    doc_info = DOCUMENT_TYPES[document_type]
    console.print(
        Panel.fit(
            f"[bold cyan]Generating:[/bold cyan] {doc_info['name']}",
            border_style="cyan",
        )
    )

    # Interactive mode - ask user for preferences
    if interactive:
        sections_to_include = _interactive_section_selection()
    elif sections:
        sections_to_include = [s.strip() for s in sections.split(",")]
    else:
        # Default sections for each document type
        if document_type == "ccd":
            sections_to_include = ["problems", "medications", "allergies"]
        elif document_type == "discharge-summary":
            sections_to_include = [
                "problems",
                "medications",
                "allergies",
                "procedures",
                "vital-signs",
            ]
        else:
            sections_to_include = []

    # Generate the document
    console.print("\n[bold]Generating test data...[/bold]")
    try:
        doc = _generate_document(document_type, sections_to_include)
        xml_string = doc.to_xml_string(pretty=True)
    except Exception as e:
        console.print(f"[red]Error generating document:[/red] {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    # Determine output path
    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = Path(f"{document_type}_{timestamp}.xml")

    # Write to file
    try:
        output.write_text(xml_string)
        console.print("\n[green]✓[/green] Document generated successfully!")
        console.print(f"[green]Output:[/green] {output.absolute()}")

        # Show summary
        _show_document_summary(doc, sections_to_include)

    except Exception as e:
        console.print(f"[red]Error writing file:[/red] {e}")
        sys.exit(1)


def _interactive_section_selection() -> list[str]:
    """Interactively select sections to include."""
    console.print("\n[bold]Select sections to include:[/bold]")

    # Show available sections
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Section", width=40)

    for i, (_code, name) in enumerate(AVAILABLE_SECTIONS, 1):
        table.add_row(str(i), name)

    console.print(table)

    # Ask user to select sections
    console.print("\n[dim]Enter section numbers separated by commas (e.g., 1,2,3)[/dim]")
    console.print("[dim]Or press Enter to include all sections[/dim]")

    selection = Prompt.ask("Sections", default="all")

    if selection.lower() in ("all", ""):
        return [code for code, _ in AVAILABLE_SECTIONS]

    # Parse selection
    selected_sections = []
    try:
        for num in selection.split(","):
            num = num.strip()
            if num:
                idx = int(num) - 1
                if 0 <= idx < len(AVAILABLE_SECTIONS):
                    selected_sections.append(AVAILABLE_SECTIONS[idx][0])
                else:
                    console.print(f"[yellow]Warning:[/yellow] Invalid section number: {num}")
    except ValueError:
        console.print("[yellow]Warning:[/yellow] Invalid input. Using all sections.")
        return [code for code, _ in AVAILABLE_SECTIONS]

    if not selected_sections:
        console.print("[yellow]No sections selected. Using default sections.[/yellow]")
        return ["problems", "medications", "allergies"]

    return selected_sections


def _generate_document(document_type: str, sections_to_include: list[str]):
    """Generate a document with test data."""
    from datetime import datetime

    from ccdakit.builders.sections import (
        AllergiesSection,
        EncountersSection,
        ImmunizationsSection,
        MedicationsSection,
        ProblemsSection,
        ProceduresSection,
        ResultsSection,
        SocialHistorySection,
        VitalSignsSection,
    )
    from ccdakit.cli.commands.data_models import (
        Allergy,
        Author,
        Immunization,
        Medication,
        Organization,
        Patient,
        Problem,
        VitalSignsOrganizer,
    )
    from ccdakit.utils.test_data import SampleDataGenerator

    # Initialize test data generator
    generator = SampleDataGenerator()

    # Generate patient record
    record = generator.generate_complete_patient_record()

    # Convert dictionaries to protocol-compliant objects
    patient = Patient(record["patient"])
    problems = [Problem(p) for p in record["problems"]]
    medications = [Medication(m) for m in record["medications"]]
    allergies = [Allergy(a) for a in record["allergies"]]
    immunizations = [Immunization(i) for i in record["immunizations"]]
    vital_signs = [VitalSignsOrganizer(v) for v in record["vital_signs"]]

    # Create author and custodian
    author = Author(
        {
            "first_name": "John",
            "last_name": "Provider",
            "time": datetime.now(),
        }
    )

    custodian = Organization(
        {
            "name": "Example Healthcare Organization",
            "telecom": "tel:+1-555-123-4567",
            "address": {
                "street": "123 Healthcare Drive",
                "city": "Medical City",
                "state": "CA",
                "zip": "94000",
            },
        }
    )

    # Empty lists for sections not yet supported by test data generator
    procedures = []
    results = []
    social_history = []
    encounters = []

    # Build section objects
    section_builders = []

    if "problems" in sections_to_include:
        problems_section = ProblemsSection(problems=problems)
        section_builders.append(problems_section)

    if "medications" in sections_to_include:
        meds_section = MedicationsSection(medications=medications)
        section_builders.append(meds_section)

    if "allergies" in sections_to_include:
        allergies_section = AllergiesSection(allergies=allergies)
        section_builders.append(allergies_section)

    if "immunizations" in sections_to_include:
        immunizations_section = ImmunizationsSection(immunizations=immunizations)
        section_builders.append(immunizations_section)

    if "vital-signs" in sections_to_include:
        vital_signs_section = VitalSignsSection(vital_signs_organizers=vital_signs)
        section_builders.append(vital_signs_section)

    if "procedures" in sections_to_include and procedures:
        procedures_section = ProceduresSection(procedures=procedures)
        section_builders.append(procedures_section)

    if "results" in sections_to_include and results:
        results_section = ResultsSection(result_organizers=results)
        section_builders.append(results_section)

    if "social-history" in sections_to_include and social_history:
        social_history_section = SocialHistorySection(smoking_statuses=social_history)
        section_builders.append(social_history_section)

    if "encounters" in sections_to_include and encounters:
        encounters_section = EncountersSection(encounters=encounters)
        section_builders.append(encounters_section)

    # Get document class
    doc_class = DOCUMENT_TYPES[document_type]["class"]

    # Create document
    doc = doc_class(
        patient=patient,
        author=author,
        custodian=custodian,
        sections=section_builders,
    )

    return doc


def _show_document_summary(doc, sections_to_include: list[str]) -> None:
    """Show summary of generated document."""
    console.print("\n" + "=" * 60)
    console.print("[bold]Document Summary[/bold]")
    console.print("=" * 60)

    # Get section names
    section_names = [name for code, name in AVAILABLE_SECTIONS if code in sections_to_include]

    console.print(f"[cyan]Sections included:[/cyan] {len(section_names)}")
    for name in section_names:
        console.print(f"  • {name}")

    console.print("\n[dim]Use the 'validate' command to check document compliance:[/dim]")
    console.print("[dim]  ccdakit validate <filename>[/dim]")
    console.print("=" * 60 + "\n")
