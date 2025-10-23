"""Anesthesia Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.anesthesia_entry import AnesthesiaProcedure
from ccdakit.builders.entries.medication import MedicationActivity
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.anesthesia import AnesthesiaProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class AnesthesiaSection(CDAElement):
    """
    Builder for C-CDA Anesthesia Section.

    Records the type of anesthesia (e.g., general, local, regional) and may state
    the actual agents used. This may be a subsection of the Procedure Description
    Section. The full details of anesthesia are usually found in a separate
    Anesthesia Note.

    Includes narrative (HTML table) and structured entries with:
    - Procedure Activity Procedure (V2) - for anesthesia type/procedure
    - Medication Activity (V2) - for anesthesia agents/medications

    Supports R2.1 version (2014-06-09).

    Template ID: 2.16.840.1.113883.10.20.22.2.25 (2014-06-09)
    LOINC Code: 59774-0 (Anesthesia)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.25",
                extension="2014-06-09",
                description="Anesthesia Section (V2) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.25",
                extension="2014-06-09",
                description="Anesthesia Section (V2) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        anesthesia_records: Sequence[AnesthesiaProtocol],
        title: str = "Anesthesia",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize AnesthesiaSection builder.

        Args:
            anesthesia_records: List of anesthesia data satisfying AnesthesiaProtocol
            title: Section title (default: "Anesthesia")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.anesthesia_records = anesthesia_records
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Anesthesia Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs
        self.add_template_ids(section)

        # Add section code (59774-0 = Anesthesia)
        code_elem = Code(
            code="59774-0",
            system="LOINC",
            display_name="Anesthesia",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table)
        self._add_narrative(section)

        # Add entries with Anesthesia Procedures and Medications
        for anesthesia in self.anesthesia_records:
            # Add anesthesia procedure entry
            self._add_procedure_entry(section, anesthesia)

            # Add medication entries if anesthesia agents are provided
            if anesthesia.anesthesia_agents:
                for agent in anesthesia.anesthesia_agents:
                    self._add_medication_entry(section, agent)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.anesthesia_records:
            # No anesthesia records - add "No anesthesia recorded" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No anesthesia recorded"
            return

        # Create table for anesthesia records
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Anesthesia Type",
            "Code",
            "Status",
            "Start Time",
            "End Time",
            "Route",
            "Agents",
            "Performer",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, anesthesia in enumerate(self.anesthesia_records, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Anesthesia type (with ID reference)
            td_type = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_type,
                f"{{{NS}}}content",
                ID=f"anesthesia-{idx}",
            )
            content.text = anesthesia.anesthesia_type

            # Code
            td_code = etree.SubElement(tr, f"{{{NS}}}td")
            td_code.text = f"{anesthesia.anesthesia_code} ({anesthesia.anesthesia_code_system})"

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            td_status.text = anesthesia.status.capitalize()

            # Start time
            td_start = etree.SubElement(tr, f"{{{NS}}}td")
            if anesthesia.start_time:
                # Format based on whether it's a date or datetime
                if hasattr(anesthesia.start_time, "hour"):
                    # It's a datetime
                    td_start.text = anesthesia.start_time.strftime("%Y-%m-%d %H:%M")
                else:
                    # It's a date
                    td_start.text = anesthesia.start_time.strftime("%Y-%m-%d")
            else:
                td_start.text = "-"

            # End time
            td_end = etree.SubElement(tr, f"{{{NS}}}td")
            if anesthesia.end_time:
                # Format based on whether it's a date or datetime
                if hasattr(anesthesia.end_time, "hour"):
                    # It's a datetime
                    td_end.text = anesthesia.end_time.strftime("%Y-%m-%d %H:%M")
                else:
                    # It's a date
                    td_end.text = anesthesia.end_time.strftime("%Y-%m-%d")
            else:
                td_end.text = "-"

            # Route
            td_route = etree.SubElement(tr, f"{{{NS}}}td")
            if anesthesia.route:
                td_route.text = anesthesia.route
            else:
                td_route.text = "-"

            # Agents/medications
            td_agents = etree.SubElement(tr, f"{{{NS}}}td")
            if anesthesia.anesthesia_agents:
                agents_list = [agent.name for agent in anesthesia.anesthesia_agents]
                td_agents.text = ", ".join(agents_list)
            else:
                td_agents.text = "-"

            # Performer
            td_performer = etree.SubElement(tr, f"{{{NS}}}td")
            if anesthesia.performer_name:
                td_performer.text = anesthesia.performer_name
            else:
                td_performer.text = "-"

    def _add_procedure_entry(self, section: etree._Element, anesthesia: AnesthesiaProtocol) -> None:
        """
        Add entry element with Procedure Activity for anesthesia type.

        Args:
            section: section element
            anesthesia: Anesthesia data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry", typeCode="DRIV")

        # Create and add Anesthesia Procedure Activity
        proc_builder = AnesthesiaProcedure(anesthesia, version=self.version)
        entry.append(proc_builder.to_element())

    def _add_medication_entry(self, section: etree._Element, medication) -> None:
        """
        Add entry element with Medication Activity for anesthesia agent.

        Args:
            section: section element
            medication: Medication data (anesthesia agent)
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry", typeCode="DRIV")

        # Create and add Medication Activity
        med_builder = MedicationActivity(medication, version=self.version)
        entry.append(med_builder.to_element())
