"""Example of creating a Health Status Evaluations and Outcomes Section."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.sections.health_status_evaluations import (
    HealthStatusEvaluationsAndOutcomesSection,
)
from ccdakit.core.base import CDAVersion


# Define Progress Toward Goal data
class ExampleProgressTowardGoal:
    """Example progress toward goal observation."""

    def __init__(
        self,
        id="progress-1",
        achievement_code="385641008",
        achievement_code_system="2.16.840.1.113883.6.96",
        achievement_display_name="Improving",
    ):
        self._id = id
        self._achievement_code = achievement_code
        self._achievement_code_system = achievement_code_system
        self._achievement_display_name = achievement_display_name

    @property
    def id(self):
        return self._id

    @property
    def achievement_code(self):
        return self._achievement_code

    @property
    def achievement_code_system(self):
        return self._achievement_code_system

    @property
    def achievement_display_name(self):
        return self._achievement_display_name


# Define Outcome Observation data
class ExampleOutcomeObservation:
    """Example outcome observation."""

    def __init__(
        self,
        id,
        code,
        code_system,
        display_name,
        value,
        value_unit,
        effective_time,
        progress_toward_goal=None,
        goal_reference_id=None,
        intervention_reference_ids=None,
        author_name=None,
        author_time=None,
    ):
        self._id = id
        self._code = code
        self._code_system = code_system
        self._display_name = display_name
        self._value = value
        self._value_unit = value_unit
        self._effective_time = effective_time
        self._progress_toward_goal = progress_toward_goal
        self._goal_reference_id = goal_reference_id
        self._intervention_reference_ids = intervention_reference_ids
        self._author_name = author_name
        self._author_time = author_time

    @property
    def id(self):
        return self._id

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def display_name(self):
        return self._display_name

    @property
    def value(self):
        return self._value

    @property
    def value_unit(self):
        return self._value_unit

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def progress_toward_goal(self):
        return self._progress_toward_goal

    @property
    def goal_reference_id(self):
        return self._goal_reference_id

    @property
    def intervention_reference_ids(self):
        return self._intervention_reference_ids

    @property
    def author_name(self):
        return self._author_name

    @property
    def author_time(self):
        return self._author_time


def main():
    """Create and display a Health Status Evaluations and Outcomes Section example."""

    # Create progress observations
    weight_progress = ExampleProgressTowardGoal(
        id="progress-weight",
        achievement_code="385641008",
        achievement_code_system="2.16.840.1.113883.6.96",
        achievement_display_name="Improving",
    )

    glucose_progress = ExampleProgressTowardGoal(
        id="progress-glucose",
        achievement_code="385651009",
        achievement_code_system="2.16.840.1.113883.6.96",
        achievement_display_name="Stabilized",
    )

    # Create outcome observations
    outcome1 = ExampleOutcomeObservation(
        id="outcome-weight",
        code="29463-7",
        code_system="LOINC",
        display_name="Body weight",
        value="180",
        value_unit="lbs",
        effective_time=date(2023, 6, 15),
        progress_toward_goal=weight_progress,
        goal_reference_id="goal-weight-loss",
        intervention_reference_ids=["intervention-diet", "intervention-exercise"],
        author_name="Dr. Jane Smith",
        author_time=datetime(2023, 6, 15, 14, 30, 0),
    )

    outcome2 = ExampleOutcomeObservation(
        id="outcome-glucose",
        code="2339-0",
        code_system="LOINC",
        display_name="Glucose [Mass/volume] in Blood",
        value="95",
        value_unit="mg/dL",
        effective_time=date(2023, 6, 15),
        progress_toward_goal=glucose_progress,
        goal_reference_id="goal-glucose-control",
        intervention_reference_ids=["intervention-medication"],
        author_name="Dr. Jane Smith",
        author_time=datetime(2023, 6, 15, 14, 30, 0),
    )

    outcome3 = ExampleOutcomeObservation(
        id="outcome-blood-pressure",
        code="85354-9",
        code_system="LOINC",
        display_name="Blood pressure panel with all children optional",
        value="120/80",
        value_unit="mmHg",
        effective_time=date(2023, 6, 15),
        progress_toward_goal=None,
        goal_reference_id="goal-bp-control",
        intervention_reference_ids=None,
        author_name="Nurse Johnson",
        author_time=datetime(2023, 6, 15, 10, 0, 0),
    )

    outcome4 = ExampleOutcomeObservation(
        id="outcome-hba1c",
        code="4548-4",
        code_system="LOINC",
        display_name="Hemoglobin A1c/Hemoglobin.total in Blood",
        value="6.8",
        value_unit="%",
        effective_time=date(2023, 5, 20),
        progress_toward_goal=None,
        goal_reference_id="goal-diabetes-control",
        intervention_reference_ids=["intervention-medication", "intervention-diet"],
        author_name="Dr. Jane Smith",
        author_time=datetime(2023, 5, 20, 16, 15, 0),
    )

    # Create the Health Status Evaluations and Outcomes Section
    section = HealthStatusEvaluationsAndOutcomesSection(
        outcomes=[outcome1, outcome2, outcome3, outcome4],
        title="Health Status Evaluations and Outcomes",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Health Status Evaluations and Outcomes Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.61")
    print("  - Code: 11383-7 (Patient Problem Outcome)")
    print("  - Number of outcomes: 4")
    print("  - Outcomes with progress observations: 2")
    print("  - Outcomes with goal references: 4")
    print("  - Outcomes with intervention references: 3")
    print("\nConformance:")
    print("  - CONF:1098-29578: Template ID present")
    print("  - CONF:1098-29580: Code 11383-7 (Patient Problem Outcome)")
    print("  - CONF:1098-29589: Title present")
    print("  - CONF:1098-29590: Narrative text present")
    print("  - CONF:1098-31227: Outcome Observation entries present")
    print("\nOutcome Details:")
    print(f"  1. {outcome1.display_name}: {outcome1.value} {outcome1.value_unit}")
    print(f"     Progress: {weight_progress.achievement_display_name}")
    print(f"     Goal: {outcome1.goal_reference_id}")
    print(
        f"     Interventions: {', '.join(outcome1.intervention_reference_ids) if outcome1.intervention_reference_ids else 'None'}"
    )
    print(f"  2. {outcome2.display_name}: {outcome2.value} {outcome2.value_unit}")
    print(f"     Progress: {glucose_progress.achievement_display_name}")
    print(f"     Goal: {outcome2.goal_reference_id}")
    print(
        f"     Interventions: {', '.join(outcome2.intervention_reference_ids) if outcome2.intervention_reference_ids else 'None'}"
    )
    print(f"  3. {outcome3.display_name}: {outcome3.value} {outcome3.value_unit}")
    print("     Progress: Not specified")
    print(f"     Goal: {outcome3.goal_reference_id}")
    print("     Interventions: None")
    print(f"  4. {outcome4.display_name}: {outcome4.value} {outcome4.value_unit}")
    print("     Progress: Not specified")
    print(f"     Goal: {outcome4.goal_reference_id}")
    print(
        f"     Interventions: {', '.join(outcome4.intervention_reference_ids) if outcome4.intervention_reference_ids else 'None'}"
    )


if __name__ == "__main__":
    main()
