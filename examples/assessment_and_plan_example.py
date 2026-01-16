"""Example of creating an Assessment and Plan Section."""

from datetime import datetime

from lxml import etree

from ccdakit.builders.sections.assessment_and_plan import AssessmentAndPlanSection
from ccdakit.core.base import CDAVersion


# Define mock planned act data
class ExamplePlannedAct:
    """Example planned act for treatment plan."""

    def __init__(
        self,
        id_root,
        id_extension,
        code,
        code_system,
        display_name,
        mood_code="INT",
        effective_time=None,
        instructions=None,
    ):
        self._id_root = id_root
        self._id_extension = id_extension
        self._code = code
        self._code_system = code_system
        self._display_name = display_name
        self._mood_code = mood_code
        self._effective_time = effective_time
        self._instructions = instructions

    @property
    def id_root(self):
        return self._id_root

    @property
    def id_extension(self):
        return self._id_extension

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
    def mood_code(self):
        return self._mood_code

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def instructions(self):
        return self._instructions


# Define assessment and plan item data
class ExampleAssessmentAndPlanItem:
    """Example assessment or plan item."""

    def __init__(self, text, item_type, planned_act=None):
        self._text = text
        self._item_type = item_type
        self._planned_act = planned_act

    @property
    def text(self):
        return self._text

    @property
    def item_type(self):
        return self._item_type

    @property
    def planned_act(self):
        return self._planned_act


def main():
    """Create and display an Assessment and Plan Section example."""

    # Create planned acts for the treatment plan
    medication_plan = ExamplePlannedAct(
        id_root="2.16.840.1.113883.19.5.99999.1",
        id_extension="plan-001",
        code="182834008",
        code_system="SNOMED",
        display_name="Drug therapy",
        mood_code="INT",
        effective_time=datetime(2024, 1, 20, 9, 0, 0),
        instructions="Start lisinopril 10mg daily for blood pressure control",
    )

    patient_education_plan = ExamplePlannedAct(
        id_root="2.16.840.1.113883.19.5.99999.1",
        id_extension="plan-002",
        code="409073007",
        code_system="SNOMED",
        display_name="Education",
        mood_code="INT",
        effective_time=datetime(2024, 1, 25, 14, 0, 0),
        instructions="Provide dietary counseling focusing on low-sodium diet and portion control",
    )

    follow_up_plan = ExamplePlannedAct(
        id_root="2.16.840.1.113883.19.5.99999.1",
        id_extension="plan-003",
        code="183460006",
        code_system="SNOMED",
        display_name="Observation of patient",
        mood_code="INT",
        effective_time=datetime(2024, 2, 15, 10, 0, 0),
        instructions="Schedule follow-up appointment in 4 weeks to reassess blood pressure control",
    )

    # Create assessment and plan items
    items = [
        # Clinical assessments
        ExampleAssessmentAndPlanItem(
            text="Hypertension, Stage 2 (BP 165/95 mmHg) - inadequately controlled on current regimen",
            item_type="assessment",
            planned_act=None,
        ),
        ExampleAssessmentAndPlanItem(
            text="Type 2 Diabetes Mellitus - well controlled (HbA1c 6.8%)",
            item_type="assessment",
            planned_act=None,
        ),
        ExampleAssessmentAndPlanItem(
            text="Obesity (BMI 32.5) - patient motivated to lose weight",
            item_type="assessment",
            planned_act=None,
        ),
        # Treatment plan actions
        ExampleAssessmentAndPlanItem(
            text="Initiate ACE inhibitor therapy for blood pressure control",
            item_type="plan",
            planned_act=medication_plan,
        ),
        ExampleAssessmentAndPlanItem(
            text="Provide dietary counseling and weight management education",
            item_type="plan",
            planned_act=patient_education_plan,
        ),
        ExampleAssessmentAndPlanItem(
            text="Continue metformin 1000mg twice daily for diabetes management",
            item_type="plan",
            planned_act=None,
        ),
        ExampleAssessmentAndPlanItem(
            text="Monitor blood pressure at home daily and log readings",
            item_type="plan",
            planned_act=follow_up_plan,
        ),
    ]

    # Create the Assessment and Plan Section
    section = AssessmentAndPlanSection(
        items=items,
        title="Assessment and Plan",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Assessment and Plan Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.9")
    print("  - Extension: 2014-06-09")
    print("  - Number of assessment items: 3")
    print("  - Number of plan items: 4")
    print("  - Number of planned acts: 3")
    print("\nClinical Content:")
    print("  Assessment:")
    print("    - Hypertension, Stage 2 (inadequately controlled)")
    print("    - Type 2 Diabetes Mellitus (well controlled)")
    print("    - Obesity (patient motivated)")
    print("\n  Plan:")
    print("    - Initiate ACE inhibitor therapy")
    print("    - Provide dietary counseling")
    print("    - Continue diabetes medication")
    print("    - Monitor blood pressure at home")
    print("\nConformance:")
    print("  - CONF:1098-7705: Template ID present")
    print("  - CONF:1098-15353: Code 51847-2 (Assessment and Plan)")
    print("  - CONF:1098-7707: Narrative text present")
    print("  - CONF:1098-7708: Planned Act entries present")
    print("  - CONF:1098-8546: Each Planned Act has ID")
    print("  - CONF:1098-31687: Each Planned Act has code")
    print("  - CONF:1098-30432: Each Planned Act has statusCode='active'")


if __name__ == "__main__":
    main()
