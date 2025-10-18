"""Hospital Discharge Instructions protocol for C-CDA documents."""

from typing import Optional, Protocol


class DischargeInstructionProtocol(Protocol):
    """
    Data contract for hospital discharge instructions.

    Hospital discharge instructions provide guidance to the patient about
    activities, medications, diet, follow-up care, and other information
    relevant after leaving the hospital.
    """

    @property
    def instruction_text(self) -> str:
        """
        The discharge instruction text (narrative content).

        This is the main instruction text that will be displayed to the patient.
        Can be a simple paragraph or formatted text with sections.

        Returns:
            Discharge instruction text
        """
        ...

    @property
    def instruction_category(self) -> Optional[str]:
        """
        Optional category of the instruction.

        Examples: "Medications", "Activity", "Diet", "Follow-up", "Wound Care", etc.

        Returns:
            Category name or None
        """
        ...
