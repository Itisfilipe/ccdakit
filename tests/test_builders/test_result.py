"""Tests for Result entry builders."""

from datetime import date, datetime
from typing import Sequence

from lxml import etree

from ccdakit.builders.entries.result import ResultObservation, ResultOrganizer
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockResult:
    """Mock result observation for testing."""

    def __init__(
        self,
        test_name="Glucose",
        test_code="2345-7",
        value="95",
        unit="mg/dL",
        status="completed",
        effective_time=date(2023, 10, 1),
        value_type=None,
        interpretation=None,
        reference_range_low=None,
        reference_range_high=None,
        reference_range_unit=None,
    ):
        self._test_name = test_name
        self._test_code = test_code
        self._value = value
        self._unit = unit
        self._status = status
        self._effective_time = effective_time
        self._value_type = value_type
        self._interpretation = interpretation
        self._reference_range_low = reference_range_low
        self._reference_range_high = reference_range_high
        self._reference_range_unit = reference_range_unit

    @property
    def test_name(self):
        return self._test_name

    @property
    def test_code(self):
        return self._test_code

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit

    @property
    def status(self):
        return self._status

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def value_type(self):
        return self._value_type

    @property
    def interpretation(self):
        return self._interpretation

    @property
    def reference_range_low(self):
        return self._reference_range_low

    @property
    def reference_range_high(self):
        return self._reference_range_high

    @property
    def reference_range_unit(self):
        return self._reference_range_unit


class MockResultOrganizer:
    """Mock result organizer for testing."""

    def __init__(
        self,
        panel_name="Complete Blood Count",
        panel_code="58410-2",
        status="completed",
        effective_time=datetime(2023, 10, 1, 10, 30),
        results=None,
    ):
        self._panel_name = panel_name
        self._panel_code = panel_code
        self._status = status
        self._effective_time = effective_time
        self._results = results or []

    @property
    def panel_name(self) -> str:
        return self._panel_name

    @property
    def panel_code(self) -> str:
        return self._panel_code

    @property
    def status(self) -> str:
        return self._status

    @property
    def effective_time(self) -> datetime:
        return self._effective_time

    @property
    def results(self) -> Sequence[MockResult]:
        return self._results


class TestResultObservation:
    """Tests for ResultObservation builder."""

    def test_result_observation_basic(self):
        """Test basic ResultObservation creation."""
        result = MockResult()
        obs = ResultObservation(result)
        elem = obs.to_element()

        assert local_name(elem) == "observation"
        assert elem.get("classCode") == "OBS"
        assert elem.get("moodCode") == "EVN"

    def test_result_observation_has_template_id_r21(self):
        """Test ResultObservation includes R2.1 template ID."""
        result = MockResult()
        obs = ResultObservation(result, version=CDAVersion.R2_1)
        elem = obs.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.2"
        assert template.get("extension") == "2023-05-01"

    def test_result_observation_has_template_id_r20(self):
        """Test ResultObservation includes R2.0 template ID."""
        result = MockResult()
        obs = ResultObservation(result, version=CDAVersion.R2_0)
        elem = obs.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.2"
        assert template.get("extension") == "2023-05-01"

    def test_result_observation_has_id(self):
        """Test ResultObservation has ID element."""
        result = MockResult()
        obs = ResultObservation(result)
        elem = obs.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None

    def test_result_observation_has_code(self):
        """Test ResultObservation has code element with LOINC."""
        result = MockResult(test_code="2345-7", test_name="Glucose")
        obs = ResultObservation(result)
        elem = obs.to_element()

        code_elem = elem.find(f"{{{NS}}}code")
        assert code_elem is not None
        assert code_elem.get("code") == "2345-7"
        assert code_elem.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert code_elem.get("displayName") == "Glucose"

    def test_result_observation_has_status_code(self):
        """Test ResultObservation has statusCode element."""
        result = MockResult(status="completed")
        obs = ResultObservation(result)
        elem = obs.to_element()

        status_elem = elem.find(f"{{{NS}}}statusCode")
        assert status_elem is not None
        assert status_elem.get("code") == "completed"

    def test_result_observation_status_mapping(self):
        """Test ResultObservation maps different statuses correctly."""
        test_cases = [
            ("completed", "completed"),
            ("final", "completed"),
            ("preliminary", "active"),
            ("active", "active"),
            ("cancelled", "cancelled"),
        ]

        for input_status, expected_status in test_cases:
            result = MockResult(status=input_status)
            obs = ResultObservation(result)
            elem = obs.to_element()

            status_elem = elem.find(f"{{{NS}}}statusCode")
            assert status_elem.get("code") == expected_status

    def test_result_observation_has_effective_time(self):
        """Test ResultObservation has effectiveTime element."""
        test_date = date(2023, 10, 15)
        result = MockResult(effective_time=test_date)
        obs = ResultObservation(result)
        elem = obs.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None
        assert time_elem.get("value") == "20231015"

    def test_result_observation_pq_value(self):
        """Test ResultObservation with PQ (physical quantity) value."""
        result = MockResult(value="95", unit="mg/dL")
        obs = ResultObservation(result)
        elem = obs.to_element()

        value_elem = elem.find(f"{{{NS}}}value")
        assert value_elem is not None
        xsi_type = value_elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        assert xsi_type == "PQ"
        assert value_elem.get("value") == "95"
        assert value_elem.get("unit") == "mg/dL"

    def test_result_observation_st_value(self):
        """Test ResultObservation with ST (string) value."""
        result = MockResult(value="Positive", unit=None, value_type="ST")
        obs = ResultObservation(result)
        elem = obs.to_element()

        value_elem = elem.find(f"{{{NS}}}value")
        assert value_elem is not None
        xsi_type = value_elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        assert xsi_type == "ST"
        assert value_elem.text == "Positive"

    def test_result_observation_cd_value(self):
        """Test ResultObservation with CD (coded) value."""
        result = MockResult(value="260385009", unit=None, value_type="CD", test_name="Glucose")
        obs = ResultObservation(result)
        elem = obs.to_element()

        value_elem = elem.find(f"{{{NS}}}value")
        assert value_elem is not None
        xsi_type = value_elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        assert xsi_type == "CD"
        assert value_elem.get("code") == "260385009"
        assert value_elem.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT

    def test_result_observation_interpretation_normal(self):
        """Test ResultObservation with normal interpretation."""
        result = MockResult(interpretation="Normal")
        obs = ResultObservation(result)
        elem = obs.to_element()

        interp_elem = elem.find(f"{{{NS}}}interpretationCode")
        assert interp_elem is not None
        assert interp_elem.get("code") == "N"
        assert interp_elem.get("codeSystem") == "2.16.840.1.113883.5.83"

    def test_result_observation_interpretation_high(self):
        """Test ResultObservation with high interpretation."""
        result = MockResult(interpretation="High")
        obs = ResultObservation(result)
        elem = obs.to_element()

        interp_elem = elem.find(f"{{{NS}}}interpretationCode")
        assert interp_elem is not None
        assert interp_elem.get("code") == "H"

    def test_result_observation_interpretation_low(self):
        """Test ResultObservation with low interpretation."""
        result = MockResult(interpretation="Low")
        obs = ResultObservation(result)
        elem = obs.to_element()

        interp_elem = elem.find(f"{{{NS}}}interpretationCode")
        assert interp_elem is not None
        assert interp_elem.get("code") == "L"

    def test_result_observation_interpretation_code_direct(self):
        """Test ResultObservation with direct code like 'H' or 'L'."""
        result = MockResult(interpretation="H")
        obs = ResultObservation(result)
        elem = obs.to_element()

        interp_elem = elem.find(f"{{{NS}}}interpretationCode")
        assert interp_elem is not None
        assert interp_elem.get("code") == "H"

    def test_result_observation_no_interpretation(self):
        """Test ResultObservation without interpretation."""
        result = MockResult(interpretation=None)
        obs = ResultObservation(result)
        elem = obs.to_element()

        interp_elem = elem.find(f"{{{NS}}}interpretationCode")
        assert interp_elem is None

    def test_result_observation_reference_range(self):
        """Test ResultObservation with reference range."""
        result = MockResult(
            reference_range_low="70",
            reference_range_high="100",
            reference_range_unit="mg/dL",
        )
        obs = ResultObservation(result)
        elem = obs.to_element()

        ref_range = elem.find(f"{{{NS}}}referenceRange")
        assert ref_range is not None

        obs_range = ref_range.find(f"{{{NS}}}observationRange")
        assert obs_range is not None

        value_elem = obs_range.find(f"{{{NS}}}value")
        assert value_elem is not None
        xsi_type = value_elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        assert xsi_type == "IVL_PQ"

        low_elem = value_elem.find(f"{{{NS}}}low")
        assert low_elem is not None
        assert low_elem.get("value") == "70"
        assert low_elem.get("unit") == "mg/dL"

        high_elem = value_elem.find(f"{{{NS}}}high")
        assert high_elem is not None
        assert high_elem.get("value") == "100"
        assert high_elem.get("unit") == "mg/dL"

    def test_result_observation_reference_range_low_only(self):
        """Test ResultObservation with only low reference range."""
        result = MockResult(
            reference_range_low="70",
            reference_range_high=None,
            reference_range_unit="mg/dL",
        )
        obs = ResultObservation(result)
        elem = obs.to_element()

        ref_range = elem.find(f"{{{NS}}}referenceRange")
        assert ref_range is not None

        value_elem = ref_range.find(f".//{{{NS}}}value")
        low_elem = value_elem.find(f"{{{NS}}}low")
        assert low_elem is not None
        assert low_elem.get("value") == "70"

        high_elem = value_elem.find(f"{{{NS}}}high")
        assert high_elem is None

    def test_result_observation_reference_range_high_only(self):
        """Test ResultObservation with only high reference range."""
        result = MockResult(
            reference_range_low=None,
            reference_range_high="100",
            reference_range_unit="mg/dL",
        )
        obs = ResultObservation(result)
        elem = obs.to_element()

        ref_range = elem.find(f"{{{NS}}}referenceRange")
        assert ref_range is not None

        value_elem = ref_range.find(f".//{{{NS}}}value")
        high_elem = value_elem.find(f"{{{NS}}}high")
        assert high_elem is not None
        assert high_elem.get("value") == "100"

        low_elem = value_elem.find(f"{{{NS}}}low")
        assert low_elem is None

    def test_result_observation_no_reference_range(self):
        """Test ResultObservation without reference range."""
        result = MockResult(
            reference_range_low=None,
            reference_range_high=None,
        )
        obs = ResultObservation(result)
        elem = obs.to_element()

        ref_range = elem.find(f"{{{NS}}}referenceRange")
        assert ref_range is None

    def test_result_observation_complete(self):
        """Test ResultObservation with all optional elements."""
        result = MockResult(
            test_name="Glucose",
            test_code="2345-7",
            value="95",
            unit="mg/dL",
            status="completed",
            effective_time=date(2023, 10, 15),
            interpretation="Normal",
            reference_range_low="70",
            reference_range_high="100",
            reference_range_unit="mg/dL",
        )
        obs = ResultObservation(result)
        elem = obs.to_element()

        # Verify all elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}value") is not None
        assert elem.find(f"{{{NS}}}interpretationCode") is not None
        assert elem.find(f"{{{NS}}}referenceRange") is not None

    def test_result_observation_minimal(self):
        """Test ResultObservation with minimal required elements."""
        result = MockResult(
            interpretation=None,
            reference_range_low=None,
            reference_range_high=None,
        )
        obs = ResultObservation(result)
        elem = obs.to_element()

        # Verify required elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}value") is not None

        # Verify optional elements are absent
        assert elem.find(f"{{{NS}}}interpretationCode") is None
        assert elem.find(f"{{{NS}}}referenceRange") is None


class TestResultOrganizer:
    """Tests for ResultOrganizer builder."""

    def test_result_organizer_basic(self):
        """Test basic ResultOrganizer creation."""
        organizer = MockResultOrganizer()
        org = ResultOrganizer(organizer)
        elem = org.to_element()

        assert local_name(elem) == "organizer"
        assert elem.get("classCode") == "CLUSTER"
        assert elem.get("moodCode") == "EVN"

    def test_result_organizer_has_template_id_r21(self):
        """Test ResultOrganizer includes R2.1 template ID."""
        organizer = MockResultOrganizer()
        org = ResultOrganizer(organizer, version=CDAVersion.R2_1)
        elem = org.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.1"
        assert template.get("extension") == "2023-05-01"

    def test_result_organizer_has_template_id_r20(self):
        """Test ResultOrganizer includes R2.0 template ID."""
        organizer = MockResultOrganizer()
        org = ResultOrganizer(organizer, version=CDAVersion.R2_0)
        elem = org.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.1"
        assert template.get("extension") == "2023-05-01"

    def test_result_organizer_has_id(self):
        """Test ResultOrganizer has ID element."""
        organizer = MockResultOrganizer()
        org = ResultOrganizer(organizer)
        elem = org.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None

    def test_result_organizer_has_code(self):
        """Test ResultOrganizer has code element with LOINC."""
        organizer = MockResultOrganizer(panel_code="58410-2", panel_name="Complete Blood Count")
        org = ResultOrganizer(organizer)
        elem = org.to_element()

        code_elem = elem.find(f"{{{NS}}}code")
        assert code_elem is not None
        assert code_elem.get("code") == "58410-2"
        assert code_elem.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert code_elem.get("displayName") == "Complete Blood Count"

    def test_result_organizer_has_status_code(self):
        """Test ResultOrganizer has statusCode element."""
        organizer = MockResultOrganizer(status="completed")
        org = ResultOrganizer(organizer)
        elem = org.to_element()

        status_elem = elem.find(f"{{{NS}}}statusCode")
        assert status_elem is not None
        assert status_elem.get("code") == "completed"

    def test_result_organizer_status_mapping(self):
        """Test ResultOrganizer maps different statuses correctly."""
        test_cases = [
            ("completed", "completed"),
            ("final", "completed"),
            ("preliminary", "active"),
        ]

        for input_status, expected_status in test_cases:
            organizer = MockResultOrganizer(status=input_status)
            org = ResultOrganizer(organizer)
            elem = org.to_element()

            status_elem = elem.find(f"{{{NS}}}statusCode")
            assert status_elem.get("code") == expected_status

    def test_result_organizer_has_effective_time(self):
        """Test ResultOrganizer has effectiveTime element."""
        test_datetime = datetime(2023, 10, 15, 14, 30)
        organizer = MockResultOrganizer(effective_time=test_datetime)
        org = ResultOrganizer(organizer)
        elem = org.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None
        # Datetime values include timezone per C-CDA spec CONF:81-10130
        assert time_elem.get("value").startswith("20231015143000")

    def test_result_organizer_with_results(self):
        """Test ResultOrganizer with multiple result observations."""
        results = [
            MockResult(test_name="Glucose", test_code="2345-7", value="95", unit="mg/dL"),
            MockResult(test_name="Hemoglobin", test_code="718-7", value="14.5", unit="g/dL"),
        ]
        organizer = MockResultOrganizer(results=results)
        org = ResultOrganizer(organizer)
        elem = org.to_element()

        components = elem.findall(f"{{{NS}}}component")
        assert len(components) == 2

        # Check first component
        obs1 = components[0].find(f"{{{NS}}}observation")
        assert obs1 is not None
        code1 = obs1.find(f"{{{NS}}}code")
        assert code1.get("code") == "2345-7"

        # Check second component
        obs2 = components[1].find(f"{{{NS}}}observation")
        assert obs2 is not None
        code2 = obs2.find(f"{{{NS}}}code")
        assert code2.get("code") == "718-7"

    def test_result_organizer_empty_results(self):
        """Test ResultOrganizer with no results."""
        organizer = MockResultOrganizer(results=[])
        org = ResultOrganizer(organizer)
        elem = org.to_element()

        components = elem.findall(f"{{{NS}}}component")
        assert len(components) == 0

    def test_result_organizer_complete(self):
        """Test ResultOrganizer with all elements."""
        results = [
            MockResult(
                test_name="Glucose",
                test_code="2345-7",
                value="95",
                unit="mg/dL",
                interpretation="Normal",
                reference_range_low="70",
                reference_range_high="100",
                reference_range_unit="mg/dL",
            ),
        ]
        organizer = MockResultOrganizer(
            panel_name="Metabolic Panel",
            panel_code="24323-8",
            status="completed",
            effective_time=datetime(2023, 10, 15, 14, 30),
            results=results,
        )
        org = ResultOrganizer(organizer)
        elem = org.to_element()

        # Verify organizer structure
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None

        # Verify component
        component = elem.find(f"{{{NS}}}component")
        assert component is not None

        # Verify nested observation
        obs = component.find(f"{{{NS}}}observation")
        assert obs is not None
        assert obs.find(f"{{{NS}}}referenceRange") is not None
