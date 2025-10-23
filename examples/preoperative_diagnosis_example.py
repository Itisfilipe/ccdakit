"""Example demonstrating Preoperative Diagnosis Section usage."""

from datetime import date

from ccdakit.builders.sections.preoperative_diagnosis import (
    PreoperativeDiagnosisSection,
)


class PreoperativeDiagnosis:
    """Example preoperative diagnosis implementation."""

    def __init__(
        self,
        name: str,
        code: str,
        code_system: str,
        diagnosis_date: date | None = None,
        status: str = "active",
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._diagnosis_date = diagnosis_date
        self._status = status

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
    def diagnosis_date(self) -> date | None:
        return self._diagnosis_date

    @property
    def status(self) -> str:
        return self._status

    @property
    def persistent_id(self):
        return None

    # ProblemProtocol compatibility
    @property
    def onset_date(self) -> date | None:
        return self._diagnosis_date

    @property
    def resolved_date(self) -> date | None:
        return None


def main():
    """Create and display a Preoperative Diagnosis Section example."""
    # Create example preoperative diagnoses
    diagnoses = [
        PreoperativeDiagnosis(
            name="Acute Appendicitis",
            code="74400008",
            code_system="SNOMED",
            diagnosis_date=date(2024, 3, 15),
            status="active",
        ),
        PreoperativeDiagnosis(
            name="Cholelithiasis",
            code="235919008",
            code_system="SNOMED",
            diagnosis_date=date(2024, 3, 10),
            status="active",
        ),
    ]

    # Build the section
    section = PreoperativeDiagnosisSection(
        diagnoses=diagnoses,
        title="Preoperative Diagnosis",
    )

    # Generate XML
    xml = section.to_string(pretty=True)
    print("Preoperative Diagnosis Section XML:")
    print("=" * 80)
    print(xml)
    print("=" * 80)


if __name__ == "__main__":
    main()
