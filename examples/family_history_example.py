"""Example of creating a Family History Section."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.family_history import FamilyHistorySection
from ccdakit.core.base import CDAVersion


# Define persistent ID class
class ExamplePersistentID:
    """Example persistent ID for tracking across document versions."""

    def __init__(self, root, extension):
        self._root = root
        self._extension = extension

    @property
    def root(self):
        return self._root

    @property
    def extension(self):
        return self._extension


# Define family member subject details
class ExampleFamilyMemberSubject:
    """Example family member subject with demographic details."""

    def __init__(
        self,
        administrative_gender_code=None,
        birth_time=None,
        deceased_ind=None,
        deceased_time=None,
    ):
        self._administrative_gender_code = administrative_gender_code
        self._birth_time = birth_time
        self._deceased_ind = deceased_ind
        self._deceased_time = deceased_time

    @property
    def administrative_gender_code(self):
        return self._administrative_gender_code

    @property
    def birth_time(self):
        return self._birth_time

    @property
    def deceased_ind(self):
        return self._deceased_ind

    @property
    def deceased_time(self):
        return self._deceased_time


# Define family history observation
class ExampleFamilyHistoryObservation:
    """Example family history observation for a specific condition."""

    def __init__(
        self,
        condition_name,
        condition_code,
        condition_code_system="SNOMED",
        observation_type_code=None,
        observation_type_display_name=None,
        effective_time=None,
        age_at_onset=None,
        deceased_age=None,
        deceased_cause_code=None,
        deceased_cause_display_name=None,
        persistent_id=None,
    ):
        self._condition_name = condition_name
        self._condition_code = condition_code
        self._condition_code_system = condition_code_system
        self._observation_type_code = observation_type_code
        self._observation_type_display_name = observation_type_display_name
        self._effective_time = effective_time
        self._age_at_onset = age_at_onset
        self._deceased_age = deceased_age
        self._deceased_cause_code = deceased_cause_code
        self._deceased_cause_display_name = deceased_cause_display_name
        self._persistent_id = persistent_id

    @property
    def condition_name(self):
        return self._condition_name

    @property
    def condition_code(self):
        return self._condition_code

    @property
    def condition_code_system(self):
        return self._condition_code_system

    @property
    def observation_type_code(self):
        return self._observation_type_code

    @property
    def observation_type_display_name(self):
        return self._observation_type_display_name

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def age_at_onset(self):
        return self._age_at_onset

    @property
    def deceased_age(self):
        return self._deceased_age

    @property
    def deceased_cause_code(self):
        return self._deceased_cause_code

    @property
    def deceased_cause_display_name(self):
        return self._deceased_cause_display_name

    @property
    def persistent_id(self):
        return self._persistent_id


# Define family member history
class ExampleFamilyMemberHistory:
    """Example family member history organizer."""

    def __init__(
        self,
        relationship_code,
        relationship_display_name,
        subject=None,
        observations=None,
        persistent_id=None,
    ):
        self._relationship_code = relationship_code
        self._relationship_display_name = relationship_display_name
        self._subject = subject
        self._observations = observations or []
        self._persistent_id = persistent_id

    @property
    def relationship_code(self):
        return self._relationship_code

    @property
    def relationship_display_name(self):
        return self._relationship_display_name

    @property
    def subject(self):
        return self._subject

    @property
    def observations(self):
        return self._observations

    @property
    def persistent_id(self):
        return self._persistent_id


def main():
    """Create and display a Family History Section example."""

    # Create father's data (deceased from heart attack)
    father_subject = ExampleFamilyMemberSubject(
        administrative_gender_code="M",
        birth_time=date(1950, 3, 15),
        deceased_ind=True,
        deceased_time=date(2015, 7, 22),
    )

    father_diabetes = ExampleFamilyHistoryObservation(
        condition_name="Type 2 Diabetes Mellitus",
        condition_code="44054006",
        condition_code_system="SNOMED",
        observation_type_code="64572001",
        observation_type_display_name="Disease",
        age_at_onset=52,
    )

    father_heart_disease = ExampleFamilyHistoryObservation(
        condition_name="Coronary Artery Disease",
        condition_code="53741008",
        condition_code_system="SNOMED",
        observation_type_code="64572001",
        observation_type_display_name="Disease",
        age_at_onset=60,
    )

    father_mi = ExampleFamilyHistoryObservation(
        condition_name="Myocardial Infarction",
        condition_code="22298006",
        condition_code_system="SNOMED",
        observation_type_code="64572001",
        observation_type_display_name="Disease",
        age_at_onset=64,
        deceased_age=65,
        deceased_cause_code="22298006",
        deceased_cause_display_name="Myocardial infarction",
    )

    # Create mother's data (living with breast cancer history)
    mother_subject = ExampleFamilyMemberSubject(
        administrative_gender_code="F",
        birth_time=date(1952, 11, 8),
        deceased_ind=False,
    )

    mother_breast_cancer = ExampleFamilyHistoryObservation(
        condition_name="Breast Cancer",
        condition_code="254837009",
        condition_code_system="SNOMED",
        observation_type_code="64572001",
        observation_type_display_name="Disease",
        age_at_onset=58,
        effective_time=date(2010, 5, 12),
    )

    mother_hypertension = ExampleFamilyHistoryObservation(
        condition_name="Essential Hypertension",
        condition_code="59621000",
        condition_code_system="SNOMED",
        observation_type_code="64572001",
        observation_type_display_name="Disease",
        age_at_onset=55,
    )

    # Create sibling's data (brother with asthma)
    brother_subject = ExampleFamilyMemberSubject(
        administrative_gender_code="M",
        birth_time=date(1978, 6, 22),
        deceased_ind=False,
    )

    brother_asthma = ExampleFamilyHistoryObservation(
        condition_name="Asthma",
        condition_code="195967001",
        condition_code_system="SNOMED",
        observation_type_code="64572001",
        observation_type_display_name="Disease",
        age_at_onset=12,
    )

    # Create family member history organizers
    father = ExampleFamilyMemberHistory(
        relationship_code="FTH",
        relationship_display_name="Father",
        subject=father_subject,
        observations=[father_diabetes, father_heart_disease, father_mi],
        persistent_id=ExamplePersistentID("2.16.840.1.113883.3.1234", "fam-member-001"),
    )

    mother = ExampleFamilyMemberHistory(
        relationship_code="MTH",
        relationship_display_name="Mother",
        subject=mother_subject,
        observations=[mother_breast_cancer, mother_hypertension],
        persistent_id=ExamplePersistentID("2.16.840.1.113883.3.1234", "fam-member-002"),
    )

    brother = ExampleFamilyMemberHistory(
        relationship_code="BRO",
        relationship_display_name="Brother",
        subject=brother_subject,
        observations=[brother_asthma],
        persistent_id=ExamplePersistentID("2.16.840.1.113883.3.1234", "fam-member-003"),
    )

    # Create the Family History Section
    section = FamilyHistorySection(
        family_members=[father, mother, brother],
        title="Family Medical History",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Family History Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.15")
    print("  - Extension: 2015-08-01")
    print("  - Number of family members: 3")
    print("  - Total conditions documented: 6")
    print("\nFamily Members:")
    print("  1. Father (Deceased 2015-07-22)")
    print("     - Type 2 Diabetes (onset age 52)")
    print("     - Coronary Artery Disease (onset age 60)")
    print("     - Myocardial Infarction (onset age 64, cause of death)")
    print("  2. Mother (Living)")
    print("     - Breast Cancer (onset age 58)")
    print("     - Essential Hypertension (onset age 55)")
    print("  3. Brother (Living)")
    print("     - Asthma (onset age 12)")
    print("\nConformance:")
    print("  - CONF:1198-7932: Template ID present")
    print("  - CONF:1198-15470: Code 10157-6 (Family History)")
    print("  - CONF:1198-7934: Title present")
    print("  - CONF:1198-7935: Narrative text present")
    print("  - CONF:1198-32431: Family History Organizer entries present")
    print("\nFeatures Demonstrated:")
    print("  - Multiple family members with different relationships")
    print("  - Deceased indicator and date (father)")
    print("  - Living status (mother, brother)")
    print("  - Gender codes (M/F)")
    print("  - Birth dates for all members")
    print("  - Age at onset for conditions")
    print("  - Cause of death information")
    print("  - SNOMED CT codes for conditions")
    print("  - Persistent IDs for tracking across document versions")
    print("  - SDTC extensions for enhanced demographics")


if __name__ == "__main__":
    main()
