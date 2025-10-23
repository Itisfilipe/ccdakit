"""Example usage of Medications Administered Section builder.

This example demonstrates how to create a Medications Administered Section
for documenting medications and fluids given during a procedure or encounter.
"""

from datetime import datetime

from ccdakit.builders.sections.medications_administered import (
    MedicationsAdministeredSection,
)


class MedicationAdministered:
    """Example medication administration data."""

    def __init__(
        self,
        name,
        code,
        dose,
        route,
        administration_time,
        administration_end_time=None,
        rate=None,
        site=None,
        status="completed",
        performer=None,
        indication=None,
        instructions=None,
    ):
        self._name = name
        self._code = code
        self._dose = dose
        self._route = route
        self._administration_time = administration_time
        self._administration_end_time = administration_end_time
        self._rate = rate
        self._site = site
        self._status = status
        self._performer = performer
        self._indication = indication
        self._instructions = instructions

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def dose(self):
        return self._dose

    @property
    def route(self):
        return self._route

    @property
    def administration_time(self):
        return self._administration_time

    @property
    def administration_end_time(self):
        return self._administration_end_time

    @property
    def rate(self):
        return self._rate

    @property
    def site(self):
        return self._site

    @property
    def status(self):
        return self._status

    @property
    def performer(self):
        return self._performer

    @property
    def indication(self):
        return self._indication

    @property
    def instructions(self):
        return self._instructions


def main():
    """Create and display a Medications Administered Section."""

    # Example medications administered during a procedure
    medications = [
        MedicationAdministered(
            name="Ondansetron 4mg/2mL injection",
            code="312086",
            dose="4 mg",
            route="iv",
            administration_time=datetime(2023, 12, 15, 14, 30),
            status="completed",
            performer="Jane Smith, RN",
            site="right arm",
            indication="Nausea prophylaxis",
            instructions="Administer slowly over 2-5 minutes",
        ),
        MedicationAdministered(
            name="Normal Saline 0.9% IV Solution",
            code="313002",
            dose="1000 mL",
            route="intravenous",
            rate="100 mL/hr",
            administration_time=datetime(2023, 12, 15, 10, 0),
            administration_end_time=datetime(2023, 12, 15, 20, 0),
            status="completed",
            performer="RN Team",
            site="left antecubital fossa",
            indication="Hydration",
        ),
        MedicationAdministered(
            name="Acetaminophen 325mg oral tablet",
            code="197806",
            dose="650 mg",
            route="oral",
            administration_time=datetime(2023, 12, 15, 16, 0),
            status="completed",
            performer="Dr. Robert Jones",
            indication="Pain management",
        ),
        MedicationAdministered(
            name="Propofol 10mg/mL emulsion",
            code="153476",
            dose="200 mg",
            route="intravenous",
            rate="20 mg/min",
            site="right antecubital fossa",
            administration_time=datetime(2023, 12, 15, 8, 0),
            administration_end_time=datetime(2023, 12, 15, 8, 10),
            status="completed",
            performer="Dr. Sarah Wilson, MD",
            indication="Sedation",
            instructions="Titrate to effect, maintain adequate sedation",
        ),
    ]

    # Create the section
    section = MedicationsAdministeredSection(
        medications=medications,
        title="Medications Administered During Procedure",
    )

    # Generate and display XML
    xml = section.to_string(pretty=True)
    print(xml)


if __name__ == "__main__":
    main()
