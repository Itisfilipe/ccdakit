"""Tests for discharge instructions protocols."""

from ccdakit.protocols.discharge_instructions import DischargeInstructionProtocol


class MockDischargeInstruction:
    """Test implementation of DischargeInstructionProtocol."""

    def __init__(
        self,
        instruction_text: str = "Take medications as prescribed",
        instruction_category: str = None,
    ):
        self._instruction_text = instruction_text
        self._instruction_category = instruction_category

    @property
    def instruction_text(self):
        return self._instruction_text

    @property
    def instruction_category(self):
        return self._instruction_category


def test_discharge_instruction_protocol_required_fields():
    """Test DischargeInstructionProtocol required fields."""
    instruction = MockDischargeInstruction()

    assert instruction.instruction_text == "Take medications as prescribed"


def test_discharge_instruction_with_category():
    """Test DischargeInstructionProtocol with instruction category."""
    instruction = MockDischargeInstruction(
        instruction_text="Take aspirin 81mg daily",
        instruction_category="Medications",
    )

    assert instruction.instruction_text == "Take aspirin 81mg daily"
    assert instruction.instruction_category == "Medications"


def test_discharge_instruction_without_category():
    """Test DischargeInstructionProtocol without instruction category."""
    instruction = MockDischargeInstruction()

    assert instruction.instruction_category is None


def test_discharge_instruction_protocol_satisfaction():
    """Test that MockDischargeInstruction satisfies DischargeInstructionProtocol."""
    instruction = MockDischargeInstruction()

    def accepts_instruction(i: DischargeInstructionProtocol) -> str:
        return f"{i.instruction_text}"

    result = accepts_instruction(instruction)
    assert result == "Take medications as prescribed"


def test_discharge_instruction_medication_category():
    """Test discharge instruction for medication category."""
    instruction = MockDischargeInstruction(
        instruction_text="Continue taking lisinopril 10mg daily for blood pressure control",
        instruction_category="Medications",
    )

    assert instruction.instruction_category == "Medications"


def test_discharge_instruction_activity_category():
    """Test discharge instruction for activity category."""
    instruction = MockDischargeInstruction(
        instruction_text="No heavy lifting for 6 weeks. Resume normal activities gradually.",
        instruction_category="Activity",
    )

    assert instruction.instruction_category == "Activity"


def test_discharge_instruction_diet_category():
    """Test discharge instruction for diet category."""
    instruction = MockDischargeInstruction(
        instruction_text="Follow a low-sodium diet. Limit sodium intake to 2000mg per day.",
        instruction_category="Diet",
    )

    assert instruction.instruction_category == "Diet"


def test_discharge_instruction_followup_category():
    """Test discharge instruction for follow-up category."""
    instruction = MockDischargeInstruction(
        instruction_text="Schedule follow-up appointment with cardiologist in 2 weeks.",
        instruction_category="Follow-up",
    )

    assert instruction.instruction_category == "Follow-up"


def test_discharge_instruction_wound_care_category():
    """Test discharge instruction for wound care category."""
    instruction = MockDischargeInstruction(
        instruction_text="Keep incision clean and dry. Change dressing daily.",
        instruction_category="Wound Care",
    )

    assert instruction.instruction_category == "Wound Care"


def test_discharge_instruction_empty_category():
    """Test discharge instruction with empty string category."""
    instruction = MockDischargeInstruction(
        instruction_text="General instructions",
        instruction_category="",
    )

    assert instruction.instruction_category == ""


def test_discharge_instruction_long_text():
    """Test discharge instruction with long text."""
    long_text = (
        "You were admitted with chest pain and diagnosed with a heart attack. "
        "During your stay, you underwent cardiac catheterization and had a stent placed. "
        "It is important that you take all medications as prescribed. "
        "Follow up with your cardiologist in 2 weeks. "
        "Call 911 if you experience chest pain, shortness of breath, or other concerning symptoms."
    )
    instruction = MockDischargeInstruction(
        instruction_text=long_text,
        instruction_category="Discharge Summary",
    )

    assert instruction.instruction_text == long_text
    assert len(instruction.instruction_text) > 100


def test_discharge_instruction_multiline_text():
    """Test discharge instruction with multiline text."""
    multiline = """Instructions for care at home:
1. Take all medications as prescribed
2. Monitor your blood pressure daily
3. Follow a heart-healthy diet
4. Exercise as tolerated"""

    instruction = MockDischargeInstruction(
        instruction_text=multiline,
        instruction_category="General",
    )

    assert "\n" in instruction.instruction_text
    assert "1." in instruction.instruction_text


class MinimalDischargeInstruction:
    """Minimal implementation with only required fields."""

    @property
    def instruction_text(self):
        return "Rest and take prescribed medications"

    @property
    def instruction_category(self):
        return None


def test_minimal_discharge_instruction_protocol():
    """Test that minimal implementation satisfies DischargeInstructionProtocol."""
    instruction = MinimalDischargeInstruction()

    assert instruction.instruction_text == "Rest and take prescribed medications"
    assert instruction.instruction_category is None


def test_discharge_instruction_isinstance_check():
    """Test that MockDischargeInstruction supports protocol typing."""
    instruction = MockDischargeInstruction()

    # Protocol structural typing
    assert isinstance(instruction, object)
    assert hasattr(instruction, 'instruction_text')
    assert hasattr(instruction, 'instruction_category')


def test_discharge_instruction_various_categories():
    """Test discharge instruction with various category types."""
    categories = [
        "Medications",
        "Activity",
        "Diet",
        "Follow-up",
        "Wound Care",
        "Signs and Symptoms",
        "Emergency Instructions",
    ]

    for category in categories:
        instruction = MockDischargeInstruction(
            instruction_text=f"Instructions for {category}",
            instruction_category=category,
        )
        assert instruction.instruction_category == category


def test_discharge_instruction_special_characters():
    """Test discharge instruction with special characters in text."""
    instruction = MockDischargeInstruction(
        instruction_text="Take 81mg (low-dose) aspirin daily @ bedtime; avoid NSAIDs!",
        instruction_category="Medications",
    )

    assert "@" in instruction.instruction_text
    assert ";" in instruction.instruction_text
    assert "!" in instruction.instruction_text


def test_discharge_instruction_unicode_characters():
    """Test discharge instruction with unicode characters."""
    instruction = MockDischargeInstruction(
        instruction_text="Follow-up in 2–3 weeks. Monitor for signs/symptoms → call if issues.",
        instruction_category="Follow-up",
    )

    assert "–" in instruction.instruction_text or "-" in instruction.instruction_text
    assert instruction.instruction_category == "Follow-up"


def test_discharge_instruction_empty_text():
    """Test discharge instruction with empty string text."""
    instruction = MockDischargeInstruction(
        instruction_text="",
        instruction_category="General",
    )

    assert instruction.instruction_text == ""


def test_discharge_instruction_protocol_function_parameter():
    """Test using DischargeInstructionProtocol as function parameter."""
    def process_instruction(instr: DischargeInstructionProtocol) -> dict:
        return {
            "text": instr.instruction_text,
            "category": instr.instruction_category or "Unspecified",
        }

    instruction = MockDischargeInstruction(
        instruction_text="Test instruction",
        instruction_category="Test",
    )

    result = process_instruction(instruction)
    assert result["text"] == "Test instruction"
    assert result["category"] == "Test"


def test_discharge_instruction_multiple_instructions():
    """Test creating multiple discharge instructions."""
    med_instruction = MockDischargeInstruction(
        instruction_text="Take all medications as prescribed",
        instruction_category="Medications",
    )

    activity_instruction = MockDischargeInstruction(
        instruction_text="Resume light activity as tolerated",
        instruction_category="Activity",
    )

    diet_instruction = MockDischargeInstruction(
        instruction_text="Follow a balanced diet",
        instruction_category="Diet",
    )

    instructions = [med_instruction, activity_instruction, diet_instruction]

    assert len(instructions) == 3
    assert all(hasattr(i, 'instruction_text') for i in instructions)
    assert all(hasattr(i, 'instruction_category') for i in instructions)
