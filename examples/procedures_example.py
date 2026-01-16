"""Example of creating a Procedures Section."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.sections.procedures import ProceduresSection
from ccdakit.core.base import CDAVersion


# Define mock procedure data
class ExampleProcedure:
    """Example procedure for demonstration."""

    def __init__(
        self,
        name,
        code,
        code_system,
        date_performed,
        status="completed",
        target_site=None,
        target_site_code=None,
        performer_name=None,
        performer_address=None,
        performer_telecom=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._date = date_performed
        self._status = status
        self._target_site = target_site
        self._target_site_code = target_site_code
        self._performer_name = performer_name
        self._performer_address = performer_address
        self._performer_telecom = performer_telecom

    @property
    def name(self):
        return self._name

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
    def status(self):
        return self._status

    @property
    def target_site(self):
        return self._target_site

    @property
    def target_site_code(self):
        return self._target_site_code

    @property
    def performer_name(self):
        return self._performer_name

    @property
    def performer_address(self):
        return self._performer_address

    @property
    def performer_telecom(self):
        return self._performer_telecom


def main():
    """Create and display a Procedures Section example."""

    # Create sample procedures
    procedures = [
        ExampleProcedure(
            name="Appendectomy",
            code="80146002",
            code_system="SNOMED CT",
            date_performed=date(2023, 3, 15),
            status="completed",
            target_site="Abdomen",
            target_site_code="818983003",
            performer_name="Dr. Sarah Johnson",
            performer_address="456 Surgical Center Dr, Medical City, ST 12345",
            performer_telecom="tel:+1-555-123-4567",
        ),
        ExampleProcedure(
            name="Colonoscopy",
            code="73761001",
            code_system="SNOMED CT",
            date_performed=datetime(2023, 6, 20, 10, 30),
            status="completed",
            target_site="Colon",
            target_site_code="71854001",
            performer_name="Dr. Michael Chen",
            performer_address="789 Endoscopy Suite, Diagnostic Hospital, ST 54321",
            performer_telecom="tel:+1-555-987-6543",
        ),
        ExampleProcedure(
            name="Total Hip Replacement",
            code="52734007",
            code_system="SNOMED CT",
            date_performed=date(2022, 11, 8),
            status="completed",
            target_site="Left hip",
            target_site_code="287579007",
            performer_name="Dr. Emily Rodriguez",
            performer_address="123 Orthopedic Center, Surgical Hospital, ST 67890",
            performer_telecom="tel:+1-555-246-8135",
        ),
    ]

    # Create the Procedures Section
    section = ProceduresSection(
        procedures=procedures,
        title="Surgical and Diagnostic Procedures",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Procedures Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.7.1")
    print("  - Extension: 2014-06-09")
    print("  - Section Code: 47519-4 (History of Procedures)")
    print("  - Number of procedures: 3")
    print("\nProcedures included:")
    for idx, proc in enumerate(procedures, start=1):
        print(f"  {idx}. {proc.name}")
        print(f"     - Code: {proc.code} ({proc.code_system})")
        print(f"     - Date: {proc.date}")
        print(f"     - Status: {proc.status}")
        print(f"     - Target Site: {proc.target_site}")
        print(f"     - Performer: {proc.performer_name}")
    print("\nConformance:")
    print("  - CONF:1098-32533: Template ID with extension present")
    print("  - CONF:1098-15421: Section code 47519-4 (LOINC)")
    print("  - CONF:1098-15422: Title present")
    print("  - CONF:1098-15423: Narrative text present")
    print("  - CONF:1098-7891: Procedure Activity entries present")


if __name__ == "__main__":
    main()
