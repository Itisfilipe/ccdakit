"""Example: Hospital Discharge Studies Summary Section

This example demonstrates how to create a Hospital Discharge Studies Summary
Section with various types of studies (imaging, laboratory, and procedure
observations) at discharge.
"""

from datetime import datetime

from lxml import etree

from ccdakit.builders.sections.discharge_studies import (
    HospitalDischargeStudiesSummarySection,
)


# Define the discharge study data classes
class DischargeStudy:
    """Represents a discharge study observation."""

    def __init__(
        self,
        study_name: str,
        study_code: str,
        value: str,
        unit: str | None = None,
        status: str = "final",
        effective_time: datetime = datetime.now(),
        value_type: str | None = None,
        interpretation: str | None = None,
        reference_range_low: str | None = None,
        reference_range_high: str | None = None,
        reference_range_unit: str | None = None,
    ):
        self.study_name = study_name
        self.study_code = study_code
        self.value = value
        self.unit = unit
        self.status = status
        self.effective_time = effective_time
        self.value_type = value_type
        self.interpretation = interpretation
        self.reference_range_low = reference_range_low
        self.reference_range_high = reference_range_high
        self.reference_range_unit = reference_range_unit

    # Compatibility properties for ResultObservationProtocol
    @property
    def test_name(self):
        return self.study_name

    @property
    def test_code(self):
        return self.study_code


class DischargeStudyOrganizer:
    """Represents a discharge study panel organizer."""

    def __init__(
        self,
        study_panel_name: str,
        study_panel_code: str,
        status: str,
        effective_time: datetime,
        studies: list[DischargeStudy],
    ):
        self.study_panel_name = study_panel_name
        self.study_panel_code = study_panel_code
        self.status = status
        self.effective_time = effective_time
        self.studies = studies

    # Compatibility properties for ResultOrganizerProtocol
    @property
    def panel_name(self):
        return self.study_panel_name

    @property
    def panel_code(self):
        return self.study_panel_code

    @property
    def results(self):
        return self.studies


def main():
    """Create and display a Hospital Discharge Studies Summary Section example."""

    # Example 1: Imaging Studies Panel
    imaging_studies = [
        DischargeStudy(
            study_name="Chest X-Ray (2 views)",
            study_code="36643-5",
            value="No acute cardiopulmonary process. Heart size is normal.",
            unit=None,
            status="final",
            effective_time=datetime(2023, 10, 15, 14, 30),
            interpretation="Normal",
        ),
        DischargeStudy(
            study_name="CT Chest with Contrast",
            study_code="75571",
            value="No pulmonary embolism. No acute findings.",
            unit=None,
            status="final",
            effective_time=datetime(2023, 10, 15, 15, 0),
            interpretation="Normal",
        ),
    ]

    imaging_organizer = DischargeStudyOrganizer(
        study_panel_name="Chest Imaging Studies",
        study_panel_code="72170-4",
        status="completed",
        effective_time=datetime(2023, 10, 15, 14, 30),
        studies=imaging_studies,
    )

    # Example 2: Laboratory Studies Panel
    lab_studies = [
        DischargeStudy(
            study_name="Hemoglobin",
            study_code="718-7",
            value="14.5",
            unit="g/dL",
            status="final",
            effective_time=datetime(2023, 10, 15, 8, 0),
            interpretation="Normal",
            reference_range_low="12.0",
            reference_range_high="16.0",
            reference_range_unit="g/dL",
        ),
        DischargeStudy(
            study_name="Hemoglobin A1c",
            study_code="4548-4",
            value="6.5",
            unit="%",
            status="final",
            effective_time=datetime(2023, 10, 15, 8, 0),
            interpretation="Normal",
            reference_range_low="4.0",
            reference_range_high="5.6",
            reference_range_unit="%",
        ),
    ]

    lab_organizer = DischargeStudyOrganizer(
        study_panel_name="Discharge Laboratory Panel",
        study_panel_code="58410-2",
        status="completed",
        effective_time=datetime(2023, 10, 15, 8, 0),
        studies=lab_studies,
    )

    # Example 3: Cardiac Studies Panel
    cardiac_studies = [
        DischargeStudy(
            study_name="Echocardiogram - Left ventricular ejection fraction",
            study_code="10230-1",
            value="55",
            unit="%",
            status="final",
            effective_time=datetime(2023, 10, 15, 11, 15),
            interpretation="Normal",
            reference_range_low="50",
            reference_range_high="70",
            reference_range_unit="%",
        ),
    ]

    cardiac_organizer = DischargeStudyOrganizer(
        study_panel_name="Cardiac Studies",
        study_panel_code="34752-6",
        status="completed",
        effective_time=datetime(2023, 10, 15, 11, 15),
        studies=cardiac_studies,
    )

    # Create the Hospital Discharge Studies Summary Section
    section = HospitalDischargeStudiesSummarySection(
        study_organizers=[imaging_organizer, lab_organizer, cardiac_organizer],
        title="Hospital Discharge Studies Summary",
    )

    # Generate XML
    xml_element = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(
        xml_element, pretty_print=True, encoding="unicode", xml_declaration=False
    )

    print("=" * 80)
    print("Hospital Discharge Studies Summary Section - Example")
    print("=" * 80)
    print(xml_string)
    print("=" * 80)

    # Also demonstrate the narrative table
    text_elem = xml_element.find(".//{urn:hl7-org:v3}text")
    if text_elem is not None:
        print("\nNarrative Text (HTML Table):")
        print("=" * 80)
        narrative_string = etree.tostring(
            text_elem, pretty_print=True, encoding="unicode"
        )
        print(narrative_string)


if __name__ == "__main__":
    main()
