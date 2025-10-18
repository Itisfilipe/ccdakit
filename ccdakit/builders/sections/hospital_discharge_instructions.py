"""Hospital Discharge Instructions Section builder for C-CDA documents."""

from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.discharge_instructions import DischargeInstructionProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class HospitalDischargeInstructionsSection(CDAElement):
    """
    Builder for C-CDA Hospital Discharge Instructions Section.

    This section records instructions provided to the patient at hospital discharge.
    It contains only narrative text (no structured entries are required or typically used).

    The section can contain general discharge instructions or categorized instructions
    (e.g., medications, diet, activity, follow-up care).

    Supports both R2.1 and R2.0 versions.

    Conformance:
    - Template ID: 2.16.840.1.113883.10.20.22.2.41
    - Code: 8653-8 (Hospital Discharge Instructions) from LOINC
    - Contains: Narrative text only (no entries required)

    References:
    - CONF:81-9919: SHALL contain templateId
    - CONF:81-10395: templateId/@root="2.16.840.1.113883.10.20.22.2.41"
    - CONF:81-15357: SHALL contain code
    - CONF:81-15358: code/@code="8653-8"
    - CONF:81-26481: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
    - CONF:81-9921: SHALL contain title
    - CONF:81-9922: SHALL contain text
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.41",
                extension=None,  # No extension in spec
                description="Hospital Discharge Instructions Section R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.41",
                extension=None,
                description="Hospital Discharge Instructions Section R2.0",
            ),
        ],
    }

    def __init__(
        self,
        instructions: Optional[Sequence[DischargeInstructionProtocol]] = None,
        narrative_text: Optional[str] = None,
        title: str = "Hospital Discharge Instructions",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize HospitalDischargeInstructionsSection builder.

        You can provide either:
        1. A list of DischargeInstructionProtocol objects (will be formatted as a list/table)
        2. A narrative_text string (will be used as-is in a paragraph)
        3. Both (instructions will be formatted as a table, narrative_text as preamble)

        Args:
            instructions: List of discharge instructions (optional)
            narrative_text: Free-form narrative text for instructions (optional)
            title: Section title (default: "Hospital Discharge Instructions")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement

        Raises:
            ValueError: If neither instructions nor narrative_text is provided
        """
        super().__init__(version=version, **kwargs)
        self.instructions = instructions or []
        self.narrative_text = narrative_text
        self.title = title

        # At least one source of content must be provided
        if not self.instructions and not self.narrative_text:
            # Allow empty content - will show default message
            self.narrative_text = "No discharge instructions provided."

    def build(self) -> etree.Element:
        """
        Build Hospital Discharge Instructions Section XML element.

        Conformance:
        - CONF:81-9919: SHALL contain templateId
        - CONF:81-10395: templateId/@root="2.16.840.1.113883.10.20.22.2.41"
        - CONF:81-15357: SHALL contain code
        - CONF:81-15358: code/@code="8653-8"
        - CONF:81-26481: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
        - CONF:81-9921: SHALL contain title
        - CONF:81-9922: SHALL contain text

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:81-9919, CONF:81-10395)
        self.add_template_ids(section)

        # Add section code (CONF:81-15357, CONF:81-15358, CONF:81-26481)
        # 8653-8 = Hospital Discharge Instructions (LOINC)
        code_elem = Code(
            code="8653-8",
            system="LOINC",
            display_name="Hospital Discharge Instructions",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:81-9921)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:81-9922)
        self._add_narrative(section)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with formatted content.

        The narrative can contain:
        1. Simple paragraph text (if narrative_text is provided)
        2. Categorized list (if instructions with categories are provided)
        3. Simple list (if instructions without categories are provided)
        4. Both paragraph and list

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        # Add preamble paragraph if narrative_text is provided
        if self.narrative_text:
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = self.narrative_text

        # Add instructions if provided
        if self.instructions:
            self._add_instructions_narrative(text)

    def _add_instructions_narrative(self, text: etree._Element) -> None:
        """
        Add instructions to narrative text.

        If instructions have categories, they're grouped by category with headers.
        Otherwise, they're shown as a simple list.

        Args:
            text: text element
        """
        # Check if any instructions have categories
        has_categories = any(
            instr.instruction_category for instr in self.instructions
        )

        if has_categories:
            self._add_categorized_instructions(text)
        else:
            self._add_simple_instructions_list(text)

    def _add_categorized_instructions(self, text: etree._Element) -> None:
        """
        Add instructions grouped by category with section headers.

        Args:
            text: text element
        """
        # Group instructions by category
        categorized = {}
        uncategorized = []

        for instr in self.instructions:
            if instr.instruction_category:
                category = instr.instruction_category
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append(instr)
            else:
                uncategorized.append(instr)

        # Add categorized sections
        for category in sorted(categorized.keys()):
            # Add category header
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            content = etree.SubElement(paragraph, f"{{{NS}}}content")
            content.set("styleCode", "Bold")
            content.text = category

            # Add instructions as list
            list_elem = etree.SubElement(text, f"{{{NS}}}list")
            list_elem.set("listType", "unordered")

            for instr in categorized[category]:
                item = etree.SubElement(list_elem, f"{{{NS}}}item")
                item.text = instr.instruction_text

        # Add uncategorized instructions if any
        if uncategorized:
            if categorized:  # Add header only if we had categories
                paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
                content = etree.SubElement(paragraph, f"{{{NS}}}content")
                content.set("styleCode", "Bold")
                content.text = "General Instructions"

            list_elem = etree.SubElement(text, f"{{{NS}}}list")
            list_elem.set("listType", "unordered")

            for instr in uncategorized:
                item = etree.SubElement(list_elem, f"{{{NS}}}item")
                item.text = instr.instruction_text

    def _add_simple_instructions_list(self, text: etree._Element) -> None:
        """
        Add instructions as a simple unordered list.

        Args:
            text: text element
        """
        list_elem = etree.SubElement(text, f"{{{NS}}}list")
        list_elem.set("listType", "unordered")

        for instr in self.instructions:
            item = etree.SubElement(list_elem, f"{{{NS}}}item")
            item.text = instr.instruction_text
