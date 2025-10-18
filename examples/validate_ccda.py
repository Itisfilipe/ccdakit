"""
Example demonstrating C-CDA document validation with XSD schemas.

This example shows how to:
1. Check if C-CDA schemas are installed
2. Validate a C-CDA document against XSD schemas
3. Handle validation errors and warnings
4. Use the SchemaManager utility
"""

from pathlib import Path

from ccdakit.validators import SchemaManager, XSDValidator


def check_schema_availability():
    """Check if C-CDA XSD schemas are available."""
    print("=" * 70)
    print("Checking Schema Availability")
    print("=" * 70)

    manager = SchemaManager()
    info = manager.get_schema_info()

    print(f"\nSchema Directory: {info['schema_dir']}")
    print(f"Schemas Installed: {info['installed']}")
    print(f"CDA.xsd Exists: {info['cda_exists']}")

    if info["files"]:
        print(f"\nFound {len(info['files'])} files:")
        for file in info["files"]:
            print(f"  - {file}")
    else:
        print("\nNo schema files found.")

    print()
    return info["installed"]


def print_installation_instructions():
    """Print instructions for installing schemas."""
    print("=" * 70)
    print("Schema Installation Required")
    print("=" * 70)
    print("\nC-CDA XSD schemas must be downloaded from HL7 before validation.")
    print("\nOption 1: Manual Download (Recommended)")
    print("-" * 70)
    print("1. Visit: https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492")
    print('2. Download "CCDA_R2.1_Schemas.zip"')
    print("3. Extract CDA.xsd and other schema files to the schemas/ directory")
    print("\nOption 2: Use SchemaManager")
    print("-" * 70)
    print(">>> from ccdakit.validators.utils import print_schema_installation_help")
    print(">>> print_schema_installation_help()")
    print()


def validate_document_example(schema_path: Path, xml_file: Path):
    """Example of validating a C-CDA document."""
    print("=" * 70)
    print("Validating C-CDA Document")
    print("=" * 70)

    print(f"\nSchema: {schema_path}")
    print(f"Document: {xml_file}")

    # Initialize validator
    print("\n[1] Initializing XSD Validator...")
    validator = XSDValidator(schema_path)
    print("    ✓ Validator initialized successfully")

    # Validate document
    print("\n[2] Validating document...")
    result = validator.validate(xml_file)

    # Display results
    print("\n[3] Validation Results:")
    print("-" * 70)

    if result.is_valid:
        print("✓ Document is VALID")
        print("  - No errors found")
    else:
        print("✗ Document is INVALID")
        print(f"  - {len(result.errors)} error(s) found")

    if result.has_warnings:
        print(f"⚠  {len(result.warnings)} warning(s) found")

    # Display detailed errors
    if result.errors:
        print("\n[4] Validation Errors:")
        print("-" * 70)
        for i, error in enumerate(result.errors, 1):
            print(f"\nError {i}:")
            print(f"  Location: {error.location or 'Unknown'}")
            print(f"  Message:  {error.message}")
            print(f"  Code:     {error.code}")

    # Display warnings
    if result.warnings:
        print("\n[5] Validation Warnings:")
        print("-" * 70)
        for i, warning in enumerate(result.warnings, 1):
            print(f"\nWarning {i}:")
            print(f"  Location: {warning.location or 'Unknown'}")
            print(f"  Message:  {warning.message}")

    print()
    return result


def validate_string_example(schema_path: Path, xml_string: str):
    """Example of validating an XML string."""
    print("=" * 70)
    print("Validating XML String")
    print("=" * 70)

    validator = XSDValidator(schema_path)
    result = validator.validate_string(xml_string)

    print(f"\nValidation Result: {'VALID' if result.is_valid else 'INVALID'}")
    print(f"Errors: {len(result.errors)}")
    print(f"Warnings: {len(result.warnings)}")
    print()

    return result


def convenience_methods_example(schema_path: Path):
    """Demonstrate convenience validation methods."""
    print("=" * 70)
    print("Convenience Methods")
    print("=" * 70)

    validator = XSDValidator(schema_path)

    # Example 1: Validate string
    print("\n[1] Validating XML String:")
    xml_string = '<?xml version="1.0"?><ClinicalDocument xmlns="urn:hl7-org:v3"></ClinicalDocument>'
    result = validator.validate_string(xml_string)
    print(f"    Result: {'VALID' if result.is_valid else 'INVALID'}")

    # Example 2: Validate bytes
    print("\n[2] Validating XML Bytes:")
    xml_bytes = xml_string.encode("utf-8")
    result = validator.validate_bytes(xml_bytes)
    print(f"    Result: {'VALID' if result.is_valid else 'INVALID'}")

    # Example 3: Validate file
    print("\n[3] Validating XML File:")
    print("    (Use validate_file(path) method)")

    print()


def main():
    """Main example function."""
    print("\n")
    print("=" * 70)
    print("C-CDA Document Validation Example")
    print("=" * 70)
    print()

    # Step 1: Check if schemas are available
    schemas_available = check_schema_availability()

    if not schemas_available:
        print_installation_instructions()
        print("⚠  Cannot run validation examples without schemas.")
        print("   Please install C-CDA XSD schemas first.")
        return

    # Get schema path
    manager = SchemaManager()
    schema_path = manager.get_cda_schema_path()

    # Check if we have an example XML file to validate
    example_xml = Path("output_ccda_with_sections.xml")

    if example_xml.exists():
        print(f"Found example document: {example_xml}")
        print("\n[Validation Example 1: File Validation]")
        result = validate_document_example(schema_path, example_xml)

        # Show how to handle validation result programmatically
        print("=" * 70)
        print("Programmatic Result Handling")
        print("=" * 70)
        print("\n# Check validation status:")
        print(f"result.is_valid = {result.is_valid}")
        print(f"result.has_warnings = {result.has_warnings}")
        print(f"len(result.errors) = {len(result.errors)}")
        print()

        # Show how to raise exception on validation failure
        print("# Raise exception if invalid:")
        print("try:")
        print("    result.raise_if_invalid()")
        print("except ValidationError as e:")
        print('    print(f"Validation failed: {e}")')
        print()

    else:
        print(f"⚠  Example XML file not found: {example_xml}")
        print("   Run 'python examples/generate_ccda.py' first to create an example document.")
        print()

    # Demonstrate convenience methods
    print("\n[Validation Example 2: Convenience Methods]")
    convenience_methods_example(schema_path)

    print("=" * 70)
    print("Example Complete")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
