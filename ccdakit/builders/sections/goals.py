"""Goals Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.goal import GoalObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.goal import GoalProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class GoalsSection(CDAElement):
    """
    Builder for C-CDA Goals Section.

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 and R2.0 versions.

    Template ID: 2.16.840.1.113883.10.20.22.2.60
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.60",
                extension=None,  # No extension specified in spec
                description="Goals Section",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.60",
                extension=None,  # Same for R2.0
                description="Goals Section",
            ),
        ],
    }

    def __init__(
        self,
        goals: Sequence[GoalProtocol],
        title: str = "Goals",
        version: CDAVersion = CDAVersion.R2_1,
        null_flavor: str = None,
        **kwargs,
    ):
        """
        Initialize GoalsSection builder.

        Args:
            goals: List of goals satisfying GoalProtocol
            title: Section title (default: "Goals")
            version: C-CDA version (R2.1 or R2.0)
            null_flavor: Optional null flavor (e.g., "NI" for no information)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.goals = goals
        self.title = title
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        """
        Build Goals Section XML element.

        Returns:
            lxml Element for section
        """
        # Validate SHALL requirements (CONF:1098-30719)
        if not self.null_flavor and not self.goals:
            raise ValueError(
                "Goals Section SHALL contain at least one entry when nullFlavor is not present "
                "(CONF:1098-30719). Either provide goals or set null_flavor='NI'."
            )

        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add null flavor if specified (CONF:1098-32819)
        if self.null_flavor:
            section.set("nullFlavor", self.null_flavor)

        # Add template IDs (CONF:1098-29584, CONF:1098-29585)
        self.add_template_ids(section)

        # Add section code (CONF:1098-29586, CONF:1098-29587, CONF:1098-29588)
        # 61146-7 = Goals (LOINC)
        code_elem = Code(
            code="61146-7",
            system="LOINC",
            display_name="Goals",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1098-30721)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:1098-30722)
        self._add_narrative(section)

        # Add entries with Goal Observations (CONF:1098-30719, CONF:1098-30720)
        if self.goals:
            for goal in self.goals:
                self._add_entry(section, goal)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.goals:
            # No goals - add "No goals documented" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No goals documented"
            return

        # Create table for goals
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = ["Goal", "Status", "Start Date", "Target Date", "Value"]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, goal in enumerate(self.goals, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Goal description (with ID reference)
            td_desc = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_desc,
                f"{{{NS}}}content",
                ID=f"goal-{idx}",
            )
            content.text = goal.description

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            td_status.text = self._format_status(goal.status)

            # Start date
            td_start = etree.SubElement(tr, f"{{{NS}}}td")
            if goal.start_date:
                td_start.text = goal.start_date.strftime("%Y-%m-%d")
            else:
                td_start.text = "Not specified"

            # Target date
            td_target = etree.SubElement(tr, f"{{{NS}}}td")
            if goal.target_date:
                td_target.text = goal.target_date.strftime("%Y-%m-%d")
            else:
                td_target.text = "Not specified"

            # Value
            td_value = etree.SubElement(tr, f"{{{NS}}}td")
            if goal.value:
                if goal.value_unit:
                    td_value.text = f"{goal.value} {goal.value_unit}"
                else:
                    td_value.text = str(goal.value)
            else:
                td_value.text = "Not specified"

    def _add_entry(self, section: etree._Element, goal: GoalProtocol) -> None:
        """
        Add entry element with Goal Observation.

        Args:
            section: section element
            goal: Goal data
        """
        # Create entry element (SHALL contain at least one entry - CONF:1098-30719)
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Goal Observation (CONF:1098-30720)
        obs_builder = GoalObservation(goal, version=self.version)
        entry.append(obs_builder.to_element())

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
