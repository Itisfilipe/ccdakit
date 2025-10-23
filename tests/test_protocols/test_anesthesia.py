"""Tests for anesthesia protocols."""

from datetime import date, datetime

from ccdakit.protocols.anesthesia import AnesthesiaProtocol
from ccdakit.protocols.medication import MedicationProtocol


class MockMedication:
    """Test implementation of MedicationProtocol for anesthesia agents."""

    def __init__(
        self,
        name: str = "Propofol 10mg/mL injection",
        code: str = "153476",
        dosage: str = "200 mg",
        route: str = "Intravenous",
        frequency: str = "single dose",
        start_date: date = None,
        end_date: date = None,
        status: str = "completed",
        instructions: str = None,
    ):
        self._name = name
        self._code = code
        self._dosage = dosage
        self._route = route
        self._frequency = frequency
        self._start_date = start_date or date(2024, 1, 15)
        self._end_date = end_date
        self._status = status
        self._instructions = instructions

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def dosage(self):
        return self._dosage

    @property
    def route(self):
        return self._route

    @property
    def frequency(self):
        return self._frequency

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def status(self):
        return self._status

    @property
    def instructions(self):
        return self._instructions


class MockAnesthesia:
    """Test implementation of AnesthesiaProtocol."""

    def __init__(
        self,
        anesthesia_type: str = "General anesthesia",
        anesthesia_code: str = "50697003",
        anesthesia_code_system: str = "SNOMED CT",
        start_time: date | datetime | None = None,
        end_time: date | datetime | None = None,
        status: str = "completed",
        anesthesia_agents: list[MedicationProtocol] | None = None,
        route: str | None = None,
        performer_name: str | None = None,
        notes: str | None = None,
    ):
        self._anesthesia_type = anesthesia_type
        self._anesthesia_code = anesthesia_code
        self._anesthesia_code_system = anesthesia_code_system
        self._start_time = start_time or datetime(2024, 1, 15, 9, 0, 0)
        self._end_time = end_time or datetime(2024, 1, 15, 11, 30, 0)
        self._status = status
        self._anesthesia_agents = anesthesia_agents
        self._route = route
        self._performer_name = performer_name
        self._notes = notes

    @property
    def anesthesia_type(self):
        return self._anesthesia_type

    @property
    def anesthesia_code(self):
        return self._anesthesia_code

    @property
    def anesthesia_code_system(self):
        return self._anesthesia_code_system

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def status(self):
        return self._status

    @property
    def anesthesia_agents(self):
        return self._anesthesia_agents

    @property
    def route(self):
        return self._route

    @property
    def performer_name(self):
        return self._performer_name

    @property
    def notes(self):
        return self._notes


def test_anesthesia_protocol_required_fields():
    """Test AnesthesiaProtocol required fields."""
    anesthesia = MockAnesthesia()

    assert anesthesia.anesthesia_type == "General anesthesia"
    assert anesthesia.anesthesia_code == "50697003"
    assert anesthesia.anesthesia_code_system == "SNOMED CT"
    assert anesthesia.status == "completed"


def test_anesthesia_protocol_with_datetime():
    """Test AnesthesiaProtocol with datetime start and end times."""
    start = datetime(2024, 3, 15, 8, 30, 0)
    end = datetime(2024, 3, 15, 10, 45, 0)
    anesthesia = MockAnesthesia(start_time=start, end_time=end)

    assert anesthesia.start_time == start
    assert anesthesia.end_time == end
    assert isinstance(anesthesia.start_time, datetime)
    assert isinstance(anesthesia.end_time, datetime)


def test_anesthesia_protocol_with_date():
    """Test AnesthesiaProtocol with date (not datetime) for times."""
    start = date(2024, 3, 15)
    end = date(2024, 3, 15)
    anesthesia = MockAnesthesia(start_time=start, end_time=end)

    assert anesthesia.start_time == start
    assert anesthesia.end_time == end


def test_anesthesia_protocol_general_anesthesia():
    """Test AnesthesiaProtocol for general anesthesia."""
    anesthesia = MockAnesthesia(
        anesthesia_type="General anesthesia",
        anesthesia_code="50697003",
        anesthesia_code_system="SNOMED CT",
        status="completed",
    )

    assert anesthesia.anesthesia_type == "General anesthesia"
    assert anesthesia.anesthesia_code == "50697003"
    assert anesthesia.status == "completed"


def test_anesthesia_protocol_local_anesthesia():
    """Test AnesthesiaProtocol for local anesthesia."""
    anesthesia = MockAnesthesia(
        anesthesia_type="Local anesthesia",
        anesthesia_code="386761002",
        anesthesia_code_system="SNOMED CT",
    )

    assert anesthesia.anesthesia_type == "Local anesthesia"
    assert anesthesia.anesthesia_code == "386761002"


def test_anesthesia_protocol_regional_anesthesia():
    """Test AnesthesiaProtocol for regional anesthesia."""
    anesthesia = MockAnesthesia(
        anesthesia_type="Regional anesthesia",
        anesthesia_code="231249005",
        anesthesia_code_system="SNOMED CT",
    )

    assert anesthesia.anesthesia_type == "Regional anesthesia"
    assert anesthesia.anesthesia_code == "231249005"


def test_anesthesia_protocol_spinal_anesthesia():
    """Test AnesthesiaProtocol for spinal anesthesia."""
    anesthesia = MockAnesthesia(
        anesthesia_type="Spinal anesthesia",
        anesthesia_code="112943005",
        anesthesia_code_system="SNOMED CT",
    )

    assert anesthesia.anesthesia_type == "Spinal anesthesia"
    assert anesthesia.anesthesia_code == "112943005"


def test_anesthesia_protocol_epidural_anesthesia():
    """Test AnesthesiaProtocol for epidural anesthesia."""
    anesthesia = MockAnesthesia(
        anesthesia_type="Epidural anesthesia",
        anesthesia_code="18946005",
        anesthesia_code_system="SNOMED CT",
    )

    assert anesthesia.anesthesia_type == "Epidural anesthesia"
    assert anesthesia.anesthesia_code == "18946005"


def test_anesthesia_protocol_with_single_agent():
    """Test AnesthesiaProtocol with a single anesthesia agent."""
    agent = MockMedication(
        name="Propofol 10mg/mL injection",
        code="153476",
        dosage="200 mg",
    )
    anesthesia = MockAnesthesia(anesthesia_agents=[agent])

    assert anesthesia.anesthesia_agents is not None
    assert len(anesthesia.anesthesia_agents) == 1
    assert anesthesia.anesthesia_agents[0].name == "Propofol 10mg/mL injection"
    assert anesthesia.anesthesia_agents[0].code == "153476"


def test_anesthesia_protocol_with_multiple_agents():
    """Test AnesthesiaProtocol with multiple anesthesia agents."""
    propofol = MockMedication(
        name="Propofol 10mg/mL injection",
        code="153476",
        dosage="200 mg",
    )
    fentanyl = MockMedication(
        name="Fentanyl 50mcg/mL injection",
        code="245134",
        dosage="100 mcg",
    )
    sevoflurane = MockMedication(
        name="Sevoflurane",
        code="203250",
        dosage="2.5%",
        route="Inhalation",
    )

    anesthesia = MockAnesthesia(anesthesia_agents=[propofol, fentanyl, sevoflurane])

    assert anesthesia.anesthesia_agents is not None
    assert len(anesthesia.anesthesia_agents) == 3
    assert anesthesia.anesthesia_agents[0].name == "Propofol 10mg/mL injection"
    assert anesthesia.anesthesia_agents[1].name == "Fentanyl 50mcg/mL injection"
    assert anesthesia.anesthesia_agents[2].name == "Sevoflurane"


def test_anesthesia_protocol_without_agents():
    """Test AnesthesiaProtocol without anesthesia agents."""
    anesthesia = MockAnesthesia(anesthesia_agents=None)

    assert anesthesia.anesthesia_agents is None


def test_anesthesia_protocol_with_route():
    """Test AnesthesiaProtocol with route of administration."""
    anesthesia = MockAnesthesia(route="Intravenous")

    assert anesthesia.route == "Intravenous"


def test_anesthesia_protocol_with_inhalation_route():
    """Test AnesthesiaProtocol with inhalation route."""
    anesthesia = MockAnesthesia(route="Inhalation")

    assert anesthesia.route == "Inhalation"


def test_anesthesia_protocol_without_route():
    """Test AnesthesiaProtocol without route."""
    anesthesia = MockAnesthesia(route=None)

    assert anesthesia.route is None


def test_anesthesia_protocol_with_performer():
    """Test AnesthesiaProtocol with performer name."""
    anesthesia = MockAnesthesia(performer_name="Dr. Sarah Johnson, MD")

    assert anesthesia.performer_name == "Dr. Sarah Johnson, MD"


def test_anesthesia_protocol_without_performer():
    """Test AnesthesiaProtocol without performer."""
    anesthesia = MockAnesthesia(performer_name=None)

    assert anesthesia.performer_name is None


def test_anesthesia_protocol_with_notes():
    """Test AnesthesiaProtocol with clinical notes."""
    notes = "Patient tolerated anesthesia well. No complications noted."
    anesthesia = MockAnesthesia(notes=notes)

    assert anesthesia.notes == notes


def test_anesthesia_protocol_without_notes():
    """Test AnesthesiaProtocol without clinical notes."""
    anesthesia = MockAnesthesia(notes=None)

    assert anesthesia.notes is None


def test_anesthesia_protocol_status_completed():
    """Test AnesthesiaProtocol with completed status."""
    anesthesia = MockAnesthesia(status="completed")

    assert anesthesia.status == "completed"


def test_anesthesia_protocol_status_active():
    """Test AnesthesiaProtocol with active status."""
    anesthesia = MockAnesthesia(status="active")

    assert anesthesia.status == "active"


def test_anesthesia_protocol_status_aborted():
    """Test AnesthesiaProtocol with aborted status."""
    anesthesia = MockAnesthesia(status="aborted")

    assert anesthesia.status == "aborted"


def test_anesthesia_protocol_satisfaction():
    """Test that MockAnesthesia satisfies AnesthesiaProtocol."""
    anesthesia = MockAnesthesia()

    def accepts_anesthesia(a: AnesthesiaProtocol) -> str:
        return f"{a.anesthesia_type} ({a.anesthesia_code})"

    result = accepts_anesthesia(anesthesia)
    assert result == "General anesthesia (50697003)"


def test_anesthesia_protocol_complete_example():
    """Test AnesthesiaProtocol with complete example data."""
    propofol = MockMedication(
        name="Propofol 10mg/mL injection",
        code="153476",
        dosage="200 mg",
        route="Intravenous",
    )
    fentanyl = MockMedication(
        name="Fentanyl 50mcg/mL injection",
        code="245134",
        dosage="100 mcg",
        route="Intravenous",
    )

    anesthesia = MockAnesthesia(
        anesthesia_type="General anesthesia",
        anesthesia_code="50697003",
        anesthesia_code_system="SNOMED CT",
        start_time=datetime(2024, 3, 15, 8, 30, 0),
        end_time=datetime(2024, 3, 15, 11, 0, 0),
        status="completed",
        anesthesia_agents=[propofol, fentanyl],
        route="Intravenous",
        performer_name="Dr. Michael Chen, MD, FASA",
        notes="Patient tolerated general anesthesia well. No complications.",
    )

    assert anesthesia.anesthesia_type == "General anesthesia"
    assert anesthesia.anesthesia_code == "50697003"
    assert anesthesia.anesthesia_code_system == "SNOMED CT"
    assert anesthesia.start_time == datetime(2024, 3, 15, 8, 30, 0)
    assert anesthesia.end_time == datetime(2024, 3, 15, 11, 0, 0)
    assert anesthesia.status == "completed"
    assert len(anesthesia.anesthesia_agents) == 2
    assert anesthesia.route == "Intravenous"
    assert anesthesia.performer_name == "Dr. Michael Chen, MD, FASA"
    assert "No complications" in anesthesia.notes


def test_medication_protocol_satisfaction_for_agent():
    """Test that MockMedication satisfies MedicationProtocol for anesthesia agents."""
    agent = MockMedication()

    def accepts_medication(m: MedicationProtocol) -> str:
        return f"{m.name} - {m.dosage}"

    result = accepts_medication(agent)
    assert result == "Propofol 10mg/mL injection - 200 mg"


class MinimalAnesthesia:
    """Minimal implementation with only required fields."""

    @property
    def anesthesia_type(self):
        return "Local anesthesia"

    @property
    def anesthesia_code(self):
        return "386761002"

    @property
    def anesthesia_code_system(self):
        return "SNOMED CT"

    @property
    def start_time(self):
        return None

    @property
    def end_time(self):
        return None

    @property
    def status(self):
        return "completed"

    @property
    def anesthesia_agents(self):
        return None

    @property
    def route(self):
        return None

    @property
    def performer_name(self):
        return None

    @property
    def notes(self):
        return None


def test_minimal_anesthesia_protocol():
    """Test that minimal implementation satisfies AnesthesiaProtocol."""
    anesthesia = MinimalAnesthesia()

    assert anesthesia.anesthesia_type == "Local anesthesia"
    assert anesthesia.anesthesia_code == "386761002"
    assert anesthesia.anesthesia_code_system == "SNOMED CT"
    assert anesthesia.status == "completed"
    assert anesthesia.start_time is None
    assert anesthesia.end_time is None
    assert anesthesia.anesthesia_agents is None
    assert anesthesia.route is None
    assert anesthesia.performer_name is None
    assert anesthesia.notes is None


def test_anesthesia_with_conscious_sedation():
    """Test AnesthesiaProtocol for conscious sedation."""
    midazolam = MockMedication(
        name="Midazolam 5mg/mL injection",
        code="892651",
        dosage="2 mg",
        route="Intravenous",
    )

    anesthesia = MockAnesthesia(
        anesthesia_type="Conscious sedation",
        anesthesia_code="72641008",
        anesthesia_code_system="SNOMED CT",
        anesthesia_agents=[midazolam],
        route="Intravenous",
        status="completed",
    )

    assert anesthesia.anesthesia_type == "Conscious sedation"
    assert anesthesia.anesthesia_code == "72641008"
    assert len(anesthesia.anesthesia_agents) == 1
    assert anesthesia.anesthesia_agents[0].name == "Midazolam 5mg/mL injection"


def test_anesthesia_duration_calculation():
    """Test that anesthesia start and end times allow duration calculation."""
    start = datetime(2024, 3, 15, 8, 30, 0)
    end = datetime(2024, 3, 15, 11, 0, 0)
    anesthesia = MockAnesthesia(start_time=start, end_time=end)

    duration = anesthesia.end_time - anesthesia.start_time
    assert duration.total_seconds() == 9000  # 2.5 hours = 150 minutes = 9000 seconds


def test_anesthesia_with_topical_route():
    """Test AnesthesiaProtocol with topical route."""
    lidocaine = MockMedication(
        name="Lidocaine 2% topical gel",
        code="855635",
        dosage="5 g",
        route="Topical",
    )

    anesthesia = MockAnesthesia(
        anesthesia_type="Local anesthesia",
        anesthesia_code="386761002",
        anesthesia_agents=[lidocaine],
        route="Topical",
    )

    assert anesthesia.route == "Topical"
    assert anesthesia.anesthesia_agents[0].route == "Topical"


def test_anesthesia_protocol_interface():
    """Test that AnesthesiaProtocol has expected interface."""
    # Import to ensure coverage
    from ccdakit.protocols.anesthesia import AnesthesiaProtocol

    # Verify protocol has expected attributes
    assert hasattr(AnesthesiaProtocol, 'anesthesia_type')
    assert hasattr(AnesthesiaProtocol, 'anesthesia_code')
    assert hasattr(AnesthesiaProtocol, 'status')
    assert hasattr(AnesthesiaProtocol, 'anesthesia_agents')
    assert hasattr(AnesthesiaProtocol, 'performer_name')
    assert hasattr(AnesthesiaProtocol, 'notes')

    # Verify docstrings exist
    assert AnesthesiaProtocol.__doc__ is not None
    assert 'Protocol defining the interface for anesthesia data' in AnesthesiaProtocol.__doc__
