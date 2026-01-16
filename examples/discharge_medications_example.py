"""Example of creating a Discharge Medications Section."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.discharge_medications import DischargeMedicationsSection
from ccdakit.core.base import CDAVersion


# Define medication data class
class ExampleDischargeMedication:
    """Example discharge medication that satisfies MedicationProtocol."""

    def __init__(
        self,
        name,
        code,
        dosage,
        route,
        frequency,
        start_date,
        end_date=None,
        status="active",
        instructions=None,
        authors=None,
        code_system=None,
    ):
        self._name = name
        self._code = code
        self._dosage = dosage
        self._route = route
        self._frequency = frequency
        self._start_date = start_date
        self._end_date = end_date
        self._status = status
        self._instructions = instructions
        self._authors = authors
        self._code_system = code_system

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def dosage(self):
        return self._dosage

    @property
    def route(self):
        return self._route

    @property
    def frequency(self):
        return self._frequency

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def status(self):
        return self._status

    @property
    def instructions(self):
        return self._instructions

    @property
    def authors(self):
        return self._authors

    @property
    def code_system(self):
        return self._code_system


def main():
    """Create and display a Discharge Medications Section example."""

    # Create sample discharge medications
    # Medication 1: Continue existing blood pressure medication
    lisinopril = ExampleDischargeMedication(
        name="Lisinopril 10mg oral tablet",
        code="314076",
        dosage="10 mg",
        route="oral",
        frequency="once daily",
        start_date=date(2024, 1, 15),
        status="active",
        instructions="Continue taking one tablet by mouth every morning for blood pressure control",
    )

    # Medication 2: New diabetes medication started during hospitalization
    metformin = ExampleDischargeMedication(
        name="Metformin 500mg oral tablet",
        code="860975",
        dosage="500 mg",
        route="oral",
        frequency="twice daily",
        start_date=date(2024, 1, 10),
        status="active",
        instructions="Take one tablet by mouth with breakfast and dinner. Monitor blood sugar levels.",
    )

    # Medication 3: Short-term antibiotic prescribed at discharge
    amoxicillin = ExampleDischargeMedication(
        name="Amoxicillin 500mg oral capsule",
        code="308191",
        dosage="500 mg",
        route="oral",
        frequency="three times daily",
        start_date=date(2024, 1, 15),
        end_date=date(2024, 1, 25),
        status="active",
        instructions="Take one capsule by mouth three times daily with food. Complete full 10-day course.",
    )

    # Create the Discharge Medications Section
    section = DischargeMedicationsSection(
        medications=[lisinopril, metformin, amoxicillin],
        title="Discharge Medications",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Discharge Medications Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.11.1")
    print("  - Extension: 2015-08-01")
    print("  - Section Code: 10183-2 (Hospital Discharge Medications)")
    print("  - Number of medications: 3")
    print("    - Active ongoing: 2 (Lisinopril, Metformin)")
    print("    - Active with end date: 1 (Amoxicillin)")
    print("\nMedication Details:")
    print("  1. Lisinopril 10mg oral tablet")
    print("     - RxNorm Code: 314076")
    print("     - Dosage: 10 mg once daily")
    print("     - Status: Active since 2024-01-15")
    print("     - Indication: Blood pressure control")
    print("\n  2. Metformin 500mg oral tablet")
    print("     - RxNorm Code: 860975")
    print("     - Dosage: 500 mg twice daily")
    print("     - Status: Active since 2024-01-10")
    print("     - Note: Started during hospitalization")
    print("\n  3. Amoxicillin 500mg oral capsule")
    print("     - RxNorm Code: 308191")
    print("     - Dosage: 500 mg three times daily")
    print("     - Status: Active (2024-01-15 to 2024-01-25)")
    print("     - Duration: 10-day course")
    print("\nConformance:")
    print("  - CONF:1198-7822: Template ID present")
    print("  - CONF:1198-15361: Code 10183-2 (Hospital Discharge Medications)")
    print("  - CONF:1198-32857: Translation code 75311-1 (Discharge Medications)")
    print("  - CONF:1198-7824: Title present")
    print("  - CONF:1198-7825: Narrative text with medication table present")
    print("  - CONF:1198-7826: Discharge Medication entries present")
    print("\nKey Differences from General Medications Section:")
    print("  - Uses code 10183-2 instead of 10160-0")
    print("  - Includes translation code 75311-1")
    print("  - Entries use Discharge Medication template (2.16.840.1.113883.10.20.22.4.35)")
    print("  - Focuses on medications patient should take/stop after discharge")
    print("  - May include new prescriptions, continued medications, and discontinued ones")
    print("\nUsage:")
    print("  This example demonstrates how to create a Discharge Medications Section with:")
    print("  - Continued medications from before hospitalization")
    print("  - New medications started during hospital stay")
    print("  - Short-term medications with specific end dates")
    print("  - Detailed patient instructions for each medication")
    print("  - RxNorm codes for standardized drug identification")


if __name__ == "__main__":
    main()
