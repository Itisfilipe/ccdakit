"""Tests for problem protocols."""

from datetime import date

from ccdakit.protocols.problem import PersistentIDProtocol, ProblemProtocol


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


class MockProblem:
    """Test implementation of ProblemProtocol."""

    def __init__(
        self,
        name: str = "Type 2 Diabetes Mellitus",
        code: str = "44054006",
        code_system: str = "SNOMED",
        onset_date: date = None,
        resolved_date: date = None,
        status: str = "active",
        persistent_id: PersistentIDProtocol = None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._onset_date = onset_date or date(2020, 1, 1)
        self._resolved_date = resolved_date
        self._status = status
        self._persistent_id = persistent_id

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def onset_date(self):
        return self._onset_date

    @property
    def resolved_date(self):
        return self._resolved_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


def test_persistent_id_protocol_properties():
    """Test that PersistentIDProtocol implementation has all required properties."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "12345")

    assert pid.root == "2.16.840.1.113883.3.TEST"
    assert pid.extension == "12345"


def test_persistent_id_protocol_satisfaction():
    """Test that MockPersistentID satisfies PersistentIDProtocol."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "12345")

    def accepts_pid(p: PersistentIDProtocol) -> str:
        return f"{p.root}^{p.extension}"

    result = accepts_pid(pid)
    assert result == "2.16.840.1.113883.3.TEST^12345"


def test_problem_protocol_required_fields():
    """Test ProblemProtocol required fields."""
    problem = MockProblem()

    assert problem.name == "Type 2 Diabetes Mellitus"
    assert problem.code == "44054006"
    assert problem.code_system == "SNOMED"
    assert problem.status == "active"


def test_problem_protocol_with_dates():
    """Test ProblemProtocol with onset and resolved dates."""
    onset = date(2020, 6, 15)
    resolved = date(2023, 1, 10)
    problem = MockProblem(onset_date=onset, resolved_date=resolved, status="resolved")

    assert problem.onset_date == onset
    assert problem.resolved_date == resolved
    assert problem.status == "resolved"


def test_problem_protocol_ongoing():
    """Test ProblemProtocol for ongoing problem."""
    problem = MockProblem(resolved_date=None, status="active")

    assert problem.resolved_date is None
    assert problem.status == "active"


def test_problem_protocol_with_persistent_id():
    """Test ProblemProtocol with persistent ID."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "PROB-123")
    problem = MockProblem(persistent_id=pid)

    assert problem.persistent_id is not None
    assert problem.persistent_id.root == "2.16.840.1.113883.3.TEST"
    assert problem.persistent_id.extension == "PROB-123"


def test_problem_protocol_without_persistent_id():
    """Test ProblemProtocol without persistent ID."""
    problem = MockProblem()

    assert problem.persistent_id is None


def test_problem_protocol_satisfaction():
    """Test that MockProblem satisfies ProblemProtocol."""
    problem = MockProblem()

    def accepts_problem(p: ProblemProtocol) -> str:
        return f"{p.name} ({p.code})"

    result = accepts_problem(problem)
    assert result == "Type 2 Diabetes Mellitus (44054006)"


def test_problem_with_snomed_code():
    """Test problem with SNOMED code."""
    problem = MockProblem(
        name="Essential Hypertension",
        code="38341003",
        code_system="SNOMED",
    )

    assert problem.code == "38341003"
    assert problem.code_system == "SNOMED"


def test_problem_with_icd10_code():
    """Test problem with ICD-10 code."""
    problem = MockProblem(
        name="Type 2 Diabetes Mellitus",
        code="E11.9",
        code_system="ICD-10",
    )

    assert problem.code == "E11.9"
    assert problem.code_system == "ICD-10"


def test_problem_status_values():
    """Test different problem status values."""
    active = MockProblem(status="active")
    inactive = MockProblem(status="inactive")
    resolved = MockProblem(status="resolved")

    assert active.status == "active"
    assert inactive.status == "inactive"
    assert resolved.status == "resolved"


class MinimalProblem:
    """Minimal implementation with only required fields."""

    @property
    def name(self):
        return "Chronic Pain"

    @property
    def code(self):
        return "82423001"

    @property
    def code_system(self):
        return "SNOMED"

    @property
    def onset_date(self):
        return None

    @property
    def resolved_date(self):
        return None

    @property
    def status(self):
        return "active"

    @property
    def persistent_id(self):
        return None


def test_minimal_problem_protocol():
    """Test that minimal implementation satisfies ProblemProtocol."""
    problem = MinimalProblem()

    assert problem.name == "Chronic Pain"
    assert problem.code == "82423001"
    assert problem.code_system == "SNOMED"
    assert problem.status == "active"
    assert problem.onset_date is None
    assert problem.resolved_date is None
    assert problem.persistent_id is None


def test_problem_with_onset_no_resolved():
    """Test problem with onset date but no resolved date."""
    problem = MockProblem(
        onset_date=date(2015, 3, 20),
        resolved_date=None,
        status="active",
    )

    assert problem.onset_date == date(2015, 3, 20)
    assert problem.resolved_date is None
    assert problem.status == "active"


def test_problem_lifecycle():
    """Test problem through its lifecycle."""
    # New problem
    problem = MockProblem(
        name="Acute Bronchitis",
        code="10509002",
        code_system="SNOMED",
        onset_date=date(2023, 12, 1),
        resolved_date=None,
        status="active",
    )

    assert problem.status == "active"
    assert problem.resolved_date is None

    # Resolved problem (simulate by creating new instance)
    resolved_problem = MockProblem(
        name="Acute Bronchitis",
        code="10509002",
        code_system="SNOMED",
        onset_date=date(2023, 12, 1),
        resolved_date=date(2023, 12, 15),
        status="resolved",
    )

    assert resolved_problem.status == "resolved"
    assert resolved_problem.resolved_date == date(2023, 12, 15)


def test_problem_protocol_property_access():
    """Test accessing all problem properties."""
    problem = MockProblem()

    # Access all properties to ensure protocol coverage
    assert isinstance(problem.name, str)
    assert isinstance(problem.code, str)
    assert isinstance(problem.code_system, str)
    assert problem.onset_date is None or isinstance(problem.onset_date, date)
    assert problem.resolved_date is None or isinstance(problem.resolved_date, date)
    assert isinstance(problem.status, str)
    assert problem.persistent_id is None or hasattr(problem.persistent_id, "root")


def test_persistent_id_protocol_property_access():
    """Test accessing all persistent ID properties."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "PROB-123")

    # Access all properties to ensure protocol coverage
    assert isinstance(pid.root, str)
    assert isinstance(pid.extension, str)


def test_problem_different_code_systems():
    """Test problem with different code systems."""
    snomed = MockProblem(code_system="SNOMED")
    icd10 = MockProblem(code_system="ICD-10")

    assert snomed.code_system == "SNOMED"
    assert icd10.code_system == "ICD-10"


def test_problem_multiple_conditions():
    """Test creating multiple problem instances."""
    problems = [
        MockProblem(name="Diabetes", code="44054006", status="active"),
        MockProblem(name="Hypertension", code="38341003", status="active"),
        MockProblem(name="Asthma", code="195967001", status="inactive"),
    ]

    assert len(problems) == 3
    assert problems[0].status == "active"
    assert problems[1].status == "active"
    assert problems[2].status == "inactive"


def test_problem_onset_without_resolved():
    """Test problem with onset but no resolution."""
    problem = MockProblem(
        onset_date=date(2020, 1, 1),
        resolved_date=None,
        status="active",
    )

    assert problem.onset_date == date(2020, 1, 1)
    assert problem.resolved_date is None
    assert problem.status == "active"


def test_problem_chronic_condition():
    """Test chronic condition problem."""
    problem = MockProblem(
        name="Chronic Kidney Disease",
        code="709044004",
        code_system="SNOMED",
        onset_date=date(2015, 6, 1),
        resolved_date=None,
        status="active",
    )

    assert problem.name == "Chronic Kidney Disease"
    assert problem.onset_date is not None
    assert problem.resolved_date is None


def test_problem_acute_resolved():
    """Test acute resolved problem."""
    problem = MockProblem(
        name="Pneumonia",
        code="233604007",
        code_system="SNOMED",
        onset_date=date(2024, 1, 1),
        resolved_date=date(2024, 1, 14),
        status="resolved",
    )

    assert problem.onset_date == date(2024, 1, 1)
    assert problem.resolved_date == date(2024, 1, 14)
    assert problem.status == "resolved"
