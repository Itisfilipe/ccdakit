"""Example of creating a Plan of Treatment Section.

This example demonstrates how to create a comprehensive Plan of Treatment Section
with multiple types of planned activities including:
- Planned observations (lab tests)
- Planned procedures
- Planned encounters (follow-up visits)
- Planned acts (patient education)
- Planned medications
- Planned supplies (medical equipment)
- Planned immunizations
- Instructions
"""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.plan_of_treatment import PlanOfTreatmentSection
from ccdakit.core.base import CDAVersion


# Mock data classes that satisfy the protocol requirements


class PersistentID:
    """Persistent identifier for tracking across document versions."""

    def __init__(self, root: str, extension: str):
        self._root = root
        self._extension = extension

    @property
    def root(self) -> str:
        return self._root

    @property
    def extension(self) -> str:
        return self._extension


class PlannedObservation:
    """Planned observation (e.g., lab test) for treatment plan."""

    def __init__(
        self,
        description: str,
        code: str,
        code_system: str,
        planned_date: date,
        status: str = "active",
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._persistent_id = persistent_id

    @property
    def description(self) -> str:
        return self._description

    @property
    def code(self) -> str:
        return self._code

    @property
    def code_system(self) -> str:
        return self._code_system

    @property
    def planned_date(self) -> date:
        return self._planned_date

    @property
    def status(self) -> str:
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class PlannedProcedure:
    """Planned procedure for treatment plan."""

    def __init__(
        self,
        description: str,
        code: str,
        code_system: str,
        planned_date: date,
        body_site: str = None,
        status: str = "active",
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._body_site = body_site
        self._status = status
        self._persistent_id = persistent_id

    @property
    def description(self) -> str:
        return self._description

    @property
    def code(self) -> str:
        return self._code

    @property
    def code_system(self) -> str:
        return self._code_system

    @property
    def planned_date(self) -> date:
        return self._planned_date

    @property
    def body_site(self) -> str:
        return self._body_site

    @property
    def status(self) -> str:
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class PlannedEncounter:
    """Planned encounter (e.g., office visit) for treatment plan."""

    def __init__(
        self,
        description: str,
        code: str,
        code_system: str,
        planned_date: date,
        encounter_type: str = None,
        status: str = "active",
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._encounter_type = encounter_type
        self._status = status
        self._persistent_id = persistent_id

    @property
    def description(self) -> str:
        return self._description

    @property
    def code(self) -> str:
        return self._code

    @property
    def code_system(self) -> str:
        return self._code_system

    @property
    def planned_date(self) -> date:
        return self._planned_date

    @property
    def encounter_type(self) -> str:
        return self._encounter_type

    @property
    def status(self) -> str:
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class PlannedAct:
    """Planned act (e.g., patient education) for treatment plan."""

    def __init__(
        self,
        description: str,
        code: str,
        code_system: str,
        planned_date: date,
        status: str = "active",
        mood_code: str = "INT",
        id_root: str = "2.16.840.1.113883.19.5.99999.1",
        id_extension: str = None,
        instructions: str = None,
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._mood_code = mood_code
        self._id_root = id_root
        self._id_extension = id_extension or f"ACT-{id(self)}"
        self._instructions = instructions
        self._persistent_id = persistent_id

    @property
    def description(self) -> str:
        return self._description

    @property
    def display_name(self) -> str:
        """Alias for description to match PlannedActProtocol."""
        return self._description

    @property
    def code(self) -> str:
        return self._code

    @property
    def code_system(self) -> str:
        return self._code_system

    @property
    def planned_date(self) -> date:
        return self._planned_date

    @property
    def effective_time(self) -> date:
        """Alias for planned_date to match PlannedActProtocol."""
        return self._planned_date

    @property
    def status(self) -> str:
        return self._status

    @property
    def mood_code(self) -> str:
        return self._mood_code

    @property
    def id_root(self) -> str:
        return self._id_root

    @property
    def id_extension(self) -> str:
        return self._id_extension

    @property
    def instructions(self) -> str:
        return self._instructions

    @property
    def persistent_id(self):
        return self._persistent_id


class PlannedMedication:
    """Planned medication for treatment plan."""

    def __init__(
        self,
        description: str,
        code: str,
        code_system: str,
        planned_date: date,
        dose: str = None,
        route: str = None,
        frequency: str = None,
        status: str = "active",
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._dose = dose
        self._route = route
        self._frequency = frequency
        self._status = status
        self._persistent_id = persistent_id

    @property
    def description(self) -> str:
        return self._description

    @property
    def code(self) -> str:
        return self._code

    @property
    def code_system(self) -> str:
        return self._code_system

    @property
    def planned_date(self) -> date:
        return self._planned_date

    @property
    def dose(self) -> str:
        return self._dose

    @property
    def route(self) -> str:
        return self._route

    @property
    def frequency(self) -> str:
        return self._frequency

    @property
    def status(self) -> str:
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class PlannedSupply:
    """Planned supply (e.g., medical equipment) for treatment plan."""

    def __init__(
        self,
        description: str,
        code: str,
        code_system: str,
        planned_date: date,
        quantity: str = None,
        status: str = "active",
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._quantity = quantity
        self._status = status
        self._persistent_id = persistent_id

    @property
    def description(self) -> str:
        return self._description

    @property
    def code(self) -> str:
        return self._code

    @property
    def code_system(self) -> str:
        return self._code_system

    @property
    def planned_date(self) -> date:
        return self._planned_date

    @property
    def quantity(self) -> str:
        return self._quantity

    @property
    def status(self) -> str:
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class PlannedImmunization:
    """Planned immunization for treatment plan."""

    def __init__(
        self,
        description: str,
        code: str,
        code_system: str,
        vaccine_code: str,
        planned_date: date,
        status: str = "active",
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._vaccine_code = vaccine_code
        self._planned_date = planned_date
        self._status = status
        self._persistent_id = persistent_id

    @property
    def description(self) -> str:
        return self._description

    @property
    def code(self) -> str:
        return self._code

    @property
    def code_system(self) -> str:
        return self._code_system

    @property
    def vaccine_code(self) -> str:
        return self._vaccine_code

    @property
    def planned_date(self) -> date:
        return self._planned_date

    @property
    def status(self) -> str:
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class Instruction:
    """Instruction for treatment plan."""

    def __init__(self, instruction_text: str, persistent_id=None):
        self._instruction_text = instruction_text
        self._persistent_id = persistent_id

    @property
    def instruction_text(self) -> str:
        return self._instruction_text

    @property
    def persistent_id(self):
        return self._persistent_id


def main():
    """Create and display a comprehensive Plan of Treatment Section example."""

    # Create planned observations (lab tests)
    hba1c_test = PlannedObservation(
        description="Hemoglobin A1c test",
        code="4548-4",
        code_system="LOINC",
        planned_date=date(2024, 12, 15),
        status="active",
        persistent_id=PersistentID("2.16.840.1.113883.19.5.99999.1", "OBS-HBA1C-001"),
    )

    lipid_panel = PlannedObservation(
        description="Lipid panel",
        code="24331-1",
        code_system="LOINC",
        planned_date=date(2024, 12, 22),
        status="active",
    )

    # Create planned procedure
    colonoscopy = PlannedProcedure(
        description="Colonoscopy screening",
        code="73761001",
        code_system="SNOMED",
        planned_date=date(2025, 3, 10),
        body_site="Colon",
        status="active",
    )

    # Create planned encounter
    follow_up_visit = PlannedEncounter(
        description="Follow-up visit for diabetes management",
        code="99213",
        code_system="CPT",
        planned_date=date(2024, 12, 30),
        encounter_type="Office Visit",
        status="active",
    )

    annual_physical = PlannedEncounter(
        description="Annual physical examination",
        code="99385",
        code_system="CPT",
        planned_date=date(2025, 6, 15),
        encounter_type="Preventive Visit",
        status="active",
    )

    # Create planned act
    diabetes_education = PlannedAct(
        description="Diabetes self-management education",
        code="385800002",
        code_system="SNOMED",
        planned_date=date(2025, 1, 5),
        status="active",
    )

    # Create planned medication
    metformin = PlannedMedication(
        description="Metformin 500mg",
        code="860975",
        code_system="RxNorm",
        planned_date=date(2024, 11, 25),
        dose="500",
        route="Oral",
        frequency="Twice daily with meals",
        status="active",
    )

    lisinopril = PlannedMedication(
        description="Lisinopril 10mg for blood pressure",
        code="314076",
        code_system="RxNorm",
        planned_date=date(2024, 11, 25),
        dose="10",
        route="Oral",
        frequency="Once daily",
        status="active",
    )

    # Create planned supply
    glucose_meter = PlannedSupply(
        description="Blood glucose meter with test strips",
        code="43252007",
        code_system="SNOMED",
        planned_date=date(2024, 12, 5),
        quantity="1",
        status="active",
    )

    # Create planned immunization
    flu_vaccine = PlannedImmunization(
        description="Influenza vaccine (seasonal)",
        code="141",
        code_system="CVX",
        vaccine_code="141",
        planned_date=date(2024, 11, 28),
        status="active",
    )

    pneumococcal_vaccine = PlannedImmunization(
        description="Pneumococcal conjugate vaccine",
        code="33",
        code_system="CVX",
        vaccine_code="33",
        planned_date=date(2025, 1, 15),
        status="active",
    )

    # Create instructions
    glucose_monitoring = Instruction(
        instruction_text="Monitor blood glucose levels daily before meals and at bedtime"
    )

    medication_timing = Instruction(
        instruction_text="Take metformin with food to reduce gastrointestinal side effects"
    )

    diet_instruction = Instruction(
        instruction_text="Follow low-carbohydrate diet plan provided by nutritionist"
    )

    # Create the Plan of Treatment Section with all planned activities
    section = PlanOfTreatmentSection(
        planned_observations=[hba1c_test, lipid_panel],
        planned_procedures=[colonoscopy],
        planned_encounters=[follow_up_visit, annual_physical],
        planned_acts=[diabetes_education],
        planned_medications=[metformin, lisinopril],
        planned_supplies=[glucose_meter],
        planned_immunizations=[flu_vaccine, pneumococcal_vaccine],
        instructions=[glucose_monitoring, medication_timing, diet_instruction],
        title="Comprehensive Treatment Plan",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Plan of Treatment Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show summary info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.10")
    print("  - Extension: 2014-06-09")
    print("  - Section Code: 18776-5 (LOINC)")
    print("\nPlanned Activities Breakdown:")
    print("  - Observations (lab tests): 2")
    print("  - Procedures: 1")
    print("  - Encounters: 2")
    print("  - Acts (education): 1")
    print("  - Medications: 2")
    print("  - Supplies: 1")
    print("  - Immunizations: 2")
    print("  - Instructions: 3")
    print("  - Total entries: 14")

    print("\nConformance Points:")
    print("  - CONF:1098-7723: Template ID for Plan of Treatment Section V2")
    print("  - CONF:1098-32501: Extension 2014-06-09 for R2.1")
    print("  - CONF:1098-14749: Code SHALL be 18776-5 (LOINC)")
    print("  - CONF:1098-16986: Title element present")
    print("  - CONF:1098-7725: Narrative text with table present")
    print("  - CONF:1098-7726: Planned Observation entries (moodCode=INT)")
    print("  - CONF:1098-8809: Planned Procedure entries")
    print("  - CONF:1098-8805: Planned Encounter entries")
    print("  - CONF:1098-8811: Planned Medication entries")
    print("  - CONF:1098-32353: Planned Immunization entries")

    print("\nUse Cases Demonstrated:")
    print("  1. Diabetes management with medications and monitoring")
    print("  2. Preventive care (colonoscopy, annual physical)")
    print("  3. Patient education and self-management")
    print("  4. Immunization planning")
    print("  5. Medical equipment supply")
    print("  6. Multiple instruction types")

    print("\nPersistent IDs:")
    print("  - HbA1c test has persistent ID for tracking across document versions")
    print("  - Other activities use auto-generated IDs")

    print("\n" + "=" * 80)
    print("\nThis example demonstrates a comprehensive treatment plan for a patient")
    print("with diabetes, including lab monitoring, medications, preventive care,")
    print("patient education, and necessary medical supplies.")


if __name__ == "__main__":
    main()
