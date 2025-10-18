"""Author and organization-related protocols for C-CDA documents."""

from datetime import datetime
from typing import Optional, Protocol, Sequence

from ccdakit.protocols.patient import AddressProtocol, TelecomProtocol


class OrganizationProtocol(Protocol):
    """Organization/facility data contract."""

    @property
    def name(self) -> str:
        """
        Organization name.

        Returns:
            Organization name
        """
        ...

    @property
    def npi(self) -> Optional[str]:
        """
        National Provider Identifier.

        Returns:
            NPI or None
        """
        ...

    @property
    def tin(self) -> Optional[str]:
        """
        Tax Identification Number.

        Returns:
            TIN or None
        """
        ...

    @property
    def oid_root(self) -> Optional[str]:
        """
        Organization's OID namespace.

        Returns:
            OID root or None
        """
        ...

    @property
    def addresses(self) -> Sequence[AddressProtocol]:
        """
        List of organization addresses.

        Returns:
            List of addresses
        """
        ...

    @property
    def telecoms(self) -> Sequence[TelecomProtocol]:
        """
        List of organization contact methods.

        Returns:
            List of contact methods
        """
        ...


class AuthorProtocol(Protocol):
    """Author data contract for CDA header."""

    @property
    def first_name(self) -> str:
        """
        Author's first name.

        Returns:
            First name
        """
        ...

    @property
    def last_name(self) -> str:
        """
        Author's last name.

        Returns:
            Last name
        """
        ...

    @property
    def middle_name(self) -> Optional[str]:
        """
        Author's middle name or initial.

        Returns:
            Middle name or None
        """
        ...

    @property
    def npi(self) -> Optional[str]:
        """
        National Provider Identifier.

        Returns:
            NPI or None
        """
        ...

    @property
    def addresses(self) -> Sequence[AddressProtocol]:
        """
        List of author addresses.

        Returns:
            List of addresses
        """
        ...

    @property
    def telecoms(self) -> Sequence[TelecomProtocol]:
        """
        List of author contact methods.

        Returns:
            List of contact methods
        """
        ...

    @property
    def time(self) -> datetime:
        """
        Time when the document was authored.

        Returns:
            Authoring time
        """
        ...

    @property
    def organization(self) -> Optional[OrganizationProtocol]:
        """
        Author's organization/facility.

        Returns:
            Organization or None
        """
        ...
