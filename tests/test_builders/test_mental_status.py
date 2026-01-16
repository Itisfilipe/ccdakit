"""Tests for Mental Status entry builders."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.entries.mental_status import (
    MentalStatusObservation,
    MentalStatusOrganizer,
)
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockPersistentID:
    """Mock persistent ID for testing."""

    def __init__(self, root="2.16.840.1.113883.19", extension="obs-123"):
        self._root = root
        self._extension = extension

    @property
    def root(self):
        return self._root

    @property
    def extension(self):
        return self._extension


class MockMentalStatusObservation:
    """Mock mental status observation for testing."""

    def __init__(
        self,
        category="Cognition",
        category_code="d110",
        category_code_system="ICF",
        value="Alert and oriented",
        value_code="248234008",
        observation_date=date(2023, 10, 15),
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
        category="Cognition",
        category_code="d110",
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

    def test_observation_has_template_id_r21(self):
        """Test MentalStatusObservation includes R2.1 template ID."""
        obs = MockMentalStatusObservation()
        builder = MentalStatusObservation(obs, version=CDAVersion.R2_1)
        elem = builder.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.74"
        assert template.get("extension") == "2015-08-01"

    def test_observation_has_template_id_r20(self):
        """Test MentalStatusObservation includes R2.0 template ID."""
        obs = MockMentalStatusObservation()
        builder = MentalStatusObservation(obs, version=CDAVersion.R2_0)
        elem = builder.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.74"
        assert template.get("extension") == "2015-08-01"

    def test_observation_has_id(self):
        """Test MentalStatusObservation has ID element."""
        obs = MockMentalStatusObservation()
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_observation_has_persistent_id(self):
        """Test MentalStatusObservation with persistent ID."""
        persistent_id = MockPersistentID(
            root="2.16.840.1.113883.19",
            extension="obs-123",
        )
        obs = MockMentalStatusObservation(persistent_id=persistent_id)
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.19"
        assert id_elem.get("extension") == "obs-123"

    def test_observation_has_code_with_translation(self):
        """Test MentalStatusObservation has code with LOINC translation."""
        obs = MockMentalStatusObservation()
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "373930000"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"
        assert code.get("displayName") == "Cognitive function"

        # Check translation
        translation = code.find(f"{{{NS}}}translation")
        assert translation is not None
        assert translation.get("code") == "75275-8"
        assert translation.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert translation.get("displayName") == "Cognitive Function"

    def test_observation_has_status_code(self):
        """Test MentalStatusObservation has statusCode=completed."""
        obs = MockMentalStatusObservation(status="completed")
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_observation_effective_time_date(self):
        """Test MentalStatusObservation effectiveTime with date."""
        obs = MockMentalStatusObservation(observation_date=date(2023, 10, 15))
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None
        assert time_elem.get("value") == "20231015"

    def test_observation_effective_time_datetime(self):
        """Test MentalStatusObservation effectiveTime with datetime."""
        obs = MockMentalStatusObservation(
            observation_date=datetime(2023, 10, 15, 14, 30)
        )
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None
        # Use startswith to accommodate timezone suffix per C-CDA spec CONF:81-10130
        assert time_elem.get("value").startswith("20231015143000")

    def test_observation_value_with_code(self):
        """Test MentalStatusObservation value with SNOMED CT code."""
        obs = MockMentalStatusObservation(
            value="Alert and oriented",
            value_code="248234008",
        )
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        xsi_type = value.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        assert xsi_type == "CD"
        assert value.get("code") == "248234008"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"
        assert value.get("displayName") == "Alert and oriented"

    def test_observation_value_without_code(self):
        """Test MentalStatusObservation value without code."""
        obs = MockMentalStatusObservation(
            value="Confused and disoriented",
            value_code=None,
        )
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("nullFlavor") == "OTH"

        original_text = value.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "Confused and disoriented"

    def test_observation_complete(self):
        """Test MentalStatusObservation with all optional elements."""
        persistent_id = MockPersistentID()
        obs = MockMentalStatusObservation(
            category="Cognition",
            value="Alert and oriented",
            value_code="248234008",
            observation_date=datetime(2023, 10, 15, 14, 30),
            status="completed",
            persistent_id=persistent_id,
        )
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        # Verify all elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}value") is not None

    def test_observation_minimal(self):
        """Test MentalStatusObservation with minimal required elements."""
        obs = MockMentalStatusObservation(
            value="Alert",
            value_code="248234008",
            observation_date=date(2023, 10, 15),
        )
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        # Verify required elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}value") is not None

    def test_observation_to_string(self):
        """Test MentalStatusObservation serialization."""
        obs = MockMentalStatusObservation()
        builder = MentalStatusObservation(obs)
        xml = builder.to_string(pretty=False)

        assert "<observation" in xml or ":observation" in xml
        assert "classCode" in xml
        assert "OBS" in xml
        assert "Alert and oriented" in xml

    def test_observation_element_order(self):
        """Test that elements are in correct order."""
        obs = MockMentalStatusObservation()
        builder = MentalStatusObservation(obs)
        elem = builder.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "id" in names
        assert "code" in names
        assert "statusCode" in names
        assert "effectiveTime" in names
        assert "value" in names


class TestMentalStatusOrganizer:
    """Tests for MentalStatusOrganizer builder."""

    def test_organizer_basic(self):
        """Test basic MentalStatusOrganizer creation."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(observations=[obs])
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        assert local_name(elem) == "organizer"
        assert elem.get("classCode") == "CLUSTER"
        assert elem.get("moodCode") == "EVN"

    def test_organizer_has_template_id_r21(self):
        """Test MentalStatusOrganizer includes R2.1 template ID."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(observations=[obs])
        organizer = MentalStatusOrganizer(organizer_data, version=CDAVersion.R2_1)
        elem = organizer.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.75"
        assert template.get("extension") == "2015-08-01"

    def test_organizer_has_template_id_r20(self):
        """Test MentalStatusOrganizer includes R2.0 template ID."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(observations=[obs])
        organizer = MentalStatusOrganizer(organizer_data, version=CDAVersion.R2_0)
        elem = organizer.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.75"
        assert template.get("extension") == "2015-08-01"

    def test_organizer_has_id(self):
        """Test MentalStatusOrganizer has ID element."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(observations=[obs])
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_organizer_has_persistent_id(self):
        """Test MentalStatusOrganizer with persistent ID."""
        persistent_id = MockPersistentID(
            root="2.16.840.1.113883.19",
            extension="org-456",
        )
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(
            observations=[obs],
            persistent_id=persistent_id,
        )
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.19"
        assert id_elem.get("extension") == "org-456"

    def test_organizer_has_code_icf(self):
        """Test MentalStatusOrganizer code with ICF code system."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(
            category="Cognition",
            category_code="d110",
            category_code_system="ICF",
            observations=[obs],
        )
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "d110"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.254"
        assert code.get("codeSystemName") == "ICF"
        assert code.get("displayName") == "Cognition"

    def test_organizer_has_code_loinc(self):
        """Test MentalStatusOrganizer code with LOINC code system."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(
            category="Mental Status",
            category_code="10190-7",
            category_code_system="LOINC",
            observations=[obs],
        )
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "10190-7"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert code.get("codeSystemName") == "LOINC"

    def test_organizer_has_code_custom_oid(self):
        """Test MentalStatusOrganizer code with custom OID."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(
            category="Custom Mental Status",
            category_code="12345",
            category_code_system="2.16.840.1.113883.6.999",
            observations=[obs],
        )
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "12345"
        # Should use the provided OID as-is
        assert code.get("codeSystem") == "2.16.840.1.113883.6.999"
        assert code.get("displayName") == "Custom Mental Status"

    def test_organizer_has_status_code(self):
        """Test MentalStatusOrganizer has statusCode=completed."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(observations=[obs])
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_organizer_effective_time_with_range(self):
        """Test MentalStatusOrganizer effectiveTime with low and high."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(
            observations=[obs],
            effective_time_low=date(2023, 1, 1),
            effective_time_high=date(2023, 12, 31),
        )
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None

        low = time_elem.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20230101"

        high = time_elem.find(f"{{{NS}}}high")
        assert high is not None
        assert high.get("value") == "20231231"

    def test_organizer_effective_time_with_datetime(self):
        """Test MentalStatusOrganizer effectiveTime with datetime."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(
            observations=[obs],
            effective_time_low=datetime(2023, 1, 1, 8, 0),
            effective_time_high=datetime(2023, 12, 31, 17, 0),
        )
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None

        low = time_elem.find(f"{{{NS}}}low")
        assert low is not None
        # Use startswith to accommodate timezone suffix per C-CDA spec CONF:81-10130
        assert low.get("value").startswith("20230101080000")

        high = time_elem.find(f"{{{NS}}}high")
        assert high is not None
        # Use startswith to accommodate timezone suffix per C-CDA spec CONF:81-10130
        assert high.get("value").startswith("20231231170000")

    def test_organizer_no_effective_time(self):
        """Test MentalStatusOrganizer without effectiveTime."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(
            observations=[obs],
            effective_time_low=None,
            effective_time_high=None,
        )
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is None

    def test_organizer_with_multiple_observations(self):
        """Test MentalStatusOrganizer with multiple observations."""
        obs1 = MockMentalStatusObservation(
            value="Alert and oriented",
            value_code="248234008",
        )
        obs2 = MockMentalStatusObservation(
            value="Depressed mood",
            value_code="366979004",
        )
        organizer_data = MockMentalStatusOrganizer(observations=[obs1, obs2])
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        components = elem.findall(f"{{{NS}}}component")
        assert len(components) == 2

        # Check first component
        obs_elem1 = components[0].find(f"{{{NS}}}observation")
        assert obs_elem1 is not None
        value1 = obs_elem1.find(f"{{{NS}}}value")
        assert value1.get("code") == "248234008"

        # Check second component
        obs_elem2 = components[1].find(f"{{{NS}}}observation")
        assert obs_elem2 is not None
        value2 = obs_elem2.find(f"{{{NS}}}value")
        assert value2.get("code") == "366979004"

    def test_organizer_component_contains_observation(self):
        """Test MentalStatusOrganizer component contains MentalStatusObservation."""
        obs = MockMentalStatusObservation(value="Alert")
        organizer_data = MockMentalStatusOrganizer(observations=[obs])
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        component = elem.find(f"{{{NS}}}component")
        assert component is not None

        observation = component.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"
        assert observation.get("moodCode") == "EVN"

    def test_organizer_complete(self):
        """Test MentalStatusOrganizer with all optional elements."""
        persistent_id = MockPersistentID()
        obs1 = MockMentalStatusObservation(
            value="Alert and oriented",
            value_code="248234008",
        )
        obs2 = MockMentalStatusObservation(
            value="Cooperative",
            value_code="225323000",
        )
        organizer_data = MockMentalStatusOrganizer(
            category="Cognition",
            category_code="d110",
            category_code_system="ICF",
            observations=[obs1, obs2],
            effective_time_low=date(2023, 1, 1),
            effective_time_high=date(2023, 12, 31),
            persistent_id=persistent_id,
        )
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        # Verify all elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None

        # Verify components
        components = elem.findall(f"{{{NS}}}component")
        assert len(components) == 2

    def test_organizer_minimal(self):
        """Test MentalStatusOrganizer with minimal required elements."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(
            category="Cognition",
            category_code="d110",
            category_code_system="ICF",
            observations=[obs],
        )
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        # Verify required elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert len(elem.findall(f"{{{NS}}}component")) == 1

        # Verify optional effectiveTime is absent
        assert elem.find(f"{{{NS}}}effectiveTime") is None

    def test_organizer_to_string(self):
        """Test MentalStatusOrganizer serialization."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(observations=[obs])
        organizer = MentalStatusOrganizer(organizer_data)
        xml = organizer.to_string(pretty=False)

        assert "<organizer" in xml or ":organizer" in xml
        assert "classCode" in xml
        assert "CLUSTER" in xml

    def test_organizer_element_order(self):
        """Test that elements are in correct order."""
        obs = MockMentalStatusObservation()
        organizer_data = MockMentalStatusOrganizer(
            observations=[obs],
            effective_time_low=date(2023, 1, 1),
        )
        organizer = MentalStatusOrganizer(organizer_data)
        elem = organizer.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "id" in names
        assert "code" in names
        assert "statusCode" in names
        assert "effectiveTime" in names
        assert "component" in names
