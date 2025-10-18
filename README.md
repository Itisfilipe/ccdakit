# ccdakit

> Python library for generating HL7 C-CDA clinical documents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

---

## ⚠️ Important Disclaimers

**This is an independent, community-driven project and is NOT an official HL7 product.**

- This library is not affiliated with, endorsed by, or officially recognized by HL7 International
- This project was developed extensively with AI assistance (Claude Code)
- While we strive for accuracy and standards compliance, this software should be thoroughly tested and validated before production use
- Always consult official HL7 specifications and perform independent validation for regulatory compliance
- Use at your own risk - see [LICENSE](LICENSE) for details

**For official HL7 resources, visit [HL7.org](https://www.hl7.org/)**

---

## Overview

**ccdakit** is a Python library for programmatic generation of HL7 C-CDA (Consolidated Clinical Document Architecture) documents. It provides a type-safe, protocol-oriented, and version-aware approach to creating ONC-compliant clinical documents.

### Why ccdakit?

Existing C-CDA solutions have limitations:
- **Template-based** (Jinja2, XSLT): Hard to validate, verbose context management
- **String manipulation**: Error-prone, no type safety
- **Vendor-specific**: Locked to particular EHR systems
- **No version management**: Can't easily support multiple C-CDA versions

### Key Features

| Feature | Description |
|---------|-------------|
| **Multi-version** | Support C-CDA R2.1, R2.0 |
| **Build-time validation** | XSD/Schematron validation during generation |
| **Protocol-oriented** | No inheritance required, works with any data model |
| **Type-safe** | Full type hints, IDE autocomplete |
| **Composable** | Reusable builders for common elements |
| **Pure Python** | Only dependency: lxml |

## Installation

### For Users

```bash
# Using pip
pip install ccdakit

# With all extras
pip install ccdakit[dev,docs,validation]
```

### For Contributors (Recommended: uv)

This project uses [uv](https://docs.astral.sh/uv/) for fast package management (10-100x faster than pip):

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup project
git clone <repository>
cd ccdakit

# Install dependencies (creates .venv automatically)
uv sync --all-extras

# Download C-CDA 2.1 references (required for development)
cd references/
git clone https://github.com/jddamore/ccda-search.git C-CDA_2.1
cd ..

# Run tests
uv run pytest
```

> **⚠️ Important for Contributors**: The C-CDA 2.1 reference documentation is not included in the repository. You must download it separately (see `references/README.md` for details). This reference is essential for implementing new sections correctly.

See [UV Guide](./docs/development/uv-guide.md) for complete uv usage guide.

## Quick Start

### Basic Example

```python
from ccdakit import (
    configure,
    CDAConfig,
    OrganizationInfo,
    CDAVersion,
    ClinicalDocument,
    ProblemsSection,
    MedicationsSection,
)
from datetime import date

# 1. Configure the library (optional, uses defaults otherwise)
config = CDAConfig(
    organization=OrganizationInfo(
        name="Example Medical Center",
        npi="1234567890",
        oid_root="2.16.840.1.113883.3.EXAMPLE",
    ),
    version=CDAVersion.R2_1,
)
configure(config)

# 2. Create data objects that satisfy protocols
# Your existing data models work automatically!
class MyPatient:
    @property
    def first_name(self):
        return "John"

    @property
    def last_name(self):
        return "Doe"

    @property
    def date_of_birth(self):
        return date(1970, 1, 1)

    @property
    def sex(self):
        return "M"

    # ... implement other required properties

class MyProblem:
    @property
    def name(self):
        return "Type 2 Diabetes Mellitus"

    @property
    def code(self):
        return "44054006"

    @property
    def code_system(self):
        return "SNOMED"

    @property
    def status(self):
        return "active"

    @property
    def onset_date(self):
        return date(2020, 3, 15)

# 3. Generate complete C-CDA document
patient = MyPatient()
problems = [MyProblem()]

doc = ClinicalDocument(
    patient=patient,
    sections=[
        ProblemsSection(problems=problems, version=CDAVersion.R2_1),
        # Add more sections as needed
    ],
    version=CDAVersion.R2_1,
)

# 4. Output formatted XML
xml = doc.to_string(pretty=True)
print(xml)

# 5. Save to file
with open("patient_ccda.xml", "w") as f:
    f.write(xml)
```

### Comprehensive Example with Multiple Sections

```python
from ccdakit import (
    ClinicalDocument,
    ProblemsSection,
    MedicationsSection,
    AllergiesSection,
    ImmunizationsSection,
    VitalSignsSection,
    CDAVersion,
)

# Create sections with your data
doc = ClinicalDocument(
    patient=patient_data,
    author=author_data,
    custodian=custodian_data,
    sections=[
        ProblemsSection(problems=problems_list, version=CDAVersion.R2_1),
        MedicationsSection(medications=meds_list, version=CDAVersion.R2_1),
        AllergiesSection(allergies=allergies_list, version=CDAVersion.R2_1),
        ImmunizationsSection(immunizations=immunizations_list, version=CDAVersion.R2_1),
        VitalSignsSection(organizers=vitals_organizers, version=CDAVersion.R2_1),
    ],
    version=CDAVersion.R2_1,
)

# Generate valid, ONC-compliant C-CDA R2.1 document
xml = doc.to_string(pretty=True)
```

### Validation Example

```python
from ccdakit.validators import XSDValidator, SchemaManager

# Check if schemas are installed
manager = SchemaManager()
if not manager.schemas_installed():
    print("Schemas not found. Download from: http://www.hl7.org/...")

# Validate your document
validator = XSDValidator()
result = validator.validate(xml)

if result.is_valid:
    print("✅ Document is valid!")
else:
    print("❌ Validation errors:")
    for issue in result.issues:
        print(f"  - {issue.message}")
```

**See [examples/generate_ccda.py](./examples/generate_ccda.py) for a complete working example with all sections.**

## Architecture

ccdakit uses a protocol-oriented design that separates data contracts from implementation:

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Application                          │
│              (EHR, HIE, Health App, etc.)                   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │    Your Data Models (adapt via protocols)           │    │
│  └────────────────────────────────────────────────────┘    │
└────────────────────────┬─────────────────────────────────────┘
                         │ Implements Protocols
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    ccdakit Library                            │
│                                                              │
│  Protocols → Builders → Validators → XML Output             │
└─────────────────────────────────────────────────────────────┘
```

### Protocol-Oriented Design

No inheritance required! Just implement the properties:

```python
from typing import Protocol
from datetime import date

# ccdakit defines protocols (interfaces)
class ProblemProtocol(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def code(self) -> str: ...

    @property
    def status(self) -> str: ...

# Your class automatically satisfies the protocol
class MyProblem:
    def __init__(self, data: dict):
        self._data = data

    @property
    def name(self) -> str:
        return self._data['problem_name']

    @property
    def code(self) -> str:
        return self._data['snomed_code']

    @property
    def status(self) -> str:
        return self._data['active_status']

# Works with ccdakit builders without any changes!
```

## Development Status

**Current Version**: 0.1.0-alpha (MVP Complete)

This project has reached **MVP completion** with comprehensive features ready for validation:

- ✅ Core architecture (base classes, protocols)
- ✅ Configuration system
- ✅ Version management (R2.1, R2.0)
- ✅ **29 Complete Clinical Sections**:

  *Core Clinical Sections (9)*:
  - ✅ Problems Section (SNOMED/ICD-10 codes)
  - ✅ Medications Section (RxNorm codes)
  - ✅ Allergies Section (RxNorm/UNII/SNOMED CT codes)
  - ✅ Immunizations Section (CVX codes)
  - ✅ Vital Signs Section (LOINC codes with organizer support)
  - ✅ Procedures Section (CPT/SNOMED codes)
  - ✅ Results Section (LOINC codes with panels)
  - ✅ Social History Section (Smoking status, etc.)
  - ✅ Encounters Section

  *Extended Clinical Sections (9)*:
  - ✅ Family History Section
  - ✅ Functional Status Section
  - ✅ Mental Status Section
  - ✅ Goals Section
  - ✅ Health Concerns Section
  - ✅ Health Status Evaluations and Outcomes Section
  - ✅ Past Medical History Section
  - ✅ Physical Exam Section
  - ✅ Assessment and Plan Section

  *Specialized/Administrative Sections (11)*:
  - ✅ Plan of Treatment Section
  - ✅ Advance Directives Section
  - ✅ Medical Equipment Section
  - ✅ Admission Medications Section
  - ✅ Discharge Medications Section
  - ✅ Hospital Discharge Instructions Section
  - ✅ Payers Section
  - ✅ Nutrition Section
  - ✅ Reason for Visit Section
  - ✅ Chief Complaint and Reason for Visit Section
  - ✅ Interventions Section
- ✅ **XSD Schema Validation** (official HL7 schemas)
- ✅ **1,903 tests, 94% Coverage**
- ✅ Complete narrative HTML table generation

**Testing & Quality**:
- 1,903 comprehensive tests across all modules
- 94% code coverage
- Type-safe with full type hints
- Parallel test execution with pytest-xdist

See [Architecture](./docs/development/architecture.md) for detailed design documentation and [roadmap](./docs/development/roadmap.md) for future plans.

## Roadmap

### Phase 1: MVP ✅ COMPLETE
- [x] Core infrastructure
- [x] Protocol system
- [x] 29 Clinical sections across Core, Extended, and Specialized categories
- [x] XSD validation
- [x] Comprehensive documentation
- [x] 1,903 tests, 94% coverage

### Phase 2: Additional Features & Sections (Next)
- [ ] Care Plan Section
- [ ] Hospital Course Section
- [ ] Admission Diagnosis Section
- [ ] Discharge Diagnosis Section
- [ ] Instructions Section

### Phase 3: Enhanced Validation & Tools
- [ ] Schematron validation (in progress)
- [ ] ONC C-CDA Validator integration
- [ ] CLI tool for document generation
- [ ] Performance optimization
- [ ] Fluent builder API enhancements

### Phase 4: Production Ready (1.0)
- [ ] Plugin system for custom sections
- [ ] Bulk generation utilities
- [ ] Complete API documentation
- [ ] Performance benchmarks
- [ ] 1.0 release

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

This is an open-source project under the MIT license. We follow the [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md).

## Requirements

- Python 3.8+
- lxml >= 4.9.0

## License

MIT License - see [LICENSE](./LICENSE) file for details.

## Acknowledgments

- Built following [HL7 C-CDA R2.1 Implementation Guide](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=492)
- Designed for [ONC Certification](https://www.healthit.gov/topic/certification-ehrs/2015-edition-test-method) compliance
- Developed extensively with AI assistance using [Claude Code](https://claude.com/claude-code)

## Disclaimer

**This project is not affiliated with HL7 International.** HL7® and C-CDA® are registered trademarks of Health Level Seven International. This is an independent implementation created to help developers work with C-CDA standards. This software was developed extensively with AI assistance and should be thoroughly validated before any production use. Always refer to official HL7 specifications for authoritative guidance.

## Support

- **Issues**: [GitHub Issues](https://github.com/Itisfilipe/ccdakit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Itisfilipe/ccdakit/discussions)
- **Documentation**: [Read the Docs](https://ccdakit.readthedocs.io)
- **HL7 Guide**: Complete primer on HL7 and C-CDA standards

---

**Status**: Alpha MVP Complete - Ready for validation and testing. Production use should await additional validation and review.
