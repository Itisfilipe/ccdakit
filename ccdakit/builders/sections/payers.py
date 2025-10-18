"""Payers Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.coverage_activity import CoverageActivity
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.payer import PayerProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class PayersSection(CDAElement):
    """
    Builder for C-CDA Payers Section.

    The Payers Section contains data on the patient's payers, whether third party
    insurance, self-pay, other payer or guarantor. Each unique instance of a payer
    and all pertinent data needed to contact, bill to, and collect from that payer
    should be included.

    Includes narrative (HTML table) and structured entries (Coverage Activities).

    Conforms to:
    - Template ID: 2.16.840.1.113883.10.20.22.2.18 (Payers Section V3)
    - Extension: 2015-08-01
    - LOINC Code: 48768-6 "Payers"

    Supports both R2.1 and R2.0 versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.18",
                extension="2015-08-01",
                description="Payers Section (V3) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.18",
                extension="2015-08-01",
                description="Payers Section (V3) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        payers: Sequence[PayerProtocol],
        title: str = "Insurance Providers",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PayersSection builder.

        Args:
            payers: List of payers satisfying PayerProtocol
            title: Section title (default: "Insurance Providers")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.payers = payers
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Payers Section XML element.

        Conforms to all CONF rules from template 2.16.840.1.113883.10.20.22.2.18:
        - CONF:1198-7924/10434/32597: templateId
        - CONF:1198-15395/15396/32149: code="48768-6" Payers
        - CONF:1198-7926: title
        - CONF:1198-7927: text
        - CONF:1198-7959/15501: entry with Coverage Activity (SHOULD)

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:1198-7924, CONF:1198-10434, CONF:1198-32597)
        self.add_template_ids(section)

        # Add section code (CONF:1198-15395, CONF:1198-15396, CONF:1198-32149)
        code_elem = Code(
            code="48768-6",
            system="LOINC",
            display_name="Payers",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1198-7926)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table) (CONF:1198-7927)
        self._add_narrative(section)

        # Add entries with Coverage Activities (CONF:1198-7959, CONF:1198-15501)
        for payer in self.payers:
            self._add_entry(section, payer)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Generates a human-readable table of payer information.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.payers:
            # No payers - add "No insurance information" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No insurance information available"
            return

        # Create table for payers
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Payer Name",
            "Insurance Type",
            "Member ID",
            "Group Number",
            "Coverage Period",
            "Priority",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, payer in enumerate(self.payers, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Payer name (with ID reference)
            td_payer = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_payer,
                f"{{{NS}}}content",
                ID=f"payer-{idx}",
            )
            content.text = payer.payer_name

            # Insurance type
            td_type = etree.SubElement(tr, f"{{{NS}}}td")
            td_type.text = payer.insurance_type

            # Member ID
            td_member = etree.SubElement(tr, f"{{{NS}}}td")
            td_member.text = payer.member_id

            # Group number
            td_group = etree.SubElement(tr, f"{{{NS}}}td")
            td_group.text = payer.group_number if payer.group_number else "N/A"

            # Coverage period
            td_period = etree.SubElement(tr, f"{{{NS}}}td")
            if payer.start_date:
                period_text = payer.start_date.strftime("%Y-%m-%d")
                if payer.end_date:
                    period_text += f" to {payer.end_date.strftime('%Y-%m-%d')}"
                else:
                    period_text += " to present"
                td_period.text = period_text
            else:
                td_period.text = "Unknown"

            # Priority/sequence
            td_priority = etree.SubElement(tr, f"{{{NS}}}td")
            if payer.sequence_number is not None:
                priority_map = {1: "Primary", 2: "Secondary", 3: "Tertiary"}
                td_priority.text = priority_map.get(
                    payer.sequence_number, f"Priority {payer.sequence_number}"
                )
            else:
                td_priority.text = "Not specified"

    def _add_entry(self, section: etree._Element, payer: PayerProtocol) -> None:
        """
        Add entry element with Coverage Activity.

        Conforms to:
        - CONF:1198-7959: SHOULD contain entry
        - CONF:1198-15501: SHALL contain Coverage Activity

        Args:
            section: section element
            payer: Payer data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry", typeCode="DRIV")

        # Create and add Coverage Activity (CONF:1198-15501)
        coverage_builder = CoverageActivity(payer, version=self.version)
        entry.append(coverage_builder.to_element())
