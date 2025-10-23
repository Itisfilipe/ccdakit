"""Continuity of Care Document (CCD) builder.

The CCD is one of the most commonly used C-CDA document types. It provides
a snapshot of a patient's clinical information at a specific point in time,
including problems, medications, allergies, procedures, immunizations, and more.

Reference: HL7 C-CDA Implementation Guide
Template ID: 2.16.840.1.113883.10.20.22.1.2
"""

from datetime import datetime
from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.document import ClinicalDocument
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.author import AuthorProtocol, OrganizationProtocol
from ccdakit.protocols.patient import PatientProtocol


class ContinuityOfCareDocument(ClinicalDocument):
    """
    Continuity of Care Document (CCD) builder.

    The CCD is a core document type in C-CDA that provides a summary of a patient's
    health status and care. It's commonly used for:
    - Care transitions between providers
    - Patient health summaries
    - Longitudinal care records
    - Health information exchange

    Required Sections (per ONC 2015 Edition):
    - Problems Section
    - Medications Section
    - Allergies Section
    - Procedures Section (optional but recommended)
    - Results Section (optional but recommended)
    - Immunizations Section (optional but recommended)
    - Vital Signs Section (optional but recommended)
    - Social History Section (optional but recommended)

    Usage:
        >>> from ccdakit.builders.documents import ContinuityOfCareDocument
        >>> from ccdakit.builders.sections import ProblemsSection, MedicationsSection
        >>>
        >>> doc = ContinuityOfCareDocument(
        ...     patient=patient_data,
        ...     author=author_data,
        ...     custodian=custodian_org,
        ...     sections=[
        ...         ProblemsSection(problems=problems),
        ...         MedicationsSection(medications=meds),
        ...     ],
        ... )
        >>> xml_string = doc.to_xml_string()
    """

    # CCD templates include both the base C-CDA template and CCD-specific template
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.1",
                extension="2015-08-01",
                description="C-CDA R2.1",
            ),
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.2",
                extension="2015-08-01",
                description="Continuity of Care Document (CCD) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.1",
                extension="2014-06-09",
                description="C-CDA R2.0",
            ),
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.2",
                extension="2014-06-09",
                description="Continuity of Care Document (CCD) R2.0",
            ),
        ],
    }

    def __init__(
        self,
        patient: PatientProtocol,
        author: AuthorProtocol,
        custodian: OrganizationProtocol,
        sections: Optional[Sequence[CDAElement]] = None,
        document_id: Optional[str] = None,
        title: str = "Continuity of Care Document",
        effective_time: Optional[datetime] = None,
        **kwargs,
    ):
        """
        Initialize CCD builder.

        Args:
            patient: Patient data satisfying PatientProtocol
            author: Author data satisfying AuthorProtocol
            custodian: Custodian organization data satisfying OrganizationProtocol
            sections: List of section builders (optional but recommended for completeness)
            document_id: Document UUID (generated if not provided)
            title: Document title (defaults to "Continuity of Care Document")
            effective_time: Document creation time (current time if not provided)
            **kwargs: Additional arguments passed to ClinicalDocument
        """
        super().__init__(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=sections,
            document_id=document_id,
            title=title,
            effective_time=effective_time,
            **kwargs,
        )

    def _add_document_code(self, doc: etree._Element) -> None:
        """
        Add CCD document type code.

        Uses LOINC code 34133-9: "Summarization of Episode Note"
        This is the standard code for CCD documents.

        Args:
            doc: ClinicalDocument element
        """
        # LOINC code for CCD
        doc_code = Code(
            code="34133-9",
            system="LOINC",
            display_name="Summarization of Episode Note",
        )
        code_elem = doc_code.to_element()
        doc.append(code_elem)

    def validate_required_sections(self) -> "tuple[bool, list[str]]":
        """
        Validate that required sections are present for ONC compliance.

        While C-CDA allows flexibility, ONC 2015 Edition certification requires
        specific sections. This method helps identify missing required sections.

        Returns:
            Tuple of (is_valid, list of missing section names)

        Example:
            >>> is_valid, missing = doc.validate_required_sections()
            >>> if not is_valid:
            ...     print(f"Missing sections: {', '.join(missing)}")
        """
        required_section_templates = {
            "2.16.840.1.113883.10.20.22.2.5.1": "Problems Section",
            "2.16.840.1.113883.10.20.22.2.1.1": "Medications Section",
            "2.16.840.1.113883.10.20.22.2.6.1": "Allergies Section",
        }

        # Get template IDs from all sections
        section_template_ids = set()
        for section in self.sections:
            if hasattr(section, "TEMPLATES") and self.version in section.TEMPLATES:
                for template in section.TEMPLATES[self.version]:
                    section_template_ids.add(template.root)

        # Check for missing required sections
        missing_sections = []
        for template_id, section_name in required_section_templates.items():
            if template_id not in section_template_ids:
                missing_sections.append(section_name)

        return len(missing_sections) == 0, missing_sections
