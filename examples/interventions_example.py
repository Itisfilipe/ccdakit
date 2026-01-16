"""Example of creating an Interventions Section."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.interventions import InterventionsSection
from ccdakit.core.base import CDAVersion


# Define intervention data classes
class ExampleIntervention:
    """Example intervention for demonstrating completed interventions."""

    def __init__(
        self,
        id,
        description,
        status="completed",
        effective_time=None,
        intervention_type=None,
        goal_reference_id=None,
        author=None,
    ):
        self._id = id
        self._description = description
        self._status = status
        self._effective_time = effective_time
        self._intervention_type = intervention_type
        self._goal_reference_id = goal_reference_id
        self._author = author

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        return self._description

    @property
    def status(self):
        return self._status

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def intervention_type(self):
        return self._intervention_type

    @property
    def goal_reference_id(self):
        return self._goal_reference_id

    @property
    def author(self):
        return self._author


class ExamplePlannedIntervention:
    """Example planned intervention for demonstrating future interventions."""

    def __init__(
        self,
        id,
        description,
        mood_code="INT",
        status="active",
        effective_time=None,
        intervention_type=None,
        goal_reference_id=None,
        author=None,
    ):
        self._id = id
        self._description = description
        self._mood_code = mood_code
        self._status = status
        self._effective_time = effective_time
        self._intervention_type = intervention_type
        self._goal_reference_id = goal_reference_id
        self._author = author

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        return self._description

    @property
    def mood_code(self):
        return self._mood_code

    @property
    def status(self):
        return self._status

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def intervention_type(self):
        return self._intervention_type

    @property
    def goal_reference_id(self):
        return self._goal_reference_id

    @property
    def author(self):
        return self._author


def main():
    """Create and display an Interventions Section example."""

    # Create completed interventions
    intervention1 = ExampleIntervention(
        id="INT-001",
        description="Patient education: proper use of inhaler and spacer device",
        status="completed",
        effective_time=date(2023, 6, 15),
        intervention_type="instruction",
        goal_reference_id="GOAL-001",
    )

    intervention2 = ExampleIntervention(
        id="INT-002",
        description="Care coordination: scheduled follow-up with pulmonologist",
        status="completed",
        effective_time=date(2023, 6, 15),
        intervention_type="encounter",
        goal_reference_id="GOAL-001",
    )

    intervention3 = ExampleIntervention(
        id="INT-003",
        description="Environmental modification: removal of household allergens and triggers",
        status="completed",
        effective_time=date(2023, 6, 20),
        intervention_type="procedure",
        goal_reference_id="GOAL-002",
    )

    # Create planned interventions
    planned1 = ExamplePlannedIntervention(
        id="PLANNED-INT-001",
        description="Physical therapy: strength training and mobility exercises 3x weekly",
        mood_code="INT",
        status="active",
        effective_time=date(2023, 7, 1),
        intervention_type="procedure",
        goal_reference_id="GOAL-003",
    )

    planned2 = ExamplePlannedIntervention(
        id="PLANNED-INT-002",
        description="Nutritional counseling: diabetes-appropriate meal planning",
        mood_code="ARQ",
        status="active",
        effective_time=date(2023, 7, 10),
        intervention_type="instruction",
        goal_reference_id="GOAL-004",
    )

    # Create the Interventions Section
    section = InterventionsSection(
        interventions=[intervention1, intervention2, intervention3],
        planned_interventions=[planned1, planned2],
        title="Patient Care Interventions",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Interventions Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.21.2.3")
    print("  - Extension: 2015-08-01")
    print("  - Number of completed interventions: 3")
    print("  - Number of planned interventions: 2")
    print("  - Total intervention entries: 5")
    print("\nIntervention Types Demonstrated:")
    print("  - Patient education (instruction)")
    print("  - Care coordination (encounter)")
    print("  - Environmental modification (procedure)")
    print("  - Physical therapy (planned procedure)")
    print("  - Nutritional counseling (planned instruction)")
    print("\nConformance:")
    print("  - CONF:1198-8680: Template ID present")
    print("  - CONF:1198-32559: Extension 2015-08-01")
    print("  - CONF:1198-15377: Code 62387-6 (Interventions Provided)")
    print("  - CONF:1198-8682: Title present")
    print("  - CONF:1198-8683: Narrative text present")
    print("  - CONF:1198-30996: Intervention Act entries present")
    print("  - CONF:1198-32730: Planned Intervention Act entries present")


if __name__ == "__main__":
    main()
