"""Medications Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.medication import MedicationActivity
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.medication import MedicationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class MedicationsSection(CDAElement):
    """
    Builder for C-CDA Medications Section.

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 (2015-08-01) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.1.1",
                extension="2014-06-09",
                description="Medications Section (entries required) R2.1",
            ),
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.1",
                extension="2014-06-09",
                description="Medications Section (entries optional) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.1.1",
                extension="2014-06-09",
                description="Medications Section (entries required) R2.0",
            ),
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.1",
                extension="2014-06-09",
                description="Medications Section (entries optional) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        medications: Sequence[MedicationProtocol],
        title: str = "Medications",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize MedicationsSection builder.

        Args:
            medications: List of medications satisfying MedicationProtocol
            title: Section title (default: "Medications")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.medications = medications
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Medications Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs
        self.add_template_ids(section)

        # Add section code (10160-0 = History of Medication use Narrative)
        code_elem = Code(
            code="10160-0",
            system="LOINC",
            display_name="History of Medication use Narrative",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table)
        self._add_narrative(section)

        # Add entries with Medication Activities
        for medication in self.medications:
            self._add_entry(section, medication)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.medications:
            # No medications - add "No known medications" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No known medications"
            return

        # Create table for medications
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Medication",
            "Dosage",
            "Route",
            "Frequency",
            "Start Date",
            "End Date",
            "Status",
        ]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, medication in enumerate(self.medications, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Medication name (with ID reference)
            td_name = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_name,
                f"{{{NS}}}content",
                ID=f"medication-{idx}",
            )
            content.text = medication.name

            # Dosage
            td_dosage = etree.SubElement(tr, f"{{{NS}}}td")
            td_dosage.text = medication.dosage

            # Route
            td_route = etree.SubElement(tr, f"{{{NS}}}td")
            td_route.text = medication.route.capitalize()

            # Frequency
            td_frequency = etree.SubElement(tr, f"{{{NS}}}td")
            td_frequency.text = medication.frequency

            # Start date
            td_start = etree.SubElement(tr, f"{{{NS}}}td")
            td_start.text = medication.start_date.strftime("%Y-%m-%d")

            # End date
            td_end = etree.SubElement(tr, f"{{{NS}}}td")
            if medication.end_date:
                td_end.text = medication.end_date.strftime("%Y-%m-%d")
            else:
                td_end.text = "Ongoing" if medication.status == "active" else "Unknown"

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            td_status.text = medication.status.capitalize()

    def _add_entry(self, section: etree._Element, medication: MedicationProtocol) -> None:
        """
        Add entry element with Medication Activity.

        Args:
            section: section element
            medication: Medication data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry", typeCode="DRIV")

        # Create and add Medication Activity
        med_builder = MedicationActivity(medication, version=self.version)
        entry.append(med_builder.to_element())
