"""Example of creating a Problems Section."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.problems import ProblemsSection
from ccdakit.core.base import CDAVersion


# Define persistent ID for problem tracking
class ExamplePersistentID:
    """Example persistent ID for problem tracking across documents."""

    def __init__(self, root, extension):
        self._root = root
        self._extension = extension

    @property
    def root(self):
        return self._root

    @property
    def extension(self):
        return self._extension


# Define problem data
class ExampleProblem:
    """Example problem data."""

    def __init__(
        self,
        name,
        code,
        code_system,
        status,
        onset_date,
        resolved_date=None,
        persistent_id=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._status = status
        self._onset_date = onset_date
        self._resolved_date = resolved_date
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
    def status(self):
        return self._status

    @property
    def onset_date(self):
        return self._onset_date

    @property
    def resolved_date(self):
        return self._resolved_date

    @property
    def persistent_id(self):
        return self._persistent_id


def main():
    """Create and display a Problems Section example."""

    # Create persistent ID for tracking
    hypertension_id = ExamplePersistentID(
        root="2.16.840.1.113883.19.5.99999.1",
        extension="PROB-HTN-001",
    )

    # Create sample problems
    problem1 = ExampleProblem(
        name="Essential Hypertension",
        code="59621000",
        code_system="SNOMED",
        status="active",
        onset_date=date(2018, 5, 10),
        persistent_id=hypertension_id,
    )

    problem2 = ExampleProblem(
        name="Type 2 Diabetes Mellitus",
        code="44054006",
        code_system="SNOMED",
        status="active",
        onset_date=date(2019, 3, 15),
    )

    problem3 = ExampleProblem(
        name="Pneumonia",
        code="233604007",
        code_system="SNOMED",
        status="resolved",
        onset_date=date(2023, 11, 5),
        resolved_date=date(2023, 12, 1),
    )

    # Create the Problems Section
    section = ProblemsSection(
        problems=[problem1, problem2, problem3],
        title="Patient Problem List",
        version=CDAVersion.R2_1,
    )

    # Generate XML
    elem = section.to_element()

    # Pretty print the XML
    xml_string = etree.tostring(elem, pretty_print=True, encoding="unicode", xml_declaration=False)

    print("Problems Section (C-CDA 2.1):")
    print("=" * 80)
    print(xml_string)

    # Show validation info
    print("\n" + "=" * 80)
    print("Summary:")
    print("  - Template ID: 2.16.840.1.113883.10.20.22.2.5.1")
    print("  - Extension: 2015-08-01")
    print("  - Number of problems: 3")
    print("  - Active problems: 2")
    print("  - Resolved problems: 1")
    print("\nProblems:")
    print("  1. Essential Hypertension (Active since 2018-05-10)")
    print("  2. Type 2 Diabetes Mellitus (Active since 2019-03-15)")
    print("  3. Pneumonia (Resolved 2023-12-01, onset 2023-11-05)")
    print("\nConformance:")
    print("  - CONF:1198-7936: Problems Section template ID present")
    print("  - CONF:1198-7938: Section code 11450-4 (Problem List)")
    print("  - CONF:1198-7940: Title present")
    print("  - CONF:1198-7942: Narrative text with table present")
    print("  - CONF:1198-15507: Problem Concern Act entries present")
    print("  - CONF:1198-9041: Each entry contains Problem Observation")


if __name__ == "__main__":
    main()
