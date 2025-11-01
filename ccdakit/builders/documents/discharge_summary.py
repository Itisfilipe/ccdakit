"""Discharge Summary Document builder.

The Discharge Summary document type summarizes a patient's hospital stay and provides
discharge instructions and follow-up care information. It's a critical document for
care transitions from inpatient to outpatient settings.

Reference: HL7 C-CDA Implementation Guide
Template ID: 2.16.840.1.113883.10.20.22.1.8
"""

from datetime import datetime
from typing import Optional, Sequence

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.document import ClinicalDocument
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.author import AuthorProtocol, OrganizationProtocol
from ccdakit.protocols.patient import PatientProtocol


class DischargeSummary(ClinicalDocument):
    """
    Discharge Summary Document builder.

    The Discharge Summary provides a comprehensive summary of a patient's hospital
    stay, including admission details, hospital course, discharge diagnoses, medications,
    and follow-up plans. It's essential for continuity of care as patients transition
    from hospital to home or other care settings.

    Typical Sections (recommended for completeness):
    - Admission Diagnosis Section
    - Admission Medications Section
    - Allergies Section
    - Chief Complaint Section
    - Discharge Diagnosis Section
    - Discharge Medications Section
    - Hospital Course Section
    - Hospital Discharge Diagnosis Section
    - Hospital Discharge Instructions Section
    - Hospital Discharge Medications Section
    - Plan of Treatment Section
    - Procedures Section
    - Reason for Visit Section

    Usage:
        >>> from ccdakit.builders.documents import DischargeSummary
        >>> from ccdakit.builders.sections import (
        ...     DischargeMedicationsSection,
        ...     HospitalDischargeInstructionsSection,
        ... )
        >>>
        >>> doc = DischargeSummary(
        ...     patient=patient_data,
        ...     author=author_data,
        ...     custodian=hospital_org,
        ...     sections=[
        ...         DischargeMedicationsSection(medications=discharge_meds),
        ...         HospitalDischargeInstructionsSection(instructions=instructions),
        ...     ],
        ...     admission_date=datetime(2024, 1, 15),
        ...     discharge_date=datetime(2024, 1, 20),
        ... )
        >>> xml_string = doc.to_xml_string()
    """

    # Discharge Summary templates include base C-CDA template and DS-specific template
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.1",
                extension="2015-08-01",
                description="C-CDA R2.1",
            ),
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.8",
                extension="2015-08-01",
                description="Discharge Summary R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.1",
                extension="2014-06-09",
                description="C-CDA R2.0",
            ),
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.1.8",
                extension="2014-06-09",
                description="Discharge Summary R2.0",
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
        title: str = "Discharge Summary",
        effective_time: Optional[datetime] = None,
        admission_date: Optional[datetime] = None,
        discharge_date: Optional[datetime] = None,
        **kwargs,
    ):
        """
        Initialize Discharge Summary builder.

        Args:
            patient: Patient data satisfying PatientProtocol
            author: Author data satisfying AuthorProtocol
            custodian: Custodian organization (hospital) data
            sections: List of section builders (discharge-specific sections recommended)
            document_id: Document UUID (generated if not provided)
            title: Document title (defaults to "Discharge Summary")
            effective_time: Document creation time (discharge date if not provided)
            admission_date: Hospital admission date (optional but recommended)
            discharge_date: Hospital discharge date (optional but recommended)
            **kwargs: Additional arguments passed to ClinicalDocument
        """
        # Use discharge_date as effective_time if provided and effective_time is not
        if effective_time is None and discharge_date is not None:
            effective_time = discharge_date

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

        self.admission_date = admission_date
        self.discharge_date = discharge_date

    def _add_document_code(self, doc: etree._Element) -> None:
        """
        Add Discharge Summary document type code.

        Uses LOINC code 18842-5: "Discharge Summarization Note"
        This is the standard code for Discharge Summary documents.

        Args:
            doc: ClinicalDocument element
        """
        # LOINC code for Discharge Summary
        doc_code = Code(
            code="18842-5",
            system="LOINC",
            display_name="Discharge Summarization Note",
        )
        code_elem = doc_code.to_element()
        doc.append(code_elem)

    def build(self) -> etree.Element:
        """
        Build Discharge Summary XML element.

        Overrides parent build() to add discharge-specific elements like
        documentationOf/serviceEvent and componentOf/encompassingEncounter
        for admission/discharge dates.

        Returns:
            lxml Element for Discharge Summary document
        """
        # Build base document
        doc = super().build()

        # Add documentationOf/serviceEvent for admission and discharge dates
        if self.admission_date or self.discharge_date:
            self._add_service_event(doc)
            # Also add componentOf/encompassingEncounter (required for discharge summary)
            self._add_encompassing_encounter(doc)

        return doc

    def _add_service_event(self, doc: etree._Element) -> None:
        """
        Add documentationOf/serviceEvent with admission and discharge dates.

        This provides the hospital encounter timeframe in a structured way.

        Per C-CDA spec (CONF:1198-14839):
        - serviceEvent SHOULD contain zero or more [0..*] performer

        Args:
            doc: ClinicalDocument element
        """
        from ccdakit.builders.common import EffectiveTime

        # Create documentationOf element
        documentation_of = etree.Element(f"{{{self.NS}}}documentationOf")

        # Create serviceEvent element
        service_event = etree.SubElement(documentation_of, f"{{{self.NS}}}serviceEvent")
        service_event.set("classCode", "PCPR")  # Care Provision

        # Add effectiveTime with admission (low) and discharge (high)
        effective_time = etree.SubElement(service_event, f"{{{self.NS}}}effectiveTime")

        if self.admission_date:
            low = etree.SubElement(effective_time, f"{{{self.NS}}}low")
            low.set("value", EffectiveTime._format_datetime(self.admission_date))

        if self.discharge_date:
            high = etree.SubElement(effective_time, f"{{{self.NS}}}high")
            high.set("value", EffectiveTime._format_datetime(self.discharge_date))

        # Add performer (SHOULD per CONF:1198-14839)
        # Use the document author as the performer
        self._add_service_event_performer(service_event)

        # Insert documentationOf before component (body) if it exists
        # Otherwise append to end
        component_elem = doc.find(f".//{{{self.NS}}}component")
        if component_elem is not None:
            # Find index of component
            doc.insert(list(doc).index(component_elem), documentation_of)
        else:
            doc.append(documentation_of)

    def _add_service_event_performer(self, service_event: etree._Element) -> None:
        """
        Add performer to serviceEvent.

        Per C-CDA spec (CONF:1198-14839):
        - serviceEvent SHOULD contain zero or more [0..*] performer

        Uses the document author as the performer.

        Args:
            service_event: serviceEvent element
        """
        from ccdakit.builders.common import Code, Identifier

        # Create performer element
        performer = etree.SubElement(service_event, f"{{{self.NS}}}performer")
        performer.set("typeCode", "PRF")  # Performer

        # Add assignedEntity
        assigned_entity = etree.SubElement(performer, f"{{{self.NS}}}assignedEntity")

        # Add ID (use NPI if available)
        id_elem = etree.SubElement(assigned_entity, f"{{{self.NS}}}id")
        if self.author.npi:
            id_elem.set("root", "2.16.840.1.113883.4.6")  # NPI OID
            id_elem.set("extension", self.author.npi)
        else:
            id_elem.set("nullFlavor", "NI")

        # Add code (physician specialty)
        code_elem = Code(
            code="200000000X",  # Allopathic & Osteopathic Physicians
            system="2.16.840.1.113883.6.101",  # NUCC Provider Taxonomy
            display_name="Physician",
        ).to_element()
        code_elem.tag = f"{{{self.NS}}}code"
        assigned_entity.append(code_elem)

        # Add assignedPerson with name
        assigned_person = etree.SubElement(assigned_entity, f"{{{self.NS}}}assignedPerson")
        name = etree.SubElement(assigned_person, f"{{{self.NS}}}name")

        # Add given name
        given = etree.SubElement(name, f"{{{self.NS}}}given")
        given.text = self.author.first_name

        # Add family name
        family = etree.SubElement(name, f"{{{self.NS}}}family")
        family.text = self.author.last_name

    def _add_encompassing_encounter(self, doc: etree._Element) -> None:
        """
        Add componentOf/encompassingEncounter for discharge summary.

        This is required for discharge summary documents to represent the hospital stay.

        Args:
            doc: ClinicalDocument element
        """
        import uuid

        # Create componentOf element
        component_of = etree.Element(f"{{{self.NS}}}componentOf")

        # Create encompassingEncounter element
        encompassing_encounter = etree.SubElement(
            component_of, f"{{{self.NS}}}encompassingEncounter"
        )

        # Add ID for the encounter
        id_elem = etree.SubElement(encompassing_encounter, f"{{{self.NS}}}id")
        id_elem.set("root", "2.16.840.1.113883.19")
        id_elem.set("extension", str(uuid.uuid4()))

        # Add code for encounter type (if available)
        code_elem = etree.SubElement(encompassing_encounter, f"{{{self.NS}}}code")
        code_elem.set("code", "IMP")  # Inpatient encounter
        code_elem.set("codeSystem", "2.16.840.1.113883.5.4")  # ActCode
        code_elem.set("codeSystemName", "ActCode")
        code_elem.set("displayName", "inpatient encounter")

        # Add effectiveTime with admission (low) and discharge (high)
        effective_time = etree.SubElement(encompassing_encounter, f"{{{self.NS}}}effectiveTime")

        if self.admission_date:
            low = etree.SubElement(effective_time, f"{{{self.NS}}}low")
            low.set("value", self.admission_date.strftime("%Y%m%d%H%M%S"))

        if self.discharge_date:
            high = etree.SubElement(effective_time, f"{{{self.NS}}}high")
            high.set("value", self.discharge_date.strftime("%Y%m%d%H%M%S"))

        # Add dischargeDispositionCode (required for discharge summary)
        discharge_disp = etree.SubElement(
            encompassing_encounter, f"{{{self.NS}}}dischargeDispositionCode"
        )
        # Default to "01" - Home or self care (routine discharge)
        discharge_disp.set("code", "01")
        discharge_disp.set("codeSystem", "2.16.840.1.113883.12.112")  # HL7 DischargeDisposition
        discharge_disp.set("displayName", "Home or self care")

        # Insert componentOf before component (body) if it exists
        # Otherwise append to end
        component_elem = doc.find(f".//{{{self.NS}}}component")
        if component_elem is not None:
            # Find index of component
            doc.insert(list(doc).index(component_elem), component_of)
        else:
            doc.append(component_of)

    def validate_discharge_sections(self) -> "tuple[bool, list[str]]":
        """
        Validate that recommended discharge-specific sections are present.

        While C-CDA allows flexibility, discharge summaries should ideally include
        certain sections for completeness and clinical utility.

        Returns:
            Tuple of (has_recommended_sections, list of missing recommended sections)

        Example:
            >>> has_all, missing = doc.validate_discharge_sections()
            >>> if not has_all:
            ...     print(f"Recommended sections missing: {', '.join(missing)}")
        """
        recommended_section_templates = {
            "2.16.840.1.113883.10.20.22.2.11": "Discharge Medications Section",
            "2.16.840.1.113883.10.20.22.2.41": "Hospital Discharge Instructions Section",
            "2.16.840.1.113883.10.20.22.2.10": "Plan of Treatment Section",
        }

        # Get template IDs from all sections
        section_template_ids = set()
        for section in self.sections:
            if hasattr(section, "TEMPLATES") and self.version in section.TEMPLATES:
                for template in section.TEMPLATES[self.version]:
                    section_template_ids.add(template.root)

        # Check for missing recommended sections
        missing_sections = []
        for template_id, section_name in recommended_section_templates.items():
            if template_id not in section_template_ids:
                missing_sections.append(section_name)

        return len(missing_sections) == 0, missing_sections
