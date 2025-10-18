"""Example: Creating a Past Medical History Section.

This example demonstrates how to build a C-CDA Past Medical History Section
that conforms to template 2.16.840.1.113883.10.20.22.2.20.
"""

from datetime import date

from ccdakit.builders.sections.past_medical_history import PastMedicalHistorySection
from ccdakit.core.base import CDAVersion


class SampleProblem:
    """Sample problem implementing ProblemProtocol."""

    def __init__(
        self,
        name,
        code,
        code_system,
        onset_date=None,
        resolved_date=None,
        status="active",
        persistent_id=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._onset_date = onset_date
        self._resolved_date = resolved_date
        self._status = status
        self._persistent_id = persistent_id

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
    def onset_date(self):
        return self._onset_date

    @property
    def resolved_date(self):
        return self._resolved_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


def main():
    """Create and display a Past Medical History section."""
    # Create sample past medical history problems
    problems = [
        SampleProblem(
            name="Essential hypertension",
            code="59621000",
            code_system="SNOMED CT",
            onset_date=date(2010, 3, 15),
            status="active",
        ),
        SampleProblem(
            name="Type 2 diabetes mellitus",
            code="44054006",
            code_system="SNOMED CT",
            onset_date=date(2012, 7, 20),
            status="active",
        ),
        SampleProblem(
            name="Appendicitis",
            code="74400008",
            code_system="SNOMED CT",
            onset_date=date(2005, 8, 10),
            resolved_date=date(2005, 8, 15),
            status="resolved",
        ),
        SampleProblem(
            name="Pneumonia",
            code="233604007",
            code_system="SNOMED CT",
            onset_date=date(2020, 1, 5),
            resolved_date=date(2020, 1, 20),
            status="resolved",
        ),
    ]

    # Create Past Medical History section (R2.1)
    section = PastMedicalHistorySection(
        problems=problems,
        title="Past Medical History",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    xml_string = section.to_string(pretty=True)
    print("Past Medical History Section (R2.1):")
    print("=" * 80)
    print(xml_string)
    print()

    # Create an empty Past Medical History section
    empty_section = PastMedicalHistorySection(
        problems=[],
        title="Past Medical History",
    )

    xml_empty = empty_section.to_string(pretty=True)
    print("Empty Past Medical History Section:")
    print("=" * 80)
    print(xml_empty)
    print()

    # Create R2.0 version
    section_r20 = PastMedicalHistorySection(
        problems=problems[:2],  # Just first two problems
        title="Past Medical History",
        version=CDAVersion.R2_0,
    )

    xml_r20 = section_r20.to_string(pretty=True)
    print("Past Medical History Section (R2.0):")
    print("=" * 80)
    print(xml_r20)


if __name__ == "__main__":
    main()
