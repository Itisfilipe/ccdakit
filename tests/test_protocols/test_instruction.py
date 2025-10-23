"""Tests for instruction protocols."""

from typing import Optional

from ccdakit.protocols.instruction import InstructionProtocol


class MockInstruction:
    """Test implementation of InstructionProtocol."""

    def __init__(
        self,
        instruction_id: str = "12345",
        text: str = "Take one tablet by mouth daily with food",
        code: Optional[str] = "409073007",
        code_system: Optional[str] = "2.16.840.1.113883.6.96",
        display_name: Optional[str] = "Education",
        status: str = "completed",
    ):
        self._id = instruction_id
        self._text = text
        self._code = code
        self._code_system = code_system
        self._display_name = display_name
        self._status = status

    @property
    def id(self) -> str:
        return self._id

    @property
    def code(self) -> Optional[str]:
        return self._code

    @property
    def code_system(self) -> Optional[str]:
        return self._code_system

    @property
    def display_name(self) -> Optional[str]:
        return self._display_name

    @property
    def text(self) -> str:
        return self._text

    @property
    def status(self) -> str:
        return self._status


def test_instruction_protocol_required_fields():
    """Test InstructionProtocol required fields."""
    instruction = MockInstruction()

    assert instruction.id == "12345"
    assert instruction.text == "Take one tablet by mouth daily with food"
    assert instruction.status == "completed"


def test_instruction_protocol_optional_fields():
    """Test InstructionProtocol optional fields."""
    instruction = MockInstruction()

    assert instruction.code == "409073007"
    assert instruction.code_system == "2.16.840.1.113883.6.96"
    assert instruction.display_name == "Education"


def test_instruction_protocol_satisfaction():
    """Test that MockInstruction satisfies InstructionProtocol."""
    instruction = MockInstruction()

    def accepts_instruction(inst: InstructionProtocol) -> str:
        return f"{inst.id}: {inst.text}"

    result = accepts_instruction(instruction)
    assert result == "12345: Take one tablet by mouth daily with food"


def test_instruction_with_medication_text():
    """Test instruction with medication-related text."""
    instruction = MockInstruction(
        instruction_id="med-inst-001",
        text="Take one tablet by mouth twice daily with meals. Complete the full course even if symptoms improve.",
        code="710837008",
        display_name="Medication education",
    )

    assert instruction.id == "med-inst-001"
    assert "twice daily" in instruction.text
    assert instruction.code == "710837008"
    assert instruction.display_name == "Medication education"
    assert instruction.status == "completed"


def test_instruction_with_education_text():
    """Test instruction with patient education text."""
    instruction = MockInstruction(
        instruction_id="edu-001",
        text="Review the medication guide provided with your prescription. Contact your doctor if you experience unusual side effects.",
        code="311401005",
        display_name="Patient education",
    )

    assert instruction.id == "edu-001"
    assert "medication guide" in instruction.text
    assert instruction.code == "311401005"
    assert instruction.display_name == "Patient education"


def test_instruction_with_follow_up_text():
    """Test instruction with follow-up care text."""
    instruction = MockInstruction(
        instruction_id="followup-001",
        text="Follow up with your primary care physician in 2 weeks to review lab results and adjust treatment as needed.",
        code="409073007",
        display_name="Education",
    )

    assert instruction.id == "followup-001"
    assert "2 weeks" in instruction.text
    assert "primary care physician" in instruction.text


def test_instruction_without_code():
    """Test instruction without a code."""
    instruction = MockInstruction(
        instruction_id="no-code-001",
        text="Monitor your blood pressure daily and record the results.",
        code=None,
        code_system=None,
        display_name=None,
    )

    assert instruction.id == "no-code-001"
    assert instruction.text == "Monitor your blood pressure daily and record the results."
    assert instruction.code is None
    assert instruction.code_system is None
    assert instruction.display_name is None
    assert instruction.status == "completed"


def test_instruction_with_snomed_code():
    """Test instruction with SNOMED CT code."""
    instruction = MockInstruction(
        instruction_id="snomed-001",
        text="Perform range of motion exercises as demonstrated by physical therapy.",
        code="409073007",
        code_system="2.16.840.1.113883.6.96",
        display_name="Education",
    )

    assert instruction.code == "409073007"
    assert instruction.code_system == "2.16.840.1.113883.6.96"
    assert instruction.status == "completed"


def test_instruction_with_diet_text():
    """Test instruction with diet-related text."""
    instruction = MockInstruction(
        instruction_id="diet-001",
        text="Follow a low-sodium diet, limiting salt intake to less than 2 grams per day.",
        code="311401005",
        display_name="Patient education",
    )

    assert "low-sodium" in instruction.text
    assert "2 grams" in instruction.text


def test_instruction_with_activity_text():
    """Test instruction with activity-related text."""
    instruction = MockInstruction(
        instruction_id="activity-001",
        text="Avoid heavy lifting or strenuous activity for 6 weeks. You may resume light walking as tolerated.",
        code="409073007",
        display_name="Education",
    )

    assert "6 weeks" in instruction.text
    assert "avoid heavy lifting" in instruction.text.lower()


def test_instruction_status_completed():
    """Test that instruction status is 'completed' as per template requirements."""
    instruction = MockInstruction()

    # Per template requirements, status SHALL be 'completed'
    assert instruction.status == "completed"


def test_multiple_instructions():
    """Test creating multiple different instructions."""
    instructions = [
        MockInstruction(
            instruction_id="inst-1",
            text="Take medication with food",
            code="710837008",
            display_name="Medication education",
        ),
        MockInstruction(
            instruction_id="inst-2",
            text="Follow up in 1 week",
            code="409073007",
            display_name="Education",
        ),
        MockInstruction(
            instruction_id="inst-3",
            text="Monitor blood glucose levels",
            code="311401005",
            display_name="Patient education",
        ),
    ]

    assert len(instructions) == 3
    assert instructions[0].id == "inst-1"
    assert instructions[1].id == "inst-2"
    assert instructions[2].id == "inst-3"


class MinimalInstruction:
    """Minimal implementation with only required fields."""

    @property
    def id(self) -> str:
        return "minimal-001"

    @property
    def code(self) -> Optional[str]:
        return None

    @property
    def code_system(self) -> Optional[str]:
        return None

    @property
    def display_name(self) -> Optional[str]:
        return None

    @property
    def text(self) -> str:
        return "Call the office if you have any questions."

    @property
    def status(self) -> str:
        return "completed"


def test_minimal_instruction_protocol():
    """Test that minimal implementation satisfies InstructionProtocol."""
    instruction = MinimalInstruction()

    assert instruction.id == "minimal-001"
    assert instruction.text == "Call the office if you have any questions."
    assert instruction.code is None
    assert instruction.code_system is None
    assert instruction.display_name is None
    assert instruction.status == "completed"


def test_minimal_instruction_satisfaction():
    """Test that MinimalInstruction satisfies InstructionProtocol."""
    instruction = MinimalInstruction()

    def accepts_instruction(inst: InstructionProtocol) -> str:
        return inst.text

    result = accepts_instruction(instruction)
    assert result == "Call the office if you have any questions."


def test_instruction_code_without_code_system():
    """Test instruction with code but no code system."""
    instruction = MockInstruction(
        code="409073007",
        code_system=None,
        display_name="Education",
    )

    assert instruction.code == "409073007"
    assert instruction.code_system is None
    assert instruction.display_name == "Education"


def test_instruction_code_system_without_code():
    """Test instruction with code system but no code."""
    instruction = MockInstruction(
        code=None,
        code_system="2.16.840.1.113883.6.96",
        display_name=None,
    )

    assert instruction.code is None
    assert instruction.code_system == "2.16.840.1.113883.6.96"


def test_instruction_display_name_only():
    """Test instruction with display name but no code."""
    instruction = MockInstruction(
        code=None,
        code_system=None,
        display_name="Patient Education",
    )

    assert instruction.code is None
    assert instruction.code_system is None
    assert instruction.display_name == "Patient Education"


def test_instruction_empty_text():
    """Test instruction with empty text (edge case)."""
    instruction = MockInstruction(
        instruction_id="empty-text",
        text="",
    )

    assert instruction.id == "empty-text"
    assert instruction.text == ""
    assert instruction.status == "completed"


def test_instruction_long_text():
    """Test instruction with very long text."""
    long_text = "Take this medication exactly as prescribed. " * 50
    instruction = MockInstruction(
        instruction_id="long-inst",
        text=long_text,
    )

    assert instruction.id == "long-inst"
    assert len(instruction.text) > 1000
    assert instruction.text.startswith("Take this medication")


def test_instruction_special_characters_in_text():
    """Test instruction with special characters in text."""
    instruction = MockInstruction(
        instruction_id="special-chars",
        text="Take 1/2 tablet @ 8:00 AM & 8:00 PM (12-hour interval) - max 2 tabs/day!",
    )

    assert instruction.id == "special-chars"
    assert "@" in instruction.text
    assert "&" in instruction.text
    assert "/" in instruction.text


def test_instruction_multiline_text():
    """Test instruction with multiline text."""
    instruction = MockInstruction(
        instruction_id="multiline",
        text="Step 1: Wash hands thoroughly\nStep 2: Open package\nStep 3: Apply as directed",
    )

    assert instruction.id == "multiline"
    assert "\n" in instruction.text
    assert "Step 1" in instruction.text
    assert "Step 3" in instruction.text


def test_instruction_unicode_characters():
    """Test instruction with unicode characters."""
    instruction = MockInstruction(
        instruction_id="unicode",
        text="Tomar una tableta por vía oral cada día con comida",
        display_name="Educación",
    )

    assert instruction.id == "unicode"
    assert "vía" in instruction.text
    assert instruction.display_name == "Educación"


def test_instruction_property_access_multiple_times():
    """Test that properties can be accessed multiple times consistently."""
    instruction = MockInstruction()

    # Access each property multiple times
    assert instruction.id == instruction.id
    assert instruction.text == instruction.text
    assert instruction.status == instruction.status
    assert instruction.code == instruction.code
    assert instruction.code_system == instruction.code_system
    assert instruction.display_name == instruction.display_name


def test_instruction_with_vis_reference():
    """Test instruction for Vaccine Information Statement."""
    instruction = MockInstruction(
        instruction_id="vis-001",
        text="Please read the Vaccine Information Statement for MMR vaccine dated 04/20/2023.",
        code="409073007",
        display_name="Education",
    )

    assert "Vaccine Information Statement" in instruction.text
    assert "MMR" in instruction.text


def test_instruction_with_decision_aid():
    """Test instruction referencing a decision aid."""
    instruction = MockInstruction(
        instruction_id="decision-aid-001",
        text="Review the shared decision aid for treatment options. Discuss questions with your provider at next visit.",
        code="311401005",
        display_name="Patient education",
    )

    assert "decision aid" in instruction.text
    assert instruction.code == "311401005"
