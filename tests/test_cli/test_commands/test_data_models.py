"""Tests for CLI data models."""

from datetime import datetime

import pytest

from ccdakit.cli.commands.data_models import (
    Address,
    Allergy,
    Author,
    DictWrapper,
    Immunization,
    Medication,
    Organization,
    Patient,
    Problem,
    Telecom,
    VitalSignsOrganizer,
)


class TestDictWrapper:
    """Tests for DictWrapper base class."""

    def test_basic_attribute_access(self):
        """Test basic attribute access through wrapper."""
        data = {"name": "John", "age": 30}
        wrapper = DictWrapper(data)

        assert wrapper.name == "John"
        assert wrapper.age == 30

    def test_missing_attribute_returns_none(self):
        """Test accessing missing attribute returns None."""
        data = {"name": "John"}
        wrapper = DictWrapper(data)

        assert wrapper.missing_key is None

    def test_private_attribute_raises_error(self):
        """Test accessing private attributes raises AttributeError."""
        data = {"name": "John"}
        wrapper = DictWrapper(data)

        with pytest.raises(AttributeError, match="has no attribute"):
            wrapper._private_attr


class TestAddress:
    """Tests for Address wrapper."""

    def test_address_with_all_fields(self):
        """Test Address with all fields."""
        data = {
            "street": "123 Main St",
            "city": "Boston",
            "state": "MA",
            "zip": "02101",
        }
        address = Address(data)

        assert address.street_lines == ["123 Main St"]
        assert address.city == "Boston"
        assert address.state == "MA"
        assert address.postal_code == "02101"
        assert address.country == "US"

    def test_address_empty_street(self):
        """Test Address with empty street."""
        data = {"street": "", "city": "Boston", "state": "MA", "zip": "02101"}
        address = Address(data)

        assert address.street_lines == []

    def test_address_missing_fields(self):
        """Test Address with missing fields."""
        data = {}
        address = Address(data)

        assert address.street_lines == []
        assert address.city == ""
        assert address.state == ""
        assert address.postal_code == ""
        assert address.country == "US"


class TestTelecom:
    """Tests for Telecom wrapper."""

    def test_telecom_with_phone(self):
        """Test Telecom with phone number."""
        data = {"phone": "555-1234"}
        telecom = Telecom(data)

        assert telecom.type == "phone"
        assert telecom.value == "555-1234"
        assert telecom.use == "home"

    def test_telecom_missing_phone(self):
        """Test Telecom with missing phone."""
        data = {}
        telecom = Telecom(data)

        assert telecom.value == ""


class TestPatient:
    """Tests for Patient wrapper."""

    def test_patient_with_full_data(self):
        """Test Patient with full data."""
        data = {
            "first_name": "John",
            "middle_name": "Q",
            "last_name": "Doe",
            "date_of_birth": "1980-01-01",
            "sex": "M",
            "race": "2106-3",
            "ethnicity": "2186-5",
            "language": "en",
            "ssn": "123-45-6789",
            "marital_status": "M",
            "addresses": [{"street": "123 Main St", "city": "Boston", "state": "MA", "zip": "02101"}],
            "telecoms": [{"phone": "555-1234"}],
        }
        patient = Patient(data)

        assert patient.first_name == "John"
        assert patient.middle_name == "Q"
        assert patient.last_name == "Doe"
        assert patient.date_of_birth == "1980-01-01"
        assert patient.sex == "M"
        assert patient.race == "2106-3"
        assert patient.ethnicity == "2186-5"
        assert patient.language == "en"
        assert patient.ssn == "123-45-6789"
        assert patient.marital_status == "M"
        assert len(patient.addresses) == 1
        assert isinstance(patient.addresses[0], Address)
        assert len(patient.telecoms) == 1
        assert isinstance(patient.telecoms[0], Telecom)

    def test_patient_with_minimal_data(self):
        """Test Patient with minimal data."""
        data = {"first_name": "John", "last_name": "Doe"}
        patient = Patient(data)

        assert patient.first_name == "John"
        assert patient.last_name == "Doe"
        assert patient.middle_name is None
        assert patient.sex == ""
        assert patient.race is None
        assert patient.ethnicity is None
        assert patient.language == "eng"
        assert patient.ssn is None
        assert patient.marital_status is None
        assert patient.addresses == []
        assert patient.telecoms == []

    def test_patient_empty_addresses_and_telecoms(self):
        """Test Patient with empty addresses and telecoms lists."""
        data = {"first_name": "John", "last_name": "Doe", "addresses": [], "telecoms": []}
        patient = Patient(data)

        assert patient.addresses == []
        assert patient.telecoms == []


class TestOrganization:
    """Tests for Organization wrapper."""

    def test_organization_with_full_data(self):
        """Test Organization with full data."""
        data = {
            "name": "Test Clinic",
            "npi": "1234567890",
            "tin": "12-3456789",
            "oid_root": "2.16.840.1.113883.3.TEST",
            "address": {"street": "123 Main St", "city": "Boston", "state": "MA", "zip": "02101"},
            "telecom": "555-1234",
        }
        org = Organization(data)

        assert org.name == "Test Clinic"
        assert org.npi == "1234567890"
        assert org.tin == "12-3456789"
        assert org.oid_root == "2.16.840.1.113883.3.TEST"
        assert len(org.addresses) == 1
        assert isinstance(org.addresses[0], Address)
        assert len(org.telecoms) == 1
        assert isinstance(org.telecoms[0], Telecom)

    def test_organization_with_minimal_data(self):
        """Test Organization with minimal data."""
        data = {}
        org = Organization(data)

        assert org.name == "Unknown Organization"
        assert org.npi is None
        assert org.tin is None
        assert org.oid_root is None
        assert org.addresses == []
        assert org.telecoms == []

    def test_organization_empty_address(self):
        """Test Organization with empty address."""
        data = {"name": "Test", "address": {}}
        org = Organization(data)

        # Empty dict should not create an address
        assert org.addresses == []

    def test_organization_empty_telecom(self):
        """Test Organization with empty telecom."""
        data = {"name": "Test", "telecom": ""}
        org = Organization(data)

        assert org.telecoms == []


class TestAuthor:
    """Tests for Author wrapper."""

    def test_author_with_full_data(self):
        """Test Author with full data."""
        now = datetime.now()
        data = {
            "first_name": "Jane",
            "middle_name": "M",
            "last_name": "Smith",
            "npi": "1234567890",
            "time": now,
        }
        author = Author(data)

        assert author.first_name == "Jane"
        assert author.middle_name == "M"
        assert author.last_name == "Smith"
        assert author.npi == "1234567890"
        assert author.time == now
        # Author provides default addresses/telecoms for C-CDA compliance
        assert len(author.addresses) == 1
        assert len(author.telecoms) == 1
        assert author.organization is None

    def test_author_with_minimal_data(self):
        """Test Author with minimal data."""
        data = {}
        author = Author(data)

        assert author.first_name == ""
        assert author.middle_name is None
        assert author.last_name == ""
        assert author.npi is None
        assert isinstance(author.time, datetime)
        # Author provides default addresses/telecoms for C-CDA compliance
        assert len(author.addresses) == 1
        assert len(author.telecoms) == 1
        assert author.organization is None


class TestProtocolWrappers:
    """Tests for protocol wrapper classes (passthrough)."""

    def test_problem_wrapper(self):
        """Test Problem wrapper."""
        data = {"code": "12345", "description": "Test problem"}
        problem = Problem(data)

        assert problem.code == "12345"
        assert problem.description == "Test problem"

    def test_medication_wrapper(self):
        """Test Medication wrapper."""
        data = {"name": "Aspirin", "dose": "81mg"}
        medication = Medication(data)

        assert medication.name == "Aspirin"
        assert medication.dose == "81mg"

    def test_allergy_wrapper(self):
        """Test Allergy wrapper."""
        data = {"substance": "Penicillin", "reaction": "Hives"}
        allergy = Allergy(data)

        assert allergy.substance == "Penicillin"
        assert allergy.reaction == "Hives"

    def test_immunization_wrapper(self):
        """Test Immunization wrapper."""
        data = {"vaccine": "COVID-19", "date": "2021-01-01"}
        immunization = Immunization(data)

        assert immunization.vaccine == "COVID-19"
        assert immunization.date == "2021-01-01"

    def test_vital_signs_organizer_wrapper(self):
        """Test VitalSignsOrganizer wrapper."""
        data = {"bp_systolic": "120", "bp_diastolic": "80"}
        vital_signs = VitalSignsOrganizer(data)

        assert vital_signs.bp_systolic == "120"
        assert vital_signs.bp_diastolic == "80"
