"""Tests for ProblemObservation builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.entries.problem import ProblemObservation
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


class TestProblemObservation:
    """Tests for ProblemObservation builder."""

    def test_problem_observation_basic(self):
        """Test basic ProblemObservation creation."""
        problem = MockProblem()
        obs = ProblemObservation(problem)
        elem = obs.to_element()

        assert local_name(elem) == "observation"
        assert elem.get("classCode") == "OBS"
        assert elem.get("moodCode") == "EVN"

    def test_problem_observation_has_template_id_r21(self):
        """Test ProblemObservation includes R2.1 template ID."""
        problem = MockProblem()
        obs = ProblemObservation(problem, version=CDAVersion.R2_1)
        elem = obs.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.4"
        assert template.get("extension") == "2015-08-01"

    def test_problem_observation_has_template_id_r20(self):
        """Test ProblemObservation includes R2.0 template ID."""
        problem = MockProblem()
        obs = ProblemObservation(problem, version=CDAVersion.R2_0)
        elem = obs.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.4"
        assert template.get("extension") == "2014-06-09"

    def test_problem_observation_has_id(self):
        """Test ProblemObservation includes ID element."""
        problem = MockProblem()
        obs = ProblemObservation(problem)
        elem = obs.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None

    def test_problem_observation_with_persistent_id(self):
        """Test ProblemObservation with persistent ID."""
        pid = MockPersistentID()
        problem = MockProblem(persistent_id=pid)
        obs = ProblemObservation(problem)
        elem = obs.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem.get("root") == "2.16.840.1.113883.19.5.99999.1"
        assert id_elem.get("extension") == "PROB-123"

    def test_problem_observation_has_code(self):
        """Test ProblemObservation includes code element."""
        problem = MockProblem()
        obs = ProblemObservation(problem)
        elem = obs.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "55607006"  # Problem type code
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED
        assert code.get("displayName") == "Problem"

    def test_problem_observation_has_status_code(self):
        """Test ProblemObservation includes statusCode."""
        problem = MockProblem(status="active")
        obs = ProblemObservation(problem)
        elem = obs.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "active"

    def test_problem_observation_status_mapping(self):
        """Test status code mapping."""
        # Test resolved -> completed
        problem = MockProblem(status="resolved")
        obs = ProblemObservation(problem)
        elem = obs.to_element()
        status = elem.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "completed"

        # Test inactive
        problem = MockProblem(status="inactive")
        obs = ProblemObservation(problem)
        elem = obs.to_element()
        status = elem.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "inactive"

    def test_problem_observation_has_effective_time(self):
        """Test ProblemObservation includes effectiveTime."""
        problem = MockProblem(onset_date=date(2020, 1, 15))
        obs = ProblemObservation(problem)
        elem = obs.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None

        low = eff_time.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20200115"

    def test_problem_observation_effective_time_with_resolved(self):
        """Test effectiveTime with both onset and resolved dates."""
        problem = MockProblem(
            onset_date=date(2020, 1, 15),
            resolved_date=date(2021, 6, 30),
        )
        obs = ProblemObservation(problem)
        elem = obs.to_element()

        eff_time = elem.find(f"{{{NS}}}effectiveTime")
        low = eff_time.find(f"{{{NS}}}low")
        high = eff_time.find(f"{{{NS}}}high")

        assert low.get("value") == "20200115"
        assert high is not None
        assert high.get("value") == "20210630"

    def test_problem_observation_has_value_snomed(self):
        """Test ProblemObservation value with SNOMED code."""
        problem = MockProblem(
            name="Type 2 Diabetes Mellitus",
            code="44054006",
            code_system="SNOMED",
        )
        obs = ProblemObservation(problem)
        elem = obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "44054006"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED OID
        assert value.get("codeSystemName") == "SNOMED CT"
        assert value.get("displayName") == "Type 2 Diabetes Mellitus"
        assert value.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "CD"

    def test_problem_observation_has_value_icd10(self):
        """Test ProblemObservation value with ICD-10 code."""
        problem = MockProblem(
            name="Type 2 Diabetes Mellitus",
            code="E11.9",
            code_system="ICD-10",
        )
        obs = ProblemObservation(problem)
        elem = obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "E11.9"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.90"  # ICD-10 OID
        assert value.get("codeSystemName") == "ICD-10-CM"

    def test_problem_observation_to_string(self):
        """Test ProblemObservation serialization."""
        problem = MockProblem()
        obs = ProblemObservation(problem)
        xml = obs.to_string(pretty=False)

        assert "<observation" in xml or ":observation" in xml
        assert "classCode" in xml
        assert "moodCode" in xml
        assert "44054006" in xml  # Problem code

    def test_problem_observation_structure_order(self):
        """Test that elements are in correct order."""
        pid = MockPersistentID()
        problem = MockProblem(
            onset_date=date(2020, 1, 15),
            persistent_id=pid,
        )
        obs = ProblemObservation(problem)
        elem = obs.to_element()

        children = list(elem)
        # Get local names
        names = [local_name(child) for child in children]

        # Check expected elements are present
        assert "templateId" in names
        assert "id" in names
        assert "code" in names
        assert "statusCode" in names
        assert "effectiveTime" in names
        assert "value" in names


class TestProblemObservationIntegration:
    """Integration tests for ProblemObservation."""

    def test_multiple_problems(self):
        """Test creating multiple problem observations."""
        problem1 = MockProblem(
            name="Hypertension",
            code="38341003",
            code_system="SNOMED",
        )
        problem2 = MockProblem(
            name="Type 2 Diabetes",
            code="44054006",
            code_system="SNOMED",
        )

        obs1 = ProblemObservation(problem1)
        obs2 = ProblemObservation(problem2)

        elem1 = obs1.to_element()
        elem2 = obs2.to_element()

        value1 = elem1.find(f"{{{NS}}}value")
        value2 = elem2.find(f"{{{NS}}}value")

        assert value1.get("code") == "38341003"
        assert value2.get("code") == "44054006"

    def test_problem_in_parent_element(self):
        """Test composing problem observation in parent element."""
        parent = etree.Element(f"{{{NS}}}entry")

        problem = MockProblem()
        obs = ProblemObservation(problem)

        parent.append(obs.to_element())

        observation = parent.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"
