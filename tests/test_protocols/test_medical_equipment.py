"""Tests for medical equipment protocols."""

from datetime import date, datetime
from typing import Optional

from ccdakit.protocols.medical_equipment import MedicalEquipmentProtocol


class MockMedicalEquipment:
    """Test implementation of MedicalEquipmentProtocol."""

    def __init__(
        self,
        name: str = "Wheelchair",
        code: Optional[str] = None,
        code_system: Optional[str] = None,
        status: str = "completed",
        date_supplied: Optional[date | datetime] = None,
        date_end: Optional[date | datetime] = None,
        quantity: Optional[int] = None,
        manufacturer: Optional[str] = None,
        model_number: Optional[str] = None,
        serial_number: Optional[str] = None,
        instructions: Optional[str] = None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._status = status
        self._date_supplied = date_supplied
        self._date_end = date_end
        self._quantity = quantity
        self._manufacturer = manufacturer
        self._model_number = model_number
        self._serial_number = serial_number
        self._instructions = instructions

    @property
    def name(self) -> str:
        return self._name

    @property
    def code(self) -> Optional[str]:
        return self._code

    @property
    def code_system(self) -> Optional[str]:
        return self._code_system

    @property
    def status(self) -> str:
        return self._status

    @property
    def date_supplied(self) -> Optional[date | datetime]:
        return self._date_supplied

    @property
    def date_end(self) -> Optional[date | datetime]:
        return self._date_end

    @property
    def quantity(self) -> Optional[int]:
        return self._quantity

    @property
    def manufacturer(self) -> Optional[str]:
        return self._manufacturer

    @property
    def model_number(self) -> Optional[str]:
        return self._model_number

    @property
    def serial_number(self) -> Optional[str]:
        return self._serial_number

    @property
    def instructions(self) -> Optional[str]:
        return self._instructions


def test_medical_equipment_protocol_required_fields():
    """Test MedicalEquipmentProtocol required fields."""
    equipment = MockMedicalEquipment()

    assert equipment.name == "Wheelchair"
    assert equipment.status == "completed"


def test_medical_equipment_protocol_satisfaction():
    """Test that MockMedicalEquipment satisfies MedicalEquipmentProtocol."""
    equipment = MockMedicalEquipment()

    def accepts_equipment(e: MedicalEquipmentProtocol) -> str:
        return f"{e.name} - {e.status}"

    result = accepts_equipment(equipment)
    assert result == "Wheelchair - completed"


def test_medical_equipment_with_snomed_code():
    """Test medical equipment with SNOMED CT code."""
    equipment = MockMedicalEquipment(
        name="Insulin Pump",
        code="469821001",
        code_system="SNOMED CT",
    )

    assert equipment.name == "Insulin Pump"
    assert equipment.code == "469821001"
    assert equipment.code_system == "SNOMED CT"


def test_medical_equipment_with_hcpcs_code():
    """Test medical equipment with HCPCS code."""
    equipment = MockMedicalEquipment(
        name="Walker",
        code="E0130",
        code_system="HCPCS",
    )

    assert equipment.code == "E0130"
    assert equipment.code_system == "HCPCS"


def test_medical_equipment_without_code():
    """Test medical equipment without code."""
    equipment = MockMedicalEquipment(
        name="Custom Device",
        code=None,
        code_system=None,
    )

    assert equipment.code is None
    assert equipment.code_system is None


def test_medical_equipment_status_values():
    """Test different status values."""
    completed = MockMedicalEquipment(status="completed")
    active = MockMedicalEquipment(status="active")
    aborted = MockMedicalEquipment(status="aborted")
    cancelled = MockMedicalEquipment(status="cancelled")

    assert completed.status == "completed"
    assert active.status == "active"
    assert aborted.status == "aborted"
    assert cancelled.status == "cancelled"


def test_medical_equipment_with_date_supplied():
    """Test medical equipment with date supplied."""
    equipment = MockMedicalEquipment(
        date_supplied=date(2024, 3, 15),
    )

    assert equipment.date_supplied == date(2024, 3, 15)
    assert isinstance(equipment.date_supplied, date)


def test_medical_equipment_with_datetime_supplied():
    """Test medical equipment with datetime supplied."""
    equipment = MockMedicalEquipment(
        date_supplied=datetime(2024, 3, 15, 10, 30, 0),
    )

    assert equipment.date_supplied == datetime(2024, 3, 15, 10, 30, 0)
    assert isinstance(equipment.date_supplied, datetime)


def test_medical_equipment_without_date_supplied():
    """Test medical equipment without date supplied."""
    equipment = MockMedicalEquipment(date_supplied=None)

    assert equipment.date_supplied is None


def test_medical_equipment_with_date_end():
    """Test medical equipment with end date."""
    equipment = MockMedicalEquipment(
        date_supplied=date(2024, 3, 15),
        date_end=date(2024, 6, 15),
    )

    assert equipment.date_end == date(2024, 6, 15)


def test_medical_equipment_with_datetime_end():
    """Test medical equipment with datetime end."""
    equipment = MockMedicalEquipment(
        date_end=datetime(2024, 6, 15, 16, 0, 0),
    )

    assert equipment.date_end == datetime(2024, 6, 15, 16, 0, 0)


def test_medical_equipment_without_date_end():
    """Test medical equipment without end date (ongoing)."""
    equipment = MockMedicalEquipment(
        date_supplied=date(2024, 3, 15),
        date_end=None,
    )

    assert equipment.date_supplied == date(2024, 3, 15)
    assert equipment.date_end is None


def test_medical_equipment_with_quantity():
    """Test medical equipment with quantity."""
    equipment = MockMedicalEquipment(
        name="Syringes",
        quantity=30,
    )

    assert equipment.quantity == 30


def test_medical_equipment_without_quantity():
    """Test medical equipment without quantity."""
    equipment = MockMedicalEquipment(quantity=None)

    assert equipment.quantity is None


def test_medical_equipment_with_manufacturer():
    """Test medical equipment with manufacturer."""
    equipment = MockMedicalEquipment(
        manufacturer="Acme Medical Devices",
    )

    assert equipment.manufacturer == "Acme Medical Devices"


def test_medical_equipment_without_manufacturer():
    """Test medical equipment without manufacturer."""
    equipment = MockMedicalEquipment(manufacturer=None)

    assert equipment.manufacturer is None


def test_medical_equipment_with_model_number():
    """Test medical equipment with model number."""
    equipment = MockMedicalEquipment(
        model_number="Model XYZ-123",
    )

    assert equipment.model_number == "Model XYZ-123"


def test_medical_equipment_without_model_number():
    """Test medical equipment without model number."""
    equipment = MockMedicalEquipment(model_number=None)

    assert equipment.model_number is None


def test_medical_equipment_with_serial_number():
    """Test medical equipment with serial number."""
    equipment = MockMedicalEquipment(
        serial_number="(01)00643169001763(11)141231(17)150707(10)A213B1(21)1234",
    )

    assert equipment.serial_number == "(01)00643169001763(11)141231(17)150707(10)A213B1(21)1234"


def test_medical_equipment_without_serial_number():
    """Test medical equipment without serial number."""
    equipment = MockMedicalEquipment(serial_number=None)

    assert equipment.serial_number is None


def test_medical_equipment_with_instructions():
    """Test medical equipment with patient instructions."""
    equipment = MockMedicalEquipment(
        name="Blood Glucose Monitor",
        instructions="Check blood glucose before each use",
    )

    assert equipment.instructions == "Check blood glucose before each use"


def test_medical_equipment_without_instructions():
    """Test medical equipment without instructions."""
    equipment = MockMedicalEquipment(instructions=None)

    assert equipment.instructions is None


def test_medical_equipment_insulin_pump_scenario():
    """Test complete insulin pump scenario."""
    equipment = MockMedicalEquipment(
        name="Insulin Pump",
        code="469821001",
        code_system="SNOMED CT",
        status="active",
        date_supplied=date(2024, 1, 15),
        date_end=None,
        quantity=1,
        manufacturer="MedTech Inc",
        model_number="IP-2000",
        serial_number="SN123456789",
        instructions="Rotate infusion sites every 2-3 days. Check basal rates daily.",
    )

    assert equipment.name == "Insulin Pump"
    assert equipment.code == "469821001"
    assert equipment.status == "active"
    assert equipment.quantity == 1
    assert equipment.manufacturer == "MedTech Inc"
    assert equipment.date_end is None


def test_medical_equipment_wheelchair_scenario():
    """Test wheelchair scenario."""
    equipment = MockMedicalEquipment(
        name="Wheelchair",
        code="58938008",
        code_system="SNOMED CT",
        status="completed",
        date_supplied=date(2024, 2, 1),
        quantity=1,
    )

    assert equipment.name == "Wheelchair"
    assert equipment.code == "58938008"
    assert equipment.status == "completed"


def test_medical_equipment_disposable_supplies_scenario():
    """Test disposable supplies scenario."""
    equipment = MockMedicalEquipment(
        name="Alcohol Swabs",
        status="completed",
        date_supplied=date(2024, 3, 10),
        quantity=100,
        instructions="Use before each injection",
    )

    assert equipment.name == "Alcohol Swabs"
    assert equipment.quantity == 100
    assert "injection" in equipment.instructions


def test_medical_equipment_cpap_machine_scenario():
    """Test CPAP machine scenario."""
    equipment = MockMedicalEquipment(
        name="CPAP Machine",
        code="706172005",
        code_system="SNOMED CT",
        status="active",
        date_supplied=date(2024, 1, 5),
        quantity=1,
        manufacturer="Sleep Solutions",
        model_number="CPAP-500",
        serial_number="SN987654321",
        instructions="Use nightly for at least 4 hours. Clean mask weekly.",
    )

    assert equipment.name == "CPAP Machine"
    assert equipment.code == "706172005"
    assert "nightly" in equipment.instructions


def test_medical_equipment_oxygen_concentrator_scenario():
    """Test oxygen concentrator scenario."""
    equipment = MockMedicalEquipment(
        name="Oxygen Concentrator",
        code="426854004",
        code_system="SNOMED CT",
        status="active",
        date_supplied=date(2024, 2, 20),
        manufacturer="OxygenTech",
        model_number="OC-300",
        instructions="Use at 2 liters per minute as prescribed",
    )

    assert equipment.name == "Oxygen Concentrator"
    assert "2 liters" in equipment.instructions


class MinimalMedicalEquipment:
    """Minimal implementation with only required fields."""

    @property
    def name(self) -> str:
        return "Basic Equipment"

    @property
    def code(self) -> Optional[str]:
        return None

    @property
    def code_system(self) -> Optional[str]:
        return None

    @property
    def status(self) -> str:
        return "completed"

    @property
    def date_supplied(self) -> Optional[date | datetime]:
        return None

    @property
    def date_end(self) -> Optional[date | datetime]:
        return None

    @property
    def quantity(self) -> Optional[int]:
        return None

    @property
    def manufacturer(self) -> Optional[str]:
        return None

    @property
    def model_number(self) -> Optional[str]:
        return None

    @property
    def serial_number(self) -> Optional[str]:
        return None

    @property
    def instructions(self) -> Optional[str]:
        return None


def test_minimal_medical_equipment_protocol():
    """Test that minimal implementation satisfies MedicalEquipmentProtocol."""
    equipment = MinimalMedicalEquipment()

    assert equipment.name == "Basic Equipment"
    assert equipment.status == "completed"
    assert equipment.code is None
    assert equipment.code_system is None
    assert equipment.date_supplied is None
    assert equipment.date_end is None
    assert equipment.quantity is None
    assert equipment.manufacturer is None
    assert equipment.model_number is None
    assert equipment.serial_number is None
    assert equipment.instructions is None


def test_minimal_medical_equipment_satisfaction():
    """Test that MinimalMedicalEquipment satisfies MedicalEquipmentProtocol."""
    equipment = MinimalMedicalEquipment()

    def accepts_equipment(e: MedicalEquipmentProtocol) -> str:
        return e.name

    result = accepts_equipment(equipment)
    assert result == "Basic Equipment"


def test_medical_equipment_property_access_multiple_times():
    """Test that properties can be accessed multiple times consistently."""
    equipment = MockMedicalEquipment()

    assert equipment.name == equipment.name
    assert equipment.code == equipment.code
    assert equipment.code_system == equipment.code_system
    assert equipment.status == equipment.status
    assert equipment.date_supplied == equipment.date_supplied
    assert equipment.date_end == equipment.date_end
    assert equipment.quantity == equipment.quantity
    assert equipment.manufacturer == equipment.manufacturer
    assert equipment.model_number == equipment.model_number
    assert equipment.serial_number == equipment.serial_number
    assert equipment.instructions == equipment.instructions


def test_medical_equipment_nebulizer_scenario():
    """Test nebulizer scenario."""
    equipment = MockMedicalEquipment(
        name="Nebulizer",
        code="334980009",
        code_system="SNOMED CT",
        status="completed",
        date_supplied=date(2024, 3, 1),
        quantity=1,
        manufacturer="RespiCare",
        instructions="Clean after each use. Replace filters monthly.",
    )

    assert equipment.name == "Nebulizer"
    assert "Clean after each use" in equipment.instructions


def test_medical_equipment_with_cpt_code():
    """Test medical equipment with CPT code."""
    equipment = MockMedicalEquipment(
        name="Blood Glucose Monitor",
        code="82962",
        code_system="CPT",
    )

    assert equipment.code == "82962"
    assert equipment.code_system == "CPT"


def test_medical_equipment_large_quantity():
    """Test medical equipment with large quantity."""
    equipment = MockMedicalEquipment(
        name="Test Strips",
        quantity=300,
    )

    assert equipment.quantity == 300


def test_medical_equipment_zero_quantity():
    """Test medical equipment with zero quantity (edge case)."""
    equipment = MockMedicalEquipment(
        name="Returned Equipment",
        quantity=0,
    )

    assert equipment.quantity == 0


def test_medical_equipment_multiline_instructions():
    """Test medical equipment with multiline instructions."""
    equipment = MockMedicalEquipment(
        name="Home Dialysis Machine",
        instructions="Step 1: Wash hands thoroughly\nStep 2: Set up machine per manual\nStep 3: Connect tubing\nStep 4: Begin treatment",
    )

    assert "\n" in equipment.instructions
    assert "Step 1" in equipment.instructions
    assert "Step 4" in equipment.instructions
