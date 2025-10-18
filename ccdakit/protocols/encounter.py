"""Protocol for Encounter data in C-CDA documents."""

from __future__ import annotations

from datetime import date, datetime
from typing import Protocol


class EncounterProtocol(Protocol):
    """
    Protocol defining the interface for encounter data.

    Represents healthcare encounters (visits, appointments, admissions, etc.).
    Used with EncounterActivity and EncountersSection builders.
    """

    @property
    def encounter_type(self) -> str:
        """Encounter type/description (e.g., 'Office Visit', 'Emergency Room')."""
        ...

    @property
    def code(self) -> str:
        """
        Encounter type code.

        Should be from ValueSet EncounterTypeCode (2.16.840.1.113883.3.88.12.80.32).
        Common codes include CPT, SNOMED CT, or local codes.
        Example: '99213' (CPT code for office visit)
        """
        ...

    @property
    def code_system(self) -> str:
        """
        Code system for the encounter code.

        Examples: 'CPT-4', 'SNOMED CT', 'ActCode'
        """
        ...

    @property
    def date(self) -> date | datetime | None:
        """
        Date/time when the encounter occurred.

        Can be a date or datetime. Required for encounters.
        For ongoing encounters, this represents the start date.
        """
        ...

    @property
    def end_date(self) -> date | datetime | None:
        """
        End date/time of the encounter.

        Optional. If provided along with date, creates a time interval.
        If not provided, the encounter is considered a point in time.
        """
        ...

    @property
    def location(self) -> str | None:
        """
        Location where the encounter took place.

        Optional. Example: 'Community Health Hospital', 'Main Clinic'
        """
        ...

    @property
    def performer_name(self) -> str | None:
        """
        Name of the healthcare provider who performed the encounter.

        Optional. Example: 'Dr. John Smith'
        """
        ...

    @property
    def discharge_disposition(self) -> str | None:
        """
        Patient discharge disposition.

        Optional. Example: 'Home', 'Skilled Nursing Facility'
        Only applicable for inpatient encounters.
        """
        ...
