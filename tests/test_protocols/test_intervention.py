"""Tests for intervention protocols."""

from datetime import date, datetime
from typing import Optional, Union

from ccdakit.protocols.intervention import (
    InterventionActivityProtocol,
    InterventionProtocol,
    PlannedInterventionProtocol,
)


class MockIntervention:
    """Test implementation of InterventionProtocol."""

    def __init__(
        self,
        id: str = "int-001",
        description: str = "Medication counseling session",
        effective_time: Optional[Union[date, datetime]] = None,
        status: str = "completed",
        intervention_type: Optional[str] = None,
        goal_reference_id: Optional[str] = None,
        author: Optional[str] = None,
    ):
        self._id = id
        self._description = description
        self._effective_time = effective_time
        self._status = status
        self._intervention_type = intervention_type
        self._goal_reference_id = goal_reference_id
        self._author = author

    @property
    def id(self) -> str:
        return self._id

    @property
    def description(self) -> str:
        return self._description

    @property
    def effective_time(self) -> Optional[Union[date, datetime]]:
        return self._effective_time

    @property
    def status(self) -> str:
        return self._status

    @property
    def intervention_type(self) -> Optional[str]:
        return self._intervention_type

    @property
    def goal_reference_id(self) -> Optional[str]:
        return self._goal_reference_id

    @property
    def author(self) -> Optional[str]:
        return self._author


class MockPlannedIntervention:
    """Test implementation of PlannedInterventionProtocol."""

    def __init__(
        self,
        id: str = "planned-int-001",
        description: str = "Planned exercise program",
        mood_code: str = "INT",
        effective_time: Optional[Union[date, datetime]] = None,
        status: str = "active",
        intervention_type: Optional[str] = None,
        goal_reference_id: str = "goal-001",
        author: Optional[str] = None,
    ):
        self._id = id
        self._description = description
        self._mood_code = mood_code
        self._effective_time = effective_time
        self._status = status
        self._intervention_type = intervention_type
        self._goal_reference_id = goal_reference_id
        self._author = author

    @property
    def id(self) -> str:
        return self._id

    @property
    def description(self) -> str:
        return self._description

    @property
    def mood_code(self) -> str:
        return self._mood_code

    @property
    def effective_time(self) -> Optional[Union[date, datetime]]:
        return self._effective_time

    @property
    def status(self) -> str:
        return self._status

    @property
    def intervention_type(self) -> Optional[str]:
        return self._intervention_type

    @property
    def goal_reference_id(self) -> str:
        return self._goal_reference_id

    @property
    def author(self) -> Optional[str]:
        return self._author


class MockInterventionActivity:
    """Test implementation of InterventionActivityProtocol."""

    def __init__(
        self,
        id: str = "activity-001",
        description: str = "Metformin 500mg",
        code: Optional[str] = None,
        code_system: Optional[str] = None,
        display_name: Optional[str] = None,
    ):
        self._id = id
        self._description = description
        self._code = code
        self._code_system = code_system
        self._display_name = display_name

    @property
    def id(self) -> str:
        return self._id

    @property
    def description(self) -> str:
        return self._description

    @property
    def code(self) -> Optional[str]:
        return self._code

    @property
    def code_system(self) -> Optional[str]:
        return self._code_system

    @property
    def display_name(self) -> Optional[str]:
        return self._display_name


def test_intervention_protocol_required_fields():
    """Test InterventionProtocol required fields."""
    intervention = MockIntervention()

    assert intervention.id == "int-001"
    assert intervention.description == "Medication counseling session"
    assert intervention.status == "completed"


def test_intervention_protocol_satisfaction():
    """Test that MockIntervention satisfies InterventionProtocol."""
    intervention = MockIntervention()

    def accepts_intervention(i: InterventionProtocol) -> str:
        return f"{i.id}: {i.description}"

    result = accepts_intervention(intervention)
    assert result == "int-001: Medication counseling session"


def test_intervention_with_date():
    """Test intervention with date effective time."""
    intervention = MockIntervention(
        effective_time=date(2024, 3, 15),
    )

    assert intervention.effective_time == date(2024, 3, 15)
    assert isinstance(intervention.effective_time, date)


def test_intervention_with_datetime():
    """Test intervention with datetime effective time."""
    intervention = MockIntervention(
        effective_time=datetime(2024, 3, 15, 14, 30, 0),
    )

    assert intervention.effective_time == datetime(2024, 3, 15, 14, 30, 0)
    assert isinstance(intervention.effective_time, datetime)


def test_intervention_without_effective_time():
    """Test intervention without effective time."""
    intervention = MockIntervention(
        effective_time=None,
    )

    assert intervention.effective_time is None


def test_intervention_with_type():
    """Test intervention with intervention type."""
    medication = MockIntervention(intervention_type="medication")
    procedure = MockIntervention(intervention_type="procedure")
    instruction = MockIntervention(intervention_type="instruction")
    encounter = MockIntervention(intervention_type="encounter")

    assert medication.intervention_type == "medication"
    assert procedure.intervention_type == "procedure"
    assert instruction.intervention_type == "instruction"
    assert encounter.intervention_type == "encounter"


def test_intervention_without_type():
    """Test intervention without intervention type."""
    intervention = MockIntervention(intervention_type=None)

    assert intervention.intervention_type is None


def test_intervention_with_goal_reference():
    """Test intervention with goal reference."""
    intervention = MockIntervention(
        goal_reference_id="goal-weight-loss",
    )

    assert intervention.goal_reference_id == "goal-weight-loss"


def test_intervention_without_goal_reference():
    """Test intervention without goal reference."""
    intervention = MockIntervention(goal_reference_id=None)

    assert intervention.goal_reference_id is None


def test_intervention_with_author():
    """Test intervention with author."""
    intervention = MockIntervention(
        author="Dr. Jane Smith",
    )

    assert intervention.author == "Dr. Jane Smith"


def test_intervention_without_author():
    """Test intervention without author."""
    intervention = MockIntervention(author=None)

    assert intervention.author is None


def test_intervention_completed_status():
    """Test intervention with completed status."""
    intervention = MockIntervention(status="completed")

    assert intervention.status == "completed"


def test_intervention_complex_scenario():
    """Test complex intervention with all fields."""
    intervention = MockIntervention(
        id="int-complex",
        description="Comprehensive diabetes management intervention",
        effective_time=datetime(2024, 3, 15, 10, 0, 0),
        status="completed",
        intervention_type="medication",
        goal_reference_id="goal-glucose-control",
        author="Dr. Johnson",
    )

    assert intervention.id == "int-complex"
    assert intervention.description == "Comprehensive diabetes management intervention"
    assert intervention.effective_time == datetime(2024, 3, 15, 10, 0, 0)
    assert intervention.status == "completed"
    assert intervention.intervention_type == "medication"
    assert intervention.goal_reference_id == "goal-glucose-control"
    assert intervention.author == "Dr. Johnson"


def test_planned_intervention_protocol_required_fields():
    """Test PlannedInterventionProtocol required fields."""
    planned = MockPlannedIntervention()

    assert planned.id == "planned-int-001"
    assert planned.description == "Planned exercise program"
    assert planned.mood_code == "INT"
    assert planned.status == "active"
    assert planned.goal_reference_id == "goal-001"


def test_planned_intervention_protocol_satisfaction():
    """Test that MockPlannedIntervention satisfies PlannedInterventionProtocol."""
    planned = MockPlannedIntervention()

    def accepts_planned(p: PlannedInterventionProtocol) -> str:
        return f"{p.id}: {p.mood_code}"

    result = accepts_planned(planned)
    assert result == "planned-int-001: INT"


def test_planned_intervention_mood_codes():
    """Test planned intervention with different mood codes."""
    int_mood = MockPlannedIntervention(mood_code="INT")
    arq_mood = MockPlannedIntervention(mood_code="ARQ")
    prms_mood = MockPlannedIntervention(mood_code="PRMS")
    prp_mood = MockPlannedIntervention(mood_code="PRP")
    rqo_mood = MockPlannedIntervention(mood_code="RQO")

    assert int_mood.mood_code == "INT"
    assert arq_mood.mood_code == "ARQ"
    assert prms_mood.mood_code == "PRMS"
    assert prp_mood.mood_code == "PRP"
    assert rqo_mood.mood_code == "RQO"


def test_planned_intervention_with_date():
    """Test planned intervention with date effective time."""
    planned = MockPlannedIntervention(
        effective_time=date(2024, 4, 1),
    )

    assert planned.effective_time == date(2024, 4, 1)


def test_planned_intervention_with_datetime():
    """Test planned intervention with datetime effective time."""
    planned = MockPlannedIntervention(
        effective_time=datetime(2024, 4, 1, 9, 0, 0),
    )

    assert planned.effective_time == datetime(2024, 4, 1, 9, 0, 0)


def test_planned_intervention_without_effective_time():
    """Test planned intervention without effective time."""
    planned = MockPlannedIntervention(effective_time=None)

    assert planned.effective_time is None


def test_planned_intervention_active_status():
    """Test planned intervention with active status."""
    planned = MockPlannedIntervention(status="active")

    assert planned.status == "active"


def test_planned_intervention_with_type():
    """Test planned intervention with intervention type."""
    planned = MockPlannedIntervention(
        intervention_type="procedure",
    )

    assert planned.intervention_type == "procedure"


def test_planned_intervention_without_type():
    """Test planned intervention without intervention type."""
    planned = MockPlannedIntervention(intervention_type=None)

    assert planned.intervention_type is None


def test_planned_intervention_with_author():
    """Test planned intervention with author."""
    planned = MockPlannedIntervention(
        author="Nurse Thompson",
    )

    assert planned.author == "Nurse Thompson"


def test_planned_intervention_without_author():
    """Test planned intervention without author."""
    planned = MockPlannedIntervention(author=None)

    assert planned.author is None


def test_planned_intervention_complex_scenario():
    """Test complex planned intervention with all fields."""
    planned = MockPlannedIntervention(
        id="planned-complex",
        description="Planned cardiac rehabilitation program",
        mood_code="INT",
        effective_time=date(2024, 5, 1),
        status="active",
        intervention_type="procedure",
        goal_reference_id="goal-cardiac-health",
        author="Dr. Williams",
    )

    assert planned.id == "planned-complex"
    assert planned.description == "Planned cardiac rehabilitation program"
    assert planned.mood_code == "INT"
    assert planned.effective_time == date(2024, 5, 1)
    assert planned.status == "active"
    assert planned.intervention_type == "procedure"
    assert planned.goal_reference_id == "goal-cardiac-health"
    assert planned.author == "Dr. Williams"


def test_intervention_activity_protocol_required_fields():
    """Test InterventionActivityProtocol required fields."""
    activity = MockInterventionActivity()

    assert activity.id == "activity-001"
    assert activity.description == "Metformin 500mg"


def test_intervention_activity_protocol_satisfaction():
    """Test that MockInterventionActivity satisfies InterventionActivityProtocol."""
    activity = MockInterventionActivity()

    def accepts_activity(a: InterventionActivityProtocol) -> str:
        return f"{a.id}: {a.description}"

    result = accepts_activity(activity)
    assert result == "activity-001: Metformin 500mg"


def test_intervention_activity_with_code():
    """Test intervention activity with code."""
    activity = MockInterventionActivity(
        code="860975",
        code_system="RxNorm",
        display_name="Metformin 500 MG Oral Tablet",
    )

    assert activity.code == "860975"
    assert activity.code_system == "RxNorm"
    assert activity.display_name == "Metformin 500 MG Oral Tablet"


def test_intervention_activity_without_code():
    """Test intervention activity without code."""
    activity = MockInterventionActivity(
        code=None,
        code_system=None,
        display_name=None,
    )

    assert activity.code is None
    assert activity.code_system is None
    assert activity.display_name is None


def test_intervention_activity_procedure():
    """Test intervention activity for procedure."""
    activity = MockInterventionActivity(
        id="procedure-001",
        description="Blood glucose monitoring",
        code="33747003",
        code_system="SNOMED",
        display_name="Blood glucose monitoring",
    )

    assert activity.id == "procedure-001"
    assert activity.description == "Blood glucose monitoring"
    assert activity.code_system == "SNOMED"


class MinimalIntervention:
    """Minimal implementation with only required fields."""

    @property
    def id(self) -> str:
        return "minimal-int"

    @property
    def description(self) -> str:
        return "Minimal intervention"

    @property
    def effective_time(self) -> Optional[Union[date, datetime]]:
        return None

    @property
    def status(self) -> str:
        return "completed"

    @property
    def intervention_type(self) -> Optional[str]:
        return None

    @property
    def goal_reference_id(self) -> Optional[str]:
        return None

    @property
    def author(self) -> Optional[str]:
        return None


def test_minimal_intervention_protocol():
    """Test that minimal implementation satisfies InterventionProtocol."""
    intervention = MinimalIntervention()

    assert intervention.id == "minimal-int"
    assert intervention.description == "Minimal intervention"
    assert intervention.status == "completed"
    assert intervention.effective_time is None
    assert intervention.intervention_type is None
    assert intervention.goal_reference_id is None
    assert intervention.author is None


class MinimalPlannedIntervention:
    """Minimal implementation with only required fields."""

    @property
    def id(self) -> str:
        return "minimal-planned"

    @property
    def description(self) -> str:
        return "Minimal planned intervention"

    @property
    def mood_code(self) -> str:
        return "INT"

    @property
    def effective_time(self) -> Optional[Union[date, datetime]]:
        return None

    @property
    def status(self) -> str:
        return "active"

    @property
    def intervention_type(self) -> Optional[str]:
        return None

    @property
    def goal_reference_id(self) -> str:
        return "goal-minimal"

    @property
    def author(self) -> Optional[str]:
        return None


def test_minimal_planned_intervention_protocol():
    """Test that minimal implementation satisfies PlannedInterventionProtocol."""
    planned = MinimalPlannedIntervention()

    assert planned.id == "minimal-planned"
    assert planned.description == "Minimal planned intervention"
    assert planned.mood_code == "INT"
    assert planned.status == "active"
    assert planned.goal_reference_id == "goal-minimal"
    assert planned.effective_time is None
    assert planned.intervention_type is None
    assert planned.author is None


class MinimalInterventionActivity:
    """Minimal implementation with only required fields."""

    @property
    def id(self) -> str:
        return "minimal-activity"

    @property
    def description(self) -> str:
        return "Minimal activity"

    @property
    def code(self) -> Optional[str]:
        return None

    @property
    def code_system(self) -> Optional[str]:
        return None

    @property
    def display_name(self) -> Optional[str]:
        return None


def test_minimal_intervention_activity_protocol():
    """Test that minimal implementation satisfies InterventionActivityProtocol."""
    activity = MinimalInterventionActivity()

    assert activity.id == "minimal-activity"
    assert activity.description == "Minimal activity"
    assert activity.code is None
    assert activity.code_system is None
    assert activity.display_name is None


def test_intervention_property_access_multiple_times():
    """Test that properties can be accessed multiple times consistently."""
    intervention = MockIntervention()

    assert intervention.id == intervention.id
    assert intervention.description == intervention.description
    assert intervention.status == intervention.status
    assert intervention.effective_time == intervention.effective_time
    assert intervention.intervention_type == intervention.intervention_type
    assert intervention.goal_reference_id == intervention.goal_reference_id
    assert intervention.author == intervention.author


def test_planned_intervention_property_access_multiple_times():
    """Test that planned intervention properties can be accessed multiple times."""
    planned = MockPlannedIntervention()

    assert planned.id == planned.id
    assert planned.description == planned.description
    assert planned.mood_code == planned.mood_code
    assert planned.status == planned.status
    assert planned.effective_time == planned.effective_time
    assert planned.intervention_type == planned.intervention_type
    assert planned.goal_reference_id == planned.goal_reference_id
    assert planned.author == planned.author


def test_intervention_activity_property_access_multiple_times():
    """Test that activity properties can be accessed multiple times."""
    activity = MockInterventionActivity()

    assert activity.id == activity.id
    assert activity.description == activity.description
    assert activity.code == activity.code
    assert activity.code_system == activity.code_system
    assert activity.display_name == activity.display_name
