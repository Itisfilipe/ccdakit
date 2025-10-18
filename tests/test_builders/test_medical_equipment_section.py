"""Tests for Medical Equipment Section and related builders."""

from datetime import date, datetime

from lxml import etree
import pytest

from ccdakit.builders.sections.medical_equipment import MedicalEquipmentSection
from ccdakit.builders.entries.medical_equipment import (
    NonMedicinalSupplyActivity,
    MedicalEquipmentOrganizer,
)
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockEquipment:
    """Mock medical equipment for testing."""

    def __init__(
        self,
        name="Wheelchair",
        code="58938008",
        code_system="SNOMED CT",
        status="completed",
        date_supplied=None,
        date_end=None,
        quantity=None,
        manufacturer=None,
        model_number=None,
        serial_number=None,
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

    def test_basic_supply_creation(self):
        """Test basic supply activity creation."""
        equipment = MockEquipment()
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        assert local_name(elem) == "supply"
        assert elem.get("classCode") == "SPLY"  # CONF:1098-8745
        assert elem.get("moodCode") in ["EVN", "INT"]  # CONF:1098-8746

    def test_supply_has_template_id_r21(self):
        """Test supply includes R2.1 template ID."""
        equipment = MockEquipment()
        supply = NonMedicinalSupplyActivity(equipment, version=CDAVersion.R2_1)
        elem = supply.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.50"  # CONF:1098-10509
        assert template.get("extension") == "2014-06-09"  # CONF:1098-32514

    def test_supply_has_id(self):
        """Test supply includes ID element."""
        equipment = MockEquipment()
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None  # CONF:1098-8748
        assert id_elem.get("root") is not None

    def test_supply_has_status_code(self):
        """Test supply includes status code."""
        equipment = MockEquipment(status="completed")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None  # CONF:1098-8749
        assert status.get("code") == "completed"  # CONF:1098-32363

    def test_supply_status_mapping(self):
        """Test various status code mappings."""
        statuses = ["completed", "active", "aborted", "cancelled"]
        for status in statuses:
            equipment = MockEquipment(status=status)
            supply = NonMedicinalSupplyActivity(equipment)
            elem = supply.to_element()

            status_elem = elem.find(f"{{{NS}}}statusCode")
            assert status_elem.get("code") == status

    def test_supply_mood_code_event(self):
        """Test mood code is EVN for completed status."""
        equipment = MockEquipment(status="completed")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        assert elem.get("moodCode") == "EVN"

    def test_supply_mood_code_intent(self):
        """Test mood code is INT for new status."""
        equipment = MockEquipment(status="new")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        assert elem.get("moodCode") == "INT"

    def test_supply_with_effective_time_single(self):
        """Test supply with single date."""
        equipment = MockEquipment(date_supplied=date(2023, 6, 15))
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None  # CONF:1098-15498
        assert time_elem.get("value") == "20230615"

    def test_supply_with_effective_time_range(self):
        """Test supply with date range."""
        equipment = MockEquipment(
            date_supplied=date(2023, 6, 15), date_end=date(2023, 12, 31)
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None  # CONF:1098-15498

        low = time_elem.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20230615"

        high = time_elem.find(f"{{{NS}}}high")
        assert high is not None  # CONF:1098-16867
        assert high.get("value") == "20231231"

    def test_supply_with_effective_time_range_datetime(self):
        """Test supply with datetime range."""
        equipment = MockEquipment(
            date_supplied=datetime(2023, 6, 15, 9, 30, 0),
            date_end=datetime(2023, 12, 31, 17, 45, 0)
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None

        low = time_elem.find(f"{{{NS}}}low")
        assert low.get("value") == "20230615093000"

        high = time_elem.find(f"{{{NS}}}high")
        assert high.get("value") == "20231231174500"

    def test_supply_with_datetime(self):
        """Test supply with datetime instead of date."""
        equipment = MockEquipment(date_supplied=datetime(2023, 6, 15, 14, 30, 0))
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None
        assert time_elem.get("value") == "20230615143000"

    def test_supply_with_quantity(self):
        """Test supply with quantity."""
        equipment = MockEquipment(quantity=30)
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        quantity_elem = elem.find(f"{{{NS}}}quantity")
        assert quantity_elem is not None  # CONF:1098-8751
        assert quantity_elem.get("value") == "30"

    def test_supply_without_quantity(self):
        """Test supply without quantity."""
        equipment = MockEquipment(quantity=None)
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        quantity_elem = elem.find(f"{{{NS}}}quantity")
        assert quantity_elem is None

    def test_supply_with_product_instance(self):
        """Test supply with product instance participant."""
        equipment = MockEquipment(
            manufacturer="Acme Medical",
            model_number="XYZ-123",
            serial_number="SN123456",
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        assert participant is not None  # CONF:1098-8752
        assert participant.get("typeCode") == "PRD"  # CONF:1098-8754

        role = participant.find(f"{{{NS}}}participantRole")
        assert role is not None  # CONF:1098-15900
        assert role.get("classCode") == "MANU"  # CONF:81-7900

    def test_product_instance_template_id(self):
        """Test product instance has correct template ID."""
        equipment = MockEquipment(manufacturer="Acme Medical")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        role = participant.find(f"{{{NS}}}participantRole")
        template = role.find(f"{{{NS}}}templateId")

        assert template is not None  # CONF:81-7901
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.37"  # CONF:81-10522

    def test_product_instance_with_serial_number(self):
        """Test product instance with serial number."""
        equipment = MockEquipment(serial_number="SN123456")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        role = participant.find(f"{{{NS}}}participantRole")
        id_elem = role.find(f"{{{NS}}}id")

        assert id_elem is not None  # CONF:81-7902
        assert id_elem.get("extension") == "SN123456"

    def test_product_instance_with_udi(self):
        """Test product instance with UDI format."""
        udi = "(01)00643169001763(11)141231(17)150707(10)A213B1(21)1234"
        equipment = MockEquipment(serial_number=udi)
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        role = participant.find(f"{{{NS}}}participantRole")
        id_elem = role.find(f"{{{NS}}}id")

        assert id_elem.get("root") == "2.16.840.1.113883.3.3719"  # FDA UDI OID
        assert id_elem.get("extension") == udi

    def test_product_instance_playing_device(self):
        """Test product instance has playingDevice."""
        equipment = MockEquipment(
            code="58938008", code_system="SNOMED CT", manufacturer="Acme"
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        role = participant.find(f"{{{NS}}}participantRole")
        device = role.find(f"{{{NS}}}playingDevice")

        assert device is not None  # CONF:81-7903

    def test_product_instance_device_code(self):
        """Test product instance device has code."""
        equipment = MockEquipment(
            code="58938008",
            code_system="SNOMED CT",
            name="Wheelchair",
            manufacturer="Acme",
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        role = participant.find(f"{{{NS}}}participantRole")
        device = role.find(f"{{{NS}}}playingDevice")
        code = device.find(f"{{{NS}}}code")

        assert code is not None  # CONF:81-16837
        assert code.get("code") == "58938008"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT OID

    def test_product_instance_scoping_entity(self):
        """Test product instance has scopingEntity."""
        equipment = MockEquipment(manufacturer="Acme Medical")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        role = participant.find(f"{{{NS}}}participantRole")
        scoping = role.find(f"{{{NS}}}scopingEntity")

        assert scoping is not None  # CONF:81-7905

        id_elem = scoping.find(f"{{{NS}}}id")
        assert id_elem is not None  # CONF:81-7908
        assert id_elem.get("extension") == "Acme Medical"

    def test_supply_with_instructions(self):
        """Test supply with patient instructions."""
        equipment = MockEquipment(instructions="Use twice daily")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is not None  # CONF:1098-30277
        assert entry_rel.get("typeCode") == "SUBJ"  # CONF:1098-30278
        assert entry_rel.get("inversionInd") == "true"  # CONF:1098-30279

    def test_instruction_template(self):
        """Test instruction has correct template."""
        equipment = MockEquipment(instructions="Use twice daily")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        act = entry_rel.find(f"{{{NS}}}act")

        assert act is not None  # CONF:1098-31393
        assert act.get("classCode") == "ACT"  # CONF:1098-7391
        assert act.get("moodCode") == "INT"  # CONF:1098-7392

        template = act.find(f"{{{NS}}}templateId")
        assert template is not None  # CONF:1098-7393
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.20"  # CONF:1098-10503
        assert template.get("extension") == "2014-06-09"  # CONF:1098-32598

    def test_instruction_content(self):
        """Test instruction contains text."""
        instruction_text = "Check blood glucose before each use"
        equipment = MockEquipment(instructions=instruction_text)
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        act = entry_rel.find(f"{{{NS}}}act")
        text = act.find(f"{{{NS}}}text")

        assert text is not None
        assert text.text == instruction_text

    def test_instruction_status_code(self):
        """Test instruction has completed status."""
        equipment = MockEquipment(instructions="Use as directed")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        entry_rel = elem.find(f"{{{NS}}}entryRelationship")
        act = entry_rel.find(f"{{{NS}}}act")
        status = act.find(f"{{{NS}}}statusCode")

        assert status is not None  # CONF:1098-7396
        assert status.get("code") == "completed"  # CONF:1098-19106

    def test_supply_without_product_instance(self):
        """Test supply without product instance data."""
        equipment = MockEquipment(
            manufacturer=None, model_number=None, serial_number=None, code=None
        )
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        assert participant is None

    def test_code_system_mapping(self):
        """Test code system OID mapping."""
        equipment = MockEquipment(code="E0143", code_system="HCPCS", manufacturer="Acme")
        supply = NonMedicinalSupplyActivity(equipment)
        elem = supply.to_element()

        participant = elem.find(f"{{{NS}}}participant")
        role = participant.find(f"{{{NS}}}participantRole")
        device = role.find(f"{{{NS}}}playingDevice")
        code = device.find(f"{{{NS}}}code")

        assert code.get("codeSystem") == "2.16.840.1.113883.6.285"  # HCPCS OID


class TestMedicalEquipmentOrganizer:
    """Tests for MedicalEquipmentOrganizer builder."""

    def test_basic_organizer_creation(self):
        """Test basic organizer creation."""
        equipment = MockEquipment()
        organizer = MedicalEquipmentOrganizer([equipment])
        elem = organizer.to_element()

        assert local_name(elem) == "organizer"
        assert elem.get("classCode") == "CLUSTER"  # CONF:1098-31020
        assert elem.get("moodCode") == "EVN"  # CONF:1098-31021

    def test_organizer_has_template_id(self):
        """Test organizer includes template ID."""
        equipment = MockEquipment()
        organizer = MedicalEquipmentOrganizer([equipment])
        elem = organizer.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None  # CONF:1098-31022
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.135"  # CONF:1098-31023
        assert template.get("extension") is None  # No extension for this template

    def test_organizer_has_id(self):
        """Test organizer includes ID."""
        equipment = MockEquipment()
        organizer = MedicalEquipmentOrganizer([equipment])
        elem = organizer.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None  # CONF:1098-31024
        assert id_elem.get("root") is not None

    def test_organizer_has_status_code(self):
        """Test organizer includes status code."""
        equipment = MockEquipment()
        organizer = MedicalEquipmentOrganizer([equipment], status="completed")
        elem = organizer.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None  # CONF:1098-31026
        assert status.get("code") == "completed"  # CONF:1098-31029

    def test_organizer_has_effective_time(self):
        """Test organizer includes effectiveTime with low and high."""
        equipment = MockEquipment()
        organizer = MedicalEquipmentOrganizer(
            [equipment],
            date_start=date(2023, 1, 1),
            date_end=date(2023, 12, 31),
        )
        elem = organizer.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None  # CONF:1098-32136

        low = time_elem.find(f"{{{NS}}}low")
        assert low is not None  # CONF:1098-32378
        assert low.get("value") == "20230101"

        high = time_elem.find(f"{{{NS}}}high")
        assert high is not None  # CONF:1098-32379
        assert high.get("value") == "20231231"

    def test_organizer_effective_time_null_flavors(self):
        """Test organizer effectiveTime with null flavors for missing dates."""
        equipment = MockEquipment()
        organizer = MedicalEquipmentOrganizer([equipment])
        elem = organizer.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        low = time_elem.find(f"{{{NS}}}low")
        high = time_elem.find(f"{{{NS}}}high")

        assert low.get("nullFlavor") == "UNK"
        assert high.get("nullFlavor") == "UNK"

    def test_organizer_effective_time_with_datetime(self):
        """Test organizer effectiveTime with datetime objects."""
        equipment = MockEquipment()
        organizer = MedicalEquipmentOrganizer(
            [equipment],
            date_start=datetime(2023, 1, 1, 8, 0, 0),
            date_end=datetime(2023, 12, 31, 17, 30, 0),
        )
        elem = organizer.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        low = time_elem.find(f"{{{NS}}}low")
        high = time_elem.find(f"{{{NS}}}high")

        assert low.get("value") == "20230101080000"
        assert high.get("value") == "20231231173000"

    def test_organizer_has_components(self):
        """Test organizer includes component elements."""
        equipment1 = MockEquipment(name="Equipment 1")
        equipment2 = MockEquipment(name="Equipment 2")
        organizer = MedicalEquipmentOrganizer([equipment1, equipment2])
        elem = organizer.to_element()

        components = elem.findall(f"{{{NS}}}component")
        assert len(components) == 2  # CONF:1098-31027

    def test_organizer_component_has_supply(self):
        """Test organizer component contains supply."""
        equipment = MockEquipment()
        organizer = MedicalEquipmentOrganizer([equipment])
        elem = organizer.to_element()

        component = elem.find(f"{{{NS}}}component")
        supply = component.find(f"{{{NS}}}supply")

        assert supply is not None  # CONF:1098-31862
        assert supply.get("classCode") == "SPLY"

    def test_organizer_empty_list_raises_error(self):
        """Test organizer with empty list raises error."""
        with pytest.raises(ValueError, match="at least one supply"):
            organizer = MedicalEquipmentOrganizer([])
            organizer.to_element()  # CONF:1098-32380

    def test_organizer_with_code(self):
        """Test organizer with optional code."""
        equipment = MockEquipment()
        organizer = MedicalEquipmentOrganizer([equipment], organizer_code="12345")
        elem = organizer.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None  # CONF:1098-31025
        assert code.get("code") == "12345"

    def test_organizer_without_code(self):
        """Test organizer without code."""
        equipment = MockEquipment()
        organizer = MedicalEquipmentOrganizer([equipment])
        elem = organizer.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is None


class TestMedicalEquipmentSection:
    """Tests for MedicalEquipmentSection builder."""

    def test_section_basic_creation(self):
        """Test basic section creation."""
        equipment = MockEquipment()
        section = MedicalEquipmentSection([equipment])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_has_template_id_r21(self):
        """Test section includes R2.1 template ID."""
        equipment = MockEquipment()
        section = MedicalEquipmentSection([equipment], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None  # CONF:1098-7944
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.23"  # CONF:1098-10404
        assert template.get("extension") == "2014-06-09"  # CONF:1098-32523

    def test_section_has_code(self):
        """Test section includes section code."""
        equipment = MockEquipment()
        section = MedicalEquipmentSection([equipment])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None  # CONF:1098-15381
        assert code.get("code") == "46264-8"  # CONF:1098-15382
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # CONF:1098-30828

    def test_section_has_title(self):
        """Test section includes title."""
        equipment = MockEquipment()
        section = MedicalEquipmentSection([equipment], title="My Equipment")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None  # CONF:1098-7946
        assert title.text == "My Equipment"

    def test_section_default_title(self):
        """Test section uses default title."""
        equipment = MockEquipment()
        section = MedicalEquipmentSection([equipment])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Medical Equipment"

    def test_section_has_text(self):
        """Test section includes narrative text."""
        equipment = MockEquipment()
        section = MedicalEquipmentSection([equipment])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None  # CONF:1098-7947

    def test_section_narrative_table(self):
        """Test narrative includes HTML table."""
        equipment = MockEquipment(name="Insulin Pump")
        section = MedicalEquipmentSection([equipment])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        assert table is not None
        assert table.get("border") == "1"

        thead = table.find(f"{{{NS}}}thead")
        assert thead is not None
        tr = thead.find(f"{{{NS}}}tr")
        ths = tr.findall(f"{{{NS}}}th")
        assert len(ths) == 8  # All columns

    def test_section_empty_narrative(self):
        """Test narrative when no equipment."""
        section = MedicalEquipmentSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No medical equipment recorded"

        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_section_has_entries(self):
        """Test section includes entry elements."""
        equipment = MockEquipment()
        section = MedicalEquipmentSection([equipment])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1  # CONF:1098-31125

    def test_section_entry_has_supply(self):
        """Test entry contains supply element."""
        equipment = MockEquipment()
        section = MedicalEquipmentSection([equipment])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        supply = entry.find(f"{{{NS}}}supply")
        assert supply is not None  # CONF:1098-31861

    def test_section_multiple_entries(self):
        """Test section with multiple equipment items."""
        equipment1 = MockEquipment(name="Equipment 1")
        equipment2 = MockEquipment(name="Equipment 2")
        section = MedicalEquipmentSection([equipment1, equipment2])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_section_with_organizer(self):
        """Test section using organizer."""
        equipment1 = MockEquipment(name="Equipment 1")
        equipment2 = MockEquipment(name="Equipment 2")
        section = MedicalEquipmentSection(
            [equipment1, equipment2],
            use_organizer=True,
            organizer_start_date=date(2023, 1, 1),
            organizer_end_date=date(2023, 12, 31),
        )
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1  # Single entry for organizer

        entry = elem.find(f"{{{NS}}}entry")
        organizer = entry.find(f"{{{NS}}}organizer")
        assert organizer is not None  # CONF:1098-30351

    def test_section_narrative_with_all_fields(self):
        """Test narrative table with all fields populated."""
        equipment = MockEquipment(
            name="Insulin Pump",
            code="43148006",
            code_system="SNOMED CT",
            date_supplied=date(2023, 6, 15),
            date_end=date(2023, 12, 31),
            quantity=1,
            status="active",
            manufacturer="Acme Medical",
            model_number="IP-2000",
            serial_number="SN98765",
        )
        section = MedicalEquipmentSection([equipment])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        assert len(tds) == 8
        # Check some content
        assert "Insulin Pump" in etree.tostring(tds[0], encoding="unicode")
        assert "43148006" in tds[1].text
        assert "2023-06-15" in tds[2].text
        assert "2023-12-31" in tds[3].text
        assert "1" in tds[4].text
        assert "Active" in tds[5].text
        assert "Acme Medical" in tds[6].text
        assert "Model: IP-2000" in tds[7].text
        assert "S/N: SN98765" in tds[7].text

    def test_section_narrative_with_missing_fields(self):
        """Test narrative table with missing optional fields."""
        equipment = MockEquipment(
            name="Walker",
            code=None,
            code_system=None,
            date_supplied=None,
            quantity=None,
            manufacturer=None,
        )
        section = MedicalEquipmentSection([equipment])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check that missing fields show "-"
        assert tds[1].text == "-"  # code
        assert tds[2].text == "-"  # date supplied
        assert tds[4].text == "-"  # quantity
        assert tds[6].text == "-"  # manufacturer

    def test_section_narrative_with_datetime_fields(self):
        """Test narrative table with datetime fields."""
        equipment = MockEquipment(
            name="Monitor",
            date_supplied=datetime(2023, 6, 15, 10, 30, 0),
            date_end=datetime(2023, 12, 31, 16, 45, 0),
        )
        section = MedicalEquipmentSection([equipment])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check datetime formatting in narrative
        assert "2023-06-15 10:30" in tds[2].text  # date supplied
        assert "2023-12-31 16:45" in tds[3].text  # date end

    def test_section_structure_order(self):
        """Test section elements are in correct order."""
        equipment = MockEquipment()
        section = MedicalEquipmentSection([equipment])
        elem = section.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        assert "templateId" in names
        assert "code" in names
        assert "title" in names
        assert "text" in names
        assert "entry" in names

        assert names.index("templateId") < names.index("code")
        assert names.index("code") < names.index("title")
        assert names.index("title") < names.index("text")
        assert names.index("text") < names.index("entry")

    def test_section_r20_version(self):
        """Test section with R2.0 version."""
        equipment = MockEquipment()
        section = MedicalEquipmentSection([equipment], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.23"
        assert template.get("extension") == "2014-06-09"


class TestMedicalEquipmentIntegration:
    """Integration tests for medical equipment builders."""

    def test_complete_section_with_all_features(self):
        """Test creating a complete section with all features."""
        equipment1 = MockEquipment(
            name="Wheelchair",
            code="58938008",
            code_system="SNOMED CT",
            status="completed",
            date_supplied=date(2023, 1, 15),
            date_end=date(2023, 6, 30),
            quantity=1,
            manufacturer="Mobility Inc",
            model_number="WC-500",
            serial_number="WC123456",
            instructions="Use for mobility assistance",
        )

        equipment2 = MockEquipment(
            name="Insulin Pump",
            code="43148006",
            code_system="SNOMED CT",
            status="active",
            date_supplied=date(2023, 3, 20),
            quantity=1,
            manufacturer="MedTech Corp",
            model_number="IP-2000",
            serial_number="(01)00643169001763(11)141231",
            instructions="Check blood glucose levels before each use",
        )

        section = MedicalEquipmentSection(
            [equipment1, equipment2], title="Patient Medical Equipment"
        )
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify narrative
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        rows = tbody.findall(f"{{{NS}}}tr")
        assert len(rows) == 2

        # Verify entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Verify first supply has product instance
        supply1 = entries[0].find(f"{{{NS}}}supply")
        participant1 = supply1.find(f"{{{NS}}}participant")
        assert participant1 is not None

        # Verify second supply has UDI
        supply2 = entries[1].find(f"{{{NS}}}supply")
        participant2 = supply2.find(f"{{{NS}}}participant")
        role2 = participant2.find(f"{{{NS}}}participantRole")
        id2 = role2.find(f"{{{NS}}}id")
        assert id2.get("root") == "2.16.840.1.113883.3.3719"  # FDA UDI OID

        # Verify both have instructions
        instr1 = supply1.find(f"{{{NS}}}entryRelationship")
        instr2 = supply2.find(f"{{{NS}}}entryRelationship")
        assert instr1 is not None
        assert instr2 is not None

    def test_section_with_organizer_integration(self):
        """Test section with organizer integration."""
        equipment_list = [
            MockEquipment(name="Cane", status="completed"),
            MockEquipment(name="Walker", status="completed"),
            MockEquipment(name="Crutches", status="completed"),
        ]

        section = MedicalEquipmentSection(
            equipment_list,
            use_organizer=True,
            organizer_start_date=date(2023, 1, 1),
            organizer_end_date=date(2023, 12, 31),
        )
        elem = section.to_element()

        # Single entry containing organizer
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        # Organizer contains 3 components
        organizer = entries[0].find(f"{{{NS}}}organizer")
        components = organizer.findall(f"{{{NS}}}component")
        assert len(components) == 3

        # Each component has a supply
        for component in components:
            supply = component.find(f"{{{NS}}}supply")
            assert supply is not None

    def test_serialization(self):
        """Test XML serialization."""
        equipment = MockEquipment(name="Blood Glucose Monitor")
        section = MedicalEquipmentSection([equipment])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "46264-8" in xml  # Section code
        assert "Medical Equipment" in xml

    def test_corner_case_no_equipment(self):
        """Test corner case with no equipment."""
        section = MedicalEquipmentSection([])
        elem = section.to_element()

        # Should still have valid structure
        assert local_name(elem) == "section"
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # No entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_corner_case_minimal_data(self):
        """Test corner case with minimal required data."""
        equipment = MockEquipment(
            name="Unknown Device",
            code=None,
            code_system=None,
            status="completed",
            date_supplied=None,
            quantity=None,
            manufacturer=None,
        )
        section = MedicalEquipmentSection([equipment])
        elem = section.to_element()

        # Should build successfully
        assert local_name(elem) == "section"

        # Supply should have minimal required elements
        supply = elem.find(f".//{{{NS}}}supply")
        assert supply is not None
        assert supply.find(f"{{{NS}}}id") is not None
        assert supply.find(f"{{{NS}}}statusCode") is not None

    def test_null_flavor_handling(self):
        """Test null flavor handling for missing data."""
        equipment = MockEquipment(manufacturer=None)
        organizer = MedicalEquipmentOrganizer([equipment])
        elem = organizer.to_element()

        # effectiveTime should have null flavors
        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        low = time_elem.find(f"{{{NS}}}low")
        high = time_elem.find(f"{{{NS}}}high")

        assert low.get("nullFlavor") == "UNK"
        assert high.get("nullFlavor") == "UNK"
