"""Instruction entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig


# CDA namespace
NS = "urn:hl7-org:v3"


class Instruction(CDAElement):
    """
    Builder for C-CDA Instruction (V2) entry.

    The Instruction template represents patient instructions. It can be used in several ways,
    such as to record patient instructions within a Medication Activity or to record fill
    instructions within a supply order. Instructions are prospective (moodCode=INT).

    If an instruction was already given, the Procedure Activity Act template should be used
    instead to represent the completed instruction.

    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    Template ID: 2.16.840.1.113883.10.20.22.4.20

    Conformance Rules:
    - SHALL contain @classCode="ACT" (CONF:1098-7391)
    - SHALL contain @moodCode="INT" (CONF:1098-7392)
    - SHALL contain templateId with root="2.16.840.1.113883.10.20.22.4.20" (CONF:1098-7393, CONF:1098-10503)
    - SHALL contain templateId extension="2014-06-09" (CONF:1098-32598)
    - SHALL contain code, SHOULD be from ValueSet Patient Education (CONF:1098-16884)
    - SHALL contain statusCode="completed" (CONF:1098-7396, CONF:1098-19106)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.20",
                extension="2014-06-09",
                description="Instruction (V2)",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.20",
                extension="2014-06-09",
                description="Instruction (V2)",
            ),
        ],
    }

    def __init__(
        self,
        instruction,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize Instruction builder.

        Args:
            instruction: Instruction data satisfying InstructionProtocol
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
        # Create act element with required attributes (CONF:1098-7391, CONF:1098-7392)
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="INT",  # Intent
        )

        # Add template IDs (CONF:1098-7393, CONF:1098-10503, CONF:1098-32598)
        self.add_template_ids(act)

        # Add IDs
        self._add_ids(act)

        # Add code (instruction type) (CONF:1098-16884)
        # SHOULD be from ValueSet Patient Education 2.16.840.1.113883.11.20.9.34
        code_val = self._get_instruction_code()
        code_system = self._get_code_system()
        display_name = self._get_display_name()

        code_elem = Code(
            code=code_val,
            system=code_system,
            display_name=display_name,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        act.append(code_elem)

        # Add status code (CONF:1098-7396, CONF:1098-19106)
        # SHALL be "completed"
        status_val = self._get_status()
        status_elem = StatusCode(status_val).to_element()
        act.append(status_elem)

        # Add text element with instruction content
        text_content = self._get_instruction_text()
        if text_content:
            text = etree.SubElement(act, f"{{{NS}}}text")
            text.text = text_content

        return act

    def _add_ids(self, act: etree._Element) -> None:
        """
        Add ID elements to act.

        Args:
            act: act element
        """
        # Add persistent ID if available
        if hasattr(self.instruction, "persistent_id") and self.instruction.persistent_id:
            pid = self.instruction.persistent_id
            id_elem = Identifier(root=pid.root, extension=pid.extension).to_element()
            act.append(id_elem)
        elif hasattr(self.instruction, "id") and self.instruction.id:
            # Use the id property
            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(self.instruction.id),
            ).to_element()
            act.append(id_elem)
        else:
            # Add a generated ID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            act.append(id_elem)

    def _get_instruction_code(self) -> str:
        """
        Get instruction code.

        Returns:
            Instruction code (defaults to SNOMED "Education" if not provided)
        """
        if hasattr(self.instruction, "code") and self.instruction.code:
            return self.instruction.code
        # Default to "Education" (SNOMED)
        return "409073007"

    def _get_code_system(self) -> str:
        """
        Get code system for instruction code.

        Returns:
            Code system (defaults to SNOMED)
        """
        if hasattr(self.instruction, "code_system") and self.instruction.code_system:
            return self.instruction.code_system
        return "SNOMED"

    def _get_display_name(self) -> str:
        """
        Get display name for instruction code.

        Returns:
            Display name
        """
        if hasattr(self.instruction, "display_name") and self.instruction.display_name:
            return self.instruction.display_name
        return "Education"

    def _get_status(self) -> str:
        """
        Get status code.

        Returns:
            Status code (must be "completed" per specification)
        """
        if hasattr(self.instruction, "status") and self.instruction.status:
            return self.instruction.status
        return "completed"

    def _get_instruction_text(self) -> str:
        """
        Get instruction text content.

        Supports both 'text' and 'instruction_text' properties for backward compatibility.

        Returns:
            Instruction text content
        """
        # Try 'text' property first (from instruction.py protocol)
        if hasattr(self.instruction, "text"):
            return self.instruction.text
        # Fall back to 'instruction_text' (from plan_of_treatment.py protocol)
        if hasattr(self.instruction, "instruction_text"):
            return self.instruction.instruction_text
        return ""
