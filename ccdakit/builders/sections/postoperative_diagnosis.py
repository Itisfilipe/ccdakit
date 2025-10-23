"""Postoperative Diagnosis Section builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig


# CDA namespace
NS = "urn:hl7-org:v3"


class PostoperativeDiagnosisSection(CDAElement):
    """
    Builder for C-CDA Postoperative Diagnosis Section.

    The Postoperative Diagnosis Section records the diagnosis or diagnoses
    discovered or confirmed during surgery. Often it is the same as the
    preoperative diagnosis.

    This is a simple narrative-only section without structured entries.
    Supports both R2.1 and R2.0 versions.

    Conformance:
    - Template ID: 2.16.840.1.113883.10.20.22.2.35
    - Code: 10218-6 (Postoperative Diagnosis) from LOINC
    - Contains: Only narrative text, no structured entries
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.35",
                extension=None,  # No extension specified for this section
                description="Postoperative Diagnosis Section",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.35",
                extension=None,
                description="Postoperative Diagnosis Section",
            ),
        ],
    }

    def __init__(
        self,
        diagnosis_text: str,
        title: str = "Postoperative Diagnosis",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PostoperativeDiagnosisSection builder.

        Args:
            diagnosis_text: The narrative text describing the postoperative diagnosis
            title: Section title (default: "Postoperative Diagnosis")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.diagnosis_text = diagnosis_text
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Postoperative Diagnosis Section XML element.

        Conformance:
        - CONF:81-8101: SHALL contain exactly one [1..1] templateId
        - CONF:81-10437: templateId/@root="2.16.840.1.113883.10.20.22.2.35"
        - CONF:81-15401: SHALL contain exactly one [1..1] code
        - CONF:81-15402: code/@code="10218-6" (Postoperative Diagnosis)
        - CONF:81-26488: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
        - CONF:81-8103: SHALL contain exactly one [1..1] title
        - CONF:81-8104: SHALL contain exactly one [1..1] text

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:81-8101, CONF:81-10437)
        self.add_template_ids(section)

        # Add section code (CONF:81-15401, CONF:81-15402, CONF:81-26488)
        # 10218-6 = Postoperative Diagnosis (LOINC)
        code_elem = Code(
            code="10218-6",
            system="LOINC",
            display_name="Postoperative Diagnosis",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:81-8103)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:81-8104)
        self._add_narrative(section)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element.

        The narrative provides human-readable content for the section.
        For Postoperative Diagnosis, this typically contains the diagnosis
        or diagnoses discovered or confirmed during surgery.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        # Add diagnosis text as paragraph
        paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
        paragraph.text = self.diagnosis_text
