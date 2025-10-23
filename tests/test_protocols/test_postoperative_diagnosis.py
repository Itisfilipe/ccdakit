"""Tests for postoperative diagnosis protocols."""

from datetime import date

from ccdakit.protocols.postoperative_diagnosis import (
    PersistentIDProtocol,
    PostoperativeDiagnosisProtocol,
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


class MockPostoperativeDiagnosis:
    """Test implementation of PostoperativeDiagnosisProtocol."""

    def __init__(
        self,
        name: str = "Appendicitis with periappendiceal abscess",
        code: str = "85189001",
        code_system: str = "SNOMED",
        onset_date: date = None,
        resolved_date: date = None,
        status: str = "active",
        persistent_id: PersistentIDProtocol = None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._onset_date = onset_date or date(2023, 10, 15)
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
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "POSTOP-123")

    assert pid.root == "2.16.840.1.113883.3.TEST"
    assert pid.extension == "POSTOP-123"


def test_persistent_id_protocol_satisfaction():
    """Test that MockPersistentID satisfies PersistentIDProtocol."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "POSTOP-456")

    def accepts_pid(p: PersistentIDProtocol) -> str:
        return f"{p.root}^{p.extension}"

    result = accepts_pid(pid)
    assert result == "2.16.840.1.113883.3.TEST^POSTOP-456"


def test_postoperative_diagnosis_protocol_required_fields():
    """Test PostoperativeDiagnosisProtocol required fields."""
    diagnosis = MockPostoperativeDiagnosis()

    assert diagnosis.name == "Appendicitis with periappendiceal abscess"
    assert diagnosis.code == "85189001"
    assert diagnosis.code_system == "SNOMED"
    assert diagnosis.status == "active"


def test_postoperative_diagnosis_protocol_with_dates():
    """Test PostoperativeDiagnosisProtocol with onset and resolved dates."""
    onset = date(2023, 11, 10)
    resolved = date(2023, 11, 20)
    diagnosis = MockPostoperativeDiagnosis(
        name="Postoperative wound infection",
        code="266179001",
        onset_date=onset,
        resolved_date=resolved,
        status="resolved",
    )

    assert diagnosis.onset_date == onset
    assert diagnosis.resolved_date == resolved
    assert diagnosis.status == "resolved"


def test_postoperative_diagnosis_protocol_ongoing():
    """Test PostoperativeDiagnosisProtocol for ongoing diagnosis."""
    diagnosis = MockPostoperativeDiagnosis(resolved_date=None, status="active")

    assert diagnosis.resolved_date is None
    assert diagnosis.status == "active"


def test_postoperative_diagnosis_protocol_with_persistent_id():
    """Test PostoperativeDiagnosisProtocol with persistent ID."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "POSTOP-789")
    diagnosis = MockPostoperativeDiagnosis(persistent_id=pid)

    assert diagnosis.persistent_id is not None
    assert diagnosis.persistent_id.root == "2.16.840.1.113883.3.TEST"
    assert diagnosis.persistent_id.extension == "POSTOP-789"


def test_postoperative_diagnosis_protocol_without_persistent_id():
    """Test PostoperativeDiagnosisProtocol without persistent ID."""
    diagnosis = MockPostoperativeDiagnosis()

    assert diagnosis.persistent_id is None


def test_postoperative_diagnosis_protocol_satisfaction():
    """Test that MockPostoperativeDiagnosis satisfies PostoperativeDiagnosisProtocol."""
    diagnosis = MockPostoperativeDiagnosis()

    def accepts_diagnosis(d: PostoperativeDiagnosisProtocol) -> str:
        return f"{d.name} ({d.code})"

    result = accepts_diagnosis(diagnosis)
    assert result == "Appendicitis with periappendiceal abscess (85189001)"


def test_postoperative_diagnosis_with_snomed_code():
    """Test postoperative diagnosis with SNOMED code."""
    diagnosis = MockPostoperativeDiagnosis(
        name="Acute cholecystitis",
        code="65275009",
        code_system="SNOMED",
    )

    assert diagnosis.code == "65275009"
    assert diagnosis.code_system == "SNOMED"


def test_postoperative_diagnosis_with_icd10_code():
    """Test postoperative diagnosis with ICD-10 code."""
    diagnosis = MockPostoperativeDiagnosis(
        name="Acute appendicitis",
        code="K35.80",
        code_system="ICD-10",
    )

    assert diagnosis.code == "K35.80"
    assert diagnosis.code_system == "ICD-10"


def test_postoperative_diagnosis_status_values():
    """Test different postoperative diagnosis status values."""
    active = MockPostoperativeDiagnosis(status="active")
    inactive = MockPostoperativeDiagnosis(status="inactive")
    resolved = MockPostoperativeDiagnosis(status="resolved")

    assert active.status == "active"
    assert inactive.status == "inactive"
    assert resolved.status == "resolved"


class MinimalPostoperativeDiagnosis:
    """Minimal implementation with only required fields."""

    @property
    def name(self):
        return "Perforated gastric ulcer"

    @property
    def code(self):
        return "397881002"

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


def test_minimal_postoperative_diagnosis_protocol():
    """Test that minimal implementation satisfies PostoperativeDiagnosisProtocol."""
    diagnosis = MinimalPostoperativeDiagnosis()

    assert diagnosis.name == "Perforated gastric ulcer"
    assert diagnosis.code == "397881002"
    assert diagnosis.code_system == "SNOMED"
    assert diagnosis.status == "active"
    assert diagnosis.onset_date is None
    assert diagnosis.resolved_date is None
    assert diagnosis.persistent_id is None


def test_postoperative_diagnosis_with_onset_no_resolved():
    """Test postoperative diagnosis with onset date but no resolved date."""
    diagnosis = MockPostoperativeDiagnosis(
        onset_date=date(2023, 9, 15),
        resolved_date=None,
        status="active",
    )

    assert diagnosis.onset_date == date(2023, 9, 15)
    assert diagnosis.resolved_date is None
    assert diagnosis.status == "active"


def test_postoperative_diagnosis_lifecycle():
    """Test postoperative diagnosis through its lifecycle."""
    # New diagnosis discovered during surgery
    diagnosis = MockPostoperativeDiagnosis(
        name="Ruptured appendix",
        code="47693006",
        code_system="SNOMED",
        onset_date=date(2023, 12, 5),
        resolved_date=None,
        status="active",
    )

    assert diagnosis.status == "active"
    assert diagnosis.resolved_date is None

    # Diagnosis after treatment (simulate by creating new instance)
    resolved_diagnosis = MockPostoperativeDiagnosis(
        name="Ruptured appendix",
        code="47693006",
        code_system="SNOMED",
        onset_date=date(2023, 12, 5),
        resolved_date=date(2023, 12, 15),
        status="resolved",
    )

    assert resolved_diagnosis.status == "resolved"
    assert resolved_diagnosis.resolved_date == date(2023, 12, 15)


def test_postoperative_diagnosis_same_as_preoperative():
    """Test scenario where postoperative diagnosis matches preoperative diagnosis."""
    diagnosis = MockPostoperativeDiagnosis(
        name="Acute appendicitis",
        code="85189001",
        code_system="SNOMED",
        onset_date=date(2023, 11, 1),
        status="active",
    )

    # Verify the diagnosis is properly structured
    assert diagnosis.name == "Acute appendicitis"
    assert diagnosis.code == "85189001"
    assert diagnosis.code_system == "SNOMED"
    assert diagnosis.onset_date == date(2023, 11, 1)


def test_postoperative_diagnosis_complications():
    """Test postoperative diagnosis for surgical complications."""
    diagnosis = MockPostoperativeDiagnosis(
        name="Postoperative hemorrhage",
        code="27268008",
        code_system="SNOMED",
        onset_date=date(2023, 10, 22),
        status="active",
    )

    assert diagnosis.name == "Postoperative hemorrhage"
    assert diagnosis.code == "27268008"
    assert diagnosis.status == "active"


def test_postoperative_diagnosis_multiple_findings():
    """Test multiple postoperative diagnoses."""
    diagnosis1 = MockPostoperativeDiagnosis(
        name="Acute cholecystitis with cholelithiasis",
        code="235888006",
        code_system="SNOMED",
    )

    diagnosis2 = MockPostoperativeDiagnosis(
        name="Adhesions of peritoneum",
        code="78327007",
        code_system="SNOMED",
    )

    assert diagnosis1.name == "Acute cholecystitis with cholelithiasis"
    assert diagnosis2.name == "Adhesions of peritoneum"
    assert diagnosis1.code != diagnosis2.code


def test_postoperative_diagnosis_confirmed_during_surgery():
    """Test diagnosis that was suspected preoperatively and confirmed during surgery."""
    diagnosis = MockPostoperativeDiagnosis(
        name="Malignant neoplasm of colon",
        code="363406005",
        code_system="SNOMED",
        onset_date=date(2023, 10, 1),
        status="active",
    )

    # Confirmed diagnosis maintains its properties
    assert diagnosis.name == "Malignant neoplasm of colon"
    assert diagnosis.code == "363406005"
    assert diagnosis.status == "active"
    assert diagnosis.onset_date == date(2023, 10, 1)
