"""Health Concerns Section builder for C-CDA documents."""

from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.health_concern import HealthConcernAct
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.health_concern import HealthConcernProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class HealthConcernsSection(CDAElement):
    """
    Builder for C-CDA Health Concerns Section (V2).

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 (2015-08-01) and R2.0 (2015-08-01) versions.

    Per spec (2.16.840.1.113883.10.20.22.2.58):
    - code="75310-3" Health concerns document from LOINC (CONF:1198-28806)
    - SHALL contain title (CONF:1198-28809)
    - SHALL contain text (CONF:1198-28810)
    - If section/@nullFlavor is not present, SHALL contain at least one
      Health Concern Act entry (CONF:1198-30768)
    - MAY contain nullFlavor="NI" (CONF:1198-32802)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.58",
                extension="2015-08-01",
                description="Health Concerns Section V2",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.58",
                extension="2015-08-01",
                description="Health Concerns Section V2",
            ),
        ],
    }

    def __init__(
        self,
        health_concerns: Sequence[HealthConcernProtocol],
        title: str = "Health Concerns",
        null_flavor: Optional[str] = None,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize HealthConcernsSection builder.

        Args:
            health_concerns: List of health concerns satisfying HealthConcernProtocol
            title: Section title (default: "Health Concerns")
            null_flavor: Optional null flavor (e.g., "NI") if no information available
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.health_concerns = health_concerns
        self.title = title
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        """
        Build Health Concerns Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add nullFlavor if specified (CONF:1198-32802)
        if self.null_flavor:
            section.set("nullFlavor", self.null_flavor)

        # Add template IDs (CONF:1198-28804)
        self.add_template_ids(section)

        # Add section code (75310-3 = Health concerns document) (CONF:1198-28806)
        code_elem = Code(
            code="75310-3",
            system="LOINC",
            display_name="Health concerns document",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1198-28809)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table) (CONF:1198-28810)
        self._add_narrative(section)

        # Add entries with Health Concern Acts (CONF:1198-30768)
        # If nullFlavor is not present, SHALL contain at least one entry
        if not self.null_flavor:
            for health_concern in self.health_concerns:
                self._add_entry(section, health_concern)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if self.null_flavor or not self.health_concerns:
            # No health concerns - add "No health concerns" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            if self.null_flavor == "NI":
                paragraph.text = "No information available"
            else:
                paragraph.text = "No health concerns"
            return

        # Create table for health concerns
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Health Concern",
            "Status",
            "Effective Time",
            "Related Observations",
            "Concern Type",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, concern in enumerate(self.health_concerns, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Health concern name (with ID reference)
            td_name = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_name,
                f"{{{NS}}}content",
                ID=f"health-concern-{idx}",
            )
            content.text = concern.name

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            td_status.text = concern.status.capitalize()

            # Effective time
            td_time = etree.SubElement(tr, f"{{{NS}}}td")
            if concern.effective_time_low:
                time_str = concern.effective_time_low.strftime("%Y-%m-%d")
                if concern.effective_time_high:
                    time_str += f" to {concern.effective_time_high.strftime('%Y-%m-%d')}"
                else:
                    time_str += " - Ongoing"
                td_time.text = time_str
            else:
                td_time.text = "Unknown"

            # Related observations
            td_observations = etree.SubElement(tr, f"{{{NS}}}td")
            if concern.observations:
                obs_list = etree.SubElement(td_observations, f"{{{NS}}}list")
                for obs in concern.observations:
                    item = etree.SubElement(obs_list, f"{{{NS}}}item")
                    item.text = f"{obs.display_name} ({obs.observation_type})"
            else:
                td_observations.text = "None"

            # Concern type (patient vs provider)
            td_type = etree.SubElement(tr, f"{{{NS}}}td")
            td_type.text = "Patient" if concern.author_is_patient else "Provider"

    def _add_entry(self, section: etree._Element, health_concern: HealthConcernProtocol) -> None:
        """
        Add entry element with Health Concern Act.

        Per CONF:1198-30768, SHALL contain at least one [1..*] entry
        such that it SHALL contain exactly one [1..1] Health Concern Act (V2).

        Args:
            section: section element
            health_concern: Health concern data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Health Concern Act
        act_builder = HealthConcernAct(health_concern, version=self.version)
        entry.append(act_builder.to_element())
