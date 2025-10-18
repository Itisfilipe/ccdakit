"""Instruction entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.plan_of_treatment import InstructionProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class Instruction(CDAElement):
    """
    Builder for C-CDA Instruction entry.

    Represents an instruction with text.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    Template ID: 2.16.840.1.113883.10.20.22.4.20
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.20",
                extension="2014-06-09",
                description="Instruction R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.20",
                extension="2014-06-09",
                description="Instruction R2.0",
            ),
        ],
    }

    def __init__(
        self,
        instruction: InstructionProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize Instruction builder.

        Args:
            instruction: Instruction data
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.instruction = instruction

    def build(self) -> etree.Element:
        """
        Build Instruction XML element.

        Returns:
            lxml Element for act
        """
        # Create act element with required attributes
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="INT",  # Intent
        )

        # Add template IDs
        self.add_template_ids(act)

        # Add IDs
        self._add_ids(act)

        # Add code (instruction type)
        code_elem = Code(
            code="409073007",
            system="SNOMED",
            display_name="instruction",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        act.append(code_elem)

        # Add status code (always completed for instructions)
        status_elem = StatusCode("completed").to_element()
        act.append(status_elem)

        # Add text element with instruction content
        text = etree.SubElement(act, f"{{{NS}}}text")
        text.text = self.instruction.instruction_text

        return act

    def _add_ids(self, act: etree._Element) -> None:
        """
        Add ID elements to act.

        Args:
            act: act element
        """
        # Add persistent ID if available
        if self.instruction.persistent_id:
            pid = self.instruction.persistent_id
            id_elem = Identifier(root=pid.root, extension=pid.extension).to_element()
            act.append(id_elem)
        else:
            # Add a generated ID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            act.append(id_elem)
