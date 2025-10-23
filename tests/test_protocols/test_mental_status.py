"""Tests for mental status protocols."""

from datetime import date, datetime
from typing import Optional

from ccdakit.protocols.mental_status import (
    MentalStatusObservationProtocol,
    MentalStatusOrganizerProtocol,
    PersistentIDProtocol,
)


class MockPersistentID:
    """Test implementation of PersistentIDProtocol."""

    def __init__(self, root: str, extension: str):
        self._root = root
        self._extension = extension

    @property
    def root(self):
        return self._root

    @property
    def extension(self):
        return self._extension


class MockMentalStatusObservation:
    """Test implementation of MentalStatusObservationProtocol."""

    def __init__(
        self,
        category: str = "Mood and Affect",
        category_code: Optional[str] = "b152",
        category_code_system: Optional[str] = "ICF",
        value: str = "Depressed mood",
        value_code: Optional[str] = "366979004",
        observation_date: date | datetime = date(2024, 3, 15),
        status: str = "active",
        persistent_id: Optional[PersistentIDProtocol] = None,
    ):
        self._category = category
        self._category_code = category_code
        self._category_code_system = category_code_system
        self._value = value
        self._value_code = value_code
        self._observation_date = observation_date
        self._status = status
        self._persistent_id = persistent_id

    @property
    def category(self):
        return self._category

    @property
    def category_code(self):
        return self._category_code

    @property
    def category_code_system(self):
        return self._category_code_system

    @property
    def value(self):
        return self._value

    @property
    def value_code(self):
        return self._value_code

    @property
    def observation_date(self):
        return self._observation_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class MockMentalStatusOrganizer:
    """Test implementation of MentalStatusOrganizerProtocol."""

    def __init__(
        self,
        category: str = "Cognition",
        category_code: str = "d163",
        category_code_system: str = "ICF",
        observations: list[MentalStatusObservationProtocol] = None,
        effective_time_low: Optional[date | datetime] = None,
        effective_time_high: Optional[date | datetime] = None,
        persistent_id: Optional[PersistentIDProtocol] = None,
    ):
        self._category = category
        self._category_code = category_code
        self._category_code_system = category_code_system
        self._observations = observations or []
        self._effective_time_low = effective_time_low
        self._effective_time_high = effective_time_high
        self._persistent_id = persistent_id

    @property
    def category(self):
        return self._category

    @property
    def category_code(self):
        return self._category_code

    @property
    def category_code_system(self):
        return self._category_code_system

    @property
    def observations(self):
        return self._observations

    @property
    def effective_time_low(self):
        return self._effective_time_low

    @property
    def effective_time_high(self):
        return self._effective_time_high

    @property
    def persistent_id(self):
        return self._persistent_id


def test_persistent_id_protocol_properties():
    """Test that PersistentIDProtocol implementation has all required properties."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "MS-12345")

    assert pid.root == "2.16.840.1.113883.3.TEST"
    assert pid.extension == "MS-12345"


def test_persistent_id_protocol_satisfaction():
    """Test that MockPersistentID satisfies PersistentIDProtocol."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "MS-12345")

    def accepts_pid(p: PersistentIDProtocol) -> str:
        return f"{p.root}^{p.extension}"

    result = accepts_pid(pid)
    assert result == "2.16.840.1.113883.3.TEST^MS-12345"


def test_mental_status_observation_required_fields():
    """Test MentalStatusObservationProtocol required fields."""
    obs = MockMentalStatusObservation()

    assert obs.category == "Mood and Affect"
    assert obs.value == "Depressed mood"
    assert obs.observation_date == date(2024, 3, 15)
    assert obs.status == "active"


def test_mental_status_observation_with_codes():
    """Test MentalStatusObservationProtocol with codes."""
    obs = MockMentalStatusObservation(
        category="Cognition",
        category_code="d163",
        category_code_system="ICF",
        value="Alert and oriented",
        value_code="422768004",
    )

    assert obs.category_code == "d163"
    assert obs.category_code_system == "ICF"
    assert obs.value_code == "422768004"


def test_mental_status_observation_without_codes():
    """Test MentalStatusObservationProtocol without codes."""
    obs = MockMentalStatusObservation(
        category_code=None,
        category_code_system=None,
        value_code=None,
    )

    assert obs.category_code is None
    assert obs.category_code_system is None
    assert obs.value_code is None


def test_mental_status_observation_with_datetime():
    """Test MentalStatusObservationProtocol with datetime observation."""
    obs = MockMentalStatusObservation(
        observation_date=datetime(2024, 3, 15, 14, 30),
    )

    assert isinstance(obs.observation_date, datetime)
    assert obs.observation_date == datetime(2024, 3, 15, 14, 30)


def test_mental_status_observation_with_persistent_id():
    """Test MentalStatusObservationProtocol with persistent ID."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "OBS-123")
    obs = MockMentalStatusObservation(persistent_id=pid)

    assert obs.persistent_id is not None
    assert obs.persistent_id.root == "2.16.840.1.113883.3.TEST"
    assert obs.persistent_id.extension == "OBS-123"


def test_mental_status_observation_without_persistent_id():
    """Test MentalStatusObservationProtocol without persistent ID."""
    obs = MockMentalStatusObservation()

    assert obs.persistent_id is None


def test_mental_status_observation_different_statuses():
    """Test MentalStatusObservationProtocol with different statuses."""
    active = MockMentalStatusObservation(status="active")
    inactive = MockMentalStatusObservation(status="inactive")
    completed = MockMentalStatusObservation(status="completed")

    assert active.status == "active"
    assert inactive.status == "inactive"
    assert completed.status == "completed"


def test_mental_status_observation_protocol_satisfaction():
    """Test that MockMentalStatusObservation satisfies MentalStatusObservationProtocol."""
    obs = MockMentalStatusObservation()

    def accepts_observation(o: MentalStatusObservationProtocol) -> str:
        return f"{o.category}: {o.value}"

    result = accepts_observation(obs)
    assert result == "Mood and Affect: Depressed mood"


def test_mental_status_organizer_required_fields():
    """Test MentalStatusOrganizerProtocol required fields."""
    organizer = MockMentalStatusOrganizer()

    assert organizer.category == "Cognition"
    assert organizer.category_code == "d163"
    assert organizer.category_code_system == "ICF"
    assert len(organizer.observations) == 0


def test_mental_status_organizer_with_observations():
    """Test MentalStatusOrganizerProtocol with observations."""
    obs1 = MockMentalStatusObservation(
        category="Cognition",
        value="Alert and oriented x3",
    )
    obs2 = MockMentalStatusObservation(
        category="Cognition",
        value="Good attention span",
    )

    organizer = MockMentalStatusOrganizer(
        observations=[obs1, obs2],
    )

    assert len(organizer.observations) == 2
    assert organizer.observations[0].value == "Alert and oriented x3"
    assert organizer.observations[1].value == "Good attention span"


def test_mental_status_organizer_with_effective_times():
    """Test MentalStatusOrganizerProtocol with effective time range."""
    organizer = MockMentalStatusOrganizer(
        effective_time_low=date(2024, 3, 1),
        effective_time_high=date(2024, 3, 15),
    )

    assert organizer.effective_time_low == date(2024, 3, 1)
    assert organizer.effective_time_high == date(2024, 3, 15)


def test_mental_status_organizer_with_datetime_effective_times():
    """Test MentalStatusOrganizerProtocol with datetime effective times."""
    organizer = MockMentalStatusOrganizer(
        effective_time_low=datetime(2024, 3, 1, 8, 0),
        effective_time_high=datetime(2024, 3, 15, 17, 0),
    )

    assert isinstance(organizer.effective_time_low, datetime)
    assert isinstance(organizer.effective_time_high, datetime)


def test_mental_status_organizer_without_effective_times():
    """Test MentalStatusOrganizerProtocol without effective times."""
    organizer = MockMentalStatusOrganizer()

    assert organizer.effective_time_low is None
    assert organizer.effective_time_high is None


def test_mental_status_organizer_with_persistent_id():
    """Test MentalStatusOrganizerProtocol with persistent ID."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "ORG-123")
    organizer = MockMentalStatusOrganizer(persistent_id=pid)

    assert organizer.persistent_id is not None
    assert organizer.persistent_id.root == "2.16.840.1.113883.3.TEST"
    assert organizer.persistent_id.extension == "ORG-123"


def test_mental_status_organizer_without_persistent_id():
    """Test MentalStatusOrganizerProtocol without persistent ID."""
    organizer = MockMentalStatusOrganizer()

    assert organizer.persistent_id is None


def test_mental_status_organizer_protocol_satisfaction():
    """Test that MockMentalStatusOrganizer satisfies MentalStatusOrganizerProtocol."""
    organizer = MockMentalStatusOrganizer()

    def accepts_organizer(o: MentalStatusOrganizerProtocol) -> str:
        return f"{o.category} ({o.category_code_system}: {o.category_code})"

    result = accepts_organizer(organizer)
    assert result == "Cognition (ICF: d163)"


def test_mental_status_observation_different_categories():
    """Test mental status observations with different categories."""
    mood = MockMentalStatusObservation(
        category="Mood and Affect",
        category_code="b152",
        value="Euthymic mood",
    )
    cognition = MockMentalStatusObservation(
        category="Cognition",
        category_code="d163",
        value="Alert and oriented",
    )
    behavior = MockMentalStatusObservation(
        category="Behavior",
        category_code="d240",
        value="Cooperative",
    )

    assert mood.category == "Mood and Affect"
    assert cognition.category == "Cognition"
    assert behavior.category == "Behavior"


def test_mental_status_observation_with_loinc_code():
    """Test mental status observation with LOINC code."""
    obs = MockMentalStatusObservation(
        category="Mental Status",
        category_code="75275-8",
        category_code_system="LOINC",
        value="Normal mental status",
    )

    assert obs.category_code == "75275-8"
    assert obs.category_code_system == "LOINC"


def test_mental_status_observation_with_snomed_code():
    """Test mental status observation with SNOMED code."""
    obs = MockMentalStatusObservation(
        category="Cognition",
        category_code="386807006",
        category_code_system="SNOMED",
        value="Memory impairment",
    )

    assert obs.category_code_system == "SNOMED"


def test_mental_status_organizer_with_loinc_code():
    """Test mental status organizer with LOINC code."""
    organizer = MockMentalStatusOrganizer(
        category="Mental Status Assessment",
        category_code="10190-7",
        category_code_system="LOINC",
    )

    assert organizer.category_code == "10190-7"
    assert organizer.category_code_system == "LOINC"


def test_mental_status_complete_assessment():
    """Test complete mental status assessment with organizer and observations."""
    pid_org = MockPersistentID("2.16.840.1.113883.3.TEST", "ORG-001")
    pid_obs1 = MockPersistentID("2.16.840.1.113883.3.TEST", "OBS-001")
    pid_obs2 = MockPersistentID("2.16.840.1.113883.3.TEST", "OBS-002")

    obs1 = MockMentalStatusObservation(
        category="Mood and Affect",
        category_code="b152",
        category_code_system="ICF",
        value="Euthymic mood, appropriate affect",
        value_code="162082000",
        observation_date=datetime(2024, 3, 15, 10, 0),
        status="completed",
        persistent_id=pid_obs1,
    )

    obs2 = MockMentalStatusObservation(
        category="Cognition",
        category_code="d163",
        category_code_system="ICF",
        value="Alert and oriented x3",
        value_code="422768004",
        observation_date=datetime(2024, 3, 15, 10, 5),
        status="completed",
        persistent_id=pid_obs2,
    )

    organizer = MockMentalStatusOrganizer(
        category="Mental Status Assessment",
        category_code="75276-6",
        category_code_system="LOINC",
        observations=[obs1, obs2],
        effective_time_low=datetime(2024, 3, 15, 10, 0),
        effective_time_high=datetime(2024, 3, 15, 10, 30),
        persistent_id=pid_org,
    )

    assert organizer.category == "Mental Status Assessment"
    assert len(organizer.observations) == 2
    assert organizer.persistent_id is not None
    assert organizer.effective_time_low == datetime(2024, 3, 15, 10, 0)
    assert organizer.effective_time_high == datetime(2024, 3, 15, 10, 30)


def test_mental_status_observation_property_access():
    """Test accessing all observation properties."""
    obs = MockMentalStatusObservation()

    # Access all properties to ensure protocol coverage
    assert isinstance(obs.category, str)
    assert obs.category_code is None or isinstance(obs.category_code, str)
    assert obs.category_code_system is None or isinstance(obs.category_code_system, str)
    assert isinstance(obs.value, str)
    assert obs.value_code is None or isinstance(obs.value_code, str)
    assert isinstance(obs.observation_date, (date, datetime))
    assert isinstance(obs.status, str)
    assert obs.persistent_id is None or hasattr(obs.persistent_id, "root")


def test_mental_status_organizer_property_access():
    """Test accessing all organizer properties."""
    organizer = MockMentalStatusOrganizer()

    # Access all properties to ensure protocol coverage
    assert isinstance(organizer.category, str)
    assert isinstance(organizer.category_code, str)
    assert isinstance(organizer.category_code_system, str)
    assert isinstance(organizer.observations, list)
    assert organizer.effective_time_low is None or isinstance(organizer.effective_time_low, (date, datetime))
    assert organizer.effective_time_high is None or isinstance(organizer.effective_time_high, (date, datetime))
    assert organizer.persistent_id is None or hasattr(organizer.persistent_id, "root")


class MinimalMentalStatusObservation:
    """Minimal implementation with only required fields."""

    @property
    def category(self):
        return "Mental Status"

    @property
    def category_code(self):
        return None

    @property
    def category_code_system(self):
        return None

    @property
    def value(self):
        return "Normal"

    @property
    def value_code(self):
        return None

    @property
    def observation_date(self):
        return date(2024, 1, 1)

    @property
    def status(self):
        return "completed"

    @property
    def persistent_id(self):
        return None


def test_minimal_mental_status_observation():
    """Test minimal mental status observation implementation."""
    obs = MinimalMentalStatusObservation()

    assert obs.category == "Mental Status"
    assert obs.value == "Normal"
    assert obs.status == "completed"
    assert obs.category_code is None
    assert obs.persistent_id is None


class MinimalMentalStatusOrganizer:
    """Minimal implementation with only required fields."""

    @property
    def category(self):
        return "Mental Status"

    @property
    def category_code(self):
        return "MS-001"

    @property
    def category_code_system(self):
        return "LOCAL"

    @property
    def observations(self):
        return []

    @property
    def effective_time_low(self):
        return None

    @property
    def effective_time_high(self):
        return None

    @property
    def persistent_id(self):
        return None


def test_minimal_mental_status_organizer():
    """Test minimal mental status organizer implementation."""
    organizer = MinimalMentalStatusOrganizer()

    assert organizer.category == "Mental Status"
    assert organizer.category_code == "MS-001"
    assert len(organizer.observations) == 0
    assert organizer.effective_time_low is None
    assert organizer.persistent_id is None
