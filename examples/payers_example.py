"""Example of creating a Payers Section."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.payers import PayersSection
from ccdakit.core.base import CDAVersion


# Define payer data class
class ExamplePayer:
    """Example payer/insurance data."""

    def __init__(
        self,
        payer_name,
        payer_id,
        member_id,
        group_number=None,
        insurance_type="PPO",
        insurance_type_code=None,
        start_date=None,
        end_date=None,
        sequence_number=None,
        subscriber_name=None,
        subscriber_id=None,
        relationship_to_subscriber="self",
        payer_phone=None,
        coverage_type_code=None,
        authorization_ids=None,
    ):
        self._payer_name = payer_name
        self._payer_id = payer_id
        self._member_id = member_id
        self._group_number = group_number
        self._insurance_type = insurance_type
        self._insurance_type_code = insurance_type_code or insurance_type
        self._start_date = start_date
        self._end_date = end_date
        self._sequence_number = sequence_number
        self._subscriber_name = subscriber_name
        self._subscriber_id = subscriber_id
        self._relationship_to_subscriber = relationship_to_subscriber
        self._payer_phone = payer_phone
        self._coverage_type_code = coverage_type_code
        self._authorization_ids = authorization_ids

    @property
    def payer_name(self):
        return self._payer_name

    @property
    def payer_id(self):
        return self._payer_id

    @property
    def member_id(self):
        return self._member_id

    @property
    def group_number(self):
        return self._group_number

    @property
    def insurance_type(self):
        return self._insurance_type

    @property
    def insurance_type_code(self):
        return self._insurance_type_code

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def sequence_number(self):
        return self._sequence_number

    @property
    def subscriber_name(self):
        return self._subscriber_name

    @property
    def subscriber_id(self):
        return self._subscriber_id

    @property
    def relationship_to_subscriber(self):
        return self._relationship_to_subscriber

    @property
    def payer_phone(self):
        return self._payer_phone

    @property
    def coverage_type_code(self):
        return self._coverage_type_code

    @property
    def authorization_ids(self):
        return self._authorization_ids


def main():
    """Create and display a Payers Section example."""

    # Create payer/insurance data
    # Primary Insurance - Blue Cross Blue Shield PPO
    primary_insurance = ExamplePayer(
        payer_name="Blue Cross Blue Shield of California",
        payer_id="60054",  # NAIC number
        member_id="BC123456789",
        group_number="GRP001234",
        insurance_type="PPO",
        insurance_type_code="PPO",
        start_date=date(2023, 1, 1),
        end_date=None,  # Ongoing coverage
        sequence_number=1,  # Primary
        subscriber_name=None,  # Patient is subscriber
        subscriber_id=None,
        relationship_to_subscriber="self",
        payer_phone="1-800-555-0001",
        coverage_type_code="SELF",
        authorization_ids=None,
    )

    # Secondary Insurance - Medicare Part B
    secondary_insurance = ExamplePayer(
        payer_name="Medicare Part B",
        payer_id="MCARE",
        member_id="1EG4-TE5-MK73",
        group_number=None,  # Medicare typically has no group number
        insurance_type="Medicare",
        insurance_type_code="MEDICARE",
        start_date=date(2022, 6, 1),
        end_date=None,
        sequence_number=2,  # Secondary
        subscriber_name=None,
        subscriber_id=None,
        relationship_to_subscriber="self",
        payer_phone="1-800-MEDICARE",
        coverage_type_code="SELF",
        authorization_ids=None,
    )

    # Tertiary Insurance - Medicaid (with subscriber different from patient)
    tertiary_insurance = ExamplePayer(
        payer_name="State Medicaid Program",
        payer_id="MEDICAID-CA",
        member_id="MCD987654321",
        group_number=None,
        insurance_type="Medicaid",
        insurance_type_code="MEDICAID",
        start_date=date(2023, 3, 1),
        end_date=None,
        sequence_number=3,  # Tertiary
        subscriber_name="Jane Doe",  # Spouse is subscriber
        subscriber_id="MCD111222333",
        relationship_to_subscriber="spouse",
        payer_phone="1-800-555-0123",
        coverage_type_code="SPOUSE",
        authorization_ids=["AUTH-2023-001", "AUTH-2023-002"],
    )

    # Create the Payers Section with multiple insurances
    section = PayersSection(
        payers=[primary_insurance, secondary_insurance, tertiary_insurance],
        title="Patient Insurance Coverage",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Payers Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show summary info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.18")
    print("  - Extension: 2015-08-01")
    print("  - LOINC Code: 48768-6 (Payers)")
    print("  - Number of payers: 3")
    print("\nPayers:")
    print("  1. Primary: Blue Cross Blue Shield of California (PPO)")
    print("     - Member ID: BC123456789")
    print("     - Group: GRP001234")
    print("     - Active since: 2023-01-01")
    print("\n  2. Secondary: Medicare Part B")
    print("     - Member ID: 1EG4-TE5-MK73")
    print("     - Active since: 2022-06-01")
    print("\n  3. Tertiary: State Medicaid Program")
    print("     - Member ID: MCD987654321")
    print("     - Subscriber: Jane Doe (spouse)")
    print("     - Active since: 2023-03-01")
    print("     - Authorizations: 2")
    print("\nConformance:")
    print("  - CONF:1198-7924: Template ID present")
    print("  - CONF:1198-15395: Code 48768-6 (Payers)")
    print("  - CONF:1198-7926: Title present")
    print("  - CONF:1198-7927: Narrative text present")
    print("  - CONF:1198-7959: Coverage Activity entries present")
    print("  - CONF:1198-15501: Policy Activity nested in Coverage Activity")


if __name__ == "__main__":
    main()
