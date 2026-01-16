"""Tests for MentalStatusSection builder."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.entries.mental_status import (
    MentalStatusObservation,
    MentalStatusOrganizer,
)
from ccdakit.builders.sections.mental_status import MentalStatusSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockMentalStatusObservation:
    """Mock mental status observation for testing."""

    def __init__(
        self,
        category="Cognition",
        category_code="d110",
        category_code_system="ICF",
        value="Alert and oriented",
        value_code="248234008",
        observation_date=date(2023, 6, 15),
        status="completed",
        persistent_id=None,
    ):
        self._category = category
        self._category_code = category_code
        self._category_code_system = category_code_system
        self._value = value
        self._value_code = value_code
        self._observation_date = observation_date
        self._status = status
        self._persistent_id = persistent_id

    @property
    def category(self):
        return self._category

    @property
    def category_code(self):
        return self._category_code

    @property
    def category_code_system(self):
        return self._category_code_system

    @property
    def value(self):
        return self._value

    @property
    def value_code(self):
        return self._value_code

    @property
    def observation_date(self):
        return self._observation_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class MockMentalStatusOrganizer:
    """Mock mental status organizer for testing."""

    def __init__(
        self,
        category="Mood and Affect",
        category_code="b152",
        category_code_system="ICF",
        observations=None,
        effective_time_low=None,
        effective_time_high=None,
        persistent_id=None,
    ):
        self._category = category
        self._category_code = category_code
        self._category_code_system = category_code_system
        self._observations = observations or []
        self._effective_time_low = effective_time_low
        self._effective_time_high = effective_time_high
        self._persistent_id = persistent_id

    @property
    def category(self):
        return self._category

    @property
    def category_code(self):
        return self._category_code

    @property
    def category_code_system(self):
        return self._category_code_system

    @property
    def observations(self):
        return self._observations

    @property
    def effective_time_low(self):
        return self._effective_time_low

    @property
    def effective_time_high(self):
        return self._effective_time_high

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPersistentID:
    """Mock persistent ID for testing."""

    def __init__(self, root="2.16.840.1.113883.19.5", extension="12345"):
        self._root = root
        self._extension = extension

    @property
    def root(self):
        return self._root

    @property
    def extension(self):
        return self._extension


class TestMentalStatusObservation:
    """Tests for MentalStatusObservation builder."""

    def test_observation_basic(self):
        """Test basic MentalStatusObservation creation."""
        obs = MockMentalStatusObservation()
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        assert local_name(elem) == "observation"
        assert elem.get("classCode") == "OBS"
        assert elem.get("moodCode") == "EVN"

    def test_observation_template_id_r21(self):
        """Test observation includes R2.1 template ID."""
        obs = MockMentalStatusObservation()
        builder = MentalStatusObservation(obs, version=CDAVersion.R2_1)
        elem = builder.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.74"
        assert template.get("extension") == "2015-08-01"

    def test_observation_has_id(self):
        """Test observation includes ID element."""
        obs = MockMentalStatusObservation()
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None

    def test_observation_persistent_id(self):
        """Test observation uses persistent ID when provided."""
        pid = MockPersistentID(root="1.2.3.4", extension="ABC123")
        obs = MockMentalStatusObservation(persistent_id=pid)
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem.get("root") == "1.2.3.4"
        assert id_elem.get("extension") == "ABC123"

    def test_observation_code_cognitive_function(self):
        """Test observation includes correct code for cognitive function."""
        obs = MockMentalStatusObservation()
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "373930000"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"
        assert code.get("displayName") == "Cognitive function"

    def test_observation_code_has_loinc_translation(self):
        """Test observation code includes LOINC translation."""
        obs = MockMentalStatusObservation()
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        code = elem.find(f"{{{NS}}}code")
        translation = code.find(f"{{{NS}}}translation")
        assert translation is not None
        assert translation.get("code") == "75275-8"
        assert translation.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert translation.get("displayName") == "Cognitive Function"

    def test_observation_status_code(self):
        """Test observation includes statusCode."""
        obs = MockMentalStatusObservation(status="completed")
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_observation_effective_time_date(self):
        """Test observation includes effectiveTime with date."""
        obs = MockMentalStatusObservation(observation_date=date(2023, 6, 15))
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None
        assert eff_time.get("value") == "20230615"

    def test_observation_effective_time_datetime(self):
        """Test observation includes effectiveTime with datetime."""
        obs = MockMentalStatusObservation(observation_date=datetime(2023, 6, 15, 14, 30, 0))
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None
        # Use startswith to accommodate timezone suffix per C-CDA spec CONF:81-10130
        assert eff_time.get("value").startswith("20230615143000")

    def test_observation_value_with_code(self):
        """Test observation value element with SNOMED code."""
        obs = MockMentalStatusObservation(
            value="Alert and oriented",
            value_code="248234008",
        )
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "CD"
        assert value.get("code") == "248234008"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"
        assert value.get("displayName") == "Alert and oriented"

    def test_observation_value_without_code(self):
        """Test observation value element without code uses nullFlavor."""
        obs = MockMentalStatusObservation(
            value="Patient appears anxious",
            value_code=None,
        )
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("nullFlavor") == "OTH"

        orig_text = value.find(f"{{{NS}}}originalText")
        assert orig_text is not None
        assert orig_text.text == "Patient appears anxious"


class TestMentalStatusOrganizer:
    """Tests for MentalStatusOrganizer builder."""

    def test_organizer_basic(self):
        """Test basic MentalStatusOrganizer creation."""
        obs = MockMentalStatusObservation()
        org = MockMentalStatusOrganizer(observations=[obs])
        builder = MentalStatusOrganizer(org)
        elem = builder.to_element()

        assert local_name(elem) == "organizer"
        assert elem.get("classCode") == "CLUSTER"
        assert elem.get("moodCode") == "EVN"

    def test_organizer_template_id_r21(self):
        """Test organizer includes R2.1 template ID."""
        obs = MockMentalStatusObservation()
        org = MockMentalStatusOrganizer(observations=[obs])
        builder = MentalStatusOrganizer(org, version=CDAVersion.R2_1)
        elem = builder.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.75"
        assert template.get("extension") == "2015-08-01"

    def test_organizer_has_id(self):
        """Test organizer includes ID element."""
        obs = MockMentalStatusObservation()
        org = MockMentalStatusOrganizer(observations=[obs])
        builder = MentalStatusOrganizer(org)
        elem = builder.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None

    def test_organizer_code_icf(self):
        """Test organizer code with ICF code system."""
        obs = MockMentalStatusObservation()
        org = MockMentalStatusOrganizer(
            category="Mood and Affect",
            category_code="b152",
            category_code_system="ICF",
            observations=[obs],
        )
        builder = MentalStatusOrganizer(org)
        elem = builder.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "b152"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.254"
        assert code.get("displayName") == "Mood and Affect"

    def test_organizer_code_loinc(self):
        """Test organizer code with LOINC code system."""
        obs = MockMentalStatusObservation()
        org = MockMentalStatusOrganizer(
            category="Cognition",
            category_code="75275-8",
            category_code_system="LOINC",
            observations=[obs],
        )
        builder = MentalStatusOrganizer(org)
        elem = builder.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "75275-8"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"

    def test_organizer_status_code(self):
        """Test organizer includes statusCode."""
        obs = MockMentalStatusObservation()
        org = MockMentalStatusOrganizer(observations=[obs])
        builder = MentalStatusOrganizer(org)
        elem = builder.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_organizer_effective_time(self):
        """Test organizer includes effectiveTime when provided."""
        obs = MockMentalStatusObservation()
        org = MockMentalStatusOrganizer(
            observations=[obs],
            effective_time_low=datetime(2023, 6, 1, 10, 0, 0),
            effective_time_high=datetime(2023, 6, 15, 16, 0, 0),
        )
        builder = MentalStatusOrganizer(org)
        elem = builder.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None

        low = eff_time.find(f"{{{NS}}}low")
        assert low is not None
        # Use startswith to accommodate timezone suffix per C-CDA spec CONF:81-10130
        assert low.get("value").startswith("20230601100000")

        high = eff_time.find(f"{{{NS}}}high")
        assert high is not None
        # Use startswith to accommodate timezone suffix per C-CDA spec CONF:81-10130
        assert high.get("value").startswith("20230615160000")

    def test_organizer_without_effective_time(self):
        """Test organizer without effectiveTime when not provided."""
        obs = MockMentalStatusObservation()
        org = MockMentalStatusOrganizer(observations=[obs])
        builder = MentalStatusOrganizer(org)
        elem = builder.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is None

    def test_organizer_components(self):
        """Test organizer includes component elements."""
        obs1 = MockMentalStatusObservation(value="Alert")
        obs2 = MockMentalStatusObservation(value="Oriented x3")
        org = MockMentalStatusOrganizer(observations=[obs1, obs2])
        builder = MentalStatusOrganizer(org)
        elem = builder.to_element()

        components = elem.findall(f"{{{NS}}}component")
        assert len(components) == 2

    def test_organizer_component_has_observation(self):
        """Test organizer component contains observation."""
        obs = MockMentalStatusObservation()
        org = MockMentalStatusOrganizer(observations=[obs])
        builder = MentalStatusOrganizer(org)
        elem = builder.to_element()

        component = elem.find(f"{{{NS}}}component")
        observation = component.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"

    def test_organizer_persistent_id(self):
        """Test organizer uses persistent ID when provided."""
        pid = MockPersistentID(root="1.2.3.4", extension="ORG789")
        obs = MockMentalStatusObservation()
        org = MockMentalStatusOrganizer(observations=[obs], persistent_id=pid)
        builder = MentalStatusOrganizer(org)
        elem = builder.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem.get("root") == "1.2.3.4"
        assert id_elem.get("extension") == "ORG789"

    def test_organizer_code_other_system(self):
        """Test organizer code with custom OID code system."""
        obs = MockMentalStatusObservation()
        org = MockMentalStatusOrganizer(
            category="Custom Category",
            category_code="12345",
            category_code_system="2.16.840.1.113883.6.999",
            observations=[obs],
        )
        builder = MentalStatusOrganizer(org)
        elem = builder.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "12345"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.999"


class TestMentalStatusSection:
    """Tests for MentalStatusSection builder."""

    def test_section_basic(self):
        """Test basic MentalStatusSection creation."""
        obs = MockMentalStatusObservation()
        section = MentalStatusSection(observations=[obs])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_template_id_r21(self):
        """Test section includes R2.1 template ID."""
        obs = MockMentalStatusObservation()
        section = MentalStatusSection(observations=[obs], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.56"
        assert template.get("extension") == "2015-08-01"

    def test_section_template_id_r20(self):
        """Test section includes R2.0 template ID."""
        obs = MockMentalStatusObservation()
        section = MentalStatusSection(observations=[obs], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.56"
        assert template.get("extension") == "2015-08-01"

    def test_section_code(self):
        """Test section includes correct code."""
        obs = MockMentalStatusObservation()
        section = MentalStatusSection(observations=[obs])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "10190-7"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert code.get("displayName") == "Mental Status"

    def test_section_title_default(self):
        """Test section uses default title."""
        obs = MockMentalStatusObservation()
        section = MentalStatusSection(observations=[obs])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Mental Status"

    def test_section_title_custom(self):
        """Test section uses custom title."""
        obs = MockMentalStatusObservation()
        section = MentalStatusSection(observations=[obs], title="Mental Health Assessment")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Mental Health Assessment"

    def test_section_has_text(self):
        """Test section includes text element."""
        obs = MockMentalStatusObservation()
        section = MentalStatusSection(observations=[obs])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_section_narrative_table(self):
        """Test narrative includes HTML table."""
        obs = MockMentalStatusObservation(
            category="Cognition",
            value="Alert and oriented",
            observation_date=date(2023, 6, 15),
        )
        section = MentalStatusSection(observations=[obs])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        assert table is not None
        assert table.get("border") == "1"

    def test_section_narrative_table_headers(self):
        """Test narrative table has correct headers."""
        obs = MockMentalStatusObservation()
        section = MentalStatusSection(observations=[obs])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        thead = table.find(f"{{{NS}}}thead")
        tr = thead.find(f"{{{NS}}}tr")
        ths = tr.findall(f"{{{NS}}}th")

        assert len(ths) == 4
        headers = [th.text for th in ths]
        assert "Category" in headers
        assert "Finding/Value" in headers
        assert "Date" in headers
        assert "Status" in headers

    def test_section_narrative_observation_content(self):
        """Test narrative contains observation data."""
        obs = MockMentalStatusObservation(
            category="Mood and Affect",
            value="Depressed mood",
            observation_date=date(2023, 6, 15),
            status="completed",
        )
        section = MentalStatusSection(observations=[obs])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        assert len(tds) == 4
        assert tds[0].text == "Mood and Affect"

        content = tds[1].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Depressed mood"
        assert content.get("ID") == "mental-status-1"

        assert tds[2].text == "2023-06-15"
        assert tds[3].text == "Completed"

    def test_section_narrative_empty(self):
        """Test narrative when no observations."""
        section = MentalStatusSection(observations=[], organizers=[])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No mental status observations recorded"

        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_section_narrative_multiple_observations(self):
        """Test narrative with multiple observations."""
        obs1 = MockMentalStatusObservation(
            category="Cognition",
            value="Alert and oriented",
            observation_date=date(2023, 6, 15),
        )
        obs2 = MockMentalStatusObservation(
            category="Mood and Affect",
            value="Anxious",
            observation_date=date(2023, 6, 15),
        )
        section = MentalStatusSection(observations=[obs1, obs2])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        assert len(trs) == 2

    def test_section_entry_with_observation(self):
        """Test section includes entry with observation."""
        obs = MockMentalStatusObservation()
        section = MentalStatusSection(observations=[obs])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        entry = entries[0]
        observation = entry.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"

    def test_section_entry_with_organizer(self):
        """Test section includes entry with organizer."""
        obs = MockMentalStatusObservation()
        org = MockMentalStatusOrganizer(observations=[obs])
        section = MentalStatusSection(organizers=[org])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        entry = entries[0]
        organizer = entry.find(f"{{{NS}}}organizer")
        assert organizer is not None
        assert organizer.get("classCode") == "CLUSTER"

    def test_section_multiple_organizers(self):
        """Test section with multiple organizers."""
        obs1 = MockMentalStatusObservation(value="Alert")
        obs2 = MockMentalStatusObservation(value="Anxious")

        org1 = MockMentalStatusOrganizer(
            category="Cognition",
            category_code="d110",
            observations=[obs1],
        )
        org2 = MockMentalStatusOrganizer(
            category="Mood and Affect",
            category_code="b152",
            observations=[obs2],
        )

        section = MentalStatusSection(organizers=[org1, org2])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_section_mixed_observations_and_organizers(self):
        """Test section with both observations and organizers."""
        obs1 = MockMentalStatusObservation(value="Alert")
        obs2 = MockMentalStatusObservation(value="Anxious")
        org = MockMentalStatusOrganizer(observations=[obs1])

        section = MentalStatusSection(observations=[obs2], organizers=[org])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check we have one organizer and one observation
        organizer = elem.find(f".//{{{NS}}}organizer")
        assert organizer is not None

        observations = elem.findall(f".//{{{NS}}}observation")
        # Should have 2 observations: 1 inside organizer, 1 standalone
        assert len(observations) >= 2

    def test_section_narrative_from_organizers(self):
        """Test narrative includes observations from organizers."""
        obs1 = MockMentalStatusObservation(
            category="Cognition",
            value="Alert",
            observation_date=date(2023, 6, 15),
        )
        obs2 = MockMentalStatusObservation(
            category="Cognition",
            value="Oriented x3",
            observation_date=date(2023, 6, 15),
        )
        org = MockMentalStatusOrganizer(
            category="Cognition Assessment",
            category_code="d110",
            observations=[obs1, obs2],
        )

        section = MentalStatusSection(organizers=[org])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        # Should have 2 rows for the 2 observations in organizer
        assert len(trs) == 2
        assert trs[0].findall(f"{{{NS}}}td")[0].text == "Cognition Assessment"

    def test_section_structure_order(self):
        """Test section elements are in correct order."""
        obs = MockMentalStatusObservation()
        section = MentalStatusSection(observations=[obs])
        elem = section.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        assert "templateId" in names
        assert "code" in names
        assert "title" in names
        assert "text" in names
        assert "entry" in names

        # Check order
        assert names.index("templateId") < names.index("code")
        assert names.index("code") < names.index("title")
        assert names.index("title") < names.index("text")
        assert names.index("text") < names.index("entry")

    def test_section_to_string(self):
        """Test section serialization."""
        obs = MockMentalStatusObservation()
        section = MentalStatusSection(observations=[obs])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "10190-7" in xml
        assert "Mental Status" in xml

    def test_section_observation_date_none(self):
        """Test section handles missing observation date."""
        obs = MockMentalStatusObservation(observation_date=None)
        section = MentalStatusSection(observations=[obs])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Date column should show "Unknown"
        assert tds[2].text == "Unknown"

    def test_section_observation_status_none(self):
        """Test section handles missing status."""
        obs = MockMentalStatusObservation(status=None)
        section = MentalStatusSection(observations=[obs])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Status column should show "Completed" as default
        assert tds[3].text == "Completed"

    def test_section_observation_category_none(self):
        """Test section handles missing category."""
        obs = MockMentalStatusObservation(category=None)
        section = MentalStatusSection(observations=[obs])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Category should show "General" as default
        assert tds[0].text == "General"


class TestMentalStatusSectionIntegration:
    """Integration tests for MentalStatusSection."""

    def test_complete_section_with_organizers(self):
        """Test creating a complete section with multiple organizers."""
        # Cognition observations
        cog_obs1 = MockMentalStatusObservation(
            category="Cognition",
            value="Alert and oriented x3",
            value_code="248234008",
            observation_date=date(2023, 6, 15),
        )
        cog_obs2 = MockMentalStatusObservation(
            category="Cognition",
            value="Good memory",
            value_code="301284009",
            observation_date=date(2023, 6, 15),
        )
        cog_org = MockMentalStatusOrganizer(
            category="Cognition",
            category_code="d110",
            category_code_system="ICF",
            observations=[cog_obs1, cog_obs2],
            effective_time_low=datetime(2023, 6, 15, 10, 0, 0),
            effective_time_high=datetime(2023, 6, 15, 10, 30, 0),
        )

        # Mood and Affect observations
        mood_obs = MockMentalStatusObservation(
            category="Mood and Affect",
            value="Depressed mood",
            value_code="366979004",
            observation_date=date(2023, 6, 15),
        )
        mood_org = MockMentalStatusOrganizer(
            category="Mood and Affect",
            category_code="b152",
            category_code_system="ICF",
            observations=[mood_obs],
        )

        section = MentalStatusSection(
            organizers=[cog_org, mood_org],
            title="Mental Status Examination",
        )
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify title
        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Mental Status Examination"

        # Verify narrative has 3 rows (2 cog + 1 mood)
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 3

        # Verify 2 organizer entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Verify each organizer has components
        for entry in entries:
            organizer = entry.find(f"{{{NS}}}organizer")
            assert organizer is not None
            components = organizer.findall(f"{{{NS}}}component")
            assert len(components) >= 1

    def test_complete_section_with_standalone_observations(self):
        """Test creating a complete section with standalone observations."""
        observations = [
            MockMentalStatusObservation(
                category="Appearance",
                value="Well-groomed",
                value_code="248157009",
                observation_date=date(2023, 6, 15),
            ),
            MockMentalStatusObservation(
                category="Behavior",
                value="Cooperative",
                value_code="225313000",
                observation_date=date(2023, 6, 15),
            ),
            MockMentalStatusObservation(
                category="Speech",
                value="Normal rate and rhythm",
                value_code="271823003",
                observation_date=date(2023, 6, 15),
            ),
        ]

        section = MentalStatusSection(observations=observations)
        elem = section.to_element()

        # Verify 3 observation entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 3

        # Verify narrative has 3 rows
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 3

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        obs = MockMentalStatusObservation()
        section = MentalStatusSection(observations=[obs])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None
        assert section_elem.find(f"{{{NS}}}text") is not None

    def test_null_flavor_handling(self):
        """Test section handles observations without codes (null flavor case)."""
        obs = MockMentalStatusObservation(
            value="Patient appears distracted and agitated",
            value_code=None,
        )
        section = MentalStatusSection(observations=[obs])
        elem = section.to_element()

        # Should still build successfully
        assert local_name(elem) == "section"

        # Check observation has nullFlavor
        observation = elem.find(f".//{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")
        assert value.get("nullFlavor") == "OTH"
