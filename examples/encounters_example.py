"""Example of creating an Encounters Section."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.sections.encounters import EncountersSection
from ccdakit.core.base import CDAVersion


class ExampleEncounter:
    """Example encounter for demonstration."""

    def __init__(
        self,
        encounter_type,
        code,
        code_system,
        date_value,
        end_date=None,
        location=None,
        performer_name=None,
        discharge_disposition=None,
    ):
        self._encounter_type = encounter_type
        self._code = code
        self._code_system = code_system
        self._date = date_value
        self._end_date = end_date
        self._location = location
        self._performer_name = performer_name
        self._discharge_disposition = discharge_disposition

    @property
    def encounter_type(self):
        return self._encounter_type

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def date(self):
        return self._date

    @property
    def end_date(self):
        return self._end_date

    @property
    def location(self):
        return self._location

    @property
    def performer_name(self):
        return self._performer_name

    @property
    def discharge_disposition(self):
        return self._discharge_disposition


def main():
    """Create and display an Encounters Section example."""

    # Create sample encounters
    # 1. Routine office visit
    office_visit = ExampleEncounter(
        encounter_type="Office Visit",
        code="99213",
        code_system="CPT-4",
        date_value=date(2023, 3, 10),
        location="Primary Care Clinic",
        performer_name="Dr. Jane Smith",
    )

    # 2. Emergency department visit (with time range)
    emergency_visit = ExampleEncounter(
        encounter_type="Emergency Department Visit",
        code="99285",
        code_system="CPT-4",
        date_value=datetime(2023, 5, 15, 2, 30),
        end_date=datetime(2023, 5, 15, 7, 15),
        location="County General Emergency Department",
        performer_name="Dr. Michael Wilson",
    )

    # 3. Inpatient hospital admission (multi-day stay)
    hospital_admission = ExampleEncounter(
        encounter_type="Inpatient Hospital Admission",
        code="32485007",
        code_system="SNOMED CT",
        date_value=date(2023, 6, 20),
        end_date=date(2023, 6, 25),
        location="Memorial Hospital",
        performer_name="Dr. Robert Johnson",
        discharge_disposition="Home",
    )

    # Create the Encounters Section
    section = EncountersSection(
        encounters=[office_visit, emergency_visit, hospital_admission],
        title="Patient Encounters",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Encounters Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.22.1")
    print("  - Extension: 2015-08-01")
    print("  - Section Code: 46240-8 (Encounters)")
    print("  - Number of encounters: 3")
    print("\nEncounter Types:")
    print("  1. Office Visit (CPT-4: 99213)")
    print("     - Single date: 2023-03-10")
    print("     - Location: Primary Care Clinic")
    print("     - Performer: Dr. Jane Smith")
    print("\n  2. Emergency Department Visit (CPT-4: 99285)")
    print("     - Date range: 2023-05-15 02:30 to 07:15")
    print("     - Location: County General Emergency Department")
    print("     - Performer: Dr. Michael Wilson")
    print("\n  3. Inpatient Hospital Admission (SNOMED CT: 32485007)")
    print("     - Date range: 2023-06-20 to 2023-06-25")
    print("     - Location: Memorial Hospital")
    print("     - Performer: Dr. Robert Johnson")
    print("     - Discharge: Home")
    print("\nConformance:")
    print("  - CONF:1198-7879: Template ID present")
    print("  - CONF:1198-7881: Code 46240-8 (Encounters)")
    print("  - CONF:1198-7882: Title present")
    print("  - CONF:1198-7883: Narrative text present")
    print("  - CONF:1198-7884: Encounter Activity entries present")


if __name__ == "__main__":
    main()
