"""Tests for GoalsSection builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.goals import GoalsSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockGoal:
    """Mock goal for testing."""

    def __init__(
        self,
        description="Improve HbA1c to less than 7%",
        code=None,
        code_system=None,
        display_name=None,
        status="active",
        start_date=date(2023, 1, 15),
        target_date=date(2023, 12, 31),
        value=None,
        value_unit=None,
        author=None,
        priority=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._display_name = display_name
        self._status = status
        self._start_date = start_date
        self._target_date = target_date
        self._value = value
        self._value_unit = value_unit
        self._author = author
        self._priority = priority

    @property
    def description(self):
        return self._description

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
    def status(self):
        return self._status

    @property
    def start_date(self):
        return self._start_date

    @property
    def target_date(self):
        return self._target_date

    @property
    def value(self):
        return self._value

    @property
    def value_unit(self):
        return self._value_unit

    @property
    def author(self):
        return self._author

    @property
    def priority(self):
        return self._priority


class TestGoalsSection:
    """Tests for GoalsSection builder."""

    def test_goals_section_basic(self):
        """Test basic GoalsSection creation."""
        goal = MockGoal()
        section = GoalsSection([goal])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_goals_section_has_template_id_r21(self):
        """Test GoalsSection includes R2.1 template ID."""
        goal = MockGoal()
        section = GoalsSection([goal], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.60"
        # No extension per spec (CONF:1098-29585)
        assert template.get("extension") is None

    def test_goals_section_has_template_id_r20(self):
        """Test GoalsSection includes R2.0 template ID."""
        goal = MockGoal()
        section = GoalsSection([goal], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.60"

    def test_goals_section_has_code(self):
        """Test GoalsSection includes section code."""
        goal = MockGoal()
        section = GoalsSection([goal])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "61146-7"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Goals"

    def test_goals_section_has_title(self):
        """Test GoalsSection includes title."""
        goal = MockGoal()
        section = GoalsSection([goal], title="Patient Goals")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Patient Goals"

    def test_goals_section_default_title(self):
        """Test GoalsSection uses default title."""
        goal = MockGoal()
        section = GoalsSection([goal])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Goals"

    def test_goals_section_has_narrative(self):
        """Test GoalsSection includes narrative text."""
        goal = MockGoal()
        section = GoalsSection([goal])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_goals_section_narrative_table(self):
        """Test narrative includes HTML table."""
        goal = MockGoal(
            description="Reduce weight to 180 lbs",
            status="active",
            start_date=date(2023, 1, 15),
            target_date=date(2023, 12, 31),
        )
        section = GoalsSection([goal])
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
        assert len(ths) == 5  # Goal, Status, Start Date, Target Date, Value

    def test_goals_section_narrative_content(self):
        """Test narrative contains goal data."""
        goal = MockGoal(
            description="Improve HbA1c to less than 7%",
            status="active",
            start_date=date(2023, 1, 15),
            target_date=date(2023, 12, 31),
            value="7",
            value_unit="%",
        )
        section = GoalsSection([goal])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 5

        # Check goal description with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Improve HbA1c to less than 7%"
        assert content.get("ID") == "goal-1"

        # Check status
        assert tds[1].text == "Active"

        # Check start date
        assert tds[2].text == "2023-01-15"

        # Check target date
        assert tds[3].text == "2023-12-31"

        # Check value
        assert tds[4].text == "7 %"

    def test_goals_section_narrative_without_start_date(self):
        """Test narrative shows 'Not specified' for missing start date."""
        goal = MockGoal(start_date=None)
        section = GoalsSection([goal])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check start date shows "Not specified"
        assert tds[2].text == "Not specified"

    def test_goals_section_narrative_without_target_date(self):
        """Test narrative shows 'Not specified' for missing target date."""
        goal = MockGoal(target_date=None)
        section = GoalsSection([goal])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check target date shows "Not specified"
        assert tds[3].text == "Not specified"

    def test_goals_section_narrative_without_value(self):
        """Test narrative shows 'Not specified' for missing value."""
        goal = MockGoal(value=None)
        section = GoalsSection([goal])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check value shows "Not specified"
        assert tds[4].text == "Not specified"

    def test_goals_section_narrative_value_without_unit(self):
        """Test narrative shows value without unit."""
        goal = MockGoal(value="Complete physical therapy", value_unit=None)
        section = GoalsSection([goal])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check value shows without unit
        assert tds[4].text == "Complete physical therapy"

    def test_goals_section_narrative_multiple_goals(self):
        """Test narrative with multiple goals."""
        goals = [
            MockGoal(description="Improve HbA1c to less than 7%"),
            MockGoal(description="Reduce weight to 180 lbs"),
            MockGoal(description="Exercise 30 minutes daily"),
        ]
        section = GoalsSection(goals)
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

        assert content1.get("ID") == "goal-1"
        assert content2.get("ID") == "goal-2"
        assert content3.get("ID") == "goal-3"

    def test_goals_section_narrative_completed_goal(self):
        """Test narrative shows completed status correctly."""
        goal = MockGoal(
            description="Complete cardiac rehabilitation",
            status="completed",
        )
        section = GoalsSection([goal])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check status
        assert tds[1].text == "Completed"

    def test_goals_section_narrative_on_hold_status(self):
        """Test narrative shows on-hold status correctly."""
        goal = MockGoal(
            description="Reduce sodium intake",
            status="on-hold",
        )
        section = GoalsSection([goal])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check status (should format "on-hold" as "On Hold")
        assert tds[1].text == "On Hold"

    def test_goals_section_empty_narrative(self):
        """Test narrative when no goals."""
        section = GoalsSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No goals documented"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_goals_section_has_entries(self):
        """Test GoalsSection includes entry elements."""
        goal = MockGoal()
        section = GoalsSection([goal])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_goals_section_entry_has_observation(self):
        """Test entry contains goal observation."""
        goal = MockGoal()
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"
        assert observation.get("moodCode") == "GOL"

    def test_goals_section_observation_has_template_id(self):
        """Test observation has correct template ID."""
        goal = MockGoal()
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        template = observation.find(f"{{{NS}}}templateId")

        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.121"
        assert template.get("extension") == "2022-06-01"

    def test_goals_section_observation_has_id(self):
        """Test observation has ID element."""
        goal = MockGoal()
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        id_elem = observation.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_goals_section_observation_has_code(self):
        """Test observation has code element."""
        goal = MockGoal(
            code="4548-4",
            code_system="LOINC",
            display_name="Hemoglobin A1c/Hemoglobin.total in Blood",
        )
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "4548-4"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC OID
        assert code.get("displayName") == "Hemoglobin A1c/Hemoglobin.total in Blood"

    def test_goals_section_observation_default_code(self):
        """Test observation has default code when not specified."""
        goal = MockGoal(code=None, code_system=None)
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "ASSERTION"

    def test_goals_section_observation_has_status_code(self):
        """Test observation has statusCode element."""
        goal = MockGoal(status="active")
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        status = observation.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "active"

    def test_goals_section_observation_completed_status(self):
        """Test observation with completed status."""
        goal = MockGoal(status="completed")
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        status = observation.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "completed"

    def test_goals_section_observation_cancelled_status(self):
        """Test observation with cancelled status."""
        goal = MockGoal(status="cancelled")
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        status = observation.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "cancelled"

    def test_goals_section_observation_has_effective_time(self):
        """Test observation includes effectiveTime."""
        goal = MockGoal(
            start_date=date(2023, 1, 15),
            target_date=date(2023, 12, 31),
        )
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        eff_time = observation.find(f"{{{NS}}}effectiveTime")

        assert eff_time is not None
        low = eff_time.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20230115"

        high = eff_time.find(f"{{{NS}}}high")
        assert high is not None
        assert high.get("value") == "20231231"

    def test_goals_section_observation_effective_time_only_start(self):
        """Test observation with only start date."""
        goal = MockGoal(
            start_date=date(2023, 1, 15),
            target_date=None,
        )
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        eff_time = observation.find(f"{{{NS}}}effectiveTime")

        assert eff_time is not None
        low = eff_time.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20230115"

    def test_goals_section_observation_no_effective_time(self):
        """Test observation without effectiveTime when dates are missing."""
        goal = MockGoal(start_date=None, target_date=None)
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        eff_time = observation.find(f"{{{NS}}}effectiveTime")

        assert eff_time is None

    def test_goals_section_observation_has_value_with_unit(self):
        """Test observation has value with unit."""
        goal = MockGoal(value="180", value_unit="lbs")
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "PQ"
        assert value.get("value") == "180"
        assert value.get("unit") == "lbs"

    def test_goals_section_observation_has_value_without_unit(self):
        """Test observation has value without unit (string type)."""
        goal = MockGoal(value="Complete physical therapy", value_unit=None)
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "ST"
        assert value.text == "Complete physical therapy"

    def test_goals_section_observation_value_from_description(self):
        """Test observation uses description as value when no explicit value."""
        goal = MockGoal(
            description="Improve mobility",
            value=None,
            value_unit=None,
        )
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.text == "Improve mobility"

    def test_goals_section_multiple_entries(self):
        """Test GoalsSection with multiple goals."""
        goals = [
            MockGoal(description="Improve HbA1c to less than 7%"),
            MockGoal(description="Reduce weight to 180 lbs"),
        ]
        section = GoalsSection(goals)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an observation
        for entry in entries:
            observation = entry.find(f"{{{NS}}}observation")
            assert observation is not None

    def test_goals_section_null_flavor(self):
        """Test GoalsSection with null flavor."""
        section = GoalsSection([], null_flavor="NI")
        elem = section.to_element()

        assert elem.get("nullFlavor") == "NI"

    def test_goals_section_to_string(self):
        """Test GoalsSection serialization."""
        goal = MockGoal()
        section = GoalsSection([goal])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "61146-7" in xml  # Section code
        assert "Goals" in xml or "goal" in xml

    def test_goals_section_structure_order(self):
        """Test that section elements are in correct order."""
        goal = MockGoal()
        section = GoalsSection([goal])
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


class TestGoalsSectionIntegration:
    """Integration tests for GoalsSection."""

    def test_complete_goals_section(self):
        """Test creating a complete goals section."""
        goals = [
            MockGoal(
                description="Improve HbA1c to less than 7%",
                code="4548-4",
                code_system="LOINC",
                display_name="Hemoglobin A1c/Hemoglobin.total in Blood",
                status="active",
                start_date=date(2023, 1, 15),
                target_date=date(2023, 12, 31),
                value="7",
                value_unit="%",
            ),
            MockGoal(
                description="Reduce weight to 180 lbs",
                code="29463-7",
                code_system="LOINC",
                display_name="Body weight",
                status="active",
                start_date=date(2023, 2, 1),
                target_date=date(2024, 2, 1),
                value="180",
                value_unit="lbs",
            ),
            MockGoal(
                description="Exercise 30 minutes daily",
                status="active",
                start_date=date(2023, 1, 1),
                target_date=None,
                value="30 minutes daily",
                value_unit=None,
            ),
        ]

        section = GoalsSection(goals, title="Patient Health Goals")
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

        goal = MockGoal()
        section = GoalsSection([goal])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_sdoh_goal(self):
        """Test Social Determinant of Health (SDOH) goal."""
        goal = MockGoal(
            description="Gain transportation security - able to access health and social needs",
            code="8689-2",
            code_system="LOINC",
            display_name="History of Social function",
            status="active",
            start_date=date(2023, 3, 1),
            target_date=date(2023, 9, 1),
        )
        section = GoalsSection([goal])
        elem = section.to_element()

        # Verify observation has SDOH code
        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "8689-2"
        assert code.get("displayName") == "History of Social function"

    def test_empty_goals_section(self):
        """Test GoalsSection with no goals."""
        section = GoalsSection([])
        elem = section.to_element()

        # Should still have required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Should have no entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

        # Narrative should show "No goals documented"
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No goals documented"

    def test_goals_section_with_snomed_code(self):
        """Test goal with SNOMED CT code."""
        goal = MockGoal(
            description="Maintain blood pressure below 140/90",
            code="182777000",
            code_system="SNOMED",
            display_name="Hypertension monitoring",
            status="active",
        )
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "182777000"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED OID

    def test_corner_case_all_optional_fields_missing(self):
        """Test goal with only required fields (description and status)."""
        goal = MockGoal(
            description="General health improvement",
            code=None,
            code_system=None,
            display_name=None,
            status="active",
            start_date=None,
            target_date=None,
            value=None,
            value_unit=None,
        )
        section = GoalsSection([goal])
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

        assert tds[0].find(f"{{{NS}}}content").text == "General health improvement"
        assert tds[1].text == "Active"
        assert tds[2].text == "Not specified"  # start date
        assert tds[3].text == "Not specified"  # target date
        assert tds[4].text == "Not specified"  # value

    def test_numeric_value_as_string(self):
        """Test that numeric values are properly converted to strings."""
        goal = MockGoal(
            description="Target HbA1c",
            value=7.5,  # numeric value
            value_unit="%",
        )
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.get("value") == "7.5"

    def test_custom_code_system(self):
        """Test goal with custom/unknown code system."""
        goal = MockGoal(
            description="Custom health goal",
            code="12345",
            code_system="2.16.840.1.113883.3.1234.5.6",  # Custom OID
            display_name="Custom Goal Type",
        )
        section = GoalsSection([goal])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "12345"
        # Should use the OID directly
        assert code.get("codeSystem") == "2.16.840.1.113883.3.1234.5.6"
        assert code.get("codeSystemName") == "2.16.840.1.113883.3.1234.5.6"
        assert code.get("displayName") == "Custom Goal Type"
