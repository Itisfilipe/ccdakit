"""Tests for discharge studies protocols."""

from datetime import date, datetime

from ccdakit.protocols.discharge_studies import (
    DischargeStudyObservationProtocol,
    DischargeStudyOrganizerProtocol,
)


class MockDischargeStudyObservation:
    """Test implementation of DischargeStudyObservationProtocol."""

    def __init__(
        self,
        study_name: str = "Chest X-Ray",
        study_code: str = "30746-2",
        value: str = "Clear lungs, no infiltrates",
        unit: str = None,
        status: str = "completed",
        effective_time=None,
        value_type: str = None,
        interpretation: str = None,
        reference_range_low: str = None,
        reference_range_high: str = None,
        reference_range_unit: str = None,
    ):
        self._study_name = study_name
        self._study_code = study_code
        self._value = value
        self._unit = unit
        self._status = status
        self._effective_time = effective_time or datetime(2024, 1, 15, 10, 30)
        self._value_type = value_type
        self._interpretation = interpretation
        self._reference_range_low = reference_range_low
        self._reference_range_high = reference_range_high
        self._reference_range_unit = reference_range_unit

    @property
    def study_name(self):
        return self._study_name

    @property
    def study_code(self):
        return self._study_code

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit

    @property
    def status(self):
        return self._status

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def value_type(self):
        return self._value_type

    @property
    def interpretation(self):
        return self._interpretation

    @property
    def reference_range_low(self):
        return self._reference_range_low

    @property
    def reference_range_high(self):
        return self._reference_range_high

    @property
    def reference_range_unit(self):
        return self._reference_range_unit


class MockDischargeStudyOrganizer:
    """Test implementation of DischargeStudyOrganizerProtocol."""

    def __init__(
        self,
        study_panel_name: str = "Complete Blood Count",
        study_panel_code: str = "57021-8",
        status: str = "completed",
        effective_time=None,
        studies=None,
    ):
        self._study_panel_name = study_panel_name
        self._study_panel_code = study_panel_code
        self._status = status
        self._effective_time = effective_time or datetime(2024, 1, 15, 8, 0)
        self._studies = studies or []

    @property
    def study_panel_name(self):
        return self._study_panel_name

    @property
    def study_panel_code(self):
        return self._study_panel_code

    @property
    def status(self):
        return self._status

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def studies(self):
        return self._studies


def test_discharge_study_observation_required_fields():
    """Test DischargeStudyObservationProtocol required fields."""
    observation = MockDischargeStudyObservation()

    assert observation.study_name == "Chest X-Ray"
    assert observation.study_code == "30746-2"
    assert observation.value == "Clear lungs, no infiltrates"
    assert observation.status == "completed"
    assert observation.effective_time == datetime(2024, 1, 15, 10, 30)


def test_discharge_study_observation_with_numeric_value():
    """Test discharge study observation with numeric value and unit."""
    observation = MockDischargeStudyObservation(
        study_name="Hemoglobin",
        study_code="718-7",
        value="14.5",
        unit="g/dL",
        value_type="PQ",
        interpretation="N",
        reference_range_low="12.0",
        reference_range_high="16.0",
        reference_range_unit="g/dL",
    )

    assert observation.study_name == "Hemoglobin"
    assert observation.study_code == "718-7"
    assert observation.value == "14.5"
    assert observation.unit == "g/dL"
    assert observation.value_type == "PQ"
    assert observation.interpretation == "N"
    assert observation.reference_range_low == "12.0"
    assert observation.reference_range_high == "16.0"
    assert observation.reference_range_unit == "g/dL"


def test_discharge_study_observation_with_text_value():
    """Test discharge study observation with text value."""
    observation = MockDischargeStudyObservation(
        study_name="CT Scan Abdomen",
        study_code="72192-0",
        value="No acute findings. Liver and spleen normal.",
        unit=None,
        value_type="ST",
        interpretation="N",
    )

    assert observation.value == "No acute findings. Liver and spleen normal."
    assert observation.unit is None
    assert observation.value_type == "ST"
    assert observation.interpretation == "N"


def test_discharge_study_observation_with_abnormal_interpretation():
    """Test discharge study observation with abnormal interpretation."""
    observation = MockDischargeStudyObservation(
        study_name="White Blood Cell Count",
        study_code="6690-2",
        value="12.5",
        unit="10*3/uL",
        value_type="PQ",
        interpretation="A",
        reference_range_low="4.5",
        reference_range_high="11.0",
        reference_range_unit="10*3/uL",
    )

    assert observation.interpretation == "A"
    assert float(observation.value) > float(observation.reference_range_high)


def test_discharge_study_observation_with_date():
    """Test discharge study observation with date instead of datetime."""
    study_date = date(2024, 1, 15)
    observation = MockDischargeStudyObservation(
        effective_time=study_date,
    )

    assert observation.effective_time == study_date


def test_discharge_study_observation_imaging_study():
    """Test discharge study observation for imaging study."""
    observation = MockDischargeStudyObservation(
        study_name="Echocardiogram",
        study_code="34552-0",
        value="LVEF 55%, Normal wall motion, No valvular disease",
        unit=None,
        value_type="ST",
        status="final",
        interpretation="N",
    )

    assert observation.study_name == "Echocardiogram"
    assert observation.status == "final"
    assert "LVEF 55%" in observation.value


def test_discharge_study_observation_lab_study():
    """Test discharge study observation for laboratory study."""
    observation = MockDischargeStudyObservation(
        study_name="Troponin I",
        study_code="10839-9",
        value="0.02",
        unit="ng/mL",
        value_type="PQ",
        status="completed",
        interpretation="N",
        reference_range_low="0.00",
        reference_range_high="0.04",
        reference_range_unit="ng/mL",
    )

    assert observation.study_name == "Troponin I"
    assert observation.unit == "ng/mL"
    assert observation.interpretation == "N"


def test_discharge_study_observation_protocol_satisfaction():
    """Test that MockDischargeStudyObservation satisfies protocol."""
    observation = MockDischargeStudyObservation()

    def accepts_observation(obs: DischargeStudyObservationProtocol) -> str:
        return f"{obs.study_name}: {obs.value}"

    result = accepts_observation(observation)
    assert result == "Chest X-Ray: Clear lungs, no infiltrates"


def test_discharge_study_organizer_required_fields():
    """Test DischargeStudyOrganizerProtocol required fields."""
    organizer = MockDischargeStudyOrganizer()

    assert organizer.study_panel_name == "Complete Blood Count"
    assert organizer.study_panel_code == "57021-8"
    assert organizer.status == "completed"
    assert organizer.effective_time == datetime(2024, 1, 15, 8, 0)
    assert organizer.studies == []


def test_discharge_study_organizer_with_studies():
    """Test discharge study organizer with multiple studies."""
    study1 = MockDischargeStudyObservation(
        study_name="Hemoglobin",
        study_code="718-7",
        value="14.5",
        unit="g/dL",
    )
    study2 = MockDischargeStudyObservation(
        study_name="White Blood Cell Count",
        study_code="6690-2",
        value="7.2",
        unit="10*3/uL",
    )
    study3 = MockDischargeStudyObservation(
        study_name="Platelet Count",
        study_code="777-3",
        value="250",
        unit="10*3/uL",
    )

    organizer = MockDischargeStudyOrganizer(
        study_panel_name="Complete Blood Count",
        study_panel_code="57021-8",
        studies=[study1, study2, study3],
    )

    assert len(organizer.studies) == 3
    assert organizer.studies[0].study_name == "Hemoglobin"
    assert organizer.studies[1].study_name == "White Blood Cell Count"
    assert organizer.studies[2].study_name == "Platelet Count"


def test_discharge_study_organizer_metabolic_panel():
    """Test discharge study organizer for metabolic panel."""
    glucose = MockDischargeStudyObservation(
        study_name="Glucose",
        study_code="2345-7",
        value="95",
        unit="mg/dL",
    )
    sodium = MockDischargeStudyObservation(
        study_name="Sodium",
        study_code="2951-2",
        value="140",
        unit="mmol/L",
    )
    potassium = MockDischargeStudyObservation(
        study_name="Potassium",
        study_code="2823-3",
        value="4.2",
        unit="mmol/L",
    )

    organizer = MockDischargeStudyOrganizer(
        study_panel_name="Basic Metabolic Panel",
        study_panel_code="51990-0",
        studies=[glucose, sodium, potassium],
    )

    assert organizer.study_panel_name == "Basic Metabolic Panel"
    assert len(organizer.studies) == 3


def test_discharge_study_organizer_cardiac_panel():
    """Test discharge study organizer for cardiac panel."""
    troponin = MockDischargeStudyObservation(
        study_name="Troponin I",
        study_code="10839-9",
        value="0.02",
        unit="ng/mL",
    )
    bnp = MockDischargeStudyObservation(
        study_name="BNP",
        study_code="30934-4",
        value="85",
        unit="pg/mL",
    )

    organizer = MockDischargeStudyOrganizer(
        study_panel_name="Cardiac Biomarkers",
        study_panel_code="83036-3",
        studies=[troponin, bnp],
    )

    assert organizer.study_panel_name == "Cardiac Biomarkers"
    assert len(organizer.studies) == 2
    assert organizer.studies[0].study_name == "Troponin I"
    assert organizer.studies[1].study_name == "BNP"


def test_discharge_study_organizer_with_date():
    """Test discharge study organizer with date instead of datetime."""
    panel_date = date(2024, 1, 15)
    organizer = MockDischargeStudyOrganizer(
        effective_time=panel_date,
    )

    assert organizer.effective_time == panel_date


def test_discharge_study_organizer_protocol_satisfaction():
    """Test that MockDischargeStudyOrganizer satisfies protocol."""
    study = MockDischargeStudyObservation()
    organizer = MockDischargeStudyOrganizer(studies=[study])

    def accepts_organizer(org: DischargeStudyOrganizerProtocol) -> str:
        return f"{org.study_panel_name} ({len(org.studies)} studies)"

    result = accepts_organizer(organizer)
    assert result == "Complete Blood Count (1 studies)"


class MinimalDischargeStudyObservation:
    """Minimal implementation with only required fields."""

    @property
    def study_name(self):
        return "MRI Brain"

    @property
    def study_code(self):
        return "72133-4"

    @property
    def value(self):
        return "Normal brain anatomy"

    @property
    def unit(self):
        return None

    @property
    def status(self):
        return "completed"

    @property
    def effective_time(self):
        return datetime(2024, 1, 15, 14, 0)

    @property
    def value_type(self):
        return None

    @property
    def interpretation(self):
        return None

    @property
    def reference_range_low(self):
        return None

    @property
    def reference_range_high(self):
        return None

    @property
    def reference_range_unit(self):
        return None


def test_minimal_discharge_study_observation():
    """Test minimal discharge study observation implementation."""
    observation = MinimalDischargeStudyObservation()

    assert observation.study_name == "MRI Brain"
    assert observation.study_code == "72133-4"
    assert observation.value == "Normal brain anatomy"
    assert observation.unit is None
    assert observation.status == "completed"
    assert observation.value_type is None
    assert observation.interpretation is None


class MinimalDischargeStudyOrganizer:
    """Minimal implementation with only required fields."""

    @property
    def study_panel_name(self):
        return "Lipid Panel"

    @property
    def study_panel_code(self):
        return "24331-1"

    @property
    def status(self):
        return "completed"

    @property
    def effective_time(self):
        return datetime(2024, 1, 15, 9, 0)

    @property
    def studies(self):
        return []


def test_minimal_discharge_study_organizer():
    """Test minimal discharge study organizer implementation."""
    organizer = MinimalDischargeStudyOrganizer()

    assert organizer.study_panel_name == "Lipid Panel"
    assert organizer.study_panel_code == "24331-1"
    assert organizer.status == "completed"
    assert len(organizer.studies) == 0


def test_discharge_study_observation_preliminary_status():
    """Test discharge study observation with preliminary status."""
    observation = MockDischargeStudyObservation(
        study_name="Blood Culture",
        study_code="600-7",
        value="Pending final results",
        status="preliminary",
    )

    assert observation.status == "preliminary"


def test_discharge_study_observation_various_interpretations():
    """Test discharge study observations with various interpretations."""
    normal = MockDischargeStudyObservation(interpretation="N")
    abnormal = MockDischargeStudyObservation(interpretation="A")
    high = MockDischargeStudyObservation(interpretation="H")
    low = MockDischargeStudyObservation(interpretation="L")

    assert normal.interpretation == "N"
    assert abnormal.interpretation == "A"
    assert high.interpretation == "H"
    assert low.interpretation == "L"


def test_discharge_study_observation_coded_value():
    """Test discharge study observation with coded value."""
    observation = MockDischargeStudyObservation(
        study_name="Blood Type",
        study_code="882-1",
        value="A positive",
        unit=None,
        value_type="CD",
    )

    assert observation.value_type == "CD"
    assert observation.unit is None


def test_complex_discharge_studies_workflow():
    """Test a complete workflow with multiple organizers and observations."""
    # Create lab studies
    lab1 = MockDischargeStudyObservation(
        study_name="Hemoglobin", study_code="718-7", value="13.5", unit="g/dL"
    )
    lab2 = MockDischargeStudyObservation(
        study_name="WBC", study_code="6690-2", value="8.0", unit="10*3/uL"
    )
    lab_panel = MockDischargeStudyOrganizer(
        study_panel_name="CBC",
        study_panel_code="57021-8",
        studies=[lab1, lab2],
    )

    # Create imaging studies
    xray = MockDischargeStudyObservation(
        study_name="Chest X-Ray",
        study_code="30746-2",
        value="Clear",
        value_type="ST",
    )
    imaging_panel = MockDischargeStudyOrganizer(
        study_panel_name="Chest Imaging",
        study_panel_code="11522-0",
        studies=[xray],
    )

    # Verify structure
    assert len(lab_panel.studies) == 2
    assert len(imaging_panel.studies) == 1
    assert lab_panel.studies[0].unit == "g/dL"
    assert imaging_panel.studies[0].value_type == "ST"
