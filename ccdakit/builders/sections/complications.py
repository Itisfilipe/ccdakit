"""Complications Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.problem import ProblemObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.complication import ComplicationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class ComplicationsSection(CDAElement):
    """
    Builder for C-CDA Complications Section.

    This section contains problems that occurred during or around the time of a procedure.
    The complications may be known risks or unanticipated problems.

    Includes narrative (HTML table) and structured entries using Problem Observations.
    Supports R2.1 (2015-08-01) version.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.37",
                extension="2015-08-01",
                description="Complications Section (V3) R2.1",
            ),
        ],
    }

    def __init__(
        self,
        complications: Sequence[ComplicationProtocol],
        title: str = "Complications",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ComplicationsSection builder.

        Args:
            complications: List of complications satisfying ComplicationProtocol
            title: Section title (default: "Complications")
            version: C-CDA version (R2.1)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.complications = complications
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Complications Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs
        self.add_template_ids(section)

        # Add section code (55109-3 = Complications)
        code_elem = Code(
            code="55109-3",
            system="LOINC",
            display_name="Complications",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table)
        self._add_narrative(section)

        # Add entries with Problem Observations
        for complication in self.complications:
            self._add_entry(section, complication)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.complications:
            # No complications - add "No complications" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No complications"
            return

        # Create table for complications
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = ["Complication", "Code", "Severity", "Status", "Onset Date", "Resolved Date"]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, complication in enumerate(self.complications, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Complication name (with ID reference)
            td_name = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_name,
                f"{{{NS}}}content",
                ID=f"complication-{idx}",
            )
            content.text = complication.name

            # Code
            td_code = etree.SubElement(tr, f"{{{NS}}}td")
            td_code.text = f"{complication.code} ({complication.code_system})"

            # Severity
            td_severity = etree.SubElement(tr, f"{{{NS}}}td")
            if complication.severity:
                td_severity.text = complication.severity.capitalize()
            else:
                td_severity.text = "Not specified"

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            td_status.text = complication.status.capitalize()

            # Onset date
            td_onset = etree.SubElement(tr, f"{{{NS}}}td")
            if complication.onset_date:
                td_onset.text = complication.onset_date.strftime("%Y-%m-%d")
            else:
                td_onset.text = "Unknown"

            # Resolved date
            td_resolved = etree.SubElement(tr, f"{{{NS}}}td")
            if complication.resolved_date:
                td_resolved.text = complication.resolved_date.strftime("%Y-%m-%d")
            else:
                td_resolved.text = "Ongoing" if complication.status == "active" else "Unknown"

    def _add_entry(self, section: etree._Element, complication: ComplicationProtocol) -> None:
        """
        Add entry element with Problem Observation.

        According to the C-CDA specification, complications are represented using
        Problem Observation entries (2.16.840.1.113883.10.20.22.4.4).

        Args:
            section: section element
            complication: Complication data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Problem Observation
        # Complications use Problem Observation directly, not wrapped in Concern Act
        obs_builder = ProblemObservation(complication, version=self.version)
        entry.append(obs_builder.to_element())
