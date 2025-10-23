"""Reason for Visit Section builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig


# CDA namespace
NS = "urn:hl7-org:v3"


class ReasonForVisitSection(CDAElement):
    """
    Builder for C-CDA Reason for Visit Section.

    This section records the patient's reason for the patient's visit as documented
    by the provider. Local policy determines whether Reason for Visit and Chief
    Complaint are in separate or combined sections.

    This is a simple narrative-only section without structured entries.
    Supports both R2.1 and R2.0 versions.

    Conformance:
    - Template ID: 2.16.840.1.113883.10.20.22.2.12
    - Code: 29299-5 (Reason for Visit) from LOINC
    - Contains: Only narrative text, no structured entries
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.12",
                extension=None,  # R2.1 does not specify extension for this section
                description="Reason for Visit Section R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.12",
                extension=None,
                description="Reason for Visit Section R2.0",
            ),
        ],
    }

    def __init__(
        self,
        reason_text: str,
        title: str = "Reason for Visit",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ReasonForVisitSection builder.

        Args:
            reason_text: The narrative text describing the reason for visit
            title: Section title (default: "Reason for Visit")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.reason_text = reason_text
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Reason for Visit Section XML element.

        Conformance:
        - CONF:81-7836: SHALL contain exactly one [1..1] templateId
        - CONF:81-10448: templateId/@root="2.16.840.1.113883.10.20.22.2.12"
        - CONF:81-15429: SHALL contain exactly one [1..1] code
        - CONF:81-15430: code/@code="29299-5" (Reason for Visit)
        - CONF:81-26494: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
        - CONF:81-7838: SHALL contain exactly one [1..1] title
        - CONF:81-7839: SHALL contain exactly one [1..1] text

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:81-7836, CONF:81-10448)
        self.add_template_ids(section)

        # Add section code (CONF:81-15429, CONF:81-15430, CONF:81-26494)
        # 29299-5 = Reason for Visit (LOINC)
        code_elem = Code(
            code="29299-5",
            system="LOINC",
            display_name="Reason for Visit",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:81-7838)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:81-7839)
        self._add_narrative(section)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element.

        The narrative provides human-readable content for the section.
        For Reason for Visit, this is typically a simple paragraph containing
        the provider's documentation of why the patient is seeking care.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        # Add reason text as paragraph
        paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
        paragraph.text = self.reason_text
