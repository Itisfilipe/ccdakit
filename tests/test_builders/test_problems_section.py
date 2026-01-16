"""Tests for section builders."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.problems import ProblemsSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockPersistentID:
    """Mock persistent ID for testing."""

    @property
    def root(self):
        return "2.16.840.1.113883.19.5.99999.1"

    @property
    def extension(self):
        return "PROB-123"


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


class TestProblemsSection:
    """Tests for ProblemsSection builder."""

    def test_problems_section_basic(self):
        """Test basic ProblemsSection creation."""
        problem = MockProblem()
        section = ProblemsSection([problem])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_problems_section_has_template_id_r21(self):
        """Test ProblemsSection includes R2.1 template ID."""
        problem = MockProblem()
        section = ProblemsSection([problem], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.5.1"
        assert template.get("extension") == "2015-08-01"

    def test_problems_section_has_template_id_r20(self):
        """Test ProblemsSection includes R2.0 template ID."""
        problem = MockProblem()
        section = ProblemsSection([problem], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.5.1"
        assert template.get("extension") == "2014-06-09"

    def test_problems_section_has_code(self):
        """Test ProblemsSection includes section code."""
        problem = MockProblem()
        section = ProblemsSection([problem])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "11450-4"  # Problem List
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Problem List"

    def test_problems_section_has_title(self):
        """Test ProblemsSection includes title."""
        problem = MockProblem()
        section = ProblemsSection([problem], title="My Problems")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Problems"

    def test_problems_section_default_title(self):
        """Test ProblemsSection uses default title."""
        problem = MockProblem()
        section = ProblemsSection([problem])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Problems"

    def test_problems_section_has_narrative(self):
        """Test ProblemsSection includes narrative text."""
        problem = MockProblem()
        section = ProblemsSection([problem])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_problems_section_narrative_table(self):
        """Test narrative includes HTML table."""
        problem = MockProblem(
            name="Hypertension",
            code="38341003",
            onset_date=date(2019, 3, 10),
        )
        section = ProblemsSection([problem])
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
        assert len(ths) == 5  # Problem, Code, Status, Onset, Resolved

    def test_problems_section_narrative_content(self):
        """Test narrative contains problem data."""
        problem = MockProblem(
            name="Diabetes",
            code="44054006",
            code_system="SNOMED",
            status="active",
            onset_date=date(2020, 1, 15),
        )
        section = ProblemsSection([problem])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 5

        # Check problem name with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Diabetes"
        assert content.get("ID") == "problem-1"

        # Check code
        assert "44054006" in tds[1].text
        assert "SNOMED" in tds[1].text

        # Check status
        assert tds[2].text == "Active"

        # Check onset date
        assert tds[3].text == "2020-01-15"

        # Check resolved date (should show "Ongoing" for active)
        assert tds[4].text == "Ongoing"

    def test_problems_section_narrative_multiple_problems(self):
        """Test narrative with multiple problems."""
        problems = [
            MockProblem(name="Hypertension", code="38341003"),
            MockProblem(name="Diabetes", code="44054006"),
            MockProblem(name="Asthma", code="195967001"),
        ]
        section = ProblemsSection(problems)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        assert len(trs) == 3

        # Check IDs are sequential
        content1 = trs[0].find(f".//{{{NS}}}content")
        content2 = trs[1].find(f".//{{{NS}}}content")
        content3 = trs[2].find(f".//{{{NS}}}content")

        assert content1.get("ID") == "problem-1"
        assert content2.get("ID") == "problem-2"
        assert content3.get("ID") == "problem-3"

    def test_problems_section_narrative_resolved_problem(self):
        """Test narrative shows resolved date for resolved problems."""
        problem = MockProblem(
            name="Pneumonia",
            code="233604007",
            status="resolved",
            onset_date=date(2020, 1, 10),
            resolved_date=date(2020, 2, 15),
        )
        section = ProblemsSection([problem])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check status
        assert tds[2].text == "Resolved"

        # Check resolved date
        assert tds[4].text == "2020-02-15"

    def test_problems_section_empty_narrative(self):
        """Test narrative when no problems."""
        section = ProblemsSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No known problems"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_problems_section_has_entries(self):
        """Test ProblemsSection includes entry elements."""
        problem = MockProblem()
        section = ProblemsSection([problem])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1
        assert entries[0].get("typeCode") == "DRIV"

    def test_problems_section_entry_has_concern_act(self):
        """Test entry contains Problem Concern Act wrapper."""
        problem = MockProblem()
        section = ProblemsSection([problem])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        # Should have Problem Concern Act wrapper
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"
        assert act.get("moodCode") == "EVN"

        # Act should have Problem Concern Act template ID
        template = act.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.3"

        # Act should have code CONC
        code = act.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "CONC"
        assert code.get("codeSystem") == "2.16.840.1.113883.5.6"

        # Act should have statusCode
        status = act.find(f"{{{NS}}}statusCode")
        assert status is not None

        # Act should have effectiveTime
        time = act.find(f"{{{NS}}}effectiveTime")
        assert time is not None

        # Act should contain entryRelationship with observation
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "SUBJ"

        observation = entry_rel.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"

    def test_problems_section_multiple_entries(self):
        """Test ProblemsSection with multiple problems."""
        problems = [
            MockProblem(name="Hypertension", code="38341003"),
            MockProblem(name="Diabetes", code="44054006"),
        ]
        section = ProblemsSection(problems)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has a Problem Concern Act with nested observation
        for entry in entries:
            act = entry.find(f"{{{NS}}}act")
            assert act is not None
            entry_rel = act.find(f"{{{NS}}}entryRelationship")
            assert entry_rel is not None
            obs = entry_rel.find(f"{{{NS}}}observation")
            assert obs is not None

    def test_problems_section_to_string(self):
        """Test ProblemsSection serialization."""
        problem = MockProblem()
        section = ProblemsSection([problem])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "11450-4" in xml  # Section code
        assert "Problem List" in xml

    def test_problems_section_structure_order(self):
        """Test that section elements are in correct order."""
        problem = MockProblem()
        section = ProblemsSection([problem])
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


class TestProblemsSectionIntegration:
    """Integration tests for ProblemsSection."""

    def test_complete_problems_section(self):
        """Test creating a complete problems section."""
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
            MockProblem(
                name="Pneumonia",
                code="233604007",
                code_system="SNOMED",
                status="resolved",
                onset_date=date(2020, 1, 5),
                resolved_date=date(2020, 2, 1),
            ),
        ]

        section = ProblemsSection(problems, title="Patient Problem List")
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify narrative table has 3 rows
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 3

        # Verify 3 entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 3

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        problem = MockProblem()
        section = ProblemsSection([problem])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_narrative_problem_with_no_onset_date(self):
        """Test narrative with problem with no onset date.

        Uses R2.0 since R2.1 requires onset_date per specification.
        """
        problem = MockProblem(
            name="Headache",
            code="25064002",
            onset_date=None,
        )
        section = ProblemsSection([problem], version=CDAVersion.R2_0)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Onset date column should show "Unknown" when onset_date is None
        assert tds[3].text == "Unknown"

    def test_entry_problem_with_no_onset_date_has_null_flavor(self):
        """Test entry element uses nullFlavor when onset_date is None.

        Uses R2.0 since R2.1 requires onset_date per specification.
        """
        problem = MockProblem(
            name="Chronic pain",
            code="82423001",
            onset_date=None,
            status="active",
        )
        section = ProblemsSection([problem], version=CDAVersion.R2_0)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        eff_time = act.find(f"{{{NS}}}effectiveTime")
        low = eff_time.find(f"{{{NS}}}low")

        # Should have nullFlavor instead of value
        assert low.get("nullFlavor") == "UNK"
        assert low.get("value") is None

    def test_entry_completed_problem_with_no_resolved_date_has_null_flavor(self):
        """Test entry element uses nullFlavor for high when resolved_date is None."""
        problem = MockProblem(
            name="Resolved condition",
            code="123456789",
            onset_date=date(2023, 1, 1),
            resolved_date=None,
            status="inactive",
        )
        section = ProblemsSection([problem])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        eff_time = act.find(f"{{{NS}}}effectiveTime")
        high = eff_time.find(f"{{{NS}}}high")

        # Should have nullFlavor instead of value for resolved date
        assert high.get("nullFlavor") == "UNK"
        assert high.get("value") is None
