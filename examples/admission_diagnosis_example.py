#!/usr/bin/env python3
"""Example demonstrating the Admission Diagnosis Section builder.

This example shows how to create a C-CDA Admission Diagnosis Section
with multiple diagnoses identified at hospital admission.
"""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.admission_diagnosis import AdmissionDiagnosisSection


# Example admission diagnosis class
class AdmissionDiagnosis:
    """Example implementation of AdmissionDiagnosisProtocol."""

    def __init__(
        self,
        name,
        code,
        code_system,
        admission_date=None,
        diagnosis_date=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._admission_date = admission_date
        self._diagnosis_date = diagnosis_date

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def admission_date(self):
        return self._admission_date

    @property
    def diagnosis_date(self):
        return self._diagnosis_date

    @property
    def persistent_id(self):
        return None

    # Required properties from ProblemProtocol
    @property
    def status(self):
        return "active"

    @property
    def onset_date(self):
        return self._diagnosis_date

    @property
    def resolved_date(self):
        return None


def main():
    """Create and display an Admission Diagnosis Section."""
    # Create sample admission diagnoses
    diagnoses = [
        AdmissionDiagnosis(
            name="Acute ST-elevation myocardial infarction",
            code="57054005",
            code_system="SNOMED",
            admission_date=date(2024, 1, 15),
            diagnosis_date=date(2024, 1, 15),
        ),
        AdmissionDiagnosis(
            name="Congestive heart failure",
            code="84114007",
            code_system="SNOMED",
            admission_date=date(2024, 1, 15),
            diagnosis_date=date(2024, 1, 15),
        ),
        AdmissionDiagnosis(
            name="Type 2 diabetes mellitus",
            code="44054006",
            code_system="SNOMED",
            admission_date=date(2024, 1, 15),
            diagnosis_date=date(2024, 1, 15),
        ),
    ]

    # Build the section
    section = AdmissionDiagnosisSection(
        diagnoses=diagnoses,
        title="Hospital Admission Diagnoses",
    )

    # Generate XML
    xml_element = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(
        xml_element,
        pretty_print=True,
        encoding="unicode",
    )

    print("Admission Diagnosis Section (V3) Example")
    print("=" * 80)
    print(xml_string)


if __name__ == "__main__":
    main()
