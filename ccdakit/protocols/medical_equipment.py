"""Protocol for Medical Equipment data in C-CDA documents."""

from datetime import date, datetime
from typing import Optional, Protocol


class MedicalEquipmentProtocol(Protocol):
    """
    Protocol defining the interface for medical equipment/supply data.

    Represents equipment supplied to the patient (e.g., pumps, inhalers, wheelchairs).
    Used with NonMedicinalSupplyActivity and MedicalEquipmentSection builders.
    """

    @property
    def name(self) -> str:
        """Equipment/supply name/description (e.g., 'Wheelchair', 'Insulin Pump')."""
        ...

    @property
    def code(self) -> Optional[str]:
        """
        Equipment/supply code (e.g., from SNOMED CT).

        Optional. Should be from standard code systems like SNOMED CT, HCPCS, or CPT.
        """
        ...

    @property
    def code_system(self) -> Optional[str]:
        """
        Code system for the equipment code.

        Optional. Examples: 'SNOMED CT', 'HCPCS', 'CPT'
        """
        ...

    @property
    def status(self) -> str:
        """
        Status of the supply activity.

        Common values: 'completed', 'active', 'aborted', 'cancelled'
        """
        ...

    @property
    def date_supplied(self) -> Optional[date | datetime]:
        """
        Date/time when the equipment was supplied.

        Optional. Can be a date or datetime.
        """
        ...

    @property
    def date_end(self) -> Optional[date | datetime]:
        """
        Date/time when the equipment usage ended or is expected to end.

        Optional. Can be a date or datetime.
        """
        ...

    @property
    def quantity(self) -> Optional[int]:
        """
        Quantity of equipment/supplies provided.

        Optional. Example: 30 (for 30 syringes)
        """
        ...

    @property
    def manufacturer(self) -> Optional[str]:
        """
        Manufacturer name of the equipment.

        Optional. Example: 'Acme Medical Devices'
        """
        ...

    @property
    def model_number(self) -> Optional[str]:
        """
        Model number/identifier of the equipment.

        Optional. Example: 'Model XYZ-123'
        """
        ...

    @property
    def serial_number(self) -> Optional[str]:
        """
        Serial number/UDI of the specific equipment instance.

        Optional. Example: '(01)00643169001763(11)141231(17)150707(10)A213B1(21)1234'
        """
        ...

    @property
    def instructions(self) -> Optional[str]:
        """
        Patient instructions for using the equipment.

        Optional. Example: 'Check blood glucose before each use'
        """
        ...
