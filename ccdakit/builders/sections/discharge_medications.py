"""Discharge Medications Section builder for C-CDA documents."""

from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.entries.discharge_medication import DischargeMedication
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.medication import MedicationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class DischargeMedicationsSection(CDAElement):
    """
    Builder for C-CDA Discharge Medications Section (entries required).

    This section contains the medications the patient is intended to take or stop after discharge.
    Current, active medications must be listed. The section may also include a patient's
    prescription history and indicate the source of the medication list.

    Conforms to:
    - Discharge Medications Section (entries required) (V3) template
      (2.16.840.1.113883.10.20.22.2.11.1:2015-08-01)

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 (2015-08-01) and R2.0 (2015-08-01) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.11.1",
                extension="2015-08-01",
                description="Discharge Medications Section (entries required) (V3) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.11.1",
                extension="2015-08-01",
                description="Discharge Medications Section (entries required) (V3) R2.0",
            ),
        ],
    }

    # LOINC code system OID
    LOINC_OID = "2.16.840.1.113883.6.1"

    def __init__(
        self,
        medications: Sequence[MedicationProtocol],
        title: str = "Discharge Medications",
        version: CDAVersion = CDAVersion.R2_1,
        null_flavor: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize DischargeMedicationsSection builder.

        Args:
            medications: List of medications satisfying MedicationProtocol
            title: Section title (default: "Discharge Medications")
            version: C-CDA version (R2.1 or R2.0)
            null_flavor: Optional null flavor (e.g., "NI" for No Information)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.medications = medications
        self.title = title
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        """
        Build Discharge Medications Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add nullFlavor if specified (CONF:1198-32812)
        if self.null_flavor:
            section.set("nullFlavor", self.null_flavor)

        # Add template IDs (CONF:1198-7822, CONF:1198-10397, CONF:1198-32562)
        self.add_template_ids(section)

        # Add section code (CONF:1198-15361, CONF:1198-15362, CONF:1198-32145)
        self._add_code(section)

        # Add title (CONF:1198-7824)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:1198-7825)
        self._add_narrative(section)

        # Add entries with Discharge Medication (CONF:1198-7826, CONF:1198-15491)
        # If section/@nullFlavor is not present: SHALL contain at least one entry
        if not self.null_flavor:
            for medication in self.medications:
                self._add_entry(section, medication)

        return section

    def _add_code(self, section: etree._Element) -> None:
        """
        Add code element to section.

        Args:
            section: section element
        """
        # CONF:1198-15361 - SHALL contain exactly one [1..1] code
        code_elem = etree.SubElement(section, f"{{{NS}}}code")

        # CONF:1198-15362 - code SHALL be "10183-2" Hospital Discharge Medications
        code_elem.set("code", "10183-2")

        # CONF:1198-32145 - codeSystem SHALL be LOINC
        code_elem.set("codeSystem", self.LOINC_OID)
        code_elem.set("codeSystemName", "LOINC")
        code_elem.set("displayName", "Hospital Discharge Medications")

        # CONF:1198-32857 - SHALL contain exactly one [1..1] translation
        translation = etree.SubElement(code_elem, f"{{{NS}}}translation")

        # CONF:1198-32858 - translation code SHALL be "75311-1" Discharge Medications
        translation.set("code", "75311-1")

        # CONF:1198-32859 - translation codeSystem SHALL be LOINC
        translation.set("codeSystem", self.LOINC_OID)
        translation.set("codeSystemName", "LOINC")
        translation.set("displayName", "Discharge Medications")

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.medications:
            # No medications - add "No discharge medications" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            if self.null_flavor:
                paragraph.text = "No information available for discharge medications"
            else:
                paragraph.text = "No discharge medications"
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
            "Instructions",
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
                ID=f"discharge-medication-{idx}",
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

            # Instructions
            td_instructions = etree.SubElement(tr, f"{{{NS}}}td")
            if medication.instructions:
                td_instructions.text = medication.instructions
            else:
                td_instructions.text = "-"

    def _add_entry(self, section: etree._Element, medication: MedicationProtocol) -> None:
        """
        Add entry element with Discharge Medication.

        Args:
            section: section element
            medication: Medication data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Discharge Medication
        discharge_med_builder = DischargeMedication(medication, version=self.version)
        entry.append(discharge_med_builder.to_element())
