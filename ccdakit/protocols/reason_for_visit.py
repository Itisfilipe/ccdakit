"""Reason for Visit protocol for C-CDA documents.

This module defines the protocol for Reason for Visit Section data.
The section records the patient's reason for the visit as documented by the provider.
"""

from typing import Protocol


class ReasonForVisitProtocol(Protocol):
    """
    Data contract for Reason for Visit Section.

    The Reason for Visit Section records the patient's reason for the patient's
    visit as documented by the provider. Local policy determines whether Reason
    for Visit and Chief Complaint are in separate or combined sections.

    This is typically a simple text-based section without structured entries.
    """

    @property
    def reason_text(self) -> str:
        """
        The reason for visit text (narrative content).

        This is the provider's documentation of why the patient is seeking care.
        Examples: "Follow-up visit for hypertension", "Annual physical exam",
        "Evaluation of chest pain"

        Returns:
            Reason for visit text
        """
        ...


__all__ = ["ReasonForVisitProtocol"]
