"""Protocol for chief complaint and reason for visit data.

This module defines the protocols (interfaces) for chief complaint objects.
Any object that implements these protocols can be passed to the chief complaint builders.
"""

from typing import Protocol


class ChiefComplaintProtocol(Protocol):
    """Protocol for chief complaint and reason for visit.

    Defines the interface for chief complaint objects that can be used with
    the ChiefComplaintAndReasonForVisitSection builder.

    This section records the patient's chief complaint (the patient's own description)
    and/or the reason for the patient's visit (the provider's description of the reason
    for visit). Local policy determines whether the information is divided into two
    sections or recorded in one section serving both purposes.

    Attributes:
        text: The chief complaint and/or reason for visit text. This is free-text
              describing why the patient is seeking care. Can be the patient's own
              words (chief complaint) or the provider's description (reason for visit).
              Examples: "Chest pain", "Annual physical examination",
              "Follow-up for hypertension"
    """

    text: str
