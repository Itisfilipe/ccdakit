"""Tests for medication administered protocols."""

from datetime import datetime
from typing import Optional

from ccdakit.protocols.medication_administered import MedicationAdministeredProtocol


class MockMedicationAdministered:
    """Test implementation of MedicationAdministeredProtocol."""

    def __init__(
        self,
        name: str = "Ondansetron 4mg/2mL injection",
        code: str = "312086",
        administration_time: datetime = datetime(2024, 3, 15, 14, 30),
        dose: str = "4 mg",
        route: str = "IV",
        status: str = "completed",
        administration_end_time: Optional[datetime] = None,
        rate: Optional[str] = None,
        site: Optional[str] = None,
        performer: Optional[str] = None,
        indication: Optional[str] = None,
        instructions: Optional[str] = None,
    ):
        self._name = name
        self._code = code
        self._administration_time = administration_time
        self._administration_end_time = administration_end_time
        self._dose = dose
        self._route = route
        self._rate = rate
        self._site = site
        self._status = status
        self._performer = performer
        self._indication = indication
        self._instructions = instructions

    @property
    def name(self) -> str:
        return self._name

    @property
    def code(self) -> str:
        return self._code

    @property
    def administration_time(self) -> datetime:
        return self._administration_time

    @property
    def administration_end_time(self) -> Optional[datetime]:
        return self._administration_end_time

    @property
    def dose(self) -> str:
        return self._dose

    @property
    def route(self) -> str:
        return self._route

    @property
    def rate(self) -> Optional[str]:
        return self._rate

    @property
    def site(self) -> Optional[str]:
        return self._site

    @property
    def status(self) -> str:
        return self._status

    @property
    def performer(self) -> Optional[str]:
        return self._performer

    @property
    def indication(self) -> Optional[str]:
        return self._indication

    @property
    def instructions(self) -> Optional[str]:
        return self._instructions


def test_medication_administered_protocol_required_fields():
    """Test MedicationAdministeredProtocol required fields."""
    med = MockMedicationAdministered()

    assert med.name == "Ondansetron 4mg/2mL injection"
    assert med.code == "312086"
    assert med.administration_time == datetime(2024, 3, 15, 14, 30)
    assert med.dose == "4 mg"
    assert med.route == "IV"
    assert med.status == "completed"


def test_medication_administered_protocol_optional_fields():
    """Test MedicationAdministeredProtocol optional fields with values."""
    med = MockMedicationAdministered(
        administration_end_time=datetime(2024, 3, 15, 14, 45),
        rate="100 mL/hr",
        site="left antecubital fossa",
        performer="Jane Smith, RN",
        indication="Nausea",
        instructions="Push slowly over 2 minutes",
    )

    assert med.administration_end_time == datetime(2024, 3, 15, 14, 45)
    assert med.rate == "100 mL/hr"
    assert med.site == "left antecubital fossa"
    assert med.performer == "Jane Smith, RN"
    assert med.indication == "Nausea"
    assert med.instructions == "Push slowly over 2 minutes"


def test_medication_administered_protocol_optional_fields_none():
    """Test MedicationAdministeredProtocol optional fields when None."""
    med = MockMedicationAdministered()

    assert med.administration_end_time is None
    assert med.rate is None
    assert med.site is None
    assert med.performer is None
    assert med.indication is None
    assert med.instructions is None


def test_medication_administered_protocol_satisfaction():
    """Test that MockMedicationAdministered satisfies MedicationAdministeredProtocol."""
    med = MockMedicationAdministered()

    def accepts_medication(m: MedicationAdministeredProtocol) -> str:
        return f"{m.name} at {m.administration_time}"

    result = accepts_medication(med)
    assert result == "Ondansetron 4mg/2mL injection at 2024-03-15 14:30:00"


def test_iv_fluid_administration():
    """Test IV fluid administration scenario."""
    normal_saline = MockMedicationAdministered(
        name="Normal Saline 0.9% IV Solution",
        code="313002",
        administration_time=datetime(2024, 3, 15, 10, 0),
        administration_end_time=datetime(2024, 3, 15, 12, 0),
        dose="1000 mL",
        route="IV",
        rate="100 mL/hr",
        site="right forearm",
        status="completed",
        performer="Dr. Robert Jones",
        indication="Dehydration",
    )

    assert normal_saline.name == "Normal Saline 0.9% IV Solution"
    assert normal_saline.dose == "1000 mL"
    assert normal_saline.rate == "100 mL/hr"
    assert normal_saline.administration_end_time == datetime(2024, 3, 15, 12, 0)


def test_precoordinated_medication():
    """Test pre-coordinated medication where dose is a count."""
    acetaminophen = MockMedicationAdministered(
        name="Acetaminophen 325mg oral tablet",
        code="197806",
        administration_time=datetime(2024, 3, 15, 9, 0),
        dose="2",  # 2 tablets
        route="PO",
        status="completed",
        indication="Pain management",
    )

    assert acetaminophen.dose == "2"
    assert acetaminophen.route == "PO"


def test_emergency_medication_administration():
    """Test emergency medication administration."""
    epinephrine = MockMedicationAdministered(
        name="Epinephrine 1mg/mL injection",
        code="727316",
        administration_time=datetime(2024, 3, 15, 15, 45),
        dose="0.3 mg",
        route="IM",
        site="right deltoid",
        status="completed",
        performer="Dr. Sarah Johnson",
        indication="Anaphylaxis",
        instructions="Administer immediately",
    )

    assert epinephrine.indication == "Anaphylaxis"
    assert epinephrine.instructions == "Administer immediately"
    assert epinephrine.site == "right deltoid"
    assert epinephrine.route == "IM"


def test_contrast_agent_administration():
    """Test contrast agent administration during imaging."""
    contrast = MockMedicationAdministered(
        name="Iohexol 300mg/mL injection",
        code="153165",
        administration_time=datetime(2024, 3, 15, 11, 15),
        dose="100 mL",
        route="IV",
        rate="2 mL/sec",
        status="completed",
        performer="Radiology Tech",
        indication="CT scan with contrast",
    )

    assert contrast.name == "Iohexol 300mg/mL injection"
    assert contrast.rate == "2 mL/sec"
    assert contrast.indication == "CT scan with contrast"


def test_multiple_medications_different_times():
    """Test scenario with multiple medication administrations."""
    meds = [
        MockMedicationAdministered(
            name="Ondansetron 4mg injection",
            code="312086",
            administration_time=datetime(2024, 3, 15, 8, 0),
            dose="4 mg",
            route="IV",
            status="completed",
        ),
        MockMedicationAdministered(
            name="Acetaminophen 325mg tablet",
            code="197806",
            administration_time=datetime(2024, 3, 15, 12, 0),
            dose="2",
            route="PO",
            status="completed",
        ),
        MockMedicationAdministered(
            name="Morphine 2mg injection",
            code="861467",
            administration_time=datetime(2024, 3, 15, 14, 0),
            dose="2 mg",
            route="IV",
            status="completed",
        ),
    ]

    assert len(meds) == 3
    assert all(m.status == "completed" for m in meds)
    assert meds[0].administration_time < meds[1].administration_time
    assert meds[1].administration_time < meds[2].administration_time


def test_medication_with_all_fields():
    """Test medication with all fields populated."""
    med = MockMedicationAdministered(
        name="Fentanyl 100mcg/2mL injection",
        code="245134",
        administration_time=datetime(2024, 3, 15, 13, 30),
        administration_end_time=datetime(2024, 3, 15, 13, 35),
        dose="50 mcg",
        route="IV",
        rate="slow push",
        site="left forearm",
        status="completed",
        performer="Dr. Michael Chen",
        indication="Pain management",
        instructions="Administer over 2-3 minutes, monitor for respiratory depression",
    )

    # Verify all fields are set
    assert med.name is not None
    assert med.code is not None
    assert med.administration_time is not None
    assert med.administration_end_time is not None
    assert med.dose is not None
    assert med.route is not None
    assert med.rate is not None
    assert med.site is not None
    assert med.status is not None
    assert med.performer is not None
    assert med.indication is not None
    assert med.instructions is not None


def test_aborted_medication_administration():
    """Test scenario where medication administration was aborted."""
    med = MockMedicationAdministered(
        name="Propofol 10mg/mL injection",
        code="153476",
        administration_time=datetime(2024, 3, 15, 16, 0),
        dose="20 mg",
        route="IV",
        status="aborted",
        performer="Dr. Lisa Anderson",
        instructions="Administration stopped due to adverse reaction",
    )

    assert med.status == "aborted"
    assert "adverse reaction" in med.instructions


def test_protocol_with_custom_implementation():
    """Test that custom implementations satisfy the protocol."""

    class CustomMedication:
        @property
        def name(self) -> str:
            return "Custom Medication"

        @property
        def code(self) -> str:
            return "12345"

        @property
        def administration_time(self) -> datetime:
            return datetime(2024, 1, 1, 12, 0)

        @property
        def administration_end_time(self) -> Optional[datetime]:
            return None

        @property
        def dose(self) -> str:
            return "10 mg"

        @property
        def route(self) -> str:
            return "PO"

        @property
        def rate(self) -> Optional[str]:
            return None

        @property
        def site(self) -> Optional[str]:
            return None

        @property
        def status(self) -> str:
            return "completed"

        @property
        def performer(self) -> Optional[str]:
            return None

        @property
        def indication(self) -> Optional[str]:
            return None

        @property
        def instructions(self) -> Optional[str]:
            return None

    custom = CustomMedication()

    def accepts_protocol(m: MedicationAdministeredProtocol) -> bool:
        return m.name == "Custom Medication"

    assert accepts_protocol(custom) is True


def test_medication_administered_protocol_property_access():
    """Test accessing all protocol properties directly."""
    med = MockMedicationAdministered(
        name="Test Medication",
        code="12345",
        administration_time=datetime(2024, 1, 1, 10, 0),
        administration_end_time=datetime(2024, 1, 1, 10, 30),
        dose="10 mg",
        route="IV",
        rate="5 mL/min",
        site="left arm",
        status="completed",
        performer="Nurse Smith",
        indication="Pain",
        instructions="Administer slowly",
    )

    # Access all properties to ensure protocol coverage
    assert isinstance(med.name, str)
    assert isinstance(med.code, str)
    assert isinstance(med.administration_time, datetime)
    assert med.administration_end_time is None or isinstance(med.administration_end_time, datetime)
    assert isinstance(med.dose, str)
    assert isinstance(med.route, str)
    assert med.rate is None or isinstance(med.rate, str)
    assert med.site is None or isinstance(med.site, str)
    assert isinstance(med.status, str)
    assert med.performer is None or isinstance(med.performer, str)
    assert med.indication is None or isinstance(med.indication, str)
    assert med.instructions is None or isinstance(med.instructions, str)


def test_medication_administered_different_statuses():
    """Test medication administered with different status values."""
    completed = MockMedicationAdministered(status="completed")
    active = MockMedicationAdministered(status="active")
    aborted = MockMedicationAdministered(status="aborted")
    held = MockMedicationAdministered(status="held")

    assert completed.status == "completed"
    assert active.status == "active"
    assert aborted.status == "aborted"
    assert held.status == "held"


def test_medication_administered_different_routes():
    """Test medication administered with different routes."""
    oral = MockMedicationAdministered(route="PO")
    iv = MockMedicationAdministered(route="IV")
    im = MockMedicationAdministered(route="IM")
    subcutaneous = MockMedicationAdministered(route="SC")
    topical = MockMedicationAdministered(route="TOPICAL")

    assert oral.route == "PO"
    assert iv.route == "IV"
    assert im.route == "IM"
    assert subcutaneous.route == "SC"
    assert topical.route == "TOPICAL"


def test_medication_administered_with_body_site_codes():
    """Test medication administered with coded body sites."""
    right_arm = MockMedicationAdministered(site="368209003")
    left_deltoid = MockMedicationAdministered(site="left deltoid")
    antecubital = MockMedicationAdministered(site="left antecubital fossa")

    assert right_arm.site == "368209003"
    assert left_deltoid.site == "left deltoid"
    assert antecubital.site == "left antecubital fossa"


def test_medication_infusion_with_rate():
    """Test medication infusion with specific rate."""
    infusion = MockMedicationAdministered(
        name="Heparin 25000 units in 250 mL D5W",
        code="5224",
        administration_time=datetime(2024, 3, 15, 8, 0),
        administration_end_time=datetime(2024, 3, 15, 20, 0),
        dose="25000 units",
        route="IV",
        rate="1000 units/hr",
        status="completed",
    )

    assert infusion.rate == "1000 units/hr"
    assert infusion.administration_end_time is not None
    assert (infusion.administration_end_time - infusion.administration_time).total_seconds() == 12 * 3600


def test_medication_administered_minimal_data():
    """Test medication administered with minimal required data only."""
    minimal = MockMedicationAdministered(
        name="Aspirin",
        code="1191",
        administration_time=datetime(2024, 3, 15, 9, 0),
        dose="81 mg",
        route="PO",
        status="completed",
    )

    assert minimal.name == "Aspirin"
    assert minimal.code == "1191"
    assert minimal.dose == "81 mg"
    assert minimal.route == "PO"
    assert minimal.status == "completed"
    assert minimal.administration_end_time is None
    assert minimal.rate is None
    assert minimal.site is None
    assert minimal.performer is None
    assert minimal.indication is None
    assert minimal.instructions is None
