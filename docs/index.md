# ccdakit

> Python library for generating HL7 C-CDA clinical documents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-1903%20passing-success)](https://github.com/Itisfilipe/ccdakit)
[![Coverage](https://img.shields.io/badge/coverage-94%25-success)](https://github.com/Itisfilipe/ccdakit)

!!! warning "Important Disclaimers"
    **This is an independent, community project and NOT an official HL7 product.**

    - Not affiliated with, endorsed by, or recognized by HL7 International
    - Developed extensively with AI assistance (Claude Code)
    - Requires thorough testing and validation before production use
    - Always consult official HL7 specifications for regulatory compliance

    **For official HL7 resources: [HL7.org](https://www.hl7.org/)**

## Overview

**ccdakit** is a Python library for programmatic generation of HL7 C-CDA (Consolidated Clinical Document Architecture) documents. It provides a type-safe, protocol-oriented, and version-aware approach to creating ONC-compliant clinical documents.

## Why ccdakit?

Existing C-CDA solutions have limitations:

- **Template-based** (Jinja2, XSLT): Hard to validate, verbose context management
- **String manipulation**: Error-prone, no type safety
- **Vendor-specific**: Locked to particular EHR systems
- **No version management**: Can't easily support multiple C-CDA versions

## Key Features

| Feature | Description |
|---------|-------------|
| **Multi-version** | Support C-CDA R2.1, R2.0 |
| **Build-time validation** | XSD/Schematron validation during generation |
| **Protocol-oriented** | No inheritance required, works with any data model |
| **Type-safe** | Full type hints, IDE autocomplete |
| **Composable** | Reusable builders for common elements |
| **Pure Python** | Only dependency: lxml |

## Quick Example

```python
from ccdakit import (
    ClinicalDocument,
    ProblemsSection,
    MedicationsSection,
    CDAVersion,
)

# Your data models automatically work!
doc = ClinicalDocument(
    patient=my_patient,
    sections=[
        ProblemsSection(problems=problems_list, version=CDAVersion.R2_1),
        MedicationsSection(medications=meds_list, version=CDAVersion.R2_1),
    ],
    version=CDAVersion.R2_1,
)

# Generate valid, ONC-compliant C-CDA R2.1 XML
xml = doc.to_string(pretty=True)
```

## Current Status

**Version**: 0.1.0-alpha (MVP Complete)

✅ **29 Complete Clinical Sections**

✅ **1,903 tests, 94% coverage**

✅ **XSD validation support**

## Getting Started

- [Installation](getting-started/installation.md) - Install ccdakit
- [Quick Start](getting-started/quickstart.md) - Create your first document
- [User Guide](guides/overview.md) - Comprehensive documentation
- [API Reference](api/core.md) - Complete API docs

## License

MIT License - see [License](about/license.md) for details.

---

**Disclaimer:** This project is not affiliated with HL7 International. HL7® and C-CDA® are registered trademarks of Health Level Seven International. This is an independent implementation developed with extensive AI assistance. Always validate against official specifications before production use.
