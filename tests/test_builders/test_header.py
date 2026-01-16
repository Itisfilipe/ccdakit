"""Tests for header component builders."""

from datetime import date, datetime
from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.header.author import Author, Custodian
from ccdakit.builders.header.record_target import RecordTarget


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockAddress:
    """Mock address for testing."""

    @property
    def street_lines(self) -> Sequence[str]:
        return ["123 Main St"]

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
    """Mock telecom for testing."""

    def __init__(self, type_="phone", value="617-555-1234", use=None):
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
    """Mock patient for testing."""

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
        return [MockTelecom()]

    @property
    def marital_status(self) -> Optional[str]:
        return "M"


class MockOrganization:
    """Mock organization for testing."""

    def __init__(self, npi="1234567890", oid_root="2.16.840.1.113883.3.TEST"):
        self._npi = npi
        self._oid_root = oid_root

    @property
    def name(self) -> str:
        return "Example Medical Center"

    @property
    def npi(self) -> Optional[str]:
        return self._npi

    @property
    def tin(self) -> Optional[str]:
        return None

    @property
    def oid_root(self) -> Optional[str]:
        return self._oid_root

    @property
    def addresses(self) -> Sequence[MockAddress]:
        return [MockAddress()]

    @property
    def telecoms(self) -> Sequence[MockTelecom]:
        return [MockTelecom(type_="phone", value="617-555-9999")]


class MockAuthor:
    """Mock author for testing."""

    def __init__(self, organization=None):
        self._organization = organization

    @property
    def first_name(self) -> str:
        return "Alice"

    @property
    def last_name(self) -> str:
        return "Smith"

    @property
    def middle_name(self) -> Optional[str]:
        return "M"

    @property
    def npi(self) -> Optional[str]:
        return "9876543210"

    @property
    def addresses(self) -> Sequence[MockAddress]:
        return [MockAddress()]

    @property
    def telecoms(self) -> Sequence[MockTelecom]:
        return [MockTelecom()]

    @property
    def time(self) -> datetime:
        return datetime(2023, 10, 17, 14, 30)

    @property
    def organization(self) -> Optional[MockOrganization]:
        return self._organization


class TestRecordTarget:
    """Tests for RecordTarget builder."""

    def test_record_target_basic(self):
        """Test basic RecordTarget building."""
        patient = MockPatient()
        rt = RecordTarget(patient)
        elem = rt.to_element()

        assert local_name(elem) == "recordTarget"
        patient_role = elem.find(f"{{{NS}}}patientRole")
        assert patient_role is not None

    def test_record_target_has_patient_identifiers(self):
        """Test RecordTarget includes patient identifiers."""
        patient = MockPatient()
        rt = RecordTarget(patient)
        elem = rt.to_element()

        patient_role = elem.find(f"{{{NS}}}patientRole")
        id_elem = patient_role.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.4.1"  # SSN OID
        assert id_elem.get("extension") == "123-45-6789"

    def test_record_target_has_addresses(self):
        """Test RecordTarget includes addresses."""
        patient = MockPatient()
        rt = RecordTarget(patient)
        elem = rt.to_element()

        patient_role = elem.find(f"{{{NS}}}patientRole")
        addr = patient_role.find(f"{{{NS}}}addr")
        assert addr is not None
        assert addr.find(f"{{{NS}}}city").text == "Boston"

    def test_record_target_has_telecoms(self):
        """Test RecordTarget includes telecoms."""
        patient = MockPatient()
        rt = RecordTarget(patient)
        elem = rt.to_element()

        patient_role = elem.find(f"{{{NS}}}patientRole")
        telecom = patient_role.find(f"{{{NS}}}telecom")
        assert telecom is not None

    def test_record_target_patient_name(self):
        """Test RecordTarget includes patient name."""
        patient = MockPatient()
        rt = RecordTarget(patient)
        elem = rt.to_element()

        patient_role = elem.find(f"{{{NS}}}patientRole")
        patient_elem = patient_role.find(f"{{{NS}}}patient")
        name = patient_elem.find(f"{{{NS}}}name")
        assert name is not None

        given_names = name.findall(f"{{{NS}}}given")
        assert len(given_names) == 2  # First and middle
        assert given_names[0].text == "John"
        assert given_names[1].text == "Q"

        family = name.find(f"{{{NS}}}family")
        assert family.text == "Doe"

    def test_record_target_gender(self):
        """Test RecordTarget includes gender."""
        patient = MockPatient()
        rt = RecordTarget(patient)
        elem = rt.to_element()

        patient_role = elem.find(f"{{{NS}}}patientRole")
        patient_elem = patient_role.find(f"{{{NS}}}patient")
        gender = patient_elem.find(f"{{{NS}}}administrativeGenderCode")
        assert gender is not None
        assert gender.get("code") == "M"
        assert gender.get("displayName") == "Male"

    def test_record_target_birth_time(self):
        """Test RecordTarget includes birth time."""
        patient = MockPatient()
        rt = RecordTarget(patient)
        elem = rt.to_element()

        patient_role = elem.find(f"{{{NS}}}patientRole")
        patient_elem = patient_role.find(f"{{{NS}}}patient")
        birth_time = patient_elem.find(f"{{{NS}}}birthTime")
        assert birth_time is not None
        assert birth_time.get("value") == "19700101"

    def test_record_target_race(self):
        """Test RecordTarget includes race."""
        patient = MockPatient()
        rt = RecordTarget(patient)
        elem = rt.to_element()

        patient_role = elem.find(f"{{{NS}}}patientRole")
        patient_elem = patient_role.find(f"{{{NS}}}patient")
        race = patient_elem.find(f"{{{NS}}}raceCode")
        assert race is not None
        assert race.get("code") == "2106-3"

    def test_record_target_ethnicity(self):
        """Test RecordTarget includes ethnicity."""
        patient = MockPatient()
        rt = RecordTarget(patient)
        elem = rt.to_element()

        patient_role = elem.find(f"{{{NS}}}patientRole")
        patient_elem = patient_role.find(f"{{{NS}}}patient")
        ethnicity = patient_elem.find(f"{{{NS}}}ethnicGroupCode")
        assert ethnicity is not None
        assert ethnicity.get("code") == "2186-5"

    def test_record_target_language(self):
        """Test RecordTarget includes language."""
        patient = MockPatient()
        rt = RecordTarget(patient)
        elem = rt.to_element()

        patient_role = elem.find(f"{{{NS}}}patientRole")
        patient_elem = patient_role.find(f"{{{NS}}}patient")
        lang_comm = patient_elem.find(f"{{{NS}}}languageCommunication")
        assert lang_comm is not None

        lang_code = lang_comm.find(f"{{{NS}}}languageCode")
        assert lang_code.get("code") == "eng"

    def test_record_target_marital_status(self):
        """Test RecordTarget includes marital status."""
        patient = MockPatient()
        rt = RecordTarget(patient)
        elem = rt.to_element()

        patient_role = elem.find(f"{{{NS}}}patientRole")
        patient_elem = patient_role.find(f"{{{NS}}}patient")
        marital = patient_elem.find(f"{{{NS}}}maritalStatusCode")
        assert marital is not None
        assert marital.get("code") == "M"


class TestAuthor:
    """Tests for Author builder."""

    def test_author_basic(self):
        """Test basic Author building."""
        author_data = MockAuthor()
        author = Author(author_data)
        elem = author.to_element()

        assert local_name(elem) == "author"
        time = elem.find(f"{{{NS}}}time")
        assert time is not None
        assert time.get("value").startswith("20231017143000")

    def test_author_has_assigned_author(self):
        """Test Author has assignedAuthor."""
        author_data = MockAuthor()
        author = Author(author_data)
        elem = author.to_element()

        assigned = elem.find(f"{{{NS}}}assignedAuthor")
        assert assigned is not None

    def test_author_has_npi(self):
        """Test Author includes NPI."""
        author_data = MockAuthor()
        author = Author(author_data)
        elem = author.to_element()

        assigned = elem.find(f"{{{NS}}}assignedAuthor")
        id_elem = assigned.find(f"{{{NS}}}id")
        assert id_elem.get("root") == "2.16.840.1.113883.4.6"  # NPI OID
        assert id_elem.get("extension") == "9876543210"

    def test_author_name(self):
        """Test Author includes name."""
        author_data = MockAuthor()
        author = Author(author_data)
        elem = author.to_element()

        assigned = elem.find(f"{{{NS}}}assignedAuthor")
        person = assigned.find(f"{{{NS}}}assignedPerson")
        name = person.find(f"{{{NS}}}name")
        assert name is not None

        given_names = name.findall(f"{{{NS}}}given")
        assert len(given_names) == 2
        assert given_names[0].text == "Alice"
        assert given_names[1].text == "M"

        family = name.find(f"{{{NS}}}family")
        assert family.text == "Smith"

    def test_author_with_organization(self):
        """Test Author with organization."""
        org = MockOrganization()
        author_data = MockAuthor(organization=org)
        author = Author(author_data)
        elem = author.to_element()

        assigned = elem.find(f"{{{NS}}}assignedAuthor")
        rep_org = assigned.find(f"{{{NS}}}representedOrganization")
        assert rep_org is not None

        name = rep_org.find(f"{{{NS}}}name")
        assert name.text == "Example Medical Center"

    def test_author_without_organization(self):
        """Test Author without organization."""
        author_data = MockAuthor()
        author = Author(author_data)
        elem = author.to_element()

        assigned = elem.find(f"{{{NS}}}assignedAuthor")
        rep_org = assigned.find(f"{{{NS}}}representedOrganization")
        assert rep_org is None


class TestCustodian:
    """Tests for Custodian builder."""

    def test_custodian_basic(self):
        """Test basic Custodian building."""
        org = MockOrganization()
        custodian = Custodian(org)
        elem = custodian.to_element()

        assert local_name(elem) == "custodian"
        assigned = elem.find(f"{{{NS}}}assignedCustodian")
        assert assigned is not None

    def test_custodian_has_organization(self):
        """Test Custodian has organization."""
        org = MockOrganization()
        custodian = Custodian(org)
        elem = custodian.to_element()

        assigned = elem.find(f"{{{NS}}}assignedCustodian")
        rep_org = assigned.find(f"{{{NS}}}representedCustodianOrganization")
        assert rep_org is not None

    def test_custodian_organization_name(self):
        """Test Custodian organization name."""
        org = MockOrganization()
        custodian = Custodian(org)
        elem = custodian.to_element()

        assigned = elem.find(f"{{{NS}}}assignedCustodian")
        rep_org = assigned.find(f"{{{NS}}}representedCustodianOrganization")
        name = rep_org.find(f"{{{NS}}}name")
        assert name.text == "Example Medical Center"

    def test_custodian_organization_npi(self):
        """Test Custodian organization NPI."""
        org = MockOrganization()
        custodian = Custodian(org)
        elem = custodian.to_element()

        assigned = elem.find(f"{{{NS}}}assignedCustodian")
        rep_org = assigned.find(f"{{{NS}}}representedCustodianOrganization")
        id_elem = rep_org.find(f"{{{NS}}}id")
        assert id_elem.get("root") == "2.16.840.1.113883.4.6"  # NPI OID
        assert id_elem.get("extension") == "1234567890"

    def test_custodian_organization_addresses(self):
        """Test Custodian organization addresses."""
        org = MockOrganization()
        custodian = Custodian(org)
        elem = custodian.to_element()

        assigned = elem.find(f"{{{NS}}}assignedCustodian")
        rep_org = assigned.find(f"{{{NS}}}representedCustodianOrganization")
        addr = rep_org.find(f"{{{NS}}}addr")
        assert addr is not None

    def test_custodian_organization_telecoms(self):
        """Test Custodian organization telecoms."""
        org = MockOrganization()
        custodian = Custodian(org)
        elem = custodian.to_element()

        assigned = elem.find(f"{{{NS}}}assignedCustodian")
        rep_org = assigned.find(f"{{{NS}}}representedCustodianOrganization")
        telecom = rep_org.find(f"{{{NS}}}telecom")
        assert telecom is not None


class TestHeaderIntegration:
    """Integration tests for header components."""

    def test_complete_header_structure(self):
        """Test building complete header with all components."""
        # Create mock data
        patient = MockPatient()
        author_data = MockAuthor(organization=MockOrganization())
        org = MockOrganization()

        # Build components
        record_target = RecordTarget(patient)
        author = Author(author_data)
        custodian = Custodian(org)

        # Create mock document header
        header = etree.Element("ClinicalDocument")
        header.append(record_target.to_element())
        header.append(author.to_element())
        header.append(custodian.to_element())

        # Verify structure
        assert header.find(f"{{{NS}}}recordTarget") is not None
        assert header.find(f"{{{NS}}}author") is not None
        assert header.find(f"{{{NS}}}custodian") is not None
