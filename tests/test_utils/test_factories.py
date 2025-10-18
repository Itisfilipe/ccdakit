"""Tests for document factories."""

from datetime import date, datetime

from lxml import etree

from ccdakit.core.base import CDAVersion
from ccdakit.utils.factories import (
    ConsultationNote,
    ContinuityOfCareDocument,
    DischargeSummary,
    DocumentFactory,
    ProgressNote,
)


class MockAddress:
    """Mock address for testing."""

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


class MockTelecom:
    """Mock telecom for testing."""

    @property
    def type(self):
        return "phone"

    @property
    def value(self):
        return "617-555-1234"

    @property
    def use(self):
        return "home"


class MockPatient:
    """Mock patient for testing."""

    @property
    def first_name(self):
        return "John"

    @property
    def last_name(self):
        return "Doe"

    @property
    def middle_name(self):
        return "Q"

    @property
    def date_of_birth(self):
        return date(1970, 1, 1)

    @property
    def sex(self):
        return "M"

    @property
    def race(self):
        return "2106-3"

    @property
    def ethnicity(self):
        return "2186-5"

    @property
    def language(self):
        return "eng"

    @property
    def ssn(self):
        return "123-45-6789"

    @property
    def addresses(self):
        return [MockAddress()]

    @property
    def telecoms(self):
        return [MockTelecom()]

    @property
    def marital_status(self):
        return "M"


class MockOrganization:
    """Mock organization for testing."""

    @property
    def name(self):
        return "Example Medical Center"

    @property
    def npi(self):
        return "1234567890"

    @property
    def tin(self):
        return None

    @property
    def oid_root(self):
        return "2.16.840.1.113883.3.TEST"

    @property
    def addresses(self):
        return [MockAddress()]

    @property
    def telecoms(self):
        return [MockTelecom()]


class MockAuthor:
    """Mock author for testing."""

    @property
    def first_name(self):
        return "Alice"

    @property
    def last_name(self):
        return "Smith"

    @property
    def middle_name(self):
        return "M"

    @property
    def npi(self):
        return "9876543210"

    @property
    def addresses(self):
        return [MockAddress()]

    @property
    def telecoms(self):
        return [MockTelecom()]

    @property
    def time(self):
        return datetime(2023, 10, 17, 14, 30)

    @property
    def organization(self):
        return MockOrganization()


class TestDocumentFactory:
    """Tests for DocumentFactory class."""

    def test_create_continuity_of_care_document(self):
        """Test creating a CCD using factory."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = DocumentFactory.create_continuity_of_care_document(
            patient=patient, author=author, custodian=custodian
        )

        assert isinstance(doc, ContinuityOfCareDocument)
        assert doc.patient == patient
        assert doc.author == author
        assert doc.custodian == custodian

    def test_create_discharge_summary(self):
        """Test creating a Discharge Summary using factory."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = DocumentFactory.create_discharge_summary(
            patient=patient, author=author, custodian=custodian
        )

        assert isinstance(doc, DischargeSummary)
        assert doc.patient == patient
        assert doc.author == author
        assert doc.custodian == custodian

    def test_create_progress_note(self):
        """Test creating a Progress Note using factory."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = DocumentFactory.create_progress_note(
            patient=patient, author=author, custodian=custodian
        )

        assert isinstance(doc, ProgressNote)
        assert doc.patient == patient
        assert doc.author == author
        assert doc.custodian == custodian

    def test_create_consultation_note(self):
        """Test creating a Consultation Note using factory."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = DocumentFactory.create_consultation_note(
            patient=patient, author=author, custodian=custodian
        )

        assert isinstance(doc, ConsultationNote)
        assert doc.patient == patient
        assert doc.author == author
        assert doc.custodian == custodian

    def test_factory_with_custom_effective_time(self):
        """Test factory with custom effective time."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()
        custom_time = datetime(2023, 5, 15, 10, 30)

        doc = DocumentFactory.create_continuity_of_care_document(
            patient=patient,
            author=author,
            custodian=custodian,
            effective_time=custom_time,
        )

        assert doc.effective_time == custom_time

    def test_factory_with_custom_document_id(self):
        """Test factory with custom document ID."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = DocumentFactory.create_continuity_of_care_document(
            patient=patient,
            author=author,
            custodian=custodian,
            document_id="CUSTOM-DOC-123",
        )

        assert doc.document_id == "CUSTOM-DOC-123"

    def test_factory_with_r20_version(self):
        """Test factory with R2.0 version."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = DocumentFactory.create_continuity_of_care_document(
            patient=patient,
            author=author,
            custodian=custodian,
            version=CDAVersion.R2_0,
        )

        assert doc.version == CDAVersion.R2_0


class TestContinuityOfCareDocument:
    """Tests for ContinuityOfCareDocument class."""

    def test_ccd_has_correct_templates_r21(self):
        """Test CCD has correct template IDs for R2.1."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ContinuityOfCareDocument(
            patient=patient, author=author, custodian=custodian, version=CDAVersion.R2_1
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        template_ids = elem.findall(".//c:templateId", ns)

        # Should have at least 2 template IDs (general C-CDA + CCD)
        assert len(template_ids) >= 2

        # Check for CCD template
        ccd_templates = [
            t for t in template_ids if t.get("root") == "2.16.840.1.113883.10.20.22.1.2"
        ]
        assert len(ccd_templates) == 1
        assert ccd_templates[0].get("extension") == "2015-08-01"

    def test_ccd_has_correct_templates_r20(self):
        """Test CCD has correct template IDs for R2.0."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ContinuityOfCareDocument(
            patient=patient, author=author, custodian=custodian, version=CDAVersion.R2_0
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        template_ids = elem.findall(".//c:templateId", ns)

        # Check for CCD template
        ccd_templates = [
            t for t in template_ids if t.get("root") == "2.16.840.1.113883.10.20.22.1.2"
        ]
        assert len(ccd_templates) == 1
        assert ccd_templates[0].get("extension") == "2014-06-09"

    def test_ccd_has_correct_document_code(self):
        """Test CCD has correct LOINC document code."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ContinuityOfCareDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        code = elem.find(".//c:code", ns)
        assert code is not None
        assert code.get("code") == "34133-9"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC

    def test_ccd_has_correct_title(self):
        """Test CCD has correct default title."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ContinuityOfCareDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        title = elem.find(".//c:title", ns)
        assert title is not None
        assert title.text == "Continuity of Care Document"

    def test_ccd_custom_title(self):
        """Test CCD with custom title."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ContinuityOfCareDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            title="Custom CCD Title",
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        title = elem.find(".//c:title", ns)
        assert title is not None
        assert title.text == "Custom CCD Title"

    def test_ccd_to_xml_string(self):
        """Test CCD serialization to XML string."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ContinuityOfCareDocument(patient=patient, author=author, custodian=custodian)
        xml_string = doc.to_xml_string()

        assert "<?xml version=" in xml_string
        assert "<ClinicalDocument" in xml_string
        assert "</ClinicalDocument>" in xml_string

        # Verify it's valid XML
        parsed = etree.fromstring(xml_string.encode("UTF-8"))
        assert parsed.tag == "{urn:hl7-org:v3}ClinicalDocument"


class TestDischargeSummary:
    """Tests for DischargeSummary class."""

    def test_discharge_summary_has_correct_templates_r21(self):
        """Test Discharge Summary has correct template IDs for R2.1."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = DischargeSummary(
            patient=patient, author=author, custodian=custodian, version=CDAVersion.R2_1
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        template_ids = elem.findall(".//c:templateId", ns)

        # Check for Discharge Summary template
        discharge_templates = [
            t for t in template_ids if t.get("root") == "2.16.840.1.113883.10.20.22.1.8"
        ]
        assert len(discharge_templates) == 1
        assert discharge_templates[0].get("extension") == "2015-08-01"

    def test_discharge_summary_has_correct_templates_r20(self):
        """Test Discharge Summary has correct template IDs for R2.0."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = DischargeSummary(
            patient=patient, author=author, custodian=custodian, version=CDAVersion.R2_0
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        template_ids = elem.findall(".//c:templateId", ns)

        # Check for Discharge Summary template
        discharge_templates = [
            t for t in template_ids if t.get("root") == "2.16.840.1.113883.10.20.22.1.8"
        ]
        assert len(discharge_templates) == 1
        assert discharge_templates[0].get("extension") == "2014-06-09"

    def test_discharge_summary_has_correct_document_code(self):
        """Test Discharge Summary has correct LOINC document code."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = DischargeSummary(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        code = elem.find(".//c:code", ns)
        assert code is not None
        assert code.get("code") == "18842-5"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC

    def test_discharge_summary_has_correct_title(self):
        """Test Discharge Summary has correct default title."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = DischargeSummary(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        title = elem.find(".//c:title", ns)
        assert title is not None
        assert title.text == "Discharge Summary"


class TestProgressNote:
    """Tests for ProgressNote class."""

    def test_progress_note_has_correct_templates_r21(self):
        """Test Progress Note has correct template IDs for R2.1."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ProgressNote(
            patient=patient, author=author, custodian=custodian, version=CDAVersion.R2_1
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        template_ids = elem.findall(".//c:templateId", ns)

        # Check for Progress Note template
        progress_templates = [
            t for t in template_ids if t.get("root") == "2.16.840.1.113883.10.20.22.1.9"
        ]
        assert len(progress_templates) == 1
        assert progress_templates[0].get("extension") == "2015-08-01"

    def test_progress_note_has_correct_templates_r20(self):
        """Test Progress Note has correct template IDs for R2.0."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ProgressNote(
            patient=patient, author=author, custodian=custodian, version=CDAVersion.R2_0
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        template_ids = elem.findall(".//c:templateId", ns)

        # Check for Progress Note template
        progress_templates = [
            t for t in template_ids if t.get("root") == "2.16.840.1.113883.10.20.22.1.9"
        ]
        assert len(progress_templates) == 1
        assert progress_templates[0].get("extension") == "2014-06-09"

    def test_progress_note_has_correct_document_code(self):
        """Test Progress Note has correct LOINC document code."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ProgressNote(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        code = elem.find(".//c:code", ns)
        assert code is not None
        assert code.get("code") == "11506-3"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC

    def test_progress_note_has_correct_title(self):
        """Test Progress Note has correct default title."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ProgressNote(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        title = elem.find(".//c:title", ns)
        assert title is not None
        assert title.text == "Progress Note"


class TestConsultationNote:
    """Tests for ConsultationNote class."""

    def test_consultation_note_has_correct_templates_r21(self):
        """Test Consultation Note has correct template IDs for R2.1."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ConsultationNote(
            patient=patient, author=author, custodian=custodian, version=CDAVersion.R2_1
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        template_ids = elem.findall(".//c:templateId", ns)

        # Check for Consultation Note template
        consultation_templates = [
            t for t in template_ids if t.get("root") == "2.16.840.1.113883.10.20.22.1.4"
        ]
        assert len(consultation_templates) == 1
        assert consultation_templates[0].get("extension") == "2015-08-01"

    def test_consultation_note_has_correct_templates_r20(self):
        """Test Consultation Note has correct template IDs for R2.0."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ConsultationNote(
            patient=patient, author=author, custodian=custodian, version=CDAVersion.R2_0
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        template_ids = elem.findall(".//c:templateId", ns)

        # Check for Consultation Note template
        consultation_templates = [
            t for t in template_ids if t.get("root") == "2.16.840.1.113883.10.20.22.1.4"
        ]
        assert len(consultation_templates) == 1
        assert consultation_templates[0].get("extension") == "2014-06-09"

    def test_consultation_note_has_correct_document_code(self):
        """Test Consultation Note has correct LOINC document code."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ConsultationNote(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        code = elem.find(".//c:code", ns)
        assert code is not None
        assert code.get("code") == "11488-4"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC

    def test_consultation_note_has_correct_title(self):
        """Test Consultation Note has correct default title."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ConsultationNote(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        title = elem.find(".//c:title", ns)
        assert title is not None
        assert title.text == "Consultation Note"


class TestDocumentIntegration:
    """Integration tests for factory-created documents."""

    def test_all_document_types_generate_valid_xml(self):
        """Test that all document types generate valid XML."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        # Create all document types
        documents = [
            DocumentFactory.create_continuity_of_care_document(
                patient=patient, author=author, custodian=custodian
            ),
            DocumentFactory.create_discharge_summary(
                patient=patient, author=author, custodian=custodian
            ),
            DocumentFactory.create_progress_note(
                patient=patient, author=author, custodian=custodian
            ),
            DocumentFactory.create_consultation_note(
                patient=patient, author=author, custodian=custodian
            ),
        ]

        # Each should generate valid XML
        for doc in documents:
            xml_string = doc.to_xml_string()
            assert xml_string is not None
            assert len(xml_string) > 0

            # Parse and verify
            parsed = etree.fromstring(xml_string.encode("UTF-8"))
            assert parsed.tag == "{urn:hl7-org:v3}ClinicalDocument"

    def test_document_has_required_header_elements(self):
        """Test that factory-created documents have required header elements."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = DocumentFactory.create_continuity_of_care_document(
            patient=patient, author=author, custodian=custodian
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}

        # Check required header elements
        assert elem.find(".//c:realmCode", ns) is not None
        assert elem.find(".//c:typeId", ns) is not None
        assert len(elem.findall(".//c:templateId", ns)) >= 1
        assert elem.find(".//c:id", ns) is not None
        assert elem.find(".//c:code", ns) is not None
        assert elem.find(".//c:title", ns) is not None
        assert elem.find(".//c:effectiveTime", ns) is not None
        assert elem.find(".//c:confidentialityCode", ns) is not None
        assert elem.find(".//c:languageCode", ns) is not None
        assert elem.find(".//c:recordTarget", ns) is not None
        assert elem.find(".//c:author", ns) is not None
        assert elem.find(".//c:custodian", ns) is not None

    def test_factory_preserves_version_across_document_types(self):
        """Test that version parameter is preserved across document types."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        for version in [CDAVersion.R2_1, CDAVersion.R2_0]:
            doc_ccd = DocumentFactory.create_continuity_of_care_document(
                patient=patient, author=author, custodian=custodian, version=version
            )
            doc_discharge = DocumentFactory.create_discharge_summary(
                patient=patient, author=author, custodian=custodian, version=version
            )
            doc_progress = DocumentFactory.create_progress_note(
                patient=patient, author=author, custodian=custodian, version=version
            )
            doc_consult = DocumentFactory.create_consultation_note(
                patient=patient, author=author, custodian=custodian, version=version
            )

            assert doc_ccd.version == version
            assert doc_discharge.version == version
            assert doc_progress.version == version
            assert doc_consult.version == version
