"""Advance Directive-related protocols for C-CDA documents."""

from datetime import date
from typing import Optional, Protocol


class AdvanceDirectiveProtocol(Protocol):
    """Advance Directive data contract."""

    @property
    def directive_type(self) -> str:
        """
        Type of advance directive.

        Should be from the Advance Directive Type Code value set (2.16.840.1.113883.1.11.20.2).
        Examples: "Resuscitate", "Do Not Resuscitate", "Living Will", etc.

        Returns:
            Directive type code or description
        """
        ...

    @property
    def directive_type_code(self) -> Optional[str]:
        """
        Code for the directive type (SNOMED CT or LOINC).

        Returns:
            Directive type code or None
        """
        ...

    @property
    def directive_type_code_system(self) -> Optional[str]:
        """
        Code system for directive type code.

        Returns:
            Code system OID or name, or None
        """
        ...

    @property
    def directive_value(self) -> str:
        """
        The detailed patient directive (coded or text).

        Examples: "Full code", "No intubation", "IV antibiotics only"

        Returns:
            Directive value description
        """
        ...

    @property
    def directive_value_code(self) -> Optional[str]:
        """
        Code for the directive value (typically SNOMED CT).

        Returns:
            Directive value code or None
        """
        ...

    @property
    def directive_value_code_system(self) -> Optional[str]:
        """
        Code system for directive value code.

        Returns:
            Code system OID or name, or None
        """
        ...

    @property
    def start_date(self) -> Optional[date]:
        """
        Date when the advance directive becomes effective.

        Returns:
            Start date or None
        """
        ...

    @property
    def end_date(self) -> Optional[date]:
        """
        Date when the advance directive ends or expires (if applicable).

        Returns:
            End date or None (None if no specified ending time)
        """
        ...

    @property
    def custodian_name(self) -> Optional[str]:
        """
        Name of the healthcare agent/proxy/custodian.

        Returns:
            Custodian name or None
        """
        ...

    @property
    def custodian_relationship(self) -> Optional[str]:
        """
        Relationship of custodian to patient.

        Should be from Personal And Legal Relationship Role Type value set.
        Examples: "Spouse", "Child", "Attorney", etc.

        Returns:
            Relationship or None
        """
        ...

    @property
    def custodian_relationship_code(self) -> Optional[str]:
        """
        Code for custodian relationship.

        Returns:
            Relationship code or None
        """
        ...

    @property
    def custodian_phone(self) -> Optional[str]:
        """
        Contact phone number for custodian.

        Returns:
            Phone number or None
        """
        ...

    @property
    def custodian_address(self) -> Optional[str]:
        """
        Address of custodian.

        Returns:
            Address or None
        """
        ...

    @property
    def verifier_name(self) -> Optional[str]:
        """
        Name of clinician who verified the advance directive.

        Returns:
            Verifier name or None
        """
        ...

    @property
    def verification_date(self) -> Optional[date]:
        """
        Date when the advance directive was verified.

        Returns:
            Verification date or None
        """
        ...

    @property
    def document_id(self) -> Optional[str]:
        """
        Identifier for the advance directive document.

        Returns:
            Document ID or None
        """
        ...

    @property
    def document_url(self) -> Optional[str]:
        """
        URL reference to the advance directive document.

        Returns:
            Document URL or None
        """
        ...

    @property
    def document_description(self) -> Optional[str]:
        """
        Description or text about the advance directive document.

        Returns:
            Document description or None
        """
        ...
