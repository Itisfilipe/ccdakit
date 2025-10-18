# Changelog

All notable changes to ccdakit will be documented here.

## [0.1.0-alpha] - 2024

### Added - MVP Complete

**Core Features**:
- Protocol-oriented design system
- Multi-version support (C-CDA R2.1, R2.0)
- Global configuration management
- Type-safe implementation with full type hints

**29 Complete Clinical Sections**:

*Core Sections (9)*:
- Problems Section (SNOMED/ICD-10 codes)
- Medications Section (RxNorm codes)
- Allergies Section (RxNorm/UNII/SNOMED codes)
- Immunizations Section (CVX codes)
- Vital Signs Section (LOINC codes with organizers)
- Procedures Section (CPT/SNOMED codes)
- Results/Labs Section (LOINC codes with panels)
- Social History Section (smoking status)
- Encounters Section

*Extended Sections (9)*:
- Family History Section
- Functional Status Section
- Medical Equipment Section
- Payers Section
- Plan of Treatment Section
- Instructions Section
- Health Concerns Section
- Goals Section
- Advance Directives Section

*Specialized Sections (11)*:
- Mental Status Section
- Nutrition Section
- Assessment Section
- Assessment and Plan Section
- Care Team Section
- Chief Complaint Section
- Chief Complaint and Reason for Visit Section
- General Status Section
- History of Present Illness Section
- Physical Exam Section
- Reason for Visit Section

**Validation**:
- XSD schema validation
- Schematron validation framework with auto-download and cleaning
  - Automatic download of official HL7 C-CDA R2.1 Schematron files
  - Automatic cleaning to fix IDREF errors (lxml compatibility)
  - Removes ~60 invalid pattern references while preserving all validation rules
  - Creates both original and cleaned versions for transparency
- Custom validation rules
- Common validation rule library

**Utilities**:
- Code system registry (SNOMED, LOINC, RxNorm, etc.)
- Value set registry with validation
- Test data generator with Faker
- Simple builder API
- Dictionary to CDA converter
- Template system

**Development**:
- 1,903 comprehensive tests
- 94% code coverage
- Ruff for linting
- Pyright for type checking
- pytest with parallel execution
- Complete documentation site

**Documentation**:
- MkDocs Material documentation
- API reference with mkdocstrings
- User guides and tutorials
- Examples and recipes
- Contributing guide

## Roadmap

### [0.2.0] - Planned

- Additional sections (Care Plan, Immunization Refusal Reason)
- Enhanced Schematron support
- ONC C-CDA Validator integration
- Performance optimizations

### [1.0.0] - Future

- Plugin system for custom sections
- Bulk generation utilities
- Complete API stability
- Production-ready release

## Links

- **Repository**: https://github.com/Itisfilipe/ccdakit
- **Documentation**: https://Itisfilipe.github.io/ccdakit
- **Issues**: https://github.com/Itisfilipe/ccdakit/issues
