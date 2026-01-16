"""Example of creating an Instructions Section."""

from lxml import etree

from ccdakit.builders.sections.instructions import InstructionsSection
from ccdakit.core.base import CDAVersion


# Define instruction data classes
class PatientInstruction:
    """Example patient instruction that satisfies InstructionProtocol."""

    def __init__(
        self,
        instruction_id,
        text,
        code=None,
        code_system=None,
        display_name=None,
        status="completed",
    ):
        self._id = instruction_id
        self._text = text
        self._code = code
        self._code_system = code_system
        self._display_name = display_name
        self._status = status

    @property
    def id(self):
        """Unique identifier for the instruction."""
        return self._id

    @property
    def text(self):
        """The instruction text content."""
        return self._text

    @property
    def code(self):
        """Type of instruction code (optional)."""
        return self._code

    @property
    def code_system(self):
        """Code system for the instruction type code."""
        return self._code_system

    @property
    def display_name(self):
        """Human-readable display name for the instruction type."""
        return self._display_name

    @property
    def status(self):
        """Status of the instruction (must be 'completed' per spec)."""
        return self._status


def main():
    """Create and display an Instructions Section example."""

    # Create sample patient instructions
    instructions = [
        PatientInstruction(
            instruction_id="INSTR-001",
            text=(
                "Take one tablet by mouth every morning with food. "
                "Do not take on an empty stomach as this may cause nausea."
            ),
            code="171044003",
            code_system="SNOMED",
            display_name="Medication education",
            status="completed",
        ),
        PatientInstruction(
            instruction_id="INSTR-002",
            text=(
                "Monitor your blood pressure daily at home using the device provided. "
                "Record readings in the log book and bring it to your next appointment. "
                "Call the clinic if systolic pressure exceeds 160 or diastolic exceeds 100."
            ),
            code="311401005",
            code_system="SNOMED",
            display_name="Patient education",
            status="completed",
        ),
        PatientInstruction(
            instruction_id="INSTR-003",
            text=(
                "Follow up with your primary care physician within 2 weeks. "
                "Schedule an appointment with the front desk before leaving today. "
                "If you experience any concerning symptoms before your appointment, "
                "call the clinic immediately."
            ),
            code="409073007",
            code_system="SNOMED",
            display_name="Education",
            status="completed",
        ),
    ]

    # Create the Instructions Section (R2.1)
    section = InstructionsSection(
        instructions=instructions,
        title="Patient Care Instructions",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(
        elem,
        pretty_print=True,
        encoding="unicode",
        xml_declaration=False,
    )

    print("Instructions Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show summary information
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.45")
    print("  - Extension: 2014-06-09")
    print("  - Number of instructions: 3")
    print("  - Section Code: 69730-0 (Instructions - LOINC)")
    print("\nInstruction Details:")
    for idx, instruction in enumerate(instructions, start=1):
        print(f"  {idx}. {instruction.display_name}")
        print(f"     Code: {instruction.code} ({instruction.code_system})")
        print(f"     Text: {instruction.text[:60]}...")
    print("\nConformance:")
    print("  - CONF:1098-10112: Template ID present")
    print("  - CONF:1098-31384: Template extension present")
    print("  - CONF:1098-15375: Code 69730-0 (Instructions)")
    print("  - CONF:1098-10114: Title present")
    print("  - CONF:1098-10115: Narrative text present")
    print("  - CONF:1098-10116: Entry elements with Instruction (V2) present")
    print("\nCommon Use Cases:")
    print("  - Patient education materials")
    print("  - Medication instructions")
    print("  - Post-procedure care instructions")
    print("  - Discharge instructions")
    print("  - Decision aids")
    print("  - Vaccine Information Statements (VIS)")


if __name__ == "__main__":
    main()
