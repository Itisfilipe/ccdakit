"""Tests for health status evaluation and outcome protocols."""

from datetime import date, datetime
from typing import Optional, Sequence

from ccdakit.protocols.health_status_evaluation import (
    OutcomeObservationProtocol,
    ProgressTowardGoalProtocol,
)


class MockProgressTowardGoal:
    """Test implementation of ProgressTowardGoalProtocol."""

    def __init__(
        self,
        id: str = "progress-001",
        achievement_code: str = "385641008",
        achievement_code_system: Optional[str] = "2.16.840.1.113883.6.96",
        achievement_display_name: Optional[str] = "Improving",
    ):
        self._id = id
        self._achievement_code = achievement_code
        self._achievement_code_system = achievement_code_system
        self._achievement_display_name = achievement_display_name

    @property
    def id(self) -> str:
        return self._id

    @property
    def achievement_code(self) -> str:
        return self._achievement_code

    @property
    def achievement_code_system(self) -> Optional[str]:
        return self._achievement_code_system

    @property
    def achievement_display_name(self) -> Optional[str]:
        return self._achievement_display_name


class MockOutcomeObservation:
    """Test implementation of OutcomeObservationProtocol."""

    def __init__(
        self,
        id: str = "outcome-001",
        code: str = "29463-7",
        code_system: Optional[str] = "LOINC",
        display_name: Optional[str] = "Body weight",
        value: Optional[str] = "85",
        value_unit: Optional[str] = "kg",
        effective_time: Optional[date] = None,
        progress_toward_goal: Optional[ProgressTowardGoalProtocol] = None,
        goal_reference_id: Optional[str] = None,
        intervention_reference_ids: Optional[Sequence[str]] = None,
        author_name: Optional[str] = None,
        author_time: Optional[datetime] = None,
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
    def id(self) -> str:
        return self._id

    @property
    def code(self) -> str:
        return self._code

    @property
    def code_system(self) -> Optional[str]:
        return self._code_system

    @property
    def display_name(self) -> Optional[str]:
        return self._display_name

    @property
    def value(self) -> Optional[str]:
        return self._value

    @property
    def value_unit(self) -> Optional[str]:
        return self._value_unit

    @property
    def effective_time(self) -> Optional[date]:
        return self._effective_time

    @property
    def progress_toward_goal(self) -> Optional[ProgressTowardGoalProtocol]:
        return self._progress_toward_goal

    @property
    def goal_reference_id(self) -> Optional[str]:
        return self._goal_reference_id

    @property
    def intervention_reference_ids(self) -> Optional[Sequence[str]]:
        return self._intervention_reference_ids

    @property
    def author_name(self) -> Optional[str]:
        return self._author_name

    @property
    def author_time(self) -> Optional[datetime]:
        return self._author_time


def test_progress_toward_goal_protocol_properties():
    """Test ProgressTowardGoalProtocol properties."""
    progress = MockProgressTowardGoal()

    assert progress.id == "progress-001"
    assert progress.achievement_code == "385641008"
    assert progress.achievement_code_system == "2.16.840.1.113883.6.96"
    assert progress.achievement_display_name == "Improving"


def test_progress_toward_goal_protocol_satisfaction():
    """Test that MockProgressTowardGoal satisfies ProgressTowardGoalProtocol."""
    progress = MockProgressTowardGoal()

    def accepts_progress(p: ProgressTowardGoalProtocol) -> str:
        return f"{p.id}: {p.achievement_code}"

    result = accepts_progress(progress)
    assert result == "progress-001: 385641008"


def test_progress_toward_goal_with_snomed_code():
    """Test progress with SNOMED CT achievement code."""
    progress = MockProgressTowardGoal(
        id="progress-snomed",
        achievement_code="385641008",
        achievement_code_system="2.16.840.1.113883.6.96",
        achievement_display_name="Improving",
    )

    assert progress.achievement_code == "385641008"
    assert progress.achievement_code_system == "2.16.840.1.113883.6.96"


def test_progress_toward_goal_minimal():
    """Test progress with minimal fields."""
    progress = MockProgressTowardGoal(
        id="progress-minimal",
        achievement_code="ASSERTION",
        achievement_code_system=None,
        achievement_display_name=None,
    )

    assert progress.id == "progress-minimal"
    assert progress.achievement_code == "ASSERTION"
    assert progress.achievement_code_system is None
    assert progress.achievement_display_name is None


def test_outcome_observation_protocol_required_fields():
    """Test OutcomeObservationProtocol required fields."""
    outcome = MockOutcomeObservation()

    assert outcome.id == "outcome-001"
    assert outcome.code == "29463-7"


def test_outcome_observation_protocol_satisfaction():
    """Test that MockOutcomeObservation satisfies OutcomeObservationProtocol."""
    outcome = MockOutcomeObservation()

    def accepts_outcome(o: OutcomeObservationProtocol) -> str:
        return f"{o.id}: {o.code}"

    result = accepts_outcome(outcome)
    assert result == "outcome-001: 29463-7"


def test_outcome_observation_with_loinc_code():
    """Test outcome observation with LOINC code."""
    outcome = MockOutcomeObservation(
        code="29463-7",
        code_system="LOINC",
        display_name="Body weight",
    )

    assert outcome.code == "29463-7"
    assert outcome.code_system == "LOINC"
    assert outcome.display_name == "Body weight"


def test_outcome_observation_with_value_and_unit():
    """Test outcome observation with value and unit."""
    outcome = MockOutcomeObservation(
        code="29463-7",
        value="85",
        value_unit="kg",
    )

    assert outcome.value == "85"
    assert outcome.value_unit == "kg"


def test_outcome_observation_without_value():
    """Test outcome observation without value."""
    outcome = MockOutcomeObservation(
        code="29463-7",
        value=None,
        value_unit=None,
    )

    assert outcome.value is None
    assert outcome.value_unit is None


def test_outcome_observation_with_effective_time():
    """Test outcome observation with effective time."""
    effective_date = date(2024, 3, 15)
    outcome = MockOutcomeObservation(
        effective_time=effective_date,
    )

    assert outcome.effective_time == effective_date


def test_outcome_observation_with_progress_toward_goal():
    """Test outcome observation with progress toward goal."""
    progress = MockProgressTowardGoal(
        id="progress-123",
        achievement_code="385641008",
        achievement_display_name="Improving",
    )
    outcome = MockOutcomeObservation(
        progress_toward_goal=progress,
    )

    assert outcome.progress_toward_goal is not None
    assert outcome.progress_toward_goal.id == "progress-123"
    assert outcome.progress_toward_goal.achievement_code == "385641008"


def test_outcome_observation_without_progress_toward_goal():
    """Test outcome observation without progress toward goal."""
    outcome = MockOutcomeObservation(
        progress_toward_goal=None,
    )

    assert outcome.progress_toward_goal is None


def test_outcome_observation_with_goal_reference():
    """Test outcome observation with goal reference."""
    outcome = MockOutcomeObservation(
        goal_reference_id="goal-001",
    )

    assert outcome.goal_reference_id == "goal-001"


def test_outcome_observation_without_goal_reference():
    """Test outcome observation without goal reference."""
    outcome = MockOutcomeObservation(
        goal_reference_id=None,
    )

    assert outcome.goal_reference_id is None


def test_outcome_observation_with_intervention_references():
    """Test outcome observation with intervention references."""
    outcome = MockOutcomeObservation(
        intervention_reference_ids=["int-001", "int-002", "int-003"],
    )

    assert outcome.intervention_reference_ids is not None
    assert len(outcome.intervention_reference_ids) == 3
    assert "int-001" in outcome.intervention_reference_ids


def test_outcome_observation_without_intervention_references():
    """Test outcome observation without intervention references."""
    outcome = MockOutcomeObservation(
        intervention_reference_ids=None,
    )

    assert outcome.intervention_reference_ids is None


def test_outcome_observation_with_author():
    """Test outcome observation with author information."""
    author_datetime = datetime(2024, 3, 15, 10, 30, 0)
    outcome = MockOutcomeObservation(
        author_name="Dr. Jane Smith",
        author_time=author_datetime,
    )

    assert outcome.author_name == "Dr. Jane Smith"
    assert outcome.author_time == author_datetime


def test_outcome_observation_without_author():
    """Test outcome observation without author information."""
    outcome = MockOutcomeObservation(
        author_name=None,
        author_time=None,
    )

    assert outcome.author_name is None
    assert outcome.author_time is None


def test_outcome_observation_body_weight_scenario():
    """Test complete body weight outcome scenario."""
    progress = MockProgressTowardGoal(
        id="progress-weight",
        achievement_code="385641008",
        achievement_code_system="2.16.840.1.113883.6.96",
        achievement_display_name="Improving",
    )

    outcome = MockOutcomeObservation(
        id="outcome-weight-001",
        code="29463-7",
        code_system="LOINC",
        display_name="Body weight",
        value="85",
        value_unit="kg",
        effective_time=date(2024, 3, 15),
        progress_toward_goal=progress,
        goal_reference_id="goal-weight-loss",
        intervention_reference_ids=["int-diet", "int-exercise"],
        author_name="Dr. Smith",
        author_time=datetime(2024, 3, 15, 14, 30, 0),
    )

    assert outcome.id == "outcome-weight-001"
    assert outcome.code == "29463-7"
    assert outcome.display_name == "Body weight"
    assert outcome.value == "85"
    assert outcome.value_unit == "kg"
    assert outcome.progress_toward_goal is not None
    assert outcome.goal_reference_id == "goal-weight-loss"
    assert len(outcome.intervention_reference_ids) == 2


def test_outcome_observation_heart_rate_scenario():
    """Test heart rate outcome scenario."""
    outcome = MockOutcomeObservation(
        id="outcome-hr-001",
        code="8867-4",
        code_system="LOINC",
        display_name="Heart rate",
        value="72",
        value_unit="beats/min",
        effective_time=date(2024, 3, 15),
    )

    assert outcome.code == "8867-4"
    assert outcome.display_name == "Heart rate"
    assert outcome.value == "72"
    assert outcome.value_unit == "beats/min"


def test_outcome_observation_glucose_scenario():
    """Test glucose outcome scenario."""
    outcome = MockOutcomeObservation(
        id="outcome-glucose-001",
        code="2339-0",
        code_system="LOINC",
        display_name="Glucose [Mass/volume] in Blood",
        value="110",
        value_unit="mg/dL",
        effective_time=date(2024, 3, 15),
    )

    assert outcome.code == "2339-0"
    assert outcome.display_name == "Glucose [Mass/volume] in Blood"
    assert outcome.value == "110"
    assert outcome.value_unit == "mg/dL"


class MinimalOutcomeObservation:
    """Minimal implementation with only required fields."""

    @property
    def id(self) -> str:
        return "minimal-outcome"

    @property
    def code(self) -> str:
        return "29463-7"

    @property
    def code_system(self) -> Optional[str]:
        return None

    @property
    def display_name(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[str]:
        return None

    @property
    def value_unit(self) -> Optional[str]:
        return None

    @property
    def effective_time(self) -> Optional[date]:
        return None

    @property
    def progress_toward_goal(self) -> Optional[ProgressTowardGoalProtocol]:
        return None

    @property
    def goal_reference_id(self) -> Optional[str]:
        return None

    @property
    def intervention_reference_ids(self) -> Optional[Sequence[str]]:
        return None

    @property
    def author_name(self) -> Optional[str]:
        return None

    @property
    def author_time(self) -> Optional[datetime]:
        return None


def test_minimal_outcome_observation_protocol():
    """Test that minimal implementation satisfies OutcomeObservationProtocol."""
    outcome = MinimalOutcomeObservation()

    assert outcome.id == "minimal-outcome"
    assert outcome.code == "29463-7"
    assert outcome.code_system is None
    assert outcome.display_name is None
    assert outcome.value is None
    assert outcome.value_unit is None
    assert outcome.effective_time is None
    assert outcome.progress_toward_goal is None
    assert outcome.goal_reference_id is None
    assert outcome.intervention_reference_ids is None
    assert outcome.author_name is None
    assert outcome.author_time is None


def test_minimal_outcome_observation_satisfaction():
    """Test that MinimalOutcomeObservation satisfies OutcomeObservationProtocol."""
    outcome = MinimalOutcomeObservation()

    def accepts_outcome(o: OutcomeObservationProtocol) -> str:
        return o.id

    result = accepts_outcome(outcome)
    assert result == "minimal-outcome"


def test_outcome_observation_with_snomed_code():
    """Test outcome observation with SNOMED CT code."""
    outcome = MockOutcomeObservation(
        code="386725007",
        code_system="SNOMED",
        display_name="Body temperature",
        value="98.6",
        value_unit="degF",
    )

    assert outcome.code_system == "SNOMED"
    assert outcome.code == "386725007"


def test_outcome_observation_multiple_interventions():
    """Test outcome observation linked to multiple interventions."""
    outcome = MockOutcomeObservation(
        intervention_reference_ids=[
            "intervention-med-001",
            "intervention-exercise-001",
            "intervention-diet-001",
            "intervention-counseling-001",
        ],
    )

    assert outcome.intervention_reference_ids is not None
    assert len(outcome.intervention_reference_ids) == 4


def test_outcome_observation_empty_intervention_list():
    """Test outcome observation with empty intervention list."""
    outcome = MockOutcomeObservation(
        intervention_reference_ids=[],
    )

    assert outcome.intervention_reference_ids is not None
    assert len(outcome.intervention_reference_ids) == 0


def test_progress_toward_goal_different_achievement_codes():
    """Test progress toward goal with different achievement codes."""
    improving = MockProgressTowardGoal(
        achievement_code="385641008",
        achievement_display_name="Improving",
    )
    worsening = MockProgressTowardGoal(
        achievement_code="385642001",
        achievement_display_name="Worsening",
    )
    unchanged = MockProgressTowardGoal(
        achievement_code="385643006",
        achievement_display_name="No change",
    )

    assert improving.achievement_code == "385641008"
    assert worsening.achievement_code == "385642001"
    assert unchanged.achievement_code == "385643006"


def test_outcome_observation_complex_scenario():
    """Test complex outcome observation with all optional fields."""
    progress = MockProgressTowardGoal(
        id="complex-progress",
        achievement_code="385641008",
        achievement_code_system="2.16.840.1.113883.6.96",
        achievement_display_name="Improving",
    )

    outcome = MockOutcomeObservation(
        id="complex-outcome",
        code="2339-0",
        code_system="LOINC",
        display_name="Glucose [Mass/volume] in Blood",
        value="105",
        value_unit="mg/dL",
        effective_time=date(2024, 3, 20),
        progress_toward_goal=progress,
        goal_reference_id="goal-glucose-control",
        intervention_reference_ids=["int-metformin", "int-diet", "int-exercise"],
        author_name="Dr. Johnson",
        author_time=datetime(2024, 3, 20, 9, 15, 30),
    )

    assert outcome.id == "complex-outcome"
    assert outcome.code == "2339-0"
    assert outcome.value == "105"
    assert outcome.progress_toward_goal.achievement_display_name == "Improving"
    assert outcome.goal_reference_id == "goal-glucose-control"
    assert len(outcome.intervention_reference_ids) == 3
    assert outcome.author_name == "Dr. Johnson"
    assert outcome.author_time.hour == 9
