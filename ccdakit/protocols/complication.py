"""Complication-related protocols for C-CDA documents.

This module defines protocols for representing complications that occurred
during or around the time of a procedure, as documented in the Complications
Section (Template ID: 2.16.840.1.113883.10.20.22.2.37).

Complications are represented using Problem Observations and may include
both known risks and unanticipated problems.
"""

from datetime import date
from typing import Optional, Protocol

from ccdakit.protocols.problem import PersistentIDProtocol


class ComplicationProtocol(Protocol):
    """
    Complication data contract.

    Represents a problem that occurred during or around the time of a procedure.
    This protocol extends the concept of a problem observation to specifically
    track complications as defined in C-CDA 2.1 Complications Section.

    The Complications Section (2.16.840.1.113883.10.20.22.2.37) contains
    Problem Observation entries (2.16.840.1.113883.10.20.22.4.4) that
    represent complications.

    Typical use cases:
        - Post-operative complications
        - Adverse events during procedures
        - Unexpected problems following medical interventions

    Examples:
        Implementing this protocol for a surgical complication:

        >>> class SurgicalComplication:
        ...     @property
        ...     def name(self) -> str:
        ...         return "Postoperative wound infection"
        ...
        ...     @property
        ...     def code(self) -> str:
        ...         return "432119003"  # SNOMED CT
        ...
        ...     @property
        ...     def code_system(self) -> str:
        ...         return "SNOMED"
        ...
        ...     @property
        ...     def onset_date(self) -> date:
        ...         return date(2024, 1, 15)  # Date complication was identified
        ...
        ...     @property
        ...     def resolved_date(self) -> Optional[date]:
        ...         return date(2024, 2, 1)  # Date complication resolved
        ...
        ...     @property
        ...     def status(self) -> str:
        ...         return "resolved"
        ...
        ...     @property
        ...     def severity(self) -> Optional[str]:
        ...         return "moderate"
        ...
        ...     @property
        ...     def related_procedure_code(self) -> Optional[str]:
        ...         return "80146002"  # Appendectomy
        ...
        ...     @property
        ...     def persistent_id(self) -> Optional[PersistentIDProtocol]:
        ...         return None
    """

    @property
    def name(self) -> str:
        """
        Human-readable complication name.

        Returns:
            Complication name/description

        Examples:
            - "Postoperative bleeding"
            - "Surgical site infection"
            - "Deep vein thrombosis"
            - "Respiratory failure"
        """
        ...

    @property
    def code(self) -> str:
        """
        SNOMED CT or ICD-10 code for the complication.

        The code should be from the Problem Value Set
        (2.16.840.1.113883.3.88.12.3221.7.4) as specified in
        Problem Observation template.

        Returns:
            Complication code

        Examples:
            - "432119003" (Postoperative wound infection)
            - "83132003" (Postoperative hemorrhage)
            - "609433001" (Postoperative sepsis)
        """
        ...

    @property
    def code_system(self) -> str:
        """
        Code system identifier.

        Returns:
            'SNOMED' or 'ICD-10'

        Note:
            SNOMED CT is preferred for problem/complication coding.
        """
        ...

    @property
    def onset_date(self) -> Optional[date]:
        """
        Date the complication was identified or started.

        This represents the effectiveTime/low in the Problem Observation.
        It should be the time when the complication became clinically active,
        typically during or shortly after the related procedure.

        Returns:
            Onset date or None if unknown

        Note:
            For complications, this is often shortly after the procedure
            that led to the complication.
        """
        ...

    @property
    def resolved_date(self) -> Optional[date]:
        """
        Date the complication was resolved.

        This represents the effectiveTime/high in the Problem Observation.
        If the complication is known to be resolved but the exact date is
        unknown, implementations should use None and indicate this through
        other means in the document.

        Returns:
            Resolved date or None if ongoing or unknown

        Note:
            - None indicates the complication is still active or resolution
              date is unknown
            - Present value indicates the complication has been resolved
        """
        ...

    @property
    def status(self) -> str:
        """
        Clinical status of the complication.

        Returns:
            Status value: 'active', 'inactive', or 'resolved'

        Examples:
            - 'active': Complication is currently present
            - 'resolved': Complication has been resolved
            - 'inactive': Complication is no longer active but not formally resolved

        Note:
            If resolved_date is present, status should typically be 'resolved'.
        """
        ...

    @property
    def severity(self) -> Optional[str]:
        """
        Severity of the complication.

        Returns:
            Severity level: 'mild', 'moderate', 'severe', or None if not specified

        Note:
            While not explicitly required by the Complications Section,
            severity can be captured through Problem Status observations
            or qualifiers in the Problem Observation.
        """
        ...

    @property
    def related_procedure_code(self) -> Optional[str]:
        """
        Code for the procedure that led to this complication.

        This provides context linking the complication to a specific
        procedure, though this relationship may also be implicit from
        document structure (e.g., complications section in procedure note).

        Returns:
            Procedure code (SNOMED CT or CPT) or None

        Examples:
            - "80146002" (Appendectomy)
            - "232717009" (Coronary artery bypass grafting)
            - "447566006" (Surgical repair of heart)

        Note:
            This is optional and may be inferred from the containing
            procedure note or operative note.
        """
        ...

    @property
    def persistent_id(self) -> Optional[PersistentIDProtocol]:
        """
        Persistent identifier across document versions.

        This allows the same complication to be tracked across multiple
        documents and updates.

        Returns:
            Persistent ID or None

        Note:
            Useful for tracking the complication's evolution across
            multiple procedure notes or follow-up documents.
        """
        ...
