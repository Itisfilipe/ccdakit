#!/usr/bin/env python3
"""
Example: Using Fluent API Builders for C-CDA Data

This example demonstrates the simplified fluent API builders that make
creating C-CDA data models easier and more intuitive.
"""

from datetime import date, datetime

from ccdakit.builders.document import ClinicalDocument
from ccdakit.builders.sections.allergies import AllergiesSection
from ccdakit.builders.sections.encounters import EncountersSection
from ccdakit.builders.sections.immunizations import ImmunizationsSection
from ccdakit.builders.sections.medications import MedicationsSection
from ccdakit.builders.sections.problems import ProblemsSection
from ccdakit.builders.sections.procedures import ProceduresSection
from ccdakit.builders.sections.results import ResultsSection
from ccdakit.builders.sections.social_history import SocialHistorySection
from ccdakit.builders.sections.vital_signs import VitalSignsSection
from ccdakit.core.base import CDAVersion
from ccdakit.utils.builders import (
    SimpleAllergyBuilder,
    SimpleEncounterBuilder,
    SimpleImmunizationBuilder,
    SimpleMedicationBuilder,
    SimplePatientBuilder,
    SimpleProblemBuilder,
    SimpleProcedureBuilder,
    SimpleResultObservationBuilder,
    SimpleResultOrganizerBuilder,
    SimpleSmokingStatusBuilder,
    SimpleVitalSignBuilder,
    SimpleVitalSignsOrganizerBuilder,
)


# ============================================================================
# Helper class to convert dict data to protocol-satisfying objects
# ============================================================================


class DictWrapper:
    """Wrapper to make dict data satisfy protocols via property access.

    This class wraps dictionary data and provides attribute access to satisfy
    protocol requirements. Since protocols use @property decorators, we need
    to implement __getattr__ to provide dynamic property access.
    """

    def __init__(self, data):
        """Initialize wrapper with data dictionary.

        Args:
            data: Dictionary containing the data to wrap
        """
        # Store data in a private attribute to avoid conflicts
        object.__setattr__(self, "_data", {})

        # Convert nested dicts and lists to DictWrapper instances
        for key, value in data.items():
            if isinstance(value, dict):
                self._data[key] = DictWrapper(value)
            elif isinstance(value, list):
                self._data[key] = [
                    DictWrapper(item) if isinstance(item, dict) else item for item in value
                ]
            else:
                self._data[key] = value

    def __getattr__(self, name):
        """Provide attribute access to wrapped data.

        This makes the wrapper satisfy protocol requirements that use @property.
        For missing attributes, returns None to support optional protocol fields.

        Args:
            name: Attribute name to access

        Returns:
            Value from wrapped data, or None if not present
        """
        if name.startswith("_"):
            # Avoid infinite recursion for private attributes
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        # Return None for missing attributes to support optional protocol fields
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        """Set attribute in wrapped data.

        Args:
            name: Attribute name
            value: Value to set
        """
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            self._data[name] = value

    def __getitem__(self, key):
        """Provide dictionary-style access to wrapped data.

        Args:
            key: Key to access

        Returns:
            Value from wrapped data

        Raises:
            KeyError: If key doesn't exist in wrapped data
        """
        return self._data[key]

    def __setitem__(self, key, value):
        """Set item using dictionary-style access.

        Args:
            key: Key to set
            value: Value to set
        """
        self._data[key] = value

    def __contains__(self, key):
        """Check if key exists in wrapped data.

        Args:
            key: Key to check

        Returns:
            True if key exists, False otherwise
        """
        return key in self._data

    def __repr__(self):
        """Return string representation."""
        return f"DictWrapper({self._data!r})"


# ============================================================================
# Build Patient Data with Fluent API
# ============================================================================


def create_patient_with_builder():
    """Create patient using fluent builder API."""
    print("Creating patient with fluent builder API...")

    patient_data = (
        SimplePatientBuilder()
        .name("Sarah", "Johnson", "Marie")
        .birth_date(date(1985, 7, 12))
        .gender("F")
        .race("2106-3")  # White (CDC Race Code)
        .ethnicity("2186-5")  # Not Hispanic or Latino
        .language("eng")  # English
        .ssn("987-65-4321")
        .marital_status("M")  # Married
        .address("456 Oak Avenue", "Cambridge", "MA", "02139", "US", "Unit 3C")
        .address("789 Pine Street", "Boston", "MA", "02101")  # Secondary address
        .phone("617-555-7890", "home")
        .phone("617-555-1111", "work")
        .phone("617-555-2222", "mobile")
        .email("sarah.johnson@email.com", "home")
        .build()
    )

    print(
        f"  Name: {patient_data['first_name']} {patient_data['middle_name']} {patient_data['last_name']}"
    )
    print(f"  DOB: {patient_data['date_of_birth']}")
    print(f"  Addresses: {len(patient_data['addresses'])}")
    print(f"  Contact methods: {len(patient_data['telecoms'])}")

    return DictWrapper(patient_data)


# ============================================================================
# Build Clinical Data with Fluent API
# ============================================================================


def create_problems_with_builder():
    """Create problem list using fluent builder API."""
    print("\nCreating problems with fluent builder API...")

    problems_data = [
        (
            SimpleProblemBuilder()
            .name("Essential Hypertension")
            .code("59621000", "SNOMED")
            .status("active")
            .onset_date(date(2018, 5, 10))
            .persistent_id("2.16.840.1.113883.3.EXAMPLE", "PROB-001")
            .build()
        ),
        (
            SimpleProblemBuilder()
            .name("Type 2 Diabetes Mellitus")
            .code("44054006", "SNOMED")
            .status("active")
            .onset_date(date(2019, 3, 15))
            .persistent_id("2.16.840.1.113883.3.EXAMPLE", "PROB-002")
            .build()
        ),
        (
            SimpleProblemBuilder()
            .name("Seasonal Allergic Rhinitis")
            .code("367498001", "SNOMED")
            .status("active")
            .onset_date(date(2015, 4, 20))
            .build()
        ),
    ]

    print(f"  Total problems: {len(problems_data)}")
    return [DictWrapper(p) for p in problems_data]


def create_medications_with_builder():
    """Create medication list using fluent builder API."""
    print("\nCreating medications with fluent builder API...")

    medications_data = [
        (
            SimpleMedicationBuilder()
            .name("Lisinopril 10mg oral tablet")
            .code("314076")  # RxNorm
            .dosage("10 mg")
            .route("oral")
            .frequency("once daily")
            .start_date(date(2018, 6, 1))
            .status("active")
            .instructions("Take in the morning with water")
            .build()
        ),
        (
            SimpleMedicationBuilder()
            .name("Metformin 500mg oral tablet")
            .code("860975")  # RxNorm
            .dosage("500 mg")
            .route("oral")
            .frequency("twice daily")
            .start_date(date(2019, 4, 1))
            .status("active")
            .instructions("Take with meals to reduce GI side effects")
            .build()
        ),
        (
            SimpleMedicationBuilder()
            .name("Atorvastatin 20mg oral tablet")
            .code("617318")  # RxNorm
            .dosage("20 mg")
            .route("oral")
            .frequency("once daily")
            .start_date(date(2020, 2, 15))
            .status("active")
            .instructions("Take at bedtime")
            .build()
        ),
    ]

    print(f"  Total medications: {len(medications_data)}")
    return [DictWrapper(m) for m in medications_data]


def create_allergies_with_builder():
    """Create allergy list using fluent builder API."""
    print("\nCreating allergies with fluent builder API...")

    allergies_data = [
        (
            SimpleAllergyBuilder()
            .allergen("Penicillin G")
            .allergen_code("7980", "RxNorm")
            .allergy_type("allergy")
            .reaction("Hives and itching")
            .severity("moderate")
            .status("active")
            .onset_date(date(1995, 8, 15))
            .build()
        ),
        (
            SimpleAllergyBuilder()
            .allergen("Shellfish")
            .allergy_type("allergy")
            .reaction("Anaphylaxis")
            .severity("severe")
            .status("active")
            .onset_date(date(2005, 6, 20))
            .build()
        ),
        (
            SimpleAllergyBuilder()
            .allergen("Latex")
            .allergy_type("allergy")
            .reaction("Contact dermatitis")
            .severity("mild")
            .status("active")
            .onset_date(date(2010, 3, 10))
            .build()
        ),
    ]

    print(f"  Total allergies: {len(allergies_data)}")
    return [DictWrapper(a) for a in allergies_data]


def create_immunizations_with_builder():
    """Create immunization history using fluent builder API."""
    print("\nCreating immunizations with fluent builder API...")

    immunizations_data = [
        (
            SimpleImmunizationBuilder()
            .vaccine("Influenza vaccine, seasonal", "141")
            .administration_date(date(2023, 9, 15))
            .status("completed")
            .lot_number("FLU2023-ABC123")
            .manufacturer("Sanofi Pasteur")
            .route("intramuscular")
            .site("left deltoid")
            .dose_quantity("0.5 mL")
            .build()
        ),
        (
            SimpleImmunizationBuilder()
            .vaccine("COVID-19 vaccine, mRNA, LNP-S, PF, 30 mcg/0.3 mL dose", "208")
            .administration_date(date(2023, 4, 10))
            .status("completed")
            .lot_number("COVID-XYZ789")
            .manufacturer("Pfizer Inc.")
            .route("intramuscular")
            .site("left deltoid")
            .dose_quantity("0.3 mL")
            .build()
        ),
        (
            SimpleImmunizationBuilder()
            .vaccine("Tetanus and diphtheria toxoids", "139")
            .administration_date(date(2020, 7, 5))
            .status("completed")
            .manufacturer("GlaxoSmithKline")
            .route("intramuscular")
            .site("right deltoid")
            .build()
        ),
    ]

    print(f"  Total immunizations: {len(immunizations_data)}")
    return [DictWrapper(i) for i in immunizations_data]


def create_vital_signs_with_builder():
    """Create vital signs using fluent builder API."""
    print("\nCreating vital signs with fluent builder API...")

    # Create individual vital sign observations
    heart_rate = (
        SimpleVitalSignBuilder()
        .observation("Heart Rate", "8867-4")
        .value("78", "bpm")
        .date(datetime(2023, 10, 20, 10, 30))
        .interpretation("Normal")
        .build()
    )

    bp_systolic = (
        SimpleVitalSignBuilder()
        .observation("Systolic Blood Pressure", "8480-6")
        .value("128", "mm[Hg]")
        .date(datetime(2023, 10, 20, 10, 30))
        .interpretation("Normal")
        .build()
    )

    bp_diastolic = (
        SimpleVitalSignBuilder()
        .observation("Diastolic Blood Pressure", "8462-4")
        .value("82", "mm[Hg]")
        .date(datetime(2023, 10, 20, 10, 30))
        .interpretation("Normal")
        .build()
    )

    temperature = (
        SimpleVitalSignBuilder()
        .observation("Body Temperature", "8310-5")
        .value("98.4", "degF")
        .date(datetime(2023, 10, 20, 10, 30))
        .interpretation("Normal")
        .build()
    )

    respiratory_rate = (
        SimpleVitalSignBuilder()
        .observation("Respiratory Rate", "9279-1")
        .value("16", "/min")
        .date(datetime(2023, 10, 20, 10, 30))
        .interpretation("Normal")
        .build()
    )

    # Create organizer for the vital signs
    organizer_data = (
        SimpleVitalSignsOrganizerBuilder()
        .date(datetime(2023, 10, 20, 10, 30))
        .add_vital_sign(heart_rate)
        .add_vital_sign(bp_systolic)
        .add_vital_sign(bp_diastolic)
        .add_vital_sign(temperature)
        .add_vital_sign(respiratory_rate)
        .build()
    )

    print(f"  Total vital signs: {len(organizer_data['vital_signs'])}")
    return [DictWrapper(organizer_data)]


def create_procedures_with_builder():
    """Create procedure history using fluent builder API."""
    print("\nCreating procedures with fluent builder API...")

    procedures_data = [
        (
            SimpleProcedureBuilder()
            .name("Colonoscopy")
            .code("73761001", "SNOMED")
            .date(date(2022, 6, 15))
            .status("completed")
            .target_site("Colon", "71854001")
            .performer("Dr. Michael Chen")
            .build()
        ),
        (
            SimpleProcedureBuilder()
            .name("Excision of skin lesion")
            .code("392091004", "SNOMED")
            .date(date(2021, 3, 20))
            .status("completed")
            .target_site("Left forearm", "723961002")
            .performer("Dr. Emily Rodriguez")
            .build()
        ),
    ]

    print(f"  Total procedures: {len(procedures_data)}")
    return [DictWrapper(p) for p in procedures_data]


def create_results_with_builder():
    """Create lab results using fluent builder API."""
    print("\nCreating lab results with fluent builder API...")

    # Create individual result observations
    glucose = (
        SimpleResultObservationBuilder()
        .test("Glucose", "2339-0")
        .value("98", "mg/dL")
        .status("final")
        .effective_time(datetime(2023, 10, 15, 8, 0))
        .value_type("PQ")
        .interpretation("N")
        .reference_range("70", "100", "mg/dL")
        .build()
    )

    hemoglobin_a1c = (
        SimpleResultObservationBuilder()
        .test("Hemoglobin A1c", "4548-4")
        .value("6.8", "%")
        .status("final")
        .effective_time(datetime(2023, 10, 15, 8, 0))
        .value_type("PQ")
        .interpretation("N")
        .reference_range("4.0", "6.0", "%")
        .build()
    )

    # Create result organizer (panel)
    metabolic_panel = (
        SimpleResultOrganizerBuilder()
        .panel("Basic Metabolic Panel", "51990-0")
        .status("completed")
        .effective_time(datetime(2023, 10, 15, 8, 0))
        .add_result(glucose)
        .add_result(hemoglobin_a1c)
        .build()
    )

    print("  Total result panels: 1")
    print(f"  Total results in panel: {len(metabolic_panel['results'])}")
    return [DictWrapper(metabolic_panel)]


def create_encounters_with_builder():
    """Create encounter history using fluent builder API."""
    print("\nCreating encounters with fluent builder API...")

    encounters_data = [
        (
            SimpleEncounterBuilder()
            .encounter_type("Office Visit", "99213", "CPT-4")
            .date(datetime(2023, 10, 20, 10, 0))
            .end_date(datetime(2023, 10, 20, 11, 0))
            .location("Community Health Center - Main Clinic")
            .performer("Dr. Alice Smith")
            .build()
        ),
        (
            SimpleEncounterBuilder()
            .encounter_type("Annual Physical", "99395", "CPT-4")
            .date(datetime(2023, 7, 15, 9, 0))
            .end_date(datetime(2023, 7, 15, 10, 30))
            .location("Community Health Center - Main Clinic")
            .performer("Dr. Alice Smith")
            .build()
        ),
    ]

    print(f"  Total encounters: {len(encounters_data)}")
    return [DictWrapper(e) for e in encounters_data]


def create_social_history_with_builder():
    """Create social history using fluent builder API."""
    print("\nCreating social history with fluent builder API...")

    smoking_status_data = (
        SimpleSmokingStatusBuilder()
        .status("Former smoker", "8517006")
        .date(datetime(2023, 10, 20))
        .build()
    )

    print("  Smoking status: Former smoker")
    return [DictWrapper(smoking_status_data)]


# ============================================================================
# Create Author and Custodian (using dict wrappers for simplicity)
# ============================================================================


def create_author():
    """Create author/provider data."""
    return DictWrapper(
        {
            "first_name": "Alice",
            "middle_name": "M",
            "last_name": "Smith",
            "npi": "9876543210",
            "time": datetime.now(),
            "addresses": [
                DictWrapper(
                    {
                        "street_lines": ["100 Medical Plaza"],
                        "city": "Cambridge",
                        "state": "MA",
                        "postal_code": "02139",
                        "country": "US",
                    }
                )
            ],
            "telecoms": [DictWrapper({"type": "phone", "value": "617-555-5555", "use": "work"})],
            "organization": DictWrapper(
                {
                    "name": "Community Health Center",
                    "npi": "1234567890",
                    "tin": None,
                    "oid_root": "2.16.840.1.113883.3.EXAMPLE",
                    "addresses": [
                        DictWrapper(
                            {
                                "street_lines": ["100 Medical Plaza"],
                                "city": "Cambridge",
                                "state": "MA",
                                "postal_code": "02139",
                                "country": "US",
                            }
                        )
                    ],
                    "telecoms": [
                        DictWrapper({"type": "phone", "value": "617-555-9999", "use": "work"})
                    ],
                }
            ),
        }
    )


def create_custodian():
    """Create custodian/organization data."""
    return DictWrapper(
        {
            "name": "Community Health Center",
            "npi": "1234567890",
            "tin": None,
            "oid_root": "2.16.840.1.113883.3.EXAMPLE",
            "addresses": [
                DictWrapper(
                    {
                        "street_lines": ["100 Medical Plaza"],
                        "city": "Cambridge",
                        "state": "MA",
                        "postal_code": "02139",
                        "country": "US",
                    }
                )
            ],
            "telecoms": [DictWrapper({"type": "phone", "value": "617-555-9999", "use": "work"})],
        }
    )


# ============================================================================
# Generate Complete C-CDA Document with Builder-Created Data
# ============================================================================


def generate_ccda_with_builders():
    """Generate complete C-CDA document using fluent builder API."""
    print("\n" + "=" * 80)
    print("Generating C-CDA R2.1 Document with Fluent Builder API")
    print("=" * 80)

    # Create all clinical data using builders
    patient = create_patient_with_builder()
    author = create_author()
    custodian = create_custodian()
    problems = create_problems_with_builder()
    medications = create_medications_with_builder()
    allergies = create_allergies_with_builder()
    immunizations = create_immunizations_with_builder()
    vital_signs = create_vital_signs_with_builder()
    procedures = create_procedures_with_builder()
    results = create_results_with_builder()
    encounters = create_encounters_with_builder()
    smoking_status = create_social_history_with_builder()

    print("\n" + "=" * 80)
    print("Building C-CDA Sections...")
    print("=" * 80)

    # Create sections
    problems_section = ProblemsSection(
        problems=problems,
        title="Problem List",
        version=CDAVersion.R2_1,
    )

    medications_section = MedicationsSection(
        medications=medications,
        title="Medications",
        version=CDAVersion.R2_1,
    )

    allergies_section = AllergiesSection(
        allergies=allergies,
        title="Allergies and Intolerances",
        version=CDAVersion.R2_1,
    )

    immunizations_section = ImmunizationsSection(
        immunizations=immunizations,
        title="Immunization History",
        version=CDAVersion.R2_1,
    )

    vital_signs_section = VitalSignsSection(
        vital_signs_organizers=vital_signs,
        title="Vital Signs",
        version=CDAVersion.R2_1,
    )

    procedures_section = ProceduresSection(
        procedures=procedures,
        title="Procedures",
        version=CDAVersion.R2_1,
    )

    results_section = ResultsSection(
        result_organizers=results,
        title="Laboratory Results",
        version=CDAVersion.R2_1,
    )

    encounters_section = EncountersSection(
        encounters=encounters,
        title="Encounters",
        version=CDAVersion.R2_1,
    )

    social_history_section = SocialHistorySection(
        smoking_statuses=smoking_status,
        title="Social History",
        version=CDAVersion.R2_1,
    )

    # Create complete document
    doc = ClinicalDocument(
        patient=patient,
        author=author,
        custodian=custodian,
        sections=[
            problems_section,
            medications_section,
            allergies_section,
            immunizations_section,
            vital_signs_section,
            procedures_section,
            results_section,
            encounters_section,
            social_history_section,
        ],
        title="Comprehensive Patient Clinical Summary",
        document_id=f"DOC-BUILDER-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        effective_time=datetime.now(),
        version=CDAVersion.R2_1,
    )

    # Generate XML
    xml_string = doc.to_xml_string(pretty=True)

    print("\n" + "=" * 80)
    print("Document Generated Successfully!")
    print("=" * 80)
    print(f"\nDocument Size: {len(xml_string):,} bytes")
    print("CDA Version: R2.1 (2015-08-01)")
    print("Total Sections: 9")

    print("\nDocument Structure:")
    print("  ✓ Patient demographics (via SimplePatientBuilder)")
    print("  ✓ Provider information")
    print("  ✓ Facility details")
    print(f"  ✓ Problems Section ({len(problems)} problems)")
    print(f"  ✓ Medications Section ({len(medications)} medications)")
    print(f"  ✓ Allergies Section ({len(allergies)} allergies)")
    print(f"  ✓ Immunizations Section ({len(immunizations)} immunizations)")
    print(
        f"  ✓ Vital Signs Section ({sum(len(vs.vital_signs) for vs in vital_signs)} measurements)"
    )
    print(f"  ✓ Procedures Section ({len(procedures)} procedures)")
    print(f"  ✓ Results Section (1 panel with {len(results[0].results)} results)")
    print(f"  ✓ Encounters Section ({len(encounters)} encounters)")
    print("  ✓ Social History Section (smoking status)")

    # Save to file
    output_file = "output_ccda_builder_example.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml_string)

    print(f"\nDocument saved to: {output_file}")

    print("\nBuilder Benefits Demonstrated:")
    print("  ✓ Fluent, chainable API - easy to read and write")
    print("  ✓ Less verbose than manual class instantiation")
    print("  ✓ Type-safe method parameters")
    print("  ✓ Clear, self-documenting code")
    print("  ✓ Reduced boilerplate")
    print("  ✓ Better IDE autocomplete support")

    return xml_string


# ============================================================================
# Main execution
# ============================================================================


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("ccdakit Example: Fluent Builder API Usage")
    print("=" * 80)
    print("\nThis example demonstrates how to use the simplified fluent builder API")
    print("to create C-CDA data models with less code and better readability.")

    # Generate document
    xml = generate_ccda_with_builders()

    print("\n" + "=" * 80)
    print("Example Complete!")
    print("=" * 80)
    print("\nCompare this example with examples/generate_ccda.py to see the difference")
    print("between manual class instantiation and fluent builder API.")
    print()
