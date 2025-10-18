"""Tests for VitalSignsSection builder."""

from datetime import datetime
from typing import Sequence

from lxml import etree

from ccdakit.builders.sections.vital_signs import VitalSignsSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockVitalSign:
    """Mock vital sign for testing."""

    def __init__(
        self,
        type="Heart Rate",
        code="8867-4",
        value="72",
        unit="bpm",
        date=datetime(2023, 10, 1, 10, 30),
        interpretation=None,
    ):
        self._type = type
        self._code = code
        self._value = value
        self._unit = unit
        self._date = date
        self._interpretation = interpretation

    @property
    def type(self):
        return self._type

    @property
    def code(self):
        return self._code

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit

    @property
    def date(self):
        return self._date

    @property
    def interpretation(self):
        return self._interpretation


class MockVitalSignsOrganizer:
    """Mock vital signs organizer for testing."""

    def __init__(self, date=datetime(2023, 10, 1, 10, 30), vital_signs=None):
        self._date = date
        self._vital_signs = vital_signs or []

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def vital_signs(self) -> Sequence[MockVitalSign]:
        return self._vital_signs


class TestVitalSignsSection:
    """Tests for VitalSignsSection builder."""

    def test_vital_signs_section_basic(self):
        """Test basic VitalSignsSection creation."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_vital_signs_section_has_template_id_r21(self):
        """Test VitalSignsSection includes R2.1 template ID."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.4.1"
        assert template.get("extension") == "2015-08-01"

    def test_vital_signs_section_has_template_id_r20(self):
        """Test VitalSignsSection includes R2.0 template ID."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.4.1"
        assert template.get("extension") == "2014-06-09"

    def test_vital_signs_section_has_code(self):
        """Test VitalSignsSection includes section code."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "8716-3"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Vital signs"

    def test_vital_signs_section_has_title(self):
        """Test VitalSignsSection includes title."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer], title="Patient Vital Signs")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Patient Vital Signs"

    def test_vital_signs_section_default_title(self):
        """Test VitalSignsSection uses default title."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Vital Signs"

    def test_vital_signs_section_has_narrative(self):
        """Test VitalSignsSection includes narrative text."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_vital_signs_section_narrative_table(self):
        """Test narrative includes HTML table."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer])
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
        assert len(ths) == 5  # Date/Time, Vital Sign, Value, Unit, Interpretation

    def test_vital_signs_section_narrative_content(self):
        """Test narrative contains vital sign data."""
        vital_signs = [
            MockVitalSign(
                type="Heart Rate",
                code="8867-4",
                value="72",
                unit="bpm",
                date=datetime(2023, 10, 15, 10, 30),
                interpretation="Normal",
            )
        ]
        organizer = MockVitalSignsOrganizer(
            date=datetime(2023, 10, 15, 10, 30),
            vital_signs=vital_signs,
        )
        section = VitalSignsSection([organizer])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 5

        # Check date/time
        assert tds[0].text == "2023-10-15 10:30"

        # Check vital sign type with ID
        content = tds[1].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Heart Rate"
        assert content.get("ID") == "vitalsign-1-1"

        # Check value
        assert tds[2].text == "72"

        # Check unit
        assert tds[3].text == "bpm"

        # Check interpretation
        assert tds[4].text == "Normal"

    def test_vital_signs_section_narrative_without_interpretation(self):
        """Test narrative shows '-' when interpretation missing."""
        vital_signs = [MockVitalSign(interpretation=None)]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check interpretation shows "-"
        assert tds[4].text == "-"

    def test_vital_signs_section_narrative_multiple_vital_signs(self):
        """Test narrative with multiple vital signs in one organizer."""
        vital_signs = [
            MockVitalSign(type="Heart Rate", code="8867-4", value="72", unit="bpm"),
            MockVitalSign(type="Systolic BP", code="8480-6", value="120", unit="mm[Hg]"),
            MockVitalSign(type="Diastolic BP", code="8462-4", value="80", unit="mm[Hg]"),
        ]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        assert len(trs) == 3

        # Check IDs are sequential within the organizer
        content1 = trs[0].find(f".//{{{NS}}}content")
        content2 = trs[1].find(f".//{{{NS}}}content")
        content3 = trs[2].find(f".//{{{NS}}}content")

        assert content1.get("ID") == "vitalsign-1-1"
        assert content2.get("ID") == "vitalsign-1-2"
        assert content3.get("ID") == "vitalsign-1-3"

    def test_vital_signs_section_narrative_multiple_organizers(self):
        """Test narrative with multiple organizers."""
        organizers = [
            MockVitalSignsOrganizer(
                date=datetime(2023, 10, 1, 10, 0),
                vital_signs=[MockVitalSign(type="Heart Rate", value="72", unit="bpm")],
            ),
            MockVitalSignsOrganizer(
                date=datetime(2023, 10, 2, 10, 0),
                vital_signs=[MockVitalSign(type="Heart Rate", value="74", unit="bpm")],
            ),
        ]
        section = VitalSignsSection(organizers)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        assert len(trs) == 2

        # Check IDs from different organizers
        content1 = trs[0].find(f".//{{{NS}}}content")
        content2 = trs[1].find(f".//{{{NS}}}content")

        assert content1.get("ID") == "vitalsign-1-1"
        assert content2.get("ID") == "vitalsign-2-1"

    def test_vital_signs_section_empty_narrative(self):
        """Test narrative when no vital signs."""
        section = VitalSignsSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No vital signs recorded"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_vital_signs_section_has_entries(self):
        """Test VitalSignsSection includes entry elements."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1
        assert entries[0].get("typeCode") == "DRIV"

    def test_vital_signs_section_entry_has_organizer(self):
        """Test entry contains organizer element."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        org = entry.find(f"{{{NS}}}organizer")
        assert org is not None
        assert org.get("classCode") == "CLUSTER"

    def test_vital_signs_section_multiple_entries(self):
        """Test VitalSignsSection with multiple organizers."""
        organizers = [
            MockVitalSignsOrganizer(vital_signs=[MockVitalSign()]),
            MockVitalSignsOrganizer(vital_signs=[MockVitalSign()]),
        ]
        section = VitalSignsSection(organizers)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an organizer
        for entry in entries:
            org = entry.find(f"{{{NS}}}organizer")
            assert org is not None

    def test_vital_signs_section_to_string(self):
        """Test VitalSignsSection serialization."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "8716-3" in xml  # Section code
        assert "Vital" in xml

    def test_vital_signs_section_structure_order(self):
        """Test that section elements are in correct order."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer])
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


class TestVitalSignsSectionIntegration:
    """Integration tests for VitalSignsSection."""

    def test_complete_vital_signs_section(self):
        """Test creating a complete vital signs section."""
        organizers = [
            MockVitalSignsOrganizer(
                date=datetime(2023, 10, 15, 10, 30),
                vital_signs=[
                    MockVitalSign(
                        type="Heart Rate",
                        code="8867-4",
                        value="72",
                        unit="bpm",
                        interpretation="Normal",
                    ),
                    MockVitalSign(
                        type="Systolic BP",
                        code="8480-6",
                        value="120",
                        unit="mm[Hg]",
                        interpretation="Normal",
                    ),
                    MockVitalSign(
                        type="Diastolic BP",
                        code="8462-4",
                        value="80",
                        unit="mm[Hg]",
                        interpretation="Normal",
                    ),
                ],
            ),
        ]

        section = VitalSignsSection(organizers, title="Vital Signs History")
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify narrative table has 3 rows (one per vital sign)
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 3

        # Verify 1 entry (1 organizer)
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        # Verify organizer has 3 components
        organizer = entries[0].find(f"{{{NS}}}organizer")
        components = organizer.findall(f"{{{NS}}}component")
        assert len(components) == 3

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        section = VitalSignsSection([organizer])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None
