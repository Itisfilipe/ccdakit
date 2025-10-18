"""Mental status-related protocols for C-CDA documents."""

from datetime import date, datetime
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


class MentalStatusObservationProtocol(Protocol):
    """Mental status observation data contract.

    Represents observations about a patient's mental status including
    appearance, attitude, behavior, mood and affect, speech and language,
    thought process, thought content, perception, cognition, insight and judgment.
    """

    @property
    def category(self) -> str:
        """
        Category of mental status (e.g., Mood and Affect, Cognition, Behavior).

        Returns:
            Category name
        """
        ...

    @property
    def category_code(self) -> Optional[str]:
        """
        Code for the mental status category (ICF or LOINC preferred).

        Returns:
            Category code or None
        """
        ...

    @property
    def category_code_system(self) -> Optional[str]:
        """
        Code system for category: 'ICF', 'LOINC', or 'SNOMED'.

        Returns:
            Code system name or None
        """
        ...

    @property
    def value(self) -> str:
        """
        Observed value/finding (e.g., 'Depressed mood', 'Alert and oriented').

        Returns:
            Observation value
        """
        ...

    @property
    def value_code(self) -> Optional[str]:
        """
        SNOMED CT code for the observed value.

        Returns:
            Value code or None
        """
        ...

    @property
    def observation_date(self) -> date | datetime:
        """
        Date/time when observation was made.

        Returns:
            Observation date or datetime
        """
        ...

    @property
    def status(self) -> str:
        """
        Status: 'active', 'inactive', 'completed'.

        Returns:
            Observation status
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


class MentalStatusOrganizerProtocol(Protocol):
    """Mental status organizer data contract.

    Groups related mental status observations into categories.
    """

    @property
    def category(self) -> str:
        """
        Category name that groups observations (e.g., 'Cognition', 'Mood and Affect').

        Returns:
            Category name
        """
        ...

    @property
    def category_code(self) -> str:
        """
        Code for the category (ICF or LOINC preferred).

        Returns:
            Category code
        """
        ...

    @property
    def category_code_system(self) -> str:
        """
        Code system for category: 'ICF' or 'LOINC'.

        Returns:
            Code system name
        """
        ...

    @property
    def observations(self) -> list[MentalStatusObservationProtocol]:
        """
        List of mental status observations in this category.

        Returns:
            List of observations
        """
        ...

    @property
    def effective_time_low(self) -> Optional[date | datetime]:
        """
        Start of time span for observations (optional).

        Returns:
            Start date/datetime or None
        """
        ...

    @property
    def effective_time_high(self) -> Optional[date | datetime]:
        """
        End of time span for observations (optional).

        Returns:
            End date/datetime or None
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
