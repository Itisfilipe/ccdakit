# C-CDA XSD Schemas

This directory contains the XSD schemas for C-CDA validation.

## Obtaining Schemas

The C-CDA XSD schemas are available from HL7:

### C-CDA R2.1
- Download from: https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492
- File: `CCDA_R2.1_Schemas.zip`
- Extract `CDA.xsd` and the `SDTC/` directory to this folder

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

## License Note

The HL7 schemas are copyrighted by Health Level Seven International (HL7).
Please review HL7's licensing terms before redistributing these schemas.

For this reason, we do not include the schemas in the repository by default.
Users must download them separately.

## Validation

To use XSD validation in ccdakit:

```python
from ccdakit import CDAConfig, configure
from ccdakit.validators import XSDValidator

config = CDAConfig(
    # ... your config
    xsd_schema_path="/path/to/schemas/CDA.xsd",
    validate_on_build=True,
)
configure(config)
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
