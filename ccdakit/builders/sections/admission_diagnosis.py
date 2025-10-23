"""Admission Diagnosis Section builder for C-CDA documents."""

from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.admission_diagnosis_entry import (
    HospitalAdmissionDiagnosis,
)
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.admission_diagnosis import AdmissionDiagnosisProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class AdmissionDiagnosisSection(CDAElement):
    """
    Builder for C-CDA Admission Diagnosis Section (V3).

    This section contains a narrative description of the problems or diagnoses
    identified by the clinician at the time of the patient's admission. This
    section may contain a coded entry which represents the admitting diagnoses.

    Template ID: 2.16.840.1.113883.10.20.22.2.43 (V3)
    Supports R2.1 (2015-08-01) version.

    The section includes:
    - Narrative table showing diagnoses
    - Hospital Admission Diagnosis entries with Problem Observations

    Conformance Requirements:
    - SHALL contain templateId (CONF:1198-9930, 1198-10391, 1198-32563)
    - SHALL contain code 46241-6 with translation 42347-5 (CONF:1198-15479, etc.)
    - SHALL contain title (CONF:1198-9932)
    - SHALL contain text (CONF:1198-9933)
    - SHOULD contain entry with Hospital Admission Diagnosis (CONF:1198-9934, 1198-15481)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.43",
                extension="2015-08-01",
                description="Admission Diagnosis Section (V3) R2.1",
            ),
        ],
    }

    def __init__(
        self,
        diagnoses: Optional[Sequence[AdmissionDiagnosisProtocol]] = None,
        title: str = "Hospital Admission Diagnosis",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize AdmissionDiagnosisSection builder.

        Args:
            diagnoses: List of admission diagnoses satisfying AdmissionDiagnosisProtocol
            title: Section title (default: "Hospital Admission Diagnosis")
            version: C-CDA version (R2.1)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.diagnoses = diagnoses or []
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Admission Diagnosis Section XML element.

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:1198-9930, 1198-10391, 1198-32563)
        self.add_template_ids(section)

        # Add section code with translation (CONF:1198-15479, 1198-15480, 1198-30865)
        self._add_code(section)

        # Add title (CONF:1198-9932)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:1198-9933)
        self._add_narrative(section)

        # Add entries (CONF:1198-9934, 1198-15481)
        for diagnosis in self.diagnoses:
            self._add_entry(section, diagnosis)

        return section

    def _add_code(self, section: etree._Element) -> None:
        """
        Add section code element with required translation.

        Conformance:
        - CONF:1198-15479: SHALL contain code
        - CONF:1198-15480: code SHALL be 46241-6
        - CONF:1198-30865: codeSystem SHALL be LOINC
        - CONF:1198-32749: SHALL contain translation
        - CONF:1198-32750: translation code SHALL be 42347-5
        - CONF:1198-32751: translation codeSystem SHALL be LOINC

        Args:
            section: section element
        """
        # Create primary code (CONF:1198-15479, 1198-15480, 1198-30865)
        code_elem = Code(
            code="46241-6",
            system="LOINC",
            display_name="Hospital Admission diagnosis",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"

        # Add required translation (CONF:1198-32749, 1198-32750, 1198-32751)
        translation = etree.SubElement(code_elem, f"{{{NS}}}translation")
        translation.set("code", "42347-5")
        translation.set("codeSystem", "2.16.840.1.113883.6.1")
        translation.set("displayName", "Admission Diagnosis")

        section.append(code_elem)

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with HTML table.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.diagnoses:
            # No diagnoses - add "No admission diagnosis documented" paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No admission diagnosis documented"
            return

        # Create table for diagnoses
        table = etree.SubElement(text, f"{{{NS}}}table", border="1", width="100%")

        # Table header
        thead = etree.SubElement(table, f"{{{NS}}}thead")
        tr = etree.SubElement(thead, f"{{{NS}}}tr")

        headers = ["Diagnosis", "Code", "Admission Date", "Diagnosis Date"]
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
                ID=f"admission-diagnosis-{idx}",
            )
            content.text = diagnosis.name

            # Code
            td_code = etree.SubElement(tr, f"{{{NS}}}td")
            td_code.text = f"{diagnosis.code} ({diagnosis.code_system})"

            # Admission date
            td_admission = etree.SubElement(tr, f"{{{NS}}}td")
            if diagnosis.admission_date:
                td_admission.text = diagnosis.admission_date.strftime("%Y-%m-%d")
            else:
                td_admission.text = "Unknown"

            # Diagnosis date
            td_diagnosis = etree.SubElement(tr, f"{{{NS}}}td")
            if diagnosis.diagnosis_date:
                td_diagnosis.text = diagnosis.diagnosis_date.strftime("%Y-%m-%d")
            else:
                td_diagnosis.text = "Unknown"

    def _add_entry(self, section: etree._Element, diagnosis: AdmissionDiagnosisProtocol) -> None:
        """
        Add entry element with Hospital Admission Diagnosis act.

        Conformance:
        - CONF:1198-9934: SHOULD contain entry
        - CONF:1198-15481: entry SHALL contain Hospital Admission Diagnosis

        Args:
            section: section element
            diagnosis: Admission diagnosis data
        """
        # Create entry element (CONF:1198-9934)
        entry = etree.SubElement(section, f"{{{NS}}}entry")

        # Create and add Hospital Admission Diagnosis act (CONF:1198-15481)
        diagnosis_builder = HospitalAdmissionDiagnosis(diagnosis, version=self.version)
        entry.append(diagnosis_builder.to_element())
