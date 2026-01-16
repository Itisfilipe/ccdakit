"""Example of creating a Physical Exam Section with wound observations."""

from datetime import datetime

from lxml import etree

from ccdakit.builders.sections.physical_exam import PhysicalExamSection
from ccdakit.core.base import CDAVersion


class ExampleWoundObservation:
    """Example wound observation for physical exam documentation.

    This class implements the WoundObservationProtocol interface,
    demonstrating how to create wound observation data for C-CDA documents.
    """

    def __init__(
        self,
        wound_type,
        wound_code,
        date,
        location=None,
        location_code=None,
        laterality=None,
        laterality_code=None,
    ):
        """Initialize a wound observation.

        Args:
            wound_type: Type of wound (e.g., "Pressure ulcer", "Surgical wound")
            wound_code: SNOMED CT code for the wound type
            date: Date and time the observation was made
            location: Optional body site where the wound is located
            location_code: Optional SNOMED CT code for the body location
            laterality: Optional laterality (e.g., "Left", "Right")
            laterality_code: Optional SNOMED CT code for laterality
        """
        self._wound_type = wound_type
        self._wound_code = wound_code
        self._date = date
        self._location = location
        self._location_code = location_code
        self._laterality = laterality
        self._laterality_code = laterality_code

    @property
    def wound_type(self):
        """Type of wound."""
        return self._wound_type

    @property
    def wound_code(self):
        """SNOMED CT code for wound type."""
        return self._wound_code

    @property
    def date(self):
        """Date and time of observation."""
        return self._date

    @property
    def location(self):
        """Body site location."""
        return self._location

    @property
    def location_code(self):
        """SNOMED CT code for body location."""
        return self._location_code

    @property
    def laterality(self):
        """Laterality of wound (Left/Right)."""
        return self._laterality

    @property
    def laterality_code(self):
        """SNOMED CT code for laterality."""
        return self._laterality_code


def main():
    """Create and display a Physical Exam Section example."""

    # Create wound observations from a patient examination
    # These observations would typically come from your EMR/EHR system

    # Example 1: Pressure ulcer on sacral region (no laterality needed)
    pressure_ulcer = ExampleWoundObservation(
        wound_type="Pressure ulcer",
        wound_code="399912005",  # SNOMED CT code
        date=datetime(2024, 1, 15, 14, 30),
        location="Sacral region",
        location_code="54735007",  # SNOMED CT code
    )

    # Example 2: Surgical wound on abdomen from recent surgery
    surgical_wound = ExampleWoundObservation(
        wound_type="Surgical wound",
        wound_code="225552003",  # SNOMED CT code
        date=datetime(2024, 1, 15, 14, 35),
        location="Abdomen",
        location_code="818983003",  # SNOMED CT code
    )

    # Example 3: Laceration on left lower leg with laterality
    laceration = ExampleWoundObservation(
        wound_type="Laceration",
        wound_code="312608009",  # SNOMED CT code
        date=datetime(2024, 1, 15, 14, 40),
        location="Lower leg",
        location_code="30021000",  # SNOMED CT code
        laterality="Left",
        laterality_code="7771000",  # SNOMED CT code for "Left"
    )

    # Example 4: Burn on right hand with laterality
    burn = ExampleWoundObservation(
        wound_type="Burn of skin",
        wound_code="125666000",  # SNOMED CT code
        date=datetime(2024, 1, 15, 14, 45),
        location="Hand",
        location_code="85562004",  # SNOMED CT code
        laterality="Right",
        laterality_code="24028007",  # SNOMED CT code for "Right"
    )

    # Example 5: Diabetic ulcer on left foot
    diabetic_ulcer = ExampleWoundObservation(
        wound_type="Diabetic foot ulcer",
        wound_code="371087003",  # SNOMED CT code
        date=datetime(2024, 1, 15, 14, 50),
        location="Foot",
        location_code="56459004",  # SNOMED CT code
        laterality="Left",
        laterality_code="7771000",  # SNOMED CT code for "Left"
    )

    # Create the Physical Exam Section with all observations
    section = PhysicalExamSection(
        wound_observations=[
            pressure_ulcer,
            surgical_wound,
            laceration,
            burn,
            diabetic_ulcer,
        ],
        title="Physical Examination Findings",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(
        elem,
        pretty_print=True,
        encoding="unicode",
        xml_declaration=False,
    )

    print("Physical Exam Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.2.10")
    print("  - Extension: 2015-08-01")
    print("  - Section Code: 29545-1 (Physical Findings)")
    print("  - Number of wound observations: 5")
    print("\nWound Observations:")
    print("  1. Pressure ulcer - Sacral region (no laterality)")
    print("  2. Surgical wound - Abdomen (no laterality)")
    print("  3. Laceration - Left lower leg")
    print("  4. Burn of skin - Right hand")
    print("  5. Diabetic foot ulcer - Left foot")
    print("\nConformance:")
    print("  - CONF:1198-7806: Template ID present")
    print("  - CONF:1198-15397: Section code present (29545-1)")
    print("  - CONF:1198-7808: Title present")
    print("  - CONF:1198-7809: Narrative text present")
    print("  - CONF:1198-31926: Wound observation entries present")
    print("\nEntry Details:")
    print("  - Each wound observation conforms to Longitudinal Care Wound Observation")
    print("  - Template: 2.16.840.1.113883.10.20.22.4.114:2015-08-01")
    print("  - Includes wound type (SNOMED CT coded)")
    print("  - Includes target site code for body location")
    print("  - Includes laterality qualifier when applicable")
    print("\nNarrative Table:")
    print("  - Human-readable table with Date/Time, Wound Type, Location, Laterality")
    print("  - Each wound type has a unique ID for referencing from structured entries")
    print("  - Laterality shown as '-' when not applicable")

    # Example of creating a section with no observations
    print("\n" + "=" * 80)
    print("\nExample with no observations (nullFlavor scenario):")
    print("=" * 80)

    empty_section = PhysicalExamSection(
        title="Physical Examination",
        version=CDAVersion.R2_1,
    )

    empty_elem = empty_section.to_element()
    empty_xml = etree.tostring(
        empty_elem,
        pretty_print=True,
        encoding="unicode",
        xml_declaration=False,
    )
    print(empty_xml)
    print("Note: When no observations are provided, narrative shows default text.")


if __name__ == "__main__":
    main()
