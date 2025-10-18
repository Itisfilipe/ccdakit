# ccdakit

**Python Library for HL7 C-CDA Clinical Document Generation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Tests](https://img.shields.io/badge/tests-1%2C903-brightgreen)](https://github.com/Itisfilipe/ccdakit)
[![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen)](https://github.com/Itisfilipe/ccdakit)

ccdakit is a Python library for programmatic generation of HL7 C-CDA (Consolidated Clinical Document Architecture) documents. Built with type safety, protocol-oriented design, and multi-version support for healthcare interoperability.

```python
from ccdakit import ClinicalDocument, ProblemsSection, CDAVersion

doc = ClinicalDocument(
    patient=patient_data,
    sections=[ProblemsSection(problems=problems_list)],
    version=CDAVersion.R2_1
)

xml = doc.to_string()  # Standards-compliant C-CDA R2.1 XML
```

---

## Why ccdakit?

Existing approaches to C-CDA generation have significant limitations:

| Challenge | ccdakit Solution |
|-----------|------------------|
| Template engines (Jinja, XSLT) are verbose and hard to validate | **Pure Python builders** with full type safety |
| String manipulation is error-prone | **Structured builders** with IDE autocomplete |
| Single version support limits flexibility | **Multi-version support** (R2.1, R2.0) |
| Vendor lock-in to specific EHR systems | **Protocol-based design** works with any data model |
| Manual validation catches errors late | **Built-in XSD validation** at generation time |
| Difficult to compose and reuse logic | **Composable section builders** |

ccdakit provides a modern, Pythonic approach to C-CDA document generation suitable for EHR systems, health information exchanges, and healthcare applications.

---

## Installation

### Standard Installation

```bash
pip install ccdakit
```

### With Optional Dependencies

```bash
# Include validation tools
pip install ccdakit[validation]

# Include development dependencies
pip install ccdakit[dev]

# All extras
pip install ccdakit[dev,validation,docs]
```

### For Contributors

This project uses [uv](https://docs.astral.sh/uv/) for dependency management:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://github.com/Itisfilipe/ccdakit.git
cd ccdakit

# Install dependencies
uv sync --all-extras

# Run test suite
uv run pytest
```

See [Development Setup](./docs/development/setup.md) for complete instructions.

---

## Quick Start

### Basic Document Generation

```python
from ccdakit import ClinicalDocument, ProblemsSection, CDAVersion
from datetime import date

# Define your data model (or use existing models)
class Problem:
    name = "Type 2 Diabetes Mellitus"
    code = "44054006"
    code_system = "SNOMED"
    status = "active"
    onset_date = date(2020, 3, 15)

# Generate C-CDA document
doc = ClinicalDocument(
    patient=patient,
    sections=[ProblemsSection(problems=[Problem()])],
    version=CDAVersion.R2_1
)

# Output XML
xml_string = doc.to_string(pretty=True)
```

### Multiple Sections

```python
from ccdakit import (
    ClinicalDocument,
    ProblemsSection,
    MedicationsSection,
    AllergiesSection,
    VitalSignsSection,
)

doc = ClinicalDocument(
    patient=patient_data,
    author=provider_data,
    custodian=organization_data,
    sections=[
        ProblemsSection(problems=problems_list),
        MedicationsSection(medications=medications_list),
        AllergiesSection(allergies=allergies_list),
        VitalSignsSection(vital_signs_organizers=vitals_list),
    ],
    version=CDAVersion.R2_1
)
```

### Validation

```python
from ccdakit.validators import XSDValidator

validator = XSDValidator()
result = validator.validate(xml_string)

if result.is_valid:
    print("Document is valid")
else:
    for issue in result.issues:
        print(f"Error: {issue.message} (line {issue.line})")
```

**Complete examples:** [examples/generate_ccda.py](./examples/generate_ccda.py)

---

## Key Features

### Comprehensive Section Support

29 complete C-CDA sections organized by clinical purpose:

**Core Clinical Sections (9)**
- Problems, Medications, Allergies, Immunizations, Vital Signs, Procedures, Results, Social History, Encounters

**Extended Clinical Sections (9)**
- Family History, Functional Status, Mental Status, Goals, Health Concerns, Health Status Evaluations, Past Medical History, Physical Exam, Assessment and Plan

**Specialized/Administrative Sections (11)**
- Plan of Treatment, Advance Directives, Medical Equipment, Admission/Discharge Medications, Hospital Discharge Instructions, Payers, Nutrition, Reason for Visit, Chief Complaint, Interventions

See [complete section documentation](./docs/api/sections.md) for details.

### Protocol-Oriented Design

Works with existing data models without inheritance requirements. Uses Python's structural typing (protocols):

```python
from typing import Protocol

# ccdakit defines the interface
class ProblemProtocol(Protocol):
    @property
    def name(self) -> str: ...
    @property
    def code(self) -> str: ...
    @property
    def status(self) -> str: ...

# Your existing models automatically satisfy the protocol
class DatabaseProblem:
    def __init__(self, db_record):
        self._record = db_record

    @property
    def name(self):
        return self._record.diagnosis_name

    @property
    def code(self):
        return self._record.snomed_code

    @property
    def status(self):
        return self._record.status

# Use directly with ccdakit builders
section = ProblemsSection(problems=[DatabaseProblem(record)])
```

### Multi-Version Support

Generate documents for different C-CDA releases:

```python
# C-CDA R2.1 (current standard)
doc_v21 = ClinicalDocument(..., version=CDAVersion.R2_1)

# C-CDA R2.0 (backward compatibility)
doc_v20 = ClinicalDocument(..., version=CDAVersion.R2_0)
```

### Built-in Validation

XSD schema validation integrated into the generation process:

- Official HL7 schemas
- Configurable validation rules
- Detailed error reporting with line numbers
- Schematron support (in development)

### Automatic Narrative Generation

Generates human-readable narrative text alongside structured data:

```python
section = ProblemsSection(problems=problems_list)

# Automatically generates both:
# 1. Structured <entry> elements with coded data
# 2. Narrative <text> element with HTML table
```

---

## Architecture

```
┌──────────────────────────────────────┐
│     Healthcare Application           │
│     (EHR, HIE, Health Platform)      │
└───────────────┬──────────────────────┘
                │ provides data
                ▼
┌──────────────────────────────────────┐
│     ccdakit Protocols                │
│     (Data Contracts)                 │
└───────────────┬──────────────────────┘
                │ implemented by
                ▼
┌──────────────────────────────────────┐
│     Section Builders                 │
│     (Problems, Medications, etc.)    │
└───────────────┬──────────────────────┘
                │ assembled by
                ▼
┌──────────────────────────────────────┐
│     Clinical Document Builder        │
└───────────────┬──────────────────────┘
                │ generates
                ▼
┌──────────────────────────────────────┐
│     Standards-Compliant XML          │
│     (HL7 C-CDA R2.1 / R2.0)         │
└──────────────────────────────────────┘
```

**Design Principles:**

- **Separation of Concerns**: Data models remain independent of generation logic
- **Type Safety**: Full type hints enable static analysis and IDE support
- **Composability**: Build complex documents from reusable components
- **Standards Compliance**: Follows HL7 C-CDA specifications exactly
- **Testability**: Protocol-based design simplifies unit testing

See [Architecture Documentation](./docs/development/architecture.md) for detailed design decisions.

---

## Project Status

**Current Release:** 0.1.0-alpha (MVP Complete)

| Metric | Status |
|--------|--------|
| **Sections** | 29 of 82 C-CDA sections implemented (35%) |
| **Test Suite** | 1,903 comprehensive tests |
| **Code Coverage** | 94% |
| **Documentation** | Complete API reference + 40-page HL7 guide |
| **Validation** | XSD validation complete, Schematron in progress |

### Implementation Status

**Phase 1: MVP** ✓ Complete
- [x] Core infrastructure and protocols
- [x] 29 clinical sections (Core, Extended, Specialized)
- [x] XSD validation framework
- [x] Multi-version support (R2.1, R2.0)
- [x] Comprehensive test coverage
- [x] Complete documentation

**Phase 2: Additional Sections** (In Progress)
- [ ] Care Plan Section
- [ ] Hospital Course Section
- [ ] Admission/Discharge Diagnosis Sections
- [ ] Instructions Section
- [ ] Additional document-specific sections

**Phase 3: Enhanced Validation** (Planned)
- [ ] Schematron validation
- [ ] ONC C-CDA Validator integration
- [ ] Custom validation rules API
- [ ] Performance optimization

**Phase 4: Production Release** (Planned)
- [ ] Plugin architecture
- [ ] CLI tooling
- [ ] Performance benchmarks
- [ ] 1.0 stable release

See [Roadmap](./docs/development/roadmap.md) for detailed plans.

---

## Documentation

Comprehensive documentation is available:

| Resource | Description |
|----------|-------------|
| [Getting Started](./docs/getting-started/quickstart.md) | Installation and first document |
| [HL7/C-CDA Implementation Guide](./docs/guides/hl7-guide/index.md) | 40-page guide to C-CDA standards |
| [API Reference](./docs/api/sections.md) | Complete API documentation |
| [Examples](./examples/) | Working code for all sections |
| [Architecture](./docs/development/architecture.md) | Design decisions and patterns |
| [Contributing](./CONTRIBUTING.md) | Development setup and guidelines |

### HL7/C-CDA Implementation Guide

We've created a comprehensive implementation guide (40 pages) that bridges official HL7 specifications and practical implementation:

- **Foundation** (5 pages): HL7 basics, CDA architecture, templates, code systems
- **Section Guides** (30 pages): Complete documentation for all 29 implemented sections
- **Appendices** (5 pages): OID reference, conformance rules, glossary

This guide complements official HL7 documentation with practical examples and implementation patterns.

[Read the complete guide →](./docs/guides/hl7-guide/index.md)

---

## Use Cases

ccdakit is designed for:

**Electronic Health Records (EHR)**
- Generate discharge summaries, continuity of care documents, referral notes
- Support ONC certification requirements
- Enable standards-based data exchange

**Health Information Exchanges (HIE)**
- Create compliant documents for cross-organization data sharing
- Support multiple C-CDA versions for interoperability
- Validate documents before transmission

**Healthcare Applications**
- Export patient data in C-CDA format
- Integrate with existing health IT systems
- Support FHIR-to-CDA conversion workflows

**Testing and Validation**
- Generate test documents for validator testing
- Create synthetic patient data for QA
- Support conformance testing

**Data Migration**
- Convert legacy formats to C-CDA
- Support system migrations and upgrades
- Enable data preservation

---

## Testing

Comprehensive test suite with 1,903 tests and 94% coverage:

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=ccdakit --cov-report=html

# Run specific test suite
uv run pytest tests/test_builders/

# Parallel execution for speed
uv run pytest -n auto
```

See [Testing Guide](./docs/development/testing.md) for details.

---

## Contributing

Contributions are welcome. Please review our guidelines:

**Before Contributing:**
- Read the [Code of Conduct](./CODE_OF_CONDUCT.md)
- Review [Contributing Guidelines](./CONTRIBUTING.md)
- Check existing [Issues](https://github.com/Itisfilipe/ccdakit/issues)

**Development Setup:**
1. Fork the repository
2. Clone your fork
3. Install dependencies: `uv sync --all-extras`
4. Download C-CDA references (see `references/README.md`)
5. Create a feature branch
6. Make changes with tests
7. Run test suite: `uv run pytest`
8. Submit pull request

See [Development Setup Guide](./docs/development/setup.md) for complete instructions.

---

## Important Disclaimers

**Independent Project**

This is an independent, community-driven project and is NOT an official HL7 product.

- **Not affiliated with HL7 International**: This library is not endorsed by or officially recognized by HL7 International
- **AI-assisted development**: This project was developed extensively with AI assistance (Claude Code)
- **Validation required**: Thoroughly test and validate before production use
- **Not a substitute for official specifications**: Always consult official HL7 documentation for regulatory compliance
- **No warranty**: See [LICENSE](./LICENSE) for details

**For official HL7 resources:** Visit [HL7.org](https://www.hl7.org/)

**Trademarks:** HL7® and C-CDA® are registered trademarks of Health Level Seven International.

---

## Requirements

- Python 3.8 or higher
- lxml >= 4.9.0 (only required dependency)

Optional dependencies for development:
- pytest (testing)
- ruff (linting)
- mkdocs-material (documentation)

---

## License

MIT License - See [LICENSE](./LICENSE) file for details.

---

## Acknowledgments

This project follows the [HL7 C-CDA Release 2.1 Implementation Guide](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=492) and is designed to support [ONC Health IT Certification](https://www.healthit.gov/topic/certification-ehrs/2015-edition-test-method) requirements.

Developed with assistance from [Claude Code](https://claude.com/claude-code).

---

## Support

- **Issues**: [GitHub Issues](https://github.com/Itisfilipe/ccdakit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Itisfilipe/ccdakit/discussions)
- **Documentation**: [Complete Documentation](./docs/index.md)

---

**Current Status:** Alpha release - MVP complete and ready for validation testing. Production use should be preceded by thorough validation against your specific requirements.
