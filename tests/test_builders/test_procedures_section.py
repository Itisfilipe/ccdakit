"""Tests for ProceduresSection builder."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.sections.procedures import ProceduresSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockProcedure:
    """Mock procedure for testing."""

    def __init__(
        self,
        name="Appendectomy",
        code="80146002",
        code_system="SNOMED CT",
        date=date(2023, 5, 15),
        status="completed",
        target_site=None,
        target_site_code=None,
        performer_name=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._date = date
        self._status = status
        self._target_site = target_site
        self._target_site_code = target_site_code
        self._performer_name = performer_name

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
    def date(self):
        return self._date

    @property
    def status(self):
        return self._status

    @property
    def target_site(self):
        return self._target_site

    @property
    def target_site_code(self):
        return self._target_site_code

    @property
    def performer_name(self):
        return self._performer_name


class TestProceduresSection:
    """Tests for ProceduresSection builder."""

    def test_procedures_section_basic(self):
        """Test basic ProceduresSection creation."""
        procedure = MockProcedure()
        section = ProceduresSection([procedure])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_procedures_section_has_template_id_r21(self):
        """Test ProceduresSection includes R2.1 template ID."""
        procedure = MockProcedure()
        section = ProceduresSection([procedure], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.7.1"
        # Per C-CDA 2.1 spec (CONF:1098-32533), extension is 2014-06-09
        assert template.get("extension") == "2014-06-09"

    def test_procedures_section_has_code(self):
        """Test ProceduresSection includes section code."""
        procedure = MockProcedure()
        section = ProceduresSection([procedure])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "47519-4"  # History of Procedures
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC

    def test_procedures_section_has_title(self):
        """Test ProceduresSection includes title."""
        procedure = MockProcedure()
        section = ProceduresSection([procedure], title="My Procedures")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Procedures"

    def test_procedures_section_default_title(self):
        """Test ProceduresSection uses default title."""
        procedure = MockProcedure()
        section = ProceduresSection([procedure])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Procedures"

    def test_procedures_section_has_narrative(self):
        """Test ProceduresSection includes narrative text."""
        procedure = MockProcedure()
        section = ProceduresSection([procedure])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_procedures_section_narrative_table(self):
        """Test narrative includes HTML table."""
        procedure = MockProcedure(
            name="Hip Replacement",
            code="52734007",
        )
        section = ProceduresSection([procedure])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        assert table is not None
        assert table.get("border") == "1"

        # Check table header
        thead = table.find(f"{{{NS}}}thead")
        assert thead is not None
        tr = thead.find(f"{{{NS}}}tr")
        ths = tr.findall(f"{{{NS}}}th")
        assert len(ths) == 6  # Procedure, Code, Date, Status, Target Site, Performer

    def test_procedures_section_empty_narrative(self):
        """Test narrative when no procedures."""
        section = ProceduresSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No procedures recorded"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_procedures_section_has_entries(self):
        """Test ProceduresSection includes entry elements."""
        procedure = MockProcedure()
        section = ProceduresSection([procedure])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1
        assert entries[0].get("typeCode") == "DRIV"

    def test_procedures_section_entry_has_procedure(self):
        """Test entry contains procedure element."""
        procedure = MockProcedure()
        section = ProceduresSection([procedure])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        proc = entry.find(f"{{{NS}}}procedure")
        assert proc is not None
        assert proc.get("classCode") == "PROC"

    def test_procedures_section_multiple_entries(self):
        """Test ProceduresSection with multiple procedures."""
        procedures = [
            MockProcedure(name="Procedure 1", code="111111"),
            MockProcedure(name="Procedure 2", code="222222"),
        ]
        section = ProceduresSection(procedures)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_procedures_section_to_string(self):
        """Test ProceduresSection serialization."""
        procedure = MockProcedure()
        section = ProceduresSection([procedure])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "47519-4" in xml  # Section code

    def test_procedures_section_structure_order(self):
        """Test that section elements are in correct order."""
        procedure = MockProcedure()
        section = ProceduresSection([procedure])
        elem = section.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "code" in names
        assert "title" in names
        assert "text" in names
        assert "entry" in names

        # templateId should come before code
        assert names.index("templateId") < names.index("code")
        # code should come before title
        assert names.index("code") < names.index("title")
        # title should come before text
        assert names.index("title") < names.index("text")
        # text should come before entry
        assert names.index("text") < names.index("entry")


class TestProceduresSectionIntegration:
    """Integration tests for ProceduresSection."""

    def test_complete_procedures_section(self):
        """Test creating a complete procedures section."""
        procedures = [
            MockProcedure(
                name="Appendectomy",
                code="80146002",
                code_system="SNOMED CT",
                date=date(2023, 3, 10),
                status="completed",
                target_site="Abdomen",
                performer_name="Dr. Jane Smith",
            ),
            MockProcedure(
                name="Hip Replacement",
                code="52734007",
                code_system="SNOMED CT",
                date=date(2023, 5, 20),
                status="completed",
                target_site="Left hip",
                target_site_code="287579007",
                performer_name="Dr. John Surgeon",
            ),
        ]

        section = ProceduresSection(procedures, title="Patient Procedure History")
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify narrative table has 2 rows
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 2

        # Verify 2 entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_narrative_procedure_with_datetime(self):
        """Test narrative with procedure using datetime instead of date."""
        procedure = MockProcedure(
            name="Appendectomy",
            code="80146002",
            date=datetime(2023, 5, 15, 14, 30),
        )
        section = ProceduresSection([procedure])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Date column should include time (index 2)
        assert tds[2].text == "2023-05-15 14:30"

    def test_narrative_procedure_with_no_date(self):
        """Test narrative with procedure with no date."""
        procedure = MockProcedure(
            name="Colonoscopy",
            code="73761001",
            date=None,
        )
        section = ProceduresSection([procedure])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Date column should show "Unknown" when date is None
        assert tds[2].text == "Unknown"
