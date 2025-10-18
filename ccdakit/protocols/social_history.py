"""Protocol for social history data.

This module defines the protocols (interfaces) for social history objects.
Any object that implements these protocols can be passed to the social history builders.
"""

from datetime import date, datetime
from typing import Protocol


class SmokingStatusProtocol(Protocol):
    """Protocol for smoking status observation.

    Defines the interface for smoking status objects that can be used with
    the SmokingStatusObservation builder.

    This represents a "snapshot in time" observation of the patient's current
    smoking status as specified in Meaningful Use Stage 2 requirements.

    Attributes:
        smoking_status: Description of smoking status (e.g., "Current every day smoker",
                       "Former smoker", "Never smoker", "Unknown if ever smoked")
        code: SNOMED CT code from Smoking Status Value Set (2.16.840.1.113883.11.20.9.38)
              Common codes:
              - 449868002: Current every day smoker
              - 428041000124106: Current some day smoker
              - 8517006: Former smoker
              - 266919005: Never smoker
              - 266927001: Unknown if ever smoked
        date: Date and time when smoking status was observed (point in time, not interval)
    """

    smoking_status: str
    code: str
    date: date | datetime
