"""Tests for past_medical_history protocols.

This module tests that past_medical_history correctly re-exports
ProblemProtocol and PersistentIDProtocol from the problem module.
"""

from datetime import date

from ccdakit.protocols.past_medical_history import PersistentIDProtocol, ProblemProtocol


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


class MockPastMedicalHistoryProblem:
    """Test implementation of ProblemProtocol for past medical history."""

    def __init__(
        self,
        name: str = "Past Myocardial Infarction",
        code: str = "22298006",
        code_system: str = "SNOMED",
        onset_date: date = None,
        resolved_date: date = None,
        status: str = "resolved",
        persistent_id: PersistentIDProtocol = None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._onset_date = onset_date or date(2015, 3, 10)
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


def test_past_medical_history_imports_problem_protocol():
    """Test that ProblemProtocol is properly imported from past_medical_history."""
    # This test ensures the import works correctly
    problem = MockPastMedicalHistoryProblem()

    assert problem.name == "Past Myocardial Infarction"
    assert problem.code == "22298006"
    assert problem.code_system == "SNOMED"


def test_past_medical_history_imports_persistent_id_protocol():
    """Test that PersistentIDProtocol is properly imported from past_medical_history."""
    # This test ensures the import works correctly
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "PMH-123")

    assert pid.root == "2.16.840.1.113883.3.TEST"
    assert pid.extension == "PMH-123"


def test_past_medical_history_protocol_satisfaction():
    """Test that past medical history problem satisfies ProblemProtocol."""
    problem = MockPastMedicalHistoryProblem()

    def accepts_problem(p: ProblemProtocol) -> str:
        return f"{p.name} ({p.code})"

    result = accepts_problem(problem)
    assert result == "Past Myocardial Infarction (22298006)"


def test_past_medical_history_with_resolved_status():
    """Test past medical history problem with resolved status."""
    problem = MockPastMedicalHistoryProblem(
        name="Appendicitis",
        code="74400008",
        code_system="SNOMED",
        onset_date=date(2010, 5, 15),
        resolved_date=date(2010, 5, 20),
        status="resolved",
    )

    assert problem.name == "Appendicitis"
    assert problem.status == "resolved"
    assert problem.onset_date == date(2010, 5, 15)
    assert problem.resolved_date == date(2010, 5, 20)


def test_past_medical_history_with_persistent_id():
    """Test past medical history problem with persistent ID."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "PMH-456")
    problem = MockPastMedicalHistoryProblem(
        name="Previous Stroke",
        code="230690007",
        code_system="SNOMED",
        persistent_id=pid,
    )

    assert problem.persistent_id is not None
    assert problem.persistent_id.root == "2.16.840.1.113883.3.TEST"
    assert problem.persistent_id.extension == "PMH-456"


def test_past_medical_history_chronic_condition():
    """Test past medical history with chronic but inactive condition."""
    problem = MockPastMedicalHistoryProblem(
        name="Childhood Asthma",
        code="56968009",
        code_system="SNOMED",
        onset_date=date(1995, 1, 1),
        resolved_date=date(2005, 12, 31),
        status="inactive",
    )

    assert problem.name == "Childhood Asthma"
    assert problem.status == "inactive"
    assert problem.onset_date.year == 1995
    assert problem.resolved_date.year == 2005


def test_past_medical_history_surgical_procedure():
    """Test past medical history for surgical procedure."""
    problem = MockPastMedicalHistoryProblem(
        name="Status post cholecystectomy",
        code="428794004",
        code_system="SNOMED",
        onset_date=date(2018, 8, 15),
        resolved_date=date(2018, 8, 15),
        status="resolved",
    )

    assert "cholecystectomy" in problem.name.lower()
    assert problem.status == "resolved"


def test_past_medical_history_with_icd10_code():
    """Test past medical history problem with ICD-10 code."""
    problem = MockPastMedicalHistoryProblem(
        name="Previous myocardial infarction",
        code="I25.2",
        code_system="ICD-10",
        onset_date=date(2015, 3, 10),
        status="resolved",
    )

    assert problem.code == "I25.2"
    assert problem.code_system == "ICD-10"


def test_past_medical_history_without_persistent_id():
    """Test past medical history problem without persistent ID."""
    problem = MockPastMedicalHistoryProblem(persistent_id=None)

    assert problem.persistent_id is None


def test_past_medical_history_multiple_conditions():
    """Test creating multiple past medical history problems."""
    conditions = [
        MockPastMedicalHistoryProblem(
            name="Previous pneumonia",
            code="233604007",
            status="resolved",
        ),
        MockPastMedicalHistoryProblem(
            name="Status post appendectomy",
            code="428794004",
            status="resolved",
        ),
        MockPastMedicalHistoryProblem(
            name="Previous fracture",
            code="125605004",
            status="resolved",
        ),
    ]

    assert len(conditions) == 3
    assert all(c.status == "resolved" for c in conditions)


class MinimalPastMedicalHistory:
    """Minimal implementation with only required fields."""

    @property
    def name(self):
        return "Past condition"

    @property
    def code(self):
        return "00000000"

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
        return "resolved"

    @property
    def persistent_id(self):
        return None


def test_minimal_past_medical_history_protocol():
    """Test that minimal implementation satisfies ProblemProtocol."""
    problem = MinimalPastMedicalHistory()

    assert problem.name == "Past condition"
    assert problem.code == "00000000"
    assert problem.code_system == "SNOMED"
    assert problem.status == "resolved"
    assert problem.onset_date is None
    assert problem.resolved_date is None
    assert problem.persistent_id is None


def test_persistent_id_protocol_satisfaction():
    """Test that persistent ID implementation satisfies protocol."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "PMH-789")

    def accepts_pid(p: PersistentIDProtocol) -> str:
        return f"{p.root}^{p.extension}"

    result = accepts_pid(pid)
    assert result == "2.16.840.1.113883.3.TEST^PMH-789"
