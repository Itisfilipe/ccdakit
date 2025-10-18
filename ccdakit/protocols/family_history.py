"""Family History-related protocols for C-CDA documents."""

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


class FamilyMemberSubjectProtocol(Protocol):
    """Family member subject details protocol (SDC extension fields)."""

    @property
    def administrative_gender_code(self) -> Optional[str]:
        """
        Administrative gender code from HL7 AdministrativeGender value set.

        Valid codes: M (Male), F (Female), UN (Undifferentiated)

        Returns:
            Gender code or None
        """
        ...

    @property
    def birth_time(self) -> Optional[date]:
        """
        Birth date of the family member.

        Returns:
            Birth date or None
        """
        ...

    @property
    def deceased_ind(self) -> Optional[bool]:
        """
        Indicator of whether family member is deceased.

        Returns:
            True if deceased, False if living, None if unknown
        """
        ...

    @property
    def deceased_time(self) -> Optional[date]:
        """
        Date when family member died.

        Returns:
            Deceased date or None
        """
        ...


class FamilyHistoryObservationProtocol(Protocol):
    """Family history observation data contract."""

    @property
    def condition_name(self) -> str:
        """
        Human-readable condition/problem name.

        Returns:
            Condition name
        """
        ...

    @property
    def condition_code(self) -> str:
        """
        SNOMED CT or ICD-10 code for the condition.

        Returns:
            Condition code
        """
        ...

    @property
    def condition_code_system(self) -> str:
        """
        Code system: 'SNOMED' or 'ICD-10'.

        Returns:
            Code system name
        """
        ...

    @property
    def observation_type_code(self) -> Optional[str]:
        """
        SNOMED CT code for observation type (e.g., 64572001 = Disease).
        Should be from Problem Type (SNOMEDCT) value set.

        Returns:
            Observation type code or None (defaults to 64572001)
        """
        ...

    @property
    def observation_type_display_name(self) -> Optional[str]:
        """
        Display name for observation type.

        Returns:
            Display name or None
        """
        ...

    @property
    def effective_time(self) -> Optional[date]:
        """
        Biologically/clinically relevant time for the observation.
        This is when the observation holds for the family member.

        Returns:
            Effective time or None
        """
        ...

    @property
    def age_at_onset(self) -> Optional[int]:
        """
        Age at which condition began (in years).

        Returns:
            Age in years or None
        """
        ...

    @property
    def deceased_age(self) -> Optional[int]:
        """
        Age at death if deceased (in years).

        Returns:
            Age at death in years or None
        """
        ...

    @property
    def deceased_cause_code(self) -> Optional[str]:
        """
        Code for cause of death.

        Returns:
            Cause of death code or None
        """
        ...

    @property
    def deceased_cause_display_name(self) -> Optional[str]:
        """
        Display name for cause of death.

        Returns:
            Cause of death display name or None
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


class FamilyMemberHistoryProtocol(Protocol):
    """Family member history organizer data contract."""

    @property
    def relationship_code(self) -> str:
        """
        Relationship code from Family Member Value Set (e.g., FTH=father, MTH=mother).
        Should be from value set 2.16.840.1.113883.1.11.19579.

        Returns:
            Relationship code
        """
        ...

    @property
    def relationship_display_name(self) -> str:
        """
        Human-readable relationship name (e.g., "Father", "Mother").

        Returns:
            Relationship display name
        """
        ...

    @property
    def subject(self) -> Optional[FamilyMemberSubjectProtocol]:
        """
        Additional subject details (gender, birth, deceased info).
        Uses SDTC extensions.

        Returns:
            Subject details or None
        """
        ...

    @property
    def observations(self) -> list:
        """
        List of family history observations for this family member.
        Each observation should satisfy FamilyHistoryObservationProtocol.

        Returns:
            List of observations
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
