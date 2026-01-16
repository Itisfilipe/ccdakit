"""Tests for FunctionalStatusSection builder."""

from datetime import datetime
from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.sections.functional_status import FunctionalStatusSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockFunctionalStatusObservation:
    """Mock functional status observation for testing."""

    def __init__(
        self,
        type="Ambulation",
        code="129006008",
        code_system=None,
        value="Walks independently",
        value_code="165245003",
        value_code_system=None,
        date=datetime(2023, 10, 1, 10, 30),
        interpretation=None,
    ):
        self._type = type
        self._code = code
        self._code_system = code_system
        self._value = value
        self._value_code = value_code
        self._value_code_system = value_code_system
        self._date = date
        self._interpretation = interpretation

    @property
    def type(self):
        return self._type

    @property
    def code(self):
        return self._code

    @property
    def code_system(self) -> Optional[str]:
        return self._code_system

    @property
    def value(self):
        return self._value

    @property
    def value_code(self):
        return self._value_code

    @property
    def value_code_system(self) -> Optional[str]:
        return self._value_code_system

    @property
    def date(self):
        return self._date

    @property
    def interpretation(self) -> Optional[str]:
        return self._interpretation


class MockFunctionalStatusOrganizer:
    """Mock functional status organizer for testing."""

    def __init__(
        self,
        category="Mobility",
        category_code="d4",
        category_code_system=None,
        observations=None,
    ):
        self._category = category
        self._category_code = category_code
        self._category_code_system = category_code_system
        self._observations = observations or []

    @property
    def category(self):
        return self._category

    @property
    def category_code(self):
        return self._category_code

    @property
    def category_code_system(self) -> Optional[str]:
        return self._category_code_system

    @property
    def observations(self) -> Sequence[MockFunctionalStatusObservation]:
        return self._observations


class TestFunctionalStatusSection:
    """Tests for FunctionalStatusSection builder."""

    def test_functional_status_section_basic(self):
        """Test basic FunctionalStatusSection creation."""
        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_functional_status_section_has_template_id_r21(self):
        """Test FunctionalStatusSection includes R2.1 template ID."""
        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.14"
        assert template.get("extension") == "2014-06-09"

    def test_functional_status_section_has_template_id_r20(self):
        """Test FunctionalStatusSection includes R2.0 template ID."""
        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.14"
        assert template.get("extension") == "2014-06-09"

    def test_functional_status_section_has_code(self):
        """Test FunctionalStatusSection includes section code (CONF:1098-14578)."""
        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "47420-5"  # CONF:1098-14579
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # CONF:1098-30866
        assert code.get("displayName") == "Functional Status"

    def test_functional_status_section_has_title(self):
        """Test FunctionalStatusSection includes title (CONF:1098-7922)."""
        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer], title="Patient Functional Status")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Patient Functional Status"

    def test_functional_status_section_default_title(self):
        """Test FunctionalStatusSection uses default title."""
        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Functional Status"

    def test_functional_status_section_has_narrative(self):
        """Test FunctionalStatusSection includes narrative text (CONF:1098-7923)."""
        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_functional_status_section_narrative_table(self):
        """Test narrative includes HTML table."""
        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer])
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
        assert len(ths) == 4  # Category, Functional Status, Value, Date/Time

    def test_functional_status_section_narrative_content(self):
        """Test narrative contains functional status data."""
        observations = [
            MockFunctionalStatusObservation(
                type="Ambulation",
                code="129006008",
                value="Walks independently",
                value_code="165245003",
                date=datetime(2023, 10, 15, 10, 30),
            )
        ]
        organizer = MockFunctionalStatusOrganizer(
            category="Mobility",
            category_code="d4",
            observations=observations,
        )
        section = FunctionalStatusSection([organizer])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 4

        # Check category
        assert tds[0].text == "Mobility"

        # Check functional status type with ID
        content = tds[1].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Ambulation"
        assert content.get("ID") == "funcstatus-1-1"

        # Check value
        assert tds[2].text == "Walks independently"

        # Check date/time
        assert tds[3].text == "2023-10-15 10:30"

    def test_functional_status_section_narrative_multiple_observations(self):
        """Test narrative with multiple observations in one organizer."""
        observations = [
            MockFunctionalStatusObservation(type="Ambulation", value="Walks independently"),
            MockFunctionalStatusObservation(type="Bathing", value="Requires minimal assistance"),
            MockFunctionalStatusObservation(type="Feeding", value="Independent"),
        ]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer])
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

        assert content1.get("ID") == "funcstatus-1-1"
        assert content2.get("ID") == "funcstatus-1-2"
        assert content3.get("ID") == "funcstatus-1-3"

    def test_functional_status_section_narrative_multiple_organizers(self):
        """Test narrative with multiple organizers."""
        organizers = [
            MockFunctionalStatusOrganizer(
                category="Mobility",
                observations=[MockFunctionalStatusObservation(type="Ambulation")],
            ),
            MockFunctionalStatusOrganizer(
                category="Self-Care",
                observations=[MockFunctionalStatusObservation(type="Bathing")],
            ),
        ]
        section = FunctionalStatusSection(organizers)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        assert len(trs) == 2

        # Check IDs from different organizers
        content1 = trs[0].find(f".//{{{NS}}}content")
        content2 = trs[1].find(f".//{{{NS}}}content")

        assert content1.get("ID") == "funcstatus-1-1"
        assert content2.get("ID") == "funcstatus-2-1"

        # Check categories
        tds1 = trs[0].findall(f"{{{NS}}}td")
        tds2 = trs[1].findall(f"{{{NS}}}td")
        assert tds1[0].text == "Mobility"
        assert tds2[0].text == "Self-Care"

    def test_functional_status_section_empty_narrative(self):
        """Test narrative when no functional status data."""
        section = FunctionalStatusSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No functional status recorded"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_functional_status_section_has_entries(self):
        """Test FunctionalStatusSection includes entry elements (CONF:1098-14414)."""
        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_functional_status_section_entry_has_organizer(self):
        """Test entry contains organizer element (CONF:1098-14415)."""
        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        org = entry.find(f"{{{NS}}}organizer")
        assert org is not None
        assert org.get("classCode") == "CLUSTER"

    def test_functional_status_section_multiple_entries(self):
        """Test FunctionalStatusSection with multiple organizers."""
        organizers = [
            MockFunctionalStatusOrganizer(observations=[MockFunctionalStatusObservation()]),
            MockFunctionalStatusOrganizer(observations=[MockFunctionalStatusObservation()]),
        ]
        section = FunctionalStatusSection(organizers)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an organizer
        for entry in entries:
            org = entry.find(f"{{{NS}}}organizer")
            assert org is not None

    def test_functional_status_section_to_string(self):
        """Test FunctionalStatusSection serialization."""
        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "47420-5" in xml  # Section code
        assert "Functional" in xml

    def test_functional_status_section_structure_order(self):
        """Test that section elements are in correct order."""
        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer])
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


class TestFunctionalStatusOrganizer:
    """Tests for FunctionalStatusOrganizer builder."""

    def test_organizer_has_template_id_r21(self):
        """Test organizer includes R2.1 template ID (CONF:1098-14361)."""
        from ccdakit.builders.entries.functional_status import FunctionalStatusOrganizer

        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        builder = FunctionalStatusOrganizer(organizer, version=CDAVersion.R2_1)
        elem = builder.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.66"  # CONF:1098-14362
        assert template.get("extension") == "2014-06-09"  # CONF:1098-32569

    def test_organizer_has_class_code(self):
        """Test organizer has classCode CLUSTER (CONF:1098-14355)."""
        from ccdakit.builders.entries.functional_status import FunctionalStatusOrganizer

        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        builder = FunctionalStatusOrganizer(organizer)
        elem = builder.to_element()

        assert elem.get("classCode") == "CLUSTER"

    def test_organizer_has_mood_code(self):
        """Test organizer has moodCode EVN (CONF:1098-14357)."""
        from ccdakit.builders.entries.functional_status import FunctionalStatusOrganizer

        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        builder = FunctionalStatusOrganizer(organizer)
        elem = builder.to_element()

        assert elem.get("moodCode") == "EVN"

    def test_organizer_has_id(self):
        """Test organizer has at least one ID (CONF:1098-14363)."""
        from ccdakit.builders.entries.functional_status import FunctionalStatusOrganizer

        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        builder = FunctionalStatusOrganizer(organizer)
        elem = builder.to_element()

        ids = elem.findall(f"{{{NS}}}id")
        assert len(ids) >= 1

    def test_organizer_has_code(self):
        """Test organizer has code element (CONF:1098-14364)."""
        from ccdakit.builders.entries.functional_status import FunctionalStatusOrganizer

        [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(category="Mobility", category_code="d4")
        builder = FunctionalStatusOrganizer(organizer)
        elem = builder.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "d4"
        assert code.get("displayName") == "Mobility"

    def test_organizer_code_uses_icf_by_default(self):
        """Test organizer code defaults to ICF code system (CONF:1098-31417)."""
        from ccdakit.builders.entries.functional_status import FunctionalStatusOrganizer

        [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(category_code="d4")
        builder = FunctionalStatusOrganizer(organizer)
        elem = builder.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code.get("codeSystem") == "2.16.840.1.113883.6.254"  # ICF

    def test_organizer_code_uses_custom_code_system(self):
        """Test organizer code can use custom code system."""
        from ccdakit.builders.entries.functional_status import FunctionalStatusOrganizer

        [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(
            category_code="74465-6", category_code_system="2.16.840.1.113883.6.1"
        )
        builder = FunctionalStatusOrganizer(organizer)
        elem = builder.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC

    def test_organizer_has_status_code(self):
        """Test organizer has statusCode completed (CONF:1098-14358, CONF:1098-31434)."""
        from ccdakit.builders.entries.functional_status import FunctionalStatusOrganizer

        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        builder = FunctionalStatusOrganizer(organizer)
        elem = builder.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_organizer_has_components(self):
        """Test organizer has component elements (CONF:1098-14359)."""
        from ccdakit.builders.entries.functional_status import FunctionalStatusOrganizer

        observations = [
            MockFunctionalStatusObservation(type="Ambulation"),
            MockFunctionalStatusObservation(type="Bathing"),
        ]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        builder = FunctionalStatusOrganizer(organizer)
        elem = builder.to_element()

        components = elem.findall(f"{{{NS}}}component")
        assert len(components) == 2

    def test_organizer_components_contain_observations(self):
        """Test components contain observations (CONF:1098-14368)."""
        from ccdakit.builders.entries.functional_status import FunctionalStatusOrganizer

        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        builder = FunctionalStatusOrganizer(organizer)
        elem = builder.to_element()

        component = elem.find(f"{{{NS}}}component")
        obs = component.find(f"{{{NS}}}observation")
        assert obs is not None
        assert obs.get("classCode") == "OBS"


class TestFunctionalStatusObservation:
    """Tests for FunctionalStatusObservation builder."""

    def test_observation_has_template_id_r21(self):
        """Test observation includes R2.1 template ID (CONF:1098-13889)."""
        from ccdakit.builders.entries.functional_status import (
            FunctionalStatusObservation,
        )

        observation = MockFunctionalStatusObservation()
        builder = FunctionalStatusObservation(observation, version=CDAVersion.R2_1)
        elem = builder.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.67"  # CONF:1098-13890
        assert template.get("extension") == "2014-06-09"  # CONF:1098-32568

    def test_observation_has_class_code(self):
        """Test observation has classCode OBS (CONF:1098-13905)."""
        from ccdakit.builders.entries.functional_status import (
            FunctionalStatusObservation,
        )

        observation = MockFunctionalStatusObservation()
        builder = FunctionalStatusObservation(observation)
        elem = builder.to_element()

        assert elem.get("classCode") == "OBS"

    def test_observation_has_mood_code(self):
        """Test observation has moodCode EVN (CONF:1098-13906)."""
        from ccdakit.builders.entries.functional_status import (
            FunctionalStatusObservation,
        )

        observation = MockFunctionalStatusObservation()
        builder = FunctionalStatusObservation(observation)
        elem = builder.to_element()

        assert elem.get("moodCode") == "EVN"

    def test_observation_has_id(self):
        """Test observation has at least one ID (CONF:1098-13907)."""
        from ccdakit.builders.entries.functional_status import (
            FunctionalStatusObservation,
        )

        observation = MockFunctionalStatusObservation()
        builder = FunctionalStatusObservation(observation)
        elem = builder.to_element()

        ids = elem.findall(f"{{{NS}}}id")
        assert len(ids) >= 1

    def test_observation_has_fixed_code(self):
        """Test observation has fixed code 54522-8 (CONF:1098-13908, CONF:1098-31522)."""
        from ccdakit.builders.entries.functional_status import (
            FunctionalStatusObservation,
        )

        observation = MockFunctionalStatusObservation()
        builder = FunctionalStatusObservation(observation)
        elem = builder.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "54522-8"  # Functional status
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # CONF:1098-31523 (LOINC)
        assert code.get("displayName") == "Functional status"

    def test_observation_has_status_code(self):
        """Test observation has statusCode completed (CONF:1098-13929, CONF:1098-19101)."""
        from ccdakit.builders.entries.functional_status import (
            FunctionalStatusObservation,
        )

        observation = MockFunctionalStatusObservation()
        builder = FunctionalStatusObservation(observation)
        elem = builder.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_observation_has_effective_time(self):
        """Test observation has effectiveTime (CONF:1098-13930)."""
        from ccdakit.builders.entries.functional_status import (
            FunctionalStatusObservation,
        )

        observation = MockFunctionalStatusObservation(date=datetime(2023, 10, 15, 10, 30))
        builder = FunctionalStatusObservation(observation)
        elem = builder.to_element()

        effective_time = elem.find(f"{{{NS}}}effectiveTime")
        assert effective_time is not None
        assert effective_time.get("value").startswith("20231015103000")

    def test_observation_has_value(self):
        """Test observation has value element (CONF:1098-13932)."""
        from ccdakit.builders.entries.functional_status import (
            FunctionalStatusObservation,
        )

        observation = MockFunctionalStatusObservation(
            value="Walks independently", value_code="165245003"
        )
        builder = FunctionalStatusObservation(observation)
        elem = builder.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "CD"
        assert value.get("code") == "165245003"
        assert value.get("displayName") == "Walks independently"

    def test_observation_value_uses_snomed_by_default(self):
        """Test observation value defaults to SNOMED CT (CONF:1098-14234)."""
        from ccdakit.builders.entries.functional_status import (
            FunctionalStatusObservation,
        )

        observation = MockFunctionalStatusObservation(value_code="165245003")
        builder = FunctionalStatusObservation(observation)
        elem = builder.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT

    def test_observation_value_uses_custom_code_system(self):
        """Test observation value can use custom code system."""
        from ccdakit.builders.entries.functional_status import (
            FunctionalStatusObservation,
        )

        observation = MockFunctionalStatusObservation(
            value_code="12345", value_code_system="2.16.840.1.113883.6.1"
        )
        builder = FunctionalStatusObservation(observation)
        elem = builder.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value.get("codeSystem") == "2.16.840.1.113883.6.1"


class TestFunctionalStatusSectionIntegration:
    """Integration tests for FunctionalStatusSection."""

    def test_complete_functional_status_section(self):
        """Test creating a complete functional status section."""
        organizers = [
            MockFunctionalStatusOrganizer(
                category="Mobility",
                category_code="d4",
                observations=[
                    MockFunctionalStatusObservation(
                        type="Ambulation",
                        code="129006008",
                        value="Walks independently",
                        value_code="165245003",
                        date=datetime(2023, 10, 15, 10, 30),
                    ),
                    MockFunctionalStatusObservation(
                        type="Transfer",
                        code="285652008",
                        value="Requires minimal assistance",
                        value_code="371152001",
                        date=datetime(2023, 10, 15, 10, 35),
                    ),
                ],
            ),
            MockFunctionalStatusOrganizer(
                category="Self-Care",
                category_code="d5",
                observations=[
                    MockFunctionalStatusObservation(
                        type="Bathing",
                        code="284785009",
                        value="Independent",
                        value_code="371153006",
                        date=datetime(2023, 10, 15, 10, 40),
                    ),
                ],
            ),
        ]

        section = FunctionalStatusSection(organizers, title="Functional Status History")
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify narrative table has 3 rows (total observations)
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 3

        # Verify 2 entries (2 organizers)
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Verify first organizer has 2 components
        organizer1 = entries[0].find(f"{{{NS}}}organizer")
        components1 = organizer1.findall(f"{{{NS}}}component")
        assert len(components1) == 2

        # Verify second organizer has 1 component
        organizer2 = entries[1].find(f"{{{NS}}}organizer")
        components2 = organizer2.findall(f"{{{NS}}}component")
        assert len(components2) == 1

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_with_no_data(self):
        """Test section handles empty data gracefully."""
        section = FunctionalStatusSection([])
        elem = section.to_element()

        # Should still have required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Should have no entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

        # Narrative should indicate no data
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert "No functional status" in paragraph.text

    def test_section_r20_version(self):
        """Test section can be created with R2.0 version."""
        observations = [MockFunctionalStatusObservation()]
        organizer = MockFunctionalStatusOrganizer(observations=observations)
        section = FunctionalStatusSection([organizer], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("extension") == "2014-06-09"

    def test_full_xml_structure(self):
        """Test complete XML structure is well-formed."""
        observations = [
            MockFunctionalStatusObservation(
                type="Ambulation",
                code="129006008",
                value="Walks independently",
                value_code="165245003",
                date=datetime(2023, 10, 15, 10, 30),
            )
        ]
        organizer = MockFunctionalStatusOrganizer(
            category="Mobility",
            category_code="d4",
            observations=observations,
        )
        section = FunctionalStatusSection([organizer])

        xml_str = section.to_string(pretty=True)

        # Verify XML is well-formed by parsing it
        parsed = etree.fromstring(xml_str.encode("utf-8"))
        assert local_name(parsed) == "section"

        # Verify key elements are present
        assert "templateId" in xml_str
        assert "47420-5" in xml_str  # Section code
        assert "Functional Status" in xml_str
        assert "Ambulation" in xml_str
        assert "Walks independently" in xml_str
