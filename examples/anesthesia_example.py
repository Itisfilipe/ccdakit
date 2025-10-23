"""Example of using the Anesthesia Section builder.

This example demonstrates how to create an Anesthesia Section for a C-CDA
document, including anesthesia type/procedure and anesthesia agents.
"""

from datetime import datetime

from ccdakit.builders.sections import AnesthesiaSection


# Mock classes for demonstration
class AnesthesiaRecord:
    """Mock anesthesia record for demonstration."""

    def __init__(self):
        self.anesthesia_type = "Conscious sedation"
        self.anesthesia_code = "48598005"
        self.anesthesia_code_system = "SNOMED CT"
        self.start_time = datetime(2023, 10, 15, 10, 30)
        self.end_time = datetime(2023, 10, 15, 12, 45)
        self.status = "completed"
        self.route = "Intravenous"
        self.performer_name = "Dr. Michael Chen, MD"
        self.notes = "Patient tolerated procedure well"

        # Anesthesia agents used
        self.anesthesia_agents = [
            AnesthesiaAgent(
                name="Propofol",
                code="8782",
                dosage="200 mg",
                route="Intravenous",
            ),
            AnesthesiaAgent(
                name="Fentanyl",
                code="4337",
                dosage="100 mcg",
                route="Intravenous",
            ),
        ]


class AnesthesiaAgent:
    """Mock anesthesia agent/medication for demonstration."""

    def __init__(self, name, code, dosage, route):
        self._name = name
        self._code = code
        self._dosage = dosage
        self._route = route
        self._status = "completed"
        self._start_date = datetime(2023, 10, 15, 10, 30)
        self._end_date = None
        self._instructions = None

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def status(self):
        return self._status

    @property
    def route(self):
        return self._route

    @property
    def dosage(self):
        return self._dosage

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def instructions(self):
        return self._instructions


def main():
    """Generate example Anesthesia Section XML."""
    # Create anesthesia record
    anesthesia = AnesthesiaRecord()

    # Build the Anesthesia Section
    section = AnesthesiaSection(
        anesthesia_records=[anesthesia],
        title="Procedure Anesthesia",
    )

    # Generate XML
    xml_string = section.to_string(pretty=True)

    print("Anesthesia Section XML:")
    print("=" * 80)
    print(xml_string)
    print("=" * 80)

    # Display information about the section
    print("\nSection Information:")
    print(f"- Template ID: 2.16.840.1.113883.10.20.22.2.25 (2014-06-09)")
    print(f"- LOINC Code: 59774-0 (Anesthesia)")
    print(f"- Anesthesia Type: {anesthesia.anesthesia_type}")
    print(f"- Number of Agents: {len(anesthesia.anesthesia_agents)}")
    print(f"- Performer: {anesthesia.performer_name}")
    print(f"- Status: {anesthesia.status}")


if __name__ == "__main__":
    main()
