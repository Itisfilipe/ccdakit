"""Problem-related protocols for C-CDA documents."""

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


class ProblemProtocol(Protocol):
    """Problem/diagnosis data contract."""

    @property
    def name(self) -> str:
        """
        Human-readable problem name.

        Returns:
            Problem name
        """
        ...

    @property
    def code(self) -> str:
        """
        SNOMED CT or ICD-10 code.

        Returns:
            Problem code
        """
        ...

    @property
    def code_system(self) -> str:
        """
        Code system: 'SNOMED' or 'ICD-10'.

        Returns:
            Code system name
        """
        ...

    @property
    def onset_date(self) -> Optional[date]:
        """
        Date problem was identified/started.

        Returns:
            Onset date or None
        """
        ...

    @property
    def resolved_date(self) -> Optional[date]:
        """
        Date problem was resolved (None if ongoing).

        Returns:
            Resolved date or None
        """
        ...

    @property
    def status(self) -> str:
        """
        Status: 'active', 'inactive', 'resolved'.

        Returns:
            Problem status
        """
        ...

    @property
    def persistent_id(self) -> Optional[PersistentIDProtocol]:
        """
        Persistent ID across document versions.

        Returns:
            Persistent ID or None
        """
        ...
