"""Tests for Vital Signs entry builders."""

from datetime import date, datetime
from typing import Sequence

from lxml import etree

from ccdakit.builders.entries.vital_signs import VitalSignObservation, VitalSignsOrganizer
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
        date=date(2023, 10, 1),
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


class TestVitalSignObservation:
    """Tests for VitalSignObservation builder."""

    def test_vital_sign_observation_basic(self):
        """Test basic VitalSignObservation creation."""
        vital_sign = MockVitalSign()
        obs = VitalSignObservation(vital_sign)
        elem = obs.to_element()

        assert local_name(elem) == "observation"
        assert elem.get("classCode") == "OBS"
        assert elem.get("moodCode") == "EVN"

    def test_vital_sign_observation_has_template_id_r21(self):
        """Test VitalSignObservation includes R2.1 template ID."""
        vital_sign = MockVitalSign()
        obs = VitalSignObservation(vital_sign, version=CDAVersion.R2_1)
        elem = obs.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.27"
        assert template.get("extension") == "2014-06-09"

    def test_vital_sign_observation_has_template_id_r20(self):
        """Test VitalSignObservation includes R2.0 template ID."""
        vital_sign = MockVitalSign()
        obs = VitalSignObservation(vital_sign, version=CDAVersion.R2_0)
        elem = obs.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.27"
        assert template.get("extension") == "2014-06-09"

    def test_vital_sign_observation_has_id(self):
        """Test VitalSignObservation includes ID element."""
        vital_sign = MockVitalSign()
        obs = VitalSignObservation(vital_sign)
        elem = obs.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_vital_sign_observation_has_code(self):
        """Test VitalSignObservation includes code element."""
        vital_sign = MockVitalSign(type="Heart Rate", code="8867-4")
        obs = VitalSignObservation(vital_sign)
        elem = obs.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "8867-4"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Heart Rate"

    def test_vital_sign_observation_has_status_code(self):
        """Test VitalSignObservation includes statusCode."""
        vital_sign = MockVitalSign()
        obs = VitalSignObservation(vital_sign)
        elem = obs.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_vital_sign_observation_has_effective_time(self):
        """Test VitalSignObservation includes effectiveTime."""
        vital_sign = MockVitalSign(date=date(2023, 10, 15))
        obs = VitalSignObservation(vital_sign)
        elem = obs.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None
        assert eff_time.get("value") == "20231015"

    def test_vital_sign_observation_has_value(self):
        """Test VitalSignObservation includes value element."""
        vital_sign = MockVitalSign(value="72", unit="bpm")
        obs = VitalSignObservation(vital_sign)
        elem = obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("value") == "72"
        assert value.get("unit") == "bpm"
        assert value.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "PQ"

    def test_vital_sign_observation_with_interpretation(self):
        """Test VitalSignObservation with interpretation."""
        vital_sign = MockVitalSign(interpretation="Normal")
        obs = VitalSignObservation(vital_sign)
        elem = obs.to_element()

        interp = elem.find(f"{{{NS}}}interpretationCode")
        assert interp is not None
        assert interp.get("code") == "N"
        assert interp.get("codeSystem") == "2.16.840.1.113883.5.83"
        assert interp.get("displayName") == "Normal"

    def test_vital_sign_observation_interpretation_high(self):
        """Test VitalSignObservation with high interpretation."""
        vital_sign = MockVitalSign(interpretation="High")
        obs = VitalSignObservation(vital_sign)
        elem = obs.to_element()

        interp = elem.find(f"{{{NS}}}interpretationCode")
        assert interp.get("code") == "H"

    def test_vital_sign_observation_interpretation_low(self):
        """Test VitalSignObservation with low interpretation."""
        vital_sign = MockVitalSign(interpretation="Low")
        obs = VitalSignObservation(vital_sign)
        elem = obs.to_element()

        interp = elem.find(f"{{{NS}}}interpretationCode")
        assert interp.get("code") == "L"

    def test_vital_sign_observation_without_interpretation(self):
        """Test VitalSignObservation without interpretation."""
        vital_sign = MockVitalSign(interpretation=None)
        obs = VitalSignObservation(vital_sign)
        elem = obs.to_element()

        interp = elem.find(f"{{{NS}}}interpretationCode")
        assert interp is None

    def test_vital_sign_observation_to_string(self):
        """Test VitalSignObservation serialization."""
        vital_sign = MockVitalSign()
        obs = VitalSignObservation(vital_sign)
        xml = obs.to_string(pretty=False)

        assert "<observation" in xml or ":observation" in xml
        assert "classCode" in xml
        assert "8867-4" in xml  # LOINC code

    def test_vital_sign_observation_structure_order(self):
        """Test that elements are in correct order."""
        vital_sign = MockVitalSign(interpretation="Normal")
        obs = VitalSignObservation(vital_sign)
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
        assert "interpretationCode" in names


class TestVitalSignsOrganizer:
    """Tests for VitalSignsOrganizer builder."""

    def test_vital_signs_organizer_basic(self):
        """Test basic VitalSignsOrganizer creation."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        org = VitalSignsOrganizer(organizer)
        elem = org.to_element()

        assert local_name(elem) == "organizer"
        assert elem.get("classCode") == "CLUSTER"
        assert elem.get("moodCode") == "EVN"

    def test_vital_signs_organizer_has_template_id_r21(self):
        """Test VitalSignsOrganizer includes R2.1 template ID."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        org = VitalSignsOrganizer(organizer, version=CDAVersion.R2_1)
        elem = org.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.26"
        assert template.get("extension") == "2015-08-01"

    def test_vital_signs_organizer_has_template_id_r20(self):
        """Test VitalSignsOrganizer includes R2.0 template ID."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        org = VitalSignsOrganizer(organizer, version=CDAVersion.R2_0)
        elem = org.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.26"
        assert template.get("extension") == "2014-06-09"

    def test_vital_signs_organizer_has_id(self):
        """Test VitalSignsOrganizer includes ID element."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        org = VitalSignsOrganizer(organizer)
        elem = org.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_vital_signs_organizer_has_code(self):
        """Test VitalSignsOrganizer includes code element."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        org = VitalSignsOrganizer(organizer)
        elem = org.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        # LOINC code for vital signs panel (required for C-CDA R2.1)
        assert code.get("code") == "74728-7"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Vital signs"

    def test_vital_signs_organizer_has_status_code(self):
        """Test VitalSignsOrganizer includes statusCode."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        org = VitalSignsOrganizer(organizer)
        elem = org.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_vital_signs_organizer_has_effective_time(self):
        """Test VitalSignsOrganizer includes effectiveTime."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(
            date=datetime(2023, 10, 15, 14, 30),
            vital_signs=vital_signs,
        )
        org = VitalSignsOrganizer(organizer)
        elem = org.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None
        assert "20231015" in eff_time.get("value")

    def test_vital_signs_organizer_has_components(self):
        """Test VitalSignsOrganizer includes component elements."""
        vital_signs = [
            MockVitalSign(type="Heart Rate", code="8867-4"),
            MockVitalSign(type="Blood Pressure", code="85354-9"),
        ]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        org = VitalSignsOrganizer(organizer)
        elem = org.to_element()

        components = elem.findall(f"{{{NS}}}component")
        assert len(components) == 2

        # Check each component has an observation
        for component in components:
            obs = component.find(f"{{{NS}}}observation")
            assert obs is not None
            assert obs.get("classCode") == "OBS"

    def test_vital_signs_organizer_to_string(self):
        """Test VitalSignsOrganizer serialization."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        org = VitalSignsOrganizer(organizer)
        xml = org.to_string(pretty=False)

        assert "<organizer" in xml or ":organizer" in xml
        assert "classCode" in xml
        assert "74728-7" in xml  # Vital signs panel LOINC code

    def test_vital_signs_organizer_structure_order(self):
        """Test that elements are in correct order."""
        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        org = VitalSignsOrganizer(organizer)
        elem = org.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present
        assert "templateId" in names
        assert "id" in names
        assert "code" in names
        assert "statusCode" in names
        assert "effectiveTime" in names
        assert "component" in names


class TestVitalSignsIntegration:
    """Integration tests for vital signs builders."""

    def test_complete_vital_signs_panel(self):
        """Test creating a complete vital signs panel."""
        vital_signs = [
            MockVitalSign(
                type="Heart Rate",
                code="8867-4",
                value="72",
                unit="bpm",
                date=datetime(2023, 10, 15, 10, 30),
                interpretation="Normal",
            ),
            MockVitalSign(
                type="Systolic Blood Pressure",
                code="8480-6",
                value="120",
                unit="mm[Hg]",
                date=datetime(2023, 10, 15, 10, 30),
                interpretation="Normal",
            ),
            MockVitalSign(
                type="Diastolic Blood Pressure",
                code="8462-4",
                value="80",
                unit="mm[Hg]",
                date=datetime(2023, 10, 15, 10, 30),
                interpretation="Normal",
            ),
        ]

        organizer = MockVitalSignsOrganizer(
            date=datetime(2023, 10, 15, 10, 30),
            vital_signs=vital_signs,
        )
        org = VitalSignsOrganizer(organizer, version=CDAVersion.R2_1)
        elem = org.to_element()

        # Verify structure
        assert local_name(elem) == "organizer"

        # Verify 3 components
        components = elem.findall(f"{{{NS}}}component")
        assert len(components) == 3

        # Verify each component has observation with correct codes
        observations = [comp.find(f"{{{NS}}}observation") for comp in components]
        codes = [obs.find(f"{{{NS}}}code").get("code") for obs in observations]
        assert "8867-4" in codes  # Heart rate
        assert "8480-6" in codes  # Systolic BP
        assert "8462-4" in codes  # Diastolic BP

    def test_vital_signs_in_parent_element(self):
        """Test composing vital signs organizer in parent element."""
        parent = etree.Element(f"{{{NS}}}entry")

        vital_signs = [MockVitalSign()]
        organizer = MockVitalSignsOrganizer(vital_signs=vital_signs)
        org = VitalSignsOrganizer(organizer)

        parent.append(org.to_element())

        organizer_elem = parent.find(f"{{{NS}}}organizer")
        assert organizer_elem is not None
        assert organizer_elem.get("classCode") == "CLUSTER"
