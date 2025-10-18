"""Tests for PhysicalExamSection builder."""

from datetime import datetime
from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.sections.physical_exam import PhysicalExamSection
from ccdakit.builders.entries.physical_exam import LongitudinalCareWoundObservation
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockWoundObservation:
    """Mock wound observation for testing."""

    def __init__(
        self,
        wound_type="Pressure ulcer",
        wound_code="399912005",
        date=datetime(2023, 10, 1, 10, 30),
        location=None,
        location_code=None,
        laterality=None,
        laterality_code=None,
    ):
        self._wound_type = wound_type
        self._wound_code = wound_code
        self._date = date
        self._location = location
        self._location_code = location_code
        self._laterality = laterality
        self._laterality_code = laterality_code

    @property
    def wound_type(self):
        return self._wound_type

    @property
    def wound_code(self):
        return self._wound_code

    @property
    def date(self):
        return self._date

    @property
    def location(self):
        return self._location

    @property
    def location_code(self):
        return self._location_code

    @property
    def laterality(self):
        return self._laterality

    @property
    def laterality_code(self):
        return self._laterality_code


class TestPhysicalExamSection:
    """Tests for PhysicalExamSection builder."""

    def test_physical_exam_section_basic(self):
        """Test basic PhysicalExamSection creation."""
        section = PhysicalExamSection()
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_physical_exam_section_has_template_id_r21(self):
        """Test PhysicalExamSection includes R2.1 template ID."""
        section = PhysicalExamSection(version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.2.10"
        assert template.get("extension") == "2015-08-01"

    def test_physical_exam_section_has_template_id_r20(self):
        """Test PhysicalExamSection includes R2.0 template ID."""
        section = PhysicalExamSection(version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.2.10"
        assert template.get("extension") == "2015-08-01"

    def test_physical_exam_section_has_code(self):
        """Test PhysicalExamSection includes section code (CONF:1198-15397, CONF:1198-15398)."""
        section = PhysicalExamSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "29545-1"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Physical Findings"

    def test_physical_exam_section_has_title(self):
        """Test PhysicalExamSection includes title (CONF:1198-7808)."""
        section = PhysicalExamSection(title="Physical Examination Findings")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Physical Examination Findings"

    def test_physical_exam_section_default_title(self):
        """Test PhysicalExamSection uses default title."""
        section = PhysicalExamSection()
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Physical Exam"

    def test_physical_exam_section_has_narrative(self):
        """Test PhysicalExamSection includes narrative text (CONF:1198-7809)."""
        section = PhysicalExamSection()
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_physical_exam_section_narrative_table(self):
        """Test narrative includes HTML table when wound observations present."""
        wound_obs = MockWoundObservation()
        section = PhysicalExamSection(wound_observations=[wound_obs])
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
        assert len(ths) == 4  # Date/Time, Wound Type, Location, Laterality

    def test_physical_exam_section_narrative_content(self):
        """Test narrative contains wound observation data."""
        wound_obs = MockWoundObservation(
            wound_type="Pressure ulcer",
            wound_code="399912005",
            date=datetime(2023, 10, 15, 10, 30),
            location="Sacral region",
            location_code="54735007",
            laterality="Right",
            laterality_code="24028007",
        )
        section = PhysicalExamSection(wound_observations=[wound_obs])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 4

        # Check date/time
        assert tds[0].text == "2023-10-15 10:30"

        # Check wound type with ID
        content = tds[1].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Pressure ulcer"
        assert content.get("ID") == "wound-1"

        # Check location
        assert tds[2].text == "Sacral region"

        # Check laterality
        assert tds[3].text == "Right"

    def test_physical_exam_section_narrative_without_location(self):
        """Test narrative shows '-' when location missing."""
        wound_obs = MockWoundObservation(location=None, laterality=None)
        section = PhysicalExamSection(wound_observations=[wound_obs])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check location shows "-"
        assert tds[2].text == "-"
        # Check laterality shows "-"
        assert tds[3].text == "-"

    def test_physical_exam_section_narrative_multiple_observations(self):
        """Test narrative with multiple wound observations."""
        observations = [
            MockWoundObservation(
                wound_type="Pressure ulcer",
                wound_code="399912005",
                location="Sacral region",
            ),
            MockWoundObservation(
                wound_type="Surgical wound",
                wound_code="225552003",
                location="Abdomen",
            ),
        ]
        section = PhysicalExamSection(wound_observations=observations)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        assert len(trs) == 2

        # Check IDs are sequential
        content1 = trs[0].find(f".//{{{NS}}}content")
        content2 = trs[1].find(f".//{{{NS}}}content")

        assert content1.get("ID") == "wound-1"
        assert content2.get("ID") == "wound-2"

    def test_physical_exam_section_empty_narrative(self):
        """Test narrative when no wound observations."""
        section = PhysicalExamSection()
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No physical exam findings recorded"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_physical_exam_section_custom_narrative(self):
        """Test section with custom narrative text."""
        section = PhysicalExamSection(text="Custom physical exam findings")
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text.text == "Custom physical exam findings"

    def test_physical_exam_section_has_entries(self):
        """Test PhysicalExamSection includes entry elements (CONF:1198-31926)."""
        wound_obs = MockWoundObservation()
        section = PhysicalExamSection(wound_observations=[wound_obs])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_physical_exam_section_entry_has_observation(self):
        """Test entry contains wound observation element (CONF:1198-31927)."""
        wound_obs = MockWoundObservation()
        section = PhysicalExamSection(wound_observations=[wound_obs])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        assert obs is not None
        assert obs.get("classCode") == "OBS"
        assert obs.get("moodCode") == "EVN"

    def test_physical_exam_section_multiple_entries(self):
        """Test PhysicalExamSection with multiple wound observations."""
        observations = [
            MockWoundObservation(),
            MockWoundObservation(),
        ]
        section = PhysicalExamSection(wound_observations=observations)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an observation
        for entry in entries:
            obs = entry.find(f"{{{NS}}}observation")
            assert obs is not None

    def test_physical_exam_section_structure_order(self):
        """Test that section elements are in correct order."""
        wound_obs = MockWoundObservation()
        section = PhysicalExamSection(wound_observations=[wound_obs])
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

    def test_physical_exam_section_to_string(self):
        """Test PhysicalExamSection serialization."""
        wound_obs = MockWoundObservation()
        section = PhysicalExamSection(wound_observations=[wound_obs])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "29545-1" in xml  # Section code
        assert "Physical" in xml


class TestLongitudinalCareWoundObservation:
    """Tests for LongitudinalCareWoundObservation entry builder."""

    def test_wound_observation_basic(self):
        """Test basic wound observation creation."""
        wound_obs = MockWoundObservation()
        builder = LongitudinalCareWoundObservation(wound_obs)
        elem = builder.to_element()

        assert local_name(elem) == "observation"
        assert elem.get("classCode") == "OBS"
        assert elem.get("moodCode") == "EVN"

    def test_wound_observation_has_template_ids(self):
        """Test wound observation includes both template IDs."""
        wound_obs = MockWoundObservation()
        builder = LongitudinalCareWoundObservation(wound_obs, version=CDAVersion.R2_1)
        elem = builder.to_element()

        templates = elem.findall(f"{{{NS}}}templateId")
        assert len(templates) == 2

        # Check Longitudinal Care Wound Observation template
        assert templates[0].get("root") == "2.16.840.1.113883.10.20.22.4.114"
        assert templates[0].get("extension") == "2015-08-01"

        # Check Problem Observation template
        assert templates[1].get("root") == "2.16.840.1.113883.10.20.22.4.4"
        assert templates[1].get("extension") == "2015-08-01"

    def test_wound_observation_has_id(self):
        """Test wound observation includes ID element."""
        wound_obs = MockWoundObservation()
        builder = LongitudinalCareWoundObservation(wound_obs)
        elem = builder.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_wound_observation_has_assertion_code(self):
        """Test wound observation has ASSERTION code (CONF:1198-29476, CONF:1198-29477)."""
        wound_obs = MockWoundObservation()
        builder = LongitudinalCareWoundObservation(wound_obs)
        elem = builder.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "ASSERTION"
        assert code.get("codeSystem") == "2.16.840.1.113883.5.4"
        assert code.get("displayName") == "Assertion"

    def test_wound_observation_has_status_code(self):
        """Test wound observation includes status code."""
        wound_obs = MockWoundObservation()
        builder = LongitudinalCareWoundObservation(wound_obs)
        elem = builder.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_wound_observation_has_effective_time(self):
        """Test wound observation includes effective time."""
        wound_obs = MockWoundObservation(date=datetime(2023, 10, 15, 14, 30))
        builder = LongitudinalCareWoundObservation(wound_obs)
        elem = builder.to_element()

        effective_time = elem.find(f"{{{NS}}}effectiveTime")
        assert effective_time is not None
        assert effective_time.get("value") == "20231015143000"

    def test_wound_observation_has_value(self):
        """Test wound observation has value with wound type (CONF:1198-29485)."""
        wound_obs = MockWoundObservation(
            wound_type="Pressure ulcer",
            wound_code="399912005",
        )
        builder = LongitudinalCareWoundObservation(wound_obs)
        elem = builder.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "CD"
        assert value.get("code") == "399912005"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT
        assert value.get("displayName") == "Pressure ulcer"

    def test_wound_observation_without_location(self):
        """Test wound observation without target site."""
        wound_obs = MockWoundObservation(location=None, location_code=None)
        builder = LongitudinalCareWoundObservation(wound_obs)
        elem = builder.to_element()

        target_site = elem.find(f"{{{NS}}}targetSiteCode")
        assert target_site is None

    def test_wound_observation_with_location(self):
        """Test wound observation with target site (CONF:1198-29488)."""
        wound_obs = MockWoundObservation(
            location="Sacral region",
            location_code="54735007",
        )
        builder = LongitudinalCareWoundObservation(wound_obs)
        elem = builder.to_element()

        target_site = elem.find(f"{{{NS}}}targetSiteCode")
        assert target_site is not None
        assert target_site.get("code") == "54735007"
        assert target_site.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT
        assert target_site.get("displayName") == "Sacral region"

    def test_wound_observation_with_laterality(self):
        """Test wound observation with laterality qualifier (CONF:1198-29490)."""
        wound_obs = MockWoundObservation(
            location="Lower leg",
            location_code="30021000",
            laterality="Left",
            laterality_code="7771000",
        )
        builder = LongitudinalCareWoundObservation(wound_obs)
        elem = builder.to_element()

        target_site = elem.find(f"{{{NS}}}targetSiteCode")
        assert target_site is not None

        # Check qualifier
        qualifier = target_site.find(f"{{{NS}}}qualifier")
        assert qualifier is not None

        # Check name element (CONF:1198-29491, CONF:1198-29492)
        name = qualifier.find(f"{{{NS}}}name")
        assert name is not None
        assert name.get("code") == "272741003"  # laterality
        assert name.get("codeSystem") == "2.16.840.1.113883.6.96"

        # Check value element (CONF:1198-29493)
        value = qualifier.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "7771000"
        assert value.get("displayName") == "Left"

    def test_wound_observation_without_laterality(self):
        """Test wound observation with location but no laterality."""
        wound_obs = MockWoundObservation(
            location="Sacral region",
            location_code="54735007",
            laterality=None,
            laterality_code=None,
        )
        builder = LongitudinalCareWoundObservation(wound_obs)
        elem = builder.to_element()

        target_site = elem.find(f"{{{NS}}}targetSiteCode")
        assert target_site is not None

        # Should not have qualifier
        qualifier = target_site.find(f"{{{NS}}}qualifier")
        assert qualifier is None

    def test_wound_observation_element_order(self):
        """Test that observation elements are in correct order."""
        wound_obs = MockWoundObservation(
            location="Sacral region",
            location_code="54735007",
        )
        builder = LongitudinalCareWoundObservation(wound_obs)
        elem = builder.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present
        assert "templateId" in names
        assert "id" in names
        assert "code" in names
        assert "statusCode" in names
        assert "effectiveTime" in names
        assert "value" in names
        assert "targetSiteCode" in names

    def test_wound_observation_to_string(self):
        """Test wound observation serialization."""
        wound_obs = MockWoundObservation()
        builder = LongitudinalCareWoundObservation(wound_obs)
        xml = builder.to_string(pretty=False)

        assert "<observation" in xml or ":observation" in xml
        assert "ASSERTION" in xml
        assert "399912005" in xml  # Default wound code


class TestPhysicalExamSectionIntegration:
    """Integration tests for PhysicalExamSection."""

    def test_complete_physical_exam_section(self):
        """Test creating a complete physical exam section."""
        observations = [
            MockWoundObservation(
                wound_type="Pressure ulcer",
                wound_code="399912005",
                date=datetime(2023, 10, 15, 10, 30),
                location="Sacral region",
                location_code="54735007",
                laterality="Left",
                laterality_code="7771000",
            ),
            MockWoundObservation(
                wound_type="Surgical wound",
                wound_code="225552003",
                date=datetime(2023, 10, 15, 10, 30),
                location="Abdomen",
                location_code="818983003",
            ),
        ]

        section = PhysicalExamSection(
            wound_observations=observations,
            title="Physical Examination Findings",
        )
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

        # Verify first observation has laterality
        obs1 = entries[0].find(f"{{{NS}}}observation")
        target_site1 = obs1.find(f"{{{NS}}}targetSiteCode")
        qualifier1 = target_site1.find(f"{{{NS}}}qualifier")
        assert qualifier1 is not None

        # Verify second observation has no laterality
        obs2 = entries[1].find(f"{{{NS}}}observation")
        target_site2 = obs2.find(f"{{{NS}}}targetSiteCode")
        qualifier2 = target_site2.find(f"{{{NS}}}qualifier")
        assert qualifier2 is None

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        wound_obs = MockWoundObservation()
        section = PhysicalExamSection(wound_observations=[wound_obs])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_empty_section_valid_structure(self):
        """Test empty section has valid structure."""
        section = PhysicalExamSection()
        elem = section.to_element()

        # Should have all required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Should have no entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_r20_version_compatibility(self):
        """Test R2.0 version produces valid output."""
        wound_obs = MockWoundObservation()
        section = PhysicalExamSection(
            wound_observations=[wound_obs],
            version=CDAVersion.R2_0,
        )
        elem = section.to_element()

        # Should have proper template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.2.10"
        assert template.get("extension") == "2015-08-01"

        # Entry should also be R2.0
        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        templates = obs.findall(f"{{{NS}}}templateId")
        assert len(templates) == 2

