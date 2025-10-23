"""Tests for HospitalDischargeInstructionsSection builder."""

from lxml import etree

from ccdakit.builders.sections.hospital_discharge_instructions import (
    HospitalDischargeInstructionsSection,
)
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockDischargeInstruction:
    """Mock discharge instruction for testing."""

    def __init__(
        self,
        instruction_text="Take medications as prescribed",
        instruction_category=None,
    ):
        self._instruction_text = instruction_text
        self._instruction_category = instruction_category

    @property
    def instruction_text(self):
        return self._instruction_text

    @property
    def instruction_category(self):
        return self._instruction_category


class TestHospitalDischargeInstructionsSection:
    """Tests for HospitalDischargeInstructionsSection builder."""

    def test_section_basic(self):
        """Test basic HospitalDischargeInstructionsSection creation."""
        section = HospitalDischargeInstructionsSection(
            narrative_text="Follow up with your doctor in 2 weeks."
        )
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_has_template_id_r21(self):
        """Test section includes R2.1 template ID (CONF:81-9919, CONF:81-10395)."""
        section = HospitalDischargeInstructionsSection(
            narrative_text="Test", version=CDAVersion.R2_1
        )
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.41"
        # No extension in spec
        assert template.get("extension") is None

    def test_section_has_template_id_r20(self):
        """Test section includes R2.0 template ID."""
        section = HospitalDischargeInstructionsSection(
            narrative_text="Test", version=CDAVersion.R2_0
        )
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.41"
        assert template.get("extension") is None

    def test_section_has_code(self):
        """Test section includes correct code (CONF:81-15357, CONF:81-15358, CONF:81-26481)."""
        section = HospitalDischargeInstructionsSection(narrative_text="Test")
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "8653-8"  # Hospital Discharge Instructions
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Hospital Discharge Instructions"

    def test_section_has_title(self):
        """Test section includes title (CONF:81-9921)."""
        section = HospitalDischargeInstructionsSection(
            narrative_text="Test", title="Discharge Instructions for Patient"
        )
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Discharge Instructions for Patient"

    def test_section_default_title(self):
        """Test section uses default title."""
        section = HospitalDischargeInstructionsSection(narrative_text="Test")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Hospital Discharge Instructions"

    def test_section_has_narrative(self):
        """Test section includes narrative text (CONF:81-9922)."""
        section = HospitalDischargeInstructionsSection(narrative_text="Test")
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_narrative_paragraph_text(self):
        """Test narrative with simple paragraph text."""
        narrative = "Please follow up with your primary care physician within 2 weeks."
        section = HospitalDischargeInstructionsSection(narrative_text=narrative)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == narrative

    def test_narrative_with_instructions_list(self):
        """Test narrative with simple instructions list."""
        instructions = [
            MockDischargeInstruction("Take all medications as prescribed"),
            MockDischargeInstruction("Rest and avoid strenuous activity"),
            MockDischargeInstruction("Follow up in 2 weeks"),
        ]
        section = HospitalDischargeInstructionsSection(instructions=instructions)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        list_elem = text.find(f"{{{NS}}}list")
        assert list_elem is not None
        assert list_elem.get("listType") == "unordered"

        items = list_elem.findall(f"{{{NS}}}item")
        assert len(items) == 3
        assert items[0].text == "Take all medications as prescribed"
        assert items[1].text == "Rest and avoid strenuous activity"
        assert items[2].text == "Follow up in 2 weeks"

    def test_narrative_with_categorized_instructions(self):
        """Test narrative with categorized instructions."""
        instructions = [
            MockDischargeInstruction("Take aspirin 81mg daily", instruction_category="Medications"),
            MockDischargeInstruction(
                "Take lisinopril 10mg daily", instruction_category="Medications"
            ),
            MockDischargeInstruction(
                "Avoid heavy lifting for 6 weeks", instruction_category="Activity"
            ),
            MockDischargeInstruction(
                "Walk 15 minutes twice daily", instruction_category="Activity"
            ),
            MockDischargeInstruction("Low sodium diet", instruction_category="Diet"),
        ]
        section = HospitalDischargeInstructionsSection(instructions=instructions)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")

        # Should have category headers (paragraphs with bold content)
        paragraphs = text.findall(f"{{{NS}}}paragraph")
        assert len(paragraphs) >= 3  # At least 3 categories

        # Find category headers
        categories_found = []
        for para in paragraphs:
            content = para.find(f"{{{NS}}}content")
            if content is not None and content.get("styleCode") == "Bold":
                categories_found.append(content.text)

        assert "Medications" in categories_found
        assert "Activity" in categories_found
        assert "Diet" in categories_found

        # Should have lists
        lists = text.findall(f"{{{NS}}}list")
        assert len(lists) >= 3  # At least 3 category lists

    def test_narrative_mixed_categorized_uncategorized(self):
        """Test narrative with both categorized and uncategorized instructions."""
        instructions = [
            MockDischargeInstruction("Take aspirin 81mg daily", instruction_category="Medications"),
            MockDischargeInstruction("Call doctor if fever develops"),
            MockDischargeInstruction("Keep wound clean and dry"),
        ]
        section = HospitalDischargeInstructionsSection(instructions=instructions)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")

        # Should have category headers
        paragraphs = text.findall(f"{{{NS}}}paragraph")
        categories_found = []
        for para in paragraphs:
            content = para.find(f"{{{NS}}}content")
            if content is not None and content.get("styleCode") == "Bold":
                categories_found.append(content.text)

        assert "Medications" in categories_found
        assert "General Instructions" in categories_found

        # Should have lists
        lists = text.findall(f"{{{NS}}}list")
        assert len(lists) >= 2

    def test_narrative_with_both_text_and_instructions(self):
        """Test narrative with both preamble text and instructions list."""
        narrative = "You are being discharged from the hospital. Please follow these instructions:"
        instructions = [
            MockDischargeInstruction("Take all medications as prescribed"),
            MockDischargeInstruction("Follow up in 2 weeks"),
        ]
        section = HospitalDischargeInstructionsSection(
            narrative_text=narrative, instructions=instructions
        )
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")

        # Should have paragraph with preamble
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == narrative

        # Should have list with instructions
        list_elem = text.find(f"{{{NS}}}list")
        assert list_elem is not None
        items = list_elem.findall(f"{{{NS}}}item")
        assert len(items) == 2

    def test_narrative_empty_default_message(self):
        """Test narrative shows default message when no content provided."""
        section = HospitalDischargeInstructionsSection()
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No discharge instructions provided."

    def test_section_no_entries(self):
        """Test section does not contain entry elements."""
        instructions = [
            MockDischargeInstruction("Take medications as prescribed"),
        ]
        section = HospitalDischargeInstructionsSection(instructions=instructions)
        elem = section.to_element()

        # Should not have any entries (this section is narrative-only)
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_section_structure_order(self):
        """Test that section elements are in correct order."""
        section = HospitalDischargeInstructionsSection(narrative_text="Test instructions")
        elem = section.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "code" in names
        assert "title" in names
        assert "text" in names

        # templateId should come before code
        assert names.index("templateId") < names.index("code")
        # code should come before title
        assert names.index("code") < names.index("title")
        # title should come before text
        assert names.index("title") < names.index("text")

    def test_section_to_string(self):
        """Test section serialization."""
        section = HospitalDischargeInstructionsSection(narrative_text="Follow up with your doctor.")
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "8653-8" in xml  # Section code
        assert "Hospital Discharge Instructions" in xml

    def test_single_instruction(self):
        """Test section with single instruction."""
        instructions = [
            MockDischargeInstruction("Take all medications as prescribed"),
        ]
        section = HospitalDischargeInstructionsSection(instructions=instructions)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        list_elem = text.find(f"{{{NS}}}list")
        items = list_elem.findall(f"{{{NS}}}item")
        assert len(items) == 1
        assert items[0].text == "Take all medications as prescribed"

    def test_long_narrative_text(self):
        """Test section with long narrative text."""
        long_text = (
            "You have been discharged from the hospital following surgery. "
            "It is important that you follow all instructions carefully to ensure "
            "proper healing and recovery. Please contact your physician immediately "
            "if you experience fever above 101°F, increased pain, redness, swelling, "
            "or discharge from the surgical site."
        )
        section = HospitalDischargeInstructionsSection(narrative_text=long_text)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == long_text

    def test_special_characters_in_text(self):
        """Test section handles special characters in text."""
        narrative = "Temperature > 101°F or < 95°F requires immediate attention."
        section = HospitalDischargeInstructionsSection(narrative_text=narrative)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        # Special characters should be preserved
        assert ">" in paragraph.text
        assert "<" in paragraph.text
        assert "°" in paragraph.text

    def test_multiple_categories_sorted(self):
        """Test categorized instructions are sorted alphabetically."""
        instructions = [
            MockDischargeInstruction("Walk daily", instruction_category="Activity"),
            MockDischargeInstruction("Low sodium", instruction_category="Diet"),
            MockDischargeInstruction("Take aspirin", instruction_category="Medications"),
            MockDischargeInstruction("Follow up", instruction_category="Follow-up Care"),
        ]
        section = HospitalDischargeInstructionsSection(instructions=instructions)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraphs = text.findall(f"{{{NS}}}paragraph")

        # Extract category headers in order
        categories = []
        for para in paragraphs:
            content = para.find(f"{{{NS}}}content")
            if content is not None and content.get("styleCode") == "Bold":
                categories.append(content.text)

        # Should be sorted alphabetically
        assert categories == sorted(categories)

    def test_empty_instruction_text(self):
        """Test handling of empty instruction text."""
        instructions = [
            MockDischargeInstruction(""),  # Empty text
        ]
        section = HospitalDischargeInstructionsSection(instructions=instructions)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        list_elem = text.find(f"{{{NS}}}list")
        items = list_elem.findall(f"{{{NS}}}item")
        assert len(items) == 1
        assert items[0].text == ""


class TestHospitalDischargeInstructionsSectionIntegration:
    """Integration tests for HospitalDischargeInstructionsSection."""

    def test_complete_section_with_all_features(self):
        """Test creating a complete discharge instructions section with all features."""
        narrative = "You are being discharged from the hospital. Please carefully follow all instructions below."
        instructions = [
            MockDischargeInstruction(
                "Take aspirin 81mg once daily with food",
                instruction_category="Medications",
            ),
            MockDischargeInstruction(
                "Take lisinopril 10mg once daily in the morning",
                instruction_category="Medications",
            ),
            MockDischargeInstruction(
                "Avoid heavy lifting (>10 lbs) for 6 weeks",
                instruction_category="Activity",
            ),
            MockDischargeInstruction(
                "Walk 15-20 minutes twice daily as tolerated",
                instruction_category="Activity",
            ),
            MockDischargeInstruction(
                "Low sodium diet (<2000mg per day)",
                instruction_category="Diet",
            ),
            MockDischargeInstruction(
                "Heart-healthy diet with plenty of fruits and vegetables",
                instruction_category="Diet",
            ),
            MockDischargeInstruction(
                "Follow up with Dr. Smith in 2 weeks",
                instruction_category="Follow-up Care",
            ),
            MockDischargeInstruction("Call 911 if you experience chest pain"),
            MockDischargeInstruction("Keep surgical wound clean and dry until follow-up visit"),
        ]

        section = HospitalDischargeInstructionsSection(
            narrative_text=narrative,
            instructions=instructions,
            title="Discharge Instructions",
        )
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify all required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Verify narrative content
        text = elem.find(f"{{{NS}}}text")

        # Should have preamble paragraph
        paragraphs = text.findall(f"{{{NS}}}paragraph")
        assert len(paragraphs) > 0
        assert paragraphs[0].text == narrative

        # Should have category headers
        categories_found = []
        for para in paragraphs:
            content = para.find(f"{{{NS}}}content")
            if content is not None and content.get("styleCode") == "Bold":
                categories_found.append(content.text)

        assert "Medications" in categories_found
        assert "Activity" in categories_found
        assert "Diet" in categories_found
        assert "Follow-up Care" in categories_found
        assert "General Instructions" in categories_found

        # Should have multiple lists (one per category)
        lists = text.findall(f"{{{NS}}}list")
        assert len(lists) == 5  # 4 categories + 1 general

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        section = HospitalDischargeInstructionsSection(
            narrative_text="Follow up with your doctor in 2 weeks."
        )

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_r20_version(self):
        """Test section with R2.0 version."""
        section = HospitalDischargeInstructionsSection(
            narrative_text="Test", version=CDAVersion.R2_0
        )
        elem = section.to_element()

        # Check template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.41"
        assert template.get("extension") is None

    def test_section_r21_version(self):
        """Test section with R2.1 version."""
        section = HospitalDischargeInstructionsSection(
            narrative_text="Test", version=CDAVersion.R2_1
        )
        elem = section.to_element()

        # Check template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.41"
        assert template.get("extension") is None

    def test_realistic_discharge_instructions(self):
        """Test with realistic discharge instructions content."""
        instructions = [
            MockDischargeInstruction(
                "Take Metoprolol 25mg twice daily for blood pressure",
                instruction_category="Medications",
            ),
            MockDischargeInstruction(
                "Take Warfarin 5mg daily in the evening (INR monitoring required)",
                instruction_category="Medications",
            ),
            MockDischargeInstruction(
                "No driving until cleared by your physician",
                instruction_category="Activity",
            ),
            MockDischargeInstruction(
                "Resume walking as tolerated, gradually increase distance",
                instruction_category="Activity",
            ),
            MockDischargeInstruction(
                "Low-fat, low-cholesterol diet",
                instruction_category="Diet",
            ),
            MockDischargeInstruction(
                "Limit caffeine and alcohol consumption",
                instruction_category="Diet",
            ),
            MockDischargeInstruction(
                "Follow up with cardiologist Dr. Johnson in 1 week",
                instruction_category="Follow-up Care",
            ),
            MockDischargeInstruction(
                "INR check in 3 days at the anticoagulation clinic",
                instruction_category="Follow-up Care",
            ),
            MockDischargeInstruction("Monitor weight daily and report gain of >2 lbs in 24 hours"),
            MockDischargeInstruction(
                "Call 911 immediately if you experience chest pain, shortness of breath, or severe dizziness"
            ),
        ]

        section = HospitalDischargeInstructionsSection(
            instructions=instructions,
            title="Discharge Instructions - Cardiac Care",
        )

        elem = section.to_element()

        # Verify it builds successfully
        assert local_name(elem) == "section"

        # Verify it can be serialized
        xml = section.to_string(pretty=True)
        assert "Cardiac Care" in xml

    def test_section_with_only_narrative(self):
        """Test section with only narrative text (no structured instructions)."""
        narrative = (
            "DISCHARGE INSTRUCTIONS\n\n"
            "1. Take all medications as prescribed\n"
            "2. Follow up with your doctor in 2 weeks\n"
            "3. Call if you have fever >101F or worsening symptoms\n"
            "4. Rest and avoid strenuous activity for 1 week"
        )

        section = HospitalDischargeInstructionsSection(narrative_text=narrative)
        elem = section.to_element()

        # Should have only paragraph, no lists
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == narrative

        lists = text.findall(f"{{{NS}}}list")
        assert len(lists) == 0

    def test_section_with_only_instructions(self):
        """Test section with only structured instructions (no preamble)."""
        instructions = [
            MockDischargeInstruction("Take aspirin 81mg daily"),
            MockDischargeInstruction("Rest for 3 days"),
            MockDischargeInstruction("Follow up in 1 week"),
        ]

        section = HospitalDischargeInstructionsSection(instructions=instructions)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")

        # Should have list
        list_elem = text.find(f"{{{NS}}}list")
        assert list_elem is not None

        # Should not have a preamble paragraph (might have category headers though)
        # Check that the first paragraph (if any) is not a simple text paragraph
        paragraphs = text.findall(f"{{{NS}}}paragraph")
        if paragraphs:
            # If there are paragraphs, they should be category headers with content elements
            for para in paragraphs:
                content = para.find(f"{{{NS}}}content")
                assert content is not None  # Should be a category header

    def test_category_with_multiple_instructions(self):
        """Test category with multiple instructions are all included."""
        instructions = [
            MockDischargeInstruction("Aspirin 81mg once daily", instruction_category="Medications"),
            MockDischargeInstruction(
                "Metoprolol 25mg twice daily", instruction_category="Medications"
            ),
            MockDischargeInstruction(
                "Lisinopril 10mg once daily", instruction_category="Medications"
            ),
            MockDischargeInstruction(
                "Atorvastatin 40mg at bedtime", instruction_category="Medications"
            ),
        ]

        section = HospitalDischargeInstructionsSection(instructions=instructions)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        lists = text.findall(f"{{{NS}}}list")

        # Should have one list for medications
        assert len(lists) == 1

        items = lists[0].findall(f"{{{NS}}}item")
        assert len(items) == 4

        # Verify all medications are present
        item_texts = [item.text for item in items]
        assert "Aspirin 81mg once daily" in item_texts
        assert "Metoprolol 25mg twice daily" in item_texts
        assert "Lisinopril 10mg once daily" in item_texts
        assert "Atorvastatin 40mg at bedtime" in item_texts
