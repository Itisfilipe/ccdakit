"""Example of creating a Functional Status Section.

This example demonstrates creating a Functional Status Section with multiple
observations organized by functional categories (mobility, self-care, communication).

The Functional Status Section contains observations and assessments of a patient's
physical abilities, including Activities of Daily Living (ADLs) and Instrumental
Activities of Daily Living (IADLs).
"""

from datetime import datetime

from lxml import etree

from ccdakit.builders.sections.functional_status import FunctionalStatusSection
from ccdakit.core.base import CDAVersion


class ExampleFunctionalStatusObservation:
    """Example functional status observation.

    Represents a single functional status assessment (e.g., ability to walk,
    bathe, dress, eat).
    """

    def __init__(
        self,
        obs_type: str,
        code: str,
        code_system: str | None = None,
        value: str = "",
        value_code: str = "",
        value_code_system: str | None = None,
        assessment_date: datetime | None = None,
        interpretation: str | None = None,
    ):
        """Initialize functional status observation.

        Args:
            obs_type: Type of functional status (e.g., "Ambulation", "Bathing")
            code: SNOMED CT code for the functional status type
            code_system: Code system OID (defaults to SNOMED CT)
            value: Description of functional ability
            value_code: SNOMED CT code for the value
            value_code_system: Code system OID for value (defaults to SNOMED CT)
            assessment_date: Date and time of assessment
            interpretation: Optional interpretation of the status
        """
        self._type = obs_type
        self._code = code
        self._code_system = code_system
        self._value = value
        self._value_code = value_code
        self._value_code_system = value_code_system
        self._date = assessment_date or datetime.now()
        self._interpretation = interpretation

    @property
    def type(self) -> str:
        return self._type

    @property
    def code(self) -> str:
        return self._code

    @property
    def code_system(self) -> str | None:
        return self._code_system

    @property
    def value(self) -> str:
        return self._value

    @property
    def value_code(self) -> str:
        return self._value_code

    @property
    def value_code_system(self) -> str | None:
        return self._value_code_system

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def interpretation(self) -> str | None:
        return self._interpretation


class ExampleFunctionalStatusOrganizer:
    """Example functional status organizer.

    Groups related functional status observations by category (e.g., Mobility,
    Self-Care, Communication). Uses ICF (International Classification of Functioning,
    Disability and Health) codes by default.
    """

    def __init__(
        self,
        category: str,
        category_code: str,
        category_code_system: str | None = None,
        observations: list | None = None,
    ):
        """Initialize functional status organizer.

        Args:
            category: Category name (e.g., "Mobility", "Self-Care")
            category_code: ICF or LOINC code for the category
            category_code_system: Code system OID (defaults to ICF)
            observations: List of functional status observations in this category
        """
        self._category = category
        self._category_code = category_code
        self._category_code_system = category_code_system
        self._observations = observations or []

    @property
    def category(self) -> str:
        return self._category

    @property
    def category_code(self) -> str:
        return self._category_code

    @property
    def category_code_system(self) -> str | None:
        return self._category_code_system

    @property
    def observations(self) -> list:
        return self._observations


def main():
    """Create and display a Functional Status Section example."""

    # Mobility observations
    mobility_observations = [
        ExampleFunctionalStatusObservation(
            obs_type="Ambulation",
            code="129006008",
            value="Walks independently",
            value_code="165245003",
            assessment_date=datetime(2024, 1, 15, 10, 30),
        ),
        ExampleFunctionalStatusObservation(
            obs_type="Transfer",
            code="285652008",
            value="Requires minimal assistance",
            value_code="371152001",
            assessment_date=datetime(2024, 1, 15, 10, 35),
        ),
        ExampleFunctionalStatusObservation(
            obs_type="Stair climbing",
            code="301587001",
            value="Unable to climb stairs",
            value_code="282039006",
            assessment_date=datetime(2024, 1, 15, 10, 40),
        ),
    ]

    # Self-care observations
    self_care_observations = [
        ExampleFunctionalStatusObservation(
            obs_type="Bathing",
            code="284785009",
            value="Independent",
            value_code="371153006",
            assessment_date=datetime(2024, 1, 15, 11, 0),
        ),
        ExampleFunctionalStatusObservation(
            obs_type="Dressing",
            code="165235000",
            value="Requires assistance with buttons",
            value_code="371152001",
            assessment_date=datetime(2024, 1, 15, 11, 5),
        ),
        ExampleFunctionalStatusObservation(
            obs_type="Feeding",
            code="289167008",
            value="Independent",
            value_code="371153006",
            assessment_date=datetime(2024, 1, 15, 11, 10),
        ),
    ]

    # Communication observations
    communication_observations = [
        ExampleFunctionalStatusObservation(
            obs_type="Expressive language",
            code="61909002",
            value="Moderate difficulty expressing thoughts",
            value_code="371152001",
            assessment_date=datetime(2024, 1, 15, 11, 15),
        ),
        ExampleFunctionalStatusObservation(
            obs_type="Receptive language",
            code="106136008",
            value="Understands simple instructions",
            value_code="165245003",
            assessment_date=datetime(2024, 1, 15, 11, 20),
        ),
    ]

    # Cognitive function observations
    cognitive_observations = [
        ExampleFunctionalStatusObservation(
            obs_type="Memory",
            code="106167005",
            value="Short-term memory impairment",
            value_code="386806002",
            assessment_date=datetime(2024, 1, 15, 11, 25),
        ),
    ]

    # Create organizers (using ICF codes for categories)
    mobility_organizer = ExampleFunctionalStatusOrganizer(
        category="Mobility",
        category_code="d4",  # ICF: Mobility
        observations=mobility_observations,
    )

    self_care_organizer = ExampleFunctionalStatusOrganizer(
        category="Self-Care",
        category_code="d5",  # ICF: Self-care
        observations=self_care_observations,
    )

    communication_organizer = ExampleFunctionalStatusOrganizer(
        category="Communication",
        category_code="d3",  # ICF: Communication
        observations=communication_observations,
    )

    cognitive_organizer = ExampleFunctionalStatusOrganizer(
        category="Mental Functions",
        category_code="b1",  # ICF: Mental functions
        observations=cognitive_observations,
    )

    # Create the Functional Status Section
    section = FunctionalStatusSection(
        organizers=[
            mobility_organizer,
            self_care_organizer,
            communication_organizer,
            cognitive_organizer,
        ],
        title="Functional Status Assessment",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Functional Status Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show summary information
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.14")
    print("  - Extension: 2014-06-09")
    print("  - Section Code: 47420-5 (Functional Status)")
    print(
        f"  - Number of organizers: {len([mobility_organizer, self_care_organizer, communication_organizer, cognitive_organizer])}"
    )
    print(
        f"  - Total observations: {len(mobility_observations) + len(self_care_observations) + len(communication_observations) + len(cognitive_observations)}"
    )
    print("\nFunctional Categories:")
    print("  - Mobility: 3 assessments (ambulation, transfer, stair climbing)")
    print("  - Self-Care: 3 assessments (bathing, dressing, feeding)")
    print("  - Communication: 2 assessments (expressive and receptive language)")
    print("  - Mental Functions: 1 assessment (memory)")
    print("\nConformance:")
    print("  - CONF:1098-7920: Template ID present")
    print("  - CONF:1098-14578: Code 47420-5 (Functional Status)")
    print("  - CONF:1098-7922: Title element present")
    print("  - CONF:1098-7923: Narrative text with HTML table")
    print("  - CONF:1098-14414: Entry elements with organizers")
    print("  - CONF:1098-14361: Functional Status Organizer template")
    print("  - CONF:1098-13889: Functional Status Observation template")
    print("\nCode Systems Used:")
    print("  - ICF (2.16.840.1.113883.6.254): Category codes")
    print("  - SNOMED CT (2.16.840.1.113883.6.96): Observation codes and values")
    print("  - LOINC (2.16.840.1.113883.6.1): Section and observation codes")


if __name__ == "__main__":
    main()
