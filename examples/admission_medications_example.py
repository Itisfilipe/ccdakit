"""Example of creating an Admission Medications Section."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.admission_medications import AdmissionMedicationsSection
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
    """Create and display an Admission Medications Section example."""

    # Create sample medications patient was taking at time of hospital admission
    # Medication 1: Blood pressure medication
    lisinopril = ExampleMedication(
        name="Lisinopril 10mg oral tablet",
        code="314076",
        dosage="10 mg",
        route="oral",
        frequency="once daily",
        start_date=date(2022, 6, 15),
        status="active",
        instructions="Take one tablet by mouth every morning for blood pressure",
    )

    # Medication 2: Diabetes medication
    metformin = ExampleMedication(
        name="Metformin 500mg oral tablet",
        code="860975",
        dosage="500 mg",
        route="oral",
        frequency="twice daily",
        start_date=date(2022, 8, 10),
        status="active",
        instructions="Take one tablet by mouth with breakfast and dinner",
    )

    # Medication 3: Cholesterol medication
    atorvastatin = ExampleMedication(
        name="Atorvastatin 20mg oral tablet",
        code="617310",
        dosage="20 mg",
        route="oral",
        frequency="once daily at bedtime",
        start_date=date(2023, 1, 5),
        status="active",
        instructions="Take one tablet by mouth at bedtime",
    )

    # Create the Admission Medications Section
    section = AdmissionMedicationsSection(
        medications=[lisinopril, metformin, atorvastatin],
        title="Medications on Admission",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Admission Medications Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.44")
    print("  - Extension: 2015-08-01")
    print("  - Number of admission medications: 3")
    print("    - All medications were active at time of admission")
    print("\nMedication Details:")
    print("  1. Lisinopril 10mg oral tablet")
    print("     - RxNorm Code: 314076")
    print("     - Dosage: 10 mg once daily")
    print("     - Started: 2022-06-15 (Blood pressure medication)")
    print("     - Status: Active at admission")
    print("\n  2. Metformin 500mg oral tablet")
    print("     - RxNorm Code: 860975")
    print("     - Dosage: 500 mg twice daily")
    print("     - Started: 2022-08-10 (Diabetes medication)")
    print("     - Status: Active at admission")
    print("\n  3. Atorvastatin 20mg oral tablet")
    print("     - RxNorm Code: 617310")
    print("     - Dosage: 20 mg once daily at bedtime")
    print("     - Started: 2023-01-05 (Cholesterol medication)")
    print("     - Status: Active at admission")
    print("\nConformance:")
    print("  - CONF:1198-10098: Template ID present")
    print("  - CONF:1198-15482: Code 42346-7 (Medications on Admission)")
    print("  - CONF:1198-10100: Title present")
    print("  - CONF:1198-10101: Narrative text with medication table present")
    print("  - CONF:1198-10102: Admission Medication entries present (SHOULD)")
    print("\nSection Purpose:")
    print("  The Admission Medications Section contains the medications the patient")
    print("  was taking prior to and at the time of admission to the facility.")
    print("\nUsage:")
    print("  This example demonstrates how to create an Admission Medications Section")
    print("  documenting medications a patient was taking at hospital admission:")
    print("  - Chronic medications for ongoing conditions")
    print("  - RxNorm codes for standardized drug identification")
    print("  - Patient instructions for proper medication use")
    print(
        "  - All medications wrapped in Admission Medication Act (template 2.16.840.1.113883.10.20.22.4.36)"
    )


if __name__ == "__main__":
    main()
