"""Instruction protocol for C-CDA documents."""

from typing import Optional, Protocol


class InstructionProtocol(Protocol):
    """
    Data contract for Instruction (V2) - template 2.16.840.1.113883.10.20.22.4.20.

    The Instruction template represents patient instructions. It can be used in several ways,
    such as to record patient instructions within a Medication Activity or to record fill
    instructions within a supply order. Instructions are prospective (moodCode=INT).

    If an instruction was already given, the Procedure Activity Act template should be used
    instead to represent the completed instruction.

    Template Information:
        - Template ID: 2.16.840.1.113883.10.20.22.4.20
        - Template Version: 2014-06-09
        - Release: C-CDA R2.1
        - Class Code: ACT (fixed)
        - Mood Code: INT (fixed - Intent)
        - Status Code: completed (fixed)

    Common Uses:
        - Patient education materials
        - Medication instructions
        - Supply fill instructions
        - Vaccine Information Statements (VIS)
        - Decision aids

    See Also:
        - Instructions Section (V2): 2.16.840.1.113883.10.20.22.2.45
        - Procedure Activity Act: For completed instructions
    """

    @property
    def id(self) -> str:
        """
        Unique identifier for the instruction.

        This ID can be referenced by other elements in the document.

        Returns:
            Instruction ID (UUID or other unique identifier)
        """
        ...

    @property
    def code(self) -> Optional[str]:
        """
        Type of instruction code.

        SHOULD be selected from ValueSet Patient Education (2.16.840.1.113883.11.20.9.34).
        Common codes include SNOMED CT codes for various patient education topics.

        Examples:
            - "409073007" - Education (SNOMED)
            - "311401005" - Patient education
            - "710837008" - Medication education

        Returns:
            Instruction type code or None
        """
        ...

    @property
    def code_system(self) -> Optional[str]:
        """
        Code system for the instruction type code.

        Common systems:
            - "2.16.840.1.113883.6.96" (SNOMED CT)
            - "SNOMED" (alias)

        Returns:
            Code system OID or name, or None if code not provided
        """
        ...

    @property
    def display_name(self) -> Optional[str]:
        """
        Human-readable display name for the instruction type code.

        Returns:
            Display name for the code, or None
        """
        ...

    @property
    def text(self) -> str:
        """
        The instruction text content.

        This is the main narrative content of the instruction that will be
        displayed to or given to the patient. It should be clear, actionable,
        and patient-friendly.

        Examples:
            - "Take one tablet by mouth daily with food"
            - "Review the medication guide provided with your prescription"
            - "Follow up with your primary care physician in 2 weeks"

        Returns:
            Instruction text content
        """
        ...

    @property
    def status(self) -> str:
        """
        Status of the instruction.

        For Instruction (V2) template, this SHALL be 'completed'.
        This indicates the instruction has been created/documented,
        not necessarily that the patient has followed it.

        Returns:
            Status code (must be 'completed' per template requirements)
        """
        ...
