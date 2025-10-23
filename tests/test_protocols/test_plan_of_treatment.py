"""Tests for plan of treatment protocols."""

from datetime import date
from typing import Optional

from ccdakit.protocols.plan_of_treatment import (
    InstructionProtocol,
    PersistentIDProtocol,
    PlannedActProtocol,
    PlannedActivityProtocol,
    PlannedEncounterProtocol,
    PlannedImmunizationProtocol,
    PlannedMedicationProtocol,
    PlannedObservationProtocol,
    PlannedProcedureProtocol,
    PlannedSupplyProtocol,
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


class MockPlannedObservation:
    """Test implementation of PlannedObservationProtocol."""

    def __init__(
        self,
        description: str = "Blood glucose monitoring",
        code: Optional[str] = "15074-8",
        code_system: Optional[str] = "LOINC",
        planned_date: Optional[date] = date(2024, 4, 1),
        status: str = "active",
        persistent_id: Optional[PersistentIDProtocol] = None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPlannedProcedure:
    """Test implementation of PlannedProcedureProtocol."""

    def __init__(
        self,
        description: str = "Colonoscopy",
        code: Optional[str] = "73761001",
        code_system: Optional[str] = "SNOMED",
        planned_date: Optional[date] = date(2024, 5, 15),
        status: str = "active",
        body_site: Optional[str] = "Colon",
        persistent_id: Optional[PersistentIDProtocol] = None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._body_site = body_site
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def body_site(self):
        return self._body_site

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPlannedEncounter:
    """Test implementation of PlannedEncounterProtocol."""

    def __init__(
        self,
        description: str = "Follow-up visit",
        code: Optional[str] = "185349003",
        code_system: Optional[str] = "SNOMED",
        planned_date: Optional[date] = date(2024, 4, 15),
        status: str = "active",
        encounter_type: Optional[str] = "office visit",
        persistent_id: Optional[PersistentIDProtocol] = None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._encounter_type = encounter_type
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def encounter_type(self):
        return self._encounter_type

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPlannedAct:
    """Test implementation of PlannedActProtocol."""

    def __init__(
        self,
        description: str = "Patient education",
        code: Optional[str] = "311401005",
        code_system: Optional[str] = "SNOMED",
        planned_date: Optional[date] = date(2024, 4, 1),
        status: str = "active",
        persistent_id: Optional[PersistentIDProtocol] = None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPlannedMedication:
    """Test implementation of PlannedMedicationProtocol."""

    def __init__(
        self,
        description: str = "Lisinopril 10mg oral tablet",
        code: Optional[str] = "314076",
        code_system: Optional[str] = "RXNORM",
        planned_date: Optional[date] = None,
        status: str = "active",
        dose: Optional[str] = "10 mg",
        route: Optional[str] = "PO",
        frequency: Optional[str] = "once daily",
        persistent_id: Optional[PersistentIDProtocol] = None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._dose = dose
        self._route = route
        self._frequency = frequency
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def dose(self):
        return self._dose

    @property
    def route(self):
        return self._route

    @property
    def frequency(self):
        return self._frequency

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPlannedSupply:
    """Test implementation of PlannedSupplyProtocol."""

    def __init__(
        self,
        description: str = "Wheelchair",
        code: Optional[str] = "58938008",
        code_system: Optional[str] = "SNOMED",
        planned_date: Optional[date] = date(2024, 4, 1),
        status: str = "active",
        quantity: Optional[str] = "1",
        persistent_id: Optional[PersistentIDProtocol] = None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._quantity = quantity
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def quantity(self):
        return self._quantity

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPlannedImmunization:
    """Test implementation of PlannedImmunizationProtocol."""

    def __init__(
        self,
        description: str = "Influenza vaccine",
        code: Optional[str] = "88",
        code_system: Optional[str] = "CVX",
        planned_date: Optional[date] = date(2024, 10, 1),
        status: str = "active",
        vaccine_code: Optional[str] = "88",
        persistent_id: Optional[PersistentIDProtocol] = None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._planned_date = planned_date
        self._status = status
        self._vaccine_code = vaccine_code
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def status(self):
        return self._status

    @property
    def vaccine_code(self):
        return self._vaccine_code

    @property
    def persistent_id(self):
        return self._persistent_id


class MockInstruction:
    """Test implementation of InstructionProtocol."""

    def __init__(
        self,
        instruction_text: str = "Take medication with food",
        persistent_id: Optional[PersistentIDProtocol] = None,
    ):
        self._instruction_text = instruction_text
        self._persistent_id = persistent_id

    @property
    def instruction_text(self):
        return self._instruction_text

    @property
    def persistent_id(self):
        return self._persistent_id


# Persistent ID tests
def test_persistent_id_protocol():
    """Test PersistentIDProtocol implementation."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "POT-123")

    assert pid.root == "2.16.840.1.113883.3.TEST"
    assert pid.extension == "POT-123"


def test_persistent_id_protocol_satisfaction():
    """Test that MockPersistentID satisfies PersistentIDProtocol."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "POT-123")

    def accepts_pid(p: PersistentIDProtocol) -> str:
        return f"{p.root}^{p.extension}"

    result = accepts_pid(pid)
    assert result == "2.16.840.1.113883.3.TEST^POT-123"


# Planned Observation tests
def test_planned_observation_required_fields():
    """Test PlannedObservationProtocol required fields."""
    obs = MockPlannedObservation()

    assert obs.description == "Blood glucose monitoring"
    assert obs.status == "active"


def test_planned_observation_with_all_fields():
    """Test PlannedObservationProtocol with all fields."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "OBS-123")
    obs = MockPlannedObservation(
        description="HbA1c test",
        code="4548-4",
        code_system="LOINC",
        planned_date=date(2024, 6, 1),
        status="active",
        persistent_id=pid,
    )

    assert obs.description == "HbA1c test"
    assert obs.code == "4548-4"
    assert obs.code_system == "LOINC"
    assert obs.planned_date == date(2024, 6, 1)
    assert obs.persistent_id is not None


def test_planned_observation_protocol_satisfaction():
    """Test that MockPlannedObservation satisfies PlannedObservationProtocol."""
    obs = MockPlannedObservation()

    def accepts_obs(o: PlannedObservationProtocol) -> str:
        return f"{o.description} - {o.status}"

    result = accepts_obs(obs)
    assert result == "Blood glucose monitoring - active"


# Planned Procedure tests
def test_planned_procedure_required_fields():
    """Test PlannedProcedureProtocol required fields."""
    proc = MockPlannedProcedure()

    assert proc.description == "Colonoscopy"
    assert proc.status == "active"


def test_planned_procedure_with_body_site():
    """Test PlannedProcedureProtocol with body site."""
    proc = MockPlannedProcedure(
        description="Appendectomy",
        body_site="Appendix",
    )

    assert proc.body_site == "Appendix"


def test_planned_procedure_protocol_satisfaction():
    """Test that MockPlannedProcedure satisfies PlannedProcedureProtocol."""
    proc = MockPlannedProcedure()

    def accepts_proc(p: PlannedProcedureProtocol) -> str:
        return f"{p.description}"

    result = accepts_proc(proc)
    assert result == "Colonoscopy"


# Planned Encounter tests
def test_planned_encounter_required_fields():
    """Test PlannedEncounterProtocol required fields."""
    enc = MockPlannedEncounter()

    assert enc.description == "Follow-up visit"
    assert enc.status == "active"


def test_planned_encounter_with_type():
    """Test PlannedEncounterProtocol with encounter type."""
    enc = MockPlannedEncounter(
        description="Annual physical",
        encounter_type="office visit",
    )

    assert enc.encounter_type == "office visit"


def test_planned_encounter_protocol_satisfaction():
    """Test that MockPlannedEncounter satisfies PlannedEncounterProtocol."""
    enc = MockPlannedEncounter()

    def accepts_enc(e: PlannedEncounterProtocol) -> str:
        return f"{e.description}"

    result = accepts_enc(enc)
    assert result == "Follow-up visit"


# Planned Act tests
def test_planned_act_required_fields():
    """Test PlannedActProtocol required fields."""
    act = MockPlannedAct()

    assert act.description == "Patient education"
    assert act.status == "active"


def test_planned_act_protocol_satisfaction():
    """Test that MockPlannedAct satisfies PlannedActProtocol."""
    act = MockPlannedAct()

    def accepts_act(a: PlannedActProtocol) -> str:
        return f"{a.description}"

    result = accepts_act(act)
    assert result == "Patient education"


# Planned Medication tests
def test_planned_medication_required_fields():
    """Test PlannedMedicationProtocol required fields."""
    med = MockPlannedMedication()

    assert med.description == "Lisinopril 10mg oral tablet"
    assert med.status == "active"


def test_planned_medication_with_details():
    """Test PlannedMedicationProtocol with medication details."""
    med = MockPlannedMedication(
        description="Metformin 500mg",
        dose="500 mg",
        route="PO",
        frequency="twice daily",
    )

    assert med.dose == "500 mg"
    assert med.route == "PO"
    assert med.frequency == "twice daily"


def test_planned_medication_protocol_satisfaction():
    """Test that MockPlannedMedication satisfies PlannedMedicationProtocol."""
    med = MockPlannedMedication()

    def accepts_med(m: PlannedMedicationProtocol) -> str:
        return f"{m.description}"

    result = accepts_med(med)
    assert result == "Lisinopril 10mg oral tablet"


# Planned Supply tests
def test_planned_supply_required_fields():
    """Test PlannedSupplyProtocol required fields."""
    supply = MockPlannedSupply()

    assert supply.description == "Wheelchair"
    assert supply.status == "active"


def test_planned_supply_with_quantity():
    """Test PlannedSupplyProtocol with quantity."""
    supply = MockPlannedSupply(
        description="Glucose test strips",
        quantity="100",
    )

    assert supply.quantity == "100"


def test_planned_supply_protocol_satisfaction():
    """Test that MockPlannedSupply satisfies PlannedSupplyProtocol."""
    supply = MockPlannedSupply()

    def accepts_supply(s: PlannedSupplyProtocol) -> str:
        return f"{s.description}"

    result = accepts_supply(supply)
    assert result == "Wheelchair"


# Planned Immunization tests
def test_planned_immunization_required_fields():
    """Test PlannedImmunizationProtocol required fields."""
    imm = MockPlannedImmunization()

    assert imm.description == "Influenza vaccine"
    assert imm.status == "active"


def test_planned_immunization_with_vaccine_code():
    """Test PlannedImmunizationProtocol with vaccine code."""
    imm = MockPlannedImmunization(
        description="COVID-19 vaccine",
        vaccine_code="213",
    )

    assert imm.vaccine_code == "213"


def test_planned_immunization_protocol_satisfaction():
    """Test that MockPlannedImmunization satisfies PlannedImmunizationProtocol."""
    imm = MockPlannedImmunization()

    def accepts_imm(i: PlannedImmunizationProtocol) -> str:
        return f"{i.description}"

    result = accepts_imm(imm)
    assert result == "Influenza vaccine"


# Instruction tests
def test_instruction_required_fields():
    """Test InstructionProtocol required fields."""
    inst = MockInstruction()

    assert inst.instruction_text == "Take medication with food"


def test_instruction_with_persistent_id():
    """Test InstructionProtocol with persistent ID."""
    pid = MockPersistentID("2.16.840.1.113883.3.TEST", "INST-123")
    inst = MockInstruction(
        instruction_text="Follow low sodium diet",
        persistent_id=pid,
    )

    assert inst.persistent_id is not None
    assert inst.persistent_id.root == "2.16.840.1.113883.3.TEST"


def test_instruction_protocol_satisfaction():
    """Test that MockInstruction satisfies InstructionProtocol."""
    inst = MockInstruction()

    def accepts_inst(i: InstructionProtocol) -> str:
        return i.instruction_text

    result = accepts_inst(inst)
    assert result == "Take medication with food"


# Test different statuses
def test_planned_activity_different_statuses():
    """Test planned activities with different statuses."""
    active = MockPlannedObservation(status="active")
    cancelled = MockPlannedObservation(status="cancelled")
    completed = MockPlannedObservation(status="completed")

    assert active.status == "active"
    assert cancelled.status == "cancelled"
    assert completed.status == "completed"


# Test optional fields as None
def test_planned_observation_optional_fields_none():
    """Test PlannedObservationProtocol with optional fields as None."""
    obs = MockPlannedObservation(
        code=None,
        code_system=None,
        planned_date=None,
        persistent_id=None,
    )

    assert obs.code is None
    assert obs.code_system is None
    assert obs.planned_date is None
    assert obs.persistent_id is None


def test_planned_procedure_optional_fields_none():
    """Test PlannedProcedureProtocol with optional fields as None."""
    proc = MockPlannedProcedure(
        body_site=None,
        code=None,
        persistent_id=None,
    )

    assert proc.body_site is None
    assert proc.code is None
    assert proc.persistent_id is None


def test_planned_medication_optional_fields_none():
    """Test PlannedMedicationProtocol with optional fields as None."""
    med = MockPlannedMedication(
        dose=None,
        route=None,
        frequency=None,
        code=None,
        persistent_id=None,
    )

    assert med.dose is None
    assert med.route is None
    assert med.frequency is None
    assert med.code is None
    assert med.persistent_id is None


def test_instruction_optional_fields_none():
    """Test InstructionProtocol with optional fields as None."""
    inst = MockInstruction(persistent_id=None)

    assert inst.persistent_id is None


# Property access tests
def test_planned_activity_property_access():
    """Test accessing all PlannedActivityProtocol properties."""
    obs = MockPlannedObservation()

    assert isinstance(obs.description, str)
    assert obs.code is None or isinstance(obs.code, str)
    assert obs.code_system is None or isinstance(obs.code_system, str)
    assert obs.planned_date is None or isinstance(obs.planned_date, date)
    assert isinstance(obs.status, str)
    assert obs.persistent_id is None or hasattr(obs.persistent_id, "root")


def test_planned_medication_property_access():
    """Test accessing all PlannedMedicationProtocol properties."""
    med = MockPlannedMedication()

    assert isinstance(med.description, str)
    assert isinstance(med.status, str)
    assert med.dose is None or isinstance(med.dose, str)
    assert med.route is None or isinstance(med.route, str)
    assert med.frequency is None or isinstance(med.frequency, str)
