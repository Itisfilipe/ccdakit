"""Protocol for physical exam data.

This module defines the protocols (interfaces) for physical exam objects.
Any object that implements these protocols can be passed to the physical exam builders.
"""

from datetime import date, datetime
from typing import Optional, Protocol, Sequence


class WoundObservationProtocol(Protocol):
    """Protocol for a wound observation entry.

    Defines the interface that wound observation objects must implement to be
    used with the LongitudinalCareWoundObservation builder.

    Attributes:
        wound_type: Type of wound (e.g., "Pressure ulcer", "Surgical wound")
        wound_code: SNOMED CT code for the wound type
        date: Date and time the observation was made
        location: Body site where the wound is located
        location_code: SNOMED CT code for the body location
        laterality: Optional laterality (e.g., "Left", "Right")
        laterality_code: Optional SNOMED CT code for laterality
    """

    wound_type: str
    wound_code: str
    date: date | datetime
    location: Optional[str]
    location_code: Optional[str]
    laterality: Optional[str]
    laterality_code: Optional[str]


class PhysicalExamSectionProtocol(Protocol):
    """Protocol for physical exam section data.

    Defines the interface for physical exam section that contains wound observations.

    Attributes:
        wound_observations: List of wound observations
    """

    wound_observations: Sequence[WoundObservationProtocol]
