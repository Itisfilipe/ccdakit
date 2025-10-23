"""Advance Directives Section builder for C-CDA documents."""

from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.advance_directive import AdvanceDirectiveObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.advance_directive import AdvanceDirectiveProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class AdvanceDirectivesSection(CDAElement):
    """
    Builder for C-CDA Advance Directives Section (entries required).

    Contains advance directives data and references to supporting documentation,
    including living wills, healthcare proxies, and CPR/resuscitation status.
    Supports both R2.1 (2015-08-01) and R2.0 (2015-08-01) versions.

    Template ID: 2.16.840.1.113883.10.20.22.2.21.1
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.21.1",
                extension="2015-08-01",
                description="Advance Directives Section (entries required) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.21.1",
                extension="2015-08-01",
                description="Advance Directives Section (entries required) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        directives: Optional[Sequence[AdvanceDirectiveProtocol]] = None,
        title: str = "Advance Directives",
        null_flavor: Optional[str] = None,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize AdvanceDirectivesSection builder.

        Args:
            directives: List of advance directives (None or empty for no information)
            title: Section title (default: "Advance Directives")
            null_flavor: NullFlavor if no information available (e.g., "NI")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.directives = directives if directives is not None else []
        self.title = title
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        """
        Build Advance Directives Section XML element.

        Conformance rules implemented:
        - CONF:1198-32800: MAY contain @nullFlavor="NI"
        - CONF:1198-30227: SHALL contain templateId
        - CONF:1198-30228: templateId/@root="2.16.840.1.113883.10.20.22.2.21.1"
        - CONF:1198-32512: templateId/@extension="2015-08-01"
        - CONF:1198-32929: SHALL contain code
        - CONF:1198-32930: code/@code="42348-3"
        - CONF:1198-32931: code/@codeSystem=LOINC
        - CONF:1198-32932: SHALL contain title
        - CONF:1198-32933: SHALL contain text
        - CONF:1198-30235: If not nullFlavor, SHALL contain entry
        - CONF:1198-30236: entry MAY contain Advance Directive Observation
        - CONF:1198-32420: entry MAY contain Advance Directive Organizer
        - CONF:1198-32881: entry SHALL contain one or more entries with
                           EITHER observation OR organizer

        Returns:
            lxml Element for section
        """
        # Create section element (CONF:1198-32800)
        section = etree.Element(f"{{{NS}}}section")
        if self.null_flavor:
            section.set("nullFlavor", self.null_flavor)

        # Add template IDs (CONF:1198-30227, 30228, 32512)
        self.add_template_ids(section)

        # Add section code (CONF:1198-32929, 32930, 32931)
        code_elem = Code(
            code="42348-3",
            system="LOINC",
            display_name="Advance Directives",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1198-32932)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:1198-32933)
        self._add_narrative(section)

        # Add entries if not nullFlavor (CONF:1198-30235, 30236, 32420, 32881)
        if not self.null_flavor:
            for directive in self.directives:
                self._add_entry(section, directive)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if self.null_flavor or not self.directives:
            # No information or no directives
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            if self.null_flavor == "NI":
                paragraph.text = "No information about advance directives"
            else:
                paragraph.text = "No advance directives on file"
            return

        # Create table for advance directives
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Type",
            "Directive",
            "Start Date",
            "End Date",
            "Custodian",
            "Verification",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, directive in enumerate(self.directives, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Directive type (with ID reference)
            td_type = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_type,
                f"{{{NS}}}content",
                ID=f"directive-{idx}",
            )
            content.text = directive.directive_type

            # Directive value/details
            td_value = etree.SubElement(tr, f"{{{NS}}}td")
            if directive.document_url:
                # Create link if URL available
                link = etree.SubElement(
                    td_value,
                    f"{{{NS}}}linkHtml",
                    href=directive.document_url,
                )
                link.text = directive.directive_value
            else:
                td_value.text = directive.directive_value

            # Start date
            td_start = etree.SubElement(tr, f"{{{NS}}}td")
            if directive.start_date:
                td_start.text = directive.start_date.strftime("%Y-%m-%d")
            else:
                td_start.text = "Unknown"

            # End date
            td_end = etree.SubElement(tr, f"{{{NS}}}td")
            if directive.end_date:
                td_end.text = directive.end_date.strftime("%Y-%m-%d")
            else:
                td_end.text = "N/A"

            # Custodian
            td_custodian = etree.SubElement(tr, f"{{{NS}}}td")
            if directive.custodian_name:
                custodian_text = directive.custodian_name
                if directive.custodian_relationship:
                    custodian_text += f" ({directive.custodian_relationship})"
                td_custodian.text = custodian_text
            else:
                td_custodian.text = "Not specified"

            # Verification
            td_verification = etree.SubElement(tr, f"{{{NS}}}td")
            if directive.verifier_name or directive.verification_date:
                verification_text = ""
                if directive.verifier_name:
                    verification_text = directive.verifier_name
                if directive.verification_date:
                    date_str = directive.verification_date.strftime("%Y-%m-%d")
                    verification_text += f" on {date_str}" if verification_text else date_str
                td_verification.text = verification_text
            else:
                td_verification.text = "Not verified"

    def _add_entry(self, section: etree._Element, directive: AdvanceDirectiveProtocol) -> None:
        """
        Add entry element with Advance Directive Observation.

        Note: This implementation creates individual observations.
        The spec also allows for Advance Directive Organizer (template
        2.16.840.1.113883.10.20.22.4.108) which groups multiple observations,
        but for simplicity we create individual observations per entry.

        Args:
            section: section element
            directive: Advance directive data
        """
        # Create entry element (CONF:1198-30235)
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Advance Directive Observation (CONF:1198-30236)
        directive_builder = AdvanceDirectiveObservation(directive, version=self.version)
        entry.append(directive_builder.to_element())
