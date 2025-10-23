"""Tests for admission diagnosis protocols."""

from datetime import date

from ccdakit.protocols.admission_diagnosis import AdmissionDiagnosisProtocol
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


class MockAdmissionDiagnosis:
    """Test implementation of AdmissionDiagnosisProtocol."""

    def __init__(
        self,
        name: str = "Acute Myocardial Infarction",
        code: str = "57054005",
        code_system: str = "SNOMED",
        admission_date: date | None = None,
        diagnosis_date: date | None = None,
        persistent_id: PersistentIDProtocol | None = None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._admission_date = admission_date
        self._diagnosis_date = diagnosis_date
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
    def admission_date(self):
        return self._admission_date

    @property
    def diagnosis_date(self):
        return self._diagnosis_date

    @property
    def persistent_id(self):
        return self._persistent_id


def test_admission_diagnosis_protocol_required_fields():
    """Test AdmissionDiagnosisProtocol required fields."""
    diagnosis = MockAdmissionDiagnosis(
        admission_date=date(2024, 1, 15), diagnosis_date=date(2024, 1, 15)
    )

    assert diagnosis.name == "Acute Myocardial Infarction"
    assert diagnosis.code == "57054005"
    assert diagnosis.code_system == "SNOMED"


def test_admission_diagnosis_protocol_with_dates():
    """Test AdmissionDiagnosisProtocol with admission and diagnosis dates."""
    admission = date(2024, 1, 15)
    diagnosis_date = date(2024, 1, 15)
    diagnosis = MockAdmissionDiagnosis(
        admission_date=admission, diagnosis_date=diagnosis_date
    )

    assert diagnosis.admission_date == admission
    assert diagnosis.diagnosis_date == diagnosis_date


def test_admission_diagnosis_protocol_with_persistent_id():
    """Test AdmissionDiagnosisProtocol with persistent ID."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "ADM-DIAG-001")
    diagnosis = MockAdmissionDiagnosis(persistent_id=pid)

    assert diagnosis.persistent_id is not None
    assert diagnosis.persistent_id.root == "2.16.840.1.113883.3.TEST"
    assert diagnosis.persistent_id.extension == "ADM-DIAG-001"


def test_admission_diagnosis_protocol_without_persistent_id():
    """Test AdmissionDiagnosisProtocol without persistent ID."""
    diagnosis = MockAdmissionDiagnosis(
        admission_date=date(2024, 1, 15), diagnosis_date=date(2024, 1, 15)
    )

    assert diagnosis.persistent_id is None


def test_admission_diagnosis_protocol_satisfaction():
    """Test that MockAdmissionDiagnosis satisfies AdmissionDiagnosisProtocol."""
    diagnosis = MockAdmissionDiagnosis(
        admission_date=date(2024, 1, 15), diagnosis_date=date(2024, 1, 15)
    )

    def accepts_admission_diagnosis(d: AdmissionDiagnosisProtocol) -> str:
        return f"{d.name} ({d.code})"

    result = accepts_admission_diagnosis(diagnosis)
    assert result == "Acute Myocardial Infarction (57054005)"


def test_admission_diagnosis_with_snomed_code():
    """Test admission diagnosis with SNOMED code."""
    diagnosis = MockAdmissionDiagnosis(
        name="Acute Myocardial Infarction",
        code="57054005",
        code_system="SNOMED",
        admission_date=date(2024, 1, 15),
        diagnosis_date=date(2024, 1, 15),
    )

    assert diagnosis.code == "57054005"
    assert diagnosis.code_system == "SNOMED"


def test_admission_diagnosis_with_icd10_code():
    """Test admission diagnosis with ICD-10 code."""
    diagnosis = MockAdmissionDiagnosis(
        name="Acute Myocardial Infarction, Unspecified",
        code="I21.9",
        code_system="ICD-10",
        admission_date=date(2024, 1, 15),
        diagnosis_date=date(2024, 1, 15),
    )

    assert diagnosis.code == "I21.9"
    assert diagnosis.code_system == "ICD-10"


def test_admission_diagnosis_different_dates():
    """Test admission diagnosis where diagnosis date differs from admission date."""
    admission = date(2024, 1, 15)
    diagnosis_date = date(2024, 1, 16)
    diagnosis = MockAdmissionDiagnosis(
        name="Pneumonia",
        code="233604007",
        admission_date=admission,
        diagnosis_date=diagnosis_date,
    )

    assert diagnosis.admission_date == admission
    assert diagnosis.diagnosis_date == diagnosis_date
    assert diagnosis.diagnosis_date != diagnosis.admission_date


def test_admission_diagnosis_same_dates():
    """Test admission diagnosis where diagnosis date is same as admission date."""
    admission = date(2024, 1, 15)
    diagnosis = MockAdmissionDiagnosis(
        name="Acute Myocardial Infarction",
        code="57054005",
        admission_date=admission,
        diagnosis_date=admission,
    )

    assert diagnosis.admission_date == diagnosis.diagnosis_date


class MinimalAdmissionDiagnosis:
    """Minimal implementation with only required fields."""

    @property
    def name(self):
        return "Sepsis"

    @property
    def code(self):
        return "91302008"

    @property
    def code_system(self):
        return "SNOMED"

    @property
    def admission_date(self):
        return None

    @property
    def diagnosis_date(self):
        return None

    @property
    def persistent_id(self):
        return None


def test_minimal_admission_diagnosis_protocol():
    """Test that minimal implementation satisfies AdmissionDiagnosisProtocol."""
    diagnosis = MinimalAdmissionDiagnosis()

    assert diagnosis.name == "Sepsis"
    assert diagnosis.code == "91302008"
    assert diagnosis.code_system == "SNOMED"
    assert diagnosis.admission_date is None
    assert diagnosis.diagnosis_date is None
    assert diagnosis.persistent_id is None


def test_admission_diagnosis_common_conditions():
    """Test admission diagnosis for common admission conditions."""
    admission_date = date(2024, 1, 15)
    diagnosis_date = date(2024, 1, 15)

    # Acute Myocardial Infarction
    ami = MockAdmissionDiagnosis(
        name="Acute Myocardial Infarction",
        code="57054005",
        code_system="SNOMED",
        admission_date=admission_date,
        diagnosis_date=diagnosis_date,
    )
    assert ami.name == "Acute Myocardial Infarction"
    assert ami.code == "57054005"

    # Pneumonia
    pneumonia = MockAdmissionDiagnosis(
        name="Pneumonia",
        code="233604007",
        code_system="SNOMED",
        admission_date=admission_date,
        diagnosis_date=diagnosis_date,
    )
    assert pneumonia.name == "Pneumonia"
    assert pneumonia.code == "233604007"

    # Congestive Heart Failure
    chf = MockAdmissionDiagnosis(
        name="Congestive Heart Failure",
        code="42343007",
        code_system="SNOMED",
        admission_date=admission_date,
        diagnosis_date=diagnosis_date,
    )
    assert chf.name == "Congestive Heart Failure"
    assert chf.code == "42343007"

    # Sepsis
    sepsis = MockAdmissionDiagnosis(
        name="Sepsis",
        code="91302008",
        code_system="SNOMED",
        admission_date=admission_date,
        diagnosis_date=diagnosis_date,
    )
    assert sepsis.name == "Sepsis"
    assert sepsis.code == "91302008"


def test_admission_diagnosis_with_optional_dates():
    """Test admission diagnosis with optional dates can be None."""
    diagnosis = MockAdmissionDiagnosis(
        name="Acute Respiratory Failure",
        code="65710008",
        code_system="SNOMED",
        admission_date=None,
        diagnosis_date=None,
    )

    assert diagnosis.admission_date is None
    assert diagnosis.diagnosis_date is None


def test_admission_diagnosis_protocol_type_checking():
    """Test that AdmissionDiagnosisProtocol enforces correct types."""
    diagnosis = MockAdmissionDiagnosis(
        name="Stroke",
        code="230690007",
        code_system="SNOMED",
        admission_date=date(2024, 2, 10),
        diagnosis_date=date(2024, 2, 10),
    )

    # Test that types are correct
    assert isinstance(diagnosis.name, str)
    assert isinstance(diagnosis.code, str)
    assert isinstance(diagnosis.code_system, str)
    assert isinstance(diagnosis.admission_date, date)
    assert isinstance(diagnosis.diagnosis_date, date)


def test_admission_diagnosis_multiple_instances():
    """Test creating multiple admission diagnoses (for multiple admitting diagnoses)."""
    admission_date = date(2024, 1, 15)
    diagnosis_date = date(2024, 1, 15)

    diagnosis1 = MockAdmissionDiagnosis(
        name="Acute Myocardial Infarction",
        code="57054005",
        code_system="SNOMED",
        admission_date=admission_date,
        diagnosis_date=diagnosis_date,
    )

    diagnosis2 = MockAdmissionDiagnosis(
        name="Type 2 Diabetes Mellitus",
        code="44054006",
        code_system="SNOMED",
        admission_date=admission_date,
        diagnosis_date=diagnosis_date,
    )

    diagnosis3 = MockAdmissionDiagnosis(
        name="Hypertension",
        code="38341003",
        code_system="SNOMED",
        admission_date=admission_date,
        diagnosis_date=diagnosis_date,
    )

    assert diagnosis1.name != diagnosis2.name
    assert diagnosis2.name != diagnosis3.name
    assert len({diagnosis1.code, diagnosis2.code, diagnosis3.code}) == 3


def test_admission_diagnosis_protocol_interface():
    """Test that AdmissionDiagnosisProtocol has expected interface."""
    # Import to ensure coverage
    from ccdakit.protocols.admission_diagnosis import AdmissionDiagnosisProtocol

    # Verify protocol has expected attributes
    assert hasattr(AdmissionDiagnosisProtocol, 'name')
    assert hasattr(AdmissionDiagnosisProtocol, 'code')
    assert hasattr(AdmissionDiagnosisProtocol, 'code_system')
    assert hasattr(AdmissionDiagnosisProtocol, 'admission_date')
    assert hasattr(AdmissionDiagnosisProtocol, 'diagnosis_date')
    assert hasattr(AdmissionDiagnosisProtocol, 'persistent_id')

    # Verify docstrings exist
    assert AdmissionDiagnosisProtocol.__doc__ is not None
    assert 'Admission diagnosis data contract' in AdmissionDiagnosisProtocol.__doc__
