"""Functional Status Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.functional_status import FunctionalStatusOrganizer
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.functional_status import FunctionalStatusOrganizerProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class FunctionalStatusSection(CDAElement):
    """
    Builder for C-CDA Functional Status Section.

    Contains observations and assessments of a patient's physical abilities,
    including Activities of Daily Living (ADLs), Instrumental Activities of
    Daily Living (IADLs), mobility, self-care, and problems that impact function.

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.

    Conformance: Template 2.16.840.1.113883.10.20.22.2.14
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.14",
                extension="2014-06-09",
                description="Functional Status Section R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.14",
                extension="2014-06-09",
                description="Functional Status Section R2.0",
            ),
        ],
    }

    # LOINC code for section per CONF:1098-14578, CONF:1098-14579
    SECTION_CODE = "47420-5"  # Functional Status

    def __init__(
        self,
        organizers: Sequence[FunctionalStatusOrganizerProtocol],
        title: str = "Functional Status",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize FunctionalStatusSection builder.

        Args:
            organizers: List of functional status organizers
            title: Section title (default: "Functional Status")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.organizers = organizers
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Functional Status Section XML element.

        Implements conformance rules:
        - CONF:1098-7920, CONF:1098-10389, CONF:1098-32567: templateId
        - CONF:1098-14578, CONF:1098-14579, CONF:1098-30866: code
        - CONF:1098-7922: title
        - CONF:1098-7923: text (narrative)
        - CONF:1098-14414, CONF:1098-14415: entry with organizer (optional)

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # CONF:1098-7920, CONF:1098-10389, CONF:1098-32567: Add template IDs
        self.add_template_ids(section)

        # CONF:1098-14578, CONF:1098-14579, CONF:1098-30866: Add section code
        code_elem = Code(
            code=self.SECTION_CODE,
            system="LOINC",
            display_name="Functional Status",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # CONF:1098-7922: Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # CONF:1098-7923: Add narrative text (HTML table)
        self._add_narrative(section)

        # CONF:1098-14414, CONF:1098-14415: Add entries with organizers
        for organizer in self.organizers:
            self._add_entry(section, organizer)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        CONF:1098-7923: SHALL contain exactly one [1..1] text

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.organizers:
            # No functional status data - add "No functional status recorded" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No functional status recorded"
            return

        # Create table for functional status
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Category",
            "Functional Status",
            "Value",
            "Date/Time",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for org_idx, organizer in enumerate(self.organizers, start=1):
            for obs_idx, observation in enumerate(organizer.observations, start=1):
                tr = etree.SubElement(tbody, f"{{{NS}}}tr")

                # Category
                td_category = etree.SubElement(tr, f"{{{NS}}}td")
                td_category.text = organizer.category

                # Functional Status type (with ID reference)
                td_type = etree.SubElement(tr, f"{{{NS}}}td")
                content = etree.SubElement(
                    td_type,
                    f"{{{NS}}}content",
                    ID=f"funcstatus-{org_idx}-{obs_idx}",
                )
                content.text = observation.type

                # Value
                td_value = etree.SubElement(tr, f"{{{NS}}}td")
                td_value.text = observation.value

                # Date/Time
                td_date = etree.SubElement(tr, f"{{{NS}}}td")
                td_date.text = observation.date.strftime("%Y-%m-%d %H:%M")

    def _add_entry(
        self, section: etree._Element, organizer: FunctionalStatusOrganizerProtocol
    ) -> None:
        """
        Add entry element with Functional Status Organizer.

        CONF:1098-14414: MAY contain zero or more [0..*] entry
        CONF:1098-14415: SHALL contain Functional Status Organizer

        Args:
            section: section element
            organizer: Functional status organizer data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Functional Status Organizer
        organizer_builder = FunctionalStatusOrganizer(organizer, version=self.version)
        entry.append(organizer_builder.to_element())
