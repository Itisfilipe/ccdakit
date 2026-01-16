"""Example of creating a Vital Signs Section.

This example demonstrates how to create a C-CDA Vital Signs Section with
multiple organizers containing various vital sign observations.
"""

from datetime import datetime

from lxml import etree

from ccdakit.builders.sections.vital_signs import VitalSignsSection
from ccdakit.core.base import CDAVersion


# Define vital sign observation data
class ExampleVitalSign:
    """Example vital sign observation."""

    def __init__(
        self,
        vital_type,
        code,
        value,
        unit,
        obs_date=None,
        interpretation=None,
    ):
        self._type = vital_type
        self._code = code
        self._value = value
        self._unit = unit
        self._date = obs_date or datetime.now()
        self._interpretation = interpretation

    @property
    def type(self):
        return self._type

    @property
    def code(self):
        return self._code

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit

    @property
    def date(self):
        return self._date

    @property
    def interpretation(self):
        return self._interpretation


# Define vital signs organizer data
class ExampleVitalSignsOrganizer:
    """Example vital signs organizer (groups observations taken at same time)."""

    def __init__(self, organizer_date, vital_signs_list=None):
        self._date = organizer_date
        self._vital_signs = vital_signs_list or []

    @property
    def date(self):
        return self._date

    @property
    def vital_signs(self):
        return self._vital_signs


def main():
    """Create and display a Vital Signs Section example."""

    # First organizer: Blood pressure and heart rate from morning visit
    morning_datetime = datetime(2024, 1, 15, 9, 30)
    morning_vitals = ExampleVitalSignsOrganizer(
        organizer_date=morning_datetime,
        vital_signs_list=[
            ExampleVitalSign(
                vital_type="Systolic Blood Pressure",
                code="8480-6",
                value="120",
                unit="mm[Hg]",
                obs_date=morning_datetime,
                interpretation="Normal",
            ),
            ExampleVitalSign(
                vital_type="Diastolic Blood Pressure",
                code="8462-4",
                value="80",
                unit="mm[Hg]",
                obs_date=morning_datetime,
                interpretation="Normal",
            ),
            ExampleVitalSign(
                vital_type="Heart Rate",
                code="8867-4",
                value="72",
                unit="bpm",
                obs_date=morning_datetime,
                interpretation="Normal",
            ),
            ExampleVitalSign(
                vital_type="Body Temperature",
                code="8310-5",
                value="36.7",
                unit="Cel",
                obs_date=morning_datetime,
                interpretation="Normal",
            ),
        ],
    )

    # Second organizer: Follow-up measurements with weight
    afternoon_datetime = datetime(2024, 1, 15, 14, 45)
    afternoon_vitals = ExampleVitalSignsOrganizer(
        organizer_date=afternoon_datetime,
        vital_signs_list=[
            ExampleVitalSign(
                vital_type="Systolic Blood Pressure",
                code="8480-6",
                value="128",
                unit="mm[Hg]",
                obs_date=afternoon_datetime,
                interpretation="High",
            ),
            ExampleVitalSign(
                vital_type="Diastolic Blood Pressure",
                code="8462-4",
                value="84",
                unit="mm[Hg]",
                obs_date=afternoon_datetime,
                interpretation="High",
            ),
            ExampleVitalSign(
                vital_type="Heart Rate",
                code="8867-4",
                value="78",
                unit="bpm",
                obs_date=afternoon_datetime,
                interpretation="Normal",
            ),
            ExampleVitalSign(
                vital_type="Body Weight",
                code="29463-7",
                value="75.5",
                unit="kg",
                obs_date=afternoon_datetime,
                interpretation=None,  # No interpretation
            ),
            ExampleVitalSign(
                vital_type="Body Height",
                code="8302-2",
                value="175",
                unit="cm",
                obs_date=afternoon_datetime,
                interpretation=None,
            ),
            ExampleVitalSign(
                vital_type="Body Mass Index",
                code="39156-5",
                value="24.7",
                unit="kg/m2",
                obs_date=afternoon_datetime,
                interpretation="Normal",
            ),
        ],
    )

    # Create the Vital Signs Section
    section = VitalSignsSection(
        vital_signs_organizers=[morning_vitals, afternoon_vitals],
        title="Vital Signs",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Vital Signs Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.4.1")
    print("  - Extension: 2015-08-01")
    print("  - Number of organizers: 2")
    print("  - Morning vitals: 4 observations")
    print("  - Afternoon vitals: 6 observations")
    print("  - Total observations: 10")
    print("\nVital Signs Details:")
    print("  Morning (09:30):")
    print("    - Blood Pressure: 120/80 mm[Hg] (Normal)")
    print("    - Heart Rate: 72 bpm (Normal)")
    print("    - Temperature: 36.7 Cel (Normal)")
    print("\n  Afternoon (14:45):")
    print("    - Blood Pressure: 128/84 mm[Hg] (High)")
    print("    - Heart Rate: 78 bpm (Normal)")
    print("    - Weight: 75.5 kg")
    print("    - Height: 175 cm")
    print("    - BMI: 24.7 kg/m2 (Normal)")
    print("\nConformance:")
    print("  - CONF:1198-7273: Template ID present")
    print("  - CONF:1198-7275: Code 8716-3 (Vital signs)")
    print("  - CONF:1198-7276: Title present")
    print("  - CONF:1198-7277: Narrative text present")
    print("  - CONF:1198-15964: Vital Signs Organizer entries present")
    print("\nCommon LOINC Codes for Vital Signs:")
    print("  - 8480-6: Systolic Blood Pressure")
    print("  - 8462-4: Diastolic Blood Pressure")
    print("  - 8867-4: Heart Rate")
    print("  - 8310-5: Body Temperature")
    print("  - 29463-7: Body Weight")
    print("  - 8302-2: Body Height")
    print("  - 39156-5: Body Mass Index")
    print("  - 9279-1: Respiratory Rate")
    print("  - 2710-2: Oxygen Saturation")


if __name__ == "__main__":
    main()
