"""Vital Signs Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.vital_signs import VitalSignsOrganizer
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.vital_signs import VitalSignsOrganizerProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class VitalSignsSection(CDAElement):
    """
    Builder for C-CDA Vital Signs Section.

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 (2015-08-01) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.4.1",
                extension="2015-08-01",
                description="Vital Signs Section (entries required) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.4.1",
                extension="2014-06-09",
                description="Vital Signs Section (entries required) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        vital_signs_organizers: Sequence[VitalSignsOrganizerProtocol],
        title: str = "Vital Signs",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize VitalSignsSection builder.

        Args:
            vital_signs_organizers: List of vital signs organizers
            title: Section title (default: "Vital Signs")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.vital_signs_organizers = vital_signs_organizers
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Vital Signs Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs
        self.add_template_ids(section)

        # Add section code (8716-3 = Vital signs)
        code_elem = Code(
            code="8716-3",
            system="LOINC",
            display_name="Vital signs",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table)
        self._add_narrative(section)

        # Add entries with Vital Signs Organizers
        for organizer in self.vital_signs_organizers:
            self._add_entry(section, organizer)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.vital_signs_organizers:
            # No vital signs - add "No vital signs recorded" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No vital signs recorded"
            return

        # Create table for vital signs
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Date/Time",
            "Vital Sign",
            "Value",
            "Unit",
            "Interpretation",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for organizer_idx, organizer in enumerate(self.vital_signs_organizers, start=1):
            for sign_idx, vital_sign in enumerate(organizer.vital_signs, start=1):
                tr = etree.SubElement(tbody, f"{{{NS}}}tr")

                # Date/Time
                td_date = etree.SubElement(tr, f"{{{NS}}}td")
                td_date.text = organizer.date.strftime("%Y-%m-%d %H:%M")

                # Vital Sign type (with ID reference)
                td_type = etree.SubElement(tr, f"{{{NS}}}td")
                content = etree.SubElement(
                    td_type,
                    f"{{{NS}}}content",
                    ID=f"vitalsign-{organizer_idx}-{sign_idx}",
                )
                content.text = vital_sign.type

                # Value
                td_value = etree.SubElement(tr, f"{{{NS}}}td")
                td_value.text = vital_sign.value

                # Unit
                td_unit = etree.SubElement(tr, f"{{{NS}}}td")
                td_unit.text = vital_sign.unit

                # Interpretation
                td_interpretation = etree.SubElement(tr, f"{{{NS}}}td")
                if vital_sign.interpretation:
                    td_interpretation.text = vital_sign.interpretation
                else:
                    td_interpretation.text = "-"

    def _add_entry(self, section: etree._Element, organizer: VitalSignsOrganizerProtocol) -> None:
        """
        Add entry element with Vital Signs Organizer.

        Args:
            section: section element
            organizer: Vital signs organizer data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry", typeCode="DRIV")

        # Create and add Vital Signs Organizer
        organizer_builder = VitalSignsOrganizer(organizer, version=self.version)
        entry.append(organizer_builder.to_element())
