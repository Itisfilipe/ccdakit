"""Conformance tests for Assessment and Plan Section against C-CDA spec."""

from datetime import datetime

from lxml import etree

from ccdakit.builders.sections.assessment_and_plan import AssessmentAndPlanSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


class MockPlannedAct:
    """Mock planned act for conformance testing."""

    def __init__(self):
        self.id_root = "2.16.840.1.113883.19"
        self.id_extension = "test-001"
        self.code = "183460006"
        self.code_system = "SNOMED"
        self.display_name = "Dressing change"
        self.mood_code = "INT"
        self.effective_time = datetime(2024, 6, 15, 10, 0, 0)
        self.instructions = "Test instructions"


class MockItem:
    """Mock item for conformance testing."""

    def __init__(self, text="Test", item_type="assessment", planned_act=None):
        self.text = text
        self.item_type = item_type
        self.planned_act = planned_act


class TestAssessmentAndPlanConformance:
    """
    Test conformance to C-CDA 2.1 specification.

    Template: Assessment and Plan Section (V2)
    Template ID: 2.16.840.1.113883.10.20.22.2.9
    Extension: 2014-06-09
    """

    def test_conf_1098_7705_template_id_required(self):
        """
        CONF:1098-7705: SHALL contain exactly one [1..1] templateId.

        The section must have a templateId element.
        """
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        templates = elem.findall(f"{{{NS}}}templateId")
        assert len(templates) >= 1, "Section must contain at least one templateId"

    def test_conf_1098_10381_template_root(self):
        """
        CONF:1098-10381: SHALL contain exactly one [1..1] @root="2.16.840.1.113883.10.20.22.2.9".

        The templateId must have the correct root OID.
        """
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.9"

    def test_conf_1098_32583_template_extension(self):
        """
        CONF:1098-32583: SHALL contain exactly one [1..1] @extension="2014-06-09".

        The templateId must have the correct extension (version date).
        """
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("extension") == "2014-06-09"

    def test_conf_1098_15353_code_required(self):
        """
        CONF:1098-15353: SHALL contain exactly one [1..1] code.

        The section must have a code element.
        """
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        codes = elem.findall(f"{{{NS}}}code")
        assert len(codes) == 1, "Section must contain exactly one code element"

    def test_conf_1098_15354_code_value(self):
        """
        CONF:1098-15354: This code SHALL contain exactly one [1..1] @code="51847-2" Assessment and Plan.

        The section code must be "51847-2" from LOINC.
        """
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code.get("code") == "51847-2"

    def test_conf_1098_32141_code_system(self):
        """
        CONF:1098-32141: This code SHALL contain exactly one [1..1] @codeSystem="2.16.840.1.113883.6.1" (LOINC).

        The section code must use the LOINC code system.
        """
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"

    def test_conf_1098_7707_text_required(self):
        """
        CONF:1098-7707: SHALL contain exactly one [1..1] text.

        The section must have a narrative text element.
        """
        section = AssessmentAndPlanSection()
        elem = section.to_element()

        texts = elem.findall(f"{{{NS}}}text")
        assert len(texts) == 1, "Section must contain exactly one text element"

    def test_conf_1098_7708_entry_optional(self):
        """
        CONF:1098-7708: MAY contain zero or more [0..*] entry.

        The section may contain entry elements (optional).
        """
        # Test with no entries
        section1 = AssessmentAndPlanSection()
        elem1 = section1.to_element()
        entries1 = elem1.findall(f"{{{NS}}}entry")
        assert len(entries1) == 0, "Section with no planned acts should have no entries"

        # Test with one entry
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section2 = AssessmentAndPlanSection([item])
        elem2 = section2.to_element()
        entries2 = elem2.findall(f"{{{NS}}}entry")
        assert len(entries2) == 1, "Section with one planned act should have one entry"

    def test_conf_1098_15448_entry_planned_act(self):
        """
        CONF:1098-15448: SHALL contain exactly one [1..1] Planned Act (V2).

        If an entry is present, it must contain a Planned Act.
        """
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        assert entry is not None

        # Check for act inside entry
        act = entry.find(f"{{{NS}}}act")
        assert act is not None, "Entry must contain an act element"

        # Check for Planned Act template ID
        template = act.find(f"{{{NS}}}templateId[@root='2.16.840.1.113883.10.20.22.4.39']")
        assert template is not None, "Act must be a Planned Act (V2)"

    # Planned Act Conformance Tests

    def test_conf_1098_8538_act_class_code(self):
        """
        CONF:1098-8538: SHALL contain exactly one [1..1] @classCode="ACT".

        The planned act must have classCode="ACT".
        """
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        assert act.get("classCode") == "ACT"

    def test_conf_1098_8539_act_mood_code(self):
        """
        CONF:1098-8539: SHALL contain exactly one [1..1] @moodCode from Planned moodCode value set.

        The planned act must have a moodCode from the value set.
        Valid values: INT, RQO, PRMS, PRP
        """
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        mood_code = act.get("moodCode")
        assert mood_code in ["INT", "RQO", "PRMS", "PRP"], f"Invalid moodCode: {mood_code}"

    def test_conf_1098_30430_act_template_id(self):
        """
        CONF:1098-30430: SHALL contain exactly one [1..1] templateId.

        The planned act must have a templateId.
        """
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        templates = act.findall(f"{{{NS}}}templateId")
        assert len(templates) >= 1, "Planned act must have a templateId"

    def test_conf_1098_30431_act_template_root(self):
        """
        CONF:1098-30431: SHALL contain exactly one [1..1] @root="2.16.840.1.113883.10.20.22.4.39".

        The planned act templateId must have the correct root.
        """
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        template = act.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.39"

    def test_conf_1098_32552_act_template_extension(self):
        """
        CONF:1098-32552: SHALL contain exactly one [1..1] @extension="2014-06-09".

        The planned act templateId must have the correct extension.
        """
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        template = act.find(f"{{{NS}}}templateId")
        assert template.get("extension") == "2014-06-09"

    def test_conf_1098_8546_act_id_required(self):
        """
        CONF:1098-8546: SHALL contain at least one [1..*] id.

        The planned act must have at least one id element.
        """
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        ids = act.findall(f"{{{NS}}}id")
        assert len(ids) >= 1, "Planned act must have at least one id"

    def test_conf_1098_31687_act_code_required(self):
        """
        CONF:1098-31687: SHALL contain exactly one [1..1] code.

        The planned act must have a code element.
        """
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        codes = act.findall(f"{{{NS}}}code")
        assert len(codes) == 1, "Planned act must have exactly one code"

    def test_conf_1098_32030_act_code_system(self):
        """
        CONF:1098-32030: Code SHOULD be selected from LOINC or SNOMED CT.

        The code should use LOINC (2.16.840.1.113883.6.1) or SNOMED (2.16.840.1.113883.6.96).
        """
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        code = act.find(f"{{{NS}}}code")
        code_system = code.get("codeSystem")

        valid_systems = ["2.16.840.1.113883.6.1", "2.16.840.1.113883.6.96"]
        assert code_system in valid_systems, (
            f"Code system should be LOINC or SNOMED, got: {code_system}"
        )

    def test_conf_1098_30432_act_status_code_required(self):
        """
        CONF:1098-30432: SHALL contain exactly one [1..1] statusCode.

        The planned act must have a statusCode element.
        """
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        status_codes = act.findall(f"{{{NS}}}statusCode")
        assert len(status_codes) == 1, "Planned act must have exactly one statusCode"

    def test_conf_1098_32019_act_status_code_active(self):
        """
        CONF:1098-32019: This statusCode SHALL contain exactly one [1..1] @code="active".

        The planned act statusCode must be "active".
        """
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        status = act.find(f"{{{NS}}}statusCode")
        assert status.get("code") == "active"

    def test_conf_1098_30433_act_effective_time_should(self):
        """
        CONF:1098-30433: SHOULD contain zero or one [0..1] effectiveTime.

        The planned act should contain an effectiveTime (but it's optional).
        """
        # Test with effectiveTime
        planned_act1 = MockPlannedAct()
        item1 = MockItem(planned_act=planned_act1)
        section1 = AssessmentAndPlanSection([item1])
        elem1 = section1.to_element()

        act1 = elem1.find(f".//{{{NS}}}act")
        time1 = act1.find(f"{{{NS}}}effectiveTime")
        assert time1 is not None, (
            "Planned act with effective_time should have effectiveTime element"
        )

        # Test without effectiveTime (set to None)
        planned_act1.effective_time = None
        item2 = MockItem(planned_act=planned_act1)
        section2 = AssessmentAndPlanSection([item2])
        elem2 = section2.to_element()

        act2 = elem2.find(f".//{{{NS}}}act")
        time2 = act2.find(f"{{{NS}}}effectiveTime")
        assert time2 is None, (
            "Planned act without effective_time should not have effectiveTime element"
        )

    def test_conf_1098_32024_instruction_entry_relationship(self):
        """
        CONF:1098-32024: MAY contain zero or more [0..*] entryRelationship.

        The planned act may contain entryRelationship for instructions.
        """
        # With instructions
        planned_act1 = MockPlannedAct()
        item1 = MockItem(planned_act=planned_act1)
        section1 = AssessmentAndPlanSection([item1])
        elem1 = section1.to_element()

        act1 = elem1.find(f".//{{{NS}}}act")
        entry_rel1 = act1.find(f"{{{NS}}}entryRelationship[@typeCode='SUBJ']")
        assert entry_rel1 is not None, "Planned act with instructions should have entryRelationship"

        # Without instructions
        planned_act1.instructions = None
        item2 = MockItem(planned_act=planned_act1)
        section2 = AssessmentAndPlanSection([item2])
        elem2 = section2.to_element()

        act2 = elem2.find(f".//{{{NS}}}act")
        entry_rel2 = act2.find(f"{{{NS}}}entryRelationship[@typeCode='SUBJ']")
        assert entry_rel2 is None, (
            "Planned act without instructions should not have entryRelationship"
        )

    def test_conf_1098_32025_instruction_type_code(self):
        """
        CONF:1098-32025: SHALL contain exactly one [1..1] @typeCode="SUBJ".

        If instruction entryRelationship is present, it must have typeCode="SUBJ".
        """
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        if entry_rel is not None:
            assert entry_rel.get("typeCode") == "SUBJ"

    def test_conf_1098_32026_instruction_template(self):
        """
        CONF:1098-32026: SHALL contain exactly one [1..1] Instruction (V2).

        If instruction entryRelationship is present, it must contain Instruction template.
        """
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship[@typeCode='SUBJ']")
        if entry_rel is not None:
            instruction_act = entry_rel.find(f"{{{NS}}}act")
            assert instruction_act is not None

            # Check for Instruction (V2) template
            template = instruction_act.find(
                f"{{{NS}}}templateId[@root='2.16.840.1.113883.10.20.22.4.20']"
            )
            assert template is not None, "Instruction must have Instruction (V2) template"

    # Version Compatibility Tests

    def test_r20_and_r21_compatibility(self):
        """Test that R2.0 and R2.1 use the same template version."""
        section_r20 = AssessmentAndPlanSection(version=CDAVersion.R2_0)
        section_r21 = AssessmentAndPlanSection(version=CDAVersion.R2_1)

        elem_r20 = section_r20.to_element()
        elem_r21 = section_r21.to_element()

        template_r20 = elem_r20.find(f"{{{NS}}}templateId")
        template_r21 = elem_r21.find(f"{{{NS}}}templateId")

        # Both should use the same template
        assert template_r20.get("root") == template_r21.get("root")
        assert template_r20.get("extension") == template_r21.get("extension")

    # Structural Tests

    def test_all_required_elements_present(self):
        """Test that all required elements are present in correct order."""
        planned_act = MockPlannedAct()
        item = MockItem(planned_act=planned_act)
        section = AssessmentAndPlanSection([item])
        elem = section.to_element()

        # Required elements in order
        required_elements = ["templateId", "code", "title", "text"]

        children = list(elem)
        child_names = [etree.QName(c).localname for c in children]

        for req_elem in required_elements:
            assert req_elem in child_names, f"Required element '{req_elem}' not found"

        # Check order (templateId before code before title before text)
        template_idx = child_names.index("templateId")
        code_idx = child_names.index("code")
        title_idx = child_names.index("title")
        text_idx = child_names.index("text")

        assert template_idx < code_idx < title_idx < text_idx, "Elements not in correct order"

    def test_narrative_text_not_empty(self):
        """Test that narrative text is never empty."""
        # Empty items list
        section1 = AssessmentAndPlanSection([])
        elem1 = section1.to_element()
        text1 = elem1.find(f"{{{NS}}}text")
        assert len(list(text1)) > 0, "Text element should not be empty"

        # With items
        item = MockItem()
        section2 = AssessmentAndPlanSection([item])
        elem2 = section2.to_element()
        text2 = elem2.find(f"{{{NS}}}text")
        assert len(list(text2)) > 0, "Text element should not be empty"
