"""Preoperative diagnosis-related protocols for C-CDA documents.

This module defines the protocol for preoperative diagnosis data used in
surgical operative notes. The preoperative diagnosis represents the
surgical diagnosis or diagnoses assigned to the patient before the surgical
procedure and is the reason for the surgery.

Template IDs:
    Section: 2.16.840.1.113883.10.20.22.2.34 (Preoperative Diagnosis Section V3)
    Entry: 2.16.840.1.113883.10.20.22.4.65 (Preoperative Diagnosis V3)
"""

from datetime import date
from typing import Optional, Protocol


class PersistentIDProtocol(Protocol):
    """Persistent identifier protocol."""

    @property
    def root(self) -> str:
        """
        OID or UUID identifying the assigning authority.

        Returns:
            Root identifier (OID or UUID)
        """
        ...

    @property
    def extension(self) -> str:
        """
        Unique identifier within the root's namespace.

        Returns:
            Extension identifier
        """
        ...


class PreoperativeDiagnosisProtocol(Protocol):
    """
    Preoperative diagnosis data contract.

    This protocol defines the data structure for surgical diagnoses assigned
    to a patient before a surgical procedure. The preoperative diagnosis is,
    in the surgeon's opinion, the diagnosis that will be confirmed during surgery.

    The preoperative diagnosis is represented as a Problem Observation within
    an Act wrapper in the C-CDA structure.

    Examples:
        >>> class MyPreopDiagnosis:
        ...     @property
        ...     def name(self) -> str:
        ...         return "Appendicitis"
        ...
        ...     @property
        ...     def code(self) -> str:
        ...         return "74400008"
        ...
        ...     @property
        ...     def code_system(self) -> str:
        ...         return "SNOMED"
        ...
        ...     @property
        ...     def diagnosis_date(self) -> date:
        ...         return date(2024, 3, 15)
        ...
        ...     @property
        ...     def status(self) -> str:
        ...         return "active"
        ...
        ...     @property
        ...     def persistent_id(self) -> Optional[PersistentIDProtocol]:
        ...         return None
        >>> diagnosis = MyPreopDiagnosis()
        >>> diagnosis.name
        'Appendicitis'
    """

    @property
    def name(self) -> str:
        """
        Human-readable diagnosis name.

        This should be a clear description of the preoperative diagnosis
        that the surgeon believes will be confirmed during surgery.

        Returns:
            Diagnosis name

        Examples:
            >>> diagnosis.name
            'Acute Appendicitis'
        """
        ...

    @property
    def code(self) -> str:
        """
        SNOMED CT or ICD-10 code for the diagnosis.

        The code should represent the specific surgical diagnosis.
        SNOMED CT codes are preferred for clinical interoperability.

        Returns:
            Diagnosis code

        Examples:
            >>> diagnosis.code
            '74400008'  # SNOMED CT code for Appendicitis
        """
        ...

    @property
    def code_system(self) -> str:
        """
        Code system: 'SNOMED' or 'ICD-10'.

        Indicates which coding system is used for the diagnosis code.
        SNOMED CT (SNOMED) is preferred for interoperability.

        Returns:
            Code system name ('SNOMED' or 'ICD-10')

        Examples:
            >>> diagnosis.code_system
            'SNOMED'
        """
        ...

    @property
    def diagnosis_date(self) -> Optional[date]:
        """
        Date the preoperative diagnosis was made.

        This is typically the date when the surgeon determined the
        diagnosis that necessitates the surgical procedure.

        Returns:
            Diagnosis date or None

        Examples:
            >>> diagnosis.diagnosis_date
            date(2024, 3, 15)
        """
        ...

    @property
    def status(self) -> str:
        """
        Status of the diagnosis: typically 'active'.

        For preoperative diagnoses, this is usually 'active' since
        it represents the current reason for surgery.

        Returns:
            Diagnosis status ('active', 'inactive', 'resolved')

        Examples:
            >>> diagnosis.status
            'active'
        """
        ...

    @property
    def persistent_id(self) -> Optional[PersistentIDProtocol]:
        """
        Persistent ID across document versions.

        This identifier allows the diagnosis to be tracked across
        multiple versions of the clinical document.

        Returns:
            Persistent ID or None

        Examples:
            >>> diagnosis.persistent_id.root
            '2.16.840.1.113883.3.HOSPITAL'
            >>> diagnosis.persistent_id.extension
            'PREOP-DIAG-12345'
        """
        ...
