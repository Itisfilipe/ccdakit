#!/usr/bin/env python3
"""
Example: Using Document Factories

This example demonstrates how to use the DocumentFactory to quickly create
common C-CDA document types with sensible defaults and appropriate template IDs.
"""

from datetime import date, datetime

from ccdakit.builders.sections.allergies import AllergiesSection
from ccdakit.builders.sections.medications import MedicationsSection
from ccdakit.builders.sections.problems import ProblemsSection
from ccdakit.core.base import CDAVersion
from ccdakit.utils.factories import DocumentFactory


# ============================================================================
# Step 1: Define data models (same as generate_ccda.py)
# ============================================================================


class Patient:
    """Patient data model that satisfies PatientProtocol."""

    def __init__(self):
        self.first_name = "Jane"
        self.middle_name = "A"
        self.last_name = "Smith"
        self.date_of_birth = date(1985, 3, 22)
        self.sex = "F"
        self.race = "2106-3"  # White
        self.ethnicity = "2186-5"  # Not Hispanic or Latino
        self.language = "eng"
        self.ssn = "987-65-4321"
        self.marital_status = "S"  # Single
        self.addresses = [Address()]
        self.telecoms = [Telecom("phone", "555-123-4567", "home")]


class Address:
    """Address data model."""

    def __init__(self):
        self.street_lines = ["456 Oak Avenue"]
        self.city = "Cambridge"
        self.state = "MA"
        self.postal_code = "02138"
        self.country = "US"


class Telecom:
    """Telecom data model."""

    def __init__(self, type_, value, use=None):
        self.type = type_
        self.value = value
        self.use = use


class Organization:
    """Organization data model."""

    def __init__(self):
        self.name = "University Hospital"
        self.npi = "9876543210"
        self.tin = None
        self.oid_root = "2.16.840.1.113883.3.UNIV"
        self.addresses = [Address()]
        self.telecoms = [Telecom("phone", "555-999-8888", "work")]


class Author:
    """Author/Provider data model."""

    def __init__(self):
        self.first_name = "Robert"
        self.middle_name = "J"
        self.last_name = "Johnson"
        self.npi = "1122334455"
        self.time = datetime.now()
        self.addresses = [Address()]
        self.telecoms = [Telecom("phone", "555-777-6666", "work")]
        self.organization = Organization()


class Problem:
    """Problem data model."""

    def __init__(self, name, code, code_system, status, onset_date, resolved_date=None):
        self.name = name
        self.code = code
        self.code_system = code_system
        self.status = status
        self.onset_date = onset_date
        self.resolved_date = resolved_date
        self.persistent_id = None


class Medication:
    """Medication data model."""

    def __init__(
        self,
        name,
        code,
        dosage,
        route,
        frequency,
        start_date,
        end_date=None,
        status="active",
        instructions=None,
    ):
        self.name = name
        self.code = code
        self.dosage = dosage
        self.route = route
        self.frequency = frequency
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.instructions = instructions


class Allergy:
    """Allergy data model."""

    def __init__(
        self,
        allergen,
        code,
        code_system,
        reaction,
        severity,
        allergy_type="allergy",
        status="active",
        onset_date=None,
    ):
        self.allergen = allergen
        self.allergen_code = code
        self.allergen_code_system = code_system
        self.allergy_type = allergy_type
        self.reaction = reaction
        self.severity = severity
        self.status = status
        self.onset_date = onset_date


# ============================================================================
# Step 2: Example 1 - Create a Continuity of Care Document (CCD)
# ============================================================================


def example_1_continuity_of_care_document():
    """
    Example 1: Create a Continuity of Care Document (CCD).

    The CCD is the most commonly used C-CDA document type. It provides
    a comprehensive snapshot of a patient's health status.
    """
    print("\n" + "=" * 70)
    print("Example 1: Continuity of Care Document (CCD)")
    print("=" * 70)

    # Create patient data
    patient = Patient()
    author = Author()
    custodian = Organization()

    # Create clinical data
    problems = [
        Problem(
            name="Asthma",
            code="195967001",
            code_system="SNOMED",
            status="active",
            onset_date=date(2015, 6, 10),
        ),
        Problem(
            name="Seasonal Allergic Rhinitis",
            code="367498001",
            code_system="SNOMED",
            status="active",
            onset_date=date(2010, 4, 15),
        ),
    ]

    medications = [
        Medication(
            name="Albuterol 90 mcg/actuation inhaler",
            code="745752",
            dosage="90 mcg",
            route="inhalation",
            frequency="as needed",
            start_date=date(2015, 7, 1),
            status="active",
            instructions="Use for asthma symptoms",
        ),
    ]

    # Create sections
    problems_section = ProblemsSection(problems=problems, version=CDAVersion.R2_1)
    medications_section = MedicationsSection(medications=medications, version=CDAVersion.R2_1)

    # Use DocumentFactory to create CCD
    ccd = DocumentFactory.create_continuity_of_care_document(
        patient=patient,
        author=author,
        custodian=custodian,
        sections=[problems_section, medications_section],
        version=CDAVersion.R2_1,
    )

    # Generate XML
    xml_string = ccd.to_xml_string(pretty=True)

    print(f"\nPatient: {patient.first_name} {patient.last_name}")
    print("Document Type: Continuity of Care Document")
    print("Template ID: 2.16.840.1.113883.10.20.22.1.2 (CCD R2.1)")
    print("Document Code: 34133-9 (LOINC)")
    print(f"Document Size: {len(xml_string):,} bytes")
    print(f"Sections: {len(ccd.sections)}")

    # Save to file
    output_file = "ccd_example.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_string)

    print(f"\nSaved to: {output_file}")

    return xml_string


# ============================================================================
# Step 3: Example 2 - Create a Discharge Summary
# ============================================================================


def example_2_discharge_summary():
    """
    Example 2: Create a Discharge Summary.

    The Discharge Summary documents the course of a patient's hospital stay,
    created at the time of discharge.
    """
    print("\n" + "=" * 70)
    print("Example 2: Discharge Summary")
    print("=" * 70)

    # Create patient data
    patient = Patient()
    author = Author()
    custodian = Organization()

    # Discharge medications
    discharge_meds = [
        Medication(
            name="Lisinopril 10mg oral tablet",
            code="314076",
            dosage="10 mg",
            route="oral",
            frequency="once daily",
            start_date=datetime.now().date(),
            status="active",
            instructions="Take in the morning for blood pressure",
        ),
        Medication(
            name="Aspirin 81mg oral tablet",
            code="243670",
            dosage="81 mg",
            route="oral",
            frequency="once daily",
            start_date=datetime.now().date(),
            status="active",
            instructions="Take with food",
        ),
    ]

    # Create sections
    medications_section = MedicationsSection(
        medications=discharge_meds,
        title="Discharge Medications",
        version=CDAVersion.R2_1,
    )

    # Use DocumentFactory to create Discharge Summary
    discharge_summary = DocumentFactory.create_discharge_summary(
        patient=patient,
        author=author,
        custodian=custodian,
        sections=[medications_section],
        version=CDAVersion.R2_1,
    )

    # Generate XML
    xml_string = discharge_summary.to_xml_string(pretty=True)

    print(f"\nPatient: {patient.first_name} {patient.last_name}")
    print("Document Type: Discharge Summary")
    print("Template ID: 2.16.840.1.113883.10.20.22.1.8 (Discharge Summary R2.1)")
    print("Document Code: 18842-5 (LOINC)")
    print(f"Document Size: {len(xml_string):,} bytes")
    print(f"Discharge Medications: {len(discharge_meds)}")

    # Save to file
    output_file = "discharge_summary_example.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_string)

    print(f"\nSaved to: {output_file}")

    return xml_string


# ============================================================================
# Step 4: Example 3 - Create a Progress Note
# ============================================================================


def example_3_progress_note():
    """
    Example 3: Create a Progress Note.

    The Progress Note documents a patient's clinical status during
    hospitalization or ongoing care.
    """
    print("\n" + "=" * 70)
    print("Example 3: Progress Note")
    print("=" * 70)

    # Create patient data
    patient = Patient()
    author = Author()
    custodian = Organization()

    # Current problems
    problems = [
        Problem(
            name="Pneumonia",
            code="233604007",
            code_system="SNOMED",
            status="active",
            onset_date=date(2023, 10, 10),
        ),
    ]

    # Create sections
    problems_section = ProblemsSection(
        problems=problems, title="Assessment", version=CDAVersion.R2_1
    )

    # Use DocumentFactory to create Progress Note
    progress_note = DocumentFactory.create_progress_note(
        patient=patient,
        author=author,
        custodian=custodian,
        sections=[problems_section],
        version=CDAVersion.R2_1,
    )

    # Generate XML
    xml_string = progress_note.to_xml_string(pretty=True)

    print(f"\nPatient: {patient.first_name} {patient.last_name}")
    print("Document Type: Progress Note")
    print("Template ID: 2.16.840.1.113883.10.20.22.1.9 (Progress Note R2.1)")
    print("Document Code: 11506-3 (LOINC)")
    print(f"Document Size: {len(xml_string):,} bytes")

    # Save to file
    output_file = "progress_note_example.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_string)

    print(f"\nSaved to: {output_file}")

    return xml_string


# ============================================================================
# Step 5: Example 4 - Create a Consultation Note
# ============================================================================


def example_4_consultation_note():
    """
    Example 4: Create a Consultation Note.

    The Consultation Note documents the opinion of a consulting provider
    regarding a patient's condition.
    """
    print("\n" + "=" * 70)
    print("Example 4: Consultation Note")
    print("=" * 70)

    # Create patient data
    patient = Patient()
    author = Author()  # Consulting provider
    custodian = Organization()

    # Consultation findings
    problems = [
        Problem(
            name="Suspected Celiac Disease",
            code="396331005",
            code_system="SNOMED",
            status="active",
            onset_date=date(2023, 9, 1),
        ),
    ]

    allergies = [
        Allergy(
            allergen="Gluten",
            code="111088007",
            code_system="SNOMED",
            reaction="Abdominal pain",
            severity="moderate",
            status="active",
        ),
    ]

    # Create sections
    problems_section = ProblemsSection(
        problems=problems, title="Consultation Findings", version=CDAVersion.R2_1
    )
    allergies_section = AllergiesSection(
        allergies=allergies, title="Allergies and Intolerances", version=CDAVersion.R2_1
    )

    # Use DocumentFactory to create Consultation Note
    consultation = DocumentFactory.create_consultation_note(
        patient=patient,
        author=author,
        custodian=custodian,
        sections=[problems_section, allergies_section],
        version=CDAVersion.R2_1,
    )

    # Generate XML
    xml_string = consultation.to_xml_string(pretty=True)

    print(f"\nPatient: {patient.first_name} {patient.last_name}")
    print(f"Consulting Provider: Dr. {author.first_name} {author.last_name}")
    print("Document Type: Consultation Note")
    print("Template ID: 2.16.840.1.113883.10.20.22.1.4 (Consultation Note R2.1)")
    print("Document Code: 11488-4 (LOINC)")
    print(f"Document Size: {len(xml_string):,} bytes")

    # Save to file
    output_file = "consultation_note_example.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_string)

    print(f"\nSaved to: {output_file}")

    return xml_string


# ============================================================================
# Step 6: Example 5 - Comparing Versions
# ============================================================================


def example_5_version_comparison():
    """
    Example 5: Compare R2.1 and R2.0 versions.

    Shows how to create documents with different C-CDA versions.
    """
    print("\n" + "=" * 70)
    print("Example 5: Version Comparison (R2.1 vs R2.0)")
    print("=" * 70)

    # Create patient data
    patient = Patient()
    author = Author()
    custodian = Organization()

    # Create CCD with R2.1
    ccd_r21 = DocumentFactory.create_continuity_of_care_document(
        patient=patient,
        author=author,
        custodian=custodian,
        version=CDAVersion.R2_1,
    )

    # Create CCD with R2.0
    ccd_r20 = DocumentFactory.create_continuity_of_care_document(
        patient=patient,
        author=author,
        custodian=custodian,
        version=CDAVersion.R2_0,
    )

    # Generate XML for both
    xml_r21 = ccd_r21.to_xml_string(pretty=True)
    xml_r20 = ccd_r20.to_xml_string(pretty=True)

    print("\nR2.1 Document:")
    print("  - Template Extension: 2015-08-01")
    print(f"  - Size: {len(xml_r21):,} bytes")

    print("\nR2.0 Document:")
    print("  - Template Extension: 2014-06-09")
    print(f"  - Size: {len(xml_r20):,} bytes")

    print("\nBoth versions use the same:")
    print("  - Template Root: 2.16.840.1.113883.10.20.22.1.2 (CCD)")
    print("  - Document Code: 34133-9 (LOINC)")

    return xml_r21, xml_r20


# ============================================================================
# Main execution
# ============================================================================


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("pyccda DocumentFactory Examples")
    print("=" * 70)
    print("\nThis example demonstrates how to use the DocumentFactory to create")
    print("common C-CDA document types with appropriate template IDs and codes.")

    # Run all examples
    example_1_continuity_of_care_document()
    example_2_discharge_summary()
    example_3_progress_note()
    example_4_consultation_note()
    example_5_version_comparison()

    print("\n" + "=" * 70)
    print("Examples Complete!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  1. ccd_example.xml - Continuity of Care Document")
    print("  2. discharge_summary_example.xml - Discharge Summary")
    print("  3. progress_note_example.xml - Progress Note")
    print("  4. consultation_note_example.xml - Consultation Note")
    print("\nKey benefits of using DocumentFactory:")
    print("  - Automatic template IDs for each document type")
    print("  - Correct LOINC document type codes")
    print("  - Sensible defaults (titles, effective time, etc.)")
    print("  - Version support (R2.1 and R2.0)")
    print("  - Consistent document structure")
    print("\nNext steps:")
    print("  - Validate documents with ONC C-CDA Validator")
    print("  - Add more clinical sections as needed")
    print("  - Customize titles and metadata")
    print()
