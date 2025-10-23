"""Tests for InstructionsSection builder."""

from lxml import etree

from ccdakit.builders.sections.instructions import InstructionsSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockInstruction:
    """Mock instruction for testing."""

    def __init__(
        self,
        id="INSTR-001",
        text="Take one tablet by mouth daily with food",
        code="171044003",
        code_system="SNOMED",
        display_name="Medication education",
        status="completed",
    ):
        self._id = id
        self._text = text
        self._code = code
        self._code_system = code_system
        self._display_name = display_name
        self._status = status

    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return self._text

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def display_name(self):
        return self._display_name

    @property
    def status(self):
        return self._status


class TestInstructionsSection:
    """Tests for InstructionsSection builder."""

    def test_instructions_section_basic(self):
        """Test basic InstructionsSection creation."""
        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_instructions_section_has_template_id_r21(self):
        """Test InstructionsSection includes R2.1 template ID."""
        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.45"
        assert template.get("extension") == "2014-06-09"

    def test_instructions_section_has_template_id_r20(self):
        """Test InstructionsSection includes R2.0 template ID."""
        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.45"
        assert template.get("extension") == "2014-06-09"

    def test_instructions_section_has_code(self):
        """Test InstructionsSection includes section code."""
        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "69730-0"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Instructions"

    def test_instructions_section_has_title(self):
        """Test InstructionsSection includes title."""
        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction], title="Patient Instructions")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Patient Instructions"

    def test_instructions_section_default_title(self):
        """Test InstructionsSection uses default title."""
        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Instructions"

    def test_instructions_section_has_narrative(self):
        """Test InstructionsSection includes narrative text."""
        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_instructions_section_narrative_table(self):
        """Test narrative includes HTML table."""
        instruction = MockInstruction(
            text="Take one tablet daily",
            display_name="Medication education",
        )
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        assert table is not None
        assert table.get("border") == "1"

        # Check table header
        thead = table.find(f"{{{NS}}}thead")
        assert thead is not None
        tr = thead.find(f"{{{NS}}}tr")
        ths = tr.findall(f"{{{NS}}}th")
        assert len(ths) == 2  # Instruction Type, Details

    def test_instructions_section_narrative_content(self):
        """Test narrative contains instruction data."""
        instruction = MockInstruction(
            text="Take with food and plenty of water",
            display_name="Medication education",
        )
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 2

        # Check type
        assert tds[0].text == "Medication education"

        # Check details with ID
        content = tds[1].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Take with food and plenty of water"
        assert content.get("ID") == "instruction-1"

    def test_instructions_section_empty_narrative(self):
        """Test narrative when no instructions."""
        section = InstructionsSection()
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No instructions documented"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_instructions_section_has_entries(self):
        """Test InstructionsSection includes entry elements."""
        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_instructions_section_entry_has_act(self):
        """Test entry contains instruction act."""
        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"
        assert act.get("moodCode") == "INT"

    def test_instructions_section_act_has_template_id(self):
        """Test instruction act has correct template ID."""
        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        template = act.find(f"{{{NS}}}templateId")

        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.20"
        assert template.get("extension") == "2014-06-09"

    def test_instructions_section_act_has_id(self):
        """Test instruction act has ID element."""
        instruction = MockInstruction(id="INSTR-123")
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        id_elem = act.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("extension") == "INSTR-123"

    def test_instructions_section_act_has_code(self):
        """Test instruction act has correct code."""
        instruction = MockInstruction(
            code="171044003",
            code_system="SNOMED",
            display_name="Medication education",
        )
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        code = act.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "171044003"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT

    def test_instructions_section_act_has_status_code(self):
        """Test instruction act has statusCode element."""
        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        status = act.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "completed"

    def test_instructions_section_act_has_text(self):
        """Test instruction act includes text element."""
        instruction = MockInstruction(text="Take medication with meals")
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        text = act.find(f"{{{NS}}}text")

        assert text is not None
        assert text.text == "Take medication with meals"

    def test_instructions_section_multiple_entries(self):
        """Test InstructionsSection with multiple instructions."""
        instructions = [
            MockInstruction(text="First instruction"),
            MockInstruction(text="Second instruction"),
        ]
        section = InstructionsSection(instructions=instructions)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_instructions_section_null_flavor(self):
        """Test InstructionsSection with null flavor."""
        section = InstructionsSection(null_flavor="NI")
        elem = section.to_element()

        assert elem.get("nullFlavor") == "NI"

    def test_instructions_section_to_string(self):
        """Test InstructionsSection serialization."""
        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "69730-0" in xml  # Section code
        assert "Instructions" in xml

    def test_instructions_section_structure_order(self):
        """Test that section elements are in correct order."""
        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "code" in names
        assert "title" in names
        assert "text" in names
        assert "entry" in names

        # templateId should come before code
        assert names.index("templateId") < names.index("code")
        # code should come before title
        assert names.index("code") < names.index("title")
        # title should come before text
        assert names.index("title") < names.index("text")
        # text should come before entry
        assert names.index("text") < names.index("entry")

    def test_instructions_section_narrative_without_display_name(self):
        """Test narrative when instruction has no display_name."""
        instruction = MockInstruction(display_name=None, code="409073007")
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Should show "Instruction (code)"
        assert "409073007" in tds[0].text

    def test_instructions_section_narrative_without_code(self):
        """Test narrative when instruction has no code."""
        instruction = MockInstruction(code=None, display_name=None)
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Should show "Instruction"
        assert tds[0].text == "Instruction"


class TestInstructionsSectionIntegration:
    """Integration tests for InstructionsSection."""

    def test_complete_instructions_section(self):
        """Test creating a complete instructions section."""
        instructions = [
            MockInstruction(
                id="INSTR-001",
                text="Take one tablet by mouth daily with food",
                code="171044003",
                display_name="Medication education",
            ),
            MockInstruction(
                id="INSTR-002",
                text="Review the medication guide provided with your prescription",
                code="311401005",
                display_name="Patient education",
            ),
            MockInstruction(
                id="INSTR-003",
                text="Follow up with your primary care physician in 2 weeks",
                code="409073007",
                display_name="Education",
            ),
        ]

        section = InstructionsSection(
            instructions=instructions,
            title="Patient Care Instructions",
        )
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify narrative table has 3 rows
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 3

        # Verify 3 entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 3

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        instruction = MockInstruction()
        section = InstructionsSection(instructions=[instruction])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_empty_instructions_section(self):
        """Test InstructionsSection with no instructions."""
        section = InstructionsSection()
        elem = section.to_element()

        # Should still have required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Should have no entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

        # Narrative should show "No instructions documented"
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No instructions documented"

    def test_corner_case_minimal_instruction(self):
        """Test instruction with minimal required fields."""
        instruction = MockInstruction(
            id="MIN-001",
            text="Minimal instruction text",
        )
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        # Should still build successfully
        assert elem is not None
        assert elem.find(f"{{{NS}}}entry") is not None

    def test_instruction_with_special_characters(self):
        """Test instruction with special characters in text."""
        instruction = MockInstruction(
            text="Take 1-2 tablets every 4-6 hours as needed for pain. Don't exceed 8 tablets/day.",
        )
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        text = act.find(f"{{{NS}}}text")

        assert "1-2 tablets" in text.text
        assert "Don't" in text.text

    def test_large_number_of_instructions(self):
        """Test section with many instructions."""
        instructions = [
            MockInstruction(id=f"INSTR-{i:03d}", text=f"Instruction {i}") for i in range(20)
        ]
        section = InstructionsSection(instructions=instructions)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 20

        # Check narrative has 20 rows
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 20

    def test_instruction_with_different_code_systems(self):
        """Test instructions with various code systems."""
        instructions = [
            MockInstruction(code="171044003", code_system="SNOMED", display_name="Medication education"),
            MockInstruction(code="LP7839-6", code_system="LOINC", display_name="Education about risk factors"),
        ]
        section = InstructionsSection(instructions=instructions)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check first entry uses SNOMED
        act1 = entries[0].find(f"{{{NS}}}act")
        code1 = act1.find(f"{{{NS}}}code")
        assert code1.get("code") == "171044003"
        assert code1.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED

        # Check second entry uses LOINC
        act2 = entries[1].find(f"{{{NS}}}act")
        code2 = act2.find(f"{{{NS}}}code")
        assert code2.get("code") == "LP7839-6"
        assert code2.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC

    def test_instruction_narrative_id_numbering(self):
        """Test that narrative IDs are numbered sequentially."""
        instructions = [
            MockInstruction(text="First instruction"),
            MockInstruction(text="Second instruction"),
            MockInstruction(text="Third instruction"),
        ]
        section = InstructionsSection(instructions=instructions)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        # Check IDs are numbered correctly
        for idx, tr in enumerate(trs, start=1):
            tds = tr.findall(f"{{{NS}}}td")
            content = tds[1].find(f"{{{NS}}}content")
            assert content.get("ID") == f"instruction-{idx}"

    def test_null_flavor_with_empty_instructions(self):
        """Test section with null flavor and no instructions."""
        section = InstructionsSection(null_flavor="NI", instructions=[])
        elem = section.to_element()

        assert elem.get("nullFlavor") == "NI"

        # Should still have required structure elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Should have no entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0


class TestInstructionsSectionBackwardCompatibility:
    """Tests for backward compatibility with plan_of_treatment protocol."""

    def test_instruction_with_instruction_text_property(self):
        """Test instruction using instruction_text property (plan_of_treatment protocol)."""

        class LegacyInstruction:
            """Mock instruction using old protocol."""

            @property
            def instruction_text(self):
                return "Take with food"

            @property
            def persistent_id(self):
                return None

            @property
            def code(self):
                return None

            @property
            def code_system(self):
                return None

            @property
            def display_name(self):
                return None

            @property
            def status(self):
                return "completed"

        instruction = LegacyInstruction()
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        text = act.find(f"{{{NS}}}text")

        assert text is not None
        assert text.text == "Take with food"

    def test_instruction_with_persistent_id(self):
        """Test instruction with persistent_id property."""

        class PersistentID:
            @property
            def root(self):
                return "2.16.840.1.113883.19"

            @property
            def extension(self):
                return "PERSISTENT-ID-123"

        class InstructionWithPersistentID:
            @property
            def text(self):
                return "Follow up in 2 weeks"

            @property
            def persistent_id(self):
                return PersistentID()

        instruction = InstructionWithPersistentID()
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        id_elem = act.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.19"
        assert id_elem.get("extension") == "PERSISTENT-ID-123"

    def test_narrative_instruction_without_text(self):
        """Test narrative with instruction that has neither text nor instruction_text."""

        class InstructionWithoutText:
            @property
            def display_name(self):
                return "Physical Therapy"

            @property
            def code(self):
                return "91251008"

        instruction = InstructionWithoutText()
        section = InstructionsSection(instructions=[instruction])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Details column should have empty content
        content = tds[1].find(f"{{{NS}}}content")
        assert content.text == ""
