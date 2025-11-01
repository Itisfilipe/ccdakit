"""Protocol for Procedure data in C-CDA documents."""

from datetime import date, datetime
from typing import Optional, Protocol


class ProcedureProtocol(Protocol):
    """
    Protocol defining the interface for procedure data.

    Represents surgical, diagnostic, or therapeutic procedures.
    Used with ProcedureActivity and ProceduresSection builders.
    """

    @property
    def name(self) -> str:
        """Procedure name/description (e.g., 'Appendectomy')."""
        ...

    @property
    def code(self) -> str:
        """
        Procedure code (e.g., '80146002' from SNOMED CT).

        Should be from one of: LOINC, SNOMED CT, CPT-4, ICD10 PCS, HCPCS, or CDT-2.
        """
        ...

    @property
    def code_system(self) -> str:
        """
        Code system for the procedure code.

        Examples: 'SNOMED CT', 'CPT-4', 'LOINC', 'ICD10 PCS'
        """
        ...

    @property
    def date(self) -> Optional[date | datetime]:
        """
        Date/time when the procedure was performed.

        Can be a date or datetime. Optional but recommended.
        """
        ...

    @property
    def status(self) -> str:
        """
        Status of the procedure.

        Common values: 'completed', 'active', 'aborted', 'cancelled'
        """
        ...

    @property
    def target_site(self) -> Optional[str]:
        """
        Target body site where procedure was performed.

        Optional. Example: 'Right knee', 'Abdomen'
        """
        ...

    @property
    def target_site_code(self) -> Optional[str]:
        """
        Code for the target body site (from SNOMED CT).

        Optional. Example: '72696002' for right knee
        """
        ...

    @property
    def performer_name(self) -> Optional[str]:
        """
        Name of the person/entity who performed the procedure.

        Optional. Example: 'Dr. Jane Smith'
        """
        ...

    @property
    def performer_address(self) -> Optional[str]:
        """
        Address of the performer.

        Optional but required if performer_name is present per C-CDA spec.
        Example: '123 Main St, City, State 12345'
        """
        ...

    @property
    def performer_telecom(self) -> Optional[str]:
        """
        Telecom contact for the performer.

        Optional but required if performer_name is present per C-CDA spec.
        Example: 'tel:+1-555-555-1234' or 'mailto:provider@example.com'
        """
        ...
