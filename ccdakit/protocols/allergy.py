"""Allergy-related protocols for C-CDA documents.

This protocol defines the interface for allergy data following C-CDA R2.1 specifications.
"""

from datetime import date
from typing import Optional, Protocol, Union


class AllergyProtocol(Protocol):
    """
    Allergy/Intolerance data contract per C-CDA R2.1 specification.

    This protocol supports all fields required and recommended by the
    Allergy - Intolerance Observation template (2.16.840.1.113883.10.20.22.4.7:2014-06-09).
    """

    @property
    def allergen(self) -> str:
        """
        Human-readable allergen name (required).

        Returns:
            Allergen name (e.g., "Penicillin", "Peanuts", "Latex")
        """
        ...

    @property
    def allergen_code(self) -> Optional[str]:
        """
        Code for the allergen from appropriate value set (recommended).

        Should be from ValueSet Substance Reactant for Intolerance
        (2.16.840.1.113762.1.4.1010.1) which includes RxNorm, UNII, and SNOMED CT.

        Returns:
            Allergen code or None
        """
        ...

    @property
    def allergen_code_system(self) -> Optional[str]:
        """
        Code system for allergen code (required if allergen_code provided).

        Returns:
            Code system name (e.g., "RxNorm", "UNII", "SNOMED CT") or None
        """
        ...

    @property
    def allergy_type(self) -> str:
        """
        Type of allergy or intolerance (required).

        Should be from ValueSet Allergy and Intolerance Type
        (2.16.840.1.113883.3.88.12.3221.6.2).

        Returns:
            Allergy type (e.g., 'allergy', 'intolerance')
        """
        ...

    @property
    def reaction(self) -> Optional[str]:
        """
        Reaction/manifestation (recommended - SHOULD be included).

        Describes the manifestation of the allergy (e.g., "Hives", "Anaphylaxis", "Nausea").
        Maps to Reaction Observation template (2.16.840.1.113883.10.20.22.4.9:2014-06-09).

        Returns:
            Reaction description or None
        """
        ...

    @property
    def severity(self) -> Optional[str]:
        """
        Severity level (optional, DEPRECATED for allergies).

        NOTE: Severity Observation is DEPRECATED for Allergy Observations per C-CDA R2.1.
        Use criticality instead to characterize allergy risk.

        If provided, can be used to infer criticality when explicit criticality not available.

        Returns:
            Severity level ('mild', 'moderate', 'severe', 'fatal') or None
        """
        ...

    @property
    def status(self) -> str:
        """
        Allergy concern status (required).

        This is used by the containing Allergy Concern Act to track whether the
        provider still has concern about this allergy.

        Returns:
            Status ('active', 'completed')
        """
        ...

    @property
    def onset_date(self) -> Optional[date]:
        """
        Date when allergy was first identified (required).

        Maps to effectiveTime/low of the Allergy Observation.
        If unknown, will be represented with nullFlavor="UNK".

        Returns:
            Onset date or None
        """
        ...

    # NEW FIELDS for C-CDA R2.1 compliance

    @property
    def resolution_date(self) -> Optional[Union[date, str]]:
        """
        Date when allergy was resolved (optional).

        Maps to effectiveTime/high of the Allergy Observation.
        - If date is known, provide a date object
        - If allergy is resolved but date unknown, provide string "UNK"
        - If allergy is not resolved, return None

        Returns:
            Resolution date, "UNK", or None
        """
        return None  # Optional field with default

    @property
    def clinical_status(self) -> Optional[str]:
        """
        Clinical status of the allergy (optional but recommended).

        Maps to Allergy Status Observation (2.16.840.1.113883.10.20.22.4.28:2019-06-20).
        This is DISTINCT from the concern status - it represents the clinical state.

        Should be from ValueSet Allergy Clinical Status (2.16.840.1.113762.1.4.1099.29).

        Returns:
            Clinical status ('active', 'inactive', 'resolved') or None
        """
        return None  # Optional field with default

    @property
    def criticality(self) -> Optional[str]:
        """
        Criticality assessment (recommended - SHOULD be included).

        Maps to Criticality Observation (2.16.840.1.113883.10.20.22.4.145).
        Indicates potential for life-threatening or organ system threatening reaction.

        Should be from ValueSet Criticality Observation (2.16.840.1.113883.1.11.20549).

        Returns:
            Criticality ('low', 'high', 'unable-to-assess') or None
        """
        return None  # Optional field with default

    @property
    def negation_ind(self) -> Optional[bool]:
        """
        Negation indicator (optional).

        Set to True to indicate that the allergy was NOT observed.
        Used in quality reporting scenarios.

        Returns:
            True if negated, False if affirmed, None if not specified
        """
        return None  # Optional field with default
