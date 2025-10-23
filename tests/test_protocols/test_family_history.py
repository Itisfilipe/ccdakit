"""Tests for family history protocols."""

from datetime import date

from ccdakit.protocols.family_history import (
    FamilyHistoryObservationProtocol,
    FamilyMemberHistoryProtocol,
    FamilyMemberSubjectProtocol,
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


class MockFamilyMemberSubject:
    """Test implementation of FamilyMemberSubjectProtocol."""

    def __init__(
        self,
        administrative_gender_code: str | None = None,
        birth_time: date | None = None,
        deceased_ind: bool | None = None,
        deceased_time: date | None = None,
    ):
        self._administrative_gender_code = administrative_gender_code
        self._birth_time = birth_time
        self._deceased_ind = deceased_ind
        self._deceased_time = deceased_time

    @property
    def administrative_gender_code(self):
        return self._administrative_gender_code

    @property
    def birth_time(self):
        return self._birth_time

    @property
    def deceased_ind(self):
        return self._deceased_ind

    @property
    def deceased_time(self):
        return self._deceased_time


class MockFamilyHistoryObservation:
    """Test implementation of FamilyHistoryObservationProtocol."""

    def __init__(
        self,
        condition_name: str = "Heart Disease",
        condition_code: str = "56265001",
        condition_code_system: str = "SNOMED",
        observation_type_code: str | None = None,
        observation_type_display_name: str | None = None,
        effective_time: date | None = None,
        age_at_onset: int | None = None,
        deceased_age: int | None = None,
        deceased_cause_code: str | None = None,
        deceased_cause_display_name: str | None = None,
        persistent_id: PersistentIDProtocol | None = None,
    ):
        self._condition_name = condition_name
        self._condition_code = condition_code
        self._condition_code_system = condition_code_system
        self._observation_type_code = observation_type_code
        self._observation_type_display_name = observation_type_display_name
        self._effective_time = effective_time
        self._age_at_onset = age_at_onset
        self._deceased_age = deceased_age
        self._deceased_cause_code = deceased_cause_code
        self._deceased_cause_display_name = deceased_cause_display_name
        self._persistent_id = persistent_id

    @property
    def condition_name(self):
        return self._condition_name

    @property
    def condition_code(self):
        return self._condition_code

    @property
    def condition_code_system(self):
        return self._condition_code_system

    @property
    def observation_type_code(self):
        return self._observation_type_code

    @property
    def observation_type_display_name(self):
        return self._observation_type_display_name

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def age_at_onset(self):
        return self._age_at_onset

    @property
    def deceased_age(self):
        return self._deceased_age

    @property
    def deceased_cause_code(self):
        return self._deceased_cause_code

    @property
    def deceased_cause_display_name(self):
        return self._deceased_cause_display_name

    @property
    def persistent_id(self):
        return self._persistent_id


class MockFamilyMemberHistory:
    """Test implementation of FamilyMemberHistoryProtocol."""

    def __init__(
        self,
        relationship_code: str = "FTH",
        relationship_display_name: str = "Father",
        subject: FamilyMemberSubjectProtocol | None = None,
        observations: list | None = None,
        persistent_id: PersistentIDProtocol | None = None,
    ):
        self._relationship_code = relationship_code
        self._relationship_display_name = relationship_display_name
        self._subject = subject
        self._observations = observations or []
        self._persistent_id = persistent_id

    @property
    def relationship_code(self):
        return self._relationship_code

    @property
    def relationship_display_name(self):
        return self._relationship_display_name

    @property
    def subject(self):
        return self._subject

    @property
    def observations(self):
        return self._observations

    @property
    def persistent_id(self):
        return self._persistent_id


def test_persistent_id_protocol():
    """Test PersistentIDProtocol implementation."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "FAM-123")

    assert pid.root == "2.16.840.1.113883.3.TEST"
    assert pid.extension == "FAM-123"


def test_family_member_subject_protocol_all_fields():
    """Test FamilyMemberSubjectProtocol with all fields."""
    subject = MockFamilyMemberSubject(
        administrative_gender_code="M",
        birth_time=date(1950, 5, 15),
        deceased_ind=True,
        deceased_time=date(2010, 8, 20),
    )

    assert subject.administrative_gender_code == "M"
    assert subject.birth_time == date(1950, 5, 15)
    assert subject.deceased_ind is True
    assert subject.deceased_time == date(2010, 8, 20)


def test_family_member_subject_protocol_minimal():
    """Test FamilyMemberSubjectProtocol with minimal fields."""
    subject = MockFamilyMemberSubject()

    assert subject.administrative_gender_code is None
    assert subject.birth_time is None
    assert subject.deceased_ind is None
    assert subject.deceased_time is None


def test_family_member_subject_living():
    """Test FamilyMemberSubjectProtocol for living family member."""
    subject = MockFamilyMemberSubject(
        administrative_gender_code="F",
        birth_time=date(1955, 3, 10),
        deceased_ind=False,
    )

    assert subject.deceased_ind is False
    assert subject.deceased_time is None


def test_family_member_subject_gender_codes():
    """Test various gender codes."""
    male = MockFamilyMemberSubject(administrative_gender_code="M")
    female = MockFamilyMemberSubject(administrative_gender_code="F")
    undifferentiated = MockFamilyMemberSubject(administrative_gender_code="UN")

    assert male.administrative_gender_code == "M"
    assert female.administrative_gender_code == "F"
    assert undifferentiated.administrative_gender_code == "UN"


def test_family_history_observation_required_fields():
    """Test FamilyHistoryObservationProtocol required fields."""
    observation = MockFamilyHistoryObservation()

    assert observation.condition_name == "Heart Disease"
    assert observation.condition_code == "56265001"
    assert observation.condition_code_system == "SNOMED"


def test_family_history_observation_with_age_at_onset():
    """Test FamilyHistoryObservationProtocol with age at onset."""
    observation = MockFamilyHistoryObservation(
        condition_name="Type 2 Diabetes",
        condition_code="44054006",
        condition_code_system="SNOMED",
        age_at_onset=45,
    )

    assert observation.age_at_onset == 45


def test_family_history_observation_with_deceased_info():
    """Test FamilyHistoryObservationProtocol with deceased information."""
    observation = MockFamilyHistoryObservation(
        condition_name="Myocardial Infarction",
        condition_code="22298006",
        condition_code_system="SNOMED",
        deceased_age=65,
        deceased_cause_code="22298006",
        deceased_cause_display_name="Myocardial Infarction",
    )

    assert observation.deceased_age == 65
    assert observation.deceased_cause_code == "22298006"
    assert observation.deceased_cause_display_name == "Myocardial Infarction"


def test_family_history_observation_with_observation_type():
    """Test FamilyHistoryObservationProtocol with observation type."""
    observation = MockFamilyHistoryObservation(
        observation_type_code="64572001",
        observation_type_display_name="Disease",
    )

    assert observation.observation_type_code == "64572001"
    assert observation.observation_type_display_name == "Disease"


def test_family_history_observation_with_effective_time():
    """Test FamilyHistoryObservationProtocol with effective time."""
    observation = MockFamilyHistoryObservation(
        effective_time=date(2015, 6, 10),
    )

    assert observation.effective_time == date(2015, 6, 10)


def test_family_history_observation_with_persistent_id():
    """Test FamilyHistoryObservationProtocol with persistent ID."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "OBS-456")
    observation = MockFamilyHistoryObservation(persistent_id=pid)

    assert observation.persistent_id is not None
    assert observation.persistent_id.root == "2.16.840.1.113883.3.TEST"
    assert observation.persistent_id.extension == "OBS-456"


def test_family_member_history_required_fields():
    """Test FamilyMemberHistoryProtocol required fields."""
    history = MockFamilyMemberHistory()

    assert history.relationship_code == "FTH"
    assert history.relationship_display_name == "Father"
    assert history.observations == []


def test_family_member_history_with_observations():
    """Test FamilyMemberHistoryProtocol with observations."""
    obs1 = MockFamilyHistoryObservation(
        condition_name="Heart Disease",
        condition_code="56265001",
        condition_code_system="SNOMED",
    )
    obs2 = MockFamilyHistoryObservation(
        condition_name="Diabetes",
        condition_code="73211009",
        condition_code_system="SNOMED",
    )

    history = MockFamilyMemberHistory(observations=[obs1, obs2])

    assert len(history.observations) == 2


def test_family_member_history_with_subject():
    """Test FamilyMemberHistoryProtocol with subject details."""
    subject = MockFamilyMemberSubject(
        administrative_gender_code="F",
        birth_time=date(1948, 7, 22),
    )

    history = MockFamilyMemberHistory(
        relationship_code="MTH",
        relationship_display_name="Mother",
        subject=subject,
    )

    assert history.subject is not None
    assert history.subject.administrative_gender_code == "F"


def test_family_member_history_with_persistent_id():
    """Test FamilyMemberHistoryProtocol with persistent ID."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "HIST-789")
    history = MockFamilyMemberHistory(persistent_id=pid)

    assert history.persistent_id is not None
    assert history.persistent_id.extension == "HIST-789"


def test_family_member_history_relationships():
    """Test various family relationships."""
    father = MockFamilyMemberHistory(
        relationship_code="FTH", relationship_display_name="Father"
    )
    mother = MockFamilyMemberHistory(
        relationship_code="MTH", relationship_display_name="Mother"
    )
    brother = MockFamilyMemberHistory(
        relationship_code="BRO", relationship_display_name="Brother"
    )
    sister = MockFamilyMemberHistory(
        relationship_code="SIS", relationship_display_name="Sister"
    )

    assert father.relationship_code == "FTH"
    assert mother.relationship_code == "MTH"
    assert brother.relationship_code == "BRO"
    assert sister.relationship_code == "SIS"


def test_family_member_history_protocol_satisfaction():
    """Test that MockFamilyMemberHistory satisfies FamilyMemberHistoryProtocol."""
    history = MockFamilyMemberHistory()

    def accepts_history(h: FamilyMemberHistoryProtocol) -> str:
        return f"{h.relationship_display_name} ({h.relationship_code})"

    result = accepts_history(history)
    assert result == "Father (FTH)"


def test_family_history_observation_protocol_satisfaction():
    """Test that MockFamilyHistoryObservation satisfies protocol."""
    observation = MockFamilyHistoryObservation()

    def accepts_observation(o: FamilyHistoryObservationProtocol) -> str:
        return f"{o.condition_name} ({o.condition_code})"

    result = accepts_observation(observation)
    assert result == "Heart Disease (56265001)"


def test_family_member_subject_protocol_satisfaction():
    """Test that MockFamilyMemberSubject satisfies protocol."""
    subject = MockFamilyMemberSubject(administrative_gender_code="M")

    def accepts_subject(s: FamilyMemberSubjectProtocol) -> str | None:
        return s.administrative_gender_code

    result = accepts_subject(subject)
    assert result == "M"


class MinimalFamilyHistoryObservation:
    """Minimal implementation of FamilyHistoryObservationProtocol."""

    @property
    def condition_name(self):
        return "Hypertension"

    @property
    def condition_code(self):
        return "38341003"

    @property
    def condition_code_system(self):
        return "SNOMED"

    @property
    def observation_type_code(self):
        return None

    @property
    def observation_type_display_name(self):
        return None

    @property
    def effective_time(self):
        return None

    @property
    def age_at_onset(self):
        return None

    @property
    def deceased_age(self):
        return None

    @property
    def deceased_cause_code(self):
        return None

    @property
    def deceased_cause_display_name(self):
        return None

    @property
    def persistent_id(self):
        return None


def test_minimal_family_history_observation():
    """Test minimal FamilyHistoryObservationProtocol implementation."""
    observation = MinimalFamilyHistoryObservation()

    assert observation.condition_name == "Hypertension"
    assert observation.condition_code == "38341003"
    assert observation.condition_code_system == "SNOMED"
    assert observation.age_at_onset is None


class MinimalFamilyMemberHistory:
    """Minimal implementation of FamilyMemberHistoryProtocol."""

    @property
    def relationship_code(self):
        return "GRNDFTH"

    @property
    def relationship_display_name(self):
        return "Grandfather"

    @property
    def subject(self):
        return None

    @property
    def observations(self):
        return []

    @property
    def persistent_id(self):
        return None


def test_minimal_family_member_history():
    """Test minimal FamilyMemberHistoryProtocol implementation."""
    history = MinimalFamilyMemberHistory()

    assert history.relationship_code == "GRNDFTH"
    assert history.relationship_display_name == "Grandfather"
    assert history.subject is None
    assert len(history.observations) == 0


def test_complete_family_history_scenario():
    """Test complete family history with all protocols."""
    # Create persistent ID
    pid = MockPersistentID("2.16.840.1.113883.3.HOSPITAL", "FAM-001")

    # Create subject details
    subject = MockFamilyMemberSubject(
        administrative_gender_code="M",
        birth_time=date(1945, 3, 15),
        deceased_ind=True,
        deceased_time=date(2020, 6, 10),
    )

    # Create observations
    heart_disease = MockFamilyHistoryObservation(
        condition_name="Coronary Artery Disease",
        condition_code="53741008",
        condition_code_system="SNOMED",
        age_at_onset=60,
    )

    diabetes = MockFamilyHistoryObservation(
        condition_name="Type 2 Diabetes Mellitus",
        condition_code="44054006",
        condition_code_system="SNOMED",
        age_at_onset=55,
    )

    # Create family member history
    history = MockFamilyMemberHistory(
        relationship_code="FTH",
        relationship_display_name="Father",
        subject=subject,
        observations=[heart_disease, diabetes],
        persistent_id=pid,
    )

    assert history.relationship_code == "FTH"
    assert history.subject.deceased_ind is True
    assert len(history.observations) == 2
    assert history.persistent_id.extension == "FAM-001"


def test_family_history_with_icd10_codes():
    """Test family history observation with ICD-10 codes."""
    observation = MockFamilyHistoryObservation(
        condition_name="Breast Cancer",
        condition_code="C50.9",
        condition_code_system="ICD-10",
    )

    assert observation.condition_code == "C50.9"
    assert observation.condition_code_system == "ICD-10"


def test_family_history_isinstance_checks():
    """Test isinstance checks for all protocols."""
    pid = MockPersistentID("1.2.3", "ABC")
    subject = MockFamilyMemberSubject()
    observation = MockFamilyHistoryObservation()
    history = MockFamilyMemberHistory()

    # All should be objects with proper attributes
    assert hasattr(pid, 'root')
    assert hasattr(subject, 'administrative_gender_code')
    assert hasattr(observation, 'condition_name')
    assert hasattr(history, 'relationship_code')


def test_family_history_observation_age_edge_cases():
    """Test family history observation with age edge cases."""
    young_onset = MockFamilyHistoryObservation(age_at_onset=0)
    old_onset = MockFamilyHistoryObservation(age_at_onset=100)
    old_deceased = MockFamilyHistoryObservation(deceased_age=105)

    assert young_onset.age_at_onset == 0
    assert old_onset.age_at_onset == 100
    assert old_deceased.deceased_age == 105


def test_family_member_subject_deceased_without_time():
    """Test deceased indicator without deceased time."""
    subject = MockFamilyMemberSubject(
        deceased_ind=True,
        deceased_time=None,
    )

    assert subject.deceased_ind is True
    assert subject.deceased_time is None


def test_empty_observations_list():
    """Test family member history with explicitly empty observations."""
    history = MockFamilyMemberHistory(observations=[])

    assert history.observations == []
    assert len(history.observations) == 0
