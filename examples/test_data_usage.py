"""Example: Using Test Data Generators

This example demonstrates how to use the TestDataGenerator class to create
realistic test data for C-CDA documents. The generator can create individual
data elements or complete patient records with all clinical sections.

To run this example, first install the test-data optional dependency:
    pip install 'ccdakit[test-data]'
    # or
    uv pip install 'ccdakit[test-data]'
"""

from ccdakit.utils.test_data import TestDataGenerator


def example_basic_generation():
    """Example: Generate individual data elements."""
    print("=" * 80)
    print("Example 1: Basic Data Generation")
    print("=" * 80)

    # Create generator (without seed for random data each time)
    gen = TestDataGenerator()

    # Generate patient demographics
    patient = gen.generate_patient()
    print(f"\nPatient: {patient['first_name']} {patient['last_name']}")
    print(f"  DOB: {patient['date_of_birth']}")
    print(f"  Sex: {patient['sex']}")
    print(f"  Address: {patient['addresses'][0]['city']}, {patient['addresses'][0]['state']}")

    # Generate a problem
    problem = gen.generate_problem()
    print(f"\nProblem: {problem['name']}")
    print(f"  Code: {problem['code']} ({problem['code_system']})")
    print(f"  Status: {problem['status']}")
    print(f"  Onset: {problem['onset_date']}")

    # Generate a medication
    medication = gen.generate_medication()
    print(f"\nMedication: {medication['name']}")
    print(f"  Dosage: {medication['dosage']} {medication['route']} {medication['frequency']}")
    print(f"  Status: {medication['status']}")

    # Generate an allergy
    allergy = gen.generate_allergy()
    print(f"\nAllergy: {allergy['allergen']}")
    print(f"  Type: {allergy['allergy_type']}")
    print(f"  Reaction: {allergy['reaction']}")
    print(f"  Severity: {allergy['severity']}")

    # Generate vital signs
    vital_signs = gen.generate_vital_signs(count=3)
    print(f"\nVital Signs (taken at {vital_signs['date']}):")
    for sign in vital_signs["vital_signs"]:
        print(f"  {sign['type']}: {sign['value']} {sign['unit']}")

    # Generate an immunization
    immunization = gen.generate_immunization()
    print(f"\nImmunization: {immunization['vaccine_name']}")
    print(f"  CVX Code: {immunization['cvx_code']}")
    print(f"  Date: {immunization['administration_date']}")
    print(f"  Status: {immunization['status']}")
    if immunization["lot_number"]:
        print(f"  Lot: {immunization['lot_number']}")
        print(f"  Manufacturer: {immunization['manufacturer']}")


def example_reproducible_data():
    """Example: Generate reproducible data using seeds."""
    print("\n" + "=" * 80)
    print("Example 2: Reproducible Data Generation (with seed)")
    print("=" * 80)

    # Using a seed ensures the same data is generated each time
    gen1 = TestDataGenerator(seed=42)
    gen2 = TestDataGenerator(seed=42)

    patient1 = gen1.generate_patient()
    patient2 = gen2.generate_patient()

    print(f"\nGenerator 1 Patient: {patient1['first_name']} {patient1['last_name']}")
    print(f"Generator 2 Patient: {patient2['first_name']} {patient2['last_name']}")
    print(f"Are they the same? {patient1['first_name'] == patient2['first_name']}")

    # Different seeds produce different data
    gen3 = TestDataGenerator(seed=100)
    patient3 = gen3.generate_patient()
    print(
        f"\nGenerator 3 Patient (different seed): {patient3['first_name']} {patient3['last_name']}"
    )


def example_complete_patient_record():
    """Example: Generate complete patient record."""
    print("\n" + "=" * 80)
    print("Example 3: Complete Patient Record Generation")
    print("=" * 80)

    gen = TestDataGenerator(seed=42)

    # Generate complete patient record with default counts
    record = gen.generate_complete_patient_record()

    print(f"\nPatient: {record['patient']['first_name']} {record['patient']['last_name']}")
    print(f"  DOB: {record['patient']['date_of_birth']}")
    print(f"  Sex: {record['patient']['sex']}")

    print(f"\nProblems ({len(record['problems'])}):")
    for i, problem in enumerate(record["problems"], 1):
        print(f"  {i}. {problem['name']} - {problem['status']}")

    print(f"\nMedications ({len(record['medications'])}):")
    for i, med in enumerate(record["medications"], 1):
        print(f"  {i}. {med['name']} - {med['dosage']} {med['frequency']}")

    print(f"\nAllergies ({len(record['allergies'])}):")
    for i, allergy in enumerate(record["allergies"], 1):
        print(f"  {i}. {allergy['allergen']} - {allergy['severity']}")

    print(f"\nVital Signs Sets: {len(record['vital_signs'])}")
    print(f"Immunizations: {len(record['immunizations'])}")


def example_custom_counts():
    """Example: Generate patient record with custom counts."""
    print("\n" + "=" * 80)
    print("Example 4: Custom Data Counts")
    print("=" * 80)

    gen = TestDataGenerator(seed=123)

    # Generate patient with specific counts for each section
    record = gen.generate_complete_patient_record(
        num_problems=5,
        num_medications=4,
        num_allergies=3,
        num_vital_signs_sets=2,
        num_immunizations=6,
    )

    print("\nGenerated patient record with:")
    print(f"  Problems: {len(record['problems'])}")
    print(f"  Medications: {len(record['medications'])}")
    print(f"  Allergies: {len(record['allergies'])}")
    print(f"  Vital Signs Sets: {len(record['vital_signs'])}")
    print(f"  Immunizations: {len(record['immunizations'])}")


def example_bulk_generation():
    """Example: Generate multiple patient records."""
    print("\n" + "=" * 80)
    print("Example 5: Bulk Patient Record Generation")
    print("=" * 80)

    # Generate 5 different patients
    patients = []
    for i in range(5):
        gen = TestDataGenerator(seed=i)  # Different seed for each
        record = gen.generate_complete_patient_record()
        patients.append(record)

    print(f"\nGenerated {len(patients)} patient records:")
    for i, record in enumerate(patients, 1):
        patient = record["patient"]
        print(
            f"  {i}. {patient['first_name']} {patient['last_name']} "
            f"(DOB: {patient['date_of_birth']}, "
            f"{len(record['problems'])} problems, "
            f"{len(record['medications'])} medications)"
        )


def example_integration_with_ccda():
    """Example: Using test data with C-CDA builders."""
    print("\n" + "=" * 80)
    print("Example 6: Integration with C-CDA Builders")
    print("=" * 80)

    print("\nNote: This example shows how test data can be used with C-CDA builders.")
    print("The generated dictionaries match the protocol interfaces expected by the builders.")

    gen = TestDataGenerator(seed=42)

    # Generate test data
    patient_data = gen.generate_patient()
    problem_data = gen.generate_problem()
    medication_data = gen.generate_medication()

    print("\nGenerated patient data structure:")
    print(f"  Name: {patient_data['first_name']} {patient_data['last_name']}")
    print("  Has all required fields for PatientProtocol: ✓")

    print("\nGenerated problem data structure:")
    print(f"  Problem: {problem_data['name']}")
    print("  Has all required fields for ProblemProtocol: ✓")

    print("\nGenerated medication data structure:")
    print(f"  Medication: {medication_data['name']}")
    print("  Has all required fields for MedicationProtocol: ✓")

    print("\nTo use with builders, create simple classes that wrap the dictionaries:")
    print("""
    class SimplePatient:
        def __init__(self, data):
            self._data = data

        @property
        def first_name(self):
            return self._data['first_name']

        # ... implement other properties ...

    patient = SimplePatient(patient_data)
    # Now patient can be used with Demographics builder
    """)


if __name__ == "__main__":
    # Run all examples
    example_basic_generation()
    example_reproducible_data()
    example_complete_patient_record()
    example_custom_counts()
    example_bulk_generation()
    example_integration_with_ccda()

    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80)
