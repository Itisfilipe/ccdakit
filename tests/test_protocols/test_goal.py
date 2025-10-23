"""Tests for goal protocols."""

from datetime import date

from ccdakit.protocols.goal import GoalProtocol


class MockGoal:
    """Test implementation of GoalProtocol."""

    def __init__(
        self,
        description: str = "Achieve target blood pressure of 120/80",
        code: str | None = None,
        code_system: str | None = None,
        display_name: str | None = None,
        status: str = "active",
        target_date: date | None = None,
        start_date: date | None = None,
        value: str | None = None,
        value_unit: str | None = None,
        author: str | None = None,
        priority: str | None = None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._display_name = display_name
        self._status = status
        self._target_date = target_date
        self._start_date = start_date
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
    def target_date(self):
        return self._target_date

    @property
    def start_date(self):
        return self._start_date

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


def test_goal_protocol_required_fields():
    """Test GoalProtocol required fields."""
    goal = MockGoal()

    assert goal.description == "Achieve target blood pressure of 120/80"
    assert goal.status == "active"


def test_goal_protocol_with_code():
    """Test GoalProtocol with LOINC code."""
    goal = MockGoal(
        description="Blood pressure goal",
        code="85354-9",
        code_system="LOINC",
        display_name="Blood pressure systolic and diastolic",
    )

    assert goal.code == "85354-9"
    assert goal.code_system == "LOINC"
    assert goal.display_name == "Blood pressure systolic and diastolic"


def test_goal_protocol_without_code():
    """Test GoalProtocol without code."""
    goal = MockGoal()

    assert goal.code is None
    assert goal.code_system is None
    assert goal.display_name is None


def test_goal_protocol_with_target_date():
    """Test GoalProtocol with target date."""
    target = date(2025, 6, 1)
    goal = MockGoal(target_date=target)

    assert goal.target_date == target


def test_goal_protocol_with_start_date():
    """Test GoalProtocol with start date."""
    start = date(2024, 10, 1)
    goal = MockGoal(start_date=start)

    assert goal.start_date == start


def test_goal_protocol_with_dates():
    """Test GoalProtocol with both start and target dates."""
    start = date(2024, 10, 1)
    target = date(2025, 6, 1)
    goal = MockGoal(start_date=start, target_date=target)

    assert goal.start_date == start
    assert goal.target_date == target


def test_goal_protocol_with_value():
    """Test GoalProtocol with value and unit."""
    goal = MockGoal(
        description="Achieve weight loss",
        value="180",
        value_unit="lbs",
    )

    assert goal.value == "180"
    assert goal.value_unit == "lbs"


def test_goal_protocol_with_author():
    """Test GoalProtocol with author."""
    goal = MockGoal(author="patient")

    assert goal.author == "patient"


def test_goal_protocol_with_priority():
    """Test GoalProtocol with priority."""
    goal = MockGoal(priority="high")

    assert goal.priority == "high"


def test_goal_status_values():
    """Test different goal status values."""
    active = MockGoal(status="active")
    cancelled = MockGoal(status="cancelled")
    completed = MockGoal(status="completed")
    on_hold = MockGoal(status="on-hold")

    assert active.status == "active"
    assert cancelled.status == "cancelled"
    assert completed.status == "completed"
    assert on_hold.status == "on-hold"


def test_goal_protocol_satisfaction():
    """Test that MockGoal satisfies GoalProtocol."""
    goal = MockGoal()

    def accepts_goal(g: GoalProtocol) -> str:
        return f"{g.description} - {g.status}"

    result = accepts_goal(goal)
    assert result == "Achieve target blood pressure of 120/80 - active"


def test_blood_pressure_goal():
    """Test blood pressure goal."""
    goal = MockGoal(
        description="Maintain blood pressure below 130/80",
        code="85354-9",
        code_system="LOINC",
        display_name="Blood pressure systolic and diastolic",
        status="active",
        target_date=date(2025, 3, 1),
        value="130/80",
        value_unit="mm[Hg]",
        author="provider",
        priority="high",
    )

    assert goal.description == "Maintain blood pressure below 130/80"
    assert goal.value == "130/80"
    assert goal.priority == "high"


def test_weight_loss_goal():
    """Test weight loss goal."""
    goal = MockGoal(
        description="Lose 20 pounds in 6 months",
        code="29463-7",
        code_system="LOINC",
        display_name="Body weight",
        status="active",
        start_date=date(2024, 10, 1),
        target_date=date(2025, 4, 1),
        value="180",
        value_unit="lbs",
        author="negotiated",
        priority="medium",
    )

    assert goal.description == "Lose 20 pounds in 6 months"
    assert goal.value == "180"
    assert goal.value_unit == "lbs"


def test_a1c_goal():
    """Test A1C goal for diabetes management."""
    goal = MockGoal(
        description="Reduce A1C to less than 7%",
        code="4548-4",
        code_system="LOINC",
        display_name="Hemoglobin A1c/Hemoglobin.total in Blood",
        status="active",
        target_date=date(2025, 1, 15),
        value="7",
        value_unit="%",
        author="provider",
        priority="high",
    )

    assert goal.code == "4548-4"
    assert goal.value == "7"
    assert goal.value_unit == "%"


def test_exercise_goal():
    """Test exercise goal."""
    goal = MockGoal(
        description="Exercise 30 minutes per day, 5 days per week",
        status="active",
        start_date=date(2024, 10, 1),
        target_date=date(2025, 10, 1),
        author="patient",
        priority="medium",
    )

    assert goal.description == "Exercise 30 minutes per day, 5 days per week"
    assert goal.author == "patient"


def test_smoking_cessation_goal():
    """Test smoking cessation goal."""
    goal = MockGoal(
        description="Quit smoking completely",
        code="72166-2",
        code_system="LOINC",
        display_name="Tobacco smoking status",
        status="active",
        target_date=date(2025, 1, 1),
        author="negotiated",
        priority="high",
    )

    assert goal.description == "Quit smoking completely"
    assert goal.priority == "high"


def test_goal_priority_levels():
    """Test different goal priority levels."""
    low = MockGoal(priority="low")
    medium = MockGoal(priority="medium")
    high = MockGoal(priority="high")

    assert low.priority == "low"
    assert medium.priority == "medium"
    assert high.priority == "high"


def test_goal_author_types():
    """Test different goal author types."""
    patient = MockGoal(author="patient")
    provider = MockGoal(author="provider")
    negotiated = MockGoal(author="negotiated")

    assert patient.author == "patient"
    assert provider.author == "provider"
    assert negotiated.author == "negotiated"


class MinimalGoal:
    """Minimal implementation with only required fields."""

    @property
    def description(self):
        return "Improve overall health"

    @property
    def code(self):
        return None

    @property
    def code_system(self):
        return None

    @property
    def display_name(self):
        return None

    @property
    def status(self):
        return "active"

    @property
    def target_date(self):
        return None

    @property
    def start_date(self):
        return None

    @property
    def value(self):
        return None

    @property
    def value_unit(self):
        return None

    @property
    def author(self):
        return None

    @property
    def priority(self):
        return None


def test_minimal_goal_protocol():
    """Test that minimal implementation satisfies GoalProtocol."""
    goal = MinimalGoal()

    assert goal.description == "Improve overall health"
    assert goal.status == "active"
    assert goal.code is None
    assert goal.target_date is None
    assert goal.value is None
    assert goal.author is None
    assert goal.priority is None


def test_goal_isinstance_check():
    """Test that MockGoal supports protocol typing."""
    goal = MockGoal()

    # Protocol structural typing
    assert isinstance(goal, object)
    assert hasattr(goal, 'description')
    assert hasattr(goal, 'status')
    assert hasattr(goal, 'code')
    assert hasattr(goal, 'target_date')
    assert hasattr(goal, 'value')
    assert hasattr(goal, 'priority')


def test_completed_goal():
    """Test completed goal."""
    goal = MockGoal(
        description="Achieve target A1C",
        code="4548-4",
        code_system="LOINC",
        status="completed",
        start_date=date(2024, 1, 1),
        target_date=date(2024, 6, 1),
        value="6.5",
        value_unit="%",
    )

    assert goal.status == "completed"


def test_cancelled_goal():
    """Test cancelled goal."""
    goal = MockGoal(
        description="Original weight goal",
        status="cancelled",
        start_date=date(2024, 1, 1),
    )

    assert goal.status == "cancelled"


def test_goal_on_hold():
    """Test goal on hold."""
    goal = MockGoal(
        description="Increase physical activity",
        status="on-hold",
        start_date=date(2024, 5, 1),
    )

    assert goal.status == "on-hold"


def test_goal_with_snomed_code():
    """Test goal with SNOMED CT code."""
    goal = MockGoal(
        description="Improve diabetic control",
        code="698360004",
        code_system="SNOMED",
        display_name="Diabetes mellitus management",
    )

    assert goal.code == "698360004"
    assert goal.code_system == "SNOMED"


def test_goal_without_dates():
    """Test goal without any dates specified."""
    goal = MockGoal(
        description="General health improvement",
        status="active",
    )

    assert goal.start_date is None
    assert goal.target_date is None


def test_goal_same_start_and_target_date():
    """Test goal with same start and target date."""
    same_date = date(2024, 12, 31)
    goal = MockGoal(
        description="One-day health goal",
        start_date=same_date,
        target_date=same_date,
    )

    assert goal.start_date == same_date
    assert goal.target_date == same_date


def test_goal_with_empty_optional_strings():
    """Test goal with empty strings for optional fields."""
    goal = MockGoal(
        description="Test goal",
        code="",
        code_system="",
        display_name="",
        value="",
        value_unit="",
        author="",
        priority="",
    )

    assert goal.code == ""
    assert goal.value == ""
    assert goal.author == ""


def test_goal_with_numeric_value_as_string():
    """Test goal with numeric values represented as strings."""
    goal = MockGoal(
        description="Target cholesterol level",
        value="200",
        value_unit="mg/dL",
    )

    assert goal.value == "200"
    assert goal.value_unit == "mg/dL"


def test_goal_with_complex_value():
    """Test goal with complex value format."""
    goal = MockGoal(
        description="Blood pressure control",
        value="120/80",
        value_unit="mm[Hg]",
    )

    assert goal.value == "120/80"
    assert "/" in goal.value


def test_goal_lifecycle():
    """Test goal through its lifecycle."""
    # New goal
    goal = MockGoal(
        description="Reduce weight to target",
        status="active",
        start_date=date(2024, 1, 1),
        target_date=date(2024, 6, 1),
        value="180",
        value_unit="lbs",
    )

    assert goal.status == "active"

    # Goal on hold (simulated by creating new instance)
    on_hold_goal = MockGoal(
        description="Reduce weight to target",
        status="on-hold",
        start_date=date(2024, 1, 1),
        target_date=date(2024, 6, 1),
    )

    assert on_hold_goal.status == "on-hold"

    # Goal completed
    completed_goal = MockGoal(
        description="Reduce weight to target",
        status="completed",
        start_date=date(2024, 1, 1),
        target_date=date(2024, 6, 1),
        value="180",
        value_unit="lbs",
    )

    assert completed_goal.status == "completed"


def test_multiple_goals_for_patient():
    """Test multiple goals for a patient."""
    bp_goal = MockGoal(
        description="Blood pressure control",
        priority="high",
        status="active",
    )

    weight_goal = MockGoal(
        description="Weight loss",
        priority="medium",
        status="active",
    )

    exercise_goal = MockGoal(
        description="Increase exercise",
        priority="medium",
        status="active",
    )

    goals = [bp_goal, weight_goal, exercise_goal]

    assert len(goals) == 3
    assert all(g.status == "active" for g in goals)


def test_goal_with_only_target_date():
    """Test goal with only target date (no start date)."""
    goal = MockGoal(
        description="Future health goal",
        start_date=None,
        target_date=date(2025, 12, 31),
    )

    assert goal.start_date is None
    assert goal.target_date == date(2025, 12, 31)


def test_goal_with_only_start_date():
    """Test goal with only start date (no target date)."""
    goal = MockGoal(
        description="Open-ended health goal",
        start_date=date(2024, 10, 1),
        target_date=None,
    )

    assert goal.start_date == date(2024, 10, 1)
    assert goal.target_date is None


def test_goal_with_all_fields():
    """Test goal with all optional fields populated."""
    goal = MockGoal(
        description="Comprehensive diabetes management",
        code="4548-4",
        code_system="LOINC",
        display_name="Hemoglobin A1c/Hemoglobin.total in Blood",
        status="active",
        target_date=date(2025, 6, 1),
        start_date=date(2024, 12, 1),
        value="6.5",
        value_unit="%",
        author="provider",
        priority="high",
    )

    assert goal.description == "Comprehensive diabetes management"
    assert goal.code == "4548-4"
    assert goal.code_system == "LOINC"
    assert goal.display_name == "Hemoglobin A1c/Hemoglobin.total in Blood"
    assert goal.status == "active"
    assert goal.target_date == date(2025, 6, 1)
    assert goal.start_date == date(2024, 12, 1)
    assert goal.value == "6.5"
    assert goal.value_unit == "%"
    assert goal.author == "provider"
    assert goal.priority == "high"
