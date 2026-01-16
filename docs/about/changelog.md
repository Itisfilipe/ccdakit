# Changelog

All notable changes to ccdakit will be documented here.

## [0.1.0-alpha] - 2025-10-23

### Added - Hospital & Surgical Sections (October 2025)

**10 New Sections** for discharge summaries, operative notes, and hospital workflows:

1. **Admission Diagnosis Section** (2.16.840.1.113883.10.20.22.2.43)
   - Documents patient diagnoses at time of admission
   - Supports problem observations with SNOMED/ICD codes
   - Includes effective times and status tracking
   - 35 tests with 100% coverage

2. **Discharge Diagnosis Section** (2.16.840.1.113883.10.20.22.2.24)
   - Final diagnoses at hospital discharge
   - Full problem observation support
   - Narrative table generation
   - 35 tests with 100% coverage

3. **Hospital Course Section** (1.3.6.1.4.1.19376.1.5.3.1.3.5)
   - Narrative description of entire hospital stay
   - Key events and interventions
   - Patient progress over time
   - 34 tests with 100% coverage

4. **Instructions Section** (2.16.840.1.113883.10.20.22.2.45)
   - Patient care instructions
   - Discharge instructions
   - Follow-up guidance
   - 33 tests with 100% coverage

5. **Anesthesia Section** (2.16.840.1.113883.10.20.22.2.25)
   - Anesthesia type and details for procedures
   - Medications and dosages
   - Monitoring data
   - 29 tests with 100% coverage

6. **Postoperative Diagnosis Section** (2.16.840.1.113883.10.20.22.2.35)
   - Diagnoses determined after surgical procedure
   - Links to operative findings
   - Problem observation entries
   - 28 tests with 100% coverage

7. **Preoperative Diagnosis Section** (2.16.840.1.113883.10.20.22.2.34)
   - Diagnoses before surgical procedure
   - Reason for surgery
   - Problem observation entries
   - 27 tests with 100% coverage

8. **Complications Section** (2.16.840.1.113883.10.20.22.2.37)
   - Procedure and hospital complications
   - Problem observations for complications
   - Severity and outcomes
   - 31 tests with 100% coverage

9. **Hospital Discharge Studies Summary Section** (2.16.840.1.113883.10.20.22.2.16)
   - Diagnostic studies performed before discharge
   - Results and interpretations
   - Pending studies
   - 32 tests with 100% coverage

10. **Medications Administered Section** (2.16.840.1.113883.10.20.22.2.38)
    - Medications given during hospitalization/encounter
    - Administration times and routes
    - Dosage information
    - 35 tests with 100% coverage

**Total Impact**:
- 319 new tests added (100% coverage)
- All sections support both R2.1 and R2.0
- Full narrative HTML table generation
- Comprehensive protocol definitions

### Added - MVP Complete (Initial Release)

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
- Health Concerns Section
- Goals Section
- Advance Directives Section
- Mental Status Section

*Specialized Sections (11)*:
- Assessment and Plan Section
- Chief Complaint and Reason for Visit Section
- Reason for Visit Section
- Nutrition Section
- Past Medical History Section
- Physical Exam Section
- Hospital Discharge Instructions Section
- Admission Medications Section
- Discharge Medications Section
- Health Status Evaluations and Outcomes Section
- Interventions Section

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
- 3,825 comprehensive tests
- 28% code coverage
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
