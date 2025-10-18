"""Medication-related protocols for C-CDA documents."""

from datetime import date
from typing import Optional, Protocol


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
