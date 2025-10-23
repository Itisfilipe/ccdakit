"""Tests for advance directive protocols."""

from datetime import date
from typing import Optional

from ccdakit.protocols.advance_directive import AdvanceDirectiveProtocol


class MockAdvanceDirective:
    """Test implementation of AdvanceDirectiveProtocol."""

    def __init__(
        self,
        directive_type: str = "Do Not Resuscitate",
        directive_type_code: Optional[str] = "304253006",
        directive_type_code_system: Optional[str] = "SNOMED CT",
        directive_value: str = "Full code",
        directive_value_code: Optional[str] = None,
        directive_value_code_system: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        custodian_name: Optional[str] = None,
        custodian_relationship: Optional[str] = None,
        custodian_relationship_code: Optional[str] = None,
        custodian_phone: Optional[str] = None,
        custodian_address: Optional[str] = None,
        verifier_name: Optional[str] = None,
        verification_date: Optional[date] = None,
        document_id: Optional[str] = None,
        document_url: Optional[str] = None,
        document_description: Optional[str] = None,
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


def test_advance_directive_protocol_required_fields():
    """Test AdvanceDirectiveProtocol required fields."""
    directive = MockAdvanceDirective()

    assert directive.directive_type == "Do Not Resuscitate"
    assert directive.directive_value == "Full code"


def test_advance_directive_protocol_with_codes():
    """Test AdvanceDirectiveProtocol with type and value codes."""
    directive = MockAdvanceDirective(
        directive_type="Resuscitate",
        directive_type_code="304252001",
        directive_type_code_system="SNOMED CT",
        directive_value="Full code",
        directive_value_code="385652002",
        directive_value_code_system="SNOMED CT",
    )

    assert directive.directive_type_code == "304252001"
    assert directive.directive_type_code_system == "SNOMED CT"
    assert directive.directive_value_code == "385652002"
    assert directive.directive_value_code_system == "SNOMED CT"


def test_advance_directive_protocol_with_dates():
    """Test AdvanceDirectiveProtocol with start and end dates."""
    start = date(2023, 1, 15)
    end = date(2024, 1, 15)
    directive = MockAdvanceDirective(start_date=start, end_date=end)

    assert directive.start_date == start
    assert directive.end_date == end


def test_advance_directive_protocol_with_custodian():
    """Test AdvanceDirectiveProtocol with custodian information."""
    directive = MockAdvanceDirective(
        custodian_name="Jane Doe",
        custodian_relationship="Spouse",
        custodian_relationship_code="SPOUSE",
        custodian_phone="555-123-4567",
        custodian_address="123 Main St, Anytown, CA 12345",
    )

    assert directive.custodian_name == "Jane Doe"
    assert directive.custodian_relationship == "Spouse"
    assert directive.custodian_relationship_code == "SPOUSE"
    assert directive.custodian_phone == "555-123-4567"
    assert directive.custodian_address == "123 Main St, Anytown, CA 12345"


def test_advance_directive_protocol_with_verifier():
    """Test AdvanceDirectiveProtocol with verifier information."""
    verification = date(2023, 1, 15)
    directive = MockAdvanceDirective(
        verifier_name="Dr. John Smith", verification_date=verification
    )

    assert directive.verifier_name == "Dr. John Smith"
    assert directive.verification_date == verification


def test_advance_directive_protocol_with_document():
    """Test AdvanceDirectiveProtocol with document information."""
    directive = MockAdvanceDirective(
        document_id="AD-12345",
        document_url="https://example.com/documents/AD-12345.pdf",
        document_description="Advance directive signed 2023-01-15",
    )

    assert directive.document_id == "AD-12345"
    assert directive.document_url == "https://example.com/documents/AD-12345.pdf"
    assert directive.document_description == "Advance directive signed 2023-01-15"


def test_advance_directive_protocol_satisfaction():
    """Test that MockAdvanceDirective satisfies AdvanceDirectiveProtocol."""
    directive = MockAdvanceDirective()

    def accepts_directive(d: AdvanceDirectiveProtocol) -> str:
        return f"{d.directive_type}: {d.directive_value}"

    result = accepts_directive(directive)
    assert result == "Do Not Resuscitate: Full code"


def test_advance_directive_dnr():
    """Test advance directive for Do Not Resuscitate."""
    directive = MockAdvanceDirective(
        directive_type="Do Not Resuscitate",
        directive_type_code="304253006",
        directive_value="No CPR",
    )

    assert directive.directive_type == "Do Not Resuscitate"
    assert directive.directive_type_code == "304253006"
    assert directive.directive_value == "No CPR"


def test_advance_directive_living_will():
    """Test advance directive for living will."""
    directive = MockAdvanceDirective(
        directive_type="Living Will",
        directive_type_code="425392003",
        directive_value="No life-sustaining measures",
    )

    assert directive.directive_type == "Living Will"
    assert directive.directive_type_code == "425392003"


def test_advance_directive_healthcare_proxy():
    """Test advance directive for healthcare proxy."""
    directive = MockAdvanceDirective(
        directive_type="Healthcare Proxy",
        directive_value="Designated agent: Jane Doe",
        custodian_name="Jane Doe",
        custodian_relationship="Spouse",
    )

    assert directive.directive_type == "Healthcare Proxy"
    assert directive.custodian_name == "Jane Doe"
    assert directive.custodian_relationship == "Spouse"


def test_advance_directive_with_no_end_date():
    """Test advance directive with no specified ending time."""
    directive = MockAdvanceDirective(
        start_date=date(2023, 1, 15), end_date=None
    )

    assert directive.start_date == date(2023, 1, 15)
    assert directive.end_date is None


def test_advance_directive_resuscitate():
    """Test advance directive for resuscitation orders."""
    directive = MockAdvanceDirective(
        directive_type="Resuscitate",
        directive_type_code="304252001",
        directive_value="Full code",
    )

    assert directive.directive_type == "Resuscitate"
    assert directive.directive_value == "Full code"


class MinimalAdvanceDirective:
    """Minimal implementation with only required fields."""

    @property
    def directive_type(self):
        return "Do Not Resuscitate"

    @property
    def directive_type_code(self):
        return None

    @property
    def directive_type_code_system(self):
        return None

    @property
    def directive_value(self):
        return "No CPR"

    @property
    def directive_value_code(self):
        return None

    @property
    def directive_value_code_system(self):
        return None

    @property
    def start_date(self):
        return None

    @property
    def end_date(self):
        return None

    @property
    def custodian_name(self):
        return None

    @property
    def custodian_relationship(self):
        return None

    @property
    def custodian_relationship_code(self):
        return None

    @property
    def custodian_phone(self):
        return None

    @property
    def custodian_address(self):
        return None

    @property
    def verifier_name(self):
        return None

    @property
    def verification_date(self):
        return None

    @property
    def document_id(self):
        return None

    @property
    def document_url(self):
        return None

    @property
    def document_description(self):
        return None


def test_minimal_advance_directive_protocol():
    """Test that minimal implementation satisfies AdvanceDirectiveProtocol."""
    directive = MinimalAdvanceDirective()

    assert directive.directive_type == "Do Not Resuscitate"
    assert directive.directive_value == "No CPR"
    assert directive.directive_type_code is None
    assert directive.directive_type_code_system is None
    assert directive.directive_value_code is None
    assert directive.directive_value_code_system is None
    assert directive.start_date is None
    assert directive.end_date is None
    assert directive.custodian_name is None
    assert directive.custodian_relationship is None
    assert directive.custodian_relationship_code is None
    assert directive.custodian_phone is None
    assert directive.custodian_address is None
    assert directive.verifier_name is None
    assert directive.verification_date is None
    assert directive.document_id is None
    assert directive.document_url is None
    assert directive.document_description is None


def test_advance_directive_complete_example():
    """Test advance directive with complete information."""
    directive = MockAdvanceDirective(
        directive_type="Do Not Resuscitate",
        directive_type_code="304253006",
        directive_type_code_system="SNOMED CT",
        directive_value="No CPR, no intubation",
        directive_value_code="385652002",
        directive_value_code_system="SNOMED CT",
        start_date=date(2023, 1, 15),
        end_date=None,
        custodian_name="Jane Doe",
        custodian_relationship="Spouse",
        custodian_relationship_code="SPOUSE",
        custodian_phone="555-123-4567",
        custodian_address="123 Main St, Anytown, CA 12345",
        verifier_name="Dr. John Smith",
        verification_date=date(2023, 1, 15),
        document_id="AD-12345",
        document_url="https://example.com/documents/AD-12345.pdf",
        document_description="Advance directive signed and notarized",
    )

    assert directive.directive_type == "Do Not Resuscitate"
    assert directive.directive_type_code == "304253006"
    assert directive.directive_value == "No CPR, no intubation"
    assert directive.custodian_name == "Jane Doe"
    assert directive.verifier_name == "Dr. John Smith"
    assert directive.document_id == "AD-12345"


def test_advance_directive_child_custodian():
    """Test advance directive with child as custodian."""
    directive = MockAdvanceDirective(
        custodian_name="John Doe Jr.",
        custodian_relationship="Child",
        custodian_relationship_code="CHILD",
    )

    assert directive.custodian_relationship == "Child"
    assert directive.custodian_relationship_code == "CHILD"


def test_advance_directive_attorney_custodian():
    """Test advance directive with attorney as custodian."""
    directive = MockAdvanceDirective(
        custodian_name="Law Firm LLC",
        custodian_relationship="Attorney",
        custodian_relationship_code="ATTORNEY",
    )

    assert directive.custodian_relationship == "Attorney"
    assert directive.custodian_relationship_code == "ATTORNEY"


def test_advance_directive_no_intubation():
    """Test advance directive for no intubation."""
    directive = MockAdvanceDirective(
        directive_type="Do Not Intubate",
        directive_value="No intubation or mechanical ventilation",
    )

    assert directive.directive_type == "Do Not Intubate"
    assert "intubation" in directive.directive_value.lower()


def test_advance_directive_antibiotics_only():
    """Test advance directive allowing IV antibiotics only."""
    directive = MockAdvanceDirective(
        directive_type="Limited Treatment",
        directive_value="IV antibiotics only, no other interventions",
    )

    assert directive.directive_type == "Limited Treatment"
    assert "antibiotics" in directive.directive_value.lower()


def test_advance_directive_type_checking():
    """Test that AdvanceDirectiveProtocol enforces correct types."""
    directive = MockAdvanceDirective(
        start_date=date(2023, 1, 15),
        verification_date=date(2023, 1, 15),
    )

    assert isinstance(directive.directive_type, str)
    assert isinstance(directive.directive_value, str)
    assert isinstance(directive.start_date, date)
    assert isinstance(directive.verification_date, date)


def test_advance_directive_without_codes():
    """Test advance directive with only text descriptions (no codes)."""
    directive = MockAdvanceDirective(
        directive_type="Living Will",
        directive_type_code=None,
        directive_type_code_system=None,
        directive_value="Comfort measures only",
        directive_value_code=None,
        directive_value_code_system=None,
    )

    assert directive.directive_type == "Living Will"
    assert directive.directive_value == "Comfort measures only"
    assert directive.directive_type_code is None
    assert directive.directive_value_code is None


def test_advance_directive_protocol_interface():
    """Test that AdvanceDirectiveProtocol has expected interface."""
    # Import to ensure coverage
    from ccdakit.protocols.advance_directive import AdvanceDirectiveProtocol

    # Verify protocol has expected attributes
    assert hasattr(AdvanceDirectiveProtocol, 'directive_type')
    assert hasattr(AdvanceDirectiveProtocol, 'directive_value')
    assert hasattr(AdvanceDirectiveProtocol, 'directive_type_code')
    assert hasattr(AdvanceDirectiveProtocol, 'directive_value_code')
    assert hasattr(AdvanceDirectiveProtocol, 'custodian_name')
    assert hasattr(AdvanceDirectiveProtocol, 'verifier_name')

    # Verify docstrings exist
    assert AdvanceDirectiveProtocol.__doc__ is not None
    assert 'Advance Directive data contract' in AdvanceDirectiveProtocol.__doc__
