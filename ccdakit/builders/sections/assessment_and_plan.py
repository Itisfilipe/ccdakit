"""Assessment and Plan Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.planned_act import PlannedAct
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.assessment_and_plan import AssessmentAndPlanItemProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class AssessmentAndPlanSection(CDAElement):
    """
    Builder for C-CDA Assessment and Plan Section (V2).

    This section represents the clinician's conclusions and working assumptions
    that will guide treatment of the patient. It may contain planned activities.

    Template ID: 2.16.840.1.113883.10.20.22.2.9
    Version: 2014-06-09

    The Assessment and Plan Section may be combined or separated to meet local
    policy requirements. See also:
    - Assessment Section: 2.16.840.1.113883.10.20.22.2.8
    - Plan of Treatment Section (V2): 2.16.840.1.113883.10.20.22.2.10
    """

    # Template IDs - Only one version (R2.0 and R2.1 use the same template)
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.9",
                extension="2014-06-09",
                description="Assessment and Plan Section (V2)",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.9",
                extension="2014-06-09",
                description="Assessment and Plan Section (V2)",
            ),
        ],
    }

    def __init__(
        self,
        items: Sequence[AssessmentAndPlanItemProtocol] = None,
        title: str = "Assessment and Plan",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize AssessmentAndPlanSection builder.

        Args:
            items: List of assessment/plan items satisfying AssessmentAndPlanItemProtocol.
                   Can be empty for narrative-only sections.
            title: Section title (default: "Assessment and Plan")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.items = items if items is not None else []
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Assessment and Plan Section XML element.

        Conformance:
            - CONF:1098-7705, 10381, 32583: SHALL contain templateId
            - CONF:1098-15353, 15354, 32141: SHALL contain code="51847-2"
            - CONF:1098-7707: SHALL contain text
            - CONF:1098-7708, 15448: MAY contain entry with Planned Act (V2)

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:1098-7705, 10381, 32583)
        self.add_template_ids(section)

        # Add section code (CONF:1098-15353, 15354, 32141)
        code_elem = Code(
            code="51847-2",
            system="LOINC",
            display_name="Assessment and Plan",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:1098-7707)
        self._add_narrative(section)

        # Add entries with Planned Acts (CONF:1098-7708, 15448)
        for item in self.items:
            if item.planned_act:
                self._add_entry(section, item.planned_act)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML content.

        The narrative can include both assessment findings and plan items.
        If no items are provided, generates a simple placeholder.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.items:
            # No items - add generic paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "Assessment and plan documented in clinical notes."
            return

        # Separate items by type
        assessments = [item for item in self.items if item.item_type == "assessment"]
        plans = [item for item in self.items if item.item_type == "plan"]

        # Add assessment section if present
        if assessments:
            self._add_narrative_section(text, "Assessment", assessments)

        # Add plan section if present
        if plans:
            self._add_narrative_section(text, "Plan", plans)

    def _add_narrative_section(
        self,
        text: etree._Element,
        heading: str,
        items: Sequence[AssessmentAndPlanItemProtocol],
    ) -> None:
        """
        Add a subsection (Assessment or Plan) to the narrative.

        Args:
            text: Parent text element
            heading: Section heading ("Assessment" or "Plan")
            items: List of items to include
        """
        # Add heading
        paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
        content = etree.SubElement(paragraph, f"{{{NS}}}content", styleCode="Bold")
        content.text = heading

        # Add items as a list
        list_elem = etree.SubElement(text, f"{{{NS}}}list", listType="unordered")

        for idx, item in enumerate(items, start=1):
            li = etree.SubElement(list_elem, f"{{{NS}}}item")
            content = etree.SubElement(li, f"{{{NS}}}content", ID=f"{heading.lower()}-{idx}")
            content.text = item.text

    def _add_entry(
        self,
        section: etree._Element,
        planned_act: "PlannedAct",
    ) -> None:
        """
        Add entry element with Planned Act.

        Per spec CONF:1098-7708, 15448:
        - MAY contain zero or more [0..*] entry
        - SHALL contain exactly one [1..1] Planned Act (V2)

        Args:
            section: section element
            planned_act: Planned act data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Planned Act
        act_builder = PlannedAct(planned_act, version=self.version)
        entry.append(act_builder.to_element())
