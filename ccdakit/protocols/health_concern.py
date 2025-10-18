"""Health Concern-related protocols for C-CDA documents."""

from datetime import date
from typing import Optional, Protocol, Sequence


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


class HealthConcernObservationProtocol(Protocol):
    """Protocol for observations/conditions within a health concern."""

    @property
    def observation_type(self) -> str:
        """
        Type of observation (problem, allergy, social_history, etc.).

        Returns:
            Observation type
        """
        ...

    @property
    def code(self) -> str:
        """
        Observation code (SNOMED, LOINC, etc.).

        Returns:
            Observation code
        """
        ...

    @property
    def code_system(self) -> str:
        """
        Code system identifier.

        Returns:
            Code system name or OID
        """
        ...

    @property
    def display_name(self) -> str:
        """
        Human-readable display name.

        Returns:
            Display name
        """
        ...


class HealthConcernProtocol(Protocol):
    """Health concern data contract."""

    @property
    def name(self) -> str:
        """
        Human-readable health concern name/description.

        Returns:
            Health concern name
        """
        ...

    @property
    def status(self) -> str:
        """
        Status: 'active', 'suspended', 'aborted', or 'completed'.

        When the underlying condition is of concern, statusCode is 'active'.
        Only when the underlying condition is no longer of concern is the
        statusCode set to 'completed'.

        Returns:
            Health concern status
        """
        ...

    @property
    def effective_time_low(self) -> Optional[date]:
        """
        Date when concern started (date condition became a concern).

        Returns:
            Start date or None
        """
        ...

    @property
    def effective_time_high(self) -> Optional[date]:
        """
        Date when concern ended (None if ongoing).

        Returns:
            End date or None
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

    @property
    def observations(self) -> Sequence[HealthConcernObservationProtocol]:
        """
        Related observations (problems, allergies, etc.).

        Returns:
            List of observations
        """
        ...

    @property
    def author_is_patient(self) -> bool:
        """
        Whether this is a patient concern (vs. provider concern).

        If True, this is a patient concern.
        If False, this is a provider concern.

        Returns:
            True if patient concern
        """
        ...
