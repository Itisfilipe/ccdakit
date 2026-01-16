"""Tests for EncounterActivity entry builder."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.entries.encounter import EncounterActivity
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"
SDTC_NS = "urn:hl7-org:sdtc"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockEncounter:
    """Mock encounter for testing."""

    def __init__(
        self,
        encounter_type="Office Visit",
        code="99213",
        code_system="CPT-4",
        date=date(2023, 5, 15),
        end_date=None,
        location=None,
        performer_name=None,
        discharge_disposition=None,
    ):
        self._encounter_type = encounter_type
        self._code = code
        self._code_system = code_system
        self._date = date
        self._end_date = end_date
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


class TestEncounterActivity:
    """Tests for EncounterActivity builder."""

    def test_encounter_activity_basic(self):
        """Test basic EncounterActivity creation."""
        encounter = MockEncounter()
        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        assert local_name(elem) == "encounter"

    def test_encounter_activity_has_class_and_mood_code(self):
        """Test encounter has correct classCode and moodCode."""
        encounter = MockEncounter()
        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        assert elem.get("classCode") == "ENC"
        assert elem.get("moodCode") == "EVN"

    def test_encounter_activity_has_template_id_r21(self):
        """Test EncounterActivity includes R2.1 template ID."""
        encounter = MockEncounter()
        activity = EncounterActivity(encounter, version=CDAVersion.R2_1)
        elem = activity.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.49"
        assert template.get("extension") == "2015-08-01"

    def test_encounter_activity_has_template_id_r20(self):
        """Test EncounterActivity includes R2.0 template ID."""
        encounter = MockEncounter()
        activity = EncounterActivity(encounter, version=CDAVersion.R2_0)
        elem = activity.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.49"
        assert template.get("extension") == "2014-06-09"

    def test_encounter_activity_has_id(self):
        """Test EncounterActivity includes ID."""
        encounter = MockEncounter()
        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None

    def test_encounter_activity_has_code(self):
        """Test EncounterActivity includes encounter code."""
        encounter = MockEncounter(
            encounter_type="Emergency Department Visit",
            code="99285",
            code_system="CPT-4",
        )
        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "99285"
        assert code.get("displayName") == "Emergency Department Visit"

    def test_encounter_activity_has_effective_time(self):
        """Test EncounterActivity includes effectiveTime."""
        encounter = MockEncounter(date=date(2023, 5, 15))
        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        time = elem.find(f"{{{NS}}}effectiveTime")
        assert time is not None
        assert time.get("value") == "20230515"

    def test_encounter_activity_with_datetime(self):
        """Test EncounterActivity with datetime instead of date."""
        encounter = MockEncounter(date=datetime(2023, 5, 15, 14, 30))
        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        time = elem.find(f"{{{NS}}}effectiveTime")
        assert time is not None
        assert time.get("value").startswith("20230515143000")

    def test_encounter_activity_with_time_interval(self):
        """Test EncounterActivity with start and end dates (interval)."""
        encounter = MockEncounter(
            date=date(2023, 5, 15),
            end_date=date(2023, 5, 17),
        )
        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        time = elem.find(f"{{{NS}}}effectiveTime")
        assert time is not None

        low = time.find(f"{{{NS}}}low")
        high = time.find(f"{{{NS}}}high")

        assert low is not None
        assert low.get("value") == "20230515"
        assert high is not None
        assert high.get("value") == "20230517"

    def test_encounter_activity_with_datetime_interval(self):
        """Test EncounterActivity with datetime interval."""
        encounter = MockEncounter(
            date=datetime(2023, 5, 15, 9, 0),
            end_date=datetime(2023, 5, 15, 10, 30),
        )
        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        time = elem.find(f"{{{NS}}}effectiveTime")
        low = time.find(f"{{{NS}}}low")
        high = time.find(f"{{{NS}}}high")

        assert low.get("value") == "20230515090000"
        assert high.get("value") == "20230515103000"

    def test_encounter_activity_with_performer(self):
        """Test EncounterActivity with performer name."""
        encounter = MockEncounter(performer_name="Jane Smith")
        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        performer = elem.find(f"{{{NS}}}performer")
        assert performer is not None
        assert performer.get("typeCode") == "PRF"

        assigned_entity = performer.find(f"{{{NS}}}assignedEntity")
        assert assigned_entity is not None

        assigned_person = assigned_entity.find(f"{{{NS}}}assignedPerson")
        assert assigned_person is not None

        name = assigned_person.find(f"{{{NS}}}name")
        assert name is not None

        given = name.find(f"{{{NS}}}given")
        family = name.find(f"{{{NS}}}family")
        assert given.text == "Jane"
        assert family.text == "Smith"

    def test_encounter_activity_with_location(self):
        """Test EncounterActivity with service delivery location."""
        encounter = MockEncounter(location="Community Health Hospital")
        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        assert participant is not None
        assert participant.get("typeCode") == "LOC"

        participant_role = participant.find(f"{{{NS}}}participantRole")
        assert participant_role is not None
        assert participant_role.get("classCode") == "SDLOC"

        # Should have Service Delivery Location template ID
        template = participant_role.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.32"

        # Should have playing entity with location name
        playing_entity = participant_role.find(f"{{{NS}}}playingEntity")
        assert playing_entity is not None
        assert playing_entity.get("classCode") == "PLC"

        name = playing_entity.find(f"{{{NS}}}name")
        assert name is not None
        assert name.text == "Community Health Hospital"

    def test_encounter_activity_with_discharge_disposition(self):
        """Test EncounterActivity with discharge disposition."""
        encounter = MockEncounter(discharge_disposition="Home")
        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        # Find discharge disposition using SDTC namespace
        disp = elem.find(f"{{{SDTC_NS}}}dischargeDispositionCode")
        assert disp is not None
        assert disp.get("displayName") == "Home"
        assert disp.get("codeSystem") is not None

    def test_encounter_activity_to_string(self):
        """Test EncounterActivity serialization."""
        encounter = MockEncounter()
        activity = EncounterActivity(encounter)
        xml = activity.to_string(pretty=False)

        assert "<encounter" in xml or ":encounter" in xml
        assert "99213" in xml  # encounter code
        assert "Office Visit" in xml

    def test_encounter_activity_code_systems(self):
        """Test different encounter code systems."""
        code_systems = [
            ("CPT-4", "2.16.840.1.113883.6.12"),
            ("SNOMED CT", "2.16.840.1.113883.6.96"),
            ("ActCode", "2.16.840.1.113883.5.4"),
        ]

        for system_name, expected_oid in code_systems:
            encounter = MockEncounter(
                code="12345",
                code_system=system_name,
            )
            activity = EncounterActivity(encounter)
            elem = activity.to_element()

            code = elem.find(f"{{{NS}}}code")
            assert code.get("codeSystem") == expected_oid


class TestEncounterActivityIntegration:
    """Integration tests for EncounterActivity."""

    def test_complete_encounter_activity(self):
        """Test creating a complete encounter activity with all fields."""
        encounter = MockEncounter(
            encounter_type="Inpatient Hospital Admission",
            code="32485007",
            code_system="SNOMED CT",
            date=datetime(2023, 6, 10, 9, 30),
            end_date=datetime(2023, 6, 12, 14, 0),
            location="Memorial Hospital",
            performer_name="Dr. Sarah Johnson",
            discharge_disposition="Home",
        )

        activity = EncounterActivity(encounter, version=CDAVersion.R2_1)
        elem = activity.to_element()

        # Verify all components
        assert local_name(elem) == "encounter"
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}performer") is not None
        assert elem.find(f"{{{NS}}}participant") is not None
        assert elem.find(f"{{{SDTC_NS}}}dischargeDispositionCode") is not None

    def test_minimal_encounter_activity(self):
        """Test creating minimal encounter activity with only required fields."""
        encounter = MockEncounter(
            encounter_type="Office Visit",
            code="99213",
            code_system="CPT-4",
            date=date(2023, 5, 15),
        )

        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        # Verify required components
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None

        # Should not have optional components
        assert elem.find(f"{{{NS}}}performer") is None
        assert elem.find(f"{{{NS}}}participant") is None
        assert elem.find(f"{{{SDTC_NS}}}dischargeDispositionCode") is None

    def test_outpatient_visit(self):
        """Test typical outpatient visit scenario."""
        encounter = MockEncounter(
            encounter_type="Outpatient Consultation",
            code="99245",
            code_system="CPT-4",
            date=datetime(2023, 5, 20, 10, 0),
            location="Primary Care Clinic",
            performer_name="Dr. Michael Chen",
        )

        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        # Verify outpatient-specific structure
        code = elem.find(f"{{{NS}}}code")
        assert code.get("code") == "99245"

        time = elem.find(f"{{{NS}}}effectiveTime")
        assert time.get("value").startswith("20230520100000")

        # Should have performer and location but no discharge
        assert elem.find(f"{{{NS}}}performer") is not None
        assert elem.find(f"{{{NS}}}participant") is not None
        assert elem.find(f"{{{SDTC_NS}}}dischargeDispositionCode") is None

    def test_inpatient_admission(self):
        """Test typical inpatient admission scenario."""
        encounter = MockEncounter(
            encounter_type="Hospital Inpatient Admission",
            code="32485007",
            code_system="SNOMED CT",
            date=datetime(2023, 6, 1, 18, 30),
            end_date=datetime(2023, 6, 5, 11, 0),
            location="St. Mary's Hospital",
            performer_name="Dr. Emily Rodriguez",
            discharge_disposition="Skilled Nursing Facility",
        )

        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        # Verify inpatient-specific structure
        time = elem.find(f"{{{NS}}}effectiveTime")
        assert time.find(f"{{{NS}}}low") is not None
        assert time.find(f"{{{NS}}}high") is not None

        # Should have discharge disposition for inpatient
        disp = elem.find(f"{{{SDTC_NS}}}dischargeDispositionCode")
        assert disp is not None
        assert disp.get("displayName") == "Skilled Nursing Facility"

    def test_emergency_department_visit(self):
        """Test emergency department visit scenario."""
        encounter = MockEncounter(
            encounter_type="Emergency Department Visit",
            code="99285",
            code_system="CPT-4",
            date=datetime(2023, 4, 15, 3, 45),
            end_date=datetime(2023, 4, 15, 8, 20),
            location="County General ER",
            performer_name="Dr. James Wilson",
        )

        activity = EncounterActivity(encounter)
        elem = activity.to_element()

        # Verify ED-specific structure
        code = elem.find(f"{{{NS}}}code")
        assert code.get("code") == "99285"

        # Should have time interval (admission to discharge from ER)
        time = elem.find(f"{{{NS}}}effectiveTime")
        assert time.find(f"{{{NS}}}low") is not None
        assert time.find(f"{{{NS}}}high") is not None
