"""Tests for patient protocols."""

from datetime import date
from typing import Optional, Sequence

from ccdakit.protocols.patient import AddressProtocol, PatientProtocol, TelecomProtocol


class MockAddress:
    """Test implementation of AddressProtocol."""

    @property
    def street_lines(self) -> Sequence[str]:
        return ["123 Main St", "Apt 4B"]

    @property
    def city(self) -> str:
        return "Boston"

    @property
    def state(self) -> str:
        return "MA"

    @property
    def postal_code(self) -> str:
        return "02101"

    @property
    def country(self) -> str:
        return "US"


class MockTelecom:
    """Test implementation of TelecomProtocol."""

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


class MockPatient:
    """Test implementation of PatientProtocol."""

    @property
    def first_name(self) -> str:
        return "John"

    @property
    def last_name(self) -> str:
        return "Doe"

    @property
    def middle_name(self) -> Optional[str]:
        return "Q"

    @property
    def date_of_birth(self) -> date:
        return date(1970, 1, 1)

    @property
    def sex(self) -> str:
        return "M"

    @property
    def race(self) -> Optional[str]:
        return "2106-3"

    @property
    def ethnicity(self) -> Optional[str]:
        return "2186-5"

    @property
    def language(self) -> Optional[str]:
        return "eng"

    @property
    def ssn(self) -> Optional[str]:
        return "123-45-6789"

    @property
    def addresses(self) -> Sequence[MockAddress]:
        return [MockAddress()]

    @property
    def telecoms(self) -> Sequence[MockTelecom]:
        return [MockTelecom("phone", "617-555-1234", "HP")]

    @property
    def marital_status(self) -> Optional[str]:
        return "M"


def test_address_protocol_properties():
    """Test that AddressProtocol implementation has all required properties."""
    address = MockAddress()

    assert address.street_lines == ["123 Main St", "Apt 4B"]
    assert address.city == "Boston"
    assert address.state == "MA"
    assert address.postal_code == "02101"
    assert address.country == "US"


def test_address_protocol_satisfaction():
    """Test that MockAddress satisfies AddressProtocol."""
    address = MockAddress()

    # This should not raise an error
    def accepts_address(addr: AddressProtocol) -> str:
        return f"{addr.city}, {addr.state}"

    result = accepts_address(address)
    assert result == "Boston, MA"


def test_telecom_protocol_with_use():
    """Test TelecomProtocol with use code."""
    telecom = MockTelecom("phone", "617-555-1234", "HP")

    assert telecom.type == "phone"
    assert telecom.value == "617-555-1234"
    assert telecom.use == "HP"


def test_telecom_protocol_without_use():
    """Test TelecomProtocol without use code."""
    telecom = MockTelecom("email", "john@example.com")

    assert telecom.type == "email"
    assert telecom.value == "john@example.com"
    assert telecom.use is None


def test_telecom_protocol_satisfaction():
    """Test that MockTelecom satisfies TelecomProtocol."""
    telecom = MockTelecom("phone", "617-555-1234", "HP")

    def accepts_telecom(t: TelecomProtocol) -> str:
        return f"{t.type}: {t.value}"

    result = accepts_telecom(telecom)
    assert result == "phone: 617-555-1234"


def test_patient_protocol_required_fields():
    """Test PatientProtocol required fields."""
    patient = MockPatient()

    assert patient.first_name == "John"
    assert patient.last_name == "Doe"
    assert patient.date_of_birth == date(1970, 1, 1)
    assert patient.sex == "M"


def test_patient_protocol_optional_fields():
    """Test PatientProtocol optional fields."""
    patient = MockPatient()

    assert patient.middle_name == "Q"
    assert patient.race == "2106-3"
    assert patient.ethnicity == "2186-5"
    assert patient.language == "eng"
    assert patient.ssn == "123-45-6789"
    assert patient.marital_status == "M"


def test_patient_protocol_collections():
    """Test PatientProtocol collection properties."""
    patient = MockPatient()

    assert len(patient.addresses) == 1
    assert isinstance(patient.addresses[0], MockAddress)

    assert len(patient.telecoms) == 1
    assert isinstance(patient.telecoms[0], MockTelecom)


def test_patient_protocol_satisfaction():
    """Test that MockPatient satisfies PatientProtocol."""
    patient = MockPatient()

    def accepts_patient(p: PatientProtocol) -> str:
        return f"{p.first_name} {p.last_name}"

    result = accepts_patient(patient)
    assert result == "John Doe"


class MinimalPatient:
    """Minimal implementation with only required fields."""

    @property
    def first_name(self) -> str:
        return "Jane"

    @property
    def last_name(self) -> str:
        return "Smith"

    @property
    def middle_name(self) -> Optional[str]:
        return None

    @property
    def date_of_birth(self) -> date:
        return date(1980, 6, 15)

    @property
    def sex(self) -> str:
        return "F"

    @property
    def race(self) -> Optional[str]:
        return None

    @property
    def ethnicity(self) -> Optional[str]:
        return None

    @property
    def language(self) -> Optional[str]:
        return None

    @property
    def ssn(self) -> Optional[str]:
        return None

    @property
    def addresses(self) -> Sequence[MockAddress]:
        return []

    @property
    def telecoms(self) -> Sequence[MockTelecom]:
        return []

    @property
    def marital_status(self) -> Optional[str]:
        return None


def test_minimal_patient_protocol():
    """Test that minimal implementation satisfies PatientProtocol."""
    patient = MinimalPatient()

    assert patient.first_name == "Jane"
    assert patient.last_name == "Smith"
    assert patient.middle_name is None
    assert patient.date_of_birth == date(1980, 6, 15)
    assert patient.sex == "F"
    assert patient.race is None
    assert len(patient.addresses) == 0
    assert len(patient.telecoms) == 0


def test_patient_with_multiple_addresses():
    """Test patient with multiple addresses."""

    class MultiAddressPatient(MockPatient):
        @property
        def addresses(self):
            home = MockAddress()
            work = MockAddress()
            return [home, work]

    patient = MultiAddressPatient()
    assert len(patient.addresses) == 2


def test_patient_with_multiple_telecoms():
    """Test patient with multiple contact methods."""

    class MultiTelecomPatient(MockPatient):
        @property
        def telecoms(self):
            return [
                MockTelecom("phone", "617-555-1234", "HP"),
                MockTelecom("email", "john@example.com"),
                MockTelecom("phone", "617-555-5678", "WP"),
            ]

    patient = MultiTelecomPatient()
    assert len(patient.telecoms) == 3
    assert patient.telecoms[0].type == "phone"
    assert patient.telecoms[1].type == "email"
    assert patient.telecoms[2].use == "WP"


def test_address_protocol_property_access():
    """Test accessing all address properties."""
    address = MockAddress()

    # Access all properties to ensure protocol coverage
    assert isinstance(address.street_lines, Sequence)
    assert isinstance(address.city, str)
    assert isinstance(address.state, str)
    assert isinstance(address.postal_code, str)
    assert isinstance(address.country, str)


def test_telecom_protocol_property_access():
    """Test accessing all telecom properties."""
    telecom = MockTelecom("phone", "555-1234", "HP")

    # Access all properties to ensure protocol coverage
    assert isinstance(telecom.type, str)
    assert isinstance(telecom.value, str)
    assert telecom.use is None or isinstance(telecom.use, str)


def test_patient_protocol_property_access():
    """Test accessing all patient properties."""
    patient = MockPatient()

    # Access all properties to ensure protocol coverage
    assert isinstance(patient.first_name, str)
    assert isinstance(patient.last_name, str)
    assert patient.middle_name is None or isinstance(patient.middle_name, str)
    assert isinstance(patient.date_of_birth, date)
    assert isinstance(patient.sex, str)
    assert patient.race is None or isinstance(patient.race, str)
    assert patient.ethnicity is None or isinstance(patient.ethnicity, str)
    assert patient.language is None or isinstance(patient.language, str)
    assert patient.ssn is None or isinstance(patient.ssn, str)
    assert isinstance(patient.addresses, Sequence)
    assert isinstance(patient.telecoms, Sequence)
    assert patient.marital_status is None or isinstance(patient.marital_status, str)


def test_patient_different_sex_values():
    """Test patient with different sex values."""

    class MalePatient(MockPatient):
        @property
        def sex(self):
            return "M"

    class FemalePatient(MockPatient):
        @property
        def sex(self):
            return "F"

    class UnknownSexPatient(MockPatient):
        @property
        def sex(self):
            return "UN"

    male = MalePatient()
    female = FemalePatient()
    unknown = UnknownSexPatient()

    assert male.sex == "M"
    assert female.sex == "F"
    assert unknown.sex == "UN"


def test_patient_different_marital_statuses():
    """Test patient with different marital status values."""

    class MarriedPatient(MockPatient):
        @property
        def marital_status(self):
            return "M"

    class SinglePatient(MockPatient):
        @property
        def marital_status(self):
            return "S"

    class DivorcedPatient(MockPatient):
        @property
        def marital_status(self):
            return "D"

    married = MarriedPatient()
    single = SinglePatient()
    divorced = DivorcedPatient()

    assert married.marital_status == "M"
    assert single.marital_status == "S"
    assert divorced.marital_status == "D"


def test_telecom_different_types():
    """Test telecom with different types."""
    phone = MockTelecom("phone", "555-1234")
    email = MockTelecom("email", "test@example.com")
    fax = MockTelecom("fax", "555-5678")
    url = MockTelecom("url", "https://example.com")

    assert phone.type == "phone"
    assert email.type == "email"
    assert fax.type == "fax"
    assert url.type == "url"


def test_telecom_different_uses():
    """Test telecom with different use codes."""
    home = MockTelecom("phone", "555-1234", "HP")
    work = MockTelecom("phone", "555-5678", "WP")
    mobile = MockTelecom("phone", "555-9999", "MC")

    assert home.use == "HP"
    assert work.use == "WP"
    assert mobile.use == "MC"


def test_address_single_street_line():
    """Test address with single street line."""

    class SingleLineAddress:
        @property
        def street_lines(self):
            return ["123 Main St"]

        @property
        def city(self):
            return "Boston"

        @property
        def state(self):
            return "MA"

        @property
        def postal_code(self):
            return "02101"

        @property
        def country(self):
            return "US"

    address = SingleLineAddress()
    assert len(address.street_lines) == 1


def test_address_multiple_street_lines():
    """Test address with multiple street lines."""

    class MultiLineAddress:
        @property
        def street_lines(self):
            return ["123 Main St", "Suite 400", "Building A", "Floor 2"]

        @property
        def city(self):
            return "Boston"

        @property
        def state(self):
            return "MA"

        @property
        def postal_code(self):
            return "02101"

        @property
        def country(self):
            return "US"

    address = MultiLineAddress()
    assert len(address.street_lines) == 4


def test_patient_with_race_and_ethnicity():
    """Test patient with race and ethnicity codes."""

    class PatientWithDemographics(MockPatient):
        @property
        def race(self):
            return "2106-3"  # White

        @property
        def ethnicity(self):
            return "2186-5"  # Not Hispanic or Latino

    patient = PatientWithDemographics()
    assert patient.race == "2106-3"
    assert patient.ethnicity == "2186-5"


def test_patient_with_language():
    """Test patient with preferred language."""

    class SpanishSpeakingPatient(MockPatient):
        @property
        def language(self):
            return "spa"

    class FrenchSpeakingPatient(MockPatient):
        @property
        def language(self):
            return "fra"

    spanish = SpanishSpeakingPatient()
    french = FrenchSpeakingPatient()

    assert spanish.language == "spa"
    assert french.language == "fra"
