"""Intervention-related protocols for C-CDA documents."""

from datetime import date, datetime
from typing import Optional, Protocol, Sequence, Union


class InterventionProtocol(Protocol):
    """
    Data contract for Intervention Act (V2) - template 2.16.840.1.113883.10.20.22.4.131.

    Represents an intervention that has occurred (moodCode=EVN).
    Interventions are actions taken to maximize the prospects of achieving goals of care,
    including removal of barriers to success.
    """

    @property
    def id(self) -> str:
        """
        Unique identifier for the intervention.

        Returns:
            Intervention ID
        """
        ...

    @property
    def description(self) -> str:
        """
        Human-readable intervention description.

        Returns:
            Intervention description text
        """
        ...

    @property
    def effective_time(self) -> Optional[Union[date, datetime]]:
        """
        Time when intervention occurred.

        Returns:
            Effective time or None
        """
        ...

    @property
    def status(self) -> str:
        """
        Intervention status. For Intervention Act (EVN mood), must be 'completed'.

        Returns:
            Status code (default: 'completed')
        """
        ...

    @property
    def intervention_type(self) -> Optional[str]:
        """
        Type of intervention (e.g., 'procedure', 'medication', 'instruction', 'encounter').

        Returns:
            Intervention type or None
        """
        ...

    @property
    def goal_reference_id(self) -> Optional[str]:
        """
        Reference to Goal Observation ID that this intervention supports.

        Returns:
            Goal observation ID or None
        """
        ...

    @property
    def author(self) -> Optional[str]:
        """
        Author of the intervention.

        Returns:
            Author identifier or None
        """
        ...


class PlannedInterventionProtocol(Protocol):
    """
    Data contract for Planned Intervention Act (V2) - template 2.16.840.1.113883.10.20.22.4.146.

    Represents a planned intervention (moodCode=INT, ARQ, PRMS, PRP, or RQO).
    All referenced interventions must have prospective mood codes.
    """

    @property
    def id(self) -> str:
        """
        Unique identifier for the planned intervention.

        Returns:
            Planned intervention ID
        """
        ...

    @property
    def description(self) -> str:
        """
        Human-readable planned intervention description.

        Returns:
            Planned intervention description text
        """
        ...

    @property
    def mood_code(self) -> str:
        """
        Mood code for planned intervention.
        Must be from Planned Intervention moodCode value set (INT, ARQ, PRMS, PRP, or RQO).

        Returns:
            Mood code (default: 'INT')
        """
        ...

    @property
    def effective_time(self) -> Optional[Union[date, datetime]]:
        """
        Planned time for intervention.

        Returns:
            Effective time or None
        """
        ...

    @property
    def status(self) -> str:
        """
        Intervention status. For Planned Intervention Act, must be 'active'.

        Returns:
            Status code (default: 'active')
        """
        ...

    @property
    def intervention_type(self) -> Optional[str]:
        """
        Type of planned intervention (e.g., 'procedure', 'medication', 'instruction', 'encounter').

        Returns:
            Intervention type or None
        """
        ...

    @property
    def goal_reference_id(self) -> str:
        """
        Reference to Goal Observation ID that this planned intervention supports.
        Required for planned interventions (CONF:1198-32673).

        Returns:
            Goal observation ID
        """
        ...

    @property
    def author(self) -> Optional[str]:
        """
        Author of the planned intervention.

        Returns:
            Author identifier or None
        """
        ...


class InterventionActivityProtocol(Protocol):
    """
    Base protocol for specific intervention activities (medications, procedures, etc.)
    that can be referenced within an Intervention Act.
    """

    @property
    def id(self) -> str:
        """
        Unique identifier for the intervention activity.

        Returns:
            Activity ID
        """
        ...

    @property
    def description(self) -> str:
        """
        Human-readable activity description.

        Returns:
            Activity description text
        """
        ...

    @property
    def code(self) -> Optional[str]:
        """
        Activity code.

        Returns:
            Activity code or None
        """
        ...

    @property
    def code_system(self) -> Optional[str]:
        """
        Code system for activity code.

        Returns:
            Code system name or OID or None
        """
        ...

    @property
    def display_name(self) -> Optional[str]:
        """
        Display name for activity code.

        Returns:
            Display name or None
        """
        ...
