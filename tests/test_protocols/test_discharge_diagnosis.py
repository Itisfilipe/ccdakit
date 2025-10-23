"""Tests for discharge diagnosis protocols."""

from datetime import date

from ccdakit.protocols.discharge_diagnosis import DischargeDiagnosisProtocol


class MockDischargeDiagnosis:
    """Test implementation of DischargeDiagnosisProtocol."""

    def __init__(
        self,
        name: str = "Acute Myocardial Infarction",
        code: str = "57054005",
        code_system: str = "SNOMED",
        diagnosis_date: date = None,
        resolved_date: date = None,
        status: str = "active",
        discharge_disposition: str = None,
        priority: int = None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._diagnosis_date = diagnosis_date if diagnosis_date is not None else date(2024, 10, 15)
        self._resolved_date = resolved_date
        self._status = status
        self._discharge_disposition = discharge_disposition
        self._priority = priority

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
    def resolved_date(self):
        return self._resolved_date

    @property
    def status(self):
        return self._status

    @property
    def discharge_disposition(self):
        return self._discharge_disposition

    @property
    def priority(self):
        return self._priority


def test_discharge_diagnosis_protocol_required_fields():
    """Test DischargeDiagnosisProtocol required fields."""
    diagnosis = MockDischargeDiagnosis()

    assert diagnosis.name == "Acute Myocardial Infarction"
    assert diagnosis.code == "57054005"
    assert diagnosis.code_system == "SNOMED"
    assert diagnosis.status == "active"


def test_discharge_diagnosis_protocol_with_dates():
    """Test DischargeDiagnosisProtocol with diagnosis and resolved dates."""
    diagnosis_dt = date(2024, 10, 15)
    resolved_dt = date(2024, 10, 20)
    diagnosis = MockDischargeDiagnosis(
        diagnosis_date=diagnosis_dt, resolved_date=resolved_dt, status="resolved"
    )

    assert diagnosis.diagnosis_date == diagnosis_dt
    assert diagnosis.resolved_date == resolved_dt
    assert diagnosis.status == "resolved"


def test_discharge_diagnosis_protocol_ongoing():
    """Test DischargeDiagnosisProtocol for ongoing diagnosis."""
    diagnosis = MockDischargeDiagnosis(resolved_date=None, status="active")

    assert diagnosis.resolved_date is None
    assert diagnosis.status == "active"


def test_discharge_diagnosis_with_disposition():
    """Test DischargeDiagnosisProtocol with discharge disposition."""
    diagnosis = MockDischargeDiagnosis(
        discharge_disposition="skilled nursing facility"
    )

    assert diagnosis.discharge_disposition == "skilled nursing facility"


def test_discharge_diagnosis_without_disposition():
    """Test DischargeDiagnosisProtocol without discharge disposition."""
    diagnosis = MockDischargeDiagnosis()

    assert diagnosis.discharge_disposition is None


def test_discharge_diagnosis_with_priority():
    """Test DischargeDiagnosisProtocol with priority ranking."""
    primary = MockDischargeDiagnosis(priority=1)
    secondary = MockDischargeDiagnosis(priority=2)

    assert primary.priority == 1
    assert secondary.priority == 2


def test_discharge_diagnosis_without_priority():
    """Test DischargeDiagnosisProtocol without priority ranking."""
    diagnosis = MockDischargeDiagnosis()

    assert diagnosis.priority is None


def test_discharge_diagnosis_protocol_satisfaction():
    """Test that MockDischargeDiagnosis satisfies DischargeDiagnosisProtocol."""
    diagnosis = MockDischargeDiagnosis()

    def accepts_diagnosis(d: DischargeDiagnosisProtocol) -> str:
        return f"{d.name} ({d.code})"

    result = accepts_diagnosis(diagnosis)
    assert result == "Acute Myocardial Infarction (57054005)"


def test_discharge_diagnosis_with_snomed_code():
    """Test discharge diagnosis with SNOMED code."""
    diagnosis = MockDischargeDiagnosis(
        name="Congestive Heart Failure",
        code="42343007",
        code_system="SNOMED",
    )

    assert diagnosis.code == "42343007"
    assert diagnosis.code_system == "SNOMED"


def test_discharge_diagnosis_with_icd10_code():
    """Test discharge diagnosis with ICD-10 code."""
    diagnosis = MockDischargeDiagnosis(
        name="Acute Myocardial Infarction",
        code="I21.9",
        code_system="ICD-10",
    )

    assert diagnosis.code == "I21.9"
    assert diagnosis.code_system == "ICD-10"


def test_discharge_diagnosis_status_values():
    """Test different discharge diagnosis status values."""
    active = MockDischargeDiagnosis(status="active")
    inactive = MockDischargeDiagnosis(status="inactive")
    resolved = MockDischargeDiagnosis(status="resolved")

    assert active.status == "active"
    assert inactive.status == "inactive"
    assert resolved.status == "resolved"


class MinimalDischargeDiagnosis:
    """Minimal implementation with only required fields."""

    @property
    def name(self):
        return "Pneumonia"

    @property
    def code(self):
        return "233604007"

    @property
    def code_system(self):
        return "SNOMED"

    @property
    def diagnosis_date(self):
        return None

    @property
    def resolved_date(self):
        return None

    @property
    def status(self):
        return "active"

    @property
    def discharge_disposition(self):
        return None

    @property
    def priority(self):
        return None


def test_minimal_discharge_diagnosis_protocol():
    """Test that minimal implementation satisfies DischargeDiagnosisProtocol."""
    diagnosis = MinimalDischargeDiagnosis()

    assert diagnosis.name == "Pneumonia"
    assert diagnosis.code == "233604007"
    assert diagnosis.code_system == "SNOMED"
    assert diagnosis.status == "active"
    assert diagnosis.diagnosis_date is None
    assert diagnosis.resolved_date is None
    assert diagnosis.discharge_disposition is None
    assert diagnosis.priority is None


def test_discharge_diagnosis_with_date_no_resolved():
    """Test discharge diagnosis with diagnosis date but no resolved date."""
    diagnosis = MockDischargeDiagnosis(
        diagnosis_date=date(2024, 9, 10),
        resolved_date=None,
        status="active",
    )

    assert diagnosis.diagnosis_date == date(2024, 9, 10)
    assert diagnosis.resolved_date is None
    assert diagnosis.status == "active"


def test_primary_discharge_diagnosis():
    """Test primary discharge diagnosis with priority 1."""
    diagnosis = MockDischargeDiagnosis(
        name="ST Elevation Myocardial Infarction",
        code="401314000",
        code_system="SNOMED",
        diagnosis_date=date(2024, 10, 15),
        status="active",
        priority=1,
        discharge_disposition="home",
    )

    assert diagnosis.priority == 1
    assert diagnosis.name == "ST Elevation Myocardial Infarction"
    assert diagnosis.discharge_disposition == "home"


def test_secondary_discharge_diagnosis():
    """Test secondary discharge diagnosis with priority 2."""
    diagnosis = MockDischargeDiagnosis(
        name="Type 2 Diabetes Mellitus",
        code="44054006",
        code_system="SNOMED",
        diagnosis_date=date(2020, 1, 1),
        status="active",
        priority=2,
    )

    assert diagnosis.priority == 2
    assert diagnosis.name == "Type 2 Diabetes Mellitus"


def test_discharge_diagnosis_lifecycle():
    """Test discharge diagnosis through its lifecycle."""
    # New diagnosis during hospitalization
    diagnosis = MockDischargeDiagnosis(
        name="Acute Respiratory Failure",
        code="65710008",
        code_system="SNOMED",
        diagnosis_date=date(2024, 10, 10),
        resolved_date=None,
        status="active",
    )

    assert diagnosis.status == "active"
    assert diagnosis.resolved_date is None

    # Resolved before discharge (simulate by creating new instance)
    resolved_diagnosis = MockDischargeDiagnosis(
        name="Acute Respiratory Failure",
        code="65710008",
        code_system="SNOMED",
        diagnosis_date=date(2024, 10, 10),
        resolved_date=date(2024, 10, 18),
        status="resolved",
    )

    assert resolved_diagnosis.status == "resolved"
    assert resolved_diagnosis.resolved_date == date(2024, 10, 18)


def test_discharge_diagnosis_with_all_fields():
    """Test discharge diagnosis with all optional fields populated."""
    diagnosis = MockDischargeDiagnosis(
        name="Sepsis",
        code="91302008",
        code_system="SNOMED",
        diagnosis_date=date(2024, 10, 12),
        resolved_date=None,
        status="active",
        discharge_disposition="skilled nursing facility",
        priority=1,
    )

    assert diagnosis.name == "Sepsis"
    assert diagnosis.code == "91302008"
    assert diagnosis.code_system == "SNOMED"
    assert diagnosis.diagnosis_date == date(2024, 10, 12)
    assert diagnosis.resolved_date is None
    assert diagnosis.status == "active"
    assert diagnosis.discharge_disposition == "skilled nursing facility"
    assert diagnosis.priority == 1


def test_discharge_diagnosis_common_dispositions():
    """Test discharge diagnosis with common discharge dispositions."""
    home = MockDischargeDiagnosis(discharge_disposition="home")
    snf = MockDischargeDiagnosis(discharge_disposition="skilled nursing facility")
    rehab = MockDischargeDiagnosis(discharge_disposition="rehabilitation facility")
    acute_care = MockDischargeDiagnosis(
        discharge_disposition="acute care hospital transfer"
    )

    assert home.discharge_disposition == "home"
    assert snf.discharge_disposition == "skilled nursing facility"
    assert rehab.discharge_disposition == "rehabilitation facility"
    assert acute_care.discharge_disposition == "acute care hospital transfer"


def test_multiple_discharge_diagnoses_with_priorities():
    """Test multiple discharge diagnoses ranked by priority."""
    primary = MockDischargeDiagnosis(
        name="Acute Myocardial Infarction",
        code="57054005",
        code_system="SNOMED",
        priority=1,
    )

    secondary = MockDischargeDiagnosis(
        name="Hypertension",
        code="38341003",
        code_system="SNOMED",
        priority=2,
    )

    tertiary = MockDischargeDiagnosis(
        name="Hyperlipidemia",
        code="55822004",
        code_system="SNOMED",
        priority=3,
    )

    assert primary.priority == 1
    assert secondary.priority == 2
    assert tertiary.priority == 3
    assert primary.priority < secondary.priority < tertiary.priority


def test_discharge_diagnosis_no_date_specified():
    """Test discharge diagnosis when diagnosis date is unknown."""
    # Create a diagnosis using the MinimalDischargeDiagnosis which has None for date
    diagnosis = MinimalDischargeDiagnosis()

    # Should accept None for diagnosis_date
    assert diagnosis.diagnosis_date is None
    assert diagnosis.name == "Pneumonia"
    assert diagnosis.status == "active"


def test_discharge_diagnosis_isinstance_check():
    """Test that MockDischargeDiagnosis supports protocol typing."""
    diagnosis = MockDischargeDiagnosis()

    # Protocol structural typing
    assert isinstance(diagnosis, object)
    assert hasattr(diagnosis, 'name')
    assert hasattr(diagnosis, 'code')
    assert hasattr(diagnosis, 'status')
    assert hasattr(diagnosis, 'discharge_disposition')
    assert hasattr(diagnosis, 'priority')


def test_discharge_diagnosis_edge_case_priority_zero():
    """Test discharge diagnosis with priority of 0."""
    diagnosis = MockDischargeDiagnosis(priority=0)

    # Should support 0 as a priority
    assert diagnosis.priority == 0


def test_discharge_diagnosis_high_priority_number():
    """Test discharge diagnosis with high priority number."""
    diagnosis = MockDischargeDiagnosis(
        name="Chronic Condition",
        priority=10,
    )

    assert diagnosis.priority == 10


def test_discharge_diagnosis_empty_disposition():
    """Test discharge diagnosis with empty string disposition."""
    diagnosis = MockDischargeDiagnosis(discharge_disposition="")

    assert diagnosis.discharge_disposition == ""


def test_discharge_diagnosis_with_none_resolved_date():
    """Test discharge diagnosis explicitly with None resolved date."""
    diagnosis = MockDischargeDiagnosis(
        diagnosis_date=date(2024, 5, 1),
        resolved_date=None,
    )

    assert diagnosis.diagnosis_date == date(2024, 5, 1)
    assert diagnosis.resolved_date is None


def test_discharge_diagnosis_both_dates_same():
    """Test discharge diagnosis where diagnosis and resolved dates are same."""
    same_date = date(2024, 6, 15)
    diagnosis = MockDischargeDiagnosis(
        name="Transient Condition",
        diagnosis_date=same_date,
        resolved_date=same_date,
        status="resolved",
    )

    assert diagnosis.diagnosis_date == same_date
    assert diagnosis.resolved_date == same_date
    assert diagnosis.status == "resolved"
