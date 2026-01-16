"""Medication-related protocols for C-CDA documents."""

from datetime import date
from typing import Any, List, Optional, Protocol


class MedicationProtocol(Protocol):
    """Medication data contract."""

    @property
    def name(self) -> str:
        """
        Human-readable medication name.

        Returns:
            Medication name (e.g., "Lisinopril 10mg oral tablet")
        """
        ...

    @property
    def code(self) -> str:
        """
        RxNorm code for the medication.

        Returns:
            RxNorm code
        """
        ...

    @property
    def dosage(self) -> str:
        """
        Dosage amount (e.g., "10 mg", "1 tablet").

        Returns:
            Dosage string
        """
        ...

    @property
    def route(self) -> str:
        """
        Route of administration (e.g., "oral", "IV", "topical").

        Returns:
            Route code or display name
        """
        ...

    @property
    def frequency(self) -> str:
        """
        Frequency of administration (e.g., "twice daily", "every 6 hours").

        Returns:
            Frequency description
        """
        ...

    @property
    def start_date(self) -> date:
        """
        Date medication was started.

        Returns:
            Start date
        """
        ...

    @property
    def end_date(self) -> Optional[date]:
        """
        Date medication was stopped (None if ongoing).

        Returns:
            End date or None
        """
        ...

    @property
    def status(self) -> str:
        """
        Medication status: 'active', 'completed', 'discontinued'.

        Returns:
            Medication status
        """
        ...

    @property
    def instructions(self) -> Optional[str]:
        """
        Patient instructions (optional).

        Returns:
            Instructions or None
        """
        ...

    @property
    def authors(self) -> Optional[List[Any]]:
        """
        Author participation information (optional).

        Each author should have:
        - id: Author identifier (e.g., NPI)
        - time: When authored (datetime)

        Returns:
            List of author objects or None
        """
        ...

    @property
    def code_system(self) -> Optional[str]:
        """
        Code system for the medication code. Defaults to RxNorm if not specified.

        Common values:
        - 'RxNorm' (2.16.840.1.113883.6.88) - Preferred for medications
        - 'NDC' (2.16.840.1.113883.6.69) - National Drug Code

        Returns:
            Code system name or None (defaults to RxNorm)
        """
        ...
