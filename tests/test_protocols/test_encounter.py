"""Tests for encounter protocols."""

from datetime import date, datetime

from ccdakit.protocols.encounter import EncounterProtocol


class MockEncounter:
    """Test implementation of EncounterProtocol."""

    def __init__(
        self,
        encounter_type: str = "Office Visit",
        code: str = "99213",
        code_system: str = "CPT-4",
        date_val: date | datetime | None = None,
        end_date_val: date | datetime | None = None,
        location: str | None = None,
        performer_name: str | None = None,
        discharge_disposition: str | None = None,
    ):
        self._encounter_type = encounter_type
        self._code = code
        self._code_system = code_system
        self._date = date_val if date_val is not None else date(2024, 10, 15)
        self._end_date = end_date_val
        self._location = location
        self._performer_name = performer_name
        self._discharge_disposition = discharge_disposition

    @property
    def encounter_type(self):
        return self._encounter_type

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
    def end_date(self):
        return self._end_date

    @property
    def location(self):
        return self._location

    @property
    def performer_name(self):
        return self._performer_name

    @property
    def discharge_disposition(self):
        return self._discharge_disposition


def test_encounter_protocol_required_fields():
    """Test EncounterProtocol required fields."""
    encounter = MockEncounter()

    assert encounter.encounter_type == "Office Visit"
    assert encounter.code == "99213"
    assert encounter.code_system == "CPT-4"
    assert encounter.date == date(2024, 10, 15)


def test_encounter_protocol_with_date():
    """Test EncounterProtocol with date."""
    encounter_date = date(2024, 5, 20)
    encounter = MockEncounter(date_val=encounter_date)

    assert encounter.date == encounter_date


def test_encounter_protocol_with_datetime():
    """Test EncounterProtocol with datetime."""
    encounter_datetime = datetime(2024, 5, 20, 14, 30)
    encounter = MockEncounter(date_val=encounter_datetime)

    assert encounter.date == encounter_datetime


def test_encounter_protocol_with_end_date():
    """Test EncounterProtocol with start and end dates."""
    start_date = date(2024, 5, 20)
    end_date = date(2024, 5, 22)
    encounter = MockEncounter(date_val=start_date, end_date_val=end_date)

    assert encounter.date == start_date
    assert encounter.end_date == end_date


def test_encounter_protocol_with_location():
    """Test EncounterProtocol with location."""
    encounter = MockEncounter(location="Community Health Hospital")

    assert encounter.location == "Community Health Hospital"


def test_encounter_protocol_with_performer():
    """Test EncounterProtocol with performer name."""
    encounter = MockEncounter(performer_name="Dr. John Smith")

    assert encounter.performer_name == "Dr. John Smith"


def test_encounter_protocol_with_discharge_disposition():
    """Test EncounterProtocol with discharge disposition."""
    encounter = MockEncounter(
        encounter_type="Inpatient Admission",
        code="IMP",
        code_system="ActCode",
        discharge_disposition="Home",
    )

    assert encounter.discharge_disposition == "Home"


def test_encounter_protocol_without_optional_fields():
    """Test EncounterProtocol without optional fields."""
    encounter = MockEncounter()

    assert encounter.end_date is None
    assert encounter.location is None
    assert encounter.performer_name is None
    assert encounter.discharge_disposition is None


def test_encounter_protocol_satisfaction():
    """Test that MockEncounter satisfies EncounterProtocol."""
    encounter = MockEncounter()

    def accepts_encounter(e: EncounterProtocol) -> str:
        return f"{e.encounter_type} ({e.code})"

    result = accepts_encounter(encounter)
    assert result == "Office Visit (99213)"


def test_office_visit_encounter():
    """Test office visit encounter."""
    encounter = MockEncounter(
        encounter_type="Office Visit",
        code="99213",
        code_system="CPT-4",
        date_val=date(2024, 6, 15),
        location="Main Clinic",
        performer_name="Dr. Jane Doe",
    )

    assert encounter.encounter_type == "Office Visit"
    assert encounter.code == "99213"
    assert encounter.code_system == "CPT-4"


def test_emergency_room_encounter():
    """Test emergency room encounter."""
    encounter = MockEncounter(
        encounter_type="Emergency Room",
        code="99285",
        code_system="CPT-4",
        date_val=datetime(2024, 7, 4, 23, 15),
        location="Emergency Department",
        performer_name="Dr. Emergency",
    )

    assert encounter.encounter_type == "Emergency Room"
    assert encounter.code == "99285"


def test_inpatient_encounter():
    """Test inpatient encounter."""
    encounter = MockEncounter(
        encounter_type="Inpatient Admission",
        code="IMP",
        code_system="ActCode",
        date_val=date(2024, 8, 1),
        end_date_val=date(2024, 8, 5),
        location="Community Health Hospital",
        discharge_disposition="Home",
    )

    assert encounter.encounter_type == "Inpatient Admission"
    assert encounter.end_date == date(2024, 8, 5)
    assert encounter.discharge_disposition == "Home"


def test_encounter_with_snomed_code():
    """Test encounter with SNOMED CT code."""
    encounter = MockEncounter(
        encounter_type="Ambulatory Encounter",
        code="185349003",
        code_system="SNOMED CT",
    )

    assert encounter.code == "185349003"
    assert encounter.code_system == "SNOMED CT"


def test_encounter_with_none_date():
    """Test encounter with None as date."""
    # Create encounter that truly has None date
    class EncounterWithNoneDate:
        @property
        def encounter_type(self):
            return "Office Visit"

        @property
        def code(self):
            return "99213"

        @property
        def code_system(self):
            return "CPT-4"

        @property
        def date(self):
            return None

        @property
        def end_date(self):
            return None

        @property
        def location(self):
            return None

        @property
        def performer_name(self):
            return None

        @property
        def discharge_disposition(self):
            return None

    encounter = EncounterWithNoneDate()

    # Should allow None for date
    assert encounter.date is None


def test_encounter_with_same_start_and_end():
    """Test encounter where start and end dates are same."""
    same_date = date(2024, 9, 10)
    encounter = MockEncounter(date_val=same_date, end_date_val=same_date)

    assert encounter.date == same_date
    assert encounter.end_date == same_date


def test_encounter_with_datetime_range():
    """Test encounter with datetime range."""
    start_dt = datetime(2024, 10, 1, 8, 0)
    end_dt = datetime(2024, 10, 1, 17, 0)
    encounter = MockEncounter(date_val=start_dt, end_date_val=end_dt)

    assert encounter.date == start_dt
    assert encounter.end_date == end_dt


def test_encounter_discharge_dispositions():
    """Test various discharge dispositions."""
    dispositions = [
        "Home",
        "Skilled Nursing Facility",
        "Rehabilitation Facility",
        "Acute Care Hospital",
        "Expired",
    ]

    for disposition in dispositions:
        encounter = MockEncounter(discharge_disposition=disposition)
        assert encounter.discharge_disposition == disposition


def test_encounter_empty_optional_strings():
    """Test encounter with empty strings for optional fields."""
    encounter = MockEncounter(
        location="",
        performer_name="",
        discharge_disposition="",
    )

    assert encounter.location == ""
    assert encounter.performer_name == ""
    assert encounter.discharge_disposition == ""


class MinimalEncounter:
    """Minimal implementation with only required fields."""

    @property
    def encounter_type(self):
        return "Consultation"

    @property
    def code(self):
        return "99241"

    @property
    def code_system(self):
        return "CPT-4"

    @property
    def date(self):
        return date(2024, 10, 20)

    @property
    def end_date(self):
        return None

    @property
    def location(self):
        return None

    @property
    def performer_name(self):
        return None

    @property
    def discharge_disposition(self):
        return None


def test_minimal_encounter_protocol():
    """Test that minimal implementation satisfies EncounterProtocol."""
    encounter = MinimalEncounter()

    assert encounter.encounter_type == "Consultation"
    assert encounter.code == "99241"
    assert encounter.code_system == "CPT-4"
    assert encounter.date == date(2024, 10, 20)
    assert encounter.end_date is None
    assert encounter.location is None
    assert encounter.performer_name is None
    assert encounter.discharge_disposition is None


def test_encounter_isinstance_check():
    """Test that MockEncounter supports protocol typing."""
    encounter = MockEncounter()

    # Protocol structural typing
    assert isinstance(encounter, object)
    assert hasattr(encounter, 'encounter_type')
    assert hasattr(encounter, 'code')
    assert hasattr(encounter, 'code_system')
    assert hasattr(encounter, 'date')
    assert hasattr(encounter, 'end_date')
    assert hasattr(encounter, 'location')
    assert hasattr(encounter, 'performer_name')
    assert hasattr(encounter, 'discharge_disposition')


def test_encounter_with_all_fields():
    """Test encounter with all optional fields populated."""
    encounter = MockEncounter(
        encounter_type="Inpatient Stay",
        code="99233",
        code_system="CPT-4",
        date_val=datetime(2024, 11, 1, 8, 0),
        end_date_val=datetime(2024, 11, 3, 16, 0),
        location="Memorial Hospital, Room 302",
        performer_name="Dr. Sarah Johnson",
        discharge_disposition="Skilled Nursing Facility",
    )

    assert encounter.encounter_type == "Inpatient Stay"
    assert encounter.code == "99233"
    assert encounter.code_system == "CPT-4"
    assert encounter.date == datetime(2024, 11, 1, 8, 0)
    assert encounter.end_date == datetime(2024, 11, 3, 16, 0)
    assert encounter.location == "Memorial Hospital, Room 302"
    assert encounter.performer_name == "Dr. Sarah Johnson"
    assert encounter.discharge_disposition == "Skilled Nursing Facility"


def test_encounter_multiple_code_systems():
    """Test encounters with different code systems."""
    cpt = MockEncounter(code_system="CPT-4")
    snomed = MockEncounter(code="185349003", code_system="SNOMED CT")
    actcode = MockEncounter(code="AMB", code_system="ActCode")

    assert cpt.code_system == "CPT-4"
    assert snomed.code_system == "SNOMED CT"
    assert actcode.code_system == "ActCode"


def test_encounter_point_in_time():
    """Test encounter as point in time (no end_date)."""
    encounter = MockEncounter(
        encounter_type="Preventive Care Visit",
        code="99385",
        code_system="CPT-4",
        date_val=date(2024, 12, 1),
        end_date_val=None,
    )

    assert encounter.date == date(2024, 12, 1)
    assert encounter.end_date is None


def test_encounter_ongoing():
    """Test ongoing encounter (has start date, no end date)."""
    encounter = MockEncounter(
        encounter_type="Hospital Stay",
        code="IMP",
        code_system="ActCode",
        date_val=date(2024, 10, 20),
        end_date_val=None,
        location="Memorial Hospital",
    )

    assert encounter.date == date(2024, 10, 20)
    assert encounter.end_date is None
    assert encounter.location == "Memorial Hospital"
