"""CLI command for listing available C-CDA sections."""

import logging
from typing import Optional

from rich.console import Console
from rich.table import Table


logger = logging.getLogger(__name__)
console = Console()


def list_sections_command(category: Optional[str] = None, verbose: bool = False) -> None:
    """List all available C-CDA section builders.

    Args:
        category: Filter by category (core, extended, specialized, hospital)
        verbose: Show additional details like template IDs and OIDs
    """
    # Categorize sections
    section_categories = {
        "core": [
            ("ProblemsSection", "Problems", "2.16.840.1.113883.10.20.22.2.5.1"),
            ("MedicationsSection", "Medications", "2.16.840.1.113883.10.20.22.2.1.1"),
            ("AllergiesSection", "Allergies and Intolerances", "2.16.840.1.113883.10.20.22.2.6.1"),
            ("ImmunizationsSection", "Immunizations", "2.16.840.1.113883.10.20.22.2.2.1"),
            ("VitalSignsSection", "Vital Signs", "2.16.840.1.113883.10.20.22.2.4.1"),
            ("ProceduresSection", "Procedures", "2.16.840.1.113883.10.20.22.2.7.1"),
            ("ResultsSection", "Results", "2.16.840.1.113883.10.20.22.2.3.1"),
            ("SocialHistorySection", "Social History", "2.16.840.1.113883.10.20.22.2.17"),
            ("EncountersSection", "Encounters", "2.16.840.1.113883.10.20.22.2.22.1"),
        ],
        "extended": [
            ("FamilyHistorySection", "Family History", "2.16.840.1.113883.10.20.22.2.15"),
            ("FunctionalStatusSection", "Functional Status", "2.16.840.1.113883.10.20.22.2.14"),
            ("MentalStatusSection", "Mental Status", "2.16.840.1.113883.10.20.22.2.56"),
            ("GoalsSection", "Goals", "2.16.840.1.113883.10.20.22.2.60"),
            ("HealthConcernsSection", "Health Concerns", "2.16.840.1.113883.10.20.22.2.58"),
            ("HealthStatusEvaluationsSection", "Health Status Evaluations and Outcomes", "2.16.840.1.113883.10.20.22.2.61"),
            ("PastMedicalHistorySection", "Past Medical History", "2.16.840.1.113883.10.20.22.2.20"),
            ("PhysicalExamSection", "Physical Exam", "2.16.840.1.113883.10.20.2.10"),
            ("AssessmentAndPlanSection", "Assessment and Plan", "2.16.840.1.113883.10.20.22.2.9"),
        ],
        "specialized": [
            ("PlanOfTreatmentSection", "Plan of Treatment", "2.16.840.1.113883.10.20.22.2.10"),
            ("AdvanceDirectivesSection", "Advance Directives", "2.16.840.1.113883.10.20.22.2.21.1"),
            ("MedicalEquipmentSection", "Medical Equipment", "2.16.840.1.113883.10.20.22.2.23"),
            ("AdmissionMedicationsSection", "Admission Medications", "2.16.840.1.113883.10.20.22.2.44"),
            ("DischargeMedicationsSection", "Discharge Medications", "2.16.840.1.113883.10.20.22.2.11.1"),
            ("HospitalDischargeInstructionsSection", "Hospital Discharge Instructions", "2.16.840.1.113883.10.20.22.2.41"),
            ("PayersSection", "Payers", "2.16.840.1.113883.10.20.22.2.18"),
            ("NutritionSection", "Nutrition", "2.16.840.1.113883.10.20.22.2.57"),
            ("ReasonForVisitSection", "Reason for Visit", "2.16.840.1.113883.10.20.22.2.12"),
            ("ChiefComplaintAndReasonForVisitSection", "Chief Complaint and Reason for Visit", "2.16.840.1.113883.10.20.22.2.13"),
            ("InterventionsSection", "Interventions", "2.16.840.1.113883.10.20.21.2.3"),
        ],
        "hospital": [
            ("AdmissionDiagnosisSection", "Admission Diagnosis", "2.16.840.1.113883.10.20.22.2.43"),
            ("DischargeDiagnosisSection", "Discharge Diagnosis", "2.16.840.1.113883.10.20.22.2.24"),
            ("HospitalCourseSection", "Hospital Course", "2.16.840.1.113883.10.20.22.2.38"),
            ("InstructionsSection", "Instructions", "2.16.840.1.113883.10.20.22.2.45"),
            ("AnesthesiaSection", "Anesthesia", "2.16.840.1.113883.10.20.22.2.25"),
            ("PostoperativeDiagnosisSection", "Postoperative Diagnosis", "2.16.840.1.113883.10.20.22.2.35"),
            ("PreoperativeDiagnosisSection", "Preoperative Diagnosis", "2.16.840.1.113883.10.20.22.2.34"),
            ("ComplicationsSection", "Complications", "2.16.840.1.113883.10.20.22.2.37"),
            ("HospitalDischargeStudiesSummarySection", "Hospital Discharge Studies Summary", "2.16.840.1.113883.10.20.22.2.16"),
            ("MedicationsAdministeredSection", "Medications Administered", "2.16.840.1.113883.10.20.22.2.38"),
        ],
    }

    # Filter by category if specified
    if category:
        if category.lower() not in section_categories:
            console.print(f"[red]Error:[/red] Unknown category: {category}")
            console.print(f"Available categories: {', '.join(section_categories.keys())}")
            return
        categories_to_show = {category.lower(): section_categories[category.lower()]}
    else:
        categories_to_show = section_categories

    # Display sections
    for cat_name, sections_list in categories_to_show.items():
        # Create table
        table = Table(title=f"{cat_name.title()} Sections ({len(sections_list)} sections)")
        table.add_column("Class Name", style="cyan", no_wrap=True)
        table.add_column("Display Name", style="green")
        if verbose:
            table.add_column("Template ID", style="yellow")

        for class_name, display_name, template_id in sections_list:
            if verbose:
                table.add_row(class_name, display_name, template_id)
            else:
                table.add_row(class_name, display_name)

        console.print(table)
        console.print()

    # Summary
    total_sections = sum(len(sections_list) for sections_list in categories_to_show.values())
    console.print(f"[bold]Total:[/bold] {total_sections} sections available")
    console.print("\n[dim]Use --verbose to see template IDs and additional details[/dim]")
