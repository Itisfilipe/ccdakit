"""Allergy-related protocols for C-CDA documents."""

from datetime import date
from typing import Optional, Protocol


class AllergyProtocol(Protocol):
    """Allergy/Intolerance data contract."""

    @property
    def allergen(self) -> str:
        """
        Human-readable allergen name.

        Returns:
            Allergen name (e.g., "Penicillin", "Peanuts", "Latex")
        """
        ...

    @property
    def allergen_code(self) -> Optional[str]:
        """
        Code for the allergen (RxNorm, UNII, or SNOMED CT).

        Returns:
            Allergen code or None
        """
        ...

    @property
    def allergen_code_system(self) -> Optional[str]:
        """
        Code system for allergen code (e.g., "RxNorm", "UNII", "SNOMED CT").

        Returns:
            Code system name or None
        """
        ...

    @property
    def allergy_type(self) -> str:
        """
        Type of allergy: 'allergy' or 'intolerance'.

        Returns:
            Allergy type
        """
        ...

    @property
    def reaction(self) -> Optional[str]:
        """
        Reaction/manifestation (e.g., "Hives", "Anaphylaxis", "Nausea").

        Returns:
            Reaction description or None
        """
        ...

    @property
    def severity(self) -> Optional[str]:
        """
        Severity: 'mild', 'moderate', 'severe', or 'fatal'.

        Returns:
            Severity level or None
        """
        ...

    @property
    def status(self) -> str:
        """
        Allergy status: 'active' or 'resolved'.

        Returns:
            Allergy status
        """
        ...

    @property
    def onset_date(self) -> Optional[date]:
        """
        Date when allergy was first identified (optional).

        Returns:
            Onset date or None
        """
        ...
