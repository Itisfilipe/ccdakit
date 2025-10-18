"""Social History Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.smoking_status import SmokingStatusObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.social_history import SmokingStatusProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class SocialHistorySection(CDAElement):
    """
    Builder for C-CDA Social History Section.

    Contains social history data that influence a patient's physical, psychological
    or emotional health (e.g., smoking status, pregnancy). This implementation focuses
    on smoking status observations as specified in Meaningful Use requirements.

    Template: 2.16.840.1.113883.10.20.22.2.17 (V3: 2015-08-01)
    Code: 29762-2 (Social History) from LOINC

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 (2015-08-01) and R2.0 (2015-08-01) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.17",
                extension="2015-08-01",
                description="Social History Section (V3) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.17",
                extension="2015-08-01",
                description="Social History Section (V3) R2.0",
            ),
        ],
    }

    # LOINC code for social history section
    SOCIAL_HISTORY_CODE = "29762-2"
    SOCIAL_HISTORY_DISPLAY = "Social History"

    def __init__(
        self,
        smoking_statuses: Sequence[SmokingStatusProtocol],
        title: str = "Social History",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize SocialHistorySection builder.

        Args:
            smoking_statuses: List of smoking status observations
            title: Section title (default: "Social History")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.smoking_statuses = smoking_statuses
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Social History Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs
        self.add_template_ids(section)

        # Add section code (29762-2 = Social History)
        code_elem = Code(
            code=self.SOCIAL_HISTORY_CODE,
            system="LOINC",
            display_name=self.SOCIAL_HISTORY_DISPLAY,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table)
        self._add_narrative(section)

        # Add entries with Smoking Status Observations
        for status in self.smoking_statuses:
            self._add_entry(section, status)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.smoking_statuses:
            # No smoking status - add "No social history information available" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No social history information available"
            return

        # Create table for smoking status
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Social History Type",
            "Status",
            "Date Observed",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, status in enumerate(self.smoking_statuses, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Social History Type
            td_type = etree.SubElement(tr, f"{{{NS}}}td")
            td_type.text = "Smoking Status"

            # Status (with ID reference)
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_status,
                f"{{{NS}}}content",
                ID=f"smoking-status-{idx}",
            )
            content.text = status.smoking_status

            # Date Observed
            td_date = etree.SubElement(tr, f"{{{NS}}}td")
            # Format date/datetime appropriately
            if hasattr(status.date, "strftime"):
                if hasattr(status.date, "hour"):
                    # It's a datetime
                    td_date.text = status.date.strftime("%Y-%m-%d %H:%M")
                else:
                    # It's a date
                    td_date.text = status.date.strftime("%Y-%m-%d")
            else:
                td_date.text = str(status.date)

    def _add_entry(self, section: etree._Element, status: SmokingStatusProtocol) -> None:
        """
        Add entry element with Smoking Status Observation.

        Args:
            section: section element
            status: Smoking status data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Smoking Status Observation
        obs_builder = SmokingStatusObservation(status, version=self.version)
        entry.append(obs_builder.to_element())
