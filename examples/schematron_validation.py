"""
Example demonstrating C-CDA document validation with Schematron rules.

This example shows how to:
1. Load and use the HL7 C-CDA R2.1 Schematron validator
2. Validate C-CDA documents for business rules and template conformance
3. Understand and interpret Schematron validation results
4. Combine XSD and Schematron validation for complete validation
5. Common fixes for Schematron validation failures
"""

from pathlib import Path

from ccdakit.validators import SchematronValidator, XSDValidator


def check_schematron_availability():
    """Check if Schematron files are available."""
    print("=" * 70)
    print("Checking Schematron Availability")
    print("=" * 70)

    schematron_path = Path("schemas/schematron/HL7_CCDA_R2.1.sch")
    voc_path = Path("schemas/schematron/voc.xml")

    print(f"\nSchematron File: {schematron_path}")
    print(f"Exists: {schematron_path.exists()}")

    if schematron_path.exists():
        size_mb = schematron_path.stat().st_size / (1024 * 1024)
        print(f"Size: {size_mb:.2f} MB")

    print(f"\nVocabulary File: {voc_path}")
    print(f"Exists: {voc_path.exists()}")

    if voc_path.exists():
        size_mb = voc_path.stat().st_size / (1024 * 1024)
        print(f"Size: {size_mb:.2f} MB")

    print()
    return schematron_path.exists() and voc_path.exists()


def print_installation_instructions():
    """Print instructions for installing Schematron files."""
    print("=" * 70)
    print("Schematron Installation Required")
    print("=" * 70)
    print("\nSchematron files are required for business rule validation.")
    print("\nAutomatic Installation:")
    print("-" * 70)
    print("The files have been automatically downloaded from HL7's GitHub repository.")
    print("\nManual Installation:")
    print("-" * 70)
    print("1. Visit: https://github.com/HL7/CDA-ccda-2.1")
    print("2. Download from the validation/ directory:")
    print('   - "Consolidated CDA Templates for Clinical Notes (US Realm) DSTU R2.1.sch"')
    print("   - voc.xml")
    print("3. Place them in: schemas/schematron/")
    print("   - Rename the .sch file to: HL7_CCDA_R2.1.sch")
    print("\nOr run the download command:")
    print("-" * 70)
    print("cd schemas/schematron")
    print('curl -L -o "HL7_CCDA_R2.1.sch" \\')
    print('  "https://raw.githubusercontent.com/HL7/CDA-ccda-2.1/master/validation/...')
    print()


def validate_document_with_schematron(xml_file: Path):
    """Example of validating a C-CDA document with Schematron."""
    print("=" * 70)
    print("Schematron Validation")
    print("=" * 70)

    print(f"\nDocument: {xml_file}")

    # Initialize validator with default HL7 C-CDA R2.1 Schematron
    print("\n[1] Initializing Schematron Validator...")
    try:
        validator = SchematronValidator()
        print("    ✓ Validator initialized successfully")
        print(f"    Schematron: {validator.schematron_location.name}")
    except FileNotFoundError as e:
        print(f"    ✗ Error: {e}")
        print("\n    Schematron files not found.")
        print("    See schemas/schematron/README.md for installation instructions.")
        return None

    # Validate document
    print("\n[2] Validating document against Schematron rules...")
    print("    (This may take a few seconds for large documents)")
    result = validator.validate(xml_file)

    # Display results
    print("\n[3] Validation Results:")
    print("-" * 70)

    if result.is_valid:
        print("✓ Document is VALID")
        print("  - All Schematron business rules passed")
        print("  - Document conforms to C-CDA R2.1 templates")
    else:
        print("✗ Document is INVALID")
        print(f"  - {len(result.errors)} Schematron assertion(s) failed")

    if result.has_warnings:
        print(f"⚠  {len(result.warnings)} warning(s) found")

    # Display detailed errors
    if result.errors:
        print("\n[4] Schematron Assertions Failed:")
        print("-" * 70)
        for i, error in enumerate(result.errors[:10], 1):  # Show first 10
            print(f"\nAssertion {i}:")
            print(f"  Location: {error.location or 'Unknown'}")
            print(f"  Rule:     {error.code}")
            print(f"  Message:  {error.message[:200]}...")  # Truncate long messages

        if len(result.errors) > 10:
            print(f"\n  ... and {len(result.errors) - 10} more errors")

    # Display warnings
    if result.warnings:
        print("\n[5] Warnings:")
        print("-" * 70)
        for i, warning in enumerate(result.warnings[:5], 1):  # Show first 5
            print(f"\nWarning {i}:")
            print(f"  Location: {warning.location or 'Unknown'}")
            print(f"  Message:  {warning.message[:200]}...")

        if len(result.warnings) > 5:
            print(f"\n  ... and {len(result.warnings) - 5} more warnings")

    print()
    return result


def combined_validation_example(xml_file: Path):
    """Example of combining XSD and Schematron validation."""
    print("=" * 70)
    print("Combined Validation (XSD + Schematron)")
    print("=" * 70)
    print("\nBest Practice: Validate with both XSD and Schematron")
    print("  1. XSD validates document structure and data types")
    print("  2. Schematron validates business rules and template conformance")
    print()

    # Step 1: XSD Validation
    print("[1] XSD Schema Validation:")
    print("-" * 70)

    xsd_schema_path = Path("schemas/CDA.xsd")

    if not xsd_schema_path.exists():
        print("⚠  XSD schema not found. Skipping XSD validation.")
        print("   See schemas/README.md for installation instructions.")
        xsd_valid = None
    else:
        xsd_validator = XSDValidator(xsd_schema_path)
        xsd_result = xsd_validator.validate(xml_file)

        if xsd_result.is_valid:
            print("✓ XSD validation PASSED")
            xsd_valid = True
        else:
            print(f"✗ XSD validation FAILED ({len(xsd_result.errors)} errors)")
            for i, error in enumerate(xsd_result.errors[:3], 1):
                print(f"  Error {i}: {error.message[:100]}...")
            xsd_valid = False

    # Step 2: Schematron Validation
    print("\n[2] Schematron Business Rule Validation:")
    print("-" * 70)

    try:
        schematron_validator = SchematronValidator()
        schematron_result = schematron_validator.validate(xml_file)

        if schematron_result.is_valid:
            print("✓ Schematron validation PASSED")
            schematron_valid = True
        else:
            print(f"✗ Schematron validation FAILED ({len(schematron_result.errors)} assertions)")
            for i, error in enumerate(schematron_result.errors[:3], 1):
                print(f"  Assertion {i}: {error.message[:100]}...")
            schematron_valid = False
    except FileNotFoundError:
        print("⚠  Schematron files not found. Skipping Schematron validation.")
        schematron_valid = None

    # Overall Result
    print("\n[3] Overall Validation Result:")
    print("-" * 70)

    if xsd_valid and schematron_valid:
        print("✓ Document is FULLY VALID")
        print("  - Passes XSD schema validation")
        print("  - Passes Schematron business rule validation")
        print("  - Ready for ONC certification or production use")
    elif xsd_valid is False or schematron_valid is False:
        print("✗ Document has VALIDATION ERRORS")
        if xsd_valid is False:
            print("  - XSD validation failed - fix structure first")
        if schematron_valid is False:
            print("  - Schematron validation failed - fix business rules")
    else:
        print("⚠  Could not complete full validation (missing validators)")

    print()


def common_schematron_errors_guide():
    """Guide to common Schematron validation errors and fixes."""
    print("=" * 70)
    print("Common Schematron Validation Errors & Fixes")
    print("=" * 70)
    print()

    errors = [
        {
            "error": "SHALL contain exactly one [1..1] realmCode",
            "cause": "Missing or multiple realmCode elements",
            "fix": 'Add: <realmCode code="US"/>',
            "example": """
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <realmCode code="US"/>  <!-- Required -->
  ...
</ClinicalDocument>
""",
        },
        {
            "error": "SHALL contain exactly one [1..1] typeId",
            "cause": "Missing or incorrect typeId",
            "fix": "Add typeId with root and extension attributes",
            "example": """
<typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
""",
        },
        {
            "error": "templateId SHALL contain exactly one [1..1] @root",
            "cause": "templateId missing root attribute or has wrong structure",
            "fix": "Ensure templateId has root attribute with OID",
            "example": """
<templateId root="2.16.840.1.113883.10.20.22.1.1"/>
<templateId root="2.16.840.1.113883.10.20.22.1.1" extension="2015-08-01"/>
""",
        },
        {
            "error": "effectiveTime SHALL be precise to the day",
            "cause": "effectiveTime value missing or not precise enough",
            "fix": "Use YYYYMMDD format (minimum)",
            "example": """
<!-- Valid formats: -->
<effectiveTime value="20230607"/>           <!-- Day precision -->
<effectiveTime value="20230607120000"/>     <!-- Full precision -->
<effectiveTime value="20230607120000-0500"/> <!-- With timezone -->
""",
        },
        {
            "error": "code SHALL be from LOINC",
            "cause": "Using wrong code system for document type code",
            "fix": "Use LOINC code with correct codeSystem OID",
            "example": """
<code code="34133-9"
      codeSystem="2.16.840.1.113883.6.1"
      codeSystemName="LOINC"
      displayName="Summarization of Episode Note"/>
""",
        },
        {
            "error": "recordTarget/patientRole/patient/name SHALL be present",
            "cause": "Missing required patient name element",
            "fix": "Add patient name with given and family elements",
            "example": """
<patient>
  <name>
    <given>John</given>
    <family>Doe</family>
  </name>
</patient>
""",
        },
        {
            "error": "administrativeGenderCode SHALL be from value set",
            "cause": "Using invalid code for administrative gender",
            "fix": "Use codes from AdministrativeGender value set (M, F, UN)",
            "example": """
<administrativeGenderCode code="M"
                          codeSystem="2.16.840.1.113883.5.1"
                          displayName="Male"/>
""",
        },
        {
            "error": "section SHALL contain exactly one [1..1] code",
            "cause": "Section missing required code element",
            "fix": "Add section code with LOINC code",
            "example": """
<section>
  <code code="11450-4"
        codeSystem="2.16.840.1.113883.6.1"
        displayName="Problem List"/>
  <title>Problems</title>
  <text>...</text>
</section>
""",
        },
    ]

    for i, error in enumerate(errors, 1):
        print(f"{i}. {error['error']}")
        print("-" * 70)
        print(f"Cause: {error['cause']}")
        print(f"Fix:   {error['fix']}")
        print(f"Example:{error['example']}")
        print()


def validate_string_example():
    """Example of validating an XML string with Schematron."""
    print("=" * 70)
    print("Validating XML String with Schematron")
    print("=" * 70)

    # Minimal C-CDA document
    xml_string = """<?xml version="1.0"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <realmCode code="US"/>
  <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.1"/>
  <id root="2.16.840.1.113883.3.3208.101.1" extension="20130607100315"/>
  <code code="34133-9" codeSystem="2.16.840.1.113883.6.1"/>
  <title>Continuity of Care Document</title>
  <effectiveTime value="20130607"/>
  <recordTarget>
    <patientRole>
      <id root="2.16.840.1.113883.3.3208.101.2" extension="Patient1"/>
      <patient>
        <name>
          <given>John</given>
          <family>Doe</family>
        </name>
      </patient>
    </patientRole>
  </recordTarget>
</ClinicalDocument>"""

    try:
        validator = SchematronValidator()
        print("\n[1] Validating minimal C-CDA document...")
        result = validator.validate_string(xml_string)

        print(f"\n[2] Result: {'VALID' if result.is_valid else 'INVALID'}")
        print(f"    Errors: {len(result.errors)}")
        print(f"    Warnings: {len(result.warnings)}")

        if not result.is_valid:
            print("\n[3] First few errors:")
            for i, error in enumerate(result.errors[:3], 1):
                print(f"    {i}. {error.message[:100]}...")
    except FileNotFoundError:
        print("\n⚠  Schematron files not found.")
        print("   See schemas/schematron/README.md for installation.")

    print()


def main():
    """Main example function."""
    print("\n")
    print("=" * 70)
    print("C-CDA Schematron Validation Example")
    print("=" * 70)
    print()

    # Step 1: Check if Schematron files are available
    schematron_available = check_schematron_availability()

    if not schematron_available:
        print_installation_instructions()
        print("⚠  Cannot run Schematron validation examples without files.")
        print("   Please install Schematron files first.")
        print()
        return

    # Step 2: Validate an example document
    example_xml = Path("output_ccda_with_sections.xml")

    if example_xml.exists():
        print(f"Found example document: {example_xml}\n")

        # Example 1: Schematron validation only
        print("[Example 1: Schematron Validation]")
        validate_document_with_schematron(example_xml)

        # Example 2: Combined validation
        print("\n[Example 2: Combined XSD + Schematron Validation]")
        combined_validation_example(example_xml)

    else:
        print(f"⚠  Example XML file not found: {example_xml}")
        print("   Run 'python examples/generate_ccda.py' first to create a document.")
        print()

        # Still show string validation example
        print("[Example: Validate XML String]")
        validate_string_example()

    # Step 3: Common errors guide
    print("\n[Guide: Common Schematron Errors]")
    common_schematron_errors_guide()

    print("=" * 70)
    print("Schematron Validation Tips")
    print("=" * 70)
    print()
    print("1. Always validate with BOTH XSD and Schematron")
    print("   - XSD catches structural errors")
    print("   - Schematron catches business rule violations")
    print()
    print("2. Fix XSD errors first")
    print("   - Structure must be valid before Schematron can run properly")
    print()
    print("3. Schematron validation is SLOW for large documents")
    print("   - Can take several seconds for complex CCDs")
    print("   - Consider caching validation results")
    print()
    print("4. Use specific template IDs for your document type")
    print("   - Different document types have different requirements")
    print("   - See C-CDA Implementation Guide for template IDs")
    print()
    print("5. Check value set bindings carefully")
    print("   - Many codes must come from specific value sets")
    print("   - Refer to VSAC for correct codes")
    print()
    print("For more information, see SCHEMATRON_GUIDE.md")
    print()

    print("=" * 70)
    print("Example Complete")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
