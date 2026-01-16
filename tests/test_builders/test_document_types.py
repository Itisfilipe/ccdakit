"""Tests for document-level builders (CCD, Discharge Summary, etc.)."""

from datetime import datetime

import pytest

from ccdakit.builders.documents import ContinuityOfCareDocument, DischargeSummary
from ccdakit.builders.sections.allergies import AllergiesSection
from ccdakit.builders.sections.discharge_medications import DischargeMedicationsSection
from ccdakit.builders.sections.hospital_discharge_instructions import (
    HospitalDischargeInstructionsSection,
)
from ccdakit.builders.sections.medications import MedicationsSection
from ccdakit.builders.sections.problems import ProblemsSection
from ccdakit.core.base import CDAVersion


class MockPatient:
    """Mock patient data model."""

    def __init__(self):
        self.first_name = "John"
        self.middle_name = "Q"
        self.last_name = "Doe"
        self.date_of_birth = datetime(1970, 5, 15)
        self.sex = "M"
        self.race = "2106-3"
        self.ethnicity = "2186-5"
        self.language = "eng"
        self.ssn = "123-45-6789"
        self.marital_status = "M"
        self.addresses = [MockAddress()]
        self.telecoms = [MockTelecom("phone", "617-555-1234", "home")]


class MockAddress:
    """Mock address data model."""

    def __init__(self):
        self.street_lines = ["123 Main St"]
        self.city = "Boston"
        self.state = "MA"
        self.postal_code = "02101"
        self.country = "US"


class MockTelecom:
    """Mock telecom data model."""

    def __init__(self, type_, value, use=None):
        self.type = type_
        self.value = value
        self.use = use


class MockOrganization:
    """Mock organization data model."""

    def __init__(self):
        self.name = "Test Hospital"
        self.npi = "1234567890"
        self.tin = None
        self.oid_root = "2.16.840.1.113883.3.TEST"
        self.addresses = [MockAddress()]
        self.telecoms = [MockTelecom("phone", "617-555-9999", "work")]


class MockAuthor:
    """Mock author data model."""

    def __init__(self):
        self.first_name = "Alice"
        self.middle_name = "M"
        self.last_name = "Smith"
        self.npi = "9876543210"
        self.time = datetime.now()
        self.addresses = [MockAddress()]
        self.telecoms = [MockTelecom("phone", "617-555-5555", "work")]
        self.organization = MockOrganization()


class MockProblem:
    """Mock problem data model."""

    def __init__(self):
        self.name = "Hypertension"
        self.code = "59621000"
        self.code_system = "SNOMED"
        self.status = "active"
        self.onset_date = datetime(2020, 1, 1)
        self.resolved_date = None
        self.persistent_id = None


class MockMedication:
    """Mock medication data model."""

    def __init__(self):
        self.name = "Lisinopril 10mg"
        self.code = "314076"
        self.dosage = "10 mg"
        self.route = "oral"
        self.frequency = "once daily"
        self.start_date = datetime(2020, 1, 1)
        self.end_date = None
        self.status = "active"
        self.instructions = "Take in morning"


class MockAllergy:
    """Mock allergy data model."""

    def __init__(self):
        self.allergen = "Penicillin"
        self.allergen_code = "373270004"
        self.allergen_code_system = "SNOMED"
        self.reaction = "Hives"
        self.reaction_code = "247472004"
        self.severity = "moderate"
        self.status = "active"
        self.onset_date = datetime(2015, 5, 10)


class MockDischargeInstruction:
    """Mock discharge instruction data model."""

    def __init__(self):
        self.text = "Follow up with primary care physician in 2 weeks"
        self.instruction_text = "Follow up with primary care physician in 2 weeks"
        self.narrative_text = "Follow up with primary care physician in 2 weeks"
        self.code = "instruction"
        self.instruction_category = "follow-up"


class TestContinuityOfCareDocument:
    """Test suite for ContinuityOfCareDocument."""

    @pytest.fixture
    def patient(self):
        """Create test patient."""
        return MockPatient()

    @pytest.fixture
    def author(self):
        """Create test author."""
        return MockAuthor()

    @pytest.fixture
    def custodian(self):
        """Create test custodian."""
        return MockOrganization()

    @pytest.fixture
    def problems(self):
        """Create test problems."""
        return [MockProblem()]

    @pytest.fixture
    def medications(self):
        """Create test medications."""
        return [MockMedication()]

    @pytest.fixture
    def allergies(self):
        """Create test allergies."""
        return [MockAllergy()]

    def test_ccd_basic_creation(self, patient, author, custodian):
        """Test creating basic CCD without sections."""
        doc = ContinuityOfCareDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            version=CDAVersion.R2_1,
        )

        assert doc is not None
        assert doc.title == "Continuity of Care Document"

    def test_ccd_has_correct_templates(self, patient, author, custodian):
        """Test CCD includes both base and CCD-specific template IDs."""
        doc = ContinuityOfCareDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            version=CDAVersion.R2_1,
        )

        elem = doc.to_element()

        # Should have 2 templateIds: base C-CDA and CCD-specific
        template_ids = elem.findall(".//{urn:hl7-org:v3}templateId")
        template_roots = [tid.get("root") for tid in template_ids[:2]]  # First 2 are document-level

        assert "2.16.840.1.113883.10.20.22.1.1" in template_roots  # Base C-CDA
        assert "2.16.840.1.113883.10.20.22.1.2" in template_roots  # CCD

    def test_ccd_has_correct_document_code(self, patient, author, custodian):
        """Test CCD uses correct LOINC code."""
        doc = ContinuityOfCareDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            version=CDAVersion.R2_1,
        )

        elem = doc.to_element()

        # Find code element
        code_elem = elem.find(".//{urn:hl7-org:v3}code")
        assert code_elem is not None
        assert code_elem.get("code") == "34133-9"
        assert code_elem.get("displayName") == "Summarization of Episode Note"

    def test_ccd_with_sections(self, patient, author, custodian, problems, medications):
        """Test CCD with clinical sections."""
        problems_section = ProblemsSection(problems=problems, version=CDAVersion.R2_1)
        meds_section = MedicationsSection(medications=medications, version=CDAVersion.R2_1)

        doc = ContinuityOfCareDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=[problems_section, meds_section],
            version=CDAVersion.R2_1,
        )

        elem = doc.to_element()

        # Should have structuredBody with 2 sections
        sections = elem.findall(
            ".//{urn:hl7-org:v3}structuredBody/{urn:hl7-org:v3}component/{urn:hl7-org:v3}section"
        )
        assert len(sections) == 2

    def test_ccd_validate_required_sections_missing(self, patient, author, custodian):
        """Test validation detects missing required sections."""
        doc = ContinuityOfCareDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=[],  # No sections
            version=CDAVersion.R2_1,
        )

        is_valid, missing = doc.validate_required_sections()

        assert is_valid is False
        assert len(missing) == 3  # Problems, Medications, Allergies
        assert "Problems Section" in missing
        assert "Medications Section" in missing
        assert "Allergies Section" in missing

    def test_ccd_validate_required_sections_complete(
        self, patient, author, custodian, problems, medications, allergies
    ):
        """Test validation passes with all required sections."""
        problems_section = ProblemsSection(problems=problems, version=CDAVersion.R2_1)
        meds_section = MedicationsSection(medications=medications, version=CDAVersion.R2_1)
        allergies_section = AllergiesSection(allergies=allergies, version=CDAVersion.R2_1)

        doc = ContinuityOfCareDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=[problems_section, meds_section, allergies_section],
            version=CDAVersion.R2_1,
        )

        is_valid, missing = doc.validate_required_sections()

        assert is_valid is True
        assert len(missing) == 0

    def test_ccd_to_xml_string(self, patient, author, custodian):
        """Test converting CCD to XML string."""
        doc = ContinuityOfCareDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()

        # Check for XML declaration (may use single or double quotes)
        assert xml_string.startswith("<?xml version=")
        assert 'encoding="UTF-8"' in xml_string or "encoding='UTF-8'" in xml_string
        assert "<ClinicalDocument" in xml_string
        assert "Continuity of Care Document" in xml_string

    def test_ccd_r20_templates(self, patient, author, custodian):
        """Test CCD R2.0 uses correct template versions."""
        doc = ContinuityOfCareDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            version=CDAVersion.R2_0,
        )

        elem = doc.to_element()

        # Find template IDs
        template_ids = elem.findall(".//{urn:hl7-org:v3}templateId")

        # Check for R2.0 extension
        extensions = [tid.get("extension") for tid in template_ids if tid.get("extension")]
        assert "2014-06-09" in extensions


class TestDischargeSummary:
    """Test suite for DischargeSummary."""

    @pytest.fixture
    def patient(self):
        """Create test patient."""
        return MockPatient()

    @pytest.fixture
    def author(self):
        """Create test author."""
        return MockAuthor()

    @pytest.fixture
    def custodian(self):
        """Create test custodian."""
        return MockOrganization()

    @pytest.fixture
    def discharge_medications(self):
        """Create test discharge medications."""
        return [MockMedication()]

    @pytest.fixture
    def discharge_instructions(self):
        """Create test discharge instructions."""
        return [MockDischargeInstruction()]

    def test_discharge_summary_basic_creation(self, patient, author, custodian):
        """Test creating basic Discharge Summary."""
        doc = DischargeSummary(
            patient=patient,
            author=author,
            custodian=custodian,
            version=CDAVersion.R2_1,
        )

        assert doc is not None
        assert doc.title == "Discharge Summary"

    def test_discharge_summary_has_correct_templates(self, patient, author, custodian):
        """Test Discharge Summary includes correct template IDs."""
        doc = DischargeSummary(
            patient=patient,
            author=author,
            custodian=custodian,
            version=CDAVersion.R2_1,
        )

        elem = doc.to_element()

        # Should have 2 templateIds: base C-CDA and Discharge Summary-specific
        template_ids = elem.findall(".//{urn:hl7-org:v3}templateId")
        template_roots = [tid.get("root") for tid in template_ids[:2]]

        assert "2.16.840.1.113883.10.20.22.1.1" in template_roots  # Base C-CDA
        assert "2.16.840.1.113883.10.20.22.1.8" in template_roots  # Discharge Summary

    def test_discharge_summary_has_correct_document_code(self, patient, author, custodian):
        """Test Discharge Summary uses correct LOINC code."""
        doc = DischargeSummary(
            patient=patient,
            author=author,
            custodian=custodian,
            version=CDAVersion.R2_1,
        )

        elem = doc.to_element()

        # Find code element
        code_elem = elem.find(".//{urn:hl7-org:v3}code")
        assert code_elem is not None
        assert code_elem.get("code") == "18842-5"
        assert code_elem.get("displayName") == "Discharge Summarization Note"

    def test_discharge_summary_with_dates(self, patient, author, custodian):
        """Test Discharge Summary with admission and discharge dates."""
        admission_date = datetime(2024, 1, 15, 8, 0)
        discharge_date = datetime(2024, 1, 20, 14, 30)

        doc = DischargeSummary(
            patient=patient,
            author=author,
            custodian=custodian,
            admission_date=admission_date,
            discharge_date=discharge_date,
            version=CDAVersion.R2_1,
        )

        elem = doc.to_element()

        # Should have documentationOf/serviceEvent
        service_event = elem.find(".//{urn:hl7-org:v3}documentationOf/{urn:hl7-org:v3}serviceEvent")
        assert service_event is not None
        assert service_event.get("classCode") == "PCPR"

        # Check dates
        effective_time = service_event.find(".//{urn:hl7-org:v3}effectiveTime")
        assert effective_time is not None

        low = effective_time.find(".//{urn:hl7-org:v3}low")
        assert low is not None
        assert low.get("value").startswith("20240115080000")

        high = effective_time.find(".//{urn:hl7-org:v3}high")
        assert high is not None
        assert high.get("value").startswith("20240120143000")

    def test_discharge_summary_uses_discharge_date_as_effective_time(
        self, patient, author, custodian
    ):
        """Test that discharge date is used as effective time if not provided."""
        discharge_date = datetime(2024, 1, 20, 14, 30)

        doc = DischargeSummary(
            patient=patient,
            author=author,
            custodian=custodian,
            discharge_date=discharge_date,
            version=CDAVersion.R2_1,
        )

        assert doc.effective_time == discharge_date

    def test_discharge_summary_with_sections(
        self, patient, author, custodian, discharge_medications, discharge_instructions
    ):
        """Test Discharge Summary with discharge-specific sections."""
        meds_section = DischargeMedicationsSection(
            medications=discharge_medications, version=CDAVersion.R2_1
        )
        instructions_section = HospitalDischargeInstructionsSection(
            instructions=discharge_instructions, version=CDAVersion.R2_1
        )

        doc = DischargeSummary(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=[meds_section, instructions_section],
            version=CDAVersion.R2_1,
        )

        elem = doc.to_element()

        # Should have structuredBody with 2 sections
        sections = elem.findall(
            ".//{urn:hl7-org:v3}structuredBody/{urn:hl7-org:v3}component/{urn:hl7-org:v3}section"
        )
        assert len(sections) == 2

    def test_discharge_summary_validate_sections_missing(self, patient, author, custodian):
        """Test validation detects missing recommended sections."""
        doc = DischargeSummary(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=[],
            version=CDAVersion.R2_1,
        )

        has_all, missing = doc.validate_discharge_sections()

        assert has_all is False
        assert len(missing) > 0
        assert any("Discharge Medications" in s for s in missing)

    def test_discharge_summary_to_xml_string(self, patient, author, custodian):
        """Test converting Discharge Summary to XML string."""
        doc = DischargeSummary(
            patient=patient,
            author=author,
            custodian=custodian,
            admission_date=datetime(2024, 1, 15),
            discharge_date=datetime(2024, 1, 20),
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()

        # Check for XML declaration (may use single or double quotes)
        assert xml_string.startswith("<?xml version=")
        assert 'encoding="UTF-8"' in xml_string or "encoding='UTF-8'" in xml_string
        assert "<ClinicalDocument" in xml_string
        assert "Discharge Summary" in xml_string
        assert "documentationOf" in xml_string
