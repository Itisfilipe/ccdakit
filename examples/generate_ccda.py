#!/usr/bin/env python3
"""
Example: Generate a Complete C-CDA Document

This example demonstrates how to use pyccda to generate a complete,
ONC-compliant C-CDA R2.1 document with patient demographics, problems, and medications.
"""

from datetime import date, datetime

from ccdakit.builders.document import ClinicalDocument
from ccdakit.builders.sections.immunizations import ImmunizationsSection
from ccdakit.builders.sections.medications import MedicationsSection
from ccdakit.builders.sections.problems import ProblemsSection
from ccdakit.builders.sections.vital_signs import VitalSignsSection
from ccdakit.core.base import CDAVersion


# ============================================================================
# Step 1: Create data models that satisfy the protocols
# ============================================================================


class Patient:
    """Patient data model that satisfies PatientProtocol."""

    def __init__(self):
        self.first_name = "John"
        self.middle_name = "Q"
        self.last_name = "Doe"
        self.date_of_birth = date(1970, 5, 15)
        self.sex = "M"
        self.race = "2106-3"  # White (CDC Race Code)
        self.ethnicity = "2186-5"  # Not Hispanic or Latino
        self.language = "eng"
        self.ssn = "123-45-6789"
        self.marital_status = "M"  # Married
        self.addresses = [Address()]
        self.telecoms = [Telecom("phone", "617-555-1234", "home")]


class Address:
    """Address data model that satisfies AddressProtocol."""

    def __init__(self):
        self.street_lines = ["123 Main Street", "Apartment 4B"]
        self.city = "Boston"
        self.state = "MA"
        self.postal_code = "02101"
        self.country = "US"


class Telecom:
    """Telecom data model that satisfies TelecomProtocol."""

    def __init__(self, type_, value, use=None):
        self.type = type_
        self.value = value
        self.use = use


class Organization:
    """Organization data model that satisfies OrganizationProtocol."""

    def __init__(self):
        self.name = "Community Health Center"
        self.npi = "1234567890"
        self.tin = None
        self.oid_root = "2.16.840.1.113883.3.EXAMPLE"
        self.addresses = [Address()]
        self.telecoms = [Telecom("phone", "617-555-9999", "work")]


class Author:
    """Author/Provider data model that satisfies AuthorProtocol."""

    def __init__(self):
        self.first_name = "Alice"
        self.middle_name = "M"
        self.last_name = "Smith"
        self.npi = "9876543210"
        self.time = datetime.now()
        self.addresses = [Address()]
        self.telecoms = [Telecom("phone", "617-555-5555", "work")]
        self.organization = Organization()


class Problem:
    """Problem data model that satisfies ProblemProtocol."""

    def __init__(self, name, code, code_system, status, onset_date, resolved_date=None):
        self.name = name
        self.code = code
        self.code_system = code_system
        self.status = status
        self.onset_date = onset_date
        self.resolved_date = resolved_date
        self.persistent_id = None  # Could add persistent tracking


class Medication:
    """Medication data model that satisfies MedicationProtocol."""

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


class Immunization:
    """Immunization data model that satisfies ImmunizationProtocol."""

    def __init__(
        self,
        vaccine_name,
        cvx_code,
        administration_date,
        status="completed",
        lot_number=None,
        manufacturer=None,
        route=None,
        site=None,
        dose_quantity=None,
    ):
        self.vaccine_name = vaccine_name
        self.cvx_code = cvx_code
        self.administration_date = administration_date
        self.status = status
        self.lot_number = lot_number
        self.manufacturer = manufacturer
        self.route = route
        self.site = site
        self.dose_quantity = dose_quantity


class VitalSign:
    """Vital sign data model that satisfies VitalSignProtocol."""

    def __init__(self, type, code, value, unit, date, interpretation=None):
        self.type = type
        self.code = code
        self.value = value
        self.unit = unit
        self.date = date
        self.interpretation = interpretation


class VitalSignsOrganizer:
    """Vital signs organizer that satisfies VitalSignsOrganizerProtocol."""

    def __init__(self, date, vital_signs):
        self.date = date
        self.vital_signs = vital_signs


# ============================================================================
# Step 2: Create clinical data
# ============================================================================


def create_patient_data():
    """Create patient demographic data."""
    return Patient()


def create_provider_data():
    """Create provider/author data."""
    return Author()


def create_organization_data():
    """Create organization/custodian data."""
    return Organization()


def create_problems_data():
    """Create patient problems list."""
    return [
        Problem(
            name="Essential Hypertension",
            code="59621000",
            code_system="SNOMED",
            status="active",
            onset_date=date(2018, 5, 10),
        ),
        Problem(
            name="Type 2 Diabetes Mellitus",
            code="44054006",
            code_system="SNOMED",
            status="active",
            onset_date=date(2019, 3, 15),
        ),
        Problem(
            name="Acute Bronchitis",
            code="10509002",
            code_system="SNOMED",
            status="resolved",
            onset_date=date(2023, 1, 5),
            resolved_date=date(2023, 2, 1),
        ),
    ]


def create_medications_data():
    """Create patient medications list."""
    return [
        Medication(
            name="Lisinopril 10mg oral tablet",
            code="314076",  # RxNorm code
            dosage="10 mg",
            route="oral",
            frequency="once daily",
            start_date=date(2018, 6, 1),
            status="active",
            instructions="Take in the morning",
        ),
        Medication(
            name="Metformin 500mg oral tablet",
            code="860975",  # RxNorm code
            dosage="500 mg",
            route="oral",
            frequency="twice daily",
            start_date=date(2019, 4, 1),
            status="active",
            instructions="Take with meals",
        ),
        Medication(
            name="Amoxicillin 500mg oral capsule",
            code="308191",  # RxNorm code
            dosage="500 mg",
            route="oral",
            frequency="three times daily",
            start_date=date(2023, 1, 10),
            end_date=date(2023, 1, 24),
            status="completed",
            instructions="Complete full course",
        ),
    ]


def create_immunizations_data():
    """Create patient immunizations list."""
    return [
        Immunization(
            vaccine_name="Influenza vaccine, seasonal",
            cvx_code="141",  # CVX code for seasonal flu
            administration_date=date(2023, 9, 15),
            status="completed",
            lot_number="ABC123456",
            manufacturer="Sanofi Pasteur",
            route="intramuscular",
            site="left deltoid",
            dose_quantity="0.5 mL",
        ),
        Immunization(
            vaccine_name="COVID-19 vaccine, mRNA",
            cvx_code="208",  # CVX code for Pfizer COVID-19
            administration_date=date(2023, 6, 1),
            status="completed",
            lot_number="XYZ789012",
            manufacturer="Pfizer Inc.",
            route="intramuscular",
            site="left deltoid",
            dose_quantity="0.3 mL",
        ),
        Immunization(
            vaccine_name="Tetanus and diphtheria toxoids",
            cvx_code="139",  # CVX code for Td
            administration_date=date(2021, 3, 10),
            status="completed",
            manufacturer="GSK",
            route="intramuscular",
            site="right deltoid",
        ),
    ]


def create_vital_signs_data():
    """Create patient vital signs data."""
    # Most recent vital signs
    return [
        VitalSignsOrganizer(
            date=datetime(2023, 10, 15, 10, 30),
            vital_signs=[
                VitalSign(
                    type="Heart Rate",
                    code="8867-4",  # LOINC code
                    value="72",
                    unit="bpm",
                    date=datetime(2023, 10, 15, 10, 30),
                    interpretation="Normal",
                ),
                VitalSign(
                    type="Systolic Blood Pressure",
                    code="8480-6",  # LOINC code
                    value="120",
                    unit="mm[Hg]",
                    date=datetime(2023, 10, 15, 10, 30),
                    interpretation="Normal",
                ),
                VitalSign(
                    type="Diastolic Blood Pressure",
                    code="8462-4",  # LOINC code
                    value="80",
                    unit="mm[Hg]",
                    date=datetime(2023, 10, 15, 10, 30),
                    interpretation="Normal",
                ),
                VitalSign(
                    type="Body Temperature",
                    code="8310-5",  # LOINC code
                    value="98.6",
                    unit="degF",
                    date=datetime(2023, 10, 15, 10, 30),
                    interpretation="Normal",
                ),
                VitalSign(
                    type="Respiratory Rate",
                    code="9279-1",  # LOINC code
                    value="16",
                    unit="/min",
                    date=datetime(2023, 10, 15, 10, 30),
                    interpretation="Normal",
                ),
            ],
        ),
    ]


# ============================================================================
# Step 3: Generate C-CDA document
# ============================================================================


def generate_ccda_document():
    """Generate a complete C-CDA R2.1 document."""

    print("Generating C-CDA R2.1 Document...")
    print("=" * 70)

    # Create data
    patient = create_patient_data()
    author = create_provider_data()
    custodian = create_organization_data()
    problems = create_problems_data()

    print(f"\nPatient: {patient.first_name} {patient.last_name}")
    print(f"DOB: {patient.date_of_birth}")
    print(f"Provider: Dr. {author.first_name} {author.last_name}")
    print(f"Facility: {custodian.name}")
    print(f"Problems: {len(problems)} documented")

    # Create document
    doc = ClinicalDocument(
        patient=patient,
        author=author,
        custodian=custodian,
        title="Patient Clinical Summary",
        document_id=f"DOC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        effective_time=datetime.now(),
        version=CDAVersion.R2_1,
    )

    # Generate XML
    xml_string = doc.to_xml_string(pretty=True)

    print("\n" + "=" * 70)
    print("Document Generated Successfully!")
    print("=" * 70)
    print(f"\nDocument Size: {len(xml_string):,} bytes")
    print("CDA Version: R2.1 (2015-08-01)")

    # Show snippet
    print("\nDocument Preview (first 1000 characters):")
    print("-" * 70)
    print(xml_string[:1000])
    print("...")
    print("-" * 70)

    # Save to file
    output_file = "output_ccda.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_string)

    print(f"\nDocument saved to: {output_file}")

    return xml_string


def generate_ccda_with_sections():
    """Generate complete C-CDA document with all clinical sections."""

    print("\nGenerating Complete C-CDA with All Sections...")
    print("=" * 70)

    # Create data
    patient = create_patient_data()
    author = create_provider_data()
    custodian = create_organization_data()
    problems = create_problems_data()
    medications = create_medications_data()
    immunizations = create_immunizations_data()
    vital_signs_organizers = create_vital_signs_data()

    print(f"\nPatient: {patient.first_name} {patient.last_name}")
    print(f"Problems: {len(problems)} documented")
    print(f"Medications: {len(medications)} documented")
    print(f"Immunizations: {len(immunizations)} documented")
    print(
        f"Vital Signs: {sum(len(org.vital_signs) for org in vital_signs_organizers)} measurements"
    )

    # Create problems section
    problems_section = ProblemsSection(
        problems=problems,
        title="Problem List",
        version=CDAVersion.R2_1,
    )

    # Create medications section
    medications_section = MedicationsSection(
        medications=medications,
        title="Medications",
        version=CDAVersion.R2_1,
    )

    # Create immunizations section
    immunizations_section = ImmunizationsSection(
        immunizations=immunizations,
        title="Immunization History",
        version=CDAVersion.R2_1,
    )

    # Create vital signs section
    vital_signs_section = VitalSignsSection(
        vital_signs_organizers=vital_signs_organizers,
        title="Vital Signs",
        version=CDAVersion.R2_1,
    )

    # Create complete document with all sections
    doc = ClinicalDocument(
        patient=patient,
        author=author,
        custodian=custodian,
        sections=[
            problems_section,
            medications_section,
            immunizations_section,
            vital_signs_section,
        ],
        title="Patient Clinical Summary - Complete",
        document_id=f"DOC-COMPLETE-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        effective_time=datetime.now(),
        version=CDAVersion.R2_1,
    )

    # Generate complete XML
    complete_xml = doc.to_xml_string(pretty=True)

    print("\n" + "=" * 70)
    print("Complete Document with All Sections Generated!")
    print("=" * 70)
    print(f"\nDocument Size: {len(complete_xml):,} bytes")
    print("CDA Version: R2.1 (2015-08-01)")
    print("Sections: 4 (Problems, Medications, Immunizations, Vital Signs)")

    # Show document preview
    print("\nComplete Document Preview (first 1200 characters):")
    print("-" * 70)
    print(complete_xml[:1200])
    print("...")
    print("-" * 70)

    # Save complete document
    complete_file = "output_ccda_with_sections.xml"
    with open(complete_file, "w", encoding="utf-8") as f:
        f.write(complete_xml)

    print(f"\nComplete document saved to: {complete_file}")
    print("\nDocument Structure:")
    print("  ✓ Patient demographics (recordTarget)")
    print("  ✓ Provider information (author)")
    print("  ✓ Facility details (custodian)")
    print("  ✓ Problems Section")
    print(f"    - {len(problems)} problems with narrative table")
    print("  ✓ Medications Section")
    print(f"    - {len(medications)} medications with narrative table")
    print("  ✓ Immunizations Section")
    print(f"    - {len(immunizations)} immunizations with narrative table")
    print("  ✓ Vital Signs Section")
    print(
        f"    - {sum(len(org.vital_signs) for org in vital_signs_organizers)} vital sign measurements with narrative table"
    )

    return complete_xml


# ============================================================================
# Main execution
# ============================================================================


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("pyccda Example: Complete C-CDA Document Generation")
    print("=" * 70)

    # Generate basic document (header only)
    doc_xml = generate_ccda_document()

    # Generate complete document with sections
    complete_xml = generate_ccda_with_sections()

    print("\n" + "=" * 70)
    print("Example Complete!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - output_ccda.xml (basic document - header only)")
    print("  - output_ccda_with_sections.xml (complete document with all sections)")
    print("\nFeatures demonstrated:")
    print("  ✓ Patient demographics and identifiers")
    print("  ✓ Provider/author information")
    print("  ✓ Organization/custodian details")
    print("  ✓ Problems section with narrative table")
    print("  ✓ Medications section with narrative table")
    print("  ✓ Immunizations section with narrative table")
    print("  ✓ Vital Signs section with narrative table")
    print("  ✓ Automatic section wrapping in structuredBody")
    print("  ✓ C-CDA R2.1 compliance")
    print("\nNext steps:")
    print("  - Validate with ONC C-CDA Validator")
    print("  - Review narrative rendering")
    print("  - Add more clinical sections (procedures, results, etc.)")
    print()
