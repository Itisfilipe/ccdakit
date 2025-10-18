"""Chief Complaint and Reason for Visit Section builder for C-CDA documents."""

from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.chief_complaint import ChiefComplaintProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class ChiefComplaintAndReasonForVisitSection(CDAElement):
    """
    Builder for C-CDA Chief Complaint and Reason for Visit Section.

    This section records the patient's chief complaint (the patient's own description)
    and/or the reason for the patient's visit (the provider's description of the reason
    for visit). Local policy determines whether the information is divided into two
    sections or recorded in one section serving both purposes.

    Template: 2.16.840.1.113883.10.20.22.2.13
    Code: 46239-0 (Chief Complaint and Reason for Visit) from LOINC

    This section contains only narrative text - no structured entries are required.
    Supports both R2.1 and R2.0 versions.

    Conformance:
    - CONF:81-7840: SHALL contain exactly one [1..1] templateId
    - CONF:81-10383: templateId/@root="2.16.840.1.113883.10.20.22.2.13"
    - CONF:81-15449: SHALL contain exactly one [1..1] code
    - CONF:81-15450: code/@code="46239-0"
    - CONF:81-26473: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
    - CONF:81-7842: SHALL contain exactly one [1..1] title
    - CONF:81-7843: SHALL contain exactly one [1..1] text
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.13",
                extension=None,  # No extension for this template
                description="Chief Complaint and Reason for Visit Section R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.2.13",
                extension=None,  # No extension for this template
                description="Chief Complaint and Reason for Visit Section R2.0",
            ),
        ],
    }

    # LOINC code for chief complaint and reason for visit section
    SECTION_CODE = "46239-0"
    SECTION_DISPLAY = "Chief Complaint and Reason for Visit"

    def __init__(
        self,
        chief_complaints: Optional[Sequence[ChiefComplaintProtocol]] = None,
        title: str = "Chief Complaint and Reason for Visit",
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ChiefComplaintAndReasonForVisitSection builder.

        Args:
            chief_complaints: List of chief complaint/reason for visit items.
                            If None or empty, displays "No chief complaint or reason for visit documented"
            title: Section title (default: "Chief Complaint and Reason for Visit")
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.chief_complaints = chief_complaints if chief_complaints is not None else []
        self.title = title

    def build(self) -> etree.Element:
        """
        Build Chief Complaint and Reason for Visit Section XML element.

        Conformance:
        - CONF:81-7840: SHALL contain templateId
        - CONF:81-10383: templateId/@root="2.16.840.1.113883.10.20.22.2.13"
        - CONF:81-15449: SHALL contain code
        - CONF:81-15450: code/@code="46239-0"
        - CONF:81-26473: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
        - CONF:81-7842: SHALL contain title
        - CONF:81-7843: SHALL contain text

        Returns:
            lxml Element for section
        """
        # Create section element
        section = etree.Element(f"{{{NS}}}section")

        # Add template IDs (CONF:81-7840, CONF:81-10383)
        self.add_template_ids(section)

        # Add section code (CONF:81-15449, CONF:81-15450, CONF:81-26473)
        # 46239-0 = Chief Complaint and Reason for Visit (LOINC)
        code_elem = Code(
            code=self.SECTION_CODE,
            system="LOINC",
            display_name=self.SECTION_DISPLAY,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        section.append(code_elem)

        # Add title (CONF:81-7842)
        title_elem = etree.SubElement(section, f"{{{NS}}}title")
        title_elem.text = self.title

        # Add narrative text (CONF:81-7843)
        self._add_narrative(section)

        return section

    def _add_narrative(self, section: etree._Element) -> None:
        """
        Add narrative text element.

        The narrative provides human-readable content for the section.
        When no chief complaints are present, displays appropriate message.
        When chief complaints exist, they are displayed as a list or paragraph.

        Args:
            section: section element
        """
        # Create text element
        text = etree.SubElement(section, f"{{{NS}}}text")

        if not self.chief_complaints:
            # No chief complaint - add default paragraph
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            paragraph.text = "No chief complaint or reason for visit documented"
            return

        # If there's only one chief complaint, display as paragraph
        if len(self.chief_complaints) == 1:
            paragraph = etree.SubElement(text, f"{{{NS}}}paragraph")
            content = etree.SubElement(
                paragraph,
                f"{{{NS}}}content",
                ID="chief-complaint-1",
            )
            content.text = self.chief_complaints[0].text
            return

        # If there are multiple chief complaints, display as a list
        list_elem = etree.SubElement(text, f"{{{NS}}}list")
        for idx, complaint in enumerate(self.chief_complaints, start=1):
            item = etree.SubElement(list_elem, f"{{{NS}}}item")
            content = etree.SubElement(
                item,
                f"{{{NS}}}content",
                ID=f"chief-complaint-{idx}",
            )
            content.text = complaint.text
