"""Planned Act entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.assessment_and_plan import PlannedActProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class PlannedAct(CDAElement):
    """
    Builder for C-CDA Planned Act entry.

    Represents planned acts that are not classified as observations or procedures.
    Examples: dressing change, patient teaching, feeding, comfort measures.

    Template ID: 2.16.840.1.113883.10.20.22.4.39
    Version: 2014-06-09
    """

    # Template IDs - Only one version (R2.0 and R2.1 use the same template)
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.39",
                extension="2014-06-09",
                description="Planned Act (V2)",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.39",
                extension="2014-06-09",
                description="Planned Act (V2)",
            ),
        ],
    }

    def __init__(
        self,
        planned_act: PlannedActProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PlannedAct builder.

        Args:
            planned_act: Planned act data satisfying PlannedActProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.planned_act = planned_act

    def build(self) -> etree.Element:
        """
        Build Planned Act XML element.

        Conformance:
            - CONF:1098-8538: SHALL contain @classCode="ACT"
            - CONF:1098-8539: SHALL contain @moodCode from Planned moodCode value set
            - CONF:1098-30430, 30431, 32552: SHALL contain templateId
            - CONF:1098-8546: SHALL contain at least one [1..*] id
            - CONF:1098-31687: SHALL contain exactly one code
            - CONF:1098-30432, 32019: SHALL contain statusCode="active"
            - CONF:1098-30433: SHOULD contain effectiveTime
            - CONF:1098-32030: Code SHOULD be from LOINC or SNOMED CT

        Returns:
            lxml Element for act
        """
        # Create act element with required attributes (CONF:1098-8538, 1098-8539)
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode=self.planned_act.mood_code,
        )

        # Add template ID (CONF:1098-30430, 30431, 32552)
        self.add_template_ids(act)

        # Add ID (CONF:1098-8546)
        id_elem = Identifier(
            root=self.planned_act.id_root,
            extension=self.planned_act.id_extension,
        ).to_element()
        act.append(id_elem)

        # Add code (CONF:1098-31687, 32030)
        code_elem = Code(
            code=self.planned_act.code,
            system=self.planned_act.code_system,
            display_name=self.planned_act.display_name,
        ).to_element()
        act.append(code_elem)

        # Add statusCode="active" (CONF:1098-30432, 32019)
        status_elem = StatusCode("active").to_element()
        act.append(status_elem)

        # Add effectiveTime if provided (CONF:1098-30433)
        if self.planned_act.effective_time:
            time_elem = EffectiveTime(
                value=self.planned_act.effective_time,
            ).to_element()
            act.append(time_elem)

        # Add instructions as entryRelationship/act if provided
        if self.planned_act.instructions:
            self._add_instructions(act)

        return act

    def _add_instructions(self, act: etree._Element) -> None:
        """
        Add instructions as an entryRelationship with Instruction (V2) template.

        Per spec CONF:1098-32024, 32025, 32026:
        - MAY contain entryRelationship with typeCode="SUBJ"
        - SHALL contain Instruction (V2) template

        Args:
            act: Parent act element
        """
        entry_rel = etree.SubElement(
            act,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",
        )

        # Create instruction act (simplified version - full Instruction template
        # would be in a separate builder, but we implement inline for simplicity)
        instruction = etree.SubElement(
            entry_rel,
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="INT",
        )

        # Add Instruction (V2) template ID
        template_id = etree.SubElement(instruction, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.20")
        template_id.set("extension", "2014-06-09")

        # Add code for instruction
        code_elem = etree.SubElement(instruction, f"{{{NS}}}code")
        code_elem.set("code", "409073007")
        code_elem.set("codeSystem", "2.16.840.1.113883.6.96")
        code_elem.set("displayName", "instruction")

        # Add text with reference or direct text
        text_elem = etree.SubElement(instruction, f"{{{NS}}}text")
        text_elem.text = self.planned_act.instructions

        # Add statusCode
        status_elem = etree.SubElement(instruction, f"{{{NS}}}statusCode")
        status_elem.set("code", "completed")
