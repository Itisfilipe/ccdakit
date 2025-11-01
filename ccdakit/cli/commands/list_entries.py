"""List all available C-CDA entry builders."""

import sys
from typing import Optional

from rich.console import Console
from rich.table import Table

console = Console()


# Entry builder registry organized by category
ENTRY_BUILDERS = {
    "Allergies & Intolerances": [
        ("AllergyObservation", "ccdakit.builders.entries.allergy", "2.16.840.1.113883.10.20.22.4.7"),
    ],
    "Problems": [
        ("ProblemObservation", "ccdakit.builders.entries.problem", "2.16.840.1.113883.10.20.22.4.4"),
        ("ProblemConcernAct", "ccdakit.builders.entries.problem", "2.16.840.1.113883.10.20.22.4.3"),
    ],
    "Medications": [
        ("MedicationActivity", "ccdakit.builders.entries.medication", "2.16.840.1.113883.10.20.22.4.16"),
        ("AdmissionMedication", "ccdakit.builders.entries.admission_medication", "2.16.840.1.113883.10.20.22.4.36"),
        ("DischargeMedication", "ccdakit.builders.entries.discharge_medication", "2.16.840.1.113883.10.20.22.4.35"),
        ("MedicationAdministeredEntry", "ccdakit.builders.entries.medication_administered_entry", "2.16.840.1.113883.10.20.22.4.16"),
    ],
    "Immunizations": [
        ("ImmunizationActivity", "ccdakit.builders.entries.immunization", "2.16.840.1.113883.10.20.22.4.52"),
    ],
    "Vital Signs": [
        ("VitalSignsOrganizer", "ccdakit.builders.entries.vital_signs", "2.16.840.1.113883.10.20.22.4.26"),
        ("VitalSignObservation", "ccdakit.builders.entries.vital_signs", "2.16.840.1.113883.10.20.22.4.27"),
    ],
    "Procedures": [
        ("ProcedureActivityProcedure", "ccdakit.builders.entries.procedure", "2.16.840.1.113883.10.20.22.4.14"),
    ],
    "Results": [
        ("ResultOrganizer", "ccdakit.builders.entries.result", "2.16.840.1.113883.10.20.22.4.1"),
        ("ResultObservation", "ccdakit.builders.entries.result", "2.16.840.1.113883.10.20.22.4.2"),
    ],
    "Encounters": [
        ("EncounterActivity", "ccdakit.builders.entries.encounter", "2.16.840.1.113883.10.20.22.4.49"),
    ],
    "Social History": [
        ("SmokingStatusObservation", "ccdakit.builders.entries.smoking_status", "2.16.840.1.113883.10.20.22.4.78"),
    ],
    "Family History": [
        ("FamilyMemberHistory", "ccdakit.builders.entries.family_member_history", "2.16.840.1.113883.10.20.22.4.46"),
    ],
    "Functional Status": [
        ("FunctionalStatusObservation", "ccdakit.builders.entries.functional_status", "2.16.840.1.113883.10.20.22.4.67"),
    ],
    "Mental Status": [
        ("MentalStatusObservation", "ccdakit.builders.entries.mental_status", "2.16.840.1.113883.10.20.22.4.74"),
    ],
    "Goals": [
        ("GoalObservation", "ccdakit.builders.entries.goal", "2.16.840.1.113883.10.20.22.4.121"),
    ],
    "Health Concerns": [
        ("HealthConcernAct", "ccdakit.builders.entries.health_concern", "2.16.840.1.113883.10.20.22.4.132"),
    ],
    "Advance Directives": [
        ("AdvanceDirectiveObservation", "ccdakit.builders.entries.advance_directive", "2.16.840.1.113883.10.20.22.4.48"),
    ],
    "Medical Equipment": [
        ("NonMedicinalSupplyActivity", "ccdakit.builders.entries.medical_equipment", "2.16.840.1.113883.10.20.22.4.50"),
    ],
    "Nutrition": [
        ("NutritionAssessment", "ccdakit.builders.entries.nutrition_assessment", "2.16.840.1.113883.10.20.22.4.138"),
        ("NutritionalStatusObservation", "ccdakit.builders.entries.nutritional_status", "2.16.840.1.113883.10.20.22.4.124"),
    ],
    "Instructions": [
        ("Instruction", "ccdakit.builders.entries.instruction", "2.16.840.1.113883.10.20.22.4.20"),
    ],
    "Interventions": [
        ("InterventionAct", "ccdakit.builders.entries.intervention_act", "2.16.840.1.113883.10.20.22.4.131"),
    ],
    "Payers": [
        ("CoverageActivity", "ccdakit.builders.entries.coverage_activity", "2.16.840.1.113883.10.20.22.4.60"),
    ],
    "Physical Exam": [
        ("PhysicalExamObservation", "ccdakit.builders.entries.physical_exam", "2.16.840.1.113883.10.20.22.4.75"),
    ],
    "Admission/Discharge": [
        ("AdmissionDiagnosisEntry", "ccdakit.builders.entries.admission_diagnosis_entry", "2.16.840.1.113883.10.20.22.4.34"),
        ("DischargeDiagnosisEntry", "ccdakit.builders.entries.discharge_diagnosis_entry", "2.16.840.1.113883.10.20.22.4.33"),
    ],
    "Surgical": [
        ("AnesthesiaEntry", "ccdakit.builders.entries.anesthesia_entry", "2.16.840.1.113883.10.20.22.4.113"),
        ("PreoperativeDiagnosisEntry", "ccdakit.builders.entries.preoperative_diagnosis_entry", "2.16.840.1.113883.10.20.22.4.65"),
        ("ComplicationEntry", "ccdakit.builders.entries.complication_entry", "2.16.840.1.113883.10.20.22.4.77"),
    ],
    "Plan of Treatment": [
        ("PlannedAct", "ccdakit.builders.entries.planned_act", "2.16.840.1.113883.10.20.22.4.39"),
        ("PlannedEncounter", "ccdakit.builders.entries.planned_encounter", "2.16.840.1.113883.10.20.22.4.40"),
        ("PlannedImmunization", "ccdakit.builders.entries.planned_immunization", "2.16.840.1.113883.10.20.22.4.120"),
        ("PlannedInterventionAct", "ccdakit.builders.entries.planned_intervention_act", "2.16.840.1.113883.10.20.22.4.146"),
        ("PlannedMedication", "ccdakit.builders.entries.planned_medication", "2.16.840.1.113883.10.20.22.4.42"),
        ("PlannedObservation", "ccdakit.builders.entries.planned_observation", "2.16.840.1.113883.10.20.22.4.44"),
        ("PlannedProcedure", "ccdakit.builders.entries.planned_procedure", "2.16.840.1.113883.10.20.22.4.41"),
        ("PlannedSupply", "ccdakit.builders.entries.planned_supply", "2.16.840.1.113883.10.20.22.4.43"),
    ],
    "Assessment": [
        ("OutcomeObservation", "ccdakit.builders.entries.outcome_observation", "2.16.840.1.113883.10.20.22.4.144"),
        ("ProgressTowardGoalObservation", "ccdakit.builders.entries.progress_toward_goal", "2.16.840.1.113883.10.20.22.4.110"),
    ],
    "Common": [
        ("EntryReference", "ccdakit.builders.entries.entry_reference", "2.16.840.1.113883.10.20.22.4.122"),
    ],
}


def list_entries_command(
    category: Optional[str] = None,
    verbose: bool = False,
) -> None:
    """
    List all available C-CDA entry builders.

    Args:
        category: Filter by category (e.g., 'medications', 'problems', 'procedures')
        verbose: Show template IDs and module paths
    """
    console.print("\n[bold cyan]C-CDA Entry Builders[/bold cyan]\n")

    # Filter categories if specified
    if category:
        category_lower = category.lower()
        filtered = {k: v for k, v in ENTRY_BUILDERS.items() if category_lower in k.lower()}
        if not filtered:
            console.print(f"[red]Error:[/red] No entries found for category '{category}'")
            console.print("\n[yellow]Available categories:[/yellow]")
            for cat in ENTRY_BUILDERS.keys():
                console.print(f"  • {cat}")
            sys.exit(1)
        categories = filtered
    else:
        categories = ENTRY_BUILDERS

    # Display each category
    total_entries = 0
    for cat_name, entries in categories.items():
        table = Table(title=f"[bold]{cat_name}[/bold]", show_header=True)
        table.add_column("Class Name", style="cyan")
        if verbose:
            table.add_column("Module", style="dim")
            table.add_column("Template ID", style="yellow")

        for entry in entries:
            class_name = entry[0]
            if verbose:
                module = entry[1]
                template_id = entry[2]
                table.add_row(class_name, module, template_id)
            else:
                table.add_row(class_name)

        console.print(table)
        console.print(f"[dim]{len(entries)} entries in this category[/dim]\n")
        total_entries += len(entries)

    # Summary
    console.print(f"[bold green]Total:[/bold green] {total_entries} entry builders available")
    console.print(f"[dim]Categories: {len(categories)}[/dim]\n")

    # Usage hint
    if not verbose:
        console.print("[dim]Tip: Use --verbose to see module paths and template IDs[/dim]")
