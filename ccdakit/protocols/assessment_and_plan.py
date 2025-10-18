"""Assessment and Plan-related protocols for C-CDA documents."""

from datetime import datetime
from typing import Optional, Protocol


class PlannedActProtocol(Protocol):
    """Planned Act data contract.

    Represents planned activities that are not classified as observations or procedures.
    Examples include dressing changes, patient teaching, feeding, or providing comfort measures.
    """

    @property
    def id_root(self) -> str:
        """
        OID for the ID root (assigning authority).

        Returns:
            ID root OID
        """
        ...

    @property
    def id_extension(self) -> str:
        """
        Unique identifier within the root's namespace.

        Returns:
            ID extension
        """
        ...

    @property
    def code(self) -> str:
        """
        LOINC or SNOMED CT code for the planned activity.

        Returns:
            Activity code
        """
        ...

    @property
    def code_system(self) -> str:
        """
        Code system: 'LOINC' or 'SNOMED'.

        Returns:
            Code system name
        """
        ...

    @property
    def display_name(self) -> str:
        """
        Human-readable description of the planned activity.

        Returns:
            Display name
        """
        ...

    @property
    def mood_code(self) -> str:
        """
        Mood code indicating the nature of the planned act.
        Valid values: 'INT' (intent), 'RQO' (request), 'PRMS' (promise), 'PRP' (proposal).

        Returns:
            Mood code
        """
        ...

    @property
    def effective_time(self) -> Optional[datetime]:
        """
        When the activity is intended to take place.

        Returns:
            Planned time or None
        """
        ...

    @property
    def instructions(self) -> Optional[str]:
        """
        Patient or provider instructions for the planned activity.

        Returns:
            Instructions text or None
        """
        ...


class AssessmentAndPlanItemProtocol(Protocol):
    """Assessment and Plan item data contract.

    Represents a single assessment finding or plan item.
    """

    @property
    def text(self) -> str:
        """
        Assessment or plan narrative text.

        Returns:
            Text description
        """
        ...

    @property
    def item_type(self) -> str:
        """
        Type of item: 'assessment' or 'plan'.

        Returns:
            Item type
        """
        ...

    @property
    def planned_act(self) -> Optional[PlannedActProtocol]:
        """
        Associated planned act for plan items.

        Returns:
            PlannedActProtocol or None
        """
        ...
