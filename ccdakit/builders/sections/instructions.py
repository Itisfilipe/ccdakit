"""Instructions Section builder for C-CDA documents."""

from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.instruction import Instruction
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.instruction import InstructionProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class InstructionsSection(CDAElement):
    """
    Builder for C-CDA Instructions Section (V2).

    This section records instructions given to a patient. It can be used to list
    patient decision aids, education materials, and other instructions provided
    to the patient or their caregivers.

    Template ID: 2.16.840.1.113883.10.20.22.2.45
    Release: 2014-06-09

    Supports both R2.1 and R2.0 versions.

    Conformance Rules:
    - MAY contain @nullFlavor="NI" (CONF:1098-32835)
    - SHALL contain templateId with root="2.16.840.1.113883.10.20.22.2.45" (CONF:1098-10112, CONF:1098-31384)
    - SHALL contain templateId extension="2014-06-09" (CONF:1098-32599)
    - SHALL contain code="69730-0" from LOINC (CONF:1098-15375, CONF:1098-15376, CONF:1098-32148)
    - SHALL contain title (CONF:1098-10114)
    - SHALL contain text (CONF:1098-10115)
    - SHALL contain at least one [1..*] entry with Instruction (V2) if @nullFlavor not present (CONF:1098-10116, CONF:1098-31398)

    Common Uses:
    - Patient education materials
    - Decision aids
    - Care instructions
    - Discharge instructions
    - Medication instructions
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.45",
                extension="2014-06-09",
                description="Instructions Section (V2)",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.45",
                extension="2014-06-09",
                description="Instructions Section (V2)",
            ),
        ],
    }

    def __init__(
        self,
        instructions: Optional[Sequence[InstructionProtocol]] = None,
        title: str = "Instructions",
        version: CDAVersion = CDAVersion.R2_1,
        null_flavor: str = None,
        **kwargs,
    ):
        """
        Initialize InstructionsSection builder.

        Args:
            instructions: List of instructions satisfying InstructionProtocol
            title: Section title (default: "Instructions")
            version: C-CDA version (R2.1 or R2.0)
            null_flavor: Optional null flavor (e.g., "NI" for no information)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.instructions = instructions or []
        self.title = title
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        """
        Build Instructions Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add null flavor if specified (CONF:1098-32835)
        if self.null_flavor:
            section.set("nullFlavor", self.null_flavor)

        # Add template IDs (CONF:1098-10112, CONF:1098-31384, CONF:1098-32599)
        self.add_template_ids(section)

        # Add section code (CONF:1098-15375, CONF:1098-15376, CONF:1098-32148)
        # 69730-0 = Instructions (LOINC)
        code_elem = Code(
            code="69730-0",
            system="LOINC",
            display_name="Instructions",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1098-10114)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:1098-10115)
        self._add_narrative(section)

        # Add entries with Instruction (V2) (CONF:1098-10116, CONF:1098-31398)
        # SHALL contain at least one entry if @nullFlavor is not present
        for instruction in self.instructions:
            self._add_instruction_entry(section, instruction)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.instructions:
            # No instructions - add "No instructions documented" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No instructions documented"
            return

        # Create table for instructions
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = ["Instruction Type", "Details"]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, instruction in enumerate(self.instructions, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Instruction Type (code display name or default)
            td_type = etree.SubElement(tr, f"{{{NS}}}td")
            if hasattr(instruction, "display_name") and instruction.display_name:
                td_type.text = instruction.display_name
            elif hasattr(instruction, "code") and instruction.code:
                td_type.text = f"Instruction ({instruction.code})"
            else:
                td_type.text = "Instruction"

            # Details (with ID reference)
            td_details = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_details,
                f"{{{NS}}}content",
                ID=f"instruction-{idx}",
            )
            # Support both 'text' and 'instruction_text' properties for backward compatibility
            if hasattr(instruction, "text"):
                content.text = instruction.text
            elif hasattr(instruction, "instruction_text"):
                content.text = instruction.instruction_text
            else:
                content.text = ""

    def _add_instruction_entry(
        self,
        section: etree._Element,
        instruction: InstructionProtocol,
    ) -> None:
        """
        Add entry element with Instruction (V2).

        Args:
            section: section element
            instruction: Instruction data
        """
        # Create entry element (SHALL contain - CONF:1098-10116)
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Instruction (V2) (CONF:1098-31398)
        instruction_builder = Instruction(instruction, version=self.version)
        entry.append(instruction_builder.to_element())
