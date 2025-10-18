"""Tests for AssessmentAndPlanSection builder."""

from datetime import datetime

import pytest
from lxml import etree

from ccdakit.builders.sections.assessment_and_plan import AssessmentAndPlanSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockPlannedAct:
    """Mock planned act for testing."""

    def __init__(
        self,
        id_root="2.16.840.1.113883.19",
        id_extension="12345",
        code="183460006",
        code_system="SNOMED",
        display_name="Dressing change",
        mood_code="INT",
        effective_time=datetime(2024, 6, 15, 10, 0, 0),
        instructions=None,
    ):
        self._id_root = id_root
        self._id_extension = id_extension
        self._code = code
        self._code_system = code_system
        self._display_name = display_name
        self._mood_code = mood_code
        self._effective_time = effective_time
        self._instructions = instructions

    @property
    def id_root(self):
        return self._id_root

    @property
    def id_extension(self):
        return self._id_extension

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
    def mood_code(self):
        return self._mood_code

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def instructions(self):
        return self._instructions


class MockAssessmentAndPlanItem:
    """Mock assessment/plan item for testing."""

    def __init__(
        self,
        text="Patient has hypertension. Will start medication.",
        item_type="assessment",
        planned_act=None,
    ):
        self._text = text
        self._item_type = item_type
        self._planned_act = planned_act

    @property
    def text(self):
        return self._text

    @property
    def item_type(self):
        return self._item_type

    @property
    def planned_act(self):
        return self._planned_act


class TestAssessmentAndPlanSection:
    """Tests for AssessmentAndPlanSection builder."""

    # Basic Section Tests

    def test_section_basic(self):
        """Test basic AssessmentAndPlanSection creation."""
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_with_items(self):
        """Test AssessmentAndPlanSection with items."""
        item = MockAssessmentAndPlanItem()
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        assert local_name(elem) == "section"

    # Template ID Tests

    def test_has_template_id_r21(self):
        """Test section includes R2.1 template ID (CONF:1098-7705, 10381, 32583)."""
        section = AssessmentAndPlanSection(version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.9"
        assert template.get("extension") == "2014-06-09"

    def test_has_template_id_r20(self):
        """Test section includes R2.0 template ID (same as R2.1)."""
        section = AssessmentAndPlanSection(version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.9"
        assert template.get("extension") == "2014-06-09"

    # Section Code Tests

    def test_has_code(self):
        """Test section includes required code (CONF:1098-15353, 15354)."""
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "51847-2"

    def test_code_system(self):
        """Test section code system is LOINC (CONF:1098-32141)."""
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"

    def test_code_display_name(self):
        """Test section code has display name."""
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code.get("displayName") == "Assessment and Plan"

    # Title Tests

    def test_has_title(self):
        """Test section includes title."""
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Assessment and Plan"

    def test_custom_title(self):
        """Test section with custom title."""
        section = AssessmentAndPlanSection(title="Clinical Assessment and Treatment Plan")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Clinical Assessment and Treatment Plan"

    # Narrative Text Tests

    def test_has_narrative(self):
        """Test section includes narrative text (CONF:1098-7707)."""
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_narrative_empty_items(self):
        """Test narrative with no items shows placeholder."""
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert "documented in clinical notes" in paragraph.text

    def test_narrative_assessment_items(self):
        """Test narrative with assessment items."""
        items = [
            MockAssessmentAndPlanItem(
                text="Hypertension is well-controlled",
                item_type="assessment",
            ),
            MockAssessmentAndPlanItem(
                text="Diabetes showing improvement",
                item_type="assessment",
            ),
        ]
        section = AssessmentAndPlanSection(items=items)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        # Check for Assessment heading
        paragraphs = text.findall(f"{{{NS}}}paragraph")
        assert any("Assessment" in (p.find(f"{{{NS}}}content").text or "") for p in paragraphs)

        # Check for list
        list_elem = text.find(f"{{{NS}}}list")
        assert list_elem is not None
        items_elems = list_elem.findall(f"{{{NS}}}item")
        assert len(items_elems) == 2

    def test_narrative_plan_items(self):
        """Test narrative with plan items."""
        items = [
            MockAssessmentAndPlanItem(
                text="Start metformin 500mg twice daily",
                item_type="plan",
            ),
            MockAssessmentAndPlanItem(
                text="Follow up in 2 weeks",
                item_type="plan",
            ),
        ]
        section = AssessmentAndPlanSection(items=items)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        # Check for Plan heading
        paragraphs = text.findall(f"{{{NS}}}paragraph")
        assert any("Plan" in (p.find(f"{{{NS}}}content").text or "") for p in paragraphs)

        # Check for list
        list_elem = text.find(f"{{{NS}}}list")
        assert list_elem is not None
        items_elems = list_elem.findall(f"{{{NS}}}item")
        assert len(items_elems) == 2

    def test_narrative_mixed_items(self):
        """Test narrative with both assessment and plan items."""
        items = [
            MockAssessmentAndPlanItem(
                text="Hypertension is well-controlled",
                item_type="assessment",
            ),
            MockAssessmentAndPlanItem(
                text="Continue current medications",
                item_type="plan",
            ),
        ]
        section = AssessmentAndPlanSection(items=items)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraphs = text.findall(f"{{{NS}}}paragraph")

        # Should have both headings
        heading_texts = [p.find(f"{{{NS}}}content").text for p in paragraphs if p.find(f"{{{NS}}}content") is not None]
        assert "Assessment" in heading_texts
        assert "Plan" in heading_texts

    def test_narrative_content_ids(self):
        """Test narrative content has proper ID references."""
        items = [
            MockAssessmentAndPlanItem(
                text="Assessment finding",
                item_type="assessment",
            ),
        ]
        section = AssessmentAndPlanSection(items=items)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        list_elem = text.find(f"{{{NS}}}list")
        item_elem = list_elem.find(f"{{{NS}}}item")
        content = item_elem.find(f"{{{NS}}}content")

        assert content.get("ID") == "assessment-1"

    # Entry Tests

    def test_entry_with_planned_act(self):
        """Test entry with Planned Act (CONF:1098-7708, 15448)."""
        planned_act = MockPlannedAct()
        item = MockAssessmentAndPlanItem(
            text="Change dressing daily",
            item_type="plan",
            planned_act=planned_act,
        )
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        # Check for Planned Act inside entry
        entry = entries[0]
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"

    def test_no_entry_without_planned_act(self):
        """Test no entry is created for items without planned acts."""
        item = MockAssessmentAndPlanItem(
            text="Assessment only",
            item_type="assessment",
            planned_act=None,
        )
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_multiple_entries(self):
        """Test multiple entries with different planned acts."""
        planned_act1 = MockPlannedAct(code="183460006", display_name="Dressing change")
        planned_act2 = MockPlannedAct(code="409073007", display_name="Patient education")

        items = [
            MockAssessmentAndPlanItem(
                text="Change dressing",
                item_type="plan",
                planned_act=planned_act1,
            ),
            MockAssessmentAndPlanItem(
                text="Educate patient",
                item_type="plan",
                planned_act=planned_act2,
            ),
        ]
        section = AssessmentAndPlanSection(items)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    # Planned Act Entry Details Tests

    def test_planned_act_has_template_id(self):
        """Test Planned Act has correct template ID."""
        planned_act = MockPlannedAct()
        item = MockAssessmentAndPlanItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        template = act.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.39"
        assert template.get("extension") == "2014-06-09"

    def test_planned_act_has_id(self):
        """Test Planned Act has ID (CONF:1098-8546)."""
        planned_act = MockPlannedAct(id_root="2.16.840.1.113883.19", id_extension="test-123")
        item = MockAssessmentAndPlanItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        id_elem = act.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.19"
        assert id_elem.get("extension") == "test-123"

    def test_planned_act_has_code(self):
        """Test Planned Act has code (CONF:1098-31687, 32030)."""
        planned_act = MockPlannedAct(
            code="183460006",
            code_system="SNOMED",
            display_name="Dressing change",
        )
        item = MockAssessmentAndPlanItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        code = act.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "183460006"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED OID
        assert code.get("displayName") == "Dressing change"

    def test_planned_act_has_status_code_active(self):
        """Test Planned Act has statusCode='active' (CONF:1098-30432, 32019)."""
        planned_act = MockPlannedAct()
        item = MockAssessmentAndPlanItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        status = act.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "active"

    def test_planned_act_has_mood_code(self):
        """Test Planned Act has proper moodCode (CONF:1098-8539)."""
        planned_act = MockPlannedAct(mood_code="INT")
        item = MockAssessmentAndPlanItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        assert act.get("moodCode") == "INT"

    def test_planned_act_different_mood_codes(self):
        """Test Planned Act supports different mood codes."""
        for mood_code in ["INT", "RQO", "PRMS", "PRP"]:
            planned_act = MockPlannedAct(mood_code=mood_code)
            item = MockAssessmentAndPlanItem(planned_act=planned_act)
            section = AssessmentAndPlanSection([item])
            elem = section.to_element()

            act = elem.find(f".//{{{NS}}}act")
            assert act.get("moodCode") == mood_code

    def test_planned_act_has_effective_time(self):
        """Test Planned Act has effectiveTime (CONF:1098-30433)."""
        planned_act = MockPlannedAct(effective_time=datetime(2024, 6, 15, 10, 30, 0))
        item = MockAssessmentAndPlanItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        time_elem = act.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None
        assert time_elem.get("value") == "20240615103000"

    def test_planned_act_without_effective_time(self):
        """Test Planned Act can omit effectiveTime (optional)."""
        planned_act = MockPlannedAct(effective_time=None)
        item = MockAssessmentAndPlanItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        time_elem = act.find(f"{{{NS}}}effectiveTime")
        assert time_elem is None

    def test_planned_act_with_instructions(self):
        """Test Planned Act with instructions (CONF:1098-32024, 32025, 32026)."""
        planned_act = MockPlannedAct(instructions="Change dressing every 8 hours")
        item = MockAssessmentAndPlanItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship[@typeCode='SUBJ']")
        assert entry_rel is not None

        # Check instruction act
        instruction_act = entry_rel.find(f"{{{NS}}}act")
        assert instruction_act is not None
        assert instruction_act.get("classCode") == "ACT"
        assert instruction_act.get("moodCode") == "INT"

        # Check instruction template ID
        template = instruction_act.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.20"

        # Check instruction text
        text_elem = instruction_act.find(f"{{{NS}}}text")
        assert text_elem.text == "Change dressing every 8 hours"

    def test_planned_act_without_instructions(self):
        """Test Planned Act without instructions."""
        planned_act = MockPlannedAct(instructions=None)
        item = MockAssessmentAndPlanItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship[@typeCode='SUBJ']")
        assert entry_rel is None

    # Code System Tests

    def test_planned_act_loinc_code(self):
        """Test Planned Act with LOINC code (CONF:1098-32030)."""
        planned_act = MockPlannedAct(
            code="57024-2",
            code_system="LOINC",
            display_name="Health behavior assessment",
        )
        item = MockAssessmentAndPlanItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        code = act.find(f"{{{NS}}}code")
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC OID

    # Edge Cases and Corner Cases

    def test_empty_items_list(self):
        """Test section with empty items list."""
        section = AssessmentAndPlanSection(items=[])
        elem = section.to_element()

        assert local_name(elem) == "section"
        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_none_items_list(self):
        """Test section with None items list."""
        section = AssessmentAndPlanSection(items=None)
        elem = section.to_element()

        assert local_name(elem) == "section"
        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_assessment_only_items(self):
        """Test section with only assessment items (no entries)."""
        items = [
            MockAssessmentAndPlanItem(text="Finding 1", item_type="assessment"),
            MockAssessmentAndPlanItem(text="Finding 2", item_type="assessment"),
        ]
        section = AssessmentAndPlanSection(items=items)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

        # But should have narrative
        text = elem.find(f"{{{NS}}}text")
        list_elem = text.find(f"{{{NS}}}list")
        assert list_elem is not None

    def test_plan_only_items(self):
        """Test section with only plan items."""
        items = [
            MockAssessmentAndPlanItem(text="Plan 1", item_type="plan"),
            MockAssessmentAndPlanItem(text="Plan 2", item_type="plan"),
        ]
        section = AssessmentAndPlanSection(items=items)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        list_elem = text.find(f"{{{NS}}}list")
        assert list_elem is not None

    def test_narrative_list_attributes(self):
        """Test narrative list has proper attributes."""
        items = [MockAssessmentAndPlanItem(text="Test", item_type="assessment")]
        section = AssessmentAndPlanSection(items=items)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        list_elem = text.find(f"{{{NS}}}list")
        assert list_elem.get("listType") == "unordered"

    # XML Structure Validation Tests

    def test_element_order(self):
        """Test elements appear in correct order per CDA schema."""
        planned_act = MockPlannedAct()
        item = MockAssessmentAndPlanItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        # Check order: templateId, code, title, text, entry
        children = list(elem)
        child_names = [local_name(c) for c in children]

        template_idx = child_names.index("templateId")
        code_idx = child_names.index("code")
        title_idx = child_names.index("title")
        text_idx = child_names.index("text")

        assert template_idx < code_idx < title_idx < text_idx

        # Entry should be after text if present
        if "entry" in child_names:
            entry_idx = child_names.index("entry")
            assert text_idx < entry_idx

    def test_namespace_consistency(self):
        """Test all elements use correct namespace."""
        planned_act = MockPlannedAct()
        item = MockAssessmentAndPlanItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        # Check section namespace
        assert elem.tag == f"{{{NS}}}section"

        # Check all descendants have namespace
        for descendant in elem.iter():
            assert descendant.tag.startswith(f"{{{NS}}}")

    # Version Compatibility Tests

    def test_r21_and_r20_use_same_template(self):
        """Test R2.1 and R2.0 versions use the same template (2014-06-09)."""
        section_r21 = AssessmentAndPlanSection(version=CDAVersion.R2_1)
        section_r20 = AssessmentAndPlanSection(version=CDAVersion.R2_0)

        elem_r21 = section_r21.to_element()
        elem_r20 = section_r20.to_element()

        template_r21 = elem_r21.find(f"{{{NS}}}templateId")
        template_r20 = elem_r20.find(f"{{{NS}}}templateId")

        assert template_r21.get("extension") == template_r20.get("extension")
        assert template_r21.get("root") == template_r20.get("root")

    # Integration Tests

    def test_complete_section_with_all_features(self):
        """Test complete section with all features enabled."""
        planned_act = MockPlannedAct(
            id_root="2.16.840.1.113883.19",
            id_extension="act-001",
            code="183460006",
            code_system="SNOMED",
            display_name="Dressing change",
            mood_code="INT",
            effective_time=datetime(2024, 6, 15, 14, 30, 0),
            instructions="Change wound dressing twice daily using sterile technique",
        )

        items = [
            MockAssessmentAndPlanItem(
                text="Stage 2 pressure ulcer on sacrum, improving",
                item_type="assessment",
            ),
            MockAssessmentAndPlanItem(
                text="Continue current wound care regimen",
                item_type="plan",
                planned_act=planned_act,
            ),
            MockAssessmentAndPlanItem(
                text="Monitor for signs of infection",
                item_type="plan",
            ),
        ]

        section = AssessmentAndPlanSection(
            items=items,
            title="Assessment and Treatment Plan",
            version=CDAVersion.R2_1,
        )
        elem = section.to_element()

        # Verify section structure
        assert local_name(elem) == "section"
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title").text == "Assessment and Treatment Plan"
        assert elem.find(f"{{{NS}}}text") is not None

        # Verify narrative has both assessment and plan sections
        text = elem.find(f"{{{NS}}}text")
        paragraphs = text.findall(f"{{{NS}}}paragraph")
        heading_texts = [
            p.find(f"{{{NS}}}content").text
            for p in paragraphs
            if p.find(f"{{{NS}}}content") is not None
        ]
        assert "Assessment" in heading_texts
        assert "Plan" in heading_texts

        # Verify entry with complete planned act
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        act = entries[0].find(f"{{{NS}}}act")
        assert act is not None
        assert act.find(f"{{{NS}}}id") is not None
        assert act.find(f"{{{NS}}}code") is not None
        assert act.find(f"{{{NS}}}statusCode").get("code") == "active"
        assert act.find(f"{{{NS}}}effectiveTime") is not None
        assert act.find(f"{{{NS}}}entryRelationship[@typeCode='SUBJ']") is not None
