"""Tests for ClinicalDocument builder."""

from datetime import date, datetime
from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.document import ClinicalDocument
from ccdakit.core.base import CDAVersion


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

    @property
    def type(self) -> str:
        return "phone"

    @property
    def value(self) -> str:
        return "617-555-1234"

    @property
    def use(self) -> Optional[str]:
        return "home"


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

    @property
    def name(self) -> str:
        return "Example Medical Center"

    @property
    def npi(self) -> Optional[str]:
        return "1234567890"

    @property
    def tin(self) -> Optional[str]:
        return None

    @property
    def oid_root(self) -> Optional[str]:
        return "2.16.840.1.113883.3.TEST"

    @property
    def addresses(self) -> Sequence[MockAddress]:
        return [MockAddress()]

    @property
    def telecoms(self) -> Sequence[MockTelecom]:
        return [MockTelecom()]


class MockAuthor:
    """Mock author for testing."""

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
        return MockOrganization()


class TestClinicalDocument:
    """Tests for ClinicalDocument builder."""

    def test_clinical_document_basic(self):
        """Test basic ClinicalDocument creation."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        assert elem.tag == "{urn:hl7-org:v3}ClinicalDocument"

    def test_clinical_document_has_namespaces(self):
        """Test ClinicalDocument includes proper namespaces."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        # Check namespaces
        nsmap = elem.nsmap
        assert nsmap[None] == "urn:hl7-org:v3"
        assert nsmap["xsi"] == "http://www.w3.org/2001/XMLSchema-instance"
        assert nsmap["sdtc"] == "urn:hl7-org:sdtc"

    def test_clinical_document_has_realm_code(self):
        """Test ClinicalDocument includes realmCode."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        # Search using XPath with namespace
        ns = {"c": "urn:hl7-org:v3"}
        realm = elem.find(".//c:realmCode", ns)
        assert realm is not None
        assert realm.get("code") == "US"

    def test_clinical_document_has_type_id(self):
        """Test ClinicalDocument includes typeId."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        type_id = elem.find(".//c:typeId", ns)
        assert type_id is not None
        assert type_id.get("root") == "2.16.840.1.113883.1.3"
        assert type_id.get("extension") == "POCD_HD000040"

    def test_clinical_document_has_template_id(self):
        """Test ClinicalDocument includes templateId."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(
            patient=patient, author=author, custodian=custodian, version=CDAVersion.R2_1
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        template_ids = elem.findall(".//c:templateId", ns)
        assert len(template_ids) >= 1
        assert template_ids[0].get("root") == "2.16.840.1.113883.10.20.22.1.1"
        assert template_ids[0].get("extension") == "2015-08-01"

    def test_clinical_document_has_id(self):
        """Test ClinicalDocument includes document id."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            document_id="TEST-DOC-123",
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        doc_id = elem.find(".//c:id", ns)
        assert doc_id is not None
        assert doc_id.get("extension") == "TEST-DOC-123"

    def test_clinical_document_has_code(self):
        """Test ClinicalDocument includes document type code."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        code = elem.find(".//c:code", ns)
        assert code is not None
        assert code.get("code") == "34133-9"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC

    def test_clinical_document_has_title(self):
        """Test ClinicalDocument includes title."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            title="Patient Summary",
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        title = elem.find(".//c:title", ns)
        assert title is not None
        assert title.text == "Patient Summary"

    def test_clinical_document_has_effective_time(self):
        """Test ClinicalDocument includes effectiveTime."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()
        eff_time = datetime(2023, 10, 17, 15, 30)

        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            effective_time=eff_time,
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        effective_time = elem.find(".//c:effectiveTime", ns)
        assert effective_time is not None
        assert effective_time.get("value") == "20231017153000"

    def test_clinical_document_has_confidentiality_code(self):
        """Test ClinicalDocument includes confidentialityCode."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        conf_code = elem.find(".//c:confidentialityCode", ns)
        assert conf_code is not None
        assert conf_code.get("code") == "N"

    def test_clinical_document_has_language_code(self):
        """Test ClinicalDocument includes languageCode."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        lang = elem.find(".//c:languageCode", ns)
        assert lang is not None
        assert lang.get("code") == "en-US"

    def test_clinical_document_has_record_target(self):
        """Test ClinicalDocument includes recordTarget."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        record_target = elem.find(".//c:recordTarget", ns)
        assert record_target is not None

    def test_clinical_document_has_author(self):
        """Test ClinicalDocument includes author."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        author_elem = elem.find(".//c:author", ns)
        assert author_elem is not None

    def test_clinical_document_has_custodian(self):
        """Test ClinicalDocument includes custodian."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        custodian_elem = elem.find(".//c:custodian", ns)
        assert custodian_elem is not None

    def test_clinical_document_to_xml_string(self):
        """Test ClinicalDocument serialization to XML string."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(patient=patient, author=author, custodian=custodian)
        xml_string = doc.to_xml_string()

        # Accept either single or double quotes in XML declaration
        assert xml_string.startswith(
            '<?xml version="1.0" encoding="UTF-8"?>'
        ) or xml_string.startswith("<?xml version='1.0' encoding='UTF-8'?>")
        assert "<ClinicalDocument" in xml_string
        assert "</ClinicalDocument>" in xml_string

    def test_clinical_document_r21_version(self):
        """Test ClinicalDocument with R2.1 version."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            version=CDAVersion.R2_1,
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        template_ids = elem.findall(".//c:templateId", ns)
        assert any(t.get("extension") == "2015-08-01" for t in template_ids)

    def test_clinical_document_r20_version(self):
        """Test ClinicalDocument with R2.0 version."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            version=CDAVersion.R2_0,
        )
        elem = doc.to_element()

        ns = {"c": "urn:hl7-org:v3"}
        template_ids = elem.findall(".//c:templateId", ns)
        assert any(t.get("extension") == "2014-06-09" for t in template_ids)

    def test_clinical_document_structure_order(self):
        """Test that ClinicalDocument elements are in correct order."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        # Get all child element tags (without namespace)
        tags = [child.tag.split("}")[1] if "}" in child.tag else child.tag for child in elem]

        # Verify expected order
        assert tags[0] == "realmCode"
        assert tags[1] == "typeId"
        assert "templateId" in tags[2]
        assert "id" in tags
        assert "code" in tags
        assert "title" in tags
        assert "recordTarget" in tags
        assert "author" in tags
        assert "custodian" in tags


class TestClinicalDocumentIntegration:
    """Integration tests for ClinicalDocument."""

    def test_complete_document_creation(self):
        """Test creating a complete valid ClinicalDocument."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            title="Patient Clinical Summary",
            document_id="DOC-12345",
            effective_time=datetime(2023, 10, 17, 10, 0),
        )

        xml_string = doc.to_xml_string(pretty=True)

        # Verify it's valid XML
        parsed = etree.fromstring(xml_string.encode("UTF-8"))
        assert parsed.tag == "{urn:hl7-org:v3}ClinicalDocument"

    def test_document_without_sections(self):
        """Test document without sections (header only)."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(patient=patient, author=author, custodian=custodian)
        elem = doc.to_element()

        # Should not have component when no sections
        ns = {"c": "urn:hl7-org:v3"}
        component = elem.find(".//c:component", ns)
        assert component is None
