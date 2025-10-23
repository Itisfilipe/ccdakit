"""Hospital Course Section builder for C-CDA documents."""

from typing import Optional

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.hospital_course import HospitalCourseProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class HospitalCourseSection(CDAElement):
    """
    Builder for C-CDA Hospital Course Section.

    This section describes the sequence of events from admission to discharge
    in a hospital facility. It is a narrative-only section that provides a
    chronological account of the patient's hospital stay.

    The Hospital Course Section is typically included in Discharge Summary
    documents to document the patient's clinical course during hospitalization,
    including significant events, treatments, procedures, and response to therapy.

    This is a narrative-only section with no structured entries.

    Conformance:
    - Template ID: 1.3.6.1.4.1.19376.1.5.3.1.3.5 (IHE)
    - Code: 8648-8 (Hospital Course) from LOINC
    - Contains: Narrative text only (no entries required)

    References:
    - CONF:81-7852: SHALL contain templateId
    - CONF:81-10459: templateId/@root="1.3.6.1.4.1.19376.1.5.3.1.3.5"
    - CONF:81-15487: SHALL contain code
    - CONF:81-15488: code/@code="8648-8"
    - CONF:81-26480: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
    - CONF:81-7854: SHALL contain title
    - CONF:81-7855: SHALL contain text
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="1.3.6.1.4.1.19376.1.5.3.1.3.5",
                extension=None,  # No extension in spec
                description="Hospital Course Section (IHE)",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="1.3.6.1.4.1.19376.1.5.3.1.3.5",
                extension=None,
                description="Hospital Course Section (IHE)",
            ),
        ],
    }

    def __init__(
        self,
        hospital_course: Optional[HospitalCourseProtocol] = None,
        narrative_text: Optional[str] = None,
        title: str = "Hospital Course",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize HospitalCourseSection builder.

        You can provide either:
        1. A HospitalCourseProtocol object with course_text property
        2. A narrative_text string directly
        3. Both (narrative_text takes precedence)

        Args:
            hospital_course: Hospital course data object implementing HospitalCourseProtocol
            narrative_text: Free-form narrative text for hospital course (takes precedence)
            title: Section title (default: "Hospital Course")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement

        Raises:
            ValueError: If neither hospital_course nor narrative_text is provided
        """
        super().__init__(version=version, **kwargs)
        self.hospital_course = hospital_course
        self.narrative_text = narrative_text
        self.title = title

        # Determine the final narrative text to use
        if self.narrative_text:
            self._final_narrative = self.narrative_text
        elif self.hospital_course:
            self._final_narrative = self.hospital_course.course_text
        else:
            # Allow empty content - will show default message
            self._final_narrative = "No hospital course information provided."

    def build(self) -> etree.Element:
        """
        Build Hospital Course Section XML element.

        Conformance:
        - CONF:81-7852: SHALL contain templateId
        - CONF:81-10459: templateId/@root="1.3.6.1.4.1.19376.1.5.3.1.3.5"
        - CONF:81-15487: SHALL contain code
        - CONF:81-15488: code/@code="8648-8"
        - CONF:81-26480: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
        - CONF:81-7854: SHALL contain title
        - CONF:81-7855: SHALL contain text

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:81-7852, CONF:81-10459)
        self.add_template_ids(section)

        # Add section code (CONF:81-15487, CONF:81-15488, CONF:81-26480)
        # 8648-8 = Hospital Course (LOINC)
        code_elem = Code(
            code="8648-8",
            system="LOINC",
            display_name="Hospital Course",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:81-7854)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:81-7855)
        self._add_narrative(section)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element with hospital course content.

        The narrative contains the chronological description of the patient's
        hospital stay. For long narratives, multiple paragraphs may be used
        to improve readability.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        # Split narrative into paragraphs if it contains double line breaks
        # This helps with readability for longer hospital courses
        if "\n\n" in self._final_narrative:
            paragraphs = self._final_narrative.split("\n\n")
            for para_text in paragraphs:
                if para_text.strip():  # Only add non-empty paragraphs
                    paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
                    paragraph.text = para_text.strip()
        else:
            # Single paragraph for simpler narratives
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = self._final_narrative
