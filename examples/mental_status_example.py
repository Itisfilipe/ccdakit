"""Example of creating a Mental Status Section."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.sections.mental_status import MentalStatusSection
from ccdakit.core.base import CDAVersion


# Define persistent ID data
class ExamplePersistentID:
    """Example persistent identifier."""

    def __init__(self, root, extension):
        self._root = root
        self._extension = extension

    @property
    def root(self):
        return self._root

    @property
    def extension(self):
        return self._extension


# Define observation data
class ExampleMentalStatusObservation:
    """Example mental status observation."""

    def __init__(
        self,
        category,
        category_code,
        category_code_system,
        value,
        value_code,
        observation_date,
        status="completed",
        persistent_id=None,
    ):
        self._category = category
        self._category_code = category_code
        self._category_code_system = category_code_system
        self._value = value
        self._value_code = value_code
        self._observation_date = observation_date
        self._status = status
        self._persistent_id = persistent_id

    @property
    def category(self):
        return self._category

    @property
    def category_code(self):
        return self._category_code

    @property
    def category_code_system(self):
        return self._category_code_system

    @property
    def value(self):
        return self._value

    @property
    def value_code(self):
        return self._value_code

    @property
    def observation_date(self):
        return self._observation_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


# Define organizer data
class ExampleMentalStatusOrganizer:
    """Example mental status organizer that groups related observations."""

    def __init__(
        self,
        category,
        category_code,
        category_code_system,
        observations,
        effective_time_low=None,
        effective_time_high=None,
        persistent_id=None,
    ):
        self._category = category
        self._category_code = category_code
        self._category_code_system = category_code_system
        self._observations = observations
        self._effective_time_low = effective_time_low
        self._effective_time_high = effective_time_high
        self._persistent_id = persistent_id

    @property
    def category(self):
        return self._category

    @property
    def category_code(self):
        return self._category_code

    @property
    def category_code_system(self):
        return self._category_code_system

    @property
    def observations(self):
        return self._observations

    @property
    def effective_time_low(self):
        return self._effective_time_low

    @property
    def effective_time_high(self):
        return self._effective_time_high

    @property
    def persistent_id(self):
        return self._persistent_id


def main():
    """Create and display a Mental Status Section example."""

    # Create cognition observations
    cog_obs1 = ExampleMentalStatusObservation(
        category="Cognition",
        category_code="d110",
        category_code_system="ICF",
        value="Alert and oriented x3",
        value_code="248234008",
        observation_date=date(2023, 6, 15),
        status="completed",
    )

    cog_obs2 = ExampleMentalStatusObservation(
        category="Cognition",
        category_code="d110",
        category_code_system="ICF",
        value="Good short-term memory",
        value_code="301284009",
        observation_date=date(2023, 6, 15),
        status="completed",
    )

    # Create cognition organizer grouping related observations
    cognition_organizer = ExampleMentalStatusOrganizer(
        category="Cognitive Function",
        category_code="d110",
        category_code_system="ICF",
        observations=[cog_obs1, cog_obs2],
        effective_time_low=datetime(2023, 6, 15, 10, 0, 0),
        effective_time_high=datetime(2023, 6, 15, 10, 30, 0),
    )

    # Create mood and affect observation
    mood_obs = ExampleMentalStatusObservation(
        category="Mood and Affect",
        category_code="b152",
        category_code_system="ICF",
        value="Depressed mood",
        value_code="366979004",
        observation_date=date(2023, 6, 15),
        status="completed",
    )

    # Create mood organizer
    mood_organizer = ExampleMentalStatusOrganizer(
        category="Mood and Affect",
        category_code="b152",
        category_code_system="ICF",
        observations=[mood_obs],
        effective_time_low=datetime(2023, 6, 15, 10, 0, 0),
    )

    # Create standalone observations (not grouped in organizer)
    appearance_obs = ExampleMentalStatusObservation(
        category="Appearance",
        category_code="d110",  # ICF code for general appearance
        category_code_system="ICF",
        value="Well-groomed",
        value_code="248157009",
        observation_date=date(2023, 6, 15),
        status="completed",
    )

    behavior_obs = ExampleMentalStatusObservation(
        category="Behavior",
        category_code="d110",
        category_code_system="ICF",
        value="Cooperative and engaged",
        value_code="225313000",
        observation_date=date(2023, 6, 15),
        status="completed",
    )

    # Create observation with no SNOMED code (demonstrates null flavor handling)
    thought_obs = ExampleMentalStatusObservation(
        category="Thought Content",
        category_code=None,
        category_code_system=None,
        value="Patient reports racing thoughts and difficulty concentrating",
        value_code=None,  # No standard code available
        observation_date=date(2023, 6, 15),
        status="completed",
    )

    # Create the Mental Status Section with both organizers and standalone observations
    section = MentalStatusSection(
        organizers=[cognition_organizer, mood_organizer],
        observations=[appearance_obs, behavior_obs, thought_obs],
        title="Mental Status Examination",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Mental Status Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.56")
    print("  - Extension: 2015-08-01")
    print("  - Number of organizers: 2")
    print("  - Number of standalone observations: 3")
    print("  - Total observations: 6 (3 in organizers + 3 standalone)")
    print("\nCategories Documented:")
    print("  - Cognitive Function (2 observations)")
    print("  - Mood and Affect (1 observation)")
    print("  - Appearance (1 observation)")
    print("  - Behavior (1 observation)")
    print("  - Thought Content (1 observation)")
    print("\nConformance:")
    print("  - CONF:1198-28293: Template ID present")
    print("  - CONF:1198-28295: Code 10190-7 (Mental Status)")
    print("  - CONF:1198-28297: Title present")
    print("  - CONF:1198-28298: Narrative text present")
    print("  - CONF:1198-28301: Mental Status Organizer entries present")
    print("  - CONF:1198-28305: Mental Status Observation entries present")
    print("\nCode Systems Used:")
    print("  - ICF (International Classification of Functioning): Category codes")
    print("  - SNOMED CT: Value codes for findings")
    print("  - LOINC: Section code")
    print("\nNotes:")
    print("  - Organizers group related observations (e.g., multiple cognition tests)")
    print("  - Standalone observations can be used for single assessments")
    print("  - Null flavor (OTH) used for 'Thought Content' observation without SNOMED code")
    print("  - Effective time range can be specified for organizers")


if __name__ == "__main__":
    main()
