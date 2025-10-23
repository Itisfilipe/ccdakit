"""Tests for HealthStatusEvaluationsAndOutcomesSection builder."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.sections.health_status_evaluations import (
    HealthStatusEvaluationsAndOutcomesSection,
)
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockProgressTowardGoal:
    """Mock progress toward goal for testing."""

    def __init__(
        self,
        id="progress-1",
        achievement_code="385641008",
        achievement_code_system="2.16.840.1.113883.6.96",
        achievement_display_name="Improving",
    ):
        self._id = id
        self._achievement_code = achievement_code
        self._achievement_code_system = achievement_code_system
        self._achievement_display_name = achievement_display_name

    @property
    def id(self):
        return self._id

    @property
    def achievement_code(self):
        return self._achievement_code

    @property
    def achievement_code_system(self):
        return self._achievement_code_system

    @property
    def achievement_display_name(self):
        return self._achievement_display_name


class MockOutcomeObservation:
    """Mock outcome observation for testing."""

    def __init__(
        self,
        id="outcome-1",
        code="29463-7",
        code_system="LOINC",
        display_name="Body weight",
        value="180",
        value_unit="lbs",
        effective_time=date(2023, 6, 15),
        progress_toward_goal=None,
        goal_reference_id=None,
        intervention_reference_ids=None,
        author_name=None,
        author_time=None,
    ):
        self._id = id
        self._code = code
        self._code_system = code_system
        self._display_name = display_name
        self._value = value
        self._value_unit = value_unit
        self._effective_time = effective_time
        self._progress_toward_goal = progress_toward_goal
        self._goal_reference_id = goal_reference_id
        self._intervention_reference_ids = intervention_reference_ids
        self._author_name = author_name
        self._author_time = author_time

    @property
    def id(self):
        return self._id

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def display_name(self):
        return self._display_name

    @property
    def value(self):
        return self._value

    @property
    def value_unit(self):
        return self._value_unit

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def progress_toward_goal(self):
        return self._progress_toward_goal

    @property
    def goal_reference_id(self):
        return self._goal_reference_id

    @property
    def intervention_reference_ids(self):
        return self._intervention_reference_ids

    @property
    def author_name(self):
        return self._author_name

    @property
    def author_time(self):
        return self._author_time


class TestHealthStatusEvaluationsAndOutcomesSection:
    """Tests for HealthStatusEvaluationsAndOutcomesSection builder."""

    def test_section_basic(self):
        """Test basic section creation."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_has_template_id_r21(self):
        """Test section includes R2.1 template ID."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.61"
        # No extension per spec (CONF:1098-29579)
        assert template.get("extension") is None

    def test_section_has_template_id_r20(self):
        """Test section includes R2.0 template ID."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.61"

    def test_section_has_code(self):
        """Test section includes section code."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "11383-7"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Patient Problem Outcome"

    def test_section_has_title(self):
        """Test section includes title."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome], title="Patient Outcomes")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Patient Outcomes"

    def test_section_default_title(self):
        """Test section uses default title."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Health Status Evaluations and Outcomes"

    def test_section_has_narrative(self):
        """Test section includes narrative text."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_section_narrative_table(self):
        """Test narrative includes HTML table."""
        outcome = MockOutcomeObservation(
            display_name="Body weight",
            value="180",
            value_unit="lbs",
            effective_time=date(2023, 6, 15),
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
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
        assert len(ths) == 4  # Outcome, Value, Date, Progress Toward Goal

    def test_section_narrative_content(self):
        """Test narrative contains outcome data."""
        progress = MockProgressTowardGoal(achievement_display_name="Improving")
        outcome = MockOutcomeObservation(
            display_name="Body weight",
            value="180",
            value_unit="lbs",
            effective_time=date(2023, 6, 15),
            progress_toward_goal=progress,
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 4

        # Check outcome description with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Body weight"
        assert content.get("ID") == "outcome-1"

        # Check value
        assert tds[1].text == "180 lbs"

        # Check date
        assert tds[2].text == "2023-06-15"

        # Check progress
        assert tds[3].text == "Improving"

    def test_section_narrative_without_value(self):
        """Test narrative shows 'Not specified' for missing value."""
        outcome = MockOutcomeObservation(value=None, value_unit=None)
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check value shows "Not specified"
        assert tds[1].text == "Not specified"

    def test_section_narrative_without_date(self):
        """Test narrative shows 'Not specified' for missing date."""
        outcome = MockOutcomeObservation(effective_time=None)
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check date shows "Not specified"
        assert tds[2].text == "Not specified"

    def test_section_narrative_without_progress(self):
        """Test narrative shows 'Not specified' for missing progress."""
        outcome = MockOutcomeObservation(progress_toward_goal=None)
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check progress shows "Not specified"
        assert tds[3].text == "Not specified"

    def test_section_narrative_value_without_unit(self):
        """Test narrative shows value without unit."""
        outcome = MockOutcomeObservation(value="Improved mobility", value_unit=None)
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check value shows without unit
        assert tds[1].text == "Improved mobility"

    def test_section_narrative_multiple_outcomes(self):
        """Test narrative with multiple outcomes."""
        outcomes = [
            MockOutcomeObservation(display_name="Body weight", value="180", value_unit="lbs"),
            MockOutcomeObservation(
                display_name="Blood pressure", value="120/80", value_unit="mmHg"
            ),
            MockOutcomeObservation(display_name="HbA1c", value="6.8", value_unit="%"),
        ]
        section = HealthStatusEvaluationsAndOutcomesSection(outcomes)
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

        assert content1.get("ID") == "outcome-1"
        assert content2.get("ID") == "outcome-2"
        assert content3.get("ID") == "outcome-3"

    def test_section_empty_narrative(self):
        """Test narrative when no outcomes."""
        section = HealthStatusEvaluationsAndOutcomesSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert "No health status evaluations" in paragraph.text

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_section_has_entries(self):
        """Test section includes entry elements."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_section_entry_has_observation(self):
        """Test entry contains outcome observation."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"
        assert observation.get("moodCode") == "EVN"

    def test_section_observation_has_template_id(self):
        """Test observation has correct template ID."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        template = observation.find(f"{{{NS}}}templateId")

        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.144"

    def test_section_observation_has_id(self):
        """Test observation has ID element."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        id_elem = observation.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_section_observation_has_code(self):
        """Test observation has code element."""
        outcome = MockOutcomeObservation(
            code="29463-7",
            code_system="LOINC",
            display_name="Body weight",
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "29463-7"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC OID
        assert code.get("displayName") == "Body weight"

    def test_section_observation_default_code(self):
        """Test observation has default code when not specified."""
        outcome = MockOutcomeObservation(code=None, code_system=None)
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "ASSERTION"

    def test_section_observation_has_status_code(self):
        """Test observation has statusCode element."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        status = observation.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "completed"

    def test_section_observation_has_effective_time(self):
        """Test observation includes effectiveTime."""
        outcome = MockOutcomeObservation(effective_time=date(2023, 6, 15))
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        eff_time = observation.find(f"{{{NS}}}effectiveTime")

        assert eff_time is not None
        assert eff_time.get("value") == "20230615"

    def test_section_observation_no_effective_time(self):
        """Test observation without effectiveTime when date is missing."""
        outcome = MockOutcomeObservation(effective_time=None)
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        eff_time = observation.find(f"{{{NS}}}effectiveTime")

        assert eff_time is None

    def test_section_observation_has_value_with_unit(self):
        """Test observation has value with unit."""
        outcome = MockOutcomeObservation(value="180", value_unit="lbs")
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "PQ"
        assert value.get("value") == "180"
        assert value.get("unit") == "lbs"

    def test_section_observation_has_value_without_unit(self):
        """Test observation has value without unit (string type)."""
        outcome = MockOutcomeObservation(value="Improved mobility", value_unit=None)
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "ST"
        assert value.text == "Improved mobility"

    def test_section_observation_with_goal_reference(self):
        """Test observation with goal reference."""
        outcome = MockOutcomeObservation(goal_reference_id="goal-123")
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")

        # Find entryRelationship with typeCode="GEVL" (Evaluates goal)
        entry_rels = observation.findall(f"{{{NS}}}entryRelationship")
        goal_ref = None
        for rel in entry_rels:
            if rel.get("typeCode") == "GEVL":
                goal_ref = rel
                break

        assert goal_ref is not None

        # Check Entry Reference structure
        ref_act = goal_ref.find(f"{{{NS}}}act")
        assert ref_act is not None
        assert ref_act.get("classCode") == "ACT"
        assert ref_act.get("moodCode") == "EVN"

        # Check template ID
        template = ref_act.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.122"

        # Check ID references the goal
        id_elem = ref_act.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("extension") == "goal-123"

    def test_section_observation_with_progress_toward_goal(self):
        """Test observation with progress toward goal."""
        progress = MockProgressTowardGoal(
            id="progress-1",
            achievement_code="385641008",
            achievement_display_name="Improving",
        )
        outcome = MockOutcomeObservation(progress_toward_goal=progress)
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")

        # Find entryRelationship with typeCode="SPRT" (Has support)
        entry_rels = observation.findall(f"{{{NS}}}entryRelationship")
        progress_rel = None
        for rel in entry_rels:
            if rel.get("typeCode") == "SPRT":
                progress_rel = rel
                break

        assert progress_rel is not None
        assert progress_rel.get("inversionInd") == "true"

        # Check Progress Toward Goal Observation structure
        progress_obs = progress_rel.find(f"{{{NS}}}observation")
        assert progress_obs is not None
        assert progress_obs.get("classCode") == "OBS"
        assert progress_obs.get("moodCode") == "EVN"

        # Check template ID
        template = progress_obs.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.110"

        # Check value has achievement code
        value = progress_obs.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "385641008"
        assert value.get("displayName") == "Improving"

    def test_section_observation_with_intervention_references(self):
        """Test observation with intervention references."""
        outcome = MockOutcomeObservation(
            intervention_reference_ids=["intervention-1", "intervention-2"]
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")

        # Find entryRelationships with typeCode="RSON" (Has reason)
        entry_rels = observation.findall(f"{{{NS}}}entryRelationship")
        intervention_refs = [rel for rel in entry_rels if rel.get("typeCode") == "RSON"]

        assert len(intervention_refs) == 2

        # Check first reference
        ref_act = intervention_refs[0].find(f"{{{NS}}}act")
        assert ref_act is not None
        id_elem = ref_act.find(f"{{{NS}}}id")
        assert id_elem.get("extension") == "intervention-1"

        # Check second reference
        ref_act = intervention_refs[1].find(f"{{{NS}}}act")
        assert ref_act is not None
        id_elem = ref_act.find(f"{{{NS}}}id")
        assert id_elem.get("extension") == "intervention-2"

    def test_section_observation_with_author(self):
        """Test observation with author."""
        outcome = MockOutcomeObservation(
            author_name="Dr. Jane Smith",
            author_time=datetime(2023, 6, 15, 14, 30, 0),
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        author = observation.find(f"{{{NS}}}author")

        assert author is not None

        # Check time
        time = author.find(f"{{{NS}}}time")
        assert time is not None
        assert time.get("value") == "20230615143000"

        # Check assigned author
        assigned_author = author.find(f"{{{NS}}}assignedAuthor")
        assert assigned_author is not None

        # Check person name
        person = assigned_author.find(f"{{{NS}}}assignedPerson")
        assert person is not None
        name = person.find(f"{{{NS}}}name")
        assert name is not None
        assert name.text == "Dr. Jane Smith"

    def test_section_multiple_entries(self):
        """Test section with multiple outcomes."""
        outcomes = [
            MockOutcomeObservation(display_name="Body weight", value="180", value_unit="lbs"),
            MockOutcomeObservation(
                display_name="Blood pressure", value="120/80", value_unit="mmHg"
            ),
        ]
        section = HealthStatusEvaluationsAndOutcomesSection(outcomes)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an observation
        for entry in entries:
            observation = entry.find(f"{{{NS}}}observation")
            assert observation is not None

    def test_section_null_flavor(self):
        """Test section with null flavor."""
        section = HealthStatusEvaluationsAndOutcomesSection([], null_flavor="NI")
        elem = section.to_element()

        assert elem.get("nullFlavor") == "NI"

    def test_section_to_string(self):
        """Test section serialization."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "11383-7" in xml  # Section code
        assert "Health Status Evaluations" in xml or "Outcome" in xml

    def test_section_structure_order(self):
        """Test that section elements are in correct order."""
        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
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


class TestHealthStatusEvaluationsAndOutcomesSectionIntegration:
    """Integration tests for HealthStatusEvaluationsAndOutcomesSection."""

    def test_complete_section(self):
        """Test creating a complete section with all features."""
        progress = MockProgressTowardGoal(
            achievement_code="385641008",
            achievement_display_name="Improving",
        )

        outcomes = [
            MockOutcomeObservation(
                id="outcome-1",
                code="29463-7",
                code_system="LOINC",
                display_name="Body weight",
                value="180",
                value_unit="lbs",
                effective_time=date(2023, 6, 15),
                progress_toward_goal=progress,
                goal_reference_id="goal-weight",
                intervention_reference_ids=["intervention-diet", "intervention-exercise"],
                author_name="Dr. Jane Smith",
                author_time=datetime(2023, 6, 15, 14, 30, 0),
            ),
            MockOutcomeObservation(
                id="outcome-2",
                code="2339-0",
                code_system="LOINC",
                display_name="Glucose [Mass/volume] in Blood",
                value="95",
                value_unit="mg/dL",
                effective_time=date(2023, 6, 15),
                goal_reference_id="goal-glucose",
            ),
        ]

        section = HealthStatusEvaluationsAndOutcomesSection(
            outcomes, title="Health Status Evaluations and Outcomes"
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

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        outcome = MockOutcomeObservation()
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_empty_section(self):
        """Test section with no outcomes."""
        section = HealthStatusEvaluationsAndOutcomesSection([])
        elem = section.to_element()

        # Should still have required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Should have no entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

        # Narrative should show "No outcomes documented"
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert "No health status evaluations" in paragraph.text

    def test_outcome_with_snomed_code(self):
        """Test outcome with SNOMED CT code."""
        outcome = MockOutcomeObservation(
            code="162598000",
            code_system="SNOMED",
            display_name="Goal not achieved",
            value="Blood pressure still elevated",
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "162598000"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED OID

    def test_corner_case_all_optional_fields_missing(self):
        """Test outcome with only required fields."""
        outcome = MockOutcomeObservation(
            code=None,
            code_system=None,
            display_name=None,
            value=None,
            value_unit=None,
            effective_time=None,
            progress_toward_goal=None,
            goal_reference_id=None,
            intervention_reference_ids=None,
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        # Should still build successfully
        assert elem is not None
        assert elem.find(f"{{{NS}}}entry") is not None

        # Check narrative handles missing fields
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Should show appropriate defaults/fallbacks
        assert tds[1].text == "Not specified"  # value
        assert tds[2].text == "Not specified"  # date
        assert tds[3].text == "Not specified"  # progress

    def test_numeric_value_as_string(self):
        """Test that numeric values are properly converted to strings."""
        outcome = MockOutcomeObservation(
            value=95.5,  # numeric value
            value_unit="mg/dL",
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.get("value") == "95.5"

    def test_custom_code_system(self):
        """Test outcome with custom/unknown code system."""
        outcome = MockOutcomeObservation(
            code="12345",
            code_system="2.16.840.1.113883.3.1234.5.6",  # Custom OID
            display_name="Custom Outcome Type",
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "12345"
        # Should use the OID directly
        assert code.get("codeSystem") == "2.16.840.1.113883.3.1234.5.6"
        assert code.get("displayName") == "Custom Outcome Type"

    def test_outcome_with_only_goal_reference(self):
        """Test outcome with only goal reference (no progress or interventions)."""
        outcome = MockOutcomeObservation(
            goal_reference_id="goal-123",
            progress_toward_goal=None,
            intervention_reference_ids=None,
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")

        # Should have one entryRelationship for goal reference
        entry_rels = observation.findall(f"{{{NS}}}entryRelationship")
        assert len(entry_rels) == 1
        assert entry_rels[0].get("typeCode") == "GEVL"

    def test_outcome_with_only_progress(self):
        """Test outcome with only progress (no goal or intervention references)."""
        progress = MockProgressTowardGoal()
        outcome = MockOutcomeObservation(
            progress_toward_goal=progress,
            goal_reference_id=None,
            intervention_reference_ids=None,
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")

        # Should have one entryRelationship for progress
        entry_rels = observation.findall(f"{{{NS}}}entryRelationship")
        assert len(entry_rels) == 1
        assert entry_rels[0].get("typeCode") == "SPRT"

    def test_narrative_with_code_fallback(self):
        """Test narrative uses code when display_name is missing."""
        outcome = MockOutcomeObservation(
            code="29463-7",
            display_name=None,
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        content = tds[0].find(f"{{{NS}}}content")
        assert "29463-7" in content.text

    def test_outcome_with_custom_code_system_in_progress(self):
        """Test progress toward goal with custom code system."""
        progress = MockProgressTowardGoal(
            achievement_code="12345",
            achievement_code_system="2.16.840.1.113883.3.1234.5.6",
            achievement_display_name="Custom Achievement",
        )
        outcome = MockOutcomeObservation(progress_toward_goal=progress)
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        entry_rels = observation.findall(f"{{{NS}}}entryRelationship")
        progress_rel = [rel for rel in entry_rels if rel.get("typeCode") == "SPRT"][0]
        progress_obs = progress_rel.find(f"{{{NS}}}observation")
        value = progress_obs.find(f"{{{NS}}}value")

        assert value.get("code") == "12345"
        assert value.get("codeSystem") == "2.16.840.1.113883.3.1234.5.6"

    def test_outcome_with_snomed_code_system_in_progress(self):
        """Test progress toward goal explicitly with SNOMED code system."""
        progress = MockProgressTowardGoal(
            achievement_code="385641008",
            achievement_code_system="SNOMED CT",
            achievement_display_name="Improving",
        )
        outcome = MockOutcomeObservation(progress_toward_goal=progress)
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        entry_rels = observation.findall(f"{{{NS}}}entryRelationship")
        progress_rel = [rel for rel in entry_rels if rel.get("typeCode") == "SPRT"][0]
        progress_obs = progress_rel.find(f"{{{NS}}}observation")
        value = progress_obs.find(f"{{{NS}}}value")

        assert value.get("code") == "385641008"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED OID
        assert value.get("codeSystemName") == "SNOMED CT"

    def test_outcome_with_author_time_only(self):
        """Test outcome with author time but no name."""
        outcome = MockOutcomeObservation(
            author_name=None,
            author_time=datetime(2023, 6, 15, 14, 30, 0),
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        author = observation.find(f"{{{NS}}}author")

        assert author is not None
        time = author.find(f"{{{NS}}}time")
        assert time is not None

    def test_outcome_with_author_name_only(self):
        """Test outcome with author name but no time."""
        outcome = MockOutcomeObservation(
            author_name="Dr. Jane Smith",
            author_time=None,
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        author = observation.find(f"{{{NS}}}author")

        assert author is not None
        person = author.find(f".//{{{NS}}}assignedPerson")
        assert person is not None

    def test_progress_without_explicit_id(self):
        """Test progress toward goal auto-generates ID when not provided."""
        # Create progress without ID

        class ProgressWithoutId:
            def __init__(self):
                self._achievement_code = "385641008"
                self._achievement_code_system = "2.16.840.1.113883.6.96"
                self._achievement_display_name = "Improving"

            @property
            def achievement_code(self):
                return self._achievement_code

            @property
            def achievement_code_system(self):
                return self._achievement_code_system

            @property
            def achievement_display_name(self):
                return self._achievement_display_name

        outcome = MockOutcomeObservation(progress_toward_goal=ProgressWithoutId())
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        entry_rels = observation.findall(f"{{{NS}}}entryRelationship")
        progress_rel = [rel for rel in entry_rels if rel.get("typeCode") == "SPRT"][0]
        progress_obs = progress_rel.find(f"{{{NS}}}observation")
        id_elem = progress_obs.find(f"{{{NS}}}id")

        # Should have auto-generated UUID
        assert id_elem is not None
        assert id_elem.get("extension") is not None

    def test_outcome_without_explicit_id(self):
        """Test outcome observation auto-generates ID when not provided."""

        class OutcomeWithoutId:
            def __init__(self):
                self._code = "29463-7"
                self._code_system = "LOINC"
                self._display_name = "Body weight"
                self._value = "180"
                self._value_unit = "lbs"

            @property
            def code(self):
                return self._code

            @property
            def code_system(self):
                return self._code_system

            @property
            def display_name(self):
                return self._display_name

            @property
            def value(self):
                return self._value

            @property
            def value_unit(self):
                return self._value_unit

        section = HealthStatusEvaluationsAndOutcomesSection([OutcomeWithoutId()])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        id_elem = observation.find(f"{{{NS}}}id")

        # Should have auto-generated UUID
        assert id_elem is not None
        assert id_elem.get("extension") is not None

    def test_narrative_no_code_or_display_name(self):
        """Test narrative fallback when both code and display_name are missing."""
        outcome = MockOutcomeObservation(
            code=None,
            code_system=None,
            display_name=None,
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        content = tds[0].find(f"{{{NS}}}content")
        assert content.text == "Outcome observation"

    def test_narrative_effective_time_as_string(self):
        """Test narrative with effective_time as a string instead of date object."""
        outcome = MockOutcomeObservation(
            display_name="Pain Level",
            value="3",
            value_unit="scale 0-10",
            effective_time="2023-06-15",  # String instead of date
        )
        section = HealthStatusEvaluationsAndOutcomesSection([outcome])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Time column should show string value (index 2)
        assert tds[2].text == "2023-06-15"
