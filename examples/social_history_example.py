"""Example of creating a Social History Section."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.sections.social_history import SocialHistorySection
from ccdakit.core.base import CDAVersion


class ExampleSmokingStatus:
    """Example smoking status data that satisfies the SmokingStatusProtocol."""

    def __init__(
        self,
        smoking_status,
        code,
        observation_date,
    ):
        self._smoking_status = smoking_status
        self._code = code
        self._date = observation_date

    @property
    def smoking_status(self):
        return self._smoking_status

    @property
    def code(self):
        return self._code

    @property
    def date(self):
        return self._date


def main():
    """Create and display a Social History Section example."""

    # Create sample smoking status observations
    # These represent "snapshot in time" observations per Meaningful Use Stage 2 requirements

    # Example 1: Current every day smoker
    current_smoker = ExampleSmokingStatus(
        smoking_status="Current every day smoker",
        code="449868002",  # SNOMED CT code from Smoking Status Value Set
        observation_date=date(2023, 10, 15),
    )

    # Example 2: Former smoker
    former_smoker = ExampleSmokingStatus(
        smoking_status="Former smoker",
        code="8517006",  # SNOMED CT code
        observation_date=date(2023, 9, 10),
    )

    # Example 3: Never smoker (with datetime to show time precision)
    never_smoker = ExampleSmokingStatus(
        smoking_status="Never smoker",
        code="266919005",  # SNOMED CT code
        observation_date=datetime(2023, 8, 5, 10, 30),
    )

    # Create the Social History Section
    section = SocialHistorySection(
        smoking_statuses=[current_smoker, former_smoker, never_smoker],
        title="Social History",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Social History Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.17")
    print("  - Extension: 2015-08-01")
    print("  - Number of smoking status observations: 3")
    print("\nSmoking Status Observations:")
    print("  1. Current every day smoker (SNOMED CT: 449868002)")
    print("     - Date observed: 2023-10-15")
    print("  2. Former smoker (SNOMED CT: 8517006)")
    print("     - Date observed: 2023-09-10")
    print("  3. Never smoker (SNOMED CT: 266919005)")
    print("     - Date observed: 2023-08-05 10:30")
    print("\nCommon Smoking Status Codes (from Value Set 2.16.840.1.113883.11.20.9.38):")
    print("  - 449868002: Current every day smoker")
    print("  - 428041000124106: Current some day smoker")
    print("  - 8517006: Former smoker")
    print("  - 266919005: Never smoker")
    print("  - 266927001: Unknown if ever smoked")
    print("\nConformance:")
    print("  - CONF:1198-7936: Template ID present")
    print("  - CONF:1198-7938: Code 29762-2 (Social History)")
    print("  - CONF:1198-7940: Title present")
    print("  - CONF:1198-7941: Narrative text with table present")
    print("  - CONF:1198-14820: Smoking Status Observation entries present")
    print("\nMeaningful Use Stage 2 Requirement:")
    print("  - This section fulfills the requirement to record smoking status")
    print("  - Each observation is a 'snapshot in time' (point in time, not interval)")


if __name__ == "__main__":
    main()
