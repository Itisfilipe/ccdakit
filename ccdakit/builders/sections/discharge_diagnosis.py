"""Discharge Diagnosis Section builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.entries.discharge_diagnosis_entry import (
    HospitalDischargeDiagnosis,
)
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.discharge_diagnosis import DischargeDiagnosisProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class DischargeDiagnosisSection(CDAElement):
    """
    Builder for C-CDA Discharge Diagnosis Section.

    This template represents problems or diagnoses present at the time of discharge
    which occurred during the hospitalization. This section includes an optional entry
    to record patient diagnoses specific to this visit. Problems that need ongoing
    tracking should also be included in the Problem Section.

    Template ID: 2.16.840.1.113883.10.20.22.2.24

    Includes narrative (HTML table) and structured entries.
    Supports both R2.1 (2015-08-01) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.24",
                extension="2015-08-01",
                description="Discharge Diagnosis Section (V3)",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.24",
                extension="2014-06-09",
                description="Discharge Diagnosis Section (V2)",
            ),
        ],
    }

    def __init__(
        self,
        diagnoses: Sequence[DischargeDiagnosisProtocol],
        title: str = "Discharge Diagnosis",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize DischargeDiagnosisSection builder.

        Args:
            diagnoses: List of discharge diagnoses satisfying DischargeDiagnosisProtocol
            title: Section title (default: "Discharge Diagnosis")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.diagnoses = diagnoses
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Discharge Diagnosis Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:1198-7979, CONF:1198-10394, CONF:1198-32549)
        self.add_template_ids(section)

        # Add section code (CONF:1198-15355, CONF:1198-15356, CONF:1198-30861)
        code_elem = etree.SubElement(section, f"{{{NS}}}code")
        code_elem.set("code", "11535-2")
        code_elem.set("codeSystem", "2.16.840.1.113883.6.1")
        code_elem.set("codeSystemName", "LOINC")
        code_elem.set("displayName", "Hospital Discharge Diagnosis")

        # Add translation (CONF:1198-32834, CONF:1198-32835, CONF:1198-32836)
        translation = etree.SubElement(code_elem, f"{{{NS}}}translation")
        translation.set("code", "78375-3")
        translation.set("codeSystem", "2.16.840.1.113883.6.1")
        translation.set("codeSystemName", "LOINC")
        translation.set("displayName", "Discharge Diagnosis")

        # Add title (CONF:1198-7981)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (HTML table) (CONF:1198-7982)
        self._add_narrative(section)

        # Add entries with Hospital Discharge Diagnosis (CONF:1198-7983, CONF:1198-15489)
        if self.diagnoses:
            entry = etree.SubElement(section, f"{{{NS}}}entry")
            discharge_diag = HospitalDischargeDiagnosis(
                self.diagnoses,
                version=self.version,
            )
            entry.append(discharge_diag.to_element())

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
            # No diagnoses - add "No discharge diagnoses" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No discharge diagnoses"
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
                ID=f"discharge-diagnosis-{idx}",
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
