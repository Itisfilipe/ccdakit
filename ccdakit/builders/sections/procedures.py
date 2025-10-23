"""Procedures Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.procedure import ProcedureActivity
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.procedure import ProcedureProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class ProceduresSection(CDAElement):
    """
    Builder for C-CDA Procedures Section.

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 (2015-08-01) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.7.1",
                extension="2015-08-01",
                description="Procedures Section (entries required) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.7.1",
                extension="2014-06-09",
                description="Procedures Section (entries required) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        procedures: Sequence[ProcedureProtocol],
        title: str = "Procedures",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ProceduresSection builder.

        Args:
            procedures: List of procedures satisfying ProcedureProtocol
            title: Section title (default: "Procedures")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.procedures = procedures
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Procedures Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs
        self.add_template_ids(section)

        # Add section code (47519-4 = History of Procedures)
        code_elem = Code(
            code="47519-4",
            system="LOINC",
            display_name="History of Procedures",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table)
        self._add_narrative(section)

        # Add entries with Procedure Activities
        for procedure in self.procedures:
            self._add_entry(section, procedure)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.procedures:
            # No procedures - add "No procedures recorded" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No procedures recorded"
            return

        # Create table for procedures
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Procedure",
            "Code",
            "Date",
            "Status",
            "Target Site",
            "Performer",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, procedure in enumerate(self.procedures, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Procedure name (with ID reference)
            td_name = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_name,
                f"{{{NS}}}content",
                ID=f"procedure-{idx}",
            )
            content.text = procedure.name

            # Code
            td_code = etree.SubElement(tr, f"{{{NS}}}td")
            td_code.text = f"{procedure.code} ({procedure.code_system})"

            # Date
            td_date = etree.SubElement(tr, f"{{{NS}}}td")
            if procedure.date:
                # Format based on whether it's a date or datetime
                if hasattr(procedure.date, "hour"):
                    # It's a datetime
                    td_date.text = procedure.date.strftime("%Y-%m-%d %H:%M")
                else:
                    # It's a date
                    td_date.text = procedure.date.strftime("%Y-%m-%d")
            else:
                td_date.text = "Unknown"

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            td_status.text = procedure.status.capitalize()

            # Target site
            td_site = etree.SubElement(tr, f"{{{NS}}}td")
            if procedure.target_site:
                td_site.text = procedure.target_site
            else:
                td_site.text = "-"

            # Performer
            td_performer = etree.SubElement(tr, f"{{{NS}}}td")
            if procedure.performer_name:
                td_performer.text = procedure.performer_name
            else:
                td_performer.text = "-"

    def _add_entry(self, section: etree._Element, procedure: ProcedureProtocol) -> None:
        """
        Add entry element with Procedure Activity.

        Args:
            section: section element
            procedure: Procedure data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry", typeCode="DRIV")

        # Create and add Procedure Activity
        proc_builder = ProcedureActivity(procedure, version=self.version)
        entry.append(proc_builder.to_element())
