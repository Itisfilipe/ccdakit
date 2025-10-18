"""Interventions Section builder for C-CDA documents."""

from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.intervention_act import InterventionAct
from ccdakit.builders.entries.planned_intervention_act import PlannedInterventionAct
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.intervention import (
    InterventionProtocol,
    PlannedInterventionProtocol,
)


# CDA namespace
NS = "urn:hl7-org:v3"


class InterventionsSection(CDAElement):
    """
    Builder for C-CDA Interventions Section (V3).

    This section represents interventions - actions taken to maximize the prospects
    of achieving the goals of care for the patient, including removal of barriers
    to success. Interventions can be planned, ordered, historical, etc.

    Interventions include actions that may be ongoing (e.g., maintenance medications,
    monitoring health status). Instructions are nested within interventions and may
    include self-care instructions.

    Template ID: 2.16.840.1.113883.10.20.21.2.3
    Release: 2015-08-01

    Supports both R2.1 and R2.0 versions.

    Conformance Rules:
    - SHALL contain templateId with root="2.16.840.1.113883.10.20.21.2.3" (CONF:1198-8680, CONF:1198-10461)
    - SHALL contain templateId extension="2015-08-01" (CONF:1198-32559)
    - SHALL contain code="62387-6" from LOINC (CONF:1198-15377, CONF:1198-15378, CONF:1198-30864)
    - SHALL contain title (CONF:1198-8682)
    - SHALL contain text (CONF:1198-8683)
    - SHOULD contain zero or more [0..*] entry with Intervention Act (CONF:1198-30996, CONF:1198-30997)
    - SHOULD contain zero or more [0..*] entry with Planned Intervention Act (CONF:1198-32730, CONF:1198-32731)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.21.2.3",
                extension="2015-08-01",
                description="Interventions Section (V3)",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.21.2.3",
                extension="2015-08-01",
                description="Interventions Section (V3)",
            ),
        ],
    }

    def __init__(
        self,
        interventions: Optional[Sequence[InterventionProtocol]] = None,
        planned_interventions: Optional[Sequence[PlannedInterventionProtocol]] = None,
        title: str = "Interventions",
        version: CDAVersion = CDAVersion.R2_1,
        null_flavor: str = None,
        **kwargs,
    ):
        """
        Initialize InterventionsSection builder.

        Args:
            interventions: List of completed interventions satisfying InterventionProtocol
            planned_interventions: List of planned interventions satisfying PlannedInterventionProtocol
            title: Section title (default: "Interventions")
            version: C-CDA version (R2.1 or R2.0)
            null_flavor: Optional null flavor (e.g., "NI" for no information)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.interventions = interventions or []
        self.planned_interventions = planned_interventions or []
        self.title = title
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        """
        Build Interventions Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add null flavor if specified
        if self.null_flavor:
            section.set("nullFlavor", self.null_flavor)

        # Add template IDs (CONF:1198-8680, CONF:1198-10461, CONF:1198-32559)
        self.add_template_ids(section)

        # Add section code (CONF:1198-15377, CONF:1198-15378, CONF:1198-30864)
        # 62387-6 = Interventions Provided (LOINC)
        code_elem = Code(
            code="62387-6",
            system="LOINC",
            display_name="Interventions Provided",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1198-8682)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:1198-8683)
        self._add_narrative(section)

        # Add entries with Intervention Acts (CONF:1198-30996, CONF:1198-30997)
        for intervention in self.interventions:
            self._add_intervention_entry(section, intervention)

        # Add entries with Planned Intervention Acts (CONF:1198-32730, CONF:1198-32731)
        for planned in self.planned_interventions:
            self._add_planned_intervention_entry(section, planned)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        # Collect all interventions
        all_interventions = []
        for intervention in self.interventions:
            all_interventions.append(("Completed", intervention))
        for planned in self.planned_interventions:
            all_interventions.append(("Planned", planned))

        if not all_interventions:
            # No interventions - add "No interventions documented" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No interventions documented"
            return

        # Create table for interventions
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = ["Type", "Description", "Status", "Date", "Goal Reference"]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, (intervention_type, intervention) in enumerate(all_interventions, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Type (Completed/Planned)
            td_type = etree.SubElement(tr, f"{{{NS}}}td")
            td_type.text = intervention_type

            # Description (with ID reference)
            td_desc = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_desc,
                f"{{{NS}}}content",
                ID=f"intervention-{idx}",
            )
            content.text = intervention.description

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            if hasattr(intervention, "status"):
                td_status.text = self._format_status(intervention.status)
            else:
                td_status.text = "Active" if intervention_type == "Planned" else "Completed"

            # Date
            td_date = etree.SubElement(tr, f"{{{NS}}}td")
            if hasattr(intervention, "effective_time") and intervention.effective_time:
                eff_time = intervention.effective_time
                if hasattr(eff_time, "strftime"):
                    td_date.text = eff_time.strftime("%Y-%m-%d")
                else:
                    td_date.text = str(eff_time)
            else:
                td_date.text = "Not specified"

            # Goal Reference
            td_goal = etree.SubElement(tr, f"{{{NS}}}td")
            if hasattr(intervention, "goal_reference_id") and intervention.goal_reference_id:
                td_goal.text = f"Goal: {intervention.goal_reference_id}"
            else:
                td_goal.text = "Not specified"

    def _add_intervention_entry(
        self,
        section: etree._Element,
        intervention: InterventionProtocol,
    ) -> None:
        """
        Add entry element with Intervention Act.

        Args:
            section: section element
            intervention: Intervention data
        """
        # Create entry element (SHOULD contain - CONF:1198-30996)
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Intervention Act (CONF:1198-30997)
        act_builder = InterventionAct(intervention, version=self.version)
        entry.append(act_builder.to_element())

    def _add_planned_intervention_entry(
        self,
        section: etree._Element,
        planned: PlannedInterventionProtocol,
    ) -> None:
        """
        Add entry element with Planned Intervention Act.

        Args:
            section: section element
            planned: Planned intervention data
        """
        # Create entry element (SHOULD contain - CONF:1198-32730)
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Planned Intervention Act (CONF:1198-32731)
        act_builder = PlannedInterventionAct(planned, version=self.version)
        entry.append(act_builder.to_element())

    def _format_status(self, status: str) -> str:
        """
        Format status for display in narrative.

        Args:
            status: Raw status string

        Returns:
            Formatted status string
        """
        # Capitalize and replace hyphens with spaces
        formatted = status.replace("-", " ").replace("_", " ")
        return formatted.title()
