"""
Example: Creating a Complications Section

This example demonstrates how to create a Complications Section for C-CDA documents.
The Complications Section contains problems that occurred during or around the time
of a procedure.
"""

from datetime import date

from ccdakit.builders.sections.complications import ComplicationsSection


class Complication:
    """Example complication implementation."""

    def __init__(
        self,
        name: str,
        code: str,
        code_system: str = "SNOMED",
        onset_date: date | None = None,
        resolved_date: date | None = None,
        status: str = "active",
        severity: str | None = None,
        related_procedure_code: str | None = None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._onset_date = onset_date
        self._resolved_date = resolved_date
        self._status = status
        self._severity = severity
        self._related_procedure_code = related_procedure_code

    @property
    def name(self) -> str:
        return self._name

    @property
    def code(self) -> str:
        return self._code

    @property
    def code_system(self) -> str:
        return self._code_system

    @property
    def onset_date(self) -> date | None:
        return self._onset_date

    @property
    def resolved_date(self) -> date | None:
        return self._resolved_date

    @property
    def status(self) -> str:
        return self._status

    @property
    def severity(self) -> str | None:
        return self._severity

    @property
    def related_procedure_code(self) -> str | None:
        return self._related_procedure_code

    @property
    def persistent_id(self):
        return None


def main():
    """Create and display a Complications Section."""
    # Create sample complications
    complications = [
        Complication(
            name="Postoperative bleeding",
            code="83132003",
            code_system="SNOMED",
            onset_date=date(2024, 1, 15),
            status="active",
            severity="severe",
            related_procedure_code="80146002",  # Appendectomy
        ),
        Complication(
            name="Surgical site infection",
            code="432119003",
            code_system="SNOMED",
            onset_date=date(2024, 1, 18),
            status="active",
            severity="moderate",
            related_procedure_code="80146002",  # Appendectomy
        ),
        Complication(
            name="Postoperative fever",
            code="386661006",
            code_system="SNOMED",
            onset_date=date(2024, 1, 16),
            resolved_date=date(2024, 1, 20),
            status="resolved",
            severity="mild",
            related_procedure_code="80146002",  # Appendectomy
        ),
    ]

    # Create Complications Section
    section = ComplicationsSection(complications=complications, title="Surgical Complications")

    # Generate XML
    xml_string = section.to_string(pretty=True)

    print("Complications Section XML:")
    print("=" * 80)
    print(xml_string)
    print("=" * 80)

    # Display summary
    print("\nSection Summary:")
    print(f"Total complications: {len(complications)}")
    print("\nComplications:")
    for comp in complications:
        print(f"  - {comp.name} ({comp.code})")
        print(f"    Status: {comp.status}, Severity: {comp.severity or 'Not specified'}")
        print(f"    Onset: {comp.onset_date}, Resolved: {comp.resolved_date or 'N/A'}")


if __name__ == "__main__":
    main()
