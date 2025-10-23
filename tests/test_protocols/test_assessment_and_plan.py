"""Tests for assessment and plan protocols."""

from datetime import datetime
from typing import Optional

from ccdakit.protocols.assessment_and_plan import (
    AssessmentAndPlanItemProtocol,
    PlannedActProtocol,
)


class MockPlannedAct:
    """Test implementation of PlannedActProtocol."""

    def __init__(
        self,
        id_root: str = "2.16.840.1.113883.3.TEST",
        id_extension: str = "PLAN-001",
        code: str = "386053000",
        code_system: str = "SNOMED",
        display_name: str = "Patient education",
        mood_code: str = "INT",
        effective_time: Optional[datetime] = None,
        instructions: Optional[str] = None,
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
    """Test implementation of AssessmentAndPlanItemProtocol."""

    def __init__(
        self,
        text: str = "Patient has stable Type 2 Diabetes",
        item_type: str = "assessment",
        planned_act: Optional[PlannedActProtocol] = None,
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


def test_planned_act_protocol_required_fields():
    """Test PlannedActProtocol required fields."""
    act = MockPlannedAct()

    assert act.id_root == "2.16.840.1.113883.3.TEST"
    assert act.id_extension == "PLAN-001"
    assert act.code == "386053000"
    assert act.code_system == "SNOMED"
    assert act.display_name == "Patient education"
    assert act.mood_code == "INT"


def test_planned_act_protocol_with_effective_time():
    """Test PlannedActProtocol with effective time."""
    effective = datetime(2024, 1, 15, 10, 0, 0)
    act = MockPlannedAct(effective_time=effective)

    assert act.effective_time == effective


def test_planned_act_protocol_with_instructions():
    """Test PlannedActProtocol with instructions."""
    act = MockPlannedAct(
        instructions="Teach patient about diabetes self-management"
    )

    assert act.instructions == "Teach patient about diabetes self-management"


def test_planned_act_protocol_satisfaction():
    """Test that MockPlannedAct satisfies PlannedActProtocol."""
    act = MockPlannedAct()

    def accepts_act(a: PlannedActProtocol) -> str:
        return f"{a.display_name} ({a.mood_code})"

    result = accepts_act(act)
    assert result == "Patient education (INT)"


def test_planned_act_mood_code_int():
    """Test planned act with mood code INT (intent)."""
    act = MockPlannedAct(mood_code="INT")

    assert act.mood_code == "INT"


def test_planned_act_mood_code_rqo():
    """Test planned act with mood code RQO (request)."""
    act = MockPlannedAct(mood_code="RQO")

    assert act.mood_code == "RQO"


def test_planned_act_mood_code_prms():
    """Test planned act with mood code PRMS (promise)."""
    act = MockPlannedAct(mood_code="PRMS")

    assert act.mood_code == "PRMS"


def test_planned_act_mood_code_prp():
    """Test planned act with mood code PRP (proposal)."""
    act = MockPlannedAct(mood_code="PRP")

    assert act.mood_code == "PRP"


def test_planned_act_with_loinc_code():
    """Test planned act with LOINC code."""
    act = MockPlannedAct(
        code="34104-0",
        code_system="LOINC",
        display_name="Patient education note",
    )

    assert act.code == "34104-0"
    assert act.code_system == "LOINC"


def test_planned_act_with_snomed_code():
    """Test planned act with SNOMED code."""
    act = MockPlannedAct(
        code="386053000",
        code_system="SNOMED",
        display_name="Evaluation procedure",
    )

    assert act.code == "386053000"
    assert act.code_system == "SNOMED"


def test_assessment_and_plan_item_protocol_required_fields():
    """Test AssessmentAndPlanItemProtocol required fields."""
    item = MockAssessmentAndPlanItem()

    assert item.text == "Patient has stable Type 2 Diabetes"
    assert item.item_type == "assessment"


def test_assessment_and_plan_item_protocol_satisfaction():
    """Test that MockAssessmentAndPlanItem satisfies AssessmentAndPlanItemProtocol."""
    item = MockAssessmentAndPlanItem()

    def accepts_item(i: AssessmentAndPlanItemProtocol) -> str:
        return f"{i.item_type}: {i.text}"

    result = accepts_item(item)
    assert result == "assessment: Patient has stable Type 2 Diabetes"


def test_assessment_item():
    """Test assessment item."""
    item = MockAssessmentAndPlanItem(
        text="Patient has stable Type 2 Diabetes",
        item_type="assessment",
    )

    assert item.item_type == "assessment"
    assert item.text == "Patient has stable Type 2 Diabetes"


def test_plan_item():
    """Test plan item."""
    item = MockAssessmentAndPlanItem(
        text="Continue metformin 1000mg twice daily",
        item_type="plan",
    )

    assert item.item_type == "plan"
    assert item.text == "Continue metformin 1000mg twice daily"


def test_plan_item_with_planned_act():
    """Test plan item with associated planned act."""
    act = MockPlannedAct(
        display_name="Patient education",
        instructions="Teach patient about foot care",
    )
    item = MockAssessmentAndPlanItem(
        text="Provide diabetes education",
        item_type="plan",
        planned_act=act,
    )

    assert item.planned_act is not None
    assert item.planned_act.display_name == "Patient education"
    assert item.planned_act.instructions == "Teach patient about foot care"


def test_assessment_item_without_planned_act():
    """Test assessment item without planned act."""
    item = MockAssessmentAndPlanItem(
        text="Blood pressure elevated",
        item_type="assessment",
        planned_act=None,
    )

    assert item.planned_act is None


class MinimalPlannedAct:
    """Minimal implementation with only required fields."""

    @property
    def id_root(self):
        return "2.16.840.1.113883.3.TEST"

    @property
    def id_extension(self):
        return "ACT-001"

    @property
    def code(self):
        return "410155007"

    @property
    def code_system(self):
        return "SNOMED"

    @property
    def display_name(self):
        return "Dressing change"

    @property
    def mood_code(self):
        return "INT"

    @property
    def effective_time(self):
        return None

    @property
    def instructions(self):
        return None


def test_minimal_planned_act_protocol():
    """Test that minimal implementation satisfies PlannedActProtocol."""
    act = MinimalPlannedAct()

    assert act.id_root == "2.16.840.1.113883.3.TEST"
    assert act.id_extension == "ACT-001"
    assert act.code == "410155007"
    assert act.code_system == "SNOMED"
    assert act.display_name == "Dressing change"
    assert act.mood_code == "INT"
    assert act.effective_time is None
    assert act.instructions is None


class MinimalAssessmentAndPlanItem:
    """Minimal implementation with only required fields."""

    @property
    def text(self):
        return "Wound healing well"

    @property
    def item_type(self):
        return "assessment"

    @property
    def planned_act(self):
        return None


def test_minimal_assessment_and_plan_item_protocol():
    """Test that minimal implementation satisfies AssessmentAndPlanItemProtocol."""
    item = MinimalAssessmentAndPlanItem()

    assert item.text == "Wound healing well"
    assert item.item_type == "assessment"
    assert item.planned_act is None


def test_planned_act_dressing_change():
    """Test planned act for dressing change."""
    act = MockPlannedAct(
        code="410155007",
        code_system="SNOMED",
        display_name="Dressing change",
        instructions="Change dressing daily",
    )

    assert act.display_name == "Dressing change"
    assert act.instructions == "Change dressing daily"


def test_planned_act_patient_teaching():
    """Test planned act for patient teaching."""
    act = MockPlannedAct(
        code="311401005",
        code_system="SNOMED",
        display_name="Patient education",
        instructions="Teach inhaler technique",
    )

    assert act.display_name == "Patient education"
    assert act.instructions == "Teach inhaler technique"


def test_planned_act_feeding():
    """Test planned act for feeding."""
    act = MockPlannedAct(
        code="129408000",
        code_system="SNOMED",
        display_name="Feeding assistance",
        instructions="Assist with meals three times daily",
    )

    assert act.display_name == "Feeding assistance"


def test_planned_act_comfort_measures():
    """Test planned act for comfort measures."""
    act = MockPlannedAct(
        code="385857005",
        code_system="SNOMED",
        display_name="Comfort measures",
        instructions="Position patient for comfort q2h",
    )

    assert act.display_name == "Comfort measures"


def test_assessment_and_plan_complete_example():
    """Test complete assessment and plan example."""
    act = MockPlannedAct(
        id_root="2.16.840.1.113883.3.TEST",
        id_extension="PLAN-DIABETES-001",
        code="386053000",
        code_system="SNOMED",
        display_name="Evaluation procedure",
        mood_code="INT",
        effective_time=datetime(2024, 2, 1, 9, 0, 0),
        instructions="Follow up A1C in 3 months",
    )

    item = MockAssessmentAndPlanItem(
        text="Type 2 Diabetes stable with current medication regimen",
        item_type="assessment",
        planned_act=act,
    )

    assert item.text == "Type 2 Diabetes stable with current medication regimen"
    assert item.item_type == "assessment"
    assert item.planned_act.display_name == "Evaluation procedure"
    assert item.planned_act.effective_time == datetime(2024, 2, 1, 9, 0, 0)


def test_multiple_assessment_items():
    """Test multiple assessment items."""
    assessment1 = MockAssessmentAndPlanItem(
        text="Blood pressure elevated at 145/92",
        item_type="assessment",
    )

    assessment2 = MockAssessmentAndPlanItem(
        text="HbA1c improved to 7.2% from 8.5%",
        item_type="assessment",
    )

    assert assessment1.item_type == "assessment"
    assert assessment2.item_type == "assessment"
    assert assessment1.text != assessment2.text


def test_multiple_plan_items():
    """Test multiple plan items."""
    plan1 = MockAssessmentAndPlanItem(
        text="Increase Lisinopril to 20mg daily",
        item_type="plan",
    )

    plan2 = MockAssessmentAndPlanItem(
        text="Continue Metformin 1000mg twice daily",
        item_type="plan",
    )

    assert plan1.item_type == "plan"
    assert plan2.item_type == "plan"
    assert plan1.text != plan2.text


def test_type_checking():
    """Test that protocols enforce correct types."""
    act = MockPlannedAct(
        effective_time=datetime(2024, 1, 15, 10, 0, 0)
    )
    item = MockAssessmentAndPlanItem(planned_act=act)

    assert isinstance(act.id_root, str)
    assert isinstance(act.id_extension, str)
    assert isinstance(act.code, str)
    assert isinstance(act.code_system, str)
    assert isinstance(act.display_name, str)
    assert isinstance(act.mood_code, str)
    assert isinstance(act.effective_time, datetime)
    assert isinstance(item.text, str)
    assert isinstance(item.item_type, str)


def test_protocol_interfaces():
    """Test that protocols have expected interfaces."""
    # Import to ensure coverage
    from ccdakit.protocols.assessment_and_plan import (
        AssessmentAndPlanItemProtocol,
        PlannedActProtocol,
    )

    # Verify PlannedActProtocol attributes
    assert hasattr(PlannedActProtocol, 'id_root')
    assert hasattr(PlannedActProtocol, 'code')
    assert hasattr(PlannedActProtocol, 'mood_code')
    assert hasattr(PlannedActProtocol, 'display_name')

    # Verify AssessmentAndPlanItemProtocol attributes
    assert hasattr(AssessmentAndPlanItemProtocol, 'text')
    assert hasattr(AssessmentAndPlanItemProtocol, 'item_type')
    assert hasattr(AssessmentAndPlanItemProtocol, 'planned_act')

    # Verify docstrings exist
    assert PlannedActProtocol.__doc__ is not None
    assert AssessmentAndPlanItemProtocol.__doc__ is not None
