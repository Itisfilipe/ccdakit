"""List all available protocol definitions (data models)."""

import inspect
import sys
from typing import Optional, get_type_hints

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def list_protocols_command(
    protocol_name: Optional[str] = None,
    verbose: bool = False,
) -> None:
    """
    List all available protocol definitions (typed data models).

    Args:
        protocol_name: Specific protocol to show details for
        verbose: Show field types and descriptions
    """
    import ccdakit.protocols as protocols_module

    console.print("\n[bold cyan]Available Protocol Definitions[/bold cyan]\n")

    # Get all protocol classes
    protocol_classes = {}
    for name in dir(protocols_module):
        if not name.startswith("_"):
            obj = getattr(protocols_module, name)
            if inspect.isclass(obj) and hasattr(obj, "__annotations__"):
                protocol_classes[name] = obj

    if not protocol_classes:
        console.print("[yellow]No protocol definitions found[/yellow]")
        return

    # If specific protocol requested
    if protocol_name:
        if protocol_name not in protocol_classes:
            console.print(f"[red]Protocol '{protocol_name}' not found[/red]")
            console.print("\n[yellow]Available protocols:[/yellow]")
            for p in sorted(protocol_classes.keys()):
                console.print(f"  • {p}")
            sys.exit(1)

        # Show protocol details
        protocol_class = protocol_classes[protocol_name]
        console.print(f"[bold cyan]Protocol:[/bold cyan] {protocol_name}\n")

        # Get annotations (field definitions)
        try:
            type_hints = get_type_hints(protocol_class)
        except Exception:
            type_hints = getattr(protocol_class, "__annotations__", {})

        if type_hints:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Field", style="cyan")
            table.add_column("Type", style="yellow")

            if verbose:
                table.add_column("Required", style="green")

            for field_name, field_type in type_hints.items():
                type_str = str(field_type).replace("typing.", "")

                if verbose:
                    # Check if Optional
                    is_optional = "Optional" in type_str or "None" in type_str
                    required = "No" if is_optional else "Yes"
                    table.add_row(field_name, type_str, required)
                else:
                    table.add_row(field_name, type_str)

            console.print(table)
        else:
            console.print("[yellow]No fields defined for this protocol[/yellow]")

        # Show docstring
        if protocol_class.__doc__:
            console.print(f"\n[bold]Description:[/bold]")
            console.print(Panel(protocol_class.__doc__.strip(), border_style="dim"))

        # Show example usage
        console.print("\n[bold]Example Usage:[/bold]")
        example = f"""from ccdakit.protocols import {protocol_name}

# Create instance
data: {protocol_name} = {{
    # Add required fields here
}}"""
        console.print(Panel(example, border_style="cyan"))

    else:
        # List all protocols by category
        categories = {
            "Core Clinical": [
                "PatientProtocol", "ProblemProtocol", "MedicationProtocol",
                "AllergyProtocol", "ImmunizationProtocol", "VitalSignsProtocol",
                "ProcedureProtocol", "ResultProtocol", "EncounterProtocol",
                "SocialHistoryProtocol"
            ],
            "Extended Clinical": [
                "FamilyHistoryProtocol", "FunctionalStatusProtocol",
                "MentalStatusProtocol", "GoalProtocol", "HealthConcernProtocol",
                "HealthStatusEvaluationProtocol", "PhysicalExamProtocol",
                "AssessmentAndPlanProtocol"
            ],
            "Specialized": [
                "PlanOfTreatmentProtocol", "AdvanceDirectiveProtocol",
                "MedicalEquipmentProtocol", "NutritionProtocol",
                "PayerProtocol", "InterventionProtocol", "InstructionProtocol"
            ],
            "Hospital/Surgical": [
                "AdmissionDiagnosisProtocol", "DischargeDiagnosisProtocol",
                "HospitalCourseProtocol", "AnesthesiaProtocol",
                "PreoperativeDiagnosisProtocol", "PostoperativeDiagnosisProtocol",
                "ComplicationProtocol", "DischargeStudiesProtocol",
                "MedicationsAdministeredProtocol"
            ],
            "Administrative": [
                "AuthorProtocol", "OrganizationProtocol", "AddressProtocol",
                "TelecomProtocol"
            ]
        }

        for category_name, protocol_list in categories.items():
            # Filter to only show protocols that exist
            existing = [p for p in protocol_list if p in protocol_classes]
            if not existing:
                continue

            table = Table(title=f"[bold]{category_name}[/bold]", show_header=True)
            table.add_column("Protocol Name", style="cyan")

            if verbose:
                table.add_column("Fields", style="yellow")

            for protocol in sorted(existing):
                if verbose:
                    protocol_class = protocol_classes[protocol]
                    try:
                        type_hints = get_type_hints(protocol_class)
                    except Exception:
                        type_hints = getattr(protocol_class, "__annotations__", {})
                    field_count = len(type_hints)
                    table.add_row(protocol, str(field_count))
                else:
                    table.add_row(protocol)

            console.print(table)
            console.print(f"[dim]{len(existing)} protocols in this category[/dim]\n")

        console.print(f"[bold green]Total:[/bold green] {len(protocol_classes)} protocols available")
        console.print("\n[dim]Tip: Specify protocol name to see field definitions[/dim]")
        console.print("[dim]Example: ccdakit list-protocols PatientProtocol[/dim]\n")
