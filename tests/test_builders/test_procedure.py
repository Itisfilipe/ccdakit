"""Tests for ProcedureActivity entry builder."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.entries.procedure import ProcedureActivity
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockProcedure:
    """Mock procedure for testing."""

    def __init__(
        self,
        name="Appendectomy",
        code="80146002",
        code_system="SNOMED CT",
        date=date(2023, 5, 15),
        status="completed",
        target_site=None,
        target_site_code=None,
        performer_name=None,
        performer_address=None,
        performer_telecom=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._date = date
        self._status = status
        self._target_site = target_site
        self._target_site_code = target_site_code
        self._performer_name = performer_name
        self._performer_address = performer_address
        self._performer_telecom = performer_telecom

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

    @property
    def performer_address(self):
        return self._performer_address

    @property
    def performer_telecom(self):
        return self._performer_telecom


class TestProcedureActivity:
    """Tests for ProcedureActivity builder."""

    def test_procedure_activity_basic(self):
        """Test basic ProcedureActivity creation."""
        procedure = MockProcedure()
        activity = ProcedureActivity(procedure)
        elem = activity.to_element()

        assert local_name(elem) == "procedure"

    def test_procedure_activity_has_class_and_mood_code(self):
        """Test procedure has correct classCode and moodCode."""
        procedure = MockProcedure()
        activity = ProcedureActivity(procedure)
        elem = activity.to_element()

        assert elem.get("classCode") == "PROC"
        assert elem.get("moodCode") == "EVN"

    def test_procedure_activity_has_template_id_r21(self):
        """Test ProcedureActivity includes R2.1 template ID."""
        procedure = MockProcedure()
        activity = ProcedureActivity(procedure, version=CDAVersion.R2_1)
        elem = activity.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.14"
        assert template.get("extension") == "2022-06-01"

    def test_procedure_activity_has_template_id_r20(self):
        """Test ProcedureActivity includes R2.0 template ID."""
        procedure = MockProcedure()
        activity = ProcedureActivity(procedure, version=CDAVersion.R2_0)
        elem = activity.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.14"
        assert template.get("extension") == "2014-06-09"

    def test_procedure_activity_has_id(self):
        """Test ProcedureActivity includes ID."""
        procedure = MockProcedure()
        activity = ProcedureActivity(procedure)
        elem = activity.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None

    def test_procedure_activity_has_code(self):
        """Test ProcedureActivity includes procedure code."""
        procedure = MockProcedure(
            name="Total Knee Replacement",
            code="609588000",
            code_system="SNOMED CT",
        )
        activity = ProcedureActivity(procedure)
        elem = activity.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "609588000"
        assert code.get("displayName") == "Total Knee Replacement"

    def test_procedure_activity_has_status_code(self):
        """Test ProcedureActivity includes status code."""
        procedure = MockProcedure(status="completed")
        activity = ProcedureActivity(procedure)
        elem = activity.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_procedure_activity_status_mapping(self):
        """Test status code mapping."""
        statuses = {
            "completed": "completed",
            "active": "active",
            "aborted": "aborted",
            "cancelled": "cancelled",
        }

        for input_status, expected in statuses.items():
            procedure = MockProcedure(status=input_status)
            activity = ProcedureActivity(procedure)
            elem = activity.to_element()

            status = elem.find(f"{{{NS}}}statusCode")
            assert status.get("code") == expected

    def test_procedure_activity_has_effective_time(self):
        """Test ProcedureActivity includes effectiveTime."""
        procedure = MockProcedure(date=date(2023, 5, 15))
        activity = ProcedureActivity(procedure)
        elem = activity.to_element()

        time = elem.find(f"{{{NS}}}effectiveTime")
        assert time is not None
        assert time.get("value") == "20230515"

    def test_procedure_activity_with_datetime(self):
        """Test ProcedureActivity with datetime instead of date."""
        procedure = MockProcedure(date=datetime(2023, 5, 15, 14, 30))
        activity = ProcedureActivity(procedure)
        elem = activity.to_element()

        time = elem.find(f"{{{NS}}}effectiveTime")
        assert time is not None
        # Datetime values include timezone per C-CDA spec CONF:81-10130
        assert time.get("value").startswith("20230515143000")

    def test_procedure_activity_with_target_site_code(self):
        """Test ProcedureActivity with target site code."""
        procedure = MockProcedure(
            target_site="Right knee",
            target_site_code="6757004",
        )
        activity = ProcedureActivity(procedure)
        elem = activity.to_element()

        target_site = elem.find(f"{{{NS}}}targetSiteCode")
        assert target_site is not None
        assert target_site.get("code") == "6757004"
        assert target_site.get("displayName") == "Right knee"

    def test_procedure_activity_with_target_site_text_only(self):
        """Test ProcedureActivity with target site text but no code."""
        procedure = MockProcedure(target_site="Abdomen")
        activity = ProcedureActivity(procedure)
        elem = activity.to_element()

        target_site = elem.find(f"{{{NS}}}targetSiteCode")
        assert target_site is not None
        assert target_site.get("nullFlavor") == "OTH"

        original_text = target_site.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "Abdomen"

    def test_procedure_activity_with_performer(self):
        """Test ProcedureActivity with performer name."""
        procedure = MockProcedure(performer_name="Jane Smith")
        activity = ProcedureActivity(procedure)
        elem = activity.to_element()

        performer = elem.find(f"{{{NS}}}performer")
        assert performer is not None

        assigned_entity = performer.find(f"{{{NS}}}assignedEntity")
        assert assigned_entity is not None

        # Check for required addr and telecom (should have nullFlavor if not provided)
        addr = assigned_entity.find(f"{{{NS}}}addr")
        assert addr is not None
        assert addr.get("nullFlavor") == "UNK"  # No address provided

        telecom = assigned_entity.find(f"{{{NS}}}telecom")
        assert telecom is not None
        assert telecom.get("nullFlavor") == "UNK"  # No telecom provided

        assigned_person = assigned_entity.find(f"{{{NS}}}assignedPerson")
        assert assigned_person is not None

        name = assigned_person.find(f"{{{NS}}}name")
        assert name is not None

        given = name.find(f"{{{NS}}}given")
        family = name.find(f"{{{NS}}}family")
        assert given.text == "Jane"
        assert family.text == "Smith"

    def test_procedure_activity_with_performer_full_details(self):
        """Test ProcedureActivity with performer including address and telecom."""
        procedure = MockProcedure(
            performer_name="Dr. John Doe",
            performer_address="123 Medical Center Dr, Boston, MA 02115",
            performer_telecom="tel:+1-617-555-1234",
        )
        activity = ProcedureActivity(procedure)
        elem = activity.to_element()

        performer = elem.find(f"{{{NS}}}performer")
        assert performer is not None

        assigned_entity = performer.find(f"{{{NS}}}assignedEntity")
        assert assigned_entity is not None

        # Check address
        addr = assigned_entity.find(f"{{{NS}}}addr")
        assert addr is not None
        street = addr.find(f"{{{NS}}}streetAddressLine")
        assert street is not None
        assert street.text == "123 Medical Center Dr"
        city = addr.find(f"{{{NS}}}city")
        assert city.text == "Boston"
        state = addr.find(f"{{{NS}}}state")
        assert state.text == "MA"
        postal = addr.find(f"{{{NS}}}postalCode")
        assert postal.text == "02115"

        # Check telecom
        telecom = assigned_entity.find(f"{{{NS}}}telecom")
        assert telecom is not None
        assert telecom.get("value") == "tel:+1-617-555-1234"

    def test_procedure_activity_to_string(self):
        """Test ProcedureActivity serialization."""
        procedure = MockProcedure()
        activity = ProcedureActivity(procedure)
        xml = activity.to_string(pretty=False)

        assert "<procedure" in xml or ":procedure" in xml
        assert "80146002" in xml  # procedure code
        assert "Appendectomy" in xml

    def test_procedure_activity_code_systems(self):
        """Test different procedure code systems."""
        code_systems = [
            ("SNOMED CT", "2.16.840.1.113883.6.96"),
            ("CPT-4", "2.16.840.1.113883.6.12"),
            ("LOINC", "2.16.840.1.113883.6.1"),
            ("ICD10 PCS", "2.16.840.1.113883.6.4"),
        ]

        for system_name, expected_oid in code_systems:
            procedure = MockProcedure(
                code="12345",
                code_system=system_name,
            )
            activity = ProcedureActivity(procedure)
            elem = activity.to_element()

            code = elem.find(f"{{{NS}}}code")
            assert code.get("codeSystem") == expected_oid


class TestProcedureActivityIntegration:
    """Integration tests for ProcedureActivity."""

    def test_complete_procedure_activity(self):
        """Test creating a complete procedure activity with all fields."""
        procedure = MockProcedure(
            name="Hip Replacement Surgery",
            code="52734007",
            code_system="SNOMED CT",
            date=datetime(2023, 6, 10, 9, 30),
            status="completed",
            target_site="Left hip",
            target_site_code="287579007",
            performer_name="Dr. John Surgeon",
        )

        activity = ProcedureActivity(procedure, version=CDAVersion.R2_1)
        elem = activity.to_element()

        # Verify all components
        assert local_name(elem) == "procedure"
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}targetSiteCode") is not None
        assert elem.find(f"{{{NS}}}performer") is not None

    def test_minimal_procedure_activity(self):
        """Test creating minimal procedure activity with only required fields."""
        procedure = MockProcedure(
            name="Blood Draw",
            code="396550006",
            code_system="SNOMED CT",
            date=None,  # No date
            status="completed",
        )

        activity = ProcedureActivity(procedure)
        elem = activity.to_element()

        # Verify required components
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None

        # effectiveTime is present with nullFlavor when no date (SHOULD per CONF:1098-7332)
        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None
        assert time_elem.get("nullFlavor") == "UNK"

        # Should not have other optional components
        assert elem.find(f"{{{NS}}}targetSiteCode") is None
        assert elem.find(f"{{{NS}}}performer") is None
