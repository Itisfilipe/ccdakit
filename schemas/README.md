# C-CDA XSD Schemas

This directory contains the XSD schemas for C-CDA validation.

## Automatic Download (Recommended)

**Good news!** XSD schemas are automatically downloaded on first use.

When you use `XSDValidator()`, ccdakit will:
1. Auto-download official HL7 C-CDA XSD schemas (~2MB)
2. Save them to `schemas/` directory
3. Cache them for future use

```bash
# Download schemas via CLI
ccdakit download-schemas --schema-type xsd

# Or let them auto-download on first validation
ccdakit validate document.xml
```

## Manual Download (If Needed)

If you prefer manual installation or need a specific version:

### C-CDA R2.1
- Download from: https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492
- File: `CCDA_R2.1_Schemas.zip`
- Extract `CDA.xsd` and related files to this folder

### C-CDA R2.0
- Download from: https://www.hl7.org/implement/standards/product_brief.cfm?product_id=379
- File: `C-CDA_R2.0_Schemas.zip`

## Directory Structure

After downloading, your structure should look like:

```
schemas/
├── README.md (this file)
├── CDA.xsd                    # Main CDA schema
├── POCD_MT000040_CCDA.xsd     # C-CDA specific constraints
├── datatypes.xsd              # CDA datatypes
├── voc.xsd                    # Vocabulary constraints
├── NarrativeBlock.xsd         # Narrative text schema
└── SDTC/                      # Structured Document Template Content
    └── infrastructureRoot.xsd
```

## Schema Versions

| Version | OID | Release Date |
|---------|-----|--------------|
| R2.1    | 2.16.840.1.113883.10.20.22.1.1 | 2015-08-01 |
| R2.0    | 2.16.840.1.113883.10.20.22.1.1 | 2014-06-09 |
| R1.1    | 2.16.840.1.113883.10.20.22.1.1 | 2012-01-01 |

## Environment Variable Configuration

For production deployments or custom locations, use the `CCDAKIT_SCHEMA_DIR` environment variable:

```bash
# Set custom schema location
export CCDAKIT_SCHEMA_DIR=/app/data/schemas

# Schemas will be downloaded to or loaded from this location
ccdakit validate document.xml
```

This is particularly useful for:
- **Production environments** (Render, Heroku, AWS) with read-only filesystems
- **Docker containers** with mounted volumes
- **Shared environments** where schemas should be in a common location

## License Note

The HL7 schemas are copyrighted by Health Level Seven International (HL7).
Please review HL7's licensing terms before redistributing these schemas.

For this reason, we do **not include the schemas in the repository**.
They are automatically downloaded during:
- First use (auto-download)
- Build time (CI/CD, deployment)
- Manual installation (`ccdakit download-schemas`)

## Validation

XSD validation with auto-download:

```python
from ccdakit.validators import XSDValidator

# Schemas auto-download on first use
validator = XSDValidator()
result = validator.validate("document.xml")

if result.is_valid:
    print("✓ Valid C-CDA document")
else:
    for error in result.errors:
        print(f"Error: {error.message}")
```

Or via CLI:

```bash
# Auto-downloads schemas if needed
ccdakit validate document.xml
```

## Schematron Files

**Good news!** Schematron files are automatically downloaded and cleaned on first use.

When you initialize `SchematronValidator()`, ccdakit will:
1. Auto-download official HL7 C-CDA R2.1 Schematron files (~63MB)
2. Auto-clean them to fix IDREF errors (required for lxml compatibility)
3. Save both original and cleaned versions to `schemas/schematron/`

The official HL7 Schematron file contains invalid pattern references that prevent lxml from loading it. ccdakit automatically cleans these files during download, removing ~60 invalid references while preserving all validation rules.

See `schemas/schematron/README.md` for detailed information about the cleaning process.

**Alternative sources** (if manual download needed):
- Official HL7: https://github.com/HL7/CDA-ccda-2.1
- ONC C-CDA Validator: https://github.com/onc-healthit/ccda-schematron
- MDHT Project: https://github.com/mdht/mdht-models
