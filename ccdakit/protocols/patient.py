"""Patient-related protocols for C-CDA documents."""

from datetime import date
from typing import Optional, Protocol, Sequence


class AddressProtocol(Protocol):
    """Address data contract."""

    @property
    def street_lines(self) -> Sequence[str]:
        """
        Street address lines (1-4 lines).

        Returns:
            List of street address lines
        """
        ...

    @property
    def city(self) -> str:
        """
        City name.

        Returns:
            City name
        """
        ...

    @property
    def state(self) -> str:
        """
        State/province code (e.g., 'CA', 'NY').

        Returns:
            State or province code
        """
        ...

    @property
    def postal_code(self) -> str:
        """
        ZIP/postal code.

        Returns:
            Postal code
        """
        ...

    @property
    def country(self) -> str:
        """
        Country code (ISO 3166-1 alpha-2, e.g., 'US').

        Returns:
            Country code
        """
        ...


class TelecomProtocol(Protocol):
    """Contact information protocol."""

    @property
    def type(self) -> str:
        """
        Type: 'phone', 'email', 'fax', 'url'.

        Returns:
            Type of contact information
        """
        ...

    @property
    def value(self) -> str:
        """
        The actual phone number, email, etc.

        Returns:
            Contact value (phone number, email address, etc.)
        """
        ...

    @property
    def use(self) -> Optional[str]:
        """
        Use code: 'HP' (home), 'WP' (work), 'MC' (mobile).

        Returns:
            Use code or None
        """
        ...


class PatientProtocol(Protocol):
    """Patient data contract."""

    @property
    def first_name(self) -> str:
        """
        Legal first name.

        Returns:
            First name
        """
        ...

    @property
    def last_name(self) -> str:
        """
        Legal last name.

        Returns:
            Last name
        """
        ...

    @property
    def middle_name(self) -> Optional[str]:
        """
        Middle name or initial.

        Returns:
            Middle name or None
        """
        ...

    @property
    def date_of_birth(self) -> date:
        """
        Date of birth.

        Returns:
            Date of birth
        """
        ...

    @property
    def sex(self) -> str:
        """
        Administrative sex: 'M', 'F', or 'UN'.

        Returns:
            Sex code
        """
        ...

    @property
    def race(self) -> Optional[str]:
        """
        Race code (CDC Race and Ethnicity).

        Returns:
            Race code or None
        """
        ...

    @property
    def ethnicity(self) -> Optional[str]:
        """
        Ethnicity code (CDC Race and Ethnicity).

        Returns:
            Ethnicity code or None
        """
        ...

    @property
    def language(self) -> Optional[str]:
        """
        Preferred language (ISO 639-2).

        Returns:
            Language code or None
        """
        ...

    @property
    def ssn(self) -> Optional[str]:
        """
        Social Security Number (US) or national ID.

        Returns:
            SSN or None
        """
        ...

    @property
    def addresses(self) -> Sequence[AddressProtocol]:
        """
        List of addresses (home, work, etc.).

        Returns:
            List of addresses
        """
        ...

    @property
    def telecoms(self) -> Sequence[TelecomProtocol]:
        """
        List of contact methods (phone, email, etc.).

        Returns:
            List of contact methods
        """
        ...

    @property
    def marital_status(self) -> Optional[str]:
        """
        Marital status code (HL7 MaritalStatus).

        Returns:
            Marital status code or None
        """
        ...
