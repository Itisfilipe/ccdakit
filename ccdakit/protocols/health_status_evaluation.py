"""Health status evaluation and outcome protocols for C-CDA documents."""

from datetime import date, datetime
from typing import Optional, Protocol, Sequence


class ProgressTowardGoalProtocol(Protocol):
    """Progress toward goal observation data contract."""

    @property
    def id(self) -> str:
        """
        Unique identifier for this progress observation.

        Returns:
            Progress observation ID
        """
        ...

    @property
    def achievement_code(self) -> str:
        """
        Goal achievement status code from Goal Achievement value set.

        Valid codes include:
        - "ASSERTION" (general assertion)
        - Goal achievement codes from SNOMED CT (e.g., "385641008" for Improving)

        Returns:
            Achievement status code
        """
        ...

    @property
    def achievement_code_system(self) -> Optional[str]:
        """
        Code system for achievement code.

        Returns:
            Code system (typically "2.16.840.1.113883.6.96" for SNOMED CT)
        """
        ...

    @property
    def achievement_display_name(self) -> Optional[str]:
        """
        Display name for achievement code.

        Returns:
            Display name or None
        """
        ...


class OutcomeObservationProtocol(Protocol):
    """Outcome observation data contract for C-CDA Health Status Evaluations."""

    @property
    def id(self) -> str:
        """
        Unique identifier for this outcome observation.

        Returns:
            Outcome observation ID
        """
        ...

    @property
    def code(self) -> str:
        """
        Observation code (typically from LOINC).

        Examples:
        - "29463-7" (Body weight)
        - "8867-4" (Heart rate)
        - "2339-0" (Glucose [Mass/volume] in Blood)

        Returns:
            Observation code
        """
        ...

    @property
    def code_system(self) -> Optional[str]:
        """
        Code system: typically 'LOINC' or 'SNOMED'.

        Returns:
            Code system name or OID
        """
        ...

    @property
    def display_name(self) -> Optional[str]:
        """
        Display name for the observation code.

        Returns:
            Display name or None
        """
        ...

    @property
    def value(self) -> Optional[str]:
        """
        Observation value (e.g., measurement result).

        Returns:
            Observation value or None
        """
        ...

    @property
    def value_unit(self) -> Optional[str]:
        """
        Unit of measure for observation value.

        Returns:
            Unit (e.g., "kg", "mmHg", "mg/dL") or None
        """
        ...

    @property
    def effective_time(self) -> Optional[date]:
        """
        Date/time when the observation was made.

        Returns:
            Observation date or None
        """
        ...

    @property
    def progress_toward_goal(self) -> Optional[ProgressTowardGoalProtocol]:
        """
        Progress toward goal observation.

        Indicates how well the patient is progressing toward a goal.

        Returns:
            Progress observation or None
        """
        ...

    @property
    def goal_reference_id(self) -> Optional[str]:
        """
        Reference ID to a Goal Observation that this outcome evaluates.

        Uses Entry Reference template to link to goal.

        Returns:
            Goal observation ID or None
        """
        ...

    @property
    def intervention_reference_ids(self) -> Optional[Sequence[str]]:
        """
        Reference IDs to Intervention Acts that led to this outcome.

        Uses Entry Reference template to link to interventions.

        Returns:
            List of intervention IDs or None
        """
        ...

    @property
    def author_name(self) -> Optional[str]:
        """
        Name of the author who documented this observation.

        Returns:
            Author name or None
        """
        ...

    @property
    def author_time(self) -> Optional[datetime]:
        """
        Date/time when this observation was authored.

        Returns:
            Author time or None
        """
        ...
