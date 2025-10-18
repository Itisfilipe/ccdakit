"""Admission Medications Section builder for C-CDA documents."""

from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.admission_medication import AdmissionMedication
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.medication import MedicationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class AdmissionMedicationsSection(CDAElement):
    """
    Builder for C-CDA Admission Medications Section (entries optional).

    The section contains the medications taken by the patient prior to
    and at the time of admission to the facility.

    Template ID: 2.16.840.1.113883.10.20.22.2.44
    Supports both R2.1 (2015-08-01) and R2.0 versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.44",
                extension="2015-08-01",
                description="Admission Medications Section (entries optional) V3",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.44",
                extension=None,  # R2.0 version may not have extension
                description="Admission Medications Section (entries optional)",
            ),
        ],
    }

    # LOINC code for Medications on Admission
    LOINC_CODE = "42346-7"
    LOINC_OID = "2.16.840.1.113883.6.1"

    def __init__(
        self,
        medications: Sequence[MedicationProtocol],
        title: str = "Admission Medications",
        version: CDAVersion = CDAVersion.R2_1,
        null_flavor: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize AdmissionMedicationsSection builder.

        Args:
            medications: List of medications satisfying MedicationProtocol
            title: Section title (default: "Admission Medications")
            version: C-CDA version (R2.1 or R2.0)
            null_flavor: Null flavor if no medications available (e.g., "NI" for no information)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.medications = medications
        self.title = title
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        """
        Build Admission Medications Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs
        # CONF:1198-10098, CONF:1198-10392, CONF:1198-32560
        self.add_template_ids(section)

        # Add section code
        # CONF:1198-15482, CONF:1198-15483, CONF:1198-32142
        code_elem = Code(
            code=self.LOINC_CODE,
            system="LOINC",
            display_name="Medications on Admission",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title
        # CONF:1198-10100
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table)
        # CONF:1198-10101
        self._add_narrative(section)

        # Add entries with Admission Medication acts
        # CONF:1198-10102 (SHOULD), CONF:1198-15484
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
            # Handle null flavor case
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            null_flavor_text = {
                "NI": "No information about admission medications",
                "NA": "Not applicable",
                "UNK": "Unknown",
                "ASKU": "Asked but unknown",
                "NAV": "Temporarily unavailable",
                "NASK": "Not asked",
                "MSK": "Masked",
                "OTH": "Other",
            }
            paragraph.text = null_flavor_text.get(
                self.null_flavor, "No admission medications recorded"
            )
            return

        if not self.medications:
            # No medications - add "No medications on admission" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No medications on admission"
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
                ID=f"admission-medication-{idx}",
            )
            content.text = medication.name

            # Dosage
            td_dosage = etree.SubElement(tr, f"{{{NS}}}td")
            td_dosage.text = str(medication.dosage) if medication.dosage else "N/A"

            # Route
            td_route = etree.SubElement(tr, f"{{{NS}}}td")
            if medication.route:
                td_route.text = medication.route.capitalize()
            else:
                td_route.text = "N/A"

            # Frequency
            td_frequency = etree.SubElement(tr, f"{{{NS}}}td")
            td_frequency.text = str(medication.frequency) if medication.frequency else "N/A"

            # Start date
            td_start = etree.SubElement(tr, f"{{{NS}}}td")
            if medication.start_date:
                td_start.text = medication.start_date.strftime("%Y-%m-%d")
            else:
                td_start.text = "Unknown"

            # End date
            td_end = etree.SubElement(tr, f"{{{NS}}}td")
            if medication.end_date:
                td_end.text = medication.end_date.strftime("%Y-%m-%d")
            elif medication.status == "active":
                td_end.text = "Ongoing"
            else:
                td_end.text = "Unknown"

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            if medication.status:
                td_status.text = medication.status.capitalize()
            else:
                td_status.text = "Unknown"

    def _add_entry(self, section: etree._Element, medication: MedicationProtocol) -> None:
        """
        Add entry element with Admission Medication.

        Args:
            section: section element
            medication: Medication data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Admission Medication (act wrapper)
        admission_med = AdmissionMedication(medication, version=self.version)
        entry.append(admission_med.to_element())
