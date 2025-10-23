"""Tests for medication protocols."""

from datetime import date
from typing import Optional

from ccdakit.protocols.medication import MedicationProtocol


class MockMedication:
    """Test implementation of MedicationProtocol."""

    def __init__(
        self,
        name: str = "Lisinopril 10mg oral tablet",
        code: str = "314076",
        dosage: str = "10 mg",
        route: str = "oral",
        frequency: str = "once daily",
        start_date: date = None,
        end_date: Optional[date] = None,
        status: str = "active",
        instructions: Optional[str] = None,
    ):
        self._name = name
        self._code = code
        self._dosage = dosage
        self._route = route
        self._frequency = frequency
        self._start_date = start_date or date(2024, 1, 1)
        self._end_date = end_date
        self._status = status
        self._instructions = instructions

    @property
    def name(self) -> str:
        return self._name

    @property
    def code(self) -> str:
        return self._code

    @property
    def dosage(self) -> str:
        return self._dosage

    @property
    def route(self) -> str:
        return self._route

    @property
    def frequency(self) -> str:
        return self._frequency

    @property
    def start_date(self) -> date:
        return self._start_date

    @property
    def end_date(self) -> Optional[date]:
        return self._end_date

    @property
    def status(self) -> str:
        return self._status

    @property
    def instructions(self) -> Optional[str]:
        return self._instructions


def test_medication_protocol_required_fields():
    """Test MedicationProtocol required fields."""
    medication = MockMedication()

    assert medication.name == "Lisinopril 10mg oral tablet"
    assert medication.code == "314076"
    assert medication.dosage == "10 mg"
    assert medication.route == "oral"
    assert medication.frequency == "once daily"
    assert medication.start_date == date(2024, 1, 1)
    assert medication.status == "active"


def test_medication_protocol_satisfaction():
    """Test that MockMedication satisfies MedicationProtocol."""
    medication = MockMedication()

    def accepts_medication(m: MedicationProtocol) -> str:
        return f"{m.name} - {m.dosage}"

    result = accepts_medication(medication)
    assert result == "Lisinopril 10mg oral tablet - 10 mg"


def test_medication_with_rxnorm_code():
    """Test medication with RxNorm code."""
    medication = MockMedication(
        name="Metformin 500mg oral tablet",
        code="860975",
    )

    assert medication.code == "860975"
    assert medication.name == "Metformin 500mg oral tablet"


def test_medication_status_values():
    """Test different medication status values."""
    active = MockMedication(status="active")
    completed = MockMedication(status="completed")
    discontinued = MockMedication(status="discontinued")

    assert active.status == "active"
    assert completed.status == "completed"
    assert discontinued.status == "discontinued"


def test_medication_with_end_date():
    """Test medication with end date."""
    medication = MockMedication(
        start_date=date(2024, 1, 1),
        end_date=date(2024, 6, 30),
        status="completed",
    )

    assert medication.start_date == date(2024, 1, 1)
    assert medication.end_date == date(2024, 6, 30)
    assert medication.status == "completed"


def test_medication_ongoing():
    """Test ongoing medication (no end date)."""
    medication = MockMedication(
        start_date=date(2024, 1, 1),
        end_date=None,
        status="active",
    )

    assert medication.start_date == date(2024, 1, 1)
    assert medication.end_date is None
    assert medication.status == "active"


def test_medication_with_instructions():
    """Test medication with patient instructions."""
    medication = MockMedication(
        instructions="Take with food. Avoid grapefruit juice.",
    )

    assert medication.instructions == "Take with food. Avoid grapefruit juice."


def test_medication_without_instructions():
    """Test medication without instructions."""
    medication = MockMedication(instructions=None)

    assert medication.instructions is None


def test_medication_routes():
    """Test different medication routes."""
    oral = MockMedication(route="oral")
    iv = MockMedication(route="IV")
    topical = MockMedication(route="topical")
    sublingual = MockMedication(route="sublingual")
    transdermal = MockMedication(route="transdermal")

    assert oral.route == "oral"
    assert iv.route == "IV"
    assert topical.route == "topical"
    assert sublingual.route == "sublingual"
    assert transdermal.route == "transdermal"


def test_medication_frequencies():
    """Test different medication frequencies."""
    once = MockMedication(frequency="once daily")
    twice = MockMedication(frequency="twice daily")
    three = MockMedication(frequency="three times daily")
    every6h = MockMedication(frequency="every 6 hours")
    prn = MockMedication(frequency="as needed")

    assert once.frequency == "once daily"
    assert twice.frequency == "twice daily"
    assert three.frequency == "three times daily"
    assert every6h.frequency == "every 6 hours"
    assert prn.frequency == "as needed"


def test_medication_dosage_formats():
    """Test different dosage formats."""
    mg = MockMedication(dosage="10 mg")
    tablet = MockMedication(dosage="1 tablet")
    ml = MockMedication(dosage="5 ml")
    units = MockMedication(dosage="20 units")
    mcg = MockMedication(dosage="100 mcg")

    assert mg.dosage == "10 mg"
    assert tablet.dosage == "1 tablet"
    assert ml.dosage == "5 ml"
    assert units.dosage == "20 units"
    assert mcg.dosage == "100 mcg"


def test_medication_aspirin_scenario():
    """Test complete aspirin scenario."""
    medication = MockMedication(
        name="Aspirin 81mg oral tablet",
        code="243670",
        dosage="81 mg",
        route="oral",
        frequency="once daily",
        start_date=date(2024, 1, 15),
        end_date=None,
        status="active",
        instructions="Take in the morning with food",
    )

    assert medication.name == "Aspirin 81mg oral tablet"
    assert medication.code == "243670"
    assert medication.dosage == "81 mg"
    assert medication.status == "active"
    assert medication.end_date is None


def test_medication_antibiotic_scenario():
    """Test antibiotic scenario with end date."""
    medication = MockMedication(
        name="Amoxicillin 500mg capsule",
        code="308191",
        dosage="500 mg",
        route="oral",
        frequency="three times daily",
        start_date=date(2024, 3, 1),
        end_date=date(2024, 3, 10),
        status="completed",
        instructions="Take with food. Complete entire course even if feeling better.",
    )

    assert medication.name == "Amoxicillin 500mg capsule"
    assert medication.frequency == "three times daily"
    assert medication.end_date == date(2024, 3, 10)
    assert medication.status == "completed"


def test_medication_insulin_scenario():
    """Test insulin scenario."""
    medication = MockMedication(
        name="Insulin glargine 100 units/mL solution",
        code="261551",
        dosage="20 units",
        route="subcutaneous",
        frequency="once daily",
        start_date=date(2024, 1, 1),
        end_date=None,
        status="active",
        instructions="Inject at bedtime. Rotate injection sites.",
    )

    assert medication.route == "subcutaneous"
    assert medication.dosage == "20 units"
    assert "injection sites" in medication.instructions


def test_medication_inhaler_scenario():
    """Test inhaler scenario."""
    medication = MockMedication(
        name="Albuterol 90 mcg/actuation inhaler",
        code="745752",
        dosage="2 puffs",
        route="inhalation",
        frequency="every 4-6 hours as needed",
        start_date=date(2024, 2, 1),
        end_date=None,
        status="active",
        instructions="Shake well before use. Rinse mouth after use.",
    )

    assert medication.route == "inhalation"
    assert medication.dosage == "2 puffs"
    assert medication.frequency == "every 4-6 hours as needed"


def test_medication_topical_scenario():
    """Test topical medication scenario."""
    medication = MockMedication(
        name="Hydrocortisone 1% cream",
        code="197579",
        dosage="Apply thin layer",
        route="topical",
        frequency="twice daily",
        start_date=date(2024, 3, 15),
        end_date=date(2024, 4, 15),
        status="active",
        instructions="Apply to affected area. Do not use on face.",
    )

    assert medication.route == "topical"
    assert medication.dosage == "Apply thin layer"


def test_medication_eye_drops_scenario():
    """Test eye drops scenario."""
    medication = MockMedication(
        name="Timolol 0.5% eye drops",
        code="310475",
        dosage="1 drop",
        route="ophthalmic",
        frequency="twice daily",
        start_date=date(2024, 1, 10),
        end_date=None,
        status="active",
        instructions="Instill in affected eye(s). Wait 5 minutes between different eye drops.",
    )

    assert medication.route == "ophthalmic"
    assert medication.dosage == "1 drop"


class MinimalMedication:
    """Minimal implementation with only required fields."""

    @property
    def name(self) -> str:
        return "Test Medication"

    @property
    def code(self) -> str:
        return "12345"

    @property
    def dosage(self) -> str:
        return "10 mg"

    @property
    def route(self) -> str:
        return "oral"

    @property
    def frequency(self) -> str:
        return "once daily"

    @property
    def start_date(self) -> date:
        return date(2024, 1, 1)

    @property
    def end_date(self) -> Optional[date]:
        return None

    @property
    def status(self) -> str:
        return "active"

    @property
    def instructions(self) -> Optional[str]:
        return None


def test_minimal_medication_protocol():
    """Test that minimal implementation satisfies MedicationProtocol."""
    medication = MinimalMedication()

    assert medication.name == "Test Medication"
    assert medication.code == "12345"
    assert medication.dosage == "10 mg"
    assert medication.route == "oral"
    assert medication.frequency == "once daily"
    assert medication.start_date == date(2024, 1, 1)
    assert medication.end_date is None
    assert medication.status == "active"
    assert medication.instructions is None


def test_minimal_medication_satisfaction():
    """Test that MinimalMedication satisfies MedicationProtocol."""
    medication = MinimalMedication()

    def accepts_medication(m: MedicationProtocol) -> str:
        return m.name

    result = accepts_medication(medication)
    assert result == "Test Medication"


def test_medication_property_access_multiple_times():
    """Test that properties can be accessed multiple times consistently."""
    medication = MockMedication()

    assert medication.name == medication.name
    assert medication.code == medication.code
    assert medication.dosage == medication.dosage
    assert medication.route == medication.route
    assert medication.frequency == medication.frequency
    assert medication.start_date == medication.start_date
    assert medication.end_date == medication.end_date
    assert medication.status == medication.status
    assert medication.instructions == medication.instructions


def test_medication_discontinued():
    """Test discontinued medication scenario."""
    medication = MockMedication(
        name="Warfarin 5mg tablet",
        code="855332",
        start_date=date(2023, 6, 1),
        end_date=date(2024, 2, 15),
        status="discontinued",
        instructions="Discontinued due to side effects",
    )

    assert medication.status == "discontinued"
    assert medication.end_date == date(2024, 2, 15)


def test_medication_with_complex_dosage():
    """Test medication with complex dosage."""
    medication = MockMedication(
        dosage="5-10 mg based on blood pressure",
    )

    assert medication.dosage == "5-10 mg based on blood pressure"


def test_medication_with_complex_frequency():
    """Test medication with complex frequency."""
    medication = MockMedication(
        frequency="Take 1 tablet in the morning and 2 tablets at bedtime",
    )

    assert medication.frequency == "Take 1 tablet in the morning and 2 tablets at bedtime"


def test_medication_with_long_instructions():
    """Test medication with long instructions."""
    long_instructions = (
        "Take this medication exactly as prescribed. "
        "Do not skip doses. Take with a full glass of water. "
        "May cause drowsiness. Do not drive or operate machinery until you know how this medication affects you. "
        "Avoid alcohol while taking this medication. "
        "Contact your doctor if symptoms persist or worsen."
    )
    medication = MockMedication(instructions=long_instructions)

    assert len(medication.instructions) > 100
    assert "Do not skip doses" in medication.instructions
    assert "Contact your doctor" in medication.instructions


def test_medication_with_empty_instructions():
    """Test medication with empty string instructions."""
    medication = MockMedication(instructions="")

    assert medication.instructions == ""


def test_medication_multiple_same_day():
    """Test multiple medications with same start date."""
    med1 = MockMedication(
        name="Medication A",
        code="111",
        start_date=date(2024, 3, 15),
    )
    med2 = MockMedication(
        name="Medication B",
        code="222",
        start_date=date(2024, 3, 15),
    )

    assert med1.start_date == med2.start_date
    assert med1.name != med2.name


def test_medication_prn_scenario():
    """Test PRN (as needed) medication."""
    medication = MockMedication(
        name="Ibuprofen 400mg tablet",
        code="197806",
        dosage="400 mg",
        route="oral",
        frequency="every 6 hours as needed",
        start_date=date(2024, 3, 1),
        status="active",
        instructions="Take with food. Do not exceed 1200 mg in 24 hours.",
    )

    assert "as needed" in medication.frequency
    assert "Do not exceed" in medication.instructions


def test_medication_patch_scenario():
    """Test transdermal patch medication."""
    medication = MockMedication(
        name="Fentanyl 25 mcg/hour patch",
        code="668621",
        dosage="25 mcg/hour",
        route="transdermal",
        frequency="change every 72 hours",
        start_date=date(2024, 1, 1),
        status="active",
        instructions="Apply to clean, dry skin. Rotate application sites.",
    )

    assert medication.route == "transdermal"
    assert "72 hours" in medication.frequency
