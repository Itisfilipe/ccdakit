"""Tests for HealthConcernsSection builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.health_concerns import HealthConcernsSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockObservation:
    """Mock observation for testing."""

    def __init__(
        self,
        observation_type="problem",
        code="233604007",
        code_system="SNOMED CT",
        display_name="Pneumonia",
    ):
        self._observation_type = observation_type
        self._code = code
        self._code_system = code_system
        self._display_name = display_name

    @property
    def observation_type(self):
        return self._observation_type

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def display_name(self):
        return self._display_name


class MockPersistentID:
    """Mock persistent ID for testing."""

    def __init__(self, root="2.16.840.1.113883.19", extension="concern-123"):
        self._root = root
        self._extension = extension

    @property
    def root(self):
        return self._root

    @property
    def extension(self):
        return self._extension


class MockHealthConcern:
    """Mock health concern for testing."""

    def __init__(
        self,
        name="Risk of Hyperkalemia",
        status="active",
        effective_time_low=date(2023, 1, 15),
        effective_time_high=None,
        persistent_id=None,
        observations=None,
        author_is_patient=False,
    ):
        self._name = name
        self._status = status
        self._effective_time_low = effective_time_low
        self._effective_time_high = effective_time_high
        self._persistent_id = persistent_id
        self._observations = observations or []
        self._author_is_patient = author_is_patient

    @property
    def name(self):
        return self._name

    @property
    def status(self):
        return self._status

    @property
    def effective_time_low(self):
        return self._effective_time_low

    @property
    def effective_time_high(self):
        return self._effective_time_high

    @property
    def persistent_id(self):
        return self._persistent_id

    @property
    def observations(self):
        return self._observations

    @property
    def author_is_patient(self):
        return self._author_is_patient


class TestHealthConcernsSection:
    """Tests for HealthConcernsSection builder."""

    def test_health_concerns_section_basic(self):
        """Test basic HealthConcernsSection creation."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_health_concerns_section_has_template_id_r21(self):
        """Test HealthConcernsSection includes R2.1 template ID."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.58"
        assert template.get("extension") == "2015-08-01"

    def test_health_concerns_section_has_template_id_r20(self):
        """Test HealthConcernsSection includes R2.0 template ID."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.58"
        assert template.get("extension") == "2015-08-01"

    def test_health_concerns_section_has_code(self):
        """Test HealthConcernsSection includes section code."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "75310-3"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Health concerns document"

    def test_health_concerns_section_has_title(self):
        """Test HealthConcernsSection includes title."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern], title="My Health Concerns")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Health Concerns"

    def test_health_concerns_section_default_title(self):
        """Test HealthConcernsSection uses default title."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Health Concerns"

    def test_health_concerns_section_has_narrative(self):
        """Test HealthConcernsSection includes narrative text."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_health_concerns_section_narrative_table(self):
        """Test narrative includes HTML table."""
        concern = MockHealthConcern(
            name="Risk of Hyperkalemia",
            status="active",
            effective_time_low=date(2023, 1, 15),
        )
        section = HealthConcernsSection([concern])
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
        assert len(ths) == 5  # Health Concern, Status, Effective Time, Observations, Type

    def test_health_concerns_section_narrative_content(self):
        """Test narrative contains health concern data."""
        obs = MockObservation(
            observation_type="problem",
            code="44054006",
            code_system="SNOMED CT",
            display_name="Diabetes mellitus type 2",
        )
        concern = MockHealthConcern(
            name="Risk of Hyperkalemia",
            status="active",
            effective_time_low=date(2023, 1, 15),
            observations=[obs],
            author_is_patient=False,
        )
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 5

        # Check concern name with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Risk of Hyperkalemia"
        assert content.get("ID") == "health-concern-1"

        # Check status
        assert tds[1].text == "Active"

        # Check effective time
        assert "2023-01-15" in tds[2].text
        assert "Ongoing" in tds[2].text

        # Check observations
        obs_list = tds[3].find(f"{{{NS}}}list")
        assert obs_list is not None
        item = obs_list.find(f"{{{NS}}}item")
        assert "Diabetes mellitus type 2" in item.text
        assert "problem" in item.text

        # Check concern type
        assert tds[4].text == "Provider"

    def test_health_concerns_section_narrative_patient_concern(self):
        """Test narrative shows patient concern type correctly."""
        concern = MockHealthConcern(
            name="Transportation difficulties",
            status="active",
            effective_time_low=date(2023, 1, 15),
            author_is_patient=True,
        )
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check concern type
        assert tds[4].text == "Patient"

    def test_health_concerns_section_narrative_completed_concern(self):
        """Test narrative shows completed concern with end date."""
        concern = MockHealthConcern(
            name="Risk of infection",
            status="completed",
            effective_time_low=date(2022, 5, 10),
            effective_time_high=date(2023, 2, 20),
        )
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check status
        assert tds[1].text == "Completed"

        # Check effective time includes end date
        assert "2022-05-10" in tds[2].text
        assert "2023-02-20" in tds[2].text

    def test_health_concerns_section_narrative_no_effective_time(self):
        """Test narrative shows 'Unknown' for missing effective time."""
        concern = MockHealthConcern(
            name="Under-insured",
            status="active",
            effective_time_low=None,
        )
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check effective time shows "Unknown"
        assert tds[2].text == "Unknown"

    def test_health_concerns_section_narrative_no_observations(self):
        """Test narrative shows 'None' for missing observations."""
        concern = MockHealthConcern(
            name="Transportation difficulties",
            status="active",
            effective_time_low=date(2023, 1, 15),
            observations=[],
        )
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check observations shows "None"
        assert tds[3].text == "None"

    def test_health_concerns_section_narrative_multiple_concerns(self):
        """Test narrative with multiple health concerns."""
        concerns = [
            MockHealthConcern(name="Risk of Hyperkalemia", status="active"),
            MockHealthConcern(name="Transportation difficulties", status="active"),
            MockHealthConcern(name="Under-insured", status="active"),
        ]
        section = HealthConcernsSection(concerns)
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

        assert content1.get("ID") == "health-concern-1"
        assert content2.get("ID") == "health-concern-2"
        assert content3.get("ID") == "health-concern-3"

    def test_health_concerns_section_narrative_multiple_observations(self):
        """Test narrative with multiple observations in a concern."""
        obs1 = MockObservation(
            observation_type="problem",
            code="44054006",
            display_name="Diabetes mellitus type 2",
        )
        obs2 = MockObservation(
            observation_type="allergy",
            code="387207008",
            display_name="Allergy to peanuts",
        )
        concern = MockHealthConcern(
            name="Multiple health issues",
            status="active",
            effective_time_low=date(2023, 1, 15),
            observations=[obs1, obs2],
        )
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check observations list has 2 items
        obs_list = tds[3].find(f"{{{NS}}}list")
        items = obs_list.findall(f"{{{NS}}}item")
        assert len(items) == 2
        assert "Diabetes mellitus type 2" in items[0].text
        assert "Allergy to peanuts" in items[1].text

    def test_health_concerns_section_empty_narrative(self):
        """Test narrative when no health concerns."""
        section = HealthConcernsSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No health concerns"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_health_concerns_section_null_flavor(self):
        """Test section with null flavor."""
        section = HealthConcernsSection([], null_flavor="NI")
        elem = section.to_element()

        # Check nullFlavor attribute
        assert elem.get("nullFlavor") == "NI"

        # Check narrative shows appropriate message
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No information available"

        # Should not have entries when nullFlavor is present
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_health_concerns_section_has_entries(self):
        """Test HealthConcernsSection includes entry elements."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_health_concerns_section_entry_has_health_concern_act(self):
        """Test entry contains Health Concern Act element."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"
        assert act.get("moodCode") == "EVN"

        # Check template ID
        template = act.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.132"

    def test_health_concerns_section_act_has_code(self):
        """Test Health Concern Act has correct code."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        code = act.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "75310-3"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Health Concern"

    def test_health_concerns_section_act_has_id(self):
        """Test Health Concern Act has ID element."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        id_elem = act.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("root") is not None

    def test_health_concerns_section_act_has_persistent_id(self):
        """Test Health Concern Act uses persistent ID when available."""
        pid = MockPersistentID(root="2.16.840.1.113883.19", extension="concern-123")
        concern = MockHealthConcern(persistent_id=pid)
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        id_elem = act.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.19"
        assert id_elem.get("extension") == "concern-123"

    def test_health_concerns_section_act_active_status(self):
        """Test Health Concern Act has active status for active concerns."""
        concern = MockHealthConcern(status="active")
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        status = act.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "active"

    def test_health_concerns_section_act_completed_status(self):
        """Test Health Concern Act has completed status for completed concerns."""
        concern = MockHealthConcern(status="completed")
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        status = act.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "completed"

    def test_health_concerns_section_act_suspended_status(self):
        """Test Health Concern Act supports suspended status."""
        concern = MockHealthConcern(status="suspended")
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        status = act.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "suspended"

    def test_health_concerns_section_act_aborted_status(self):
        """Test Health Concern Act supports aborted status."""
        concern = MockHealthConcern(status="aborted")
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        status = act.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "aborted"

    def test_health_concerns_section_act_effective_time(self):
        """Test Health Concern Act includes effectiveTime."""
        concern = MockHealthConcern(
            effective_time_low=date(2023, 1, 15),
            status="active",
        )
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        eff_time = act.find(f"{{{NS}}}effectiveTime")

        assert eff_time is not None
        low = eff_time.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20230115"

    def test_health_concerns_section_act_effective_time_with_high(self):
        """Test Health Concern Act includes effectiveTime with high date."""
        concern = MockHealthConcern(
            effective_time_low=date(2022, 5, 10),
            effective_time_high=date(2023, 2, 20),
            status="completed",
        )
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        eff_time = act.find(f"{{{NS}}}effectiveTime")

        assert eff_time is not None
        low = eff_time.find(f"{{{NS}}}low")
        high = eff_time.find(f"{{{NS}}}high")
        assert low is not None
        assert low.get("value") == "20220510"
        assert high is not None
        assert high.get("value") == "20230220"

    def test_health_concerns_section_act_no_effective_time(self):
        """Test Health Concern Act handles missing effectiveTime."""
        concern = MockHealthConcern(
            effective_time_low=None,
            effective_time_high=None,
        )
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        eff_time = act.find(f"{{{NS}}}effectiveTime")

        # effectiveTime is optional (MAY contain)
        # If no dates provided, it should not be present
        assert eff_time is None

    def test_health_concerns_section_act_has_observation(self):
        """Test Health Concern Act contains observation."""
        obs = MockObservation(
            observation_type="problem",
            code="44054006",
            code_system="SNOMED CT",
            display_name="Diabetes mellitus type 2",
        )
        concern = MockHealthConcern(observations=[obs])
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")

        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "REFR"

        observation = entry_rel.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"
        assert observation.get("moodCode") == "EVN"

    def test_health_concerns_section_act_observation_has_template(self):
        """Test observation has appropriate template ID."""
        obs = MockObservation(observation_type="problem")
        concern = MockHealthConcern(observations=[obs])
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        template = observation.find(f"{{{NS}}}templateId")

        assert template is not None
        # Problem observation template
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.4"

    def test_health_concerns_section_act_observation_code(self):
        """Test observation has correct code."""
        obs = MockObservation(
            observation_type="problem",
            code="44054006",
            code_system="SNOMED CT",
            display_name="Diabetes mellitus type 2",
        )
        concern = MockHealthConcern(observations=[obs])
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "44054006"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT OID
        assert code.get("displayName") == "Diabetes mellitus type 2"

    def test_health_concerns_section_act_observation_loinc_code(self):
        """Test observation with LOINC code system."""
        obs = MockObservation(
            observation_type="result",
            code="2339-0",
            code_system="LOINC",
            display_name="Glucose [Mass/volume] in Blood",
        )
        concern = MockHealthConcern(observations=[obs])
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "2339-0"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC OID
        assert code.get("codeSystemName") == "LOINC"

    def test_health_concerns_section_act_observation_custom_code_system(self):
        """Test observation with custom code system."""
        obs = MockObservation(
            observation_type="custom",
            code="12345",
            code_system="2.16.840.1.999999",
            display_name="Custom observation",
        )
        concern = MockHealthConcern(observations=[obs])
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "12345"
        assert code.get("codeSystem") == "2.16.840.1.999999"
        # Custom code system - no codeSystemName expected

    def test_health_concerns_section_act_multiple_observations(self):
        """Test Health Concern Act with multiple observations."""
        obs1 = MockObservation(
            observation_type="problem",
            code="44054006",
            display_name="Diabetes mellitus type 2",
        )
        obs2 = MockObservation(
            observation_type="allergy",
            code="387207008",
            display_name="Allergy to peanuts",
        )
        concern = MockHealthConcern(observations=[obs1, obs2])
        section = HealthConcernsSection([concern])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rels = act.findall(f"{{{NS}}}entryRelationship")

        assert len(entry_rels) == 2

        # Check each has an observation
        for entry_rel in entry_rels:
            observation = entry_rel.find(f"{{{NS}}}observation")
            assert observation is not None

    def test_health_concerns_section_multiple_entries(self):
        """Test HealthConcernsSection with multiple health concerns."""
        concerns = [
            MockHealthConcern(name="Risk of Hyperkalemia", status="active"),
            MockHealthConcern(name="Transportation difficulties", status="active"),
        ]
        section = HealthConcernsSection(concerns)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an act
        for entry in entries:
            act = entry.find(f"{{{NS}}}act")
            assert act is not None

    def test_health_concerns_section_to_string(self):
        """Test HealthConcernsSection serialization."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "75310-3" in xml  # Section code
        assert "Health" in xml  # Should contain "Health"

    def test_health_concerns_section_structure_order(self):
        """Test that section elements are in correct order."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern])
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


class TestHealthConcernsSectionIntegration:
    """Integration tests for HealthConcernsSection."""

    def test_complete_health_concerns_section(self):
        """Test creating a complete health concerns section."""
        obs1 = MockObservation(
            observation_type="problem",
            code="44054006",
            code_system="SNOMED CT",
            display_name="Diabetes mellitus type 2",
        )
        obs2 = MockObservation(
            observation_type="social_history",
            code="160903007",
            code_system="SNOMED CT",
            display_name="Lives alone",
        )

        concerns = [
            MockHealthConcern(
                name="Risk of Hyperkalemia",
                status="active",
                effective_time_low=date(2023, 1, 15),
                observations=[obs1],
                author_is_patient=False,
            ),
            MockHealthConcern(
                name="Transportation difficulties",
                status="active",
                effective_time_low=date(2023, 2, 10),
                observations=[obs2],
                author_is_patient=True,
            ),
            MockHealthConcern(
                name="Under-insured",
                status="active",
                effective_time_low=date(2023, 3, 5),
                observations=[],
                author_is_patient=False,
            ),
        ]

        section = HealthConcernsSection(concerns, title="Patient Health Concerns")
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

    def test_section_with_persistent_ids(self):
        """Test section with persistent IDs for health concerns."""
        pid1 = MockPersistentID(extension="concern-001")
        pid2 = MockPersistentID(extension="concern-002")

        concerns = [
            MockHealthConcern(name="Concern 1", persistent_id=pid1),
            MockHealthConcern(name="Concern 2", persistent_id=pid2),
        ]

        section = HealthConcernsSection(concerns)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check persistent IDs are used
        act1 = entries[0].find(f"{{{NS}}}act")
        id1 = act1.find(f"{{{NS}}}id")
        assert id1.get("extension") == "concern-001"

        act2 = entries[1].find(f"{{{NS}}}act")
        id2 = act2.find(f"{{{NS}}}id")
        assert id2.get("extension") == "concern-002"

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        concern = MockHealthConcern()
        section = HealthConcernsSection([concern])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_with_various_observation_types(self):
        """Test section with various observation types."""
        observations = [
            MockObservation(observation_type="problem", display_name="Diabetes"),
            MockObservation(observation_type="allergy", display_name="Penicillin allergy"),
            MockObservation(observation_type="social_history", display_name="Smoker"),
            MockObservation(observation_type="vital_sign", display_name="High BP"),
            MockObservation(observation_type="result", display_name="Abnormal HbA1c"),
        ]

        concern = MockHealthConcern(
            name="Multiple health issues",
            observations=observations,
        )

        section = HealthConcernsSection([concern])
        elem = section.to_element()

        # Verify all observations are included
        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rels = act.findall(f"{{{NS}}}entryRelationship")
        assert len(entry_rels) == 5

    def test_section_corner_case_empty_with_null_flavor(self):
        """Test corner case of empty section with null flavor."""
        section = HealthConcernsSection([], null_flavor="NI")
        elem = section.to_element()

        # Should have nullFlavor
        assert elem.get("nullFlavor") == "NI"

        # Should have narrative
        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should not have entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_section_corner_case_concern_without_observations(self):
        """Test corner case of concern without observations."""
        concern = MockHealthConcern(
            name="Social determinant concern",
            status="active",
            observations=[],
        )

        section = HealthConcernsSection([concern])
        elem = section.to_element()

        # Should still have entry
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        # Act should not have entryRelationship elements
        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rels = act.findall(f"{{{NS}}}entryRelationship")
        assert len(entry_rels) == 0

    def test_section_r20_version(self):
        """Test section builder with R2.0 version."""
        concern = MockHealthConcern()
        section = HealthConcernsSection([concern], version=CDAVersion.R2_0)
        elem = section.to_element()

        # Should have R2.0 template
        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.58"
        # R2.0 uses same extension as R2.1 for this template
        assert template.get("extension") == "2015-08-01"
