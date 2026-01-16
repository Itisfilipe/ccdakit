"""Example of creating a Medical Equipment Section."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.medical_equipment import MedicalEquipmentSection
from ccdakit.core.base import CDAVersion


# Define medical equipment data
class ExampleEquipment:
    """Example medical equipment data."""

    def __init__(
        self,
        name,
        code=None,
        code_system=None,
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


def main():
    """Create and display a Medical Equipment Section example."""

    # Create medical equipment items
    wheelchair = ExampleEquipment(
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
        instructions="Use for mobility assistance as needed",
    )

    cpap_machine = ExampleEquipment(
        name="Continuous Positive Airway Pressure Device",
        code="261323006",
        code_system="SNOMED CT",
        status="active",
        date_supplied=date(2023, 3, 10),
        quantity=1,
        manufacturer="SleepTech Medical",
        model_number="CPAP-Pro-3000",
        serial_number="(01)00643169001763(11)141231(17)150707(10)A213B1(21)1234",
        instructions="Use nightly with heated humidifier. Clean mask daily.",
    )

    insulin_pump = ExampleEquipment(
        name="Insulin Pump",
        code="43148006",
        code_system="SNOMED CT",
        status="active",
        date_supplied=date(2023, 5, 20),
        quantity=1,
        manufacturer="DiabetesCare Corp",
        model_number="IP-2000X",
        serial_number="SN-IP-98765",
        instructions="Check blood glucose before each use. Replace infusion set every 3 days.",
    )

    # Create the Medical Equipment Section
    section = MedicalEquipmentSection(
        equipment_list=[wheelchair, cpap_machine, insulin_pump],
        title="Medical Equipment",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Medical Equipment Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.23")
    print("  - Extension: 2014-06-09")
    print("  - Number of equipment items: 3")
    print(f"    1. {wheelchair.name} - {wheelchair.manufacturer} ({wheelchair.status})")
    print(f"    2. {cpap_machine.name} - {cpap_machine.manufacturer} ({cpap_machine.status})")
    print(f"    3. {insulin_pump.name} - {insulin_pump.manufacturer} ({insulin_pump.status})")
    print("\nConformance:")
    print("  - CONF:1098-7944: Template ID present")
    print("  - CONF:1098-15382: Code 46264-8 (Medical Equipment)")
    print("  - CONF:1098-7946: Title present")
    print("  - CONF:1098-7947: Narrative text present")
    print("  - CONF:1098-31125: Non-Medicinal Supply Activity entries present")
    print("\nFeatures demonstrated:")
    print("  - Complete equipment details (code, manufacturer, model, serial)")
    print("  - Date ranges (supplied and end dates)")
    print("  - Patient instructions")
    print("  - UDI format serial number (CPAP machine)")
    print("  - Multiple equipment statuses (completed, active)")


if __name__ == "__main__":
    main()
