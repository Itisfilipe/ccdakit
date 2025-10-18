"""Integration tests for complete C-CDA document generation."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.document import ClinicalDocument
from ccdakit.builders.sections.medications import MedicationsSection
from ccdakit.builders.sections.problems import ProblemsSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


# ============================================================================
# Mock Data Classes
# ============================================================================


class MockAddress:
    """Mock address for testing."""

    @property
    def street_lines(self):
        return ["123 Main St", "Suite 400"]

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

    def __init__(self, type_="phone", value="617-555-1234", use="home"):
        self._type = type_
        self._value = value
        self._use = use

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @property
    def use(self):
        return self._use


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
        return date(1970, 5, 15)

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
        return "Community Health Center"

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
        return [MockTelecom(type_="phone", value="617-555-9999", use="work")]


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


class MockProblem:
    """Mock problem for testing."""

    def __init__(
        self,
        name="Type 2 Diabetes Mellitus",
        code="44054006",
        code_system="SNOMED",
        onset_date=date(2020, 1, 15),
        resolved_date=None,
        status="active",
        persistent_id=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._onset_date = onset_date
        self._resolved_date = resolved_date
        self._status = status
        self._persistent_id = persistent_id

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def onset_date(self):
        return self._onset_date

    @property
    def resolved_date(self):
        return self._resolved_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class MockMedication:
    """Mock medication for testing."""

    def __init__(
        self,
        name="Lisinopril 10mg tablet",
        code="314076",
        dosage="10 mg",
        route="oral",
        frequency="once daily",
        start_date=date(2020, 1, 1),
        end_date=None,
        status="active",
        instructions=None,
    ):
        self._name = name
        self._code = code
        self._dosage = dosage
        self._route = route
        self._frequency = frequency
        self._start_date = start_date
        self._end_date = end_date
        self._status = status
        self._instructions = instructions

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def dosage(self):
        return self._dosage

    @property
    def route(self):
        return self._route

    @property
    def frequency(self):
        return self._frequency

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def status(self):
        return self._status

    @property
    def instructions(self):
        return self._instructions


# ============================================================================
# Integration Tests
# ============================================================================


class TestCompleteCCDADocument:
    """Integration tests for complete C-CDA document generation."""

    def test_minimal_document(self):
        """Test generating minimal complete C-CDA document."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        # Create document
        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
        )

        # Generate XML
        elem = doc.to_element()

        # Verify it's a valid document
        assert local_name(elem) == "ClinicalDocument"

        # Verify namespaces
        nsmap = elem.nsmap
        assert nsmap[None] == "urn:hl7-org:v3"
        assert nsmap["xsi"] == "http://www.w3.org/2001/XMLSchema-instance"

        # Verify required header elements
        assert elem.find(f"{{{NS}}}realmCode") is not None
        assert elem.find(f"{{{NS}}}typeId") is not None
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}confidentialityCode") is not None
        assert elem.find(f"{{{NS}}}languageCode") is not None
        assert elem.find(f"{{{NS}}}recordTarget") is not None
        assert elem.find(f"{{{NS}}}author") is not None
        assert elem.find(f"{{{NS}}}custodian") is not None

    def test_document_with_problems_section(self):
        """Test C-CDA document with problems section."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        # Create problems
        problems = [
            MockProblem(
                name="Essential Hypertension",
                code="59621000",
                code_system="SNOMED",
                status="active",
                onset_date=date(2018, 5, 10),
            ),
            MockProblem(
                name="Type 2 Diabetes Mellitus",
                code="44054006",
                code_system="SNOMED",
                status="active",
                onset_date=date(2019, 3, 15),
            ),
        ]

        # Create problems section
        problems_section = ProblemsSection(problems=problems, version=CDAVersion.R2_1)

        # Create document with sections
        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=[problems_section],
            title="Patient Summary",
            document_id="DOC-2023-12345",
            effective_time=datetime(2023, 10, 17, 10, 30),
            version=CDAVersion.R2_1,
        )

        elem = doc.to_element()

        # Verify document structure
        assert local_name(elem) == "ClinicalDocument"

        # Verify patient data is included
        record_target = elem.find(f"{{{NS}}}recordTarget")
        patient_role = record_target.find(f"{{{NS}}}patientRole")
        patient_elem = patient_role.find(f"{{{NS}}}patient")
        name = patient_elem.find(f"{{{NS}}}name")
        given = name.find(f"{{{NS}}}given")
        assert given.text == "John"

        # Verify component/structuredBody structure
        component = elem.find(f"{{{NS}}}component")
        assert component is not None
        structured_body = component.find(f"{{{NS}}}structuredBody")
        assert structured_body is not None

        # Verify section is wrapped in component
        section_components = structured_body.findall(f"{{{NS}}}component")
        assert len(section_components) == 1

        # Verify section exists
        section = section_components[0].find(f"{{{NS}}}section")
        assert section is not None

        # Verify problems are in the section
        entries = section.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_document_xml_serialization(self):
        """Test that document can be serialized to valid XML."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
        )

        # Serialize to string
        xml_string = doc.to_xml_string(pretty=True)

        # Verify it's valid XML
        assert xml_string.startswith("<?xml")
        assert "<ClinicalDocument" in xml_string or ":ClinicalDocument" in xml_string

        # Verify can be parsed back
        parsed = etree.fromstring(xml_string.encode("UTF-8"))
        assert parsed.tag == f"{{{NS}}}ClinicalDocument"

    def test_document_version_r21(self):
        """Test document with R2.1 version."""
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

        # Find template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("extension") == "2015-08-01"

    def test_document_version_r20(self):
        """Test document with R2.0 version."""
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

        # Find template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("extension") == "2014-06-09"

    def test_document_custom_metadata(self):
        """Test document with custom metadata."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            title="Comprehensive Health Summary",
            document_id="CUSTOM-ID-12345",
            effective_time=datetime(2023, 12, 25, 15, 45),
        )

        elem = doc.to_element()

        # Verify custom title
        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Comprehensive Health Summary"

        # Verify custom ID
        doc_id = elem.find(f"{{{NS}}}id")
        assert doc_id.get("extension") == "CUSTOM-ID-12345"

        # Verify custom effective time
        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time.get("value") == "20231225154500"


class TestProblemsIntegration:
    """Integration tests for problems section in full document context."""

    def test_standalone_problems_section(self):
        """Test creating standalone problems section."""
        problems = [
            MockProblem(
                name="Hypertension",
                code="38341003",
                code_system="SNOMED",
                status="active",
                onset_date=date(2019, 3, 10),
            ),
        ]

        section = ProblemsSection(problems)
        elem = section.to_element()

        # Verify section structure
        assert local_name(elem) == "section"

        # Verify has narrative
        text = elem.find(f"{{{NS}}}text")
        assert text is not None
        table = text.find(f"{{{NS}}}table")
        assert table is not None

        # Verify has entry with Problem Concern Act wrapper
        entry = elem.find(f"{{{NS}}}entry")
        assert entry is not None
        # Should have Problem Concern Act
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        # Observation should be nested in entryRelationship
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is not None
        obs = entry_rel.find(f"{{{NS}}}observation")
        assert obs is not None

    def test_problems_section_xml_quality(self):
        """Test XML quality of problems section."""
        problems = [
            MockProblem(
                name="Type 2 Diabetes",
                code="44054006",
                code_system="SNOMED",
                status="active",
                onset_date=date(2020, 1, 15),
            ),
        ]

        section = ProblemsSection(problems, version=CDAVersion.R2_1)
        xml = section.to_string(pretty=True)

        # Verify proper formatting
        assert "\n" in xml  # Pretty printed

        # Verify contains expected content
        assert "Type 2 Diabetes" in xml
        assert "44054006" in xml
        assert "SNOMED" in xml

        # Parse and verify
        parsed = etree.fromstring(xml.encode("UTF-8"))
        assert local_name(parsed) == "section"

    def test_multiple_problems_narrative_and_entries(self):
        """Test that narrative and entries stay in sync."""
        problems = [
            MockProblem(name="Problem 1", code="C1", onset_date=date(2020, 1, 1)),
            MockProblem(name="Problem 2", code="C2", onset_date=date(2020, 2, 1)),
            MockProblem(name="Problem 3", code="C3", onset_date=date(2020, 3, 1)),
        ]

        section = ProblemsSection(problems)
        elem = section.to_element()

        # Count narrative rows
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        rows = tbody.findall(f"{{{NS}}}tr")
        assert len(rows) == 3

        # Count entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 3

        # Verify they match
        assert len(rows) == len(entries)


class TestDocumentStructureValidation:
    """Tests validating overall document structure."""

    def test_document_element_order(self):
        """Test that document elements are in correct CDA order."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
        )

        elem = doc.to_element()
        children = [local_name(c) for c in elem]

        # Verify key elements are present
        assert "realmCode" in children
        assert "typeId" in children
        assert "templateId" in children
        assert "id" in children
        assert "code" in children
        assert "title" in children
        assert "effectiveTime" in children
        assert "confidentialityCode" in children
        assert "languageCode" in children
        assert "recordTarget" in children
        assert "author" in children
        assert "custodian" in children

        # Verify header ordering (basic checks)
        assert children.index("realmCode") < children.index("typeId")
        assert children.index("typeId") < children.index("templateId")
        assert children.index("recordTarget") < children.index("author")
        assert children.index("author") < children.index("custodian")

    def test_document_size_reasonable(self):
        """Test that generated documents are reasonably sized."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
        )

        xml = doc.to_xml_string(pretty=True)

        # Should be substantial but not huge for minimal doc
        assert len(xml) > 1000  # At least 1KB
        assert len(xml) < 100000  # But less than 100KB for minimal

    def test_document_namespace_consistency(self):
        """Test that all elements use consistent namespaces."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
        )

        elem = doc.to_element()

        # Walk the tree and verify all elements are namespaced
        def check_namespaces(element):
            # All CDA elements should be in the CDA namespace
            if element.tag.startswith("{"):
                namespace = element.tag.split("}")[0][1:]
                # Should be CDA namespace for CDA elements
                assert namespace in [
                    "urn:hl7-org:v3",
                    "http://www.w3.org/2001/XMLSchema-instance",
                ]

            # Check children
            for child in element:
                check_namespaces(child)

        check_namespaces(elem)


class TestDocumentWithMultipleSections:
    """Tests for documents with multiple clinical sections."""

    def test_document_with_medications_section(self):
        """Test document with medications section."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        # Create medications
        medications = [
            MockMedication(
                name="Lisinopril 10mg tablet",
                code="314076",
                dosage="10 mg",
                route="oral",
                frequency="once daily",
                start_date=date(2020, 1, 1),
                status="active",
            ),
        ]

        # Create medications section
        medications_section = MedicationsSection(medications=medications, version=CDAVersion.R2_1)

        # Create document
        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=[medications_section],
            version=CDAVersion.R2_1,
        )

        elem = doc.to_element()

        # Verify section is present
        component = elem.find(f"{{{NS}}}component")
        structured_body = component.find(f"{{{NS}}}structuredBody")
        section_components = structured_body.findall(f"{{{NS}}}component")
        assert len(section_components) == 1

        section = section_components[0].find(f"{{{NS}}}section")
        assert section is not None

        # Verify medication entry
        entries = section.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_document_with_multiple_sections(self):
        """Test document with both problems and medications sections."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        # Create problems
        problems = [
            MockProblem(
                name="Hypertension",
                code="38341003",
                code_system="SNOMED",
                status="active",
                onset_date=date(2019, 1, 1),
            ),
            MockProblem(
                name="Diabetes",
                code="44054006",
                code_system="SNOMED",
                status="active",
                onset_date=date(2020, 1, 1),
            ),
        ]

        # Create medications
        medications = [
            MockMedication(
                name="Lisinopril 10mg tablet",
                code="314076",
                dosage="10 mg",
                route="oral",
                frequency="once daily",
                start_date=date(2019, 6, 1),
                status="active",
            ),
            MockMedication(
                name="Metformin 500mg tablet",
                code="860975",
                dosage="500 mg",
                route="oral",
                frequency="twice daily",
                start_date=date(2020, 3, 1),
                status="active",
            ),
        ]

        # Create sections
        problems_section = ProblemsSection(problems=problems, version=CDAVersion.R2_1)
        medications_section = MedicationsSection(medications=medications, version=CDAVersion.R2_1)

        # Create document with multiple sections
        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=[problems_section, medications_section],
            title="Comprehensive Summary",
            version=CDAVersion.R2_1,
        )

        elem = doc.to_element()

        # Verify both sections are present
        component = elem.find(f"{{{NS}}}component")
        structured_body = component.find(f"{{{NS}}}structuredBody")
        section_components = structured_body.findall(f"{{{NS}}}component")
        assert len(section_components) == 2

        # Verify both sections exist
        sections = [comp.find(f"{{{NS}}}section") for comp in section_components]
        assert all(s is not None for s in sections)

        # Verify first section (problems) has 2 entries
        problems_entries = sections[0].findall(f"{{{NS}}}entry")
        assert len(problems_entries) == 2

        # Verify second section (medications) has 2 entries
        medications_entries = sections[1].findall(f"{{{NS}}}entry")
        assert len(medications_entries) == 2

    def test_document_with_sections_serialization(self):
        """Test that document with sections can be serialized."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        problems = [MockProblem()]
        medications = [MockMedication()]

        problems_section = ProblemsSection(problems=problems, version=CDAVersion.R2_1)
        medications_section = MedicationsSection(medications=medications, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=[problems_section, medications_section],
            version=CDAVersion.R2_1,
        )

        # Serialize to string
        xml_string = doc.to_xml_string(pretty=True)

        # Verify it's valid XML
        assert xml_string.startswith("<?xml")
        assert "ClinicalDocument" in xml_string

        # Verify sections are present in output
        assert "structuredBody" in xml_string
        assert "section" in xml_string

        # Parse and verify
        parsed = etree.fromstring(xml_string.encode("UTF-8"))
        assert local_name(parsed) == "ClinicalDocument"

        # Verify can find sections
        component = parsed.find(f"{{{NS}}}component")
        structured_body = component.find(f"{{{NS}}}structuredBody")
        section_components = structured_body.findall(f"{{{NS}}}component")
        assert len(section_components) == 2

    def test_document_sections_maintain_order(self):
        """Test that sections maintain their order in the document."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        # Create sections in specific order
        problems = [MockProblem(name="Problem A")]
        medications = [MockMedication(name="Medication B")]

        problems_section = ProblemsSection(
            problems=problems, title="Problems List", version=CDAVersion.R2_1
        )
        medications_section = MedicationsSection(
            medications=medications, title="Medications List", version=CDAVersion.R2_1
        )

        # Add sections in specific order
        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=[problems_section, medications_section],
            version=CDAVersion.R2_1,
        )

        elem = doc.to_element()
        component = elem.find(f"{{{NS}}}component")
        structured_body = component.find(f"{{{NS}}}structuredBody")
        section_components = structured_body.findall(f"{{{NS}}}component")

        # Get section titles
        sections = [comp.find(f"{{{NS}}}section") for comp in section_components]
        titles = [s.find(f"{{{NS}}}title").text for s in sections]

        # Verify order is preserved
        assert titles[0] == "Problems List"
        assert titles[1] == "Medications List"

    def test_empty_sections_list(self):
        """Test document with empty sections list."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        # Create document with empty sections
        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=[],
            version=CDAVersion.R2_1,
        )

        elem = doc.to_element()

        # Verify no component/body is added
        component = elem.find(f"{{{NS}}}component")
        assert component is None

    def test_document_without_sections_parameter(self):
        """Test document created without sections parameter (defaults to empty)."""
        patient = MockPatient()
        author = MockAuthor()
        custodian = MockOrganization()

        # Create document without sections parameter
        doc = ClinicalDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            version=CDAVersion.R2_1,
        )

        elem = doc.to_element()

        # Verify no component/body is added
        component = elem.find(f"{{{NS}}}component")
        assert component is None
