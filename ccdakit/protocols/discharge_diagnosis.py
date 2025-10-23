"""Discharge diagnosis-related protocols for C-CDA documents.

This module defines protocols for discharge diagnoses, which represent problems
or diagnoses present at the time of discharge that occurred during hospitalization.

Template IDs:
    - Discharge Diagnosis Section (V3): 2.16.840.1.113883.10.20.22.2.24
    - Hospital Discharge Diagnosis (V3): 2.16.840.1.113883.10.20.22.4.33
    - Problem Observation (V4): 2.16.840.1.113883.10.20.22.4.4

Reference:
    C-CDA 2.1 Implementation Guide
"""

from datetime import date
from typing import Optional, Protocol


class DischargeDiagnosisProtocol(Protocol):
    """
    Discharge diagnosis data contract.

    This protocol defines the structure for a discharge diagnosis, which represents
    a problem or diagnosis present at the time of discharge. Discharge diagnoses
    document conditions that occurred during hospitalization or need ongoing
    monitoring after discharge.

    The protocol reuses the problem/diagnosis data model since discharge diagnoses
    are conceptually the same as problems, just in a specific discharge context.

    Template ID: 2.16.840.1.113883.10.20.22.2.24 (Section)
                 2.16.840.1.113883.10.20.22.4.33 (Entry)

    Examples:
        >>> class MyDischargeDiagnosis:
        ...     @property
        ...     def name(self) -> str:
        ...         return "Acute Myocardial Infarction"
        ...
        ...     @property
        ...     def code(self) -> str:
        ...         return "57054005"
        ...
        ...     @property
        ...     def code_system(self) -> str:
        ...         return "SNOMED"
        ...
        ...     @property
        ...     def diagnosis_date(self) -> date:
        ...         return date(2024, 10, 15)
        ...
        ...     @property
        ...     def status(self) -> str:
        ...         return "active"
    """

    @property
    def name(self) -> str:
        """
        Human-readable diagnosis name.

        This should be a clear, clinical description of the discharge diagnosis
        that can be displayed to users.

        Returns:
            Diagnosis name (e.g., "Acute Myocardial Infarction")
        """
        ...

    @property
    def code(self) -> str:
        """
        Standard medical code for the diagnosis.

        Should be a SNOMED CT or ICD-10 code representing the diagnosis.
        SNOMED CT is preferred when available.

        Returns:
            Diagnosis code (e.g., "57054005" for AMI in SNOMED)
        """
        ...

    @property
    def code_system(self) -> str:
        """
        Code system identifier.

        Indicates which terminology system the code comes from.

        Returns:
            Code system name: 'SNOMED', 'ICD-10', or other standard
        """
        ...

    @property
    def diagnosis_date(self) -> Optional[date]:
        """
        Date the diagnosis was identified or became relevant.

        For discharge diagnoses, this is typically the date the condition
        was diagnosed during the hospital stay. May be None if the exact
        date is unknown.

        Returns:
            Diagnosis date or None if unknown
        """
        ...

    @property
    def resolved_date(self) -> Optional[date]:
        """
        Date the diagnosis was resolved.

        For most discharge diagnoses, this will be None since they represent
        ongoing conditions requiring monitoring. If the condition was resolved
        during hospitalization, this date should be set.

        Returns:
            Resolution date or None if ongoing
        """
        ...

    @property
    def status(self) -> str:
        """
        Current status of the diagnosis.

        Valid values align with C-CDA Problem Status value set:
        - 'active': Condition is ongoing
        - 'inactive': Condition is not currently active but not fully resolved
        - 'resolved': Condition has been fully resolved

        Most discharge diagnoses will be 'active' since they represent
        conditions requiring ongoing care or monitoring.

        Returns:
            Diagnosis status
        """
        ...

    @property
    def discharge_disposition(self) -> Optional[str]:
        """
        Patient's discharge disposition related to this diagnosis.

        Optional field indicating where the patient was discharged to,
        particularly relevant for this diagnosis (e.g., "home", "skilled nursing
        facility", "acute care hospital").

        Returns:
            Discharge disposition or None
        """
        ...

    @property
    def priority(self) -> Optional[int]:
        """
        Priority ranking of this diagnosis.

        Optional field for ranking diagnoses by importance. Lower numbers
        indicate higher priority. For example, priority=1 would be the primary
        discharge diagnosis.

        Returns:
            Priority ranking (1-based) or None
        """
        ...
