"""Payer-related protocols for C-CDA documents."""

from datetime import date
from typing import Optional, Protocol


class PayerProtocol(Protocol):
    """Payer/Insurance data contract for Coverage Activity."""

    @property
    def payer_name(self) -> str:
        """
        Name of the insurance payer/company.

        Returns:
            Payer name (e.g., "Aetna", "Blue Cross Blue Shield")
        """
        ...

    @property
    def payer_id(self) -> str:
        """
        Unique identifier for the payer.

        Returns:
            Payer ID (e.g., NAIC number)
        """
        ...

    @property
    def member_id(self) -> str:
        """
        Member/subscriber ID from insurance card.

        Returns:
            Member ID
        """
        ...

    @property
    def group_number(self) -> Optional[str]:
        """
        Group/policy number (optional).

        Returns:
            Group number or None
        """
        ...

    @property
    def insurance_type(self) -> str:
        """
        Type of insurance (e.g., "HMO", "PPO", "Medicare", "Medicaid").

        Returns:
            Insurance type code or name
        """
        ...

    @property
    def insurance_type_code(self) -> Optional[str]:
        """
        Code for insurance type from value set (optional).

        Returns:
            Insurance type code or None
        """
        ...

    @property
    def start_date(self) -> Optional[date]:
        """
        Coverage start date (optional).

        Returns:
            Start date or None
        """
        ...

    @property
    def end_date(self) -> Optional[date]:
        """
        Coverage end date (optional, None if ongoing).

        Returns:
            End date or None
        """
        ...

    @property
    def sequence_number(self) -> Optional[int]:
        """
        Priority/sequence number for this coverage (1=primary, 2=secondary, etc.).

        Returns:
            Sequence number or None
        """
        ...

    @property
    def subscriber_name(self) -> Optional[str]:
        """
        Name of policy subscriber if different from patient (optional).

        Returns:
            Subscriber name or None if patient is subscriber
        """
        ...

    @property
    def subscriber_id(self) -> Optional[str]:
        """
        Subscriber identifier if different from member (optional).

        Returns:
            Subscriber ID or None
        """
        ...

    @property
    def relationship_to_subscriber(self) -> Optional[str]:
        """
        Patient's relationship to subscriber (e.g., "self", "spouse", "child").

        Returns:
            Relationship code or None if patient is subscriber
        """
        ...

    @property
    def payer_phone(self) -> Optional[str]:
        """
        Payer contact phone number (optional).

        Returns:
            Phone number or None
        """
        ...

    @property
    def coverage_type_code(self) -> Optional[str]:
        """
        Code for coverage role type (optional).

        Returns:
            Coverage type code or None
        """
        ...

    @property
    def authorization_ids(self) -> Optional[list]:
        """
        List of authorization IDs related to this coverage (optional).

        Returns:
            List of authorization ID strings or None
        """
        ...
