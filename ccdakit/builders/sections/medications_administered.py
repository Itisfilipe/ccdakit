"""Medications Administered Section builder for C-CDA documents."""

from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.medication_administered_entry import (
    MedicationAdministeredActivity,
)
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.medication_administered import MedicationAdministeredProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class MedicationsAdministeredSection(CDAElement):
    """
    Builder for C-CDA Medications Administered Section (V2).

    This section documents medications and fluids administered during a procedure,
    encounter, or other clinical activity, excluding anesthetic medications (which
    should be documented in the Anesthesia Section).

    Template ID: 2.16.840.1.113883.10.20.22.2.38 (2014-06-09)
    LOINC Code: 29549-3 (Medications Administered)

    Typically used in:
    - Procedure Notes
    - Emergency Department visits
    - Inpatient encounters
    - Surgical procedures

    Note: Anesthesia medications should use the Anesthesia Section
    (2.16.840.1.113883.10.20.22.2.25) instead.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.38",
                extension="2014-06-09",
                description="Medications Administered Section (V2) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.38",
                extension="2014-06-09",
                description="Medications Administered Section (V2) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        medications: Sequence[MedicationAdministeredProtocol],
        title: str = "Medications Administered",
        version: CDAVersion = CDAVersion.R2_1,
        null_flavor: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize MedicationsAdministeredSection builder.

        Args:
            medications: List of medications satisfying MedicationAdministeredProtocol
            title: Section title (default: "Medications Administered")
            version: C-CDA version (R2.1 or R2.0)
            null_flavor: Null flavor code if section has no information (e.g., "NI")
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.medications = medications
        self.title = title
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        """
        Build Medications Administered Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add null flavor if specified
        if self.null_flavor:
            section.set("nullFlavor", self.null_flavor)

        # Add template IDs (CONF:1098-8152, CONF:1098-10405, CONF:1098-32525)
        self.add_template_ids(section)

        # Add section code (CONF:1098-15383, CONF:1098-15384, CONF:1098-30829)
        code_elem = Code(
            code="29549-3",
            system="LOINC",
            display_name="Medications Administered",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1098-8154)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table) (CONF:1098-8155)
        self._add_narrative(section)

        # Add entries with Medication Activities (CONF:1098-8156, CONF:1098-15499)
        if not self.null_flavor:
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

        if self.null_flavor:
            # No information available
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No information available about medications administered"
            return

        if not self.medications:
            # No medications administered
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No medications administered"
            return

        # Create table for medications
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = [
            "Medication",
            "Dose",
            "Route",
            "Administration Time",
            "Site",
            "Rate",
            "Performer",
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
                ID=f"medication-administered-{idx}",
            )
            content.text = medication.name

            # Dose
            td_dose = etree.SubElement(tr, f"{{{NS}}}td")
            td_dose.text = medication.dose

            # Route
            td_route = etree.SubElement(tr, f"{{{NS}}}td")
            td_route.text = medication.route.capitalize()

            # Administration time
            td_time = etree.SubElement(tr, f"{{{NS}}}td")
            if medication.administration_end_time:
                # Show time range for infusions
                td_time.text = (
                    f"{medication.administration_time.strftime('%Y-%m-%d %H:%M')} - "
                    f"{medication.administration_end_time.strftime('%Y-%m-%d %H:%M')}"
                )
            else:
                td_time.text = medication.administration_time.strftime("%Y-%m-%d %H:%M")

            # Site (optional)
            td_site = etree.SubElement(tr, f"{{{NS}}}td")
            td_site.text = medication.site if medication.site else "-"

            # Rate (optional)
            td_rate = etree.SubElement(tr, f"{{{NS}}}td")
            td_rate.text = medication.rate if medication.rate else "-"

            # Performer (optional)
            td_performer = etree.SubElement(tr, f"{{{NS}}}td")
            td_performer.text = medication.performer if medication.performer else "-"

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            td_status.text = medication.status.capitalize()

    def _add_entry(
        self, section: etree._Element, medication: MedicationAdministeredProtocol
    ) -> None:
        """
        Add entry element with Medication Activity.

        Args:
            section: section element
            medication: Medication administration data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry", typeCode="DRIV")

        # Create and add Medication Administered Activity
        med_builder = MedicationAdministeredActivity(medication, version=self.version)
        entry.append(med_builder.to_element())
