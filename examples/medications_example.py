"""Example of creating a Medications Section."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.medications import MedicationsSection
from ccdakit.core.base import CDAVersion


# Define medication data class
class ExampleMedication:
    """Example medication that satisfies MedicationProtocol."""

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
    """Create and display a Medications Section example."""

    # Create sample medications
    # Medication 1: Active blood pressure medication
    lisinopril = ExampleMedication(
        name="Lisinopril 10mg oral tablet",
        code="314076",
        dosage="10 mg",
        route="oral",
        frequency="once daily",
        start_date=date(2023, 1, 15),
        status="active",
        instructions="Take one tablet by mouth every morning",
    )

    # Medication 2: Active diabetes medication
    metformin = ExampleMedication(
        name="Metformin 500mg oral tablet",
        code="860975",
        dosage="500 mg",
        route="oral",
        frequency="twice daily",
        start_date=date(2023, 2, 20),
        status="active",
        instructions="Take one tablet by mouth with breakfast and dinner",
    )

    # Medication 3: Completed antibiotic course
    amoxicillin = ExampleMedication(
        name="Amoxicillin 500mg oral capsule",
        code="308191",
        dosage="500 mg",
        route="oral",
        frequency="three times daily",
        start_date=date(2023, 11, 1),
        end_date=date(2023, 11, 14),
        status="completed",
        instructions="Take one capsule by mouth three times daily with food",
    )

    # Create the Medications Section
    section = MedicationsSection(
        medications=[lisinopril, metformin, amoxicillin],
        title="Current and Recent Medications",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Medications Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.1.1")
    print("  - Extension: 2015-08-01")
    print("  - Number of medications: 3")
    print("    - Active: 2 (Lisinopril, Metformin)")
    print("    - Completed: 1 (Amoxicillin)")
    print("\nMedication Details:")
    print("  1. Lisinopril 10mg oral tablet")
    print("     - RxNorm Code: 314076")
    print("     - Dosage: 10 mg once daily")
    print("     - Status: Active since 2023-01-15")
    print("\n  2. Metformin 500mg oral tablet")
    print("     - RxNorm Code: 860975")
    print("     - Dosage: 500 mg twice daily")
    print("     - Status: Active since 2023-02-20")
    print("\n  3. Amoxicillin 500mg oral capsule")
    print("     - RxNorm Code: 308191")
    print("     - Dosage: 500 mg three times daily")
    print("     - Status: Completed (2023-11-01 to 2023-11-14)")
    print("\nConformance:")
    print("  - CONF:1098-7572: Template ID present")
    print("  - CONF:1098-7573: Code 10160-0 (History of medication use)")
    print("  - CONF:1098-7574: Title present")
    print("  - CONF:1098-7575: Narrative text with medication table present")
    print("  - CONF:1098-7576: Medication Activity entries present")
    print("\nUsage:")
    print("  This example demonstrates how to create a Medications Section with:")
    print("  - Active medications with ongoing treatment")
    print("  - Completed medications with end dates")
    print("  - Patient instructions for each medication")
    print("  - RxNorm codes for standardized drug identification")


if __name__ == "__main__":
    main()
