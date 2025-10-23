"""Tests for health concern protocols."""

from datetime import date
from typing import Optional, Sequence

from ccdakit.protocols.health_concern import (
    HealthConcernObservationProtocol,
    HealthConcernProtocol,
    PersistentIDProtocol,
)


class MockPersistentID:
    """Test implementation of PersistentIDProtocol."""

    def __init__(self, root: str, extension: str):
        self._root = root
        self._extension = extension

    @property
    def root(self) -> str:
        return self._root

    @property
    def extension(self) -> str:
        return self._extension


class MockHealthConcernObservation:
    """Test implementation of HealthConcernObservationProtocol."""

    def __init__(
        self,
        observation_type: str = "problem",
        code: str = "44054006",
        code_system: str = "SNOMED",
        display_name: str = "Type 2 Diabetes Mellitus",
    ):
        self._observation_type = observation_type
        self._code = code
        self._code_system = code_system
        self._display_name = display_name

    @property
    def observation_type(self) -> str:
        return self._observation_type

    @property
    def code(self) -> str:
        return self._code

    @property
    def code_system(self) -> str:
        return self._code_system

    @property
    def display_name(self) -> str:
        return self._display_name


class MockHealthConcern:
    """Test implementation of HealthConcernProtocol."""

    def __init__(
        self,
        name: str = "Diabetes Management",
        status: str = "active",
        effective_time_low: Optional[date] = None,
        effective_time_high: Optional[date] = None,
        persistent_id: Optional[PersistentIDProtocol] = None,
        observations: Optional[Sequence[HealthConcernObservationProtocol]] = None,
        author_is_patient: bool = False,
    ):
        self._name = name
        self._status = status
        self._effective_time_low = effective_time_low
        self._effective_time_high = effective_time_high
        self._persistent_id = persistent_id
        self._observations = observations or []
        self._author_is_patient = author_is_patient

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> str:
        return self._status

    @property
    def effective_time_low(self) -> Optional[date]:
        return self._effective_time_low

    @property
    def effective_time_high(self) -> Optional[date]:
        return self._effective_time_high

    @property
    def persistent_id(self) -> Optional[PersistentIDProtocol]:
        return self._persistent_id

    @property
    def observations(self) -> Sequence[HealthConcernObservationProtocol]:
        return self._observations

    @property
    def author_is_patient(self) -> bool:
        return self._author_is_patient


def test_persistent_id_protocol_properties():
    """Test that PersistentIDProtocol implementation has all required properties."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "HC-12345")

    assert pid.root == "2.16.840.1.113883.3.TEST"
    assert pid.extension == "HC-12345"


def test_persistent_id_protocol_satisfaction():
    """Test that MockPersistentID satisfies PersistentIDProtocol."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "HC-12345")

    def accepts_pid(p: PersistentIDProtocol) -> str:
        return f"{p.root}^{p.extension}"

    result = accepts_pid(pid)
    assert result == "2.16.840.1.113883.3.TEST^HC-12345"


def test_health_concern_observation_protocol_properties():
    """Test HealthConcernObservationProtocol properties."""
    obs = MockHealthConcernObservation()

    assert obs.observation_type == "problem"
    assert obs.code == "44054006"
    assert obs.code_system == "SNOMED"
    assert obs.display_name == "Type 2 Diabetes Mellitus"


def test_health_concern_observation_protocol_satisfaction():
    """Test that MockHealthConcernObservation satisfies HealthConcernObservationProtocol."""
    obs = MockHealthConcernObservation()

    def accepts_observation(o: HealthConcernObservationProtocol) -> str:
        return f"{o.observation_type}: {o.display_name}"

    result = accepts_observation(obs)
    assert result == "problem: Type 2 Diabetes Mellitus"


def test_health_concern_observation_types():
    """Test different observation types."""
    problem_obs = MockHealthConcernObservation(observation_type="problem")
    allergy_obs = MockHealthConcernObservation(
        observation_type="allergy",
        code="387207008",
        display_name="Penicillin allergy",
    )
    social_obs = MockHealthConcernObservation(
        observation_type="social_history",
        code="229819007",
        display_name="Tobacco use",
    )

    assert problem_obs.observation_type == "problem"
    assert allergy_obs.observation_type == "allergy"
    assert social_obs.observation_type == "social_history"


def test_health_concern_protocol_required_fields():
    """Test HealthConcernProtocol required fields."""
    concern = MockHealthConcern()

    assert concern.name == "Diabetes Management"
    assert concern.status == "active"
    assert isinstance(concern.observations, Sequence)
    assert isinstance(concern.author_is_patient, bool)


def test_health_concern_protocol_satisfaction():
    """Test that MockHealthConcern satisfies HealthConcernProtocol."""
    concern = MockHealthConcern()

    def accepts_concern(c: HealthConcernProtocol) -> str:
        return f"{c.name} - {c.status}"

    result = accepts_concern(concern)
    assert result == "Diabetes Management - active"


def test_health_concern_with_dates():
    """Test HealthConcernProtocol with effective dates."""
    start_date = date(2023, 1, 15)
    end_date = date(2023, 12, 31)
    concern = MockHealthConcern(
        effective_time_low=start_date,
        effective_time_high=end_date,
        status="completed",
    )

    assert concern.effective_time_low == start_date
    assert concern.effective_time_high == end_date
    assert concern.status == "completed"


def test_health_concern_ongoing():
    """Test ongoing health concern (no end date)."""
    concern = MockHealthConcern(
        effective_time_low=date(2023, 1, 15),
        effective_time_high=None,
        status="active",
    )

    assert concern.effective_time_low == date(2023, 1, 15)
    assert concern.effective_time_high is None
    assert concern.status == "active"


def test_health_concern_with_persistent_id():
    """Test HealthConcernProtocol with persistent ID."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "HC-001")
    concern = MockHealthConcern(persistent_id=pid)

    assert concern.persistent_id is not None
    assert concern.persistent_id.root == "2.16.840.1.113883.3.TEST"
    assert concern.persistent_id.extension == "HC-001"


def test_health_concern_without_persistent_id():
    """Test HealthConcernProtocol without persistent ID."""
    concern = MockHealthConcern()

    assert concern.persistent_id is None


def test_health_concern_with_observations():
    """Test HealthConcernProtocol with observations."""
    obs1 = MockHealthConcernObservation(
        observation_type="problem",
        code="44054006",
        display_name="Type 2 Diabetes Mellitus",
    )
    obs2 = MockHealthConcernObservation(
        observation_type="problem",
        code="38341003",
        display_name="Essential Hypertension",
    )
    concern = MockHealthConcern(observations=[obs1, obs2])

    assert len(concern.observations) == 2
    assert concern.observations[0].display_name == "Type 2 Diabetes Mellitus"
    assert concern.observations[1].display_name == "Essential Hypertension"


def test_health_concern_without_observations():
    """Test HealthConcernProtocol with empty observations list."""
    concern = MockHealthConcern(observations=[])

    assert len(concern.observations) == 0


def test_health_concern_patient_concern():
    """Test health concern authored by patient."""
    concern = MockHealthConcern(
        name="Chronic Pain Management",
        author_is_patient=True,
    )

    assert concern.author_is_patient is True
    assert concern.name == "Chronic Pain Management"


def test_health_concern_provider_concern():
    """Test health concern authored by provider."""
    concern = MockHealthConcern(
        name="Cardiac Risk Factors",
        author_is_patient=False,
    )

    assert concern.author_is_patient is False
    assert concern.name == "Cardiac Risk Factors"


def test_health_concern_status_values():
    """Test different health concern status values."""
    active = MockHealthConcern(status="active")
    suspended = MockHealthConcern(status="suspended")
    aborted = MockHealthConcern(status="aborted")
    completed = MockHealthConcern(status="completed")

    assert active.status == "active"
    assert suspended.status == "suspended"
    assert aborted.status == "aborted"
    assert completed.status == "completed"


def test_health_concern_complex_scenario():
    """Test complex health concern with all fields."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "HC-COMPLEX")
    obs1 = MockHealthConcernObservation(
        observation_type="problem",
        code="44054006",
        display_name="Type 2 Diabetes Mellitus",
    )
    obs2 = MockHealthConcernObservation(
        observation_type="allergy",
        code="387207008",
        display_name="Penicillin allergy",
    )

    concern = MockHealthConcern(
        name="Complex Chronic Disease Management",
        status="active",
        effective_time_low=date(2023, 1, 1),
        effective_time_high=None,
        persistent_id=pid,
        observations=[obs1, obs2],
        author_is_patient=False,
    )

    assert concern.name == "Complex Chronic Disease Management"
    assert concern.status == "active"
    assert concern.effective_time_low == date(2023, 1, 1)
    assert concern.effective_time_high is None
    assert concern.persistent_id.extension == "HC-COMPLEX"
    assert len(concern.observations) == 2
    assert concern.author_is_patient is False


class MinimalHealthConcern:
    """Minimal implementation with only required fields."""

    @property
    def name(self) -> str:
        return "Minimal Concern"

    @property
    def status(self) -> str:
        return "active"

    @property
    def effective_time_low(self) -> Optional[date]:
        return None

    @property
    def effective_time_high(self) -> Optional[date]:
        return None

    @property
    def persistent_id(self) -> Optional[PersistentIDProtocol]:
        return None

    @property
    def observations(self) -> Sequence[HealthConcernObservationProtocol]:
        return []

    @property
    def author_is_patient(self) -> bool:
        return False


def test_minimal_health_concern_protocol():
    """Test that minimal implementation satisfies HealthConcernProtocol."""
    concern = MinimalHealthConcern()

    assert concern.name == "Minimal Concern"
    assert concern.status == "active"
    assert concern.effective_time_low is None
    assert concern.effective_time_high is None
    assert concern.persistent_id is None
    assert len(concern.observations) == 0
    assert concern.author_is_patient is False


def test_minimal_health_concern_satisfaction():
    """Test that MinimalHealthConcern satisfies HealthConcernProtocol."""
    concern = MinimalHealthConcern()

    def accepts_concern(c: HealthConcernProtocol) -> bool:
        return len(c.name) > 0 and c.status in ["active", "suspended", "aborted", "completed"]

    result = accepts_concern(concern)
    assert result is True


def test_health_concern_lifecycle():
    """Test health concern through its lifecycle."""
    # New concern
    concern = MockHealthConcern(
        name="Postoperative Recovery",
        status="active",
        effective_time_low=date(2024, 1, 10),
        effective_time_high=None,
    )

    assert concern.status == "active"
    assert concern.effective_time_high is None

    # Completed concern
    completed_concern = MockHealthConcern(
        name="Postoperative Recovery",
        status="completed",
        effective_time_low=date(2024, 1, 10),
        effective_time_high=date(2024, 3, 15),
    )

    assert completed_concern.status == "completed"
    assert completed_concern.effective_time_high == date(2024, 3, 15)


def test_health_concern_with_mixed_observations():
    """Test health concern with multiple observation types."""
    problem = MockHealthConcernObservation(
        observation_type="problem",
        code="73211009",
        display_name="Diabetes mellitus",
    )
    allergy = MockHealthConcernObservation(
        observation_type="allergy",
        code="91936005",
        display_name="Allergy to penicillin",
    )
    social = MockHealthConcernObservation(
        observation_type="social_history",
        code="229819007",
        display_name="Tobacco smoking behavior",
    )

    concern = MockHealthConcern(
        name="Comprehensive Health Management",
        observations=[problem, allergy, social],
    )

    assert len(concern.observations) == 3
    assert concern.observations[0].observation_type == "problem"
    assert concern.observations[1].observation_type == "allergy"
    assert concern.observations[2].observation_type == "social_history"
