"""Example: Creating a Discharge Diagnosis Section.

This example demonstrates how to create a C-CDA Discharge Diagnosis Section
with multiple discharge diagnoses.
"""

from datetime import date

from ccdakit.builders.sections.discharge_diagnosis import DischargeDiagnosisSection


class DischargeDiagnosis:
    """Simple discharge diagnosis implementation."""

    def __init__(
        self,
        name: str,
        code: str,
        code_system: str,
        status: str = "active",
        diagnosis_date: date | None = None,
        resolved_date: date | None = None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._status = status
        self._diagnosis_date = diagnosis_date
        self._resolved_date = resolved_date

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
    def status(self) -> str:
        return self._status

    @property
    def diagnosis_date(self) -> date | None:
        return self._diagnosis_date

    @property
    def onset_date(self) -> date | None:
        """Alias for diagnosis_date to satisfy ProblemProtocol."""
        return self._diagnosis_date

    @property
    def resolved_date(self) -> date | None:
        return self._resolved_date

    @property
    def discharge_disposition(self) -> str | None:
        return None

    @property
    def priority(self) -> int | None:
        return None

    @property
    def persistent_id(self):
        return None


def main():
    """Create and display a discharge diagnosis section."""
    # Create sample discharge diagnoses
    diagnoses = [
        DischargeDiagnosis(
            name="Acute Myocardial Infarction",
            code="57054005",
            code_system="SNOMED CT",
            status="active",
            diagnosis_date=date(2024, 10, 15),
        ),
        DischargeDiagnosis(
            name="Congestive Heart Failure",
            code="42343007",
            code_system="SNOMED CT",
            status="active",
            diagnosis_date=date(2024, 10, 15),
        ),
        DischargeDiagnosis(
            name="Acute Respiratory Failure",
            code="65710008",
            code_system="SNOMED CT",
            status="resolved",
            diagnosis_date=date(2024, 10, 14),
            resolved_date=date(2024, 10, 20),
        ),
    ]

    # Build the section
    section = DischargeDiagnosisSection(
        diagnoses=diagnoses,
        title="Hospital Discharge Diagnoses",
    )

    # Convert to XML and display
    xml_string = section.to_string(pretty=True)
    print("Discharge Diagnosis Section XML:")
    print("=" * 80)
    print(xml_string)
    print("=" * 80)

    # Display summary
    print(f"\nSummary:")
    print(f"- Total diagnoses: {len(diagnoses)}")
    print(f"- Active diagnoses: {sum(1 for d in diagnoses if d.status == 'active')}")
    print(
        f"- Resolved diagnoses: {sum(1 for d in diagnoses if d.status == 'resolved')}"
    )


if __name__ == "__main__":
    main()
