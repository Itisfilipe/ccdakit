"""Results Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.result import ResultOrganizer
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.result import ResultOrganizerProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class ResultsSection(CDAElement):
    """
    Builder for C-CDA Results Section (entries required).

    Includes narrative (HTML table) and structured entries for lab results.
    Implements Results Section V3 (template 2.16.840.1.113883.10.20.22.2.3.1:2015-08-01).

    Key features:
    - Groups lab results by panel/organizer
    - Displays test name, value, unit, interpretation, and reference range
    - Supports LOINC codes for test identification
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.3.1",
                extension="2015-08-01",
                description="Results Section (entries required) V3",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.3.1",
                extension="2015-08-01",
                description="Results Section (entries required) V3",
            ),
        ],
    }

    def __init__(
        self,
        result_organizers: Sequence[ResultOrganizerProtocol],
        title: str = "Results",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ResultsSection builder.

        Args:
            result_organizers: List of result organizers (lab panels)
            title: Section title (default: "Results")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.result_organizers = result_organizers
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Results Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs
        self.add_template_ids(section)

        # Add section code (30954-2 = Relevant diagnostic tests and/or laboratory data)
        code_elem = Code(
            code="30954-2",
            system="LOINC",
            display_name="Relevant diagnostic tests and/or laboratory data",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table)
        self._add_narrative(section)

        # Add entries with Result Organizers
        for organizer in self.result_organizers:
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

        if not self.result_organizers:
            # No results - add "No lab results available" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No lab results available"
            return

        # Create table for results
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Panel",
            "Test",
            "Value",
            "Unit",
            "Interpretation",
            "Reference Range",
            "Date",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for organizer_idx, organizer in enumerate(self.result_organizers, start=1):
            # Add each result in the organizer
            for result_idx, result in enumerate(organizer.results, start=1):
                tr = etree.SubElement(tbody, f"{{{NS}}}tr")

                # Panel name (only on first row of each panel)
                td_panel = etree.SubElement(tr, f"{{{NS}}}td")
                if result_idx == 1:
                    content_panel = etree.SubElement(
                        td_panel,
                        f"{{{NS}}}content",
                        ID=f"result-panel-{organizer_idx}",
                    )
                    content_panel.text = organizer.panel_name
                else:
                    td_panel.text = ""  # Empty for subsequent rows

                # Test name (with ID reference)
                td_test = etree.SubElement(tr, f"{{{NS}}}td")
                content_test = etree.SubElement(
                    td_test,
                    f"{{{NS}}}content",
                    ID=f"result-{organizer_idx}-{result_idx}",
                )
                content_test.text = result.test_name

                # Value
                td_value = etree.SubElement(tr, f"{{{NS}}}td")
                td_value.text = result.value

                # Unit
                td_unit = etree.SubElement(tr, f"{{{NS}}}td")
                if result.unit:
                    td_unit.text = result.unit
                else:
                    td_unit.text = "-"

                # Interpretation
                td_interpretation = etree.SubElement(tr, f"{{{NS}}}td")
                if result.interpretation:
                    td_interpretation.text = result.interpretation
                else:
                    td_interpretation.text = "-"

                # Reference Range
                td_range = etree.SubElement(tr, f"{{{NS}}}td")
                if result.reference_range_low or result.reference_range_high:
                    range_text = []
                    if result.reference_range_low:
                        range_text.append(result.reference_range_low)
                    if result.reference_range_high:
                        if range_text:
                            range_text.append(f" - {result.reference_range_high}")
                        else:
                            range_text.append(f"< {result.reference_range_high}")
                    if result.reference_range_unit:
                        range_text.append(f" {result.reference_range_unit}")
                    td_range.text = "".join(range_text)
                else:
                    td_range.text = "-"

                # Date (from organizer or result)
                td_date = etree.SubElement(tr, f"{{{NS}}}td")
                # Use organizer date for consistency
                td_date.text = organizer.effective_time.strftime("%Y-%m-%d")

    def _add_entry(self, section: etree._Element, organizer: ResultOrganizerProtocol) -> None:
        """
        Add entry element with Result Organizer.

        Args:
            section: section element
            organizer: Result organizer data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry", typeCode="DRIV")

        # Create and add Result Organizer
        organizer_builder = ResultOrganizer(organizer, version=self.version)
        entry.append(organizer_builder.to_element())
