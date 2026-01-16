"""Example of creating a Nutrition Section.

This example demonstrates how to create a Nutrition Section that includes:
- Nutritional status observations with SNOMED CT codes
- Nutrition assessments (diet followed, nutrition intake, weight changes)
- Multiple nutritional statuses over time
- Proper narrative table generation with assessment details
- Both coded and text values for assessment findings

The example shows three common scenarios:
1. Well-nourished patient on a low sodium diet
2. Patient at risk for malnutrition on a diabetic diet
3. Malnourished patient receiving enteral feeding

Template: 2.16.840.1.113883.10.20.22.2.57 (Nutrition Section)
"""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.nutrition import NutritionSection
from ccdakit.core.base import CDAVersion


# Define nutrition assessment data
class ExampleNutritionAssessment:
    """Example nutrition assessment observation."""

    def __init__(
        self,
        assessment_type,
        code,
        value,
        value_code=None,
        assessment_date=None,
    ):
        self._assessment_type = assessment_type
        self._code = code
        self._value = value
        self._value_code = value_code
        self._date = assessment_date or date.today()

    @property
    def assessment_type(self):
        return self._assessment_type

    @property
    def code(self):
        return self._code

    @property
    def value(self):
        return self._value

    @property
    def value_code(self):
        return self._value_code

    @property
    def date(self):
        return self._date


# Define nutritional status data
class ExampleNutritionalStatus:
    """Example nutritional status observation."""

    def __init__(
        self,
        status,
        status_code,
        status_date=None,
        assessments=None,
    ):
        self._status = status
        self._status_code = status_code
        self._date = status_date or date.today()
        self._assessments = assessments or []

    @property
    def status(self):
        return self._status

    @property
    def status_code(self):
        return self._status_code

    @property
    def date(self):
        return self._date

    @property
    def assessments(self):
        return self._assessments


def main():
    """Create and display a Nutrition Section example."""

    # Create nutrition assessments for a well-nourished patient
    diet_assessment = ExampleNutritionAssessment(
        assessment_type="Diet followed",
        code="226234005",  # Diet followed (observable entity)
        value="Low sodium diet",
        value_code="160670007",  # Low sodium diet
        assessment_date=date(2023, 10, 15),
    )

    intake_assessment = ExampleNutritionAssessment(
        assessment_type="Nutrition intake",
        code="226379006",  # Nutrition intake (observable entity)
        value="Adequate oral intake",
        value_code="289141003",  # Adequate oral intake
        assessment_date=date(2023, 10, 15),
    )

    # Create first nutritional status with assessments
    status1 = ExampleNutritionalStatus(
        status="Well nourished",
        status_code="17621005",  # Normal nutritional status
        status_date=date(2023, 10, 15),
        assessments=[diet_assessment, intake_assessment],
    )

    # Create nutrition assessment for a patient at risk
    diabetic_diet_assessment = ExampleNutritionAssessment(
        assessment_type="Diet followed",
        code="226234005",  # Diet followed (observable entity)
        value="Diabetic diet",
        value_code="160679008",  # Diabetic diet
        assessment_date=date(2023, 9, 15),
    )

    # Create second nutritional status
    status2 = ExampleNutritionalStatus(
        status="At risk for malnutrition",
        status_code="102636007",  # At risk for nutritional problem
        status_date=date(2023, 9, 15),
        assessments=[diabetic_diet_assessment],
    )

    # Create nutrition assessment for a malnourished patient
    enteral_feeding_assessment = ExampleNutritionAssessment(
        assessment_type="Nutrition intake",
        code="226379006",  # Nutrition intake (observable entity)
        value="Enteral feeding",
        value_code="229912004",  # Enteral feeding
        assessment_date=date(2023, 8, 1),
    )

    weight_loss_assessment = ExampleNutritionAssessment(
        assessment_type="Weight change",
        code="27113001",  # Body weight
        value="Unintentional weight loss 10% in 6 months",
        value_code=None,  # No specific code for this finding
        assessment_date=date(2023, 8, 1),
    )

    # Create third nutritional status
    status3 = ExampleNutritionalStatus(
        status="Malnourished",
        status_code="248325000",  # Malnourished
        status_date=date(2023, 8, 1),
        assessments=[enteral_feeding_assessment, weight_loss_assessment],
    )

    # Create the Nutrition Section
    section = NutritionSection(
        nutritional_statuses=[status1, status2, status3],
        title="Patient Nutrition",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Nutrition Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.57")
    print("  - Code: 61144-2 (Diet and nutrition) from LOINC")
    print("  - Number of nutritional statuses: 3")
    print("  - Total assessments: 5")
    print("\nNutritional Status Observations:")
    print("  1. Well nourished (17621005)")
    print("     - Diet followed: Low sodium diet")
    print("     - Nutrition intake: Adequate oral intake")
    print("  2. At risk for malnutrition (102636007)")
    print("     - Diet followed: Diabetic diet")
    print("  3. Malnourished (248325000)")
    print("     - Nutrition intake: Enteral feeding")
    print("     - Weight change: Unintentional weight loss 10% in 6 months")
    print("\nConformance:")
    print("  - CONF:1098-30477: Template ID present")
    print("  - CONF:1098-30478: Template ID root = 2.16.840.1.113883.10.20.22.2.57")
    print("  - CONF:1098-30318: Section code present")
    print("  - CONF:1098-30319: Code = 61144-2")
    print("  - CONF:1098-30320: Code system = LOINC (2.16.840.1.113883.6.1)")
    print("  - CONF:1098-31042: Title present")
    print("  - CONF:1098-31043: Narrative text present")
    print("  - CONF:1098-30321: Entry elements present")
    print("  - CONF:1098-30322: Nutritional Status Observation entries present")
    print("\nClinical Use Cases:")
    print("  - Monitoring nutritional status over time")
    print("  - Documenting special dietary requirements")
    print("  - Tracking nutrition interventions (e.g., enteral feeding)")
    print("  - Assessing risk for malnutrition")
    print("  - Supporting care coordination for patients with complex nutrition needs")


if __name__ == "__main__":
    main()
