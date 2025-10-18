"""
Example demonstrating value set usage in pyccda.

This example shows how to:
1. Look up valid codes in value sets
2. Validate user input against value sets
3. Get display names for codes
4. List available value sets
5. Search for codes by display name
6. Load and save value sets from/to JSON files
"""

from pathlib import Path

from ccdakit.utils.value_sets import ValueSetRegistry


def example_basic_validation():
    """Example: Basic code validation."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Code Validation")
    print("=" * 60)

    # Validate problem status codes
    code = "55561003"
    if ValueSetRegistry.validate_code("PROBLEM_STATUS", code):
        display = ValueSetRegistry.get_display_name("PROBLEM_STATUS", code)
        print(f"✓ Code {code} is valid: {display}")
    else:
        print(f"✗ Code {code} is invalid")

    # Try an invalid code
    invalid_code = "99999999"
    if ValueSetRegistry.validate_code("PROBLEM_STATUS", invalid_code):
        print(f"✓ Code {invalid_code} is valid")
    else:
        print(f"✗ Code {invalid_code} is invalid for PROBLEM_STATUS")

    print()


def example_user_input_validation():
    """Example: Validating user input."""
    print("=" * 60)
    print("EXAMPLE 2: User Input Validation")
    print("=" * 60)

    # Simulate user selecting a gender
    user_gender = "M"

    if ValueSetRegistry.validate_code("ADMINISTRATIVE_GENDER", user_gender):
        display = ValueSetRegistry.get_display_name("ADMINISTRATIVE_GENDER", user_gender)
        system = ValueSetRegistry.get_code_system("ADMINISTRATIVE_GENDER", user_gender)
        print(f"User selected gender: {display}")
        print(f"Code: {user_gender}")
        print(f"Code system: {system}")
    else:
        print(f"Invalid gender code: {user_gender}")

    print()


def example_listing_available_codes():
    """Example: Listing all available codes in a value set."""
    print("=" * 60)
    print("EXAMPLE 3: Listing Available Codes")
    print("=" * 60)

    # List all smoking status codes
    print("Available Smoking Status codes:")
    codes = ValueSetRegistry.get_codes("SMOKING_STATUS")

    for code in codes:
        display = ValueSetRegistry.get_display_name("SMOKING_STATUS", code)
        print(f"  - {code}: {display}")

    print()


def example_value_set_metadata():
    """Example: Getting value set metadata."""
    print("=" * 60)
    print("EXAMPLE 4: Value Set Metadata")
    print("=" * 60)

    vs = ValueSetRegistry.get_value_set("PROBLEM_STATUS")
    if vs:
        print(f"Name: {vs['name']}")
        print(f"OID: {vs['oid']}")
        print(f"Description: {vs['description']}")
        print(f"Number of codes: {len(vs['codes'])}")

    print()


def example_searching_by_display_name():
    """Example: Search for codes by display name."""
    print("=" * 60)
    print("EXAMPLE 5: Searching by Display Name")
    print("=" * 60)

    # Search for observation interpretation codes containing "high"
    search_term = "high"
    codes = ValueSetRegistry.search_by_display("OBSERVATION_INTERPRETATION", search_term)

    print(f"Codes containing '{search_term}':")
    for code in codes:
        display = ValueSetRegistry.get_display_name("OBSERVATION_INTERPRETATION", code)
        print(f"  - {code}: {display}")

    print()


def example_listing_all_value_sets():
    """Example: List all available value sets."""
    print("=" * 60)
    print("EXAMPLE 6: Listing All Value Sets")
    print("=" * 60)

    value_sets = ValueSetRegistry.list_value_sets()
    print(f"Total value sets: {len(value_sets)}\n")

    for vs_name in sorted(value_sets):
        vs = ValueSetRegistry.get_value_set(vs_name)
        code_count = len(vs["codes"])
        print(f"{vs_name:30} - {vs['name']:40} ({code_count} codes)")

    print()


def example_vital_signs():
    """Example: Working with vital sign codes."""
    print("=" * 60)
    print("EXAMPLE 7: Vital Sign Codes")
    print("=" * 60)

    vital_signs = [
        ("8310-5", "Body temperature"),
        ("8867-4", "Heart rate"),
        ("8480-6", "Systolic blood pressure"),
        ("8462-4", "Diastolic blood pressure"),
        ("2710-2", "Oxygen saturation"),
    ]

    print("Common Vital Signs:")
    for code, _expected_display in vital_signs:
        if ValueSetRegistry.validate_code("VITAL_SIGN_RESULT_TYPE", code):
            display = ValueSetRegistry.get_display_name("VITAL_SIGN_RESULT_TYPE", code)
            system = ValueSetRegistry.get_code_system("VITAL_SIGN_RESULT_TYPE", code)
            print(f"  ✓ {code} ({system}): {display}")
        else:
            print(f"  ✗ {code} is not valid")

    print()


def example_encounter_types():
    """Example: Working with encounter type codes."""
    print("=" * 60)
    print("EXAMPLE 8: Encounter Types")
    print("=" * 60)

    encounters = ["AMB", "EMER", "IMP", "HH", "VR"]

    print("Encounter Type Codes:")
    for code in encounters:
        display = ValueSetRegistry.get_display_name("ENCOUNTER_TYPE", code)
        print(f"  {code:10} - {display}")

    print()


def example_observation_interpretation():
    """Example: Observation interpretation codes."""
    print("=" * 60)
    print("EXAMPLE 9: Observation Interpretation")
    print("=" * 60)

    # Simulate interpreting lab results
    results = [
        ("Glucose", 95, "N"),
        ("Cholesterol", 250, "H"),
        ("Potassium", 2.8, "L"),
        ("Troponin", 5.2, "HH"),
    ]

    print("Lab Result Interpretations:")
    for test_name, value, interpretation_code in results:
        if ValueSetRegistry.validate_code("OBSERVATION_INTERPRETATION", interpretation_code):
            interpretation = ValueSetRegistry.get_display_name(
                "OBSERVATION_INTERPRETATION", interpretation_code
            )
            print(f"  {test_name:15} = {value:6.1f} [{interpretation_code}] - {interpretation}")
        else:
            print(f"  {test_name:15} = {value:6.1f} [Invalid code: {interpretation_code}]")

    print()


def example_medication_workflow():
    """Example: Medication status workflow."""
    print("=" * 60)
    print("EXAMPLE 10: Medication Status Workflow")
    print("=" * 60)

    # Simulate medication lifecycle
    statuses = [
        ("55561003", "Patient is currently taking medication"),
        ("completed", "Patient finished medication course"),
        ("aborted", "Medication was discontinued"),
    ]

    print("Medication Status Transitions:")
    for status_code, description in statuses:
        display = ValueSetRegistry.get_display_name("MEDICATION_STATUS", status_code)
        system = ValueSetRegistry.get_code_system("MEDICATION_STATUS", status_code)
        print(f"  {status_code:12} ({system:15}) - {display:20} - {description}")

    print()


def example_complete_code_info():
    """Example: Getting complete code information."""
    print("=" * 60)
    print("EXAMPLE 11: Complete Code Information")
    print("=" * 60)

    code = "255604002"
    value_set = "ALLERGY_SEVERITY"

    info = ValueSetRegistry.get_code_info(value_set, code)
    if info:
        print(f"Code: {code}")
        print(f"Display: {info['display']}")
        print(f"System: {info['system']}")

        # Also show value set context
        vs = ValueSetRegistry.get_value_set(value_set)
        print(f"Value Set: {vs['name']}")
        print(f"OID: {vs['oid']}")
        print(f"Description: {vs['description']}")
    else:
        print(f"Code {code} not found in {value_set}")

    print()


def example_null_flavors():
    """Example: Working with null flavors."""
    print("=" * 60)
    print("EXAMPLE 12: Null Flavors for Missing Data")
    print("=" * 60)

    null_flavors = ["NI", "UNK", "NA", "ASKU", "NASK"]

    print("Common Null Flavors:")
    for code in null_flavors:
        display = ValueSetRegistry.get_display_name("NULL_FLAVOR", code)
        print(f"  {code:6} - {display}")

    print()


def example_lookup_by_oid():
    """Example: Looking up value set by OID."""
    print("=" * 60)
    print("EXAMPLE 13: Lookup Value Set by OID")
    print("=" * 60)

    oid = "2.16.840.1.113883.11.20.9.38"  # Smoking Status OID
    vs = ValueSetRegistry.get_value_set_by_oid(oid)

    if vs:
        print(f"Found value set for OID: {oid}")
        print(f"Name: {vs['name']}")
        print(f"Description: {vs['description']}")
        print(f"Number of codes: {len(vs['codes'])}")
    else:
        print(f"No value set found for OID: {oid}")

    print()


def example_json_export_import():
    """Example: Export and import value sets to/from JSON."""
    print("=" * 60)
    print("EXAMPLE 14: Export/Import Value Sets")
    print("=" * 60)

    # Export a value set to JSON
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "exported_problem_status.json"

        print(f"Exporting PROBLEM_STATUS to: {output_file}")
        ValueSetRegistry.save_to_json("PROBLEM_STATUS", str(output_file))
        print("✓ Exported successfully")

        # Load it back
        print(f"\nLoading value set from: {output_file}")
        loaded_data = ValueSetRegistry.load_from_json(str(output_file))
        print("✓ Loaded successfully")
        print(f"  Name: {loaded_data['name']}")
        print(f"  OID: {loaded_data['oid']}")
        print(f"  Codes: {len(loaded_data['codes'])}")

    print()


def example_loading_external_value_sets():
    """Example: Load external value set JSON files."""
    print("=" * 60)
    print("EXAMPLE 15: Loading External Value Set Files")
    print("=" * 60)

    # Try to load bundled value set files
    value_sets_dir = Path(__file__).parent.parent / "pyccda" / "utils" / "value_sets"

    if value_sets_dir.exists():
        json_files = list(value_sets_dir.glob("*.json"))
        print(f"Found {len(json_files)} value set JSON files:\n")

        for json_file in json_files:
            try:
                vs_data = ValueSetRegistry.load_from_json(str(json_file))
                print(
                    f"✓ {json_file.name:30} - {vs_data['name']:40} ({len(vs_data['codes'])} codes)"
                )
            except Exception as e:
                print(f"✗ {json_file.name:30} - Error: {e}")
    else:
        print(f"Value sets directory not found: {value_sets_dir}")

    print()


def main():
    """Run all examples."""
    print("\n")
    print("*" * 60)
    print("VALUE SET USAGE EXAMPLES")
    print("*" * 60)
    print("\n")

    example_basic_validation()
    example_user_input_validation()
    example_listing_available_codes()
    example_value_set_metadata()
    example_searching_by_display_name()
    example_listing_all_value_sets()
    example_vital_signs()
    example_encounter_types()
    example_observation_interpretation()
    example_medication_workflow()
    example_complete_code_info()
    example_null_flavors()
    example_lookup_by_oid()
    example_json_export_import()
    example_loading_external_value_sets()

    print("*" * 60)
    print("All examples completed!")
    print("*" * 60)


if __name__ == "__main__":
    main()
