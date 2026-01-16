"""Tests for Complications Section builder."""

from datetime import date

import pytest
from lxml import etree

from ccdakit.builders.sections.complications import ComplicationsSection
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
        return "COMP-123"


class MockComplication:
    """Mock complication for testing."""

    def __init__(
        self,
        name="Postoperative wound infection",
        code="432119003",
        code_system="SNOMED",
        onset_date=date(2024, 1, 15),
        resolved_date=None,
        status="active",
        severity=None,
        related_procedure_code=None,
        persistent_id=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._onset_date = onset_date
        self._resolved_date = resolved_date
        self._status = status
        self._severity = severity
        self._related_procedure_code = related_procedure_code
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
    def severity(self):
        return self._severity

    @property
    def related_procedure_code(self):
        return self._related_procedure_code

    @property
    def persistent_id(self):
        return self._persistent_id


class TestComplicationsSection:
    """Tests for ComplicationsSection builder."""

    def test_complications_section_basic(self):
        """Test basic ComplicationsSection creation."""
        complication = MockComplication()
        section = ComplicationsSection([complication])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_complications_section_has_template_id_r21(self):
        """Test ComplicationsSection includes R2.1 template ID."""
        complication = MockComplication()
        section = ComplicationsSection([complication], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.37"
        assert template.get("extension") == "2015-08-01"

    def test_complications_section_has_code(self):
        """Test ComplicationsSection includes section code."""
        complication = MockComplication()
        section = ComplicationsSection([complication])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "55109-3"  # Complications
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Complications"

    def test_complications_section_has_title(self):
        """Test ComplicationsSection includes title."""
        complication = MockComplication()
        section = ComplicationsSection([complication], title="Surgical Complications")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Surgical Complications"

    def test_complications_section_default_title(self):
        """Test ComplicationsSection uses default title."""
        complication = MockComplication()
        section = ComplicationsSection([complication])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Complications"

    def test_complications_section_has_narrative(self):
        """Test ComplicationsSection includes narrative text."""
        complication = MockComplication()
        section = ComplicationsSection([complication])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_complications_section_narrative_table(self):
        """Test narrative includes HTML table."""
        complication = MockComplication(
            name="Postoperative bleeding",
            code="83132003",
            onset_date=date(2024, 1, 10),
        )
        section = ComplicationsSection([complication])
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
        assert len(ths) == 6  # Complication, Code, Severity, Status, Onset, Resolved

    def test_complications_section_narrative_content(self):
        """Test narrative contains complication data."""
        complication = MockComplication(
            name="Surgical site infection",
            code="432119003",
            code_system="SNOMED",
            status="active",
            severity="moderate",
            onset_date=date(2024, 1, 15),
        )
        section = ComplicationsSection([complication])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 6

        # Check complication name with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Surgical site infection"
        assert content.get("ID") == "complication-1"

        # Check code
        assert "432119003" in tds[1].text
        assert "SNOMED" in tds[1].text

        # Check severity
        assert tds[2].text == "Moderate"

        # Check status
        assert tds[3].text == "Active"

        # Check onset date
        assert tds[4].text == "2024-01-15"

        # Check resolved date (should show "Ongoing" for active)
        assert tds[5].text == "Ongoing"

    def test_complications_section_narrative_no_severity(self):
        """Test narrative when severity is not specified."""
        complication = MockComplication(
            name="Deep vein thrombosis",
            code="128053003",
            severity=None,
        )
        section = ComplicationsSection([complication])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check severity shows "Not specified"
        assert tds[2].text == "Not specified"

    def test_complications_section_narrative_multiple_complications(self):
        """Test narrative with multiple complications."""
        complications = [
            MockComplication(
                name="Postoperative bleeding",
                code="83132003",
                severity="severe",
            ),
            MockComplication(
                name="Wound infection",
                code="432119003",
                severity="moderate",
            ),
            MockComplication(
                name="Deep vein thrombosis",
                code="128053003",
                severity="mild",
            ),
        ]
        section = ComplicationsSection(complications)
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

        assert content1.get("ID") == "complication-1"
        assert content2.get("ID") == "complication-2"
        assert content3.get("ID") == "complication-3"

        # Check severities
        tds1 = trs[0].findall(f"{{{NS}}}td")
        tds2 = trs[1].findall(f"{{{NS}}}td")
        tds3 = trs[2].findall(f"{{{NS}}}td")

        assert tds1[2].text == "Severe"
        assert tds2[2].text == "Moderate"
        assert tds3[2].text == "Mild"

    def test_complications_section_narrative_resolved_complication(self):
        """Test narrative shows resolved date for resolved complications."""
        complication = MockComplication(
            name="Postoperative fever",
            code="386661006",
            status="resolved",
            onset_date=date(2024, 1, 10),
            resolved_date=date(2024, 1, 20),
        )
        section = ComplicationsSection([complication])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check status
        assert tds[3].text == "Resolved"

        # Check resolved date
        assert tds[5].text == "2024-01-20"

    def test_complications_section_empty_narrative(self):
        """Test narrative when no complications."""
        section = ComplicationsSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No complications"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_complications_section_has_entries(self):
        """Test ComplicationsSection includes entry elements."""
        complication = MockComplication()
        section = ComplicationsSection([complication])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_complications_section_entry_has_observation(self):
        """Test entry contains Problem Observation."""
        complication = MockComplication()
        section = ComplicationsSection([complication])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        # Should have Problem Observation (not wrapped in Concern Act for complications)
        observation = entry.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"
        assert observation.get("moodCode") == "EVN"

        # Observation should have Problem Observation template ID
        template = observation.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.4"

        # Observation should have code for Problem
        code = observation.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "55607006"  # Problem

        # Observation should have statusCode
        status = observation.find(f"{{{NS}}}statusCode")
        assert status is not None

        # Observation should have value (the complication code)
        value = observation.find(f"{{{NS}}}value")
        assert value is not None

    def test_complications_section_multiple_entries(self):
        """Test ComplicationsSection with multiple complications."""
        complications = [
            MockComplication(name="Bleeding", code="83132003"),
            MockComplication(name="Infection", code="432119003"),
        ]
        section = ComplicationsSection(complications)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has a Problem Observation
        for entry in entries:
            obs = entry.find(f"{{{NS}}}observation")
            assert obs is not None

    def test_complications_section_to_string(self):
        """Test ComplicationsSection serialization."""
        complication = MockComplication()
        section = ComplicationsSection([complication])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "55109-3" in xml  # Section code
        assert "Complications" in xml

    def test_complications_section_structure_order(self):
        """Test that section elements are in correct order."""
        complication = MockComplication()
        section = ComplicationsSection([complication])
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

    def test_complications_section_severity_levels(self):
        """Test complications with different severity levels."""
        complications = [
            MockComplication(
                name="Minor wound dehiscence",
                code="277579005",
                severity="mild",
            ),
            MockComplication(
                name="Moderate bleeding",
                code="83132003",
                severity="moderate",
            ),
            MockComplication(
                name="Septic shock",
                code="76571007",
                severity="severe",
            ),
        ]
        section = ComplicationsSection(complications)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        # Verify severity column for each complication
        for idx, expected_severity in enumerate(["Mild", "Moderate", "Severe"]):
            tds = trs[idx].findall(f"{{{NS}}}td")
            assert tds[2].text == expected_severity

    def test_complications_section_unknown_onset_date(self):
        """Test that R2.1 raises ValueError when onset_date is None.

        R2.1 requires onset_date per C-CDA specification.
        """
        complication = MockComplication(
            name="Unknown onset complication",
            code="123456789",
            onset_date=None,
        )
        section = ComplicationsSection([complication])

        with pytest.raises(ValueError, match="onset date"):
            section.to_element()

    def test_complications_section_with_persistent_id(self):
        """Test complication with persistent identifier."""
        complication = MockComplication(
            name="Tracked complication",
            code="123456789",
            persistent_id=MockPersistentID(),
        )
        section = ComplicationsSection([complication])
        elem = section.to_element()

        # Check that the observation has the persistent ID
        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        id_elem = observation.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.19.5.99999.1"
        assert id_elem.get("extension") == "COMP-123"


class TestComplicationsSectionIntegration:
    """Integration tests for ComplicationsSection."""

    def test_complete_complications_section(self):
        """Test creating a complete complications section."""
        complications = [
            MockComplication(
                name="Postoperative bleeding",
                code="83132003",
                code_system="SNOMED",
                status="active",
                severity="severe",
                onset_date=date(2024, 1, 15),
            ),
            MockComplication(
                name="Surgical site infection",
                code="432119003",
                code_system="SNOMED",
                status="active",
                severity="moderate",
                onset_date=date(2024, 1, 18),
            ),
            MockComplication(
                name="Postoperative fever",
                code="386661006",
                code_system="SNOMED",
                status="resolved",
                severity="mild",
                onset_date=date(2024, 1, 16),
                resolved_date=date(2024, 1, 20),
            ),
        ]

        section = ComplicationsSection(complications, title="Surgical Complications")
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

        complication = MockComplication()
        section = ComplicationsSection([complication])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_complications_section_procedure_linkage(self):
        """Test complication with related procedure code."""
        complication = MockComplication(
            name="Post-appendectomy infection",
            code="432119003",
            code_system="SNOMED",
            severity="moderate",
            related_procedure_code="80146002",  # Appendectomy
        )
        section = ComplicationsSection([complication])
        elem = section.to_element()

        # Verify the complication is represented
        assert local_name(elem) == "section"
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        # The related_procedure_code is stored in the protocol
        # but may not be directly represented in the basic XML structure
        # This test verifies that the section handles it without errors
        assert complication.related_procedure_code == "80146002"

    def test_empty_complications_section(self):
        """Test section with no complications."""
        section = ComplicationsSection([])
        elem = section.to_element()

        # Verify basic structure
        assert local_name(elem) == "section"

        # Verify no entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

        # Verify narrative shows "No complications"
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph.text == "No complications"

    def test_complications_mixed_statuses(self):
        """Test complications with various statuses."""
        complications = [
            MockComplication(
                name="Active bleeding",
                code="83132003",
                status="active",
                severity="severe",
            ),
            MockComplication(
                name="Resolved infection",
                code="432119003",
                status="resolved",
                severity="moderate",
                resolved_date=date(2024, 2, 1),
            ),
            MockComplication(
                name="Inactive wound issue",
                code="123456789",
                status="inactive",
                severity="mild",
            ),
        ]
        section = ComplicationsSection(complications)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        # Verify statuses
        tds1 = trs[0].findall(f"{{{NS}}}td")
        tds2 = trs[1].findall(f"{{{NS}}}td")
        tds3 = trs[2].findall(f"{{{NS}}}td")

        assert tds1[3].text == "Active"
        assert tds2[3].text == "Resolved"
        assert tds3[3].text == "Inactive"
