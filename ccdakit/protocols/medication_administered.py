"""Medication administration protocols for C-CDA documents.

This module defines protocols for medications that have been administered to patients,
typically during procedures or encounters. This differs from prescribed medications
(MedicationProtocol) which represents ongoing medication regimens.

Reference: Medications Administered Section (V2)
Template ID: 2.16.840.1.113883.10.20.22.2.38 (2014-06-09)
Entry Template: Medication Activity (V2) 2.16.840.1.113883.10.20.22.4.16 (2014-06-09)
"""

from datetime import datetime
from typing import Optional, Protocol


class MedicationAdministeredProtocol(Protocol):
    """
    Medication administration data contract.

    Represents a medication or fluid that was administered to a patient during
    a procedure, encounter, or other clinical activity. This protocol captures
    the actual administration event with specific timing, dose, and route
    information.

    Examples:
        Typical use cases include:
        - IV fluids administered during surgery
        - Medications given during emergency department visit
        - Contrast agents used during imaging procedures
        - Medications administered during inpatient stay

    Note:
        Anesthesia medications should be documented in the Anesthesia Section
        (2.16.840.1.113883.10.20.22.2.25) rather than using this protocol.
    """

    @property
    def name(self) -> str:
        """
        Human-readable medication name.

        Returns:
            Medication name (e.g., "Acetaminophen 325mg oral tablet",
            "Normal Saline 0.9% IV Solution")

        Examples:
            - "Acetaminophen 325mg oral tablet"
            - "Ondansetron 4mg/2mL injection"
            - "Normal Saline 0.9% IV Solution"
        """
        ...

    @property
    def code(self) -> str:
        """
        RxNorm code for the medication.

        Returns:
            RxNorm code identifier

        Examples:
            - "197806" for Acetaminophen 325mg oral tablet
            - "312086" for Ondansetron 4mg injection
        """
        ...

    @property
    def administration_time(self) -> datetime:
        """
        Date and time when the medication was administered.

        Returns:
            Administration timestamp

        Note:
            For medications administered over a duration (e.g., IV infusions),
            this represents the start time. Use administration_end_time for
            the completion time.
        """
        ...

    @property
    def administration_end_time(self) -> Optional[datetime]:
        """
        Date and time when medication administration ended (optional).

        Returns:
            End timestamp or None for single-dose administrations

        Note:
            Primarily used for IV infusions or medications administered
            over an extended period.
        """
        ...

    @property
    def dose(self) -> str:
        """
        Dosage amount administered.

        Returns:
            Dose string with units (e.g., "325 mg", "2 tablets", "100 mL")

        Examples:
            - "325 mg" (if consumable is not pre-coordinated)
            - "2" (if consumable is pre-coordinated like "tablet")
            - "500 mL" (for IV fluids)

        Note:
            For pre-coordinated products (e.g., "metoprolol 25mg tablet"),
            dose represents the number of units (e.g., "2" tablets).
            For non-pre-coordinated products (e.g., "metoprolol"), dose
            must include physical quantity with units (e.g., "25 mg").
        """
        ...

    @property
    def route(self) -> str:
        """
        Route of administration.

        Returns:
            Route code or display name from FDA route of administration value set

        Examples:
            - "PO" (oral)
            - "IV" (intravenous)
            - "IM" (intramuscular)
            - "ORAL" (by mouth)
            - "C38276" (intravenous - NCI code)

        Note:
            Should use codes from SPL Drug Route of Administration Terminology
            value set (2.16.840.1.113883.3.88.12.3221.8.7).
        """
        ...

    @property
    def rate(self) -> Optional[str]:
        """
        Rate of administration (optional).

        Returns:
            Rate with units (e.g., "100 mL/hr", "20 mg/min") or None

        Note:
            Primarily used for IV infusions to specify the infusion rate.
        """
        ...

    @property
    def site(self) -> Optional[str]:
        """
        Anatomical site of administration (optional).

        Returns:
            Body site code or description (e.g., "left arm", "right deltoid") or None

        Examples:
            - "368209003" (SNOMED CT code for right arm)
            - "left antecubital fossa"
            - "right deltoid"
        """
        ...

    @property
    def status(self) -> str:
        """
        Administration status.

        Returns:
            Status code: typically 'completed' for administered medications,
            or 'active', 'aborted', 'held'

        Note:
            Should use codes from Medication Status value set
            (2.16.840.1.113762.1.4.1099.11).
        """
        ...

    @property
    def performer(self) -> Optional[str]:
        """
        Name of person who administered the medication (optional).

        Returns:
            Performer name (e.g., "Dr. Jane Smith, RN") or None

        Examples:
            - "Dr. Robert Jones"
            - "Jane Smith, RN"
            - "Pharmacy"
        """
        ...

    @property
    def indication(self) -> Optional[str]:
        """
        Reason for administration (optional).

        Returns:
            Indication or reason text or None

        Examples:
            - "Pain management"
            - "Nausea"
            - "Anxiety"
            - "Pre-operative sedation"
        """
        ...

    @property
    def instructions(self) -> Optional[str]:
        """
        Administration instructions or notes (optional).

        Returns:
            Free text instructions or None

        Examples:
            - "Administer over 15 minutes"
            - "Push slowly over 2 minutes"
            - "Titrate to effect"
        """
        ...
