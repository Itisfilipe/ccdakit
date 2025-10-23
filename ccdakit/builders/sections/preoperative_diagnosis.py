"""Preoperative Diagnosis Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.preoperative_diagnosis_entry import (
    PreoperativeDiagnosisEntry,
)
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.preoperative_diagnosis import PreoperativeDiagnosisProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class PreoperativeDiagnosisSection(CDAElement):
    """
    Builder for C-CDA Preoperative Diagnosis Section.

    The Preoperative Diagnosis Section records the surgical diagnoses assigned
    to the patient before the surgical procedure which are the reason for the
    surgery. The preoperative diagnosis is, in the surgeon's opinion, the
    diagnosis that will be confirmed during surgery.

    Includes narrative (HTML table) and structured entries.
    Supports R2.1 (2015-08-01) version.

    Template ID: 2.16.840.1.113883.10.20.22.2.34
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.34",
                extension="2015-08-01",
                description="Preoperative Diagnosis Section R2.1",
            ),
        ],
    }

    def __init__(
        self,
        diagnoses: Sequence[PreoperativeDiagnosisProtocol],
        title: str = "Preoperative Diagnosis",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PreoperativeDiagnosisSection builder.

        Args:
            diagnoses: List of preoperative diagnoses satisfying PreoperativeDiagnosisProtocol
            title: Section title (default: "Preoperative Diagnosis")
            version: C-CDA version (R2.1)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.diagnoses = diagnoses
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Preoperative Diagnosis Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:1198-8097, CONF:1198-10439, CONF:1198-32551)
        self.add_template_ids(section)

        # Add section code (CONF:1198-15405, CONF:1198-15406, CONF:1198-30863)
        code_elem = Code(
            code="10219-4",
            system="LOINC",
            display_name="Preoperative Diagnosis",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:1198-8099)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table) (CONF:1198-8100)
        self._add_narrative(section)

        # Add entries with Preoperative Diagnosis Acts (CONF:1198-10096, CONF:1198-15504)
        for diagnosis in self.diagnoses:
            self._add_entry(section, diagnosis)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.diagnoses:
            # No diagnoses - add "No preoperative diagnosis" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No preoperative diagnosis"
            return

        # Create table for diagnoses
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = ["Diagnosis", "Code", "Status", "Diagnosis Date"]
        for header_text in headers:
            th = etree.SubElement(tr, f"{{{NS}}}th")
            th.text = header_text

        # Table body
        tbody = etree.SubElement(table, f"{{{NS}}}tbody")

        for idx, diagnosis in enumerate(self.diagnoses, start=1):
            tr = etree.SubElement(tbody, f"{{{NS}}}tr")

            # Diagnosis name (with ID reference)
            td_name = etree.SubElement(tr, f"{{{NS}}}td")
            content = etree.SubElement(
                td_name,
                f"{{{NS}}}content",
                ID=f"preop-diagnosis-{idx}",
            )
            content.text = diagnosis.name

            # Code
            td_code = etree.SubElement(tr, f"{{{NS}}}td")
            td_code.text = f"{diagnosis.code} ({diagnosis.code_system})"

            # Status
            td_status = etree.SubElement(tr, f"{{{NS}}}td")
            td_status.text = diagnosis.status.capitalize()

            # Diagnosis date
            td_date = etree.SubElement(tr, f"{{{NS}}}td")
            if diagnosis.diagnosis_date:
                td_date.text = diagnosis.diagnosis_date.strftime("%Y-%m-%d")
            else:
                td_date.text = "Unknown"

    def _add_entry(self, section: etree._Element, diagnosis: PreoperativeDiagnosisProtocol) -> None:
        """
        Add entry element with Preoperative Diagnosis Act.

        Args:
            section: section element
            diagnosis: Preoperative diagnosis data
        """
        # Create entry element
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Preoperative Diagnosis Act
        act_builder = PreoperativeDiagnosisEntry(diagnosis, version=self.version)
        entry.append(act_builder.to_element())
