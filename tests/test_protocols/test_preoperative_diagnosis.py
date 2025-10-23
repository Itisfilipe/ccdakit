"""Tests for preoperative diagnosis protocols."""

from datetime import date

from ccdakit.protocols.preoperative_diagnosis import (
    PersistentIDProtocol,
    PreoperativeDiagnosisProtocol,
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


class MockPreoperativeDiagnosis:
    """Test implementation of PreoperativeDiagnosisProtocol."""

    def __init__(
        self,
        name: str = "Acute Appendicitis",
        code: str = "74400008",
        code_system: str = "SNOMED",
        diagnosis_date: date = date(2024, 3, 15),
        status: str = "active",
        persistent_id: PersistentIDProtocol = None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._diagnosis_date = diagnosis_date
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
    def diagnosis_date(self):
        return self._diagnosis_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


def test_persistent_id_protocol_properties():
    """Test that PersistentIDProtocol implementation has all required properties."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "PREOP-12345")

    assert pid.root == "2.16.840.1.113883.3.TEST"
    assert pid.extension == "PREOP-12345"


def test_persistent_id_protocol_satisfaction():
    """Test that MockPersistentID satisfies PersistentIDProtocol."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "PREOP-12345")

    def accepts_pid(p: PersistentIDProtocol) -> str:
        return f"{p.root}^{p.extension}"

    result = accepts_pid(pid)
    assert result == "2.16.840.1.113883.3.TEST^PREOP-12345"


def test_preoperative_diagnosis_protocol_required_fields():
    """Test PreoperativeDiagnosisProtocol required fields."""
    diagnosis = MockPreoperativeDiagnosis()

    assert diagnosis.name == "Acute Appendicitis"
    assert diagnosis.code == "74400008"
    assert diagnosis.code_system == "SNOMED"
    assert diagnosis.status == "active"


def test_preoperative_diagnosis_protocol_with_diagnosis_date():
    """Test PreoperativeDiagnosisProtocol with diagnosis date."""
    diagnosis_date = date(2024, 3, 15)
    diagnosis = MockPreoperativeDiagnosis(diagnosis_date=diagnosis_date)

    assert diagnosis.diagnosis_date == diagnosis_date


def test_preoperative_diagnosis_protocol_without_diagnosis_date():
    """Test PreoperativeDiagnosisProtocol with None diagnosis date."""
    diagnosis = MockPreoperativeDiagnosis(diagnosis_date=None)

    assert diagnosis.diagnosis_date is None


def test_preoperative_diagnosis_protocol_with_persistent_id():
    """Test PreoperativeDiagnosisProtocol with persistent ID."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "PREOP-DIAG-123")
    diagnosis = MockPreoperativeDiagnosis(persistent_id=pid)

    assert diagnosis.persistent_id is not None
    assert diagnosis.persistent_id.root == "2.16.840.1.113883.3.TEST"
    assert diagnosis.persistent_id.extension == "PREOP-DIAG-123"


def test_preoperative_diagnosis_protocol_without_persistent_id():
    """Test PreoperativeDiagnosisProtocol without persistent ID."""
    diagnosis = MockPreoperativeDiagnosis()

    assert diagnosis.persistent_id is None


def test_preoperative_diagnosis_protocol_satisfaction():
    """Test that MockPreoperativeDiagnosis satisfies PreoperativeDiagnosisProtocol."""
    diagnosis = MockPreoperativeDiagnosis()

    def accepts_diagnosis(d: PreoperativeDiagnosisProtocol) -> str:
        return f"{d.name} ({d.code})"

    result = accepts_diagnosis(diagnosis)
    assert result == "Acute Appendicitis (74400008)"


def test_preoperative_diagnosis_with_snomed_code():
    """Test preoperative diagnosis with SNOMED code."""
    diagnosis = MockPreoperativeDiagnosis(
        name="Cholecystitis",
        code="76581006",
        code_system="SNOMED",
    )

    assert diagnosis.code == "76581006"
    assert diagnosis.code_system == "SNOMED"


def test_preoperative_diagnosis_with_icd10_code():
    """Test preoperative diagnosis with ICD-10 code."""
    diagnosis = MockPreoperativeDiagnosis(
        name="Acute Appendicitis",
        code="K35.80",
        code_system="ICD-10",
    )

    assert diagnosis.code == "K35.80"
    assert diagnosis.code_system == "ICD-10"


def test_preoperative_diagnosis_status_values():
    """Test different preoperative diagnosis status values."""
    active = MockPreoperativeDiagnosis(status="active")
    inactive = MockPreoperativeDiagnosis(status="inactive")
    resolved = MockPreoperativeDiagnosis(status="resolved")

    assert active.status == "active"
    assert inactive.status == "inactive"
    assert resolved.status == "resolved"


class MinimalPreoperativeDiagnosis:
    """Minimal implementation with only required fields."""

    @property
    def name(self):
        return "Inguinal Hernia"

    @property
    def code(self):
        return "396232000"

    @property
    def code_system(self):
        return "SNOMED"

    @property
    def diagnosis_date(self):
        return None

    @property
    def status(self):
        return "active"

    @property
    def persistent_id(self):
        return None


def test_minimal_preoperative_diagnosis_protocol():
    """Test that minimal implementation satisfies PreoperativeDiagnosisProtocol."""
    diagnosis = MinimalPreoperativeDiagnosis()

    assert diagnosis.name == "Inguinal Hernia"
    assert diagnosis.code == "396232000"
    assert diagnosis.code_system == "SNOMED"
    assert diagnosis.status == "active"
    assert diagnosis.diagnosis_date is None
    assert diagnosis.persistent_id is None


def test_preoperative_diagnosis_common_surgical_conditions():
    """Test preoperative diagnosis for common surgical conditions."""
    # Appendicitis
    appendicitis = MockPreoperativeDiagnosis(
        name="Acute Appendicitis",
        code="74400008",
        code_system="SNOMED",
        diagnosis_date=date(2024, 3, 15),
    )
    assert appendicitis.name == "Acute Appendicitis"
    assert appendicitis.code == "74400008"

    # Cholecystitis
    cholecystitis = MockPreoperativeDiagnosis(
        name="Acute Cholecystitis",
        code="76581006",
        code_system="SNOMED",
        diagnosis_date=date(2024, 3, 16),
    )
    assert cholecystitis.name == "Acute Cholecystitis"
    assert cholecystitis.code == "76581006"

    # Hernia
    hernia = MockPreoperativeDiagnosis(
        name="Inguinal Hernia",
        code="396232000",
        code_system="SNOMED",
        diagnosis_date=date(2024, 3, 17),
    )
    assert hernia.name == "Inguinal Hernia"
    assert hernia.code == "396232000"


def test_preoperative_diagnosis_full_specification():
    """Test preoperative diagnosis with all fields populated."""
    pid = MockPersistentID("2.16.840.1.113883.3.HOSPITAL", "PREOP-DIAG-20240315-001")
    diagnosis = MockPreoperativeDiagnosis(
        name="Acute Appendicitis with Peritonitis",
        code="85189001",
        code_system="SNOMED",
        diagnosis_date=date(2024, 3, 15),
        status="active",
        persistent_id=pid,
    )

    assert diagnosis.name == "Acute Appendicitis with Peritonitis"
    assert diagnosis.code == "85189001"
    assert diagnosis.code_system == "SNOMED"
    assert diagnosis.diagnosis_date == date(2024, 3, 15)
    assert diagnosis.status == "active"
    assert diagnosis.persistent_id is not None
    assert diagnosis.persistent_id.root == "2.16.840.1.113883.3.HOSPITAL"
    assert diagnosis.persistent_id.extension == "PREOP-DIAG-20240315-001"


def test_preoperative_diagnosis_type_checking():
    """Test that type checking works with protocol."""
    diagnosis = MockPreoperativeDiagnosis()

    # This should pass type checking
    def process_diagnosis(d: PreoperativeDiagnosisProtocol) -> str:
        return f"Preoperative Diagnosis: {d.name} (Code: {d.code}, System: {d.code_system})"

    result = process_diagnosis(diagnosis)
    assert "Preoperative Diagnosis: Acute Appendicitis" in result
    assert "Code: 74400008" in result
    assert "System: SNOMED" in result


def test_preoperative_diagnosis_multiple_instances():
    """Test creating multiple preoperative diagnosis instances."""
    diagnoses = [
        MockPreoperativeDiagnosis(
            name="Acute Appendicitis",
            code="74400008",
            code_system="SNOMED",
        ),
        MockPreoperativeDiagnosis(
            name="Rule out Peritonitis",
            code="48661000",
            code_system="SNOMED",
        ),
        MockPreoperativeDiagnosis(
            name="Abdominal Pain",
            code="21522001",
            code_system="SNOMED",
        ),
    ]

    assert len(diagnoses) == 3
    assert diagnoses[0].name == "Acute Appendicitis"
    assert diagnoses[1].name == "Rule out Peritonitis"
    assert diagnoses[2].name == "Abdominal Pain"


def test_preoperative_diagnosis_with_date_comparison():
    """Test preoperative diagnosis date comparison."""
    early_diagnosis = MockPreoperativeDiagnosis(
        diagnosis_date=date(2024, 3, 1)
    )
    late_diagnosis = MockPreoperativeDiagnosis(
        diagnosis_date=date(2024, 3, 15)
    )

    assert early_diagnosis.diagnosis_date < late_diagnosis.diagnosis_date


def test_preoperative_diagnosis_protocol_property_access():
    """Test accessing all preoperative diagnosis properties."""
    diagnosis = MockPreoperativeDiagnosis()

    # Access all properties to ensure protocol coverage
    assert isinstance(diagnosis.name, str)
    assert isinstance(diagnosis.code, str)
    assert isinstance(diagnosis.code_system, str)
    assert diagnosis.diagnosis_date is None or isinstance(diagnosis.diagnosis_date, date)
    assert isinstance(diagnosis.status, str)
    assert diagnosis.persistent_id is None or hasattr(diagnosis.persistent_id, "root")


def test_preoperative_diagnosis_different_statuses():
    """Test preoperative diagnosis with different status values."""
    active = MockPreoperativeDiagnosis(status="active")
    inactive = MockPreoperativeDiagnosis(status="inactive")

    assert active.status == "active"
    assert inactive.status == "inactive"


def test_preoperative_diagnosis_emergency_surgery():
    """Test preoperative diagnosis for emergency surgery."""
    diagnosis = MockPreoperativeDiagnosis(
        name="Acute Appendicitis with Perforation",
        code="85189001",
        code_system="SNOMED",
        diagnosis_date=date(2024, 3, 15),
        status="active",
    )

    assert "Appendicitis" in diagnosis.name
    assert diagnosis.status == "active"


def test_preoperative_diagnosis_elective_surgery():
    """Test preoperative diagnosis for elective surgery."""
    diagnosis = MockPreoperativeDiagnosis(
        name="Cholelithiasis",
        code="235919008",
        code_system="SNOMED",
        diagnosis_date=date(2024, 2, 1),
        status="active",
    )

    assert diagnosis.name == "Cholelithiasis"
    assert diagnosis.diagnosis_date == date(2024, 2, 1)
