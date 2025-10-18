"""Goal-related protocols for C-CDA documents."""

from datetime import date
from typing import Optional, Protocol


class GoalProtocol(Protocol):
    """Goal data contract for C-CDA Goals Section."""

    @property
    def description(self) -> str:
        """
        Human-readable goal description.

        Returns:
            Goal description text
        """
        ...

    @property
    def code(self) -> Optional[str]:
        """
        Goal code (typically from LOINC).

        Returns:
            Goal code or None
        """
        ...

    @property
    def code_system(self) -> Optional[str]:
        """
        Code system: typically 'LOINC' or 'SNOMED'.

        Returns:
            Code system name or None
        """
        ...

    @property
    def display_name(self) -> Optional[str]:
        """
        Display name for the goal code.

        Returns:
            Display name or None
        """
        ...

    @property
    def status(self) -> str:
        """
        Goal status: 'active', 'cancelled', 'completed', 'on-hold'.

        Returns:
            Goal status from ActStatus value set
        """
        ...

    @property
    def target_date(self) -> Optional[date]:
        """
        Target date for goal achievement.

        Returns:
            Target date or None
        """
        ...

    @property
    def start_date(self) -> Optional[date]:
        """
        Date goal was established.

        Returns:
            Start date or None
        """
        ...

    @property
    def value(self) -> Optional[str]:
        """
        Goal value/observation value (e.g., target weight, blood pressure).

        Returns:
            Goal value or None
        """
        ...

    @property
    def value_unit(self) -> Optional[str]:
        """
        Unit of measure for goal value.

        Returns:
            Unit or None
        """
        ...

    @property
    def author(self) -> Optional[str]:
        """
        Author of the goal (patient, provider, or negotiated).

        Returns:
            Author identifier or None
        """
        ...

    @property
    def priority(self) -> Optional[str]:
        """
        Priority of the goal (low, medium, high).

        Returns:
            Priority or None
        """
        ...
