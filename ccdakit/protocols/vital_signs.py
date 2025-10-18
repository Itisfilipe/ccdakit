"""Protocol for vital signs data.

This module defines the protocols (interfaces) for vital signs objects.
Any object that implements these protocols can be passed to the vital signs builders.
"""

from datetime import date, datetime
from typing import Optional, Protocol, Sequence


class VitalSignProtocol(Protocol):
    """Protocol for a single vital sign observation.

    Defines the interface that vital sign observation objects must implement to be
    used with the VitalSignObservation builder.

    Attributes:
        type: Type of vital sign (e.g., "Blood Pressure", "Heart Rate", "Temperature")
        code: LOINC code for the vital sign
        value: Measured value
        unit: Unit of measurement (e.g., "mm[Hg]", "bpm", "Cel")
        date: Date and time the observation was taken
        interpretation: Optional interpretation (e.g., "Normal", "High", "Low")
    """

    type: str
    code: str
    value: str
    unit: str
    date: date | datetime
    interpretation: Optional[str]


class VitalSignsOrganizerProtocol(Protocol):
    """Protocol for a group of vital sign observations taken at the same time.

    Defines the interface for a vital signs organizer that groups related observations.

    Attributes:
        date: Date and time when the vital signs were taken
        vital_signs: List of vital sign observations
    """

    date: date | datetime
    vital_signs: Sequence[VitalSignProtocol]
