"""Examples of using data validation utilities.

This example demonstrates how to validate data before building C-CDA documents
to catch errors early and ensure data quality.
"""

from datetime import date, datetime

from ccdakit.utils.validators import DataValidator


def example_1_validate_patient():
    """Example 1: Validating patient data before building."""
    print("=" * 70)
    print("Example 1: Validating Patient Data")
    print("=" * 70)

    # Valid patient data
    patient = {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": date(1980, 1, 15),
        "sex": "M",
        "addresses": [
            {
                "street_lines": ["123 Main St", "Apt 4B"],
                "city": "Boston",
                "state": "MA",
                "postal_code": "02101",
                "country": "US",
            }
        ],
        "telecoms": [
            {"type": "phone", "value": "617-555-1234", "use": "HP"},
            {"type": "email", "value": "john.doe@example.com", "use": "WP"},
        ],
    }

    result = DataValidator.validate_patient_data(patient)

    print("\nValidation Result:")
    print(f"Is Valid: {result.is_valid}")
    print(f"Errors: {len(result.errors)}")
    print(f"Warnings: {len(result.warnings)}")

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  - {error}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  - {warning}")


def example_2_handle_validation_errors():
    """Example 2: Handling validation errors."""
    print("\n" + "=" * 70)
    print("Example 2: Handling Validation Errors")
    print("=" * 70)

    # Invalid patient data (missing required fields)
    invalid_patient = {
        "first_name": "Jane",
        # Missing: last_name, date_of_birth, sex
    }

    result = DataValidator.validate_patient_data(invalid_patient)

    print(f"\nValidation Result: {'PASSED' if result.is_valid else 'FAILED'}")

    if not result.is_valid:
        print(f"\nFound {len(result.errors)} error(s):")
        for error in result.errors:
            print(f"  - {error.message}")

        # You can choose to raise an exception or handle errors differently
        try:
            result.raise_if_invalid()
        except Exception as e:
            print(f"\nCaught validation error: {type(e).__name__}")


def example_3_validate_problem_with_warnings():
    """Example 3: Validation with warnings (data is valid but suspicious)."""
    print("\n" + "=" * 70)
    print("Example 3: Validation with Warnings")
    print("=" * 70)

    # Problem data with inconsistent status
    problem = {
        "name": "Essential Hypertension",
        "code": "59621000",
        "code_system": "SNOMED",
        "status": "active",  # Status is active...
        "onset_date": date(2020, 1, 1),
        "resolved_date": date(2020, 6, 1),  # ...but has resolved_date
    }

    result = DataValidator.validate_problem_data(problem)

    print(f"\nValidation Result: {result.is_valid}")
    print(f"Has Warnings: {result.has_warnings}")

    if result.has_warnings:
        print(f"\nFound {len(result.warnings)} warning(s):")
        for warning in result.warnings:
            print(f"  - {warning.message}")
        print("\nWarnings indicate potential data quality issues but don't prevent building.")


def example_4_batch_validation():
    """Example 4: Batch validation of multiple items."""
    print("\n" + "=" * 70)
    print("Example 4: Batch Validation")
    print("=" * 70)

    medications = [
        {
            "name": "Lisinopril 10mg",
            "code": "314076",
            "dosage": "10 mg",
            "route": "oral",
            "frequency": "once daily",
            "start_date": date(2020, 1, 1),
            "status": "active",
        },
        {
            "name": "Metformin 500mg",
            "code": "860975",
            "dosage": "500 mg",
            "route": "oral",
            "frequency": "twice daily",
            "start_date": date(2019, 6, 1),
            "status": "active",
        },
        {
            "name": "Aspirin",  # Missing required fields
            "code": "1191",
        },
    ]

    print(f"\nValidating {len(medications)} medications...")

    valid_count = 0
    invalid_count = 0

    for i, med in enumerate(medications):
        result = DataValidator.validate_medication_data(med)
        if result.is_valid:
            valid_count += 1
            print(f"  Medication {i + 1}: Valid")
        else:
            invalid_count += 1
            print(f"  Medication {i + 1}: INVALID - {len(result.errors)} error(s)")
            for error in result.errors:
                print(f"    - {error.message}")

    print(f"\nSummary: {valid_count} valid, {invalid_count} invalid")


def example_5_validate_vital_signs():
    """Example 5: Validating vital signs with range checks."""
    print("\n" + "=" * 70)
    print("Example 5: Vital Signs Validation with Range Checks")
    print("=" * 70)

    vital_signs = {
        "date": datetime(2023, 10, 1, 10, 30),
        "vital_signs": [
            {
                "type": "Blood Pressure Systolic",
                "code": "8480-6",
                "value": "350",  # Suspiciously high
                "unit": "mm[Hg]",
            },
            {
                "type": "Heart Rate",
                "code": "8867-4",
                "value": "72",  # Normal
                "unit": "bpm",
            },
            {
                "type": "Body Temperature",
                "code": "8310-5",
                "value": "98.6",
                "unit": "[degF]",
            },
        ],
    }

    result = DataValidator.validate_vital_signs_data(vital_signs)

    print(f"\nValidation Result: {result.is_valid}")

    if result.has_warnings:
        print(f"\nWarnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  - {warning.message}")
        print("\nRange warnings help identify data entry errors.")


def example_6_validate_results():
    """Example 6: Validating lab results with reference ranges."""
    print("\n" + "=" * 70)
    print("Example 6: Lab Results Validation")
    print("=" * 70)

    lab_results = {
        "panel_name": "Complete Blood Count",
        "panel_code": "58410-2",
        "status": "final",
        "effective_time": datetime(2023, 10, 1, 9, 0),
        "results": [
            {
                "test_name": "Hemoglobin",
                "test_code": "718-7",
                "value": "14.5",
                "unit": "g/dL",
                "status": "final",
                "effective_time": datetime(2023, 10, 1, 9, 0),
                "reference_range_low": "12.0",
                "reference_range_high": "16.0",
                "reference_range_unit": "g/dL",
                "interpretation": "N",
            },
            {
                "test_name": "White Blood Cell Count",
                "test_code": "6690-2",
                "value": "7.5",
                "unit": "10*3/uL",
                "status": "final",
                "effective_time": datetime(2023, 10, 1, 9, 0),
                "reference_range_low": "4.5",
                "reference_range_high": "11.0",
                "reference_range_unit": "10*3/uL",
            },
        ],
    }

    result = DataValidator.validate_result_data(lab_results)

    print(f"\nValidation Result: {result.is_valid}")
    print(f"Panel: {lab_results['panel_name']}")
    print(f"Number of tests: {len(lab_results['results'])}")

    if result.is_valid:
        print("\nAll lab results validated successfully!")


def example_7_custom_validation_workflow():
    """Example 7: Custom validation workflow with error accumulation."""
    print("\n" + "=" * 70)
    print("Example 7: Custom Validation Workflow")
    print("=" * 70)

    # Simulate building a complete patient record
    patient_record = {
        "patient": {
            "first_name": "Alice",
            "last_name": "Smith",
            "date_of_birth": date(1975, 3, 20),
            "sex": "F",
        },
        "problems": [
            {
                "name": "Type 2 Diabetes",
                "code": "44054006",
                "code_system": "SNOMED",
                "status": "active",
                "onset_date": date(2018, 5, 1),
            }
        ],
        "medications": [
            {
                "name": "Metformin 1000mg",
                "code": "860999",
                "dosage": "1000 mg",
                "route": "oral",
                "frequency": "twice daily",
                "start_date": date(2018, 5, 15),
                "status": "active",
            }
        ],
        "allergies": [
            {
                "allergen": "Penicillin",
                "allergen_code": "7980",
                "allergen_code_system": "RxNorm",
                "allergy_type": "allergy",
                "status": "active",
                "severity": "severe",
                "reaction": "Anaphylaxis",
            }
        ],
    }

    print("\nValidating complete patient record...")

    all_valid = True
    total_errors = 0
    total_warnings = 0

    # Validate patient
    result = DataValidator.validate_patient_data(patient_record["patient"])
    print(f"\n  Patient: {'Valid' if result.is_valid else 'INVALID'}")
    if not result.is_valid:
        all_valid = False
        total_errors += len(result.errors)
    total_warnings += len(result.warnings)

    # Validate problems
    for i, problem in enumerate(patient_record["problems"]):
        result = DataValidator.validate_problem_data(problem)
        print(f"  Problem {i + 1}: {'Valid' if result.is_valid else 'INVALID'}")
        if not result.is_valid:
            all_valid = False
            total_errors += len(result.errors)
        total_warnings += len(result.warnings)

    # Validate medications
    for i, med in enumerate(patient_record["medications"]):
        result = DataValidator.validate_medication_data(med)
        print(f"  Medication {i + 1}: {'Valid' if result.is_valid else 'INVALID'}")
        if not result.is_valid:
            all_valid = False
            total_errors += len(result.errors)
        total_warnings += len(result.warnings)

    # Validate allergies
    for i, allergy in enumerate(patient_record["allergies"]):
        result = DataValidator.validate_allergy_data(allergy)
        print(f"  Allergy {i + 1}: {'Valid' if result.is_valid else 'INVALID'}")
        if not result.is_valid:
            all_valid = False
            total_errors += len(result.errors)
        total_warnings += len(result.warnings)

    print("\nValidation Summary:")
    print(f"  Overall: {'PASSED' if all_valid else 'FAILED'}")
    print(f"  Total Errors: {total_errors}")
    print(f"  Total Warnings: {total_warnings}")

    if all_valid:
        print("\n  Ready to build C-CDA document!")
    else:
        print("\n  Fix errors before building C-CDA document.")


def example_8_validate_before_building():
    """Example 8: Integration with document building."""
    print("\n" + "=" * 70)
    print("Example 8: Validate Before Building")
    print("=" * 70)

    problem_data = {
        "name": "Essential Hypertension",
        "code": "59621000",
        "code_system": "SNOMED",
        "status": "active",
        "onset_date": date(2020, 1, 1),
    }

    print("\nValidating problem data before building...")

    # Validate first
    validation_result = DataValidator.validate_problem_data(problem_data)

    if validation_result.is_valid:
        print("  Validation passed!")
        print("\n  You can now safely build the C-CDA problem entry:")
        print("    from ccdakit.builders.entries.problem import ProblemConcernAct")
        print("    problem_entry = ProblemConcernAct(problem_data).build()")
    else:
        print("  Validation failed!")
        print("\n  Errors found:")
        for error in validation_result.errors:
            print(f"    - {error.message}")
        print("\n  Fix these errors before building.")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("C-CDA Data Validation Examples")
    print("=" * 70)

    example_1_validate_patient()
    example_2_handle_validation_errors()
    example_3_validate_problem_with_warnings()
    example_4_batch_validation()
    example_5_validate_vital_signs()
    example_6_validate_results()
    example_7_custom_validation_workflow()
    example_8_validate_before_building()

    print("\n" + "=" * 70)
    print("Examples Complete")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  1. Always validate data before building C-CDA documents")
    print("  2. Errors prevent building; warnings indicate potential issues")
    print("  3. Use batch validation for multiple items")
    print("  4. Range checks help identify data entry errors")
    print("  5. ValidationResult.raise_if_invalid() for strict validation")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
