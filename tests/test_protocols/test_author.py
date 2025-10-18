"""Tests for author and organization protocols."""

from datetime import datetime
from typing import Optional, Sequence

from ccdakit.protocols.author import AuthorProtocol, OrganizationProtocol


class MockAddress:
    """Simple address implementation for testing."""

    @property
    def street_lines(self) -> Sequence[str]:
        return ["100 Medical Plaza"]

    @property
    def city(self) -> str:
        return "San Francisco"

    @property
    def state(self) -> str:
        return "CA"

    @property
    def postal_code(self) -> str:
        return "94102"

    @property
    def country(self) -> str:
        return "US"


class MockTelecom:
    """Simple telecom implementation for testing."""

    def __init__(self, type_: str, value: str, use: str = None):
        self._type = type_
        self._value = value
        self._use = use

    @property
    def type(self) -> str:
        return self._type

    @property
    def value(self) -> str:
        return self._value

    @property
    def use(self) -> Optional[str]:
        return self._use


class MockOrganization:
    """Mock implementation of OrganizationProtocol for testing."""

    def __init__(
        self,
        name: str = "Example Medical Center",
        npi: str = "1234567890",
        tin: str = None,
        oid_root: str = "2.16.840.1.113883.3.EXAMPLE",
    ):
        self._name = name
        self._npi = npi
        self._tin = tin
        self._oid_root = oid_root

    @property
    def name(self) -> str:
        return self._name

    @property
    def npi(self) -> Optional[str]:
        return self._npi

    @property
    def tin(self) -> Optional[str]:
        return self._tin

    @property
    def oid_root(self) -> Optional[str]:
        return self._oid_root

    @property
    def addresses(self) -> Sequence[MockAddress]:
        return [MockAddress()]

    @property
    def telecoms(self) -> Sequence[MockTelecom]:
        return [MockTelecom("phone", "415-555-1234", "WP")]


class MockAuthor:
    """Mock implementation of AuthorProtocol for testing."""

    def __init__(
        self,
        first_name: str = "Alice",
        last_name: str = "Smith",
        middle_name: str = "M",
        npi: str = "9876543210",
        time: datetime = None,
        organization: OrganizationProtocol = None,
    ):
        self._first_name = first_name
        self._last_name = last_name
        self._middle_name = middle_name
        self._npi = npi
        self._time = time or datetime(2023, 10, 17, 14, 30)
        self._organization = organization

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def middle_name(self) -> Optional[str]:
        return self._middle_name

    @property
    def npi(self) -> Optional[str]:
        return self._npi

    @property
    def addresses(self) -> Sequence[MockAddress]:
        return [MockAddress()]

    @property
    def telecoms(self) -> Sequence[MockTelecom]:
        return [MockTelecom("phone", "415-555-9876", "WP")]

    @property
    def time(self) -> datetime:
        return self._time

    @property
    def organization(self) -> Optional[MockOrganization]:
        return self._organization


def test_organization_protocol_required_fields():
    """Test OrganizationProtocol required fields."""
    org = MockOrganization()

    assert org.name == "Example Medical Center"
    assert org.npi == "1234567890"


def test_organization_protocol_optional_fields():
    """Test OrganizationProtocol optional fields."""
    org = MockOrganization(tin="12-3456789")

    assert org.tin == "12-3456789"
    assert org.oid_root == "2.16.840.1.113883.3.EXAMPLE"


def test_organization_protocol_collections():
    """Test OrganizationProtocol collection properties."""
    org = MockOrganization()

    assert len(org.addresses) == 1
    assert len(org.telecoms) == 1


def test_organization_protocol_satisfaction():
    """Test that MockOrganization satisfies OrganizationProtocol."""
    org = MockOrganization()

    def accepts_org(o: OrganizationProtocol) -> str:
        return f"{o.name} (NPI: {o.npi})"

    result = accepts_org(org)
    assert result == "Example Medical Center (NPI: 1234567890)"


def test_author_protocol_required_fields():
    """Test AuthorProtocol required fields."""
    author = MockAuthor()

    assert author.first_name == "Alice"
    assert author.last_name == "Smith"
    assert author.time == datetime(2023, 10, 17, 14, 30)


def test_author_protocol_optional_fields():
    """Test AuthorProtocol optional fields."""
    author = MockAuthor()

    assert author.middle_name == "M"
    assert author.npi == "9876543210"


def test_author_protocol_collections():
    """Test AuthorProtocol collection properties."""
    author = MockAuthor()

    assert len(author.addresses) == 1
    assert len(author.telecoms) == 1


def test_author_protocol_with_organization():
    """Test AuthorProtocol with organization."""
    org = MockOrganization()
    author = MockAuthor(organization=org)

    assert author.organization is not None
    assert author.organization.name == "Example Medical Center"


def test_author_protocol_without_organization():
    """Test AuthorProtocol without organization."""
    author = MockAuthor()

    assert author.organization is None


def test_author_protocol_satisfaction():
    """Test that MockAuthor satisfies AuthorProtocol."""
    author = MockAuthor()

    def accepts_author(a: AuthorProtocol) -> str:
        return f"Dr. {a.first_name} {a.last_name}"

    result = accepts_author(author)
    assert result == "Dr. Alice Smith"


class MinimalOrganization:
    """Minimal implementation with only required fields."""

    @property
    def name(self) -> str:
        return "City Clinic"

    @property
    def npi(self) -> Optional[str]:
        return None

    @property
    def tin(self) -> Optional[str]:
        return None

    @property
    def oid_root(self) -> Optional[str]:
        return None

    @property
    def addresses(self) -> Sequence[MockAddress]:
        return []

    @property
    def telecoms(self) -> Sequence[MockTelecom]:
        return []


def test_minimal_organization_protocol():
    """Test that minimal implementation satisfies OrganizationProtocol."""
    org = MinimalOrganization()

    assert org.name == "City Clinic"
    assert org.npi is None
    assert org.tin is None
    assert org.oid_root is None
    assert len(org.addresses) == 0
    assert len(org.telecoms) == 0


class MinimalAuthor:
    """Minimal implementation with only required fields."""

    @property
    def first_name(self) -> str:
        return "Bob"

    @property
    def last_name(self) -> str:
        return "Johnson"

    @property
    def middle_name(self) -> Optional[str]:
        return None

    @property
    def npi(self) -> Optional[str]:
        return None

    @property
    def addresses(self) -> Sequence[MockAddress]:
        return []

    @property
    def telecoms(self) -> Sequence[MockTelecom]:
        return []

    @property
    def time(self) -> datetime:
        return datetime(2023, 10, 17, 10, 0)

    @property
    def organization(self) -> Optional[MockOrganization]:
        return None


def test_minimal_author_protocol():
    """Test that minimal implementation satisfies AuthorProtocol."""
    author = MinimalAuthor()

    assert author.first_name == "Bob"
    assert author.last_name == "Johnson"
    assert author.middle_name is None
    assert author.npi is None
    assert author.time == datetime(2023, 10, 17, 10, 0)
    assert author.organization is None
    assert len(author.addresses) == 0
    assert len(author.telecoms) == 0


def test_author_with_full_organization():
    """Test author with fully specified organization."""
    org = MockOrganization(
        name="Advanced Healthcare Systems",
        npi="1112223330",
        tin="98-7654321",
        oid_root="2.16.840.1.113883.3.AHS",
    )

    author = MockAuthor(organization=org)

    assert author.organization.name == "Advanced Healthcare Systems"
    assert author.organization.npi == "1112223330"
    assert author.organization.tin == "98-7654321"
    assert author.organization.oid_root == "2.16.840.1.113883.3.AHS"


def test_organization_with_multiple_addresses():
    """Test organization with multiple addresses."""

    class MultiAddressOrg(MockOrganization):
        @property
        def addresses(self):
            return [MockAddress(), MockAddress()]

    org = MultiAddressOrg()
    assert len(org.addresses) == 2


def test_organization_with_multiple_telecoms():
    """Test organization with multiple contact methods."""

    class MultiTelecomOrg(MockOrganization):
        @property
        def telecoms(self):
            return [
                MockTelecom("phone", "415-555-1234", "WP"),
                MockTelecom("fax", "415-555-1235"),
                MockTelecom("email", "info@example.com"),
            ]

    org = MultiTelecomOrg()
    assert len(org.telecoms) == 3


def test_author_time_formatting():
    """Test author with specific time."""
    specific_time = datetime(2023, 12, 25, 15, 45, 30)
    author = MockAuthor(time=specific_time)

    assert author.time == specific_time
    assert author.time.year == 2023
    assert author.time.month == 12
    assert author.time.day == 25
