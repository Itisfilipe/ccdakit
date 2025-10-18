"""Protocol for functional status data.

This module defines the protocols (interfaces) for functional status objects.
Any object that implements these protocols can be passed to the functional status builders.
"""

from datetime import date, datetime
from typing import Optional, Protocol, Sequence


class FunctionalStatusObservationProtocol(Protocol):
    """Protocol for a single functional status observation.

    Defines the interface that functional status observation objects must implement
    to be used with the FunctionalStatusObservation builder.

    Attributes:
        type: Type/description of functional status (e.g., "Ambulation", "Bathing", "Feeding")
        code: Code for the functional status (SNOMED CT recommended)
        code_system: Code system OID (default: SNOMED CT)
        value: Coded value representing the functional status
        value_code: Code for the value (SNOMED CT recommended)
        value_code_system: Code system OID for value
        date: Date and time the observation was made
        interpretation: Optional interpretation of the status
    """

    type: str
    code: str
    code_system: Optional[str]
    value: str
    value_code: str
    value_code_system: Optional[str]
    date: date | datetime
    interpretation: Optional[str]


class FunctionalStatusOrganizerProtocol(Protocol):
    """Protocol for a group of related functional status observations.

    Defines the interface for a functional status organizer that groups
    related observations by category (e.g., mobility, self-care, communication).

    Attributes:
        category: Category of functional status (e.g., "Mobility", "Self-Care")
        category_code: Code for the category (ICF or LOINC recommended)
        category_code_system: Code system OID for category
        observations: List of functional status observations in this category
    """

    category: str
    category_code: str
    category_code_system: Optional[str]
    observations: Sequence[FunctionalStatusObservationProtocol]
