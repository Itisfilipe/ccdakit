"""Plan of Treatment-related protocols for C-CDA documents."""

from datetime import date
from typing import Optional, Protocol


class PersistentIDProtocol(Protocol):
    """Persistent identifier protocol."""

    @property
    def root(self) -> str:
        """
        OID or UUID identifying the assigning authority.

        Returns:
            Root identifier (OID or UUID)
        """
        ...

    @property
    def extension(self) -> str:
        """
        Unique identifier within the root's namespace.

        Returns:
            Extension identifier
        """
        ...


class PlannedActivityProtocol(Protocol):
    """Base protocol for planned activities in Plan of Treatment."""

    @property
    def description(self) -> str:
        """
        Human-readable description of planned activity.

        Returns:
            Activity description
        """
        ...

    @property
    def code(self) -> Optional[str]:
        """
        Activity code (SNOMED, LOINC, CPT, etc.).

        Returns:
            Activity code or None
        """
        ...

    @property
    def code_system(self) -> Optional[str]:
        """
        Code system: 'SNOMED', 'LOINC', 'CPT', etc.

        Returns:
            Code system name or None
        """
        ...

    @property
    def planned_date(self) -> Optional[date]:
        """
        Date/time activity is planned for.

        Returns:
            Planned date or None
        """
        ...

    @property
    def status(self) -> str:
        """
        Status: 'active', 'cancelled', 'completed', etc.

        Returns:
            Activity status
        """
        ...

    @property
    def persistent_id(self) -> Optional[PersistentIDProtocol]:
        """
        Persistent ID across document versions.

        Returns:
            Persistent ID or None
        """
        ...


class PlannedObservationProtocol(PlannedActivityProtocol):
    """Protocol for planned observation entries."""

    pass


class PlannedProcedureProtocol(PlannedActivityProtocol):
    """Protocol for planned procedure entries."""

    @property
    def body_site(self) -> Optional[str]:
        """
        Anatomical site for procedure.

        Returns:
            Body site description or None
        """
        ...


class PlannedEncounterProtocol(PlannedActivityProtocol):
    """Protocol for planned encounter entries."""

    @property
    def encounter_type(self) -> Optional[str]:
        """
        Type of encounter (e.g., 'office visit', 'follow-up').

        Returns:
            Encounter type or None
        """
        ...


class PlannedActProtocol(PlannedActivityProtocol):
    """Protocol for planned act entries."""

    pass


class PlannedMedicationProtocol(PlannedActivityProtocol):
    """Protocol for planned medication activity entries."""

    @property
    def dose(self) -> Optional[str]:
        """
        Medication dose.

        Returns:
            Dose description or None
        """
        ...

    @property
    def route(self) -> Optional[str]:
        """
        Route of administration.

        Returns:
            Route description or None
        """
        ...

    @property
    def frequency(self) -> Optional[str]:
        """
        Medication frequency.

        Returns:
            Frequency description or None
        """
        ...


class PlannedSupplyProtocol(PlannedActivityProtocol):
    """Protocol for planned supply entries."""

    @property
    def quantity(self) -> Optional[str]:
        """
        Quantity of supply.

        Returns:
            Quantity description or None
        """
        ...


class PlannedImmunizationProtocol(PlannedActivityProtocol):
    """Protocol for planned immunization activity entries."""

    @property
    def vaccine_code(self) -> Optional[str]:
        """
        CVX vaccine code.

        Returns:
            Vaccine code or None
        """
        ...


class InstructionProtocol(Protocol):
    """Protocol for instruction entries."""

    @property
    def instruction_text(self) -> str:
        """
        Text of the instruction.

        Returns:
            Instruction text
        """
        ...

    @property
    def persistent_id(self) -> Optional[PersistentIDProtocol]:
        """
        Persistent ID across document versions.

        Returns:
            Persistent ID or None
        """
        ...
