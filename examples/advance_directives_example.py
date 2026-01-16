"""Example of creating an Advance Directives Section."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.advance_directives import AdvanceDirectivesSection
from ccdakit.core.base import CDAVersion


# Define advance directive data class
class ExampleAdvanceDirective:
    """Example advance directive for demonstration."""

    def __init__(
        self,
        directive_type,
        directive_type_code=None,
        directive_type_code_system=None,
        directive_value=None,
        directive_value_code=None,
        directive_value_code_system=None,
        start_date=None,
        end_date=None,
        custodian_name=None,
        custodian_relationship=None,
        custodian_relationship_code=None,
        custodian_phone=None,
        custodian_address=None,
        verifier_name=None,
        verification_date=None,
        document_id=None,
        document_url=None,
        document_description=None,
    ):
        self._directive_type = directive_type
        self._directive_type_code = directive_type_code
        self._directive_type_code_system = directive_type_code_system
        self._directive_value = directive_value
        self._directive_value_code = directive_value_code
        self._directive_value_code_system = directive_value_code_system
        self._start_date = start_date
        self._end_date = end_date
        self._custodian_name = custodian_name
        self._custodian_relationship = custodian_relationship
        self._custodian_relationship_code = custodian_relationship_code
        self._custodian_phone = custodian_phone
        self._custodian_address = custodian_address
        self._verifier_name = verifier_name
        self._verification_date = verification_date
        self._document_id = document_id
        self._document_url = document_url
        self._document_description = document_description

    @property
    def directive_type(self):
        return self._directive_type

    @property
    def directive_type_code(self):
        return self._directive_type_code

    @property
    def directive_type_code_system(self):
        return self._directive_type_code_system

    @property
    def directive_value(self):
        return self._directive_value

    @property
    def directive_value_code(self):
        return self._directive_value_code

    @property
    def directive_value_code_system(self):
        return self._directive_value_code_system

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def custodian_name(self):
        return self._custodian_name

    @property
    def custodian_relationship(self):
        return self._custodian_relationship

    @property
    def custodian_relationship_code(self):
        return self._custodian_relationship_code

    @property
    def custodian_phone(self):
        return self._custodian_phone

    @property
    def custodian_address(self):
        return self._custodian_address

    @property
    def verifier_name(self):
        return self._verifier_name

    @property
    def verification_date(self):
        return self._verification_date

    @property
    def document_id(self):
        return self._document_id

    @property
    def document_url(self):
        return self._document_url

    @property
    def document_description(self):
        return self._document_description


def main():
    """Create and display an Advance Directives Section example."""

    # Create advance directives with different types
    directive1 = ExampleAdvanceDirective(
        directive_type="Do Not Resuscitate",
        directive_type_code="304253006",
        directive_type_code_system="SNOMED CT",
        directive_value="Full code - resuscitation permitted",
        directive_value_code="304251008",
        directive_value_code_system="SNOMED CT",
        start_date=date(2023, 1, 15),
        end_date=None,
        custodian_name="Jane Smith",
        custodian_relationship="Spouse",
        custodian_relationship_code="SPS",
        custodian_phone="555-123-4567",
        custodian_address="123 Main St, Anytown, CA 12345",
        verifier_name="Dr. Robert Johnson",
        verification_date=date(2023, 1, 16),
        document_id="1.2.3.4.5.6.7",
        document_url="http://example.com/directives/dnr-directive.pdf",
    )

    directive2 = ExampleAdvanceDirective(
        directive_type="Healthcare Proxy",
        directive_type_code="304251006",
        directive_type_code_system="SNOMED CT",
        directive_value="Jane Smith designated as healthcare proxy",
        directive_value_code=None,
        directive_value_code_system=None,
        start_date=date(2023, 1, 15),
        end_date=None,
        custodian_name="Jane Smith",
        custodian_relationship="Spouse",
        custodian_relationship_code="SPS",
        custodian_phone="555-123-4567",
        custodian_address="123 Main St, Anytown, CA 12345",
        verifier_name="Dr. Robert Johnson",
        verification_date=date(2023, 1, 16),
        document_id="1.2.3.4.5.6.8",
    )

    directive3 = ExampleAdvanceDirective(
        directive_type="Living Will",
        directive_type_code="425392003",
        directive_type_code_system="SNOMED CT",
        directive_value="No intubation or mechanical ventilation for terminal condition",
        directive_value_code="304252001",
        directive_value_code_system="SNOMED CT",
        start_date=date(2022, 6, 10),
        end_date=None,
        custodian_name="Attorney Michael Davis",
        custodian_relationship="Attorney",
        custodian_relationship_code="ATTO",
        custodian_phone="555-987-6543",
        custodian_address="456 Legal Ave, Suite 100, Anytown, CA 12345",
        verifier_name="Dr. Sarah Martinez",
        verification_date=date(2022, 6, 15),
        document_id="1.2.3.4.5.6.9",
        document_url="http://example.com/directives/living-will.pdf",
        document_description="Living will signed on 2022-06-10",
    )

    # Create the Advance Directives Section
    section = AdvanceDirectivesSection(
        directives=[directive1, directive2, directive3],
        title="Patient Advance Directives",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Advance Directives Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show summary info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.21.1")
    print("  - Extension: 2015-08-01")
    print("  - Number of directives: 3")
    print("\nDirective Types:")
    print("  1. Do Not Resuscitate - with healthcare proxy")
    print("  2. Healthcare Proxy - designating spouse as proxy")
    print("  3. Living Will - specifying end-of-life preferences")
    print("\nConformance:")
    print("  - CONF:1198-30227: Template ID present")
    print("  - CONF:1198-32929: Code 42348-3 (Advance Directives)")
    print("  - CONF:1198-32932: Title present")
    print("  - CONF:1198-32933: Narrative text present")
    print("  - CONF:1198-30235: Advance directive observation entries present")
    print("  - CONF:1198-30236: Each entry contains Advance Directive Observation")
    print("\nKey Features Demonstrated:")
    print("  - Multiple advance directive types (DNR, Healthcare Proxy, Living Will)")
    print("  - SNOMED CT coding for directive types and values")
    print("  - Effective time periods with start dates")
    print("  - Healthcare proxy/custodian information with contact details")
    print("  - Clinical verification by healthcare providers")
    print("  - Document references with URLs")


if __name__ == "__main__":
    main()
