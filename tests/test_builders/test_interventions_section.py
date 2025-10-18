"""Tests for InterventionsSection builder."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.sections.interventions import InterventionsSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockIntervention:
    """Mock intervention for testing."""

    def __init__(
        self,
        id="INT-001",
        description="Elevate head of bed and provide humidified O2",
        status="completed",
        effective_time=date(2023, 6, 15),
        intervention_type="procedure",
        goal_reference_id=None,
        author=None,
    ):
        self._id = id
        self._description = description
        self._status = status
        self._effective_time = effective_time
        self._intervention_type = intervention_type
        self._goal_reference_id = goal_reference_id
        self._author = author

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        return self._description

    @property
    def status(self):
        return self._status

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def intervention_type(self):
        return self._intervention_type

    @property
    def goal_reference_id(self):
        return self._goal_reference_id

    @property
    def author(self):
        return self._author


class MockPlannedIntervention:
    """Mock planned intervention for testing."""

    def __init__(
        self,
        id="PLANNED-INT-001",
        description="Physical therapy for mobility improvement",
        mood_code="INT",
        status="active",
        effective_time=date(2023, 7, 1),
        intervention_type="procedure",
        goal_reference_id="GOAL-001",
        author=None,
    ):
        self._id = id
        self._description = description
        self._mood_code = mood_code
        self._status = status
        self._effective_time = effective_time
        self._intervention_type = intervention_type
        self._goal_reference_id = goal_reference_id
        self._author = author

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        return self._description

    @property
    def mood_code(self):
        return self._mood_code

    @property
    def status(self):
        return self._status

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def intervention_type(self):
        return self._intervention_type

    @property
    def goal_reference_id(self):
        return self._goal_reference_id

    @property
    def author(self):
        return self._author


class TestInterventionsSection:
    """Tests for InterventionsSection builder."""

    def test_interventions_section_basic(self):
        """Test basic InterventionsSection creation."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_interventions_section_has_template_id_r21(self):
        """Test InterventionsSection includes R2.1 template ID."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.21.2.3"
        assert template.get("extension") == "2015-08-01"

    def test_interventions_section_has_template_id_r20(self):
        """Test InterventionsSection includes R2.0 template ID."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.21.2.3"
        assert template.get("extension") == "2015-08-01"

    def test_interventions_section_has_code(self):
        """Test InterventionsSection includes section code."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "62387-6"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Interventions Provided"

    def test_interventions_section_has_title(self):
        """Test InterventionsSection includes title."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention], title="Care Interventions")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Care Interventions"

    def test_interventions_section_default_title(self):
        """Test InterventionsSection uses default title."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Interventions"

    def test_interventions_section_has_narrative(self):
        """Test InterventionsSection includes narrative text."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_interventions_section_narrative_table(self):
        """Test narrative includes HTML table."""
        intervention = MockIntervention(
            description="Elevate head of bed",
            effective_time=date(2023, 6, 15),
        )
        section = InterventionsSection(interventions=[intervention])
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
        assert len(ths) == 5  # Type, Description, Status, Date, Goal Reference

    def test_interventions_section_narrative_content(self):
        """Test narrative contains intervention data."""
        intervention = MockIntervention(
            description="Elevate head of bed and provide O2",
            status="completed",
            effective_time=date(2023, 6, 15),
            goal_reference_id="GOAL-001",
        )
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 5

        # Check type
        assert tds[0].text == "Completed"

        # Check description with ID
        content = tds[1].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Elevate head of bed and provide O2"
        assert content.get("ID") == "intervention-1"

        # Check status
        assert tds[2].text == "Completed"

        # Check date
        assert tds[3].text == "2023-06-15"

        # Check goal reference
        assert "GOAL-001" in tds[4].text

    def test_interventions_section_narrative_planned_intervention(self):
        """Test narrative includes planned interventions."""
        planned = MockPlannedIntervention(
            description="Physical therapy session",
            effective_time=date(2023, 7, 1),
            goal_reference_id="GOAL-002",
        )
        section = InterventionsSection(planned_interventions=[planned])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")

        # Check type
        assert tds[0].text == "Planned"

        # Check description
        content = tds[1].find(f"{{{NS}}}content")
        assert content.text == "Physical therapy session"

        # Check status
        assert tds[2].text == "Active"

    def test_interventions_section_narrative_mixed_interventions(self):
        """Test narrative with both completed and planned interventions."""
        interventions = [MockIntervention(description="Completed intervention")]
        planned = [MockPlannedIntervention(description="Planned intervention")]

        section = InterventionsSection(
            interventions=interventions,
            planned_interventions=planned,
        )
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        assert len(trs) == 2

        # Check types
        assert trs[0].findall(f"{{{NS}}}td")[0].text == "Completed"
        assert trs[1].findall(f"{{{NS}}}td")[0].text == "Planned"

    def test_interventions_section_empty_narrative(self):
        """Test narrative when no interventions."""
        section = InterventionsSection()
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No interventions documented"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_interventions_section_has_entries(self):
        """Test InterventionsSection includes entry elements."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_interventions_section_entry_has_act(self):
        """Test entry contains intervention act."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"
        assert act.get("moodCode") == "EVN"

    def test_interventions_section_act_has_template_id(self):
        """Test intervention act has correct template ID."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        template = act.find(f"{{{NS}}}templateId")

        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.131"
        assert template.get("extension") == "2015-08-01"

    def test_interventions_section_act_has_id(self):
        """Test intervention act has ID element."""
        intervention = MockIntervention(id="INT-123")
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        id_elem = act.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("extension") == "INT-123"

    def test_interventions_section_act_has_code(self):
        """Test intervention act has correct code."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        code = act.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "362956003"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT

    def test_interventions_section_act_has_status_code(self):
        """Test intervention act has statusCode element."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        status = act.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "completed"

    def test_interventions_section_act_has_effective_time(self):
        """Test intervention act includes effectiveTime."""
        intervention = MockIntervention(effective_time=date(2023, 6, 15))
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        eff_time = act.find(f"{{{NS}}}effectiveTime")

        assert eff_time is not None
        assert eff_time.get("value") == "20230615"

    def test_interventions_section_act_with_goal_reference(self):
        """Test intervention act with goal reference."""
        intervention = MockIntervention(goal_reference_id="GOAL-001")
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")

        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "RSON"

        ref_act = entry_rel.find(f"{{{NS}}}act")
        assert ref_act is not None

        template = ref_act.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.122"

        id_elem = ref_act.find(f"{{{NS}}}id")
        assert id_elem.get("root") == "GOAL-001"

    def test_interventions_section_planned_act_entry(self):
        """Test planned intervention act entry."""
        planned = MockPlannedIntervention()
        section = InterventionsSection(planned_interventions=[planned])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"
        assert act.get("moodCode") == "INT"

    def test_interventions_section_planned_act_has_template_id(self):
        """Test planned intervention act has correct template ID."""
        planned = MockPlannedIntervention()
        section = InterventionsSection(planned_interventions=[planned])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        template = act.find(f"{{{NS}}}templateId")

        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.146"
        assert template.get("extension") == "2015-08-01"

    def test_interventions_section_planned_act_has_status_code(self):
        """Test planned intervention act has statusCode active."""
        planned = MockPlannedIntervention()
        section = InterventionsSection(planned_interventions=[planned])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        status = act.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "active"

    def test_interventions_section_planned_act_with_goal_reference(self):
        """Test planned intervention act with goal reference."""
        planned = MockPlannedIntervention(goal_reference_id="GOAL-002")
        section = InterventionsSection(planned_interventions=[planned])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")

        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "RSON"

        ref_act = entry_rel.find(f"{{{NS}}}act")
        id_elem = ref_act.find(f"{{{NS}}}id")
        assert id_elem.get("root") == "GOAL-002"

    def test_interventions_section_multiple_entries(self):
        """Test InterventionsSection with multiple interventions."""
        interventions = [
            MockIntervention(description="First intervention"),
            MockIntervention(description="Second intervention"),
        ]
        section = InterventionsSection(interventions=interventions)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_interventions_section_mixed_entries(self):
        """Test InterventionsSection with both types."""
        interventions = [MockIntervention()]
        planned = [MockPlannedIntervention()]

        section = InterventionsSection(
            interventions=interventions,
            planned_interventions=planned,
        )
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_interventions_section_null_flavor(self):
        """Test InterventionsSection with null flavor."""
        section = InterventionsSection(null_flavor="NI")
        elem = section.to_element()

        assert elem.get("nullFlavor") == "NI"

    def test_interventions_section_to_string(self):
        """Test InterventionsSection serialization."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "62387-6" in xml  # Section code
        assert "Interventions" in xml

    def test_interventions_section_structure_order(self):
        """Test that section elements are in correct order."""
        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention])
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

    def test_interventions_section_datetime_effective_time(self):
        """Test intervention with datetime effective time."""
        intervention = MockIntervention(effective_time=datetime(2023, 6, 15, 10, 30))
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        eff_time = act.find(f"{{{NS}}}effectiveTime")

        assert eff_time is not None
        assert eff_time.get("value") == "20230615"

    def test_interventions_section_without_effective_time(self):
        """Test intervention without effective time."""
        intervention = MockIntervention(effective_time=None)
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        eff_time = act.find(f"{{{NS}}}effectiveTime")

        # Should not have effectiveTime element
        assert eff_time is None

    def test_interventions_section_without_goal_reference(self):
        """Test intervention without goal reference."""
        intervention = MockIntervention(goal_reference_id=None)
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")

        # Should not have entryRelationship for goal
        assert entry_rel is None

    def test_planned_intervention_mood_code_arq(self):
        """Test planned intervention with ARQ mood code."""
        planned = MockPlannedIntervention(mood_code="ARQ")
        section = InterventionsSection(planned_interventions=[planned])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act.get("moodCode") == "ARQ"

    def test_planned_intervention_mood_code_prms(self):
        """Test planned intervention with PRMS mood code."""
        planned = MockPlannedIntervention(mood_code="PRMS")
        section = InterventionsSection(planned_interventions=[planned])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act.get("moodCode") == "PRMS"

    def test_planned_intervention_invalid_mood_code_defaults_to_int(self):
        """Test planned intervention with invalid mood code defaults to INT."""
        planned = MockPlannedIntervention(mood_code="INVALID")
        section = InterventionsSection(planned_interventions=[planned])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act.get("moodCode") == "INT"

    def test_interventions_section_narrative_without_date(self):
        """Test narrative shows 'Not specified' for missing date."""
        intervention = MockIntervention(effective_time=None)
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check date shows "Not specified"
        assert tds[3].text == "Not specified"

    def test_interventions_section_narrative_without_goal_reference(self):
        """Test narrative shows 'Not specified' for missing goal reference."""
        intervention = MockIntervention(goal_reference_id=None)
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check goal reference shows "Not specified"
        assert tds[4].text == "Not specified"


class TestInterventionsSectionIntegration:
    """Integration tests for InterventionsSection."""

    def test_complete_interventions_section(self):
        """Test creating a complete interventions section."""
        interventions = [
            MockIntervention(
                id="INT-001",
                description="Elevate head of bed 30 degrees",
                status="completed",
                effective_time=date(2023, 6, 15),
                goal_reference_id="GOAL-001",
            ),
            MockIntervention(
                id="INT-002",
                description="Provide humidified O2 per nasal cannula",
                status="completed",
                effective_time=date(2023, 6, 15),
                goal_reference_id="GOAL-001",
            ),
        ]

        planned = [
            MockPlannedIntervention(
                id="PLANNED-001",
                description="Physical therapy session for mobility",
                mood_code="INT",
                effective_time=date(2023, 7, 1),
                goal_reference_id="GOAL-002",
            ),
        ]

        section = InterventionsSection(
            interventions=interventions,
            planned_interventions=planned,
            title="Patient Care Interventions",
        )
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

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        intervention = MockIntervention()
        section = InterventionsSection(interventions=[intervention])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_empty_interventions_section(self):
        """Test InterventionsSection with no interventions."""
        section = InterventionsSection()
        elem = section.to_element()

        # Should still have required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Should have no entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

        # Narrative should show "No interventions documented"
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No interventions documented"

    def test_corner_case_minimal_intervention(self):
        """Test intervention with only required fields."""
        intervention = MockIntervention(
            id="MIN-001",
            description="Minimal intervention",
            status="completed",
            effective_time=None,
            goal_reference_id=None,
        )
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        # Should still build successfully
        assert elem is not None
        assert elem.find(f"{{{NS}}}entry") is not None

    def test_corner_case_minimal_planned_intervention(self):
        """Test planned intervention with minimal required fields."""
        planned = MockPlannedIntervention(
            id="MIN-PLANNED-001",
            description="Minimal planned intervention",
            goal_reference_id="GOAL-001",  # Required for planned
            effective_time=None,
        )
        section = InterventionsSection(planned_interventions=[planned])
        elem = section.to_element()

        # Should still build successfully
        assert elem is not None
        entry = elem.find(f"{{{NS}}}entry")
        assert entry is not None

        # Should have goal reference (required for planned)
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is not None

    def test_planned_intervention_without_goal_creates_placeholder(self):
        """Test planned intervention without goal reference creates placeholder."""
        planned = MockPlannedIntervention(goal_reference_id=None)
        section = InterventionsSection(planned_interventions=[planned])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")

        # Should still have entryRelationship (required)
        assert entry_rel is not None

        ref_act = entry_rel.find(f"{{{NS}}}act")
        id_elem = ref_act.find(f"{{{NS}}}id")

        # Should have nullFlavor
        assert id_elem.get("nullFlavor") == "UNK"

    def test_intervention_with_string_effective_time(self):
        """Test intervention with string effective time."""

        class MockInterventionStringTime(MockIntervention):
            def __init__(self):
                super().__init__()
                self._effective_time = "20230615"

        intervention = MockInterventionStringTime()
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        eff_time = act.find(f"{{{NS}}}effectiveTime")

        assert eff_time is not None
        assert eff_time.get("value") == "20230615"

    def test_multiple_interventions_with_different_goals(self):
        """Test multiple interventions referencing different goals."""
        interventions = [
            MockIntervention(
                description="Intervention for goal 1",
                goal_reference_id="GOAL-001",
            ),
            MockIntervention(
                description="Intervention for goal 2",
                goal_reference_id="GOAL-002",
            ),
            MockIntervention(
                description="Intervention without goal",
                goal_reference_id=None,
            ),
        ]
        section = InterventionsSection(interventions=interventions)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 3

        # Check first entry has goal reference
        act1 = entries[0].find(f"{{{NS}}}act")
        entry_rel1 = act1.find(f"{{{NS}}}entryRelationship")
        assert entry_rel1 is not None

        # Check third entry has no goal reference
        act3 = entries[2].find(f"{{{NS}}}act")
        entry_rel3 = act3.find(f"{{{NS}}}entryRelationship")
        assert entry_rel3 is None

    def test_status_formatting_in_narrative(self):
        """Test that status is formatted properly in narrative."""
        intervention = MockIntervention(status="on-hold")
        section = InterventionsSection(interventions=[intervention])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Status should be formatted as "On Hold"
        assert tds[2].text == "On Hold"

    def test_large_number_of_interventions(self):
        """Test section with many interventions."""
        interventions = [
            MockIntervention(id=f"INT-{i:03d}", description=f"Intervention {i}")
            for i in range(20)
        ]
        section = InterventionsSection(interventions=interventions)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 20

        # Check narrative has 20 rows
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 20
