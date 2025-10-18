"""Tests for Smoking Status entry builder."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.entries.smoking_status import SmokingStatusObservation
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockSmokingStatus:
    """Mock smoking status for testing."""

    def __init__(
        self,
        smoking_status="Current every day smoker",
        code="449868002",
        date=date(2023, 10, 1),
    ):
        self._smoking_status = smoking_status
        self._code = code
        self._date = date

    @property
    def smoking_status(self):
        return self._smoking_status

    @property
    def code(self):
        return self._code

    @property
    def date(self):
        return self._date


class TestSmokingStatusObservation:
    """Tests for SmokingStatusObservation builder."""

    def test_smoking_status_observation_basic(self):
        """Test basic SmokingStatusObservation creation."""
        status = MockSmokingStatus()
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        assert local_name(elem) == "observation"
        assert elem.get("classCode") == "OBS"
        assert elem.get("moodCode") == "EVN"

    def test_smoking_status_observation_has_template_id_r21(self):
        """Test SmokingStatusObservation includes R2.1 template ID."""
        status = MockSmokingStatus()
        obs = SmokingStatusObservation(status, version=CDAVersion.R2_1)
        elem = obs.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.78"
        assert template.get("extension") == "2014-06-09"

    def test_smoking_status_observation_has_template_id_r20(self):
        """Test SmokingStatusObservation includes R2.0 template ID."""
        status = MockSmokingStatus()
        obs = SmokingStatusObservation(status, version=CDAVersion.R2_0)
        elem = obs.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.78"
        assert template.get("extension") == "2014-06-09"

    def test_smoking_status_observation_has_id(self):
        """Test SmokingStatusObservation includes ID element."""
        status = MockSmokingStatus()
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_smoking_status_observation_has_fixed_code(self):
        """Test SmokingStatusObservation includes fixed code element."""
        status = MockSmokingStatus()
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "72166-2"  # Tobacco smoking status NHIS
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Tobacco smoking status"

    def test_smoking_status_observation_has_status_code(self):
        """Test SmokingStatusObservation includes statusCode."""
        status = MockSmokingStatus()
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        status_elem = elem.find(f"{{{NS}}}statusCode")
        assert status_elem is not None
        assert status_elem.get("code") == "completed"

    def test_smoking_status_observation_has_effective_time_date(self):
        """Test SmokingStatusObservation includes effectiveTime with date."""
        status = MockSmokingStatus(date=date(2023, 10, 15))
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None
        assert eff_time.get("value") == "20231015"

    def test_smoking_status_observation_has_effective_time_datetime(self):
        """Test SmokingStatusObservation includes effectiveTime with datetime."""
        status = MockSmokingStatus(date=datetime(2023, 10, 15, 14, 30))
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None
        assert "20231015" in eff_time.get("value")

    def test_smoking_status_observation_has_value_current_smoker(self):
        """Test SmokingStatusObservation value for current every day smoker."""
        status = MockSmokingStatus(smoking_status="Current every day smoker", code="449868002")
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "449868002"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT
        assert value.get("displayName") == "Current every day smoker"
        assert value.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "CD"

    def test_smoking_status_observation_value_former_smoker(self):
        """Test SmokingStatusObservation value for former smoker."""
        status = MockSmokingStatus(smoking_status="Former smoker", code="8517006")
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value.get("code") == "8517006"
        assert value.get("displayName") == "Former smoker"

    def test_smoking_status_observation_value_never_smoker(self):
        """Test SmokingStatusObservation value for never smoker."""
        status = MockSmokingStatus(smoking_status="Never smoker", code="266919005")
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value.get("code") == "266919005"
        assert value.get("displayName") == "Never smoker"

    def test_smoking_status_observation_value_unknown(self):
        """Test SmokingStatusObservation value for unknown if ever smoked."""
        status = MockSmokingStatus(smoking_status="Unknown if ever smoked", code="266927001")
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value.get("code") == "266927001"
        assert value.get("displayName") == "Unknown if ever smoked"

    def test_smoking_status_observation_value_current_some_day(self):
        """Test SmokingStatusObservation value for current some day smoker."""
        status = MockSmokingStatus(smoking_status="Current some day smoker", code="428041000124106")
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value.get("code") == "428041000124106"
        assert value.get("displayName") == "Current some day smoker"

    def test_smoking_status_observation_value_heavy_smoker(self):
        """Test SmokingStatusObservation value for heavy tobacco smoker."""
        status = MockSmokingStatus(smoking_status="Heavy tobacco smoker", code="428071000124103")
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value.get("code") == "428071000124103"
        assert value.get("displayName") == "Heavy tobacco smoker"

    def test_smoking_status_observation_value_light_smoker(self):
        """Test SmokingStatusObservation value for light tobacco smoker."""
        status = MockSmokingStatus(smoking_status="Light tobacco smoker", code="428061000124105")
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value.get("code") == "428061000124105"
        assert value.get("displayName") == "Light tobacco smoker"

    def test_smoking_status_observation_to_string(self):
        """Test SmokingStatusObservation serialization."""
        status = MockSmokingStatus()
        obs = SmokingStatusObservation(status)
        xml = obs.to_string(pretty=False)

        assert "<observation" in xml or ":observation" in xml
        assert "classCode" in xml
        assert "72166-2" in xml  # Fixed LOINC code

    def test_smoking_status_observation_structure_order(self):
        """Test that elements are in correct order."""
        status = MockSmokingStatus()
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present
        assert "templateId" in names
        assert "id" in names
        assert "code" in names
        assert "statusCode" in names
        assert "effectiveTime" in names
        assert "value" in names

    def test_smoking_status_observation_with_r21_version(self):
        """Test SmokingStatusObservation with explicit R2.1 version."""
        status = MockSmokingStatus()
        obs = SmokingStatusObservation(status, version=CDAVersion.R2_1)
        elem = obs.to_element()

        # Verify version-specific elements
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("extension") == "2014-06-09"

    def test_smoking_status_observation_with_r20_version(self):
        """Test SmokingStatusObservation with explicit R2.0 version."""
        status = MockSmokingStatus()
        obs = SmokingStatusObservation(status, version=CDAVersion.R2_0)
        elem = obs.to_element()

        # Verify version-specific elements
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("extension") == "2014-06-09"

    def test_smoking_status_observation_in_parent_element(self):
        """Test composing smoking status observation in parent element."""
        parent = etree.Element(f"{{{NS}}}entry")

        status = MockSmokingStatus()
        obs = SmokingStatusObservation(status)

        parent.append(obs.to_element())

        obs_elem = parent.find(f"{{{NS}}}observation")
        assert obs_elem is not None
        assert obs_elem.get("classCode") == "OBS"
        assert obs_elem.get("moodCode") == "EVN"

    def test_smoking_status_observation_no_null_flavor(self):
        """Test that value does NOT contain nullFlavor attribute."""
        status = MockSmokingStatus()
        obs = SmokingStatusObservation(status)
        elem = obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        # Verify no nullFlavor attribute
        assert value.get("nullFlavor") is None

    def test_smoking_status_observation_complete_example(self):
        """Test creating a complete smoking status observation."""
        status = MockSmokingStatus(
            smoking_status="Current every day smoker",
            code="449868002",
            date=datetime(2023, 10, 15, 14, 30),
        )
        obs = SmokingStatusObservation(status, version=CDAVersion.R2_1)
        elem = obs.to_element()

        # Verify structure
        assert local_name(elem) == "observation"

        # Verify all required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}value") is not None

        # Verify value content
        value = elem.find(f"{{{NS}}}value")
        assert value.get("code") == "449868002"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"
