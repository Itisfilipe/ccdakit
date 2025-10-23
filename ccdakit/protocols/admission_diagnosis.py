"""Admission diagnosis-related protocols for C-CDA documents.

This module defines protocols for the Admission Diagnosis Section (Template ID:
2.16.840.1.113883.10.20.22.2.43) and Hospital Admission Diagnosis entry (Template
ID: 2.16.840.1.113883.10.20.22.4.34).

The Admission Diagnosis Section contains a narrative description of the problems or
diagnoses identified by the clinician at the time of the patient's admission. This
section may contain a coded entry which represents the admitting diagnoses.
"""

from datetime import date
from typing import Optional, Protocol

from ccdakit.protocols.problem import PersistentIDProtocol


class AdmissionDiagnosisProtocol(Protocol):
    """
    Admission diagnosis data contract.

    Represents problems or diagnoses identified by the clinician at the time of
    the patient's admission. This protocol follows the Hospital Admission Diagnosis
    (V3) template (2.16.840.1.113883.10.20.22.4.34).

    The admission diagnosis may contain multiple Problem Observations to represent
    multiple diagnoses for a hospital admission.

    Template Reference:
        Section: 2.16.840.1.113883.10.20.22.2.43 (Admission Diagnosis Section V3)
        Entry: 2.16.840.1.113883.10.20.22.4.34 (Hospital Admission Diagnosis V3)

    Required Elements:
        - name: Human-readable diagnosis name
        - code: SNOMED CT or ICD-10 diagnosis code
        - code_system: Code system identifier ('SNOMED' or 'ICD-10')

    Optional Elements:
        - admission_date: Date of hospital admission
        - diagnosis_date: Date diagnosis was identified
        - persistent_id: Persistent identifier across document versions

    Example:
        >>> class MyAdmissionDiagnosis:
        ...     @property
        ...     def name(self):
        ...         return "Acute Myocardial Infarction"
        ...
        ...     @property
        ...     def code(self):
        ...         return "57054005"
        ...
        ...     @property
        ...     def code_system(self):
        ...         return "SNOMED"
        ...
        ...     @property
        ...     def admission_date(self):
        ...         return date(2024, 1, 15)
        ...
        ...     @property
        ...     def diagnosis_date(self):
        ...         return date(2024, 1, 15)
        ...
        ...     @property
        ...     def persistent_id(self):
        ...         return None
    """

    @property
    def name(self) -> str:
        """
        Human-readable admission diagnosis name.

        This is the display name for the diagnosis identified at admission.

        Returns:
            Diagnosis name (e.g., "Acute Myocardial Infarction")

        Example:
            >>> diagnosis.name
            'Acute Myocardial Infarction'
        """
        ...

    @property
    def code(self) -> str:
        """
        SNOMED CT or ICD-10 diagnosis code.

        The coded value representing the admission diagnosis. SNOMED CT is
        preferred, but ICD-10 codes are also commonly used.

        Returns:
            Diagnosis code (e.g., "57054005" for SNOMED, "I21.9" for ICD-10)

        Example:
            >>> diagnosis.code
            '57054005'
        """
        ...

    @property
    def code_system(self) -> str:
        """
        Code system: 'SNOMED' or 'ICD-10'.

        Identifies the coding system used for the diagnosis code.

        Returns:
            Code system name ('SNOMED' or 'ICD-10')

        Example:
            >>> diagnosis.code_system
            'SNOMED'
        """
        ...

    @property
    def admission_date(self) -> Optional[date]:
        """
        Date of hospital admission.

        The date when the patient was admitted to the hospital. May be None
        if the admission date is not available.

        Returns:
            Admission date or None

        Example:
            >>> diagnosis.admission_date
            datetime.date(2024, 1, 15)
        """
        ...

    @property
    def diagnosis_date(self) -> Optional[date]:
        """
        Date diagnosis was identified.

        The date when this specific diagnosis was identified by the clinician.
        This may be the same as or different from the admission date. May be
        None if the diagnosis date is not available.

        Returns:
            Diagnosis identification date or None

        Example:
            >>> diagnosis.diagnosis_date
            datetime.date(2024, 1, 15)
        """
        ...

    @property
    def persistent_id(self) -> Optional[PersistentIDProtocol]:
        """
        Persistent ID across document versions.

        Provides a consistent identifier for this diagnosis across different
        versions of the clinical document. This is optional but recommended
        for tracking diagnoses over time.

        Returns:
            Persistent ID or None

        Example:
            >>> diagnosis.persistent_id.root
            '2.16.840.1.113883.3.TEST'
            >>> diagnosis.persistent_id.extension
            'ADM-DIAG-001'
        """
        ...
