# C-CDA Schematron Files

This directory contains Schematron validation files for C-CDA document validation.

## Files

### HL7_CCDA_R2.1.sch
- **Source**: [HL7 CDA-ccda-2.1 GitHub Repository](https://github.com/HL7/CDA-ccda-2.1)
- **Original Name**: Consolidated CDA Templates for Clinical Notes (US Realm) DSTU R2.1.sch
- **Version**: R2.1 (Generated from Trifolia on 9/2/2022)
- **Last Updated**: 09/08/2025
- **Size**: ~987 KB
- **Description**: Official HL7 C-CDA R2.1 Schematron rules for validating Consolidated CDA documents

### voc.xml
- **Source**: [HL7 CDA-ccda-2.1 GitHub Repository](https://github.com/HL7/CDA-ccda-2.1)
- **Size**: ~62 MB
- **Description**: Vocabulary file required for Schematron validation. Contains value set definitions and code system mappings used by the Schematron rules.

## Recent Updates (from HL7_CCDA_R2.1.sch)

- **09/08/2025**: Remove C-CDA 1.1 backwards compatibility requirement (Jira: CDA-21381)
- **09/08/2025**: Remove AdvanceDirective high time nullFlavor fixed value (Jira: CDA-21398)
- **08/21/2025**: Update every extension-less templateId requirements (Jira: CDA-21367)
- **07/30/2025**: Update Vital Signs Organizer to allow LOINC-only when only 2.1 templateId is present (Jira: CDA-21374)
- **07/25/2025**: Fix MedicationActivity effectiveTime rule (Jira: CDA-21382)
- **07/25/2025**: Allow nullFlavor on CONF:81-10127 (Jira: CDA-20445)
- **07/25/2025**: Require CD on CONF:1098-28042 (Jira: CDA-20068)
- **03/21/2024**: Allow nullFlavor on CONF:1098-7508 (Jira: CDA-20881)

## Automatic Download

**Good news!** You don't need to manually download these files anymore.

Starting with ccdakit v0.1.0, Schematron files are automatically downloaded on first use:

```python
from ccdakit.validators import SchematronValidator

# Files are automatically downloaded on first use (one-time, ~63MB)
validator = SchematronValidator()  # Auto-downloads if not present

# Validate a document
result = validator.validate(document)

if result.is_valid:
    print("✓ Document passes Schematron validation!")
else:
    print(f"✗ Found {len(result.errors)} validation errors:")
    for error in result.errors:
        print(f"  - {error}")
```

## Manual Download (Optional)

If you prefer to download manually or automatic download fails, you can:

### Option 1: Use the download utility

```python
from ccdakit.validators import download_schematron_files

# Download files manually
if download_schematron_files():
    print("✓ Schematron files ready!")
```

### Option 2: Provide your own files

```python
from ccdakit.validators import SchematronValidator

# Use your own Schematron file
validator = SchematronValidator(
    schematron_path="/path/to/your/custom.sch",
    auto_download=False  # Disable automatic download
)
```

## What is Schematron?

Schematron is a rule-based validation language for XML documents. Unlike XSD which validates document structure, Schematron validates:

- **Business rules**: Logic constraints (e.g., "if medication is active, it must have a start date")
- **Template conformance**: C-CDA template requirements (e.g., required sections, template IDs)
- **Code system validation**: Verification of codes against value sets
- **Cross-reference validation**: Relationships between different parts of the document

## Known Limitations

### lxml Compatibility Issue

⚠️ **Important**: The official HL7 C-CDA R2.1 Schematron file (`HL7_CCDA_R2.1.sch`) has structural issues that prevent it from being loaded by lxml's strict ISO Schematron parser:

- Missing "warnings" phase patterns (file only defines "errors" phase)
- Contains invalid pattern references (IDREF attributes pointing to non-existent IDs)
- Does not conform to strict ISO Schematron schema validation

**Impact**: While the Schematron validator in ccdakit works perfectly with custom/simple Schematron files, it cannot currently load the official HL7 file due to lxml's strict validation.

**Alternatives**:
1. **XSD Validation** (Recommended): Use `XSDValidator` for structure and data type validation - this works perfectly and covers most validation needs
2. **Custom Schematron**: Create simplified Schematron rules for your specific needs
3. **External Tools**: Use ONC's C-CDA Validator or other Java-based Schematron processors

**Future Work**: We're investigating:
- Pre-processing the HL7 Schematron to fix structural issues
- Using XSLT-based Schematron validation (more permissive)
- Integration with external validation services

## ONC Certification

The C-CDA R2.1 Schematron rules are required for ONC (Office of the National Coordinator for Health IT) certification. Passing Schematron validation is a key requirement for certified EHR systems.

**Note**: For ONC certification, you should use the official ONC C-CDA Validator tool or Java-based Schematron processors alongside ccdakit's XSD validation.

## License

These files are provided "as is" by HL7 and Lantana Consulting Group LLC. See the license text in the Schematron file for full terms.

## References

- [HL7 C-CDA R2.1 GitHub Repository](https://github.com/HL7/CDA-ccda-2.1)
- [HL7 C-CDA Implementation Guide](https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492)
- [Schematron Documentation](http://schematron.com/)
- [ISO Schematron Standard](https://www.iso.org/standard/55982.html)

## Updating Files

To update to the latest version:

```bash
cd schemas/schematron

# Download latest Schematron file
curl -L -o "HL7_CCDA_R2.1.sch" \
  "https://raw.githubusercontent.com/HL7/CDA-ccda-2.1/master/validation/Consolidated%20CDA%20Templates%20for%20Clinical%20Notes%20%28US%20Realm%29%20DSTU%20R2.1.sch"

# Download latest vocabulary file
curl -L -o "voc.xml" \
  "https://raw.githubusercontent.com/HL7/CDA-ccda-2.1/master/validation/voc.xml"
```

Check the [releases page](https://github.com/HL7/CDA-ccda-2.1/releases) for the latest version information.
