"""Tests for procedure protocols."""

from datetime import date, datetime
from typing import Optional

from ccdakit.protocols.procedure import ProcedureProtocol


class MockProcedure:
    """Test implementation of ProcedureProtocol."""

    def __init__(
        self,
        name: str = "Appendectomy",
        code: str = "80146002",
        code_system: str = "SNOMED CT",
        date: Optional[date | datetime] = date(2024, 3, 15),
        status: str = "completed",
        target_site: Optional[str] = None,
        target_site_code: Optional[str] = None,
        performer_name: Optional[str] = None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._date = date
        self._status = status
        self._target_site = target_site
        self._target_site_code = target_site_code
        self._performer_name = performer_name

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
    def date(self):
        return self._date

    @property
    def status(self):
        return self._status

    @property
    def target_site(self):
        return self._target_site

    @property
    def target_site_code(self):
        return self._target_site_code

    @property
    def performer_name(self):
        return self._performer_name


def test_procedure_protocol_required_fields():
    """Test ProcedureProtocol required fields."""
    proc = MockProcedure()

    assert proc.name == "Appendectomy"
    assert proc.code == "80146002"
    assert proc.code_system == "SNOMED CT"
    assert proc.status == "completed"


def test_procedure_protocol_with_date():
    """Test ProcedureProtocol with date."""
    proc = MockProcedure(date=date(2024, 3, 15))

    assert proc.date == date(2024, 3, 15)


def test_procedure_protocol_with_datetime():
    """Test ProcedureProtocol with datetime."""
    proc = MockProcedure(date=datetime(2024, 3, 15, 10, 30))

    assert proc.date == datetime(2024, 3, 15, 10, 30)


def test_procedure_protocol_without_date():
    """Test ProcedureProtocol without date."""
    proc = MockProcedure(date=None)

    assert proc.date is None


def test_procedure_protocol_with_target_site():
    """Test ProcedureProtocol with target site."""
    proc = MockProcedure(
        name="Knee arthroscopy",
        code="387713003",
        target_site="Right knee",
        target_site_code="72696002",
    )

    assert proc.target_site == "Right knee"
    assert proc.target_site_code == "72696002"


def test_procedure_protocol_without_target_site():
    """Test ProcedureProtocol without target site."""
    proc = MockProcedure(
        target_site=None,
        target_site_code=None,
    )

    assert proc.target_site is None
    assert proc.target_site_code is None


def test_procedure_protocol_with_performer():
    """Test ProcedureProtocol with performer name."""
    proc = MockProcedure(
        performer_name="Dr. Jane Smith",
    )

    assert proc.performer_name == "Dr. Jane Smith"


def test_procedure_protocol_without_performer():
    """Test ProcedureProtocol without performer name."""
    proc = MockProcedure(performer_name=None)

    assert proc.performer_name is None


def test_procedure_protocol_satisfaction():
    """Test that MockProcedure satisfies ProcedureProtocol."""
    proc = MockProcedure()

    def accepts_procedure(p: ProcedureProtocol) -> str:
        return f"{p.name} ({p.code})"

    result = accepts_procedure(proc)
    assert result == "Appendectomy (80146002)"


def test_procedure_with_snomed_ct_code():
    """Test procedure with SNOMED CT code."""
    proc = MockProcedure(
        name="Cholecystectomy",
        code="38102005",
        code_system="SNOMED CT",
    )

    assert proc.code == "38102005"
    assert proc.code_system == "SNOMED CT"


def test_procedure_with_cpt4_code():
    """Test procedure with CPT-4 code."""
    proc = MockProcedure(
        name="Appendectomy",
        code="44950",
        code_system="CPT-4",
    )

    assert proc.code == "44950"
    assert proc.code_system == "CPT-4"


def test_procedure_with_loinc_code():
    """Test procedure with LOINC code."""
    proc = MockProcedure(
        name="Chest X-ray",
        code="24627-2",
        code_system="LOINC",
    )

    assert proc.code == "24627-2"
    assert proc.code_system == "LOINC"


def test_procedure_with_icd10_pcs_code():
    """Test procedure with ICD10 PCS code."""
    proc = MockProcedure(
        name="Appendectomy",
        code="0DTJ0ZZ",
        code_system="ICD10 PCS",
    )

    assert proc.code == "0DTJ0ZZ"
    assert proc.code_system == "ICD10 PCS"


def test_procedure_different_statuses():
    """Test procedure with different status values."""
    completed = MockProcedure(status="completed")
    active = MockProcedure(status="active")
    aborted = MockProcedure(status="aborted")
    cancelled = MockProcedure(status="cancelled")

    assert completed.status == "completed"
    assert active.status == "active"
    assert aborted.status == "aborted"
    assert cancelled.status == "cancelled"


def test_procedure_surgical_procedures():
    """Test various surgical procedures."""
    appendectomy = MockProcedure(
        name="Appendectomy",
        code="80146002",
        code_system="SNOMED CT",
        target_site="Appendix",
    )
    cholecystectomy = MockProcedure(
        name="Laparoscopic cholecystectomy",
        code="45595009",
        code_system="SNOMED CT",
        target_site="Gallbladder",
    )

    assert appendectomy.name == "Appendectomy"
    assert cholecystectomy.name == "Laparoscopic cholecystectomy"


def test_procedure_diagnostic_procedures():
    """Test diagnostic procedures."""
    colonoscopy = MockProcedure(
        name="Colonoscopy",
        code="73761001",
        code_system="SNOMED CT",
        target_site="Colon",
    )
    mri = MockProcedure(
        name="MRI of brain",
        code="241615005",
        code_system="SNOMED CT",
        target_site="Brain",
    )

    assert colonoscopy.name == "Colonoscopy"
    assert mri.name == "MRI of brain"


def test_procedure_therapeutic_procedures():
    """Test therapeutic procedures."""
    physical_therapy = MockProcedure(
        name="Physical therapy",
        code="91251008",
        code_system="SNOMED CT",
    )

    assert physical_therapy.name == "Physical therapy"


def test_procedure_with_all_fields():
    """Test procedure with all fields populated."""
    proc = MockProcedure(
        name="Total knee replacement",
        code="179344006",
        code_system="SNOMED CT",
        date=datetime(2024, 3, 15, 8, 30),
        status="completed",
        target_site="Right knee",
        target_site_code="72696002",
        performer_name="Dr. John Surgeon",
    )

    assert proc.name == "Total knee replacement"
    assert proc.code == "179344006"
    assert proc.code_system == "SNOMED CT"
    assert proc.date == datetime(2024, 3, 15, 8, 30)
    assert proc.status == "completed"
    assert proc.target_site == "Right knee"
    assert proc.target_site_code == "72696002"
    assert proc.performer_name == "Dr. John Surgeon"


def test_procedure_property_access():
    """Test accessing all procedure properties."""
    proc = MockProcedure()

    # Access all properties to ensure protocol coverage
    assert isinstance(proc.name, str)
    assert isinstance(proc.code, str)
    assert isinstance(proc.code_system, str)
    assert proc.date is None or isinstance(proc.date, (date, datetime))
    assert isinstance(proc.status, str)
    assert proc.target_site is None or isinstance(proc.target_site, str)
    assert proc.target_site_code is None or isinstance(proc.target_site_code, str)
    assert proc.performer_name is None or isinstance(proc.performer_name, str)


class MinimalProcedure:
    """Minimal implementation with only required fields."""

    @property
    def name(self):
        return "Simple procedure"

    @property
    def code(self):
        return "00000000"

    @property
    def code_system(self):
        return "SNOMED CT"

    @property
    def date(self):
        return None

    @property
    def status(self):
        return "completed"

    @property
    def target_site(self):
        return None

    @property
    def target_site_code(self):
        return None

    @property
    def performer_name(self):
        return None


def test_minimal_procedure_protocol():
    """Test minimal procedure implementation."""
    proc = MinimalProcedure()

    assert proc.name == "Simple procedure"
    assert proc.code == "00000000"
    assert proc.code_system == "SNOMED CT"
    assert proc.status == "completed"
    assert proc.date is None
    assert proc.target_site is None
    assert proc.performer_name is None


def test_procedure_multiple_instances():
    """Test creating multiple procedure instances."""
    procedures = [
        MockProcedure(
            name="Appendectomy",
            code="80146002",
            date=date(2024, 1, 15),
        ),
        MockProcedure(
            name="Cholecystectomy",
            code="38102005",
            date=date(2024, 2, 20),
        ),
        MockProcedure(
            name="Colonoscopy",
            code="73761001",
            date=date(2024, 3, 10),
        ),
    ]

    assert len(procedures) == 3
    assert procedures[0].name == "Appendectomy"
    assert procedures[1].name == "Cholecystectomy"
    assert procedures[2].name == "Colonoscopy"


def test_procedure_with_coded_target_site():
    """Test procedure with coded target site."""
    proc = MockProcedure(
        name="Cardiac catheterization",
        code="41976001",
        code_system="SNOMED CT",
        target_site="Heart",
        target_site_code="80891009",
    )

    assert proc.target_site == "Heart"
    assert proc.target_site_code == "80891009"


def test_procedure_with_text_target_site():
    """Test procedure with text-only target site."""
    proc = MockProcedure(
        name="Skin biopsy",
        code="240977001",
        code_system="SNOMED CT",
        target_site="Left forearm",
        target_site_code=None,
    )

    assert proc.target_site == "Left forearm"
    assert proc.target_site_code is None


def test_procedure_date_comparison():
    """Test procedure date comparison."""
    early_proc = MockProcedure(date=date(2024, 1, 1))
    late_proc = MockProcedure(date=date(2024, 12, 31))

    assert early_proc.date < late_proc.date


def test_procedure_datetime_precision():
    """Test procedure with datetime precision."""
    proc = MockProcedure(
        name="Emergency appendectomy",
        code="80146002",
        code_system="SNOMED CT",
        date=datetime(2024, 3, 15, 23, 45, 30),
        status="completed",
    )

    assert isinstance(proc.date, datetime)
    assert proc.date.hour == 23
    assert proc.date.minute == 45
    assert proc.date.second == 30
