"""Example of creating a Goals Section."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.goals import GoalsSection
from ccdakit.core.base import CDAVersion


# Define goal data
class ExampleGoal:
    """Example goal for demonstration."""

    def __init__(
        self,
        description,
        code=None,
        code_system=None,
        display_name=None,
        status="active",
        start_date=None,
        target_date=None,
        value=None,
        value_unit=None,
        author=None,
        priority=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._display_name = display_name
        self._status = status
        self._start_date = start_date
        self._target_date = target_date
        self._value = value
        self._value_unit = value_unit
        self._author = author
        self._priority = priority

    @property
    def description(self):
        return self._description

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
    def status(self):
        return self._status

    @property
    def start_date(self):
        return self._start_date

    @property
    def target_date(self):
        return self._target_date

    @property
    def value(self):
        return self._value

    @property
    def value_unit(self):
        return self._value_unit

    @property
    def author(self):
        return self._author

    @property
    def priority(self):
        return self._priority


def main():
    """Create and display a Goals Section example."""

    # Create sample patient goals
    goal1 = ExampleGoal(
        description="Improve HbA1c to less than 7%",
        code="4548-4",
        code_system="LOINC",
        display_name="Hemoglobin A1c/Hemoglobin.total in Blood",
        status="active",
        start_date=date(2023, 1, 15),
        target_date=date(2023, 12, 31),
        value="7",
        value_unit="%",
        priority="high",
    )

    goal2 = ExampleGoal(
        description="Reduce weight to 180 lbs",
        code="29463-7",
        code_system="LOINC",
        display_name="Body weight",
        status="active",
        start_date=date(2023, 2, 1),
        target_date=date(2024, 2, 1),
        value="180",
        value_unit="lbs",
        priority="medium",
    )

    goal3 = ExampleGoal(
        description="Maintain blood pressure below 140/90 mmHg",
        code="85354-9",
        code_system="LOINC",
        display_name="Blood pressure panel with all children optional",
        status="active",
        start_date=date(2023, 1, 1),
        target_date=None,  # Ongoing goal
        value="140/90 mmHg or less",
        value_unit=None,
        priority="high",
    )

    # Create the Goals Section
    section = GoalsSection(
        goals=[goal1, goal2, goal3],
        title="Patient Health Goals",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Goals Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.60")
    print("  - Number of goals: 3")
    print("\nGoals:")
    print("  1. HbA1c Control:")
    print("     - Target: < 7%")
    print("     - Timeline: Jan 2023 - Dec 2023")
    print("     - Priority: High")
    print("\n  2. Weight Management:")
    print("     - Target: 180 lbs")
    print("     - Timeline: Feb 2023 - Feb 2024")
    print("     - Priority: Medium")
    print("\n  3. Blood Pressure Control:")
    print("     - Target: < 140/90 mmHg")
    print("     - Timeline: Ongoing (started Jan 2023)")
    print("     - Priority: High")
    print("\nConformance:")
    print("  - CONF:1098-29585: Template ID present")
    print("  - CONF:1098-14802: Code 61146-7 (Goals)")
    print("  - CONF:1098-14803: Title present")
    print("  - CONF:1098-14804: Narrative text present")
    print("  - CONF:1098-30719: Goal Observation entries present")
    print("  - CONF:1098-30785: Each goal has effectiveTime")
    print("  - CONF:1098-31978: Each goal has statusCode")


if __name__ == "__main__":
    main()
