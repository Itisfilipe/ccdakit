"""Factory methods for creating common C-CDA document types with sensible defaults."""

from datetime import datetime
from typing import List, Optional

from ccdakit.builders.common import Code
from ccdakit.builders.document import ClinicalDocument
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.author import AuthorProtocol, OrganizationProtocol
from ccdakit.protocols.patient import PatientProtocol


class DocumentFactory:
    """
    Factory for creating common C-CDA document types.

    This factory provides convenience methods for creating standard C-CDA document
    types with appropriate template IDs and default configurations. Each factory
    method returns a ClinicalDocument configured for a specific document type.

    Examples:
        >>> # Create a Continuity of Care Document
        >>> ccd = DocumentFactory.create_continuity_of_care_document(
        ...     patient=patient,
        ...     author=author,
        ...     custodian=custodian,
        ...     sections=[problems_section, medications_section],
        ... )
        >>>
        >>> # Create a Discharge Summary
        >>> discharge = DocumentFactory.create_discharge_summary(
        ...     patient=patient,
        ...     author=author,
        ...     custodian=custodian,
        ...     sections=[discharge_diagnosis_section, discharge_meds_section],
        ... )
    """

    @staticmethod
    def create_continuity_of_care_document(
        patient: PatientProtocol,
        author: AuthorProtocol,
        custodian: OrganizationProtocol,
        sections: Optional[List[CDAElement]] = None,
        effective_time: Optional[datetime] = None,
        document_id: Optional[str] = None,
        version: CDAVersion = CDAVersion.R2_1,
    ) -> "ContinuityOfCareDocument":
        """
        Create a Continuity of Care Document (CCD).

        The CCD is the most commonly used C-CDA document type, designed to provide
        a comprehensive summary of a patient's health status and care. It typically
        includes all major clinical sections.

        Template IDs:
            - R2.1: 2.16.840.1.113883.10.20.22.1.2 (2015-08-01)
            - R2.0: 2.16.840.1.113883.10.20.22.1.2 (2014-06-09)

        Common sections:
            - Problems (required)
            - Medications (required)
            - Allergies (required)
            - Immunizations
            - Procedures
            - Results
            - Vital Signs
            - Encounters
            - Social History
            - Plan of Care

        Args:
            patient: Patient data satisfying PatientProtocol
            author: Author data satisfying AuthorProtocol
            custodian: Custodian organization data satisfying OrganizationProtocol
            sections: List of section builders (optional)
            effective_time: Document creation time (current time if not provided)
            document_id: Document UUID (generated if not provided)
            version: C-CDA version (R2.1 by default)

        Returns:
            ContinuityOfCareDocument instance ready to build XML

        Examples:
            >>> from ccdakit.utils.factories import DocumentFactory
            >>> from ccdakit.builders.sections.problems import ProblemsSection
            >>> from ccdakit.builders.sections.medications import MedicationsSection
            >>>
            >>> ccd = DocumentFactory.create_continuity_of_care_document(
            ...     patient=my_patient,
            ...     author=my_author,
            ...     custodian=my_organization,
            ...     sections=[
            ...         ProblemsSection(problems=[...]),
            ...         MedicationsSection(medications=[...]),
            ...     ],
            ... )
            >>> xml = ccd.to_xml_string()
        """
        return ContinuityOfCareDocument(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=sections,
            effective_time=effective_time,
            document_id=document_id,
            version=version,
        )

    @staticmethod
    def create_discharge_summary(
        patient: PatientProtocol,
        author: AuthorProtocol,
        custodian: OrganizationProtocol,
        sections: Optional[List[CDAElement]] = None,
        effective_time: Optional[datetime] = None,
        document_id: Optional[str] = None,
        version: CDAVersion = CDAVersion.R2_1,
    ) -> "DischargeSummary":
        """
        Create a Discharge Summary document.

        The Discharge Summary provides a comprehensive summary of a patient's
        hospital stay, created at the time of discharge. It documents the reason
        for hospitalization, procedures performed, hospital course, and discharge
        instructions.

        Template IDs:
            - R2.1: 2.16.840.1.113883.10.20.22.1.8 (2015-08-01)
            - R2.0: 2.16.840.1.113883.10.20.22.1.8 (2014-06-09)

        Required sections:
            - Hospital Discharge Diagnosis
            - Discharge Medications
            - Hospital Course
            - Discharge Instructions (optional but recommended)

        Args:
            patient: Patient data satisfying PatientProtocol
            author: Author data satisfying AuthorProtocol
            custodian: Custodian organization data satisfying OrganizationProtocol
            sections: List of section builders (optional)
            effective_time: Document creation time (current time if not provided)
            document_id: Document UUID (generated if not provided)
            version: C-CDA version (R2.1 by default)

        Returns:
            DischargeSummary instance ready to build XML

        Examples:
            >>> discharge = DocumentFactory.create_discharge_summary(
            ...     patient=my_patient,
            ...     author=my_author,
            ...     custodian=my_hospital,
            ...     sections=[
            ...         discharge_diagnosis_section,
            ...         discharge_medications_section,
            ...         hospital_course_section,
            ...     ],
            ... )
            >>> xml = discharge.to_xml_string()
        """
        return DischargeSummary(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=sections,
            effective_time=effective_time,
            document_id=document_id,
            version=version,
        )

    @staticmethod
    def create_progress_note(
        patient: PatientProtocol,
        author: AuthorProtocol,
        custodian: OrganizationProtocol,
        sections: Optional[List[CDAElement]] = None,
        effective_time: Optional[datetime] = None,
        document_id: Optional[str] = None,
        version: CDAVersion = CDAVersion.R2_1,
    ) -> "ProgressNote":
        """
        Create a Progress Note document.

        The Progress Note documents a patient's clinical status during
        hospitalization or ongoing care. It is used to record observations,
        assessments, and plans during the course of treatment.

        Template IDs:
            - R2.1: 2.16.840.1.113883.10.20.22.1.9 (2015-08-01)
            - R2.0: 2.16.840.1.113883.10.20.22.1.9 (2014-06-09)

        Common sections:
            - Assessment and Plan
            - Subjective
            - Objective
            - Assessment
            - Plan of Care
            - Vital Signs
            - Results

        Args:
            patient: Patient data satisfying PatientProtocol
            author: Author data satisfying AuthorProtocol
            custodian: Custodian organization data satisfying OrganizationProtocol
            sections: List of section builders (optional)
            effective_time: Document creation time (current time if not provided)
            document_id: Document UUID (generated if not provided)
            version: C-CDA version (R2.1 by default)

        Returns:
            ProgressNote instance ready to build XML

        Examples:
            >>> progress_note = DocumentFactory.create_progress_note(
            ...     patient=my_patient,
            ...     author=my_provider,
            ...     custodian=my_clinic,
            ...     sections=[
            ...         assessment_and_plan_section,
            ...         vital_signs_section,
            ...     ],
            ... )
            >>> xml = progress_note.to_xml_string()
        """
        return ProgressNote(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=sections,
            effective_time=effective_time,
            document_id=document_id,
            version=version,
        )

    @staticmethod
    def create_consultation_note(
        patient: PatientProtocol,
        author: AuthorProtocol,
        custodian: OrganizationProtocol,
        sections: Optional[List[CDAElement]] = None,
        effective_time: Optional[datetime] = None,
        document_id: Optional[str] = None,
        version: CDAVersion = CDAVersion.R2_1,
    ) -> "ConsultationNote":
        """
        Create a Consultation Note document.

        The Consultation Note documents the opinion of a consulting provider
        regarding a patient's condition. It is used when one provider seeks
        input from another specialist or provider.

        Template IDs:
            - R2.1: 2.16.840.1.113883.10.20.22.1.4 (2015-08-01)
            - R2.0: 2.16.840.1.113883.10.20.22.1.4 (2014-06-09)

        Common sections:
            - Reason for Referral
            - History of Present Illness
            - Assessment and Plan
            - Medications
            - Allergies
            - Problems
            - Results

        Args:
            patient: Patient data satisfying PatientProtocol
            author: Author data satisfying AuthorProtocol
            custodian: Custodian organization data satisfying OrganizationProtocol
            sections: List of section builders (optional)
            effective_time: Document creation time (current time if not provided)
            document_id: Document UUID (generated if not provided)
            version: C-CDA version (R2.1 by default)

        Returns:
            ConsultationNote instance ready to build XML

        Examples:
            >>> consultation = DocumentFactory.create_consultation_note(
            ...     patient=my_patient,
            ...     author=consulting_provider,
            ...     custodian=consulting_organization,
            ...     sections=[
            ...         reason_for_referral_section,
            ...         assessment_section,
            ...     ],
            ... )
            >>> xml = consultation.to_xml_string()
        """
        return ConsultationNote(
            patient=patient,
            author=author,
            custodian=custodian,
            sections=sections,
            effective_time=effective_time,
            document_id=document_id,
            version=version,
        )


class ContinuityOfCareDocument(ClinicalDocument):
    """
    Continuity of Care Document (CCD).

    The CCD is designed to provide a snapshot summary of a patient's health status
    and care. It's the most commonly used C-CDA document type.

    This class extends ClinicalDocument with CCD-specific template IDs and
    document type codes.
    """

    # CCD-specific templates
    TEMPLATES = {
        CDAVersion.R2_1: [
            # General C-CDA header
            *ClinicalDocument.TEMPLATES[CDAVersion.R2_1],
            # CCD template
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.2",
                extension="2015-08-01",
                description="Continuity of Care Document R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            # General C-CDA header
            *ClinicalDocument.TEMPLATES[CDAVersion.R2_0],
            # CCD template
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.2",
                extension="2014-06-09",
                description="Continuity of Care Document R2.0",
            ),
        ],
    }

    def __init__(self, title: str = "Continuity of Care Document", **kwargs):
        """
        Initialize ContinuityOfCareDocument.

        Args:
            title: Document title (default: "Continuity of Care Document")
            **kwargs: Additional arguments passed to ClinicalDocument
        """
        super().__init__(title=title, **kwargs)

    def _add_document_code(self, doc):
        """Add CCD-specific document type code."""
        # LOINC code for Continuity of Care Document
        doc_code = Code(
            code="34133-9",
            system="LOINC",
            display_name="Summarization of Episode Note",
        )
        code_elem = doc_code.to_element()
        doc.append(code_elem)


class DischargeSummary(ClinicalDocument):
    """
    Discharge Summary document.

    The Discharge Summary provides a comprehensive summary of a patient's
    hospital stay, created at the time of discharge.

    This class extends ClinicalDocument with Discharge Summary-specific
    template IDs and document type codes.
    """

    # Discharge Summary templates
    TEMPLATES = {
        CDAVersion.R2_1: [
            # General C-CDA header
            *ClinicalDocument.TEMPLATES[CDAVersion.R2_1],
            # Discharge Summary template
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.8",
                extension="2015-08-01",
                description="Discharge Summary R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            # General C-CDA header
            *ClinicalDocument.TEMPLATES[CDAVersion.R2_0],
            # Discharge Summary template
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.8",
                extension="2014-06-09",
                description="Discharge Summary R2.0",
            ),
        ],
    }

    def __init__(self, title: str = "Discharge Summary", **kwargs):
        """
        Initialize DischargeSummary.

        Args:
            title: Document title (default: "Discharge Summary")
            **kwargs: Additional arguments passed to ClinicalDocument
        """
        super().__init__(title=title, **kwargs)

    def _add_document_code(self, doc):
        """Add Discharge Summary-specific document type code."""
        # LOINC code for Discharge Summary
        doc_code = Code(
            code="18842-5",
            system="LOINC",
            display_name="Discharge Summary",
        )
        code_elem = doc_code.to_element()
        doc.append(code_elem)


class ProgressNote(ClinicalDocument):
    """
    Progress Note document.

    The Progress Note documents a patient's clinical status during
    hospitalization or ongoing care.

    This class extends ClinicalDocument with Progress Note-specific
    template IDs and document type codes.
    """

    # Progress Note templates
    TEMPLATES = {
        CDAVersion.R2_1: [
            # General C-CDA header
            *ClinicalDocument.TEMPLATES[CDAVersion.R2_1],
            # Progress Note template
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.9",
                extension="2015-08-01",
                description="Progress Note R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            # General C-CDA header
            *ClinicalDocument.TEMPLATES[CDAVersion.R2_0],
            # Progress Note template
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.9",
                extension="2014-06-09",
                description="Progress Note R2.0",
            ),
        ],
    }

    def __init__(self, title: str = "Progress Note", **kwargs):
        """
        Initialize ProgressNote.

        Args:
            title: Document title (default: "Progress Note")
            **kwargs: Additional arguments passed to ClinicalDocument
        """
        super().__init__(title=title, **kwargs)

    def _add_document_code(self, doc):
        """Add Progress Note-specific document type code."""
        # LOINC code for Progress Note
        doc_code = Code(
            code="11506-3",
            system="LOINC",
            display_name="Progress Note",
        )
        code_elem = doc_code.to_element()
        doc.append(code_elem)


class ConsultationNote(ClinicalDocument):
    """
    Consultation Note document.

    The Consultation Note documents the opinion of a consulting provider
    regarding a patient's condition.

    This class extends ClinicalDocument with Consultation Note-specific
    template IDs and document type codes.
    """

    # Consultation Note templates
    TEMPLATES = {
        CDAVersion.R2_1: [
            # General C-CDA header
            *ClinicalDocument.TEMPLATES[CDAVersion.R2_1],
            # Consultation Note template
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.4",
                extension="2015-08-01",
                description="Consultation Note R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            # General C-CDA header
            *ClinicalDocument.TEMPLATES[CDAVersion.R2_0],
            # Consultation Note template
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.4",
                extension="2014-06-09",
                description="Consultation Note R2.0",
            ),
        ],
    }

    def __init__(self, title: str = "Consultation Note", **kwargs):
        """
        Initialize ConsultationNote.

        Args:
            title: Document title (default: "Consultation Note")
            **kwargs: Additional arguments passed to ClinicalDocument
        """
        super().__init__(title=title, **kwargs)

    def _add_document_code(self, doc):
        """Add Consultation Note-specific document type code."""
        # LOINC code for Consultation Note
        doc_code = Code(
            code="11488-4",
            system="LOINC",
            display_name="Consultation Note",
        )
        code_elem = doc_code.to_element()
        doc.append(code_elem)
