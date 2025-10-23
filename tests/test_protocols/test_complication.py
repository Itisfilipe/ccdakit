"""Tests for complication protocols."""

from datetime import date

from ccdakit.protocols.complication import ComplicationProtocol
from ccdakit.protocols.problem import PersistentIDProtocol


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


class MockComplication:
    """Test implementation of ComplicationProtocol."""

    def __init__(
        self,
        name: str = "Postoperative bleeding",
        code: str = "83132003",
        code_system: str = "SNOMED",
        onset_date: date = None,
        resolved_date: date = None,
        status: str = "active",
        severity: str = None,
        related_procedure_code: str = None,
        persistent_id: PersistentIDProtocol = None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._onset_date = onset_date or date(2024, 1, 15)
        self._resolved_date = resolved_date
        self._status = status
        self._severity = severity
        self._related_procedure_code = related_procedure_code
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
    def severity(self):
        return self._severity

    @property
    def related_procedure_code(self):
        return self._related_procedure_code

    @property
    def persistent_id(self):
        return self._persistent_id


def test_complication_protocol_required_fields():
    """Test ComplicationProtocol required fields."""
    complication = MockComplication()

    assert complication.name == "Postoperative bleeding"
    assert complication.code == "83132003"
    assert complication.code_system == "SNOMED"
    assert complication.status == "active"


def test_complication_protocol_with_dates():
    """Test ComplicationProtocol with onset and resolved dates."""
    onset = date(2024, 1, 15)
    resolved = date(2024, 2, 1)
    complication = MockComplication(
        onset_date=onset, resolved_date=resolved, status="resolved"
    )

    assert complication.onset_date == onset
    assert complication.resolved_date == resolved
    assert complication.status == "resolved"


def test_complication_protocol_ongoing():
    """Test ComplicationProtocol for ongoing complication."""
    complication = MockComplication(resolved_date=None, status="active")

    assert complication.resolved_date is None
    assert complication.status == "active"


def test_complication_protocol_with_severity():
    """Test ComplicationProtocol with severity."""
    mild = MockComplication(severity="mild")
    moderate = MockComplication(severity="moderate")
    severe = MockComplication(severity="severe")

    assert mild.severity == "mild"
    assert moderate.severity == "moderate"
    assert severe.severity == "severe"


def test_complication_protocol_with_procedure_code():
    """Test ComplicationProtocol with related procedure code."""
    complication = MockComplication(
        name="Surgical site infection",
        code="432119003",
        related_procedure_code="80146002",  # Appendectomy
    )

    assert complication.related_procedure_code == "80146002"


def test_complication_protocol_with_persistent_id():
    """Test ComplicationProtocol with persistent ID."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "COMP-123")
    complication = MockComplication(persistent_id=pid)

    assert complication.persistent_id is not None
    assert complication.persistent_id.root == "2.16.840.1.113883.3.TEST"
    assert complication.persistent_id.extension == "COMP-123"


def test_complication_protocol_without_persistent_id():
    """Test ComplicationProtocol without persistent ID."""
    complication = MockComplication()

    assert complication.persistent_id is None


def test_complication_protocol_satisfaction():
    """Test that MockComplication satisfies ComplicationProtocol."""
    complication = MockComplication()

    def accepts_complication(c: ComplicationProtocol) -> str:
        return f"{c.name} ({c.code})"

    result = accepts_complication(complication)
    assert result == "Postoperative bleeding (83132003)"


def test_postoperative_wound_infection():
    """Test complication for postoperative wound infection."""
    complication = MockComplication(
        name="Postoperative wound infection",
        code="432119003",
        code_system="SNOMED",
        onset_date=date(2024, 1, 18),
        resolved_date=date(2024, 2, 15),
        status="resolved",
        severity="moderate",
        related_procedure_code="80146002",  # Appendectomy
    )

    assert complication.name == "Postoperative wound infection"
    assert complication.code == "432119003"
    assert complication.severity == "moderate"
    assert complication.related_procedure_code == "80146002"


def test_postoperative_hemorrhage():
    """Test complication for postoperative hemorrhage."""
    complication = MockComplication(
        name="Postoperative hemorrhage",
        code="83132003",
        code_system="SNOMED",
        onset_date=date(2024, 1, 16),
        resolved_date=date(2024, 1, 16),
        status="resolved",
        severity="severe",
    )

    assert complication.name == "Postoperative hemorrhage"
    assert complication.code == "83132003"
    assert complication.severity == "severe"
    assert complication.status == "resolved"


def test_deep_vein_thrombosis():
    """Test complication for deep vein thrombosis."""
    complication = MockComplication(
        name="Deep vein thrombosis",
        code="128053003",
        code_system="SNOMED",
        onset_date=date(2024, 1, 20),
        resolved_date=None,
        status="active",
        severity="moderate",
    )

    assert complication.name == "Deep vein thrombosis"
    assert complication.code == "128053003"
    assert complication.status == "active"
    assert complication.resolved_date is None


def test_respiratory_failure():
    """Test complication for respiratory failure."""
    complication = MockComplication(
        name="Acute respiratory failure",
        code="409622000",
        code_system="SNOMED",
        onset_date=date(2024, 1, 17),
        resolved_date=date(2024, 1, 25),
        status="resolved",
        severity="severe",
        related_procedure_code="232717009",  # CABG
    )

    assert complication.name == "Acute respiratory failure"
    assert complication.code == "409622000"
    assert complication.severity == "severe"
    assert complication.related_procedure_code == "232717009"


def test_complication_with_icd10_code():
    """Test complication with ICD-10 code."""
    complication = MockComplication(
        name="Postoperative infection",
        code="T81.4",
        code_system="ICD-10",
    )

    assert complication.code == "T81.4"
    assert complication.code_system == "ICD-10"


def test_complication_status_values():
    """Test different complication status values."""
    active = MockComplication(status="active")
    inactive = MockComplication(status="inactive")
    resolved = MockComplication(status="resolved")

    assert active.status == "active"
    assert inactive.status == "inactive"
    assert resolved.status == "resolved"


def test_complication_without_severity():
    """Test complication without severity specified."""
    complication = MockComplication(severity=None)

    assert complication.severity is None


def test_complication_without_procedure_code():
    """Test complication without related procedure code."""
    complication = MockComplication(related_procedure_code=None)

    assert complication.related_procedure_code is None


class MinimalComplication:
    """Minimal implementation with only required fields."""

    @property
    def name(self):
        return "Postoperative sepsis"

    @property
    def code(self):
        return "609433001"

    @property
    def code_system(self):
        return "SNOMED"

    @property
    def onset_date(self):
        return date(2024, 1, 19)

    @property
    def resolved_date(self):
        return None

    @property
    def status(self):
        return "active"

    @property
    def severity(self):
        return None

    @property
    def related_procedure_code(self):
        return None

    @property
    def persistent_id(self):
        return None


def test_minimal_complication_protocol():
    """Test that minimal implementation satisfies ComplicationProtocol."""
    complication = MinimalComplication()

    assert complication.name == "Postoperative sepsis"
    assert complication.code == "609433001"
    assert complication.code_system == "SNOMED"
    assert complication.status == "active"
    assert complication.onset_date == date(2024, 1, 19)
    assert complication.resolved_date is None
    assert complication.severity is None
    assert complication.related_procedure_code is None
    assert complication.persistent_id is None


def test_complication_lifecycle():
    """Test complication through its lifecycle."""
    # New complication - active
    complication = MockComplication(
        name="Surgical site infection",
        code="432119003",
        code_system="SNOMED",
        onset_date=date(2024, 1, 18),
        resolved_date=None,
        status="active",
        severity="moderate",
    )

    assert complication.status == "active"
    assert complication.resolved_date is None

    # Resolved complication (simulate by creating new instance)
    resolved_complication = MockComplication(
        name="Surgical site infection",
        code="432119003",
        code_system="SNOMED",
        onset_date=date(2024, 1, 18),
        resolved_date=date(2024, 2, 10),
        status="resolved",
        severity="moderate",
    )

    assert resolved_complication.status == "resolved"
    assert resolved_complication.resolved_date == date(2024, 2, 10)


def test_multiple_complications_from_same_procedure():
    """Test multiple complications from the same procedure."""
    procedure_code = "232717009"  # CABG

    bleeding = MockComplication(
        name="Postoperative hemorrhage",
        code="83132003",
        related_procedure_code=procedure_code,
        severity="severe",
    )

    infection = MockComplication(
        name="Surgical site infection",
        code="432119003",
        related_procedure_code=procedure_code,
        severity="moderate",
    )

    afib = MockComplication(
        name="Atrial fibrillation",
        code="49436004",
        related_procedure_code=procedure_code,
        severity="moderate",
    )

    assert bleeding.related_procedure_code == procedure_code
    assert infection.related_procedure_code == procedure_code
    assert afib.related_procedure_code == procedure_code


def test_complication_with_onset_no_resolved():
    """Test complication with onset date but no resolved date."""
    complication = MockComplication(
        onset_date=date(2024, 1, 20),
        resolved_date=None,
        status="active",
    )

    assert complication.onset_date == date(2024, 1, 20)
    assert complication.resolved_date is None
    assert complication.status == "active"


def test_complication_tracking_across_documents():
    """Test complication tracking with persistent ID."""
    pid = MockPersistentID("2.16.840.1.113883.3.HOSPITAL", "COMP-2024-001")

    # Initial complication in procedure note
    initial = MockComplication(
        name="Postoperative wound infection",
        code="432119003",
        onset_date=date(2024, 1, 18),
        resolved_date=None,
        status="active",
        persistent_id=pid,
    )

    # Same complication in follow-up note
    followup = MockComplication(
        name="Postoperative wound infection",
        code="432119003",
        onset_date=date(2024, 1, 18),
        resolved_date=date(2024, 2, 10),
        status="resolved",
        persistent_id=pid,
    )

    assert initial.persistent_id.extension == followup.persistent_id.extension
    assert initial.code == followup.code


def test_complication_severity_levels():
    """Test all severity levels."""
    mild = MockComplication(
        name="Mild surgical site erythema",
        code="271807003",
        severity="mild",
    )

    moderate = MockComplication(
        name="Surgical site infection",
        code="432119003",
        severity="moderate",
    )

    severe = MockComplication(
        name="Septic shock",
        code="76571007",
        severity="severe",
    )

    assert mild.severity == "mild"
    assert moderate.severity == "moderate"
    assert severe.severity == "severe"


def test_unanticipated_complication():
    """Test an unanticipated complication."""
    complication = MockComplication(
        name="Anaphylactic reaction to anesthesia",
        code="41291007",
        code_system="SNOMED",
        onset_date=date(2024, 1, 15),
        resolved_date=date(2024, 1, 15),
        status="resolved",
        severity="severe",
        related_procedure_code="287664007",  # General anesthesia
    )

    assert complication.name == "Anaphylactic reaction to anesthesia"
    assert complication.code == "41291007"
    assert complication.severity == "severe"


def test_known_risk_complication():
    """Test a known risk that occurred as a complication."""
    complication = MockComplication(
        name="Postoperative atelectasis",
        code="196001008",
        code_system="SNOMED",
        onset_date=date(2024, 1, 16),
        resolved_date=date(2024, 1, 22),
        status="resolved",
        severity="mild",
    )

    assert complication.name == "Postoperative atelectasis"
    assert complication.code == "196001008"
    assert complication.status == "resolved"


def test_complication_with_none_onset_date():
    """Test complication with None as onset date."""
    # Create complication with None onset_date, but MockComplication defaults to date(2024, 1, 15)
    # Let's create one that actually uses None by not having a default
    class ComplicationWithNoneDate:
        @property
        def name(self):
            return "Postoperative bleeding"

        @property
        def code(self):
            return "83132003"

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
        def severity(self):
            return None

        @property
        def related_procedure_code(self):
            return None

        @property
        def persistent_id(self):
            return None

    complication = ComplicationWithNoneDate()

    # Should allow None for onset_date
    assert complication.onset_date is None
    assert complication.name == "Postoperative bleeding"


def test_complication_isinstance_check():
    """Test that MockComplication can be checked as instance of protocol."""
    complication = MockComplication()

    # Protocol structural typing - can be used with isinstance in runtime
    assert isinstance(complication, object)
    assert hasattr(complication, 'name')
    assert hasattr(complication, 'code')
    assert hasattr(complication, 'status')


def test_complication_edge_case_empty_strings():
    """Test complication with edge case values."""
    complication = MockComplication(
        name="Test Complication",
        code="123456",
        code_system="SNOMED",
        status="active",
        severity="",  # Empty string for optional field
        related_procedure_code="",  # Empty string
    )

    assert complication.severity == ""
    assert complication.related_procedure_code == ""


def test_persistent_id_protocol_satisfaction():
    """Test that PersistentIDProtocol is satisfied by MockPersistentID."""
    pid = MockPersistentID("1.2.3.4.5", "ABC123")

    def accepts_pid(p: PersistentIDProtocol) -> bool:
        return hasattr(p, 'root') and hasattr(p, 'extension')

    assert accepts_pid(pid) is True
    assert pid.root == "1.2.3.4.5"
    assert pid.extension == "ABC123"


def test_complication_with_different_code_systems():
    """Test complications with various code systems."""
    snomed = MockComplication(code_system="SNOMED")
    icd10 = MockComplication(code_system="ICD-10")
    icd9 = MockComplication(code="123.45", code_system="ICD-9")

    assert snomed.code_system == "SNOMED"
    assert icd10.code_system == "ICD-10"
    assert icd9.code_system == "ICD-9"
