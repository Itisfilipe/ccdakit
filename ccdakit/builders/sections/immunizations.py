"""Immunizations Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.immunization import ImmunizationActivity
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.immunization import ImmunizationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class ImmunizationsSection(CDAElement):
    """
    Builder for C-CDA Immunizations Section.

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 (2015-08-01) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.2.1",
                extension="2015-08-01",
                description="Immunizations Section (entries required) R2.1",
            ),
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.2",
                extension="2015-08-01",
                description="Immunizations Section (entries optional) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.2.1",
                extension="2014-06-09",
                description="Immunizations Section (entries required) R2.0",
            ),
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.2",
                extension="2014-06-09",
                description="Immunizations Section (entries optional) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        immunizations: Sequence[ImmunizationProtocol],
        title: str = "Immunizations",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ImmunizationsSection builder.

        Args:
            immunizations: List of immunizations satisfying ImmunizationProtocol
            title: Section title (default: "Immunizations")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.immunizations = immunizations
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Immunizations Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs
        self.add_template_ids(section)

        # Add section code (11369-6 = History of Immunization Narrative)
        code_elem = Code(
            code="11369-6",
            system="LOINC",
            display_name="History of Immunization Narrative",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table)
        self._add_narrative(section)

        # Add entries with Immunization Activities
        for immunization in self.immunizations:
            self._add_entry(section, immunization)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.immunizations:
            # No immunizations - add "No known immunizations" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No known immunizations"
            return

        # Create table for immunizations
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Vaccine",
            "Date",
            "Status",
            "Lot Number",
            "Manufacturer",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, immunization in enumerate(self.immunizations, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Vaccine name (with ID reference)
            td_name = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_name,
                f"{{{NS}}}content",
                ID=f"immunization-{idx}",
            )
            content.text = immunization.vaccine_name

            # Administration date
            td_date = etree.SubElement(tr, f"{{{NS}}}td")
            td_date.text = immunization.administration_date.strftime("%Y-%m-%d")

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            td_status.text = immunization.status.capitalize()

            # Lot number
            td_lot = etree.SubElement(tr, f"{{{NS}}}td")
            if immunization.lot_number:
                td_lot.text = immunization.lot_number
            else:
                td_lot.text = "Not recorded"

            # Manufacturer
            td_manufacturer = etree.SubElement(tr, f"{{{NS}}}td")
            if immunization.manufacturer:
                td_manufacturer.text = immunization.manufacturer
            else:
                td_manufacturer.text = "Not recorded"

    def _add_entry(self, section: etree._Element, immunization: ImmunizationProtocol) -> None:
        """
        Add entry element with Immunization Activity.

        Args:
            section: section element
            immunization: Immunization data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry", typeCode="DRIV")

        # Create and add Immunization Activity
        imm_builder = ImmunizationActivity(immunization, version=self.version)
        entry.append(imm_builder.to_element())
