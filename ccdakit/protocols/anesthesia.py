"""Protocol for Anesthesia data in C-CDA documents."""

from datetime import date, datetime
from typing import Optional, Protocol

from ccdakit.protocols.medication import MedicationProtocol


class AnesthesiaProtocol(Protocol):
    """
    Protocol defining the interface for anesthesia data.

    Represents anesthesia information including the type of anesthesia
    (e.g., general, local, regional) and the actual agents/medications used.
    Used with AnesthesiaSection builder for Procedure Notes and Operative Notes.

    This protocol is based on the Anesthesia Section (V2) template:
    Template ID: 2.16.840.1.113883.10.20.22.2.25 (2014-06-09)

    The Anesthesia Section MAY contain:
    - Procedure Activity Procedure (V2) - describing the anesthesia procedure/type
    - Medication Activity (V2) - describing the anesthesia agents used
    """

    @property
    def anesthesia_type(self) -> str:
        """
        Type of anesthesia administered.

        Common values:
        - 'General anesthesia'
        - 'Local anesthesia'
        - 'Regional anesthesia'
        - 'Spinal anesthesia'
        - 'Epidural anesthesia'
        - 'Conscious sedation'

        Returns:
            Human-readable anesthesia type
        """
        ...

    @property
    def anesthesia_code(self) -> str:
        """
        SNOMED CT code for the anesthesia type.

        Example codes:
        - '50697003' for General anesthesia
        - '386761002' for Local anesthesia
        - '231249005' for Regional anesthesia
        - '18946005' for Epidural anesthesia
        - '50697003' for General anesthesia

        Returns:
            SNOMED CT code for anesthesia type
        """
        ...

    @property
    def anesthesia_code_system(self) -> str:
        """
        Code system for the anesthesia code.

        Typically 'SNOMED CT' for anesthesia procedures.

        Returns:
            Code system (usually 'SNOMED CT')
        """
        ...

    @property
    def start_time(self) -> Optional[date | datetime]:
        """
        Date/time when anesthesia was started.

        Can be a date or datetime. Optional but recommended for
        tracking anesthesia duration.

        Returns:
            Start date/time or None
        """
        ...

    @property
    def end_time(self) -> Optional[date | datetime]:
        """
        Date/time when anesthesia was stopped.

        Can be a date or datetime. Optional but recommended for
        tracking anesthesia duration.

        Returns:
            End date/time or None
        """
        ...

    @property
    def status(self) -> str:
        """
        Status of the anesthesia procedure.

        Common values: 'completed', 'active', 'aborted'

        Returns:
            Anesthesia status
        """
        ...

    @property
    def anesthesia_agents(self) -> "Optional[list[MedicationProtocol]]":
        """
        List of anesthesia medications/agents used.

        Optional. Each agent should satisfy MedicationProtocol.
        Examples: Propofol, Sevoflurane, Fentanyl, Lidocaine

        Returns:
            List of anesthesia medications or None
        """
        ...

    @property
    def route(self) -> Optional[str]:
        """
        Primary route of administration for anesthesia.

        Optional. Common values:
        - 'Inhalation'
        - 'Intravenous'
        - 'Intramuscular'
        - 'Subcutaneous'
        - 'Topical'

        Returns:
            Route of administration or None
        """
        ...

    @property
    def performer_name(self) -> Optional[str]:
        """
        Name of the anesthesiologist or anesthetist.

        Optional. Example: 'Dr. John Smith, MD'

        Returns:
            Performer name or None
        """
        ...

    @property
    def notes(self) -> Optional[str]:
        """
        Additional clinical notes about the anesthesia.

        Optional. Free-text notes about complications, patient response,
        or other relevant clinical observations.

        Returns:
            Clinical notes or None
        """
        ...
