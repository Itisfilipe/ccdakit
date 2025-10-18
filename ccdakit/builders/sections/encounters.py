"""Encounters Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.encounter import EncounterActivity
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.encounter import EncounterProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class EncountersSection(CDAElement):
    """
    Builder for C-CDA Encounters Section (entries required).

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 (2015-08-01) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.22.1",
                extension="2015-08-01",
                description="Encounters Section (entries required) V3",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.22.1",
                extension="2014-06-09",
                description="Encounters Section (entries required) V2",
            ),
        ],
    }

    def __init__(
        self,
        encounters: Sequence[EncounterProtocol],
        title: str = "Encounters",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize EncountersSection builder.

        Args:
            encounters: List of encounters satisfying EncounterProtocol
            title: Section title (default: "Encounters")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.encounters = encounters
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Encounters Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs
        self.add_template_ids(section)

        # Add section code (46240-8 = Encounters)
        code_elem = Code(
            code="46240-8",
            system="LOINC",
            display_name="Encounters",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table)
        self._add_narrative(section)

        # Add entries with Encounter Activities
        for encounter in self.encounters:
            self._add_entry(section, encounter)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.encounters:
            # No encounters - add "No encounters recorded" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No encounters recorded"
            return

        # Create table for encounters
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Encounter Type",
            "Code",
            "Date",
            "Location",
            "Performer",
            "Discharge Disposition",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, encounter in enumerate(self.encounters, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Encounter type (with ID reference)
            td_type = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_type,
                f"{{{NS}}}content",
                ID=f"encounter-{idx}",
            )
            content.text = encounter.encounter_type

            # Code
            td_code = etree.SubElement(tr, f"{{{NS}}}td")
            td_code.text = f"{encounter.code} ({encounter.code_system})"

            # Date
            td_date = etree.SubElement(tr, f"{{{NS}}}td")
            if encounter.date:
                # Format based on whether it's a date or datetime
                if hasattr(encounter.date, "hour"):
                    # It's a datetime
                    date_str = encounter.date.strftime("%Y-%m-%d %H:%M")
                else:
                    # It's a date
                    date_str = encounter.date.strftime("%Y-%m-%d")

                # Add end date if available
                if encounter.end_date:
                    if hasattr(encounter.end_date, "hour"):
                        end_str = encounter.end_date.strftime("%Y-%m-%d %H:%M")
                    else:
                        end_str = encounter.end_date.strftime("%Y-%m-%d")
                    td_date.text = f"{date_str} to {end_str}"
                else:
                    td_date.text = date_str
            else:
                td_date.text = "Unknown"

            # Location
            td_location = etree.SubElement(tr, f"{{{NS}}}td")
            if encounter.location:
                td_location.text = encounter.location
            else:
                td_location.text = "-"

            # Performer
            td_performer = etree.SubElement(tr, f"{{{NS}}}td")
            if encounter.performer_name:
                td_performer.text = encounter.performer_name
            else:
                td_performer.text = "-"

            # Discharge Disposition
            td_disposition = etree.SubElement(tr, f"{{{NS}}}td")
            if encounter.discharge_disposition:
                td_disposition.text = encounter.discharge_disposition
            else:
                td_disposition.text = "-"

    def _add_entry(self, section: etree._Element, encounter: EncounterProtocol) -> None:
        """
        Add entry element with Encounter Activity.

        Args:
            section: section element
            encounter: Encounter data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry", typeCode="DRIV")

        # Create and add Encounter Activity
        enc_builder = EncounterActivity(encounter, version=self.version)
        entry.append(enc_builder.to_element())
