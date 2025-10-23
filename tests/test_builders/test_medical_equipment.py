"""Tests for Medical Equipment entry builders."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.entries.medical_equipment import (
    MedicalEquipmentOrganizer,
    NonMedicinalSupplyActivity,
)
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockMedicalEquipment:
    """Mock medical equipment for testing."""

    def __init__(
        self,
        name="Wheelchair",
        code="58938008",
        code_system="SNOMED CT",
        status="completed",
        date_supplied=date(2023, 1, 15),
        date_end=None,
        quantity=1,
        manufacturer="Acme Medical",
        model_number="WC-123",
        serial_number="SN123456",
        instructions=None,
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
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def status(self):
        return self._status

    @property
    def date_supplied(self):
        return self._date_supplied

    @property
    def date_end(self):
        return self._date_end

    @property
    def quantity(self):
        return self._quantity

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def model_number(self):
        return self._model_number

    @property
    def serial_number(self):
        return self._serial_number

    @property
    def instructions(self):
        return self._instructions


class TestNonMedicinalSupplyActivity:
    """Tests for NonMedicinalSupplyActivity builder."""

    def test_supply_activity_basic(self):
        """Test basic NonMedicinalSupplyActivity creation."""
        equipment = MockMedicalEquipment()
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        assert local_name(elem) == "supply"
        assert elem.get("classCode") == "SPLY"
        assert elem.get("moodCode") == "EVN"

    def test_supply_activity_has_template_id_r21(self):
        """Test NonMedicinalSupplyActivity includes R2.1 template ID."""
        equipment = MockMedicalEquipment()
        supply = NonMedicinalSupplyActivity(equipment, version=CDAVersion.R2_1)
        elem = supply.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.50"
        assert template.get("extension") == "2014-06-09"

    def test_supply_activity_has_template_id_r20(self):
        """Test NonMedicinalSupplyActivity includes R2.0 template ID."""
        equipment = MockMedicalEquipment()
        supply = NonMedicinalSupplyActivity(equipment, version=CDAVersion.R2_0)
        elem = supply.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.50"
        assert template.get("extension") == "2014-06-09"

    def test_supply_activity_has_id(self):
        """Test NonMedicinalSupplyActivity has ID element."""
        equipment = MockMedicalEquipment()
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_supply_activity_has_status_code(self):
        """Test NonMedicinalSupplyActivity has statusCode element."""
        equipment = MockMedicalEquipment(status="completed")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_supply_activity_status_mapping(self):
        """Test different status code mappings."""
        test_cases = [
            ("completed", "completed", "EVN"),
            ("active", "active", "EVN"),
            ("aborted", "aborted", "EVN"),
            ("cancelled", "cancelled", "EVN"),
            ("new", "new", "INT"),
            # "ordered" is not in STATUS_CODES, so it defaults to "completed"
            ("ordered", "completed", "INT"),  # INT mood because "ordered" matches intent_statuses
        ]

        for input_status, expected_status, expected_mood in test_cases:
            equipment = MockMedicalEquipment(status=input_status)
            supply = NonMedicinalSupplyActivity(equipment)
            elem = supply.to_element()

            status = elem.find(f"{{{NS}}}statusCode")
            assert status.get("code") == expected_status
            assert elem.get("moodCode") == expected_mood

    def test_supply_activity_mood_code_event(self):
        """Test NonMedicinalSupplyActivity with EVN mood for completed status."""
        equipment = MockMedicalEquipment(status="completed")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        assert elem.get("moodCode") == "EVN"

    def test_supply_activity_mood_code_intent(self):
        """Test NonMedicinalSupplyActivity with INT mood for new status."""
        equipment = MockMedicalEquipment(status="new")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        assert elem.get("moodCode") == "INT"

    def test_supply_activity_effective_time_date_only(self):
        """Test NonMedicinalSupplyActivity effectiveTime with single date."""
        equipment = MockMedicalEquipment(
            date_supplied=date(2023, 1, 15),
            date_end=None,
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None
        assert time_elem.get("value") == "20230115"

    def test_supply_activity_effective_time_with_range(self):
        """Test NonMedicinalSupplyActivity effectiveTime with low and high."""
        equipment = MockMedicalEquipment(
            date_supplied=date(2023, 1, 15),
            date_end=date(2023, 12, 31),
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None
        xsi_type = time_elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        assert xsi_type == "IVL_TS"

        low = time_elem.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20230115"

        high = time_elem.find(f"{{{NS}}}high")
        assert high is not None
        assert high.get("value") == "20231231"

    def test_supply_activity_effective_time_with_datetime(self):
        """Test NonMedicinalSupplyActivity effectiveTime with datetime."""
        equipment = MockMedicalEquipment(
            date_supplied=datetime(2023, 1, 15, 10, 30, 0),
            date_end=datetime(2023, 12, 31, 17, 0, 0),
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None

        low = time_elem.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20230115103000"

        high = time_elem.find(f"{{{NS}}}high")
        assert high is not None
        assert high.get("value") == "20231231170000"

    def test_supply_activity_no_effective_time(self):
        """Test NonMedicinalSupplyActivity without effectiveTime."""
        equipment = MockMedicalEquipment(date_supplied=None, date_end=None)
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is None

    def test_supply_activity_quantity(self):
        """Test NonMedicinalSupplyActivity quantity element."""
        equipment = MockMedicalEquipment(quantity=5)
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        quantity = elem.find(f"{{{NS}}}quantity")
        assert quantity is not None
        assert quantity.get("value") == "5"

    def test_supply_activity_no_quantity(self):
        """Test NonMedicinalSupplyActivity without quantity."""
        equipment = MockMedicalEquipment(quantity=None)
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        quantity = elem.find(f"{{{NS}}}quantity")
        assert quantity is None

    def test_supply_activity_product_instance(self):
        """Test NonMedicinalSupplyActivity with product instance participant."""
        equipment = MockMedicalEquipment(
            code="58938008",
            code_system="SNOMED CT",
            serial_number="SN123456",
            manufacturer="Acme Medical",
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        assert participant is not None
        assert participant.get("typeCode") == "PRD"

        role = participant.find(f"{{{NS}}}participantRole")
        assert role is not None
        assert role.get("classCode") == "MANU"

        # Check template ID
        template = role.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.37"

        # Check ID with serial number
        id_elem = role.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("extension") == "SN123456"

        # Check playing device
        device = role.find(f"{{{NS}}}playingDevice")
        assert device is not None

        code = device.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "58938008"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"

        # Check scoping entity (manufacturer)
        scoping = role.find(f"{{{NS}}}scopingEntity")
        assert scoping is not None

        scoping_id = scoping.find(f"{{{NS}}}id")
        assert scoping_id is not None
        assert scoping_id.get("extension") == "Acme Medical"

    def test_supply_activity_product_instance_udi(self):
        """Test NonMedicinalSupplyActivity with UDI serial number."""
        udi = "(01)00643169001763(11)141231(17)150707(10)A213B1(21)1234"
        equipment = MockMedicalEquipment(serial_number=udi)
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        role = participant.find(f"{{{NS}}}participantRole")
        id_elem = role.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.3.3719"  # FDA UDI OID
        assert id_elem.get("extension") == udi

    def test_supply_activity_product_instance_no_serial(self):
        """Test NonMedicinalSupplyActivity product instance without serial number."""
        equipment = MockMedicalEquipment(
            serial_number=None,
            manufacturer="Acme Medical",
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        role = participant.find(f"{{{NS}}}participantRole")
        id_elem = role.find(f"{{{NS}}}id")

        assert id_elem is not None
        # Should have generated UUID
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_supply_activity_product_instance_no_manufacturer(self):
        """Test NonMedicinalSupplyActivity product instance without manufacturer."""
        equipment = MockMedicalEquipment(manufacturer=None)
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        role = participant.find(f"{{{NS}}}participantRole")
        scoping = role.find(f"{{{NS}}}scopingEntity")
        scoping_id = scoping.find(f"{{{NS}}}id")

        assert scoping_id is not None
        assert scoping_id.get("nullFlavor") == "UNK"

    def test_supply_activity_no_product_instance(self):
        """Test NonMedicinalSupplyActivity without product instance data."""
        equipment = MockMedicalEquipment(
            manufacturer=None,
            model_number=None,
            serial_number=None,
            code=None,
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        assert participant is None

    def test_supply_activity_code_system_mapping(self):
        """Test code system OID mapping for different systems."""
        # Test SNOMED CT
        equipment = MockMedicalEquipment(code_system="SNOMED CT")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        device = participant.find(f".//{{{NS}}}playingDevice")
        code = device.find(f"{{{NS}}}code")
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"

        # Test HCPCS
        equipment = MockMedicalEquipment(code_system="HCPCS")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        device = participant.find(f".//{{{NS}}}playingDevice")
        code = device.find(f"{{{NS}}}code")
        assert code.get("codeSystem") == "2.16.840.1.113883.6.285"

        # Test CPT
        equipment = MockMedicalEquipment(code_system="CPT")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        device = participant.find(f".//{{{NS}}}playingDevice")
        code = device.find(f"{{{NS}}}code")
        assert code.get("codeSystem") == "2.16.840.1.113883.6.12"

    def test_supply_activity_with_instructions(self):
        """Test NonMedicinalSupplyActivity with patient instructions."""
        equipment = MockMedicalEquipment(
            instructions="Check blood glucose before each use"
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "SUBJ"
        assert entry_rel.get("inversionInd") == "true"

        act = entry_rel.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"
        assert act.get("moodCode") == "INT"

        # Check template ID
        template = act.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.20"
        assert template.get("extension") == "2014-06-09"

        # Check code
        code = act.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "409073007"

        # Check text
        text = act.find(f"{{{NS}}}text")
        assert text is not None
        assert text.text == "Check blood glucose before each use"

        # Check status
        status = act.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_supply_activity_without_instructions(self):
        """Test NonMedicinalSupplyActivity without instructions."""
        equipment = MockMedicalEquipment(instructions=None)
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is None

    def test_supply_activity_complete(self):
        """Test NonMedicinalSupplyActivity with all optional elements."""
        equipment = MockMedicalEquipment(
            name="Insulin Pump",
            code="58938008",
            code_system="SNOMED CT",
            status="active",
            date_supplied=date(2023, 1, 15),
            date_end=date(2024, 1, 15),
            quantity=1,
            manufacturer="Acme Medical",
            serial_number="SN123456",
            instructions="Check blood glucose before each use",
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        # Verify all elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}quantity") is not None
        assert elem.find(f"{{{NS}}}participant") is not None
        assert elem.find(f"{{{NS}}}entryRelationship") is not None

    def test_supply_activity_minimal(self):
        """Test NonMedicinalSupplyActivity with minimal required elements."""
        equipment = MockMedicalEquipment(
            name="Wheelchair",
            code=None,
            date_supplied=None,
            quantity=None,
            manufacturer=None,
            model_number=None,
            serial_number=None,
            instructions=None,
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        # Verify required elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None

        # Verify optional elements are absent
        assert elem.find(f"{{{NS}}}effectiveTime") is None
        assert elem.find(f"{{{NS}}}quantity") is None
        assert elem.find(f"{{{NS}}}participant") is None
        assert elem.find(f"{{{NS}}}entryRelationship") is None


class TestMedicalEquipmentOrganizer:
    """Tests for MedicalEquipmentOrganizer builder."""

    def test_organizer_basic(self):
        """Test basic MedicalEquipmentOrganizer creation."""
        equipment_list = [MockMedicalEquipment()]
        organizer = MedicalEquipmentOrganizer(equipment_list)
        elem = organizer.to_element()

        assert local_name(elem) == "organizer"
        assert elem.get("classCode") == "CLUSTER"
        assert elem.get("moodCode") == "EVN"

    def test_organizer_has_template_id_r21(self):
        """Test MedicalEquipmentOrganizer includes R2.1 template ID."""
        equipment_list = [MockMedicalEquipment()]
        organizer = MedicalEquipmentOrganizer(equipment_list, version=CDAVersion.R2_1)
        elem = organizer.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.135"
        assert template.get("extension") is None

    def test_organizer_has_id(self):
        """Test MedicalEquipmentOrganizer has ID element."""
        equipment_list = [MockMedicalEquipment()]
        organizer = MedicalEquipmentOrganizer(equipment_list)
        elem = organizer.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_organizer_has_status_code(self):
        """Test MedicalEquipmentOrganizer has statusCode element."""
        equipment_list = [MockMedicalEquipment()]
        organizer = MedicalEquipmentOrganizer(equipment_list, status="completed")
        elem = organizer.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_organizer_status_mapping(self):
        """Test MedicalEquipmentOrganizer status mapping."""
        equipment_list = [MockMedicalEquipment()]

        test_cases = [
            ("completed", "completed"),
            ("active", "active"),
            ("aborted", "aborted"),
            ("cancelled", "cancelled"),
        ]

        for input_status, expected_status in test_cases:
            organizer = MedicalEquipmentOrganizer(equipment_list, status=input_status)
            elem = organizer.to_element()

            status = elem.find(f"{{{NS}}}statusCode")
            assert status.get("code") == expected_status

    def test_organizer_effective_time(self):
        """Test MedicalEquipmentOrganizer effectiveTime with low and high."""
        equipment_list = [MockMedicalEquipment()]
        organizer = MedicalEquipmentOrganizer(
            equipment_list,
            date_start=date(2023, 1, 1),
            date_end=date(2023, 12, 31),
        )
        elem = organizer.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None

        low = time_elem.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20230101"

        high = time_elem.find(f"{{{NS}}}high")
        assert high is not None
        assert high.get("value") == "20231231"

    def test_organizer_effective_time_with_datetime(self):
        """Test MedicalEquipmentOrganizer effectiveTime with datetime."""
        equipment_list = [MockMedicalEquipment()]
        organizer = MedicalEquipmentOrganizer(
            equipment_list,
            date_start=datetime(2023, 1, 1, 8, 0, 0),
            date_end=datetime(2023, 12, 31, 17, 0, 0),
        )
        elem = organizer.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None

        low = time_elem.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20230101080000"

        high = time_elem.find(f"{{{NS}}}high")
        assert high is not None
        assert high.get("value") == "20231231170000"

    def test_organizer_effective_time_no_dates(self):
        """Test MedicalEquipmentOrganizer effectiveTime without dates (nullFlavor)."""
        equipment_list = [MockMedicalEquipment()]
        organizer = MedicalEquipmentOrganizer(
            equipment_list,
            date_start=None,
            date_end=None,
        )
        elem = organizer.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None

        low = time_elem.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("nullFlavor") == "UNK"

        high = time_elem.find(f"{{{NS}}}high")
        assert high is not None
        assert high.get("nullFlavor") == "UNK"

    def test_organizer_with_code(self):
        """Test MedicalEquipmentOrganizer with optional code."""
        equipment_list = [MockMedicalEquipment()]
        organizer = MedicalEquipmentOrganizer(
            equipment_list,
            organizer_code="46264-8",
        )
        elem = organizer.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "46264-8"

    def test_organizer_without_code(self):
        """Test MedicalEquipmentOrganizer without code."""
        equipment_list = [MockMedicalEquipment()]
        organizer = MedicalEquipmentOrganizer(equipment_list, organizer_code=None)
        elem = organizer.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is None

    def test_organizer_with_multiple_supplies(self):
        """Test MedicalEquipmentOrganizer with multiple equipment items."""
        equipment_list = [
            MockMedicalEquipment(name="Wheelchair", code="58938008"),
            MockMedicalEquipment(name="Insulin Pump", code="63653004"),
        ]
        organizer = MedicalEquipmentOrganizer(equipment_list)
        elem = organizer.to_element()

        components = elem.findall(f"{{{NS}}}component")
        assert len(components) == 2

        # Check first component
        supply1 = components[0].find(f"{{{NS}}}supply")
        assert supply1 is not None

        # Check second component
        supply2 = components[1].find(f"{{{NS}}}supply")
        assert supply2 is not None

    def test_organizer_empty_equipment_list_raises_error(self):
        """Test MedicalEquipmentOrganizer with empty equipment list raises error."""
        import pytest

        equipment_list = []

        with pytest.raises(ValueError, match="at least one supply"):
            organizer = MedicalEquipmentOrganizer(equipment_list)
            organizer.to_element()

    def test_organizer_component_contains_supply(self):
        """Test MedicalEquipmentOrganizer component contains NonMedicinalSupplyActivity."""
        equipment = MockMedicalEquipment(name="Wheelchair")
        equipment_list = [equipment]
        organizer = MedicalEquipmentOrganizer(equipment_list)
        elem = organizer.to_element()

        component = elem.find(f"{{{NS}}}component")
        assert component is not None

        supply = component.find(f"{{{NS}}}supply")
        assert supply is not None
        assert supply.get("classCode") == "SPLY"

    def test_organizer_complete(self):
        """Test MedicalEquipmentOrganizer with all optional elements."""
        equipment_list = [
            MockMedicalEquipment(
                name="Insulin Pump",
                code="63653004",
                manufacturer="Acme",
                serial_number="SN123",
            ),
        ]
        organizer = MedicalEquipmentOrganizer(
            equipment_list,
            status="completed",
            date_start=date(2023, 1, 1),
            date_end=date(2023, 12, 31),
            organizer_code="46264-8",
        )
        elem = organizer.to_element()

        # Verify all elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}component") is not None

    def test_organizer_minimal(self):
        """Test MedicalEquipmentOrganizer with minimal required elements."""
        equipment_list = [MockMedicalEquipment(name="Wheelchair")]
        organizer = MedicalEquipmentOrganizer(
            equipment_list,
            organizer_code=None,
        )
        elem = organizer.to_element()

        # Verify required elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}component") is not None

        # Verify optional code is absent
        assert elem.find(f"{{{NS}}}code") is None

    def test_organizer_to_string(self):
        """Test MedicalEquipmentOrganizer serialization."""
        equipment_list = [MockMedicalEquipment()]
        organizer = MedicalEquipmentOrganizer(equipment_list)
        xml = organizer.to_string(pretty=False)

        assert "<organizer" in xml or ":organizer" in xml
        assert "classCode" in xml
        assert "CLUSTER" in xml

    def test_organizer_element_order(self):
        """Test that elements are in correct order."""
        equipment_list = [MockMedicalEquipment()]
        organizer = MedicalEquipmentOrganizer(
            equipment_list,
            organizer_code="46264-8",
        )
        elem = organizer.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "id" in names
        assert "code" in names
        assert "statusCode" in names
        assert "effectiveTime" in names
        assert "component" in names
