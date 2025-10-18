# Roadmap

Future development plans for ccdakit.

**Last Updated**: 2025-10-18
**Current Version**: v0.1.0-alpha

---

## Current Status

### ✅ Phase 1: MVP Complete

**Accomplishments**:
- ✅ Core infrastructure (builders, protocols, validation)
- ✅ **29 C-CDA sections implemented** (35.4% of all 82 C-CDA sections)
- ✅ **Document-level builders**: ContinuityOfCareDocument (CCD), DischargeSummary
- ✅ XSD validation support
- ✅ Schematron validator (works with custom schemas; HL7 official file has compatibility issues)
- ✅ Protocol-oriented design (no inheritance required)
- ✅ Multi-version support (R2.0, R2.1)
- ✅ **1,903 tests passing** with **94% code coverage**
- ✅ Comprehensive documentation site
- ✅ Utility modules (factories, converters, value sets, test data generators)
- ✅ Custom validation rules engine

**Implemented Sections**:

*Core Clinical Sections (9)*:
- Problems Section
- Medications Section
- Allergies Section
- Immunizations Section
- Vital Signs Section
- Procedures Section
- Results Section
- Social History Section
- Encounters Section

*Extended Clinical Sections (9)*:
- Family History Section
- Functional Status Section
- Mental Status Section
- Goals Section
- Health Concerns Section
- Health Status Evaluations and Outcomes Section
- Past Medical History Section
- Physical Exam Section
- Assessment and Plan Section

*Specialized/Administrative Sections (11)*:
- Plan of Treatment Section
- Advance Directives Section
- Medical Equipment Section
- Admission Medications Section
- Discharge Medications Section
- Hospital Discharge Instructions Section
- Payers Section
- Nutrition Section
- Reason for Visit Section
- Chief Complaint and Reason for Visit Section
- Interventions Section

### Known Gaps & Limitations

**Validation**:
- Schematron validation implementation complete, but official HL7 C-CDA R2.1 Schematron file is incompatible with lxml's strict ISO Schematron parser
  - Works perfectly with custom/simple Schematron files
  - Recommend using XSD validation (fully functional) or external ONC validator for production
  - See `schemas/schematron/README.md` for details and alternatives

**Missing Sections** (53 remaining sections - not critical for most use cases):
- Care Team, Immunization Recommendation, Transfer Summary, etc.
- Most commonly used sections are already implemented

**Technical Debt** (Low priority):
- Some **kwargs type annotations need cleanup
- Minor pyright warnings in test files
- Could benefit from more inline documentation

---

## Release Planning

### Immediate (Pre-Release v0.1.0)

**Target**: December 2024

- [ ] PyPI Publishing
  - [ ] Finalize package metadata
  - [ ] Test build process
  - [ ] Test upload to TestPyPI
  - [ ] Publish to PyPI
  - [ ] Verify installation works
- [ ] GitHub Actions
  - [ ] Set up CI/CD for tests
  - [ ] Set up automatic docs deployment
  - [ ] Add coverage reporting
- [ ] Release Tasks
  - [ ] Create git tag v0.1.0
  - [ ] Create GitHub Release with changelog
  - [ ] Add badges to README (build, coverage, PyPI)
  - [ ] Write announcement blog post

### Phase 2: Additional Sections & Features

**Target**: Q1 2025

**Priority Sections** (based on common use cases):
- [ ] Care Plan Section
- [ ] Hospital Course Section
- [ ] Admission Diagnosis Section
- [ ] Discharge Diagnosis Section
- [ ] Instructions Section (general)

**Enhanced Features**:
- [ ] Fluent builder API improvements
- [ ] Better error messages with context
- [ ] Performance optimizations for bulk generation
- [ ] Memory usage optimization for large documents
- [ ] Document validation report generator

**Documentation**:
- [ ] Video tutorials for common workflows
- [ ] Interactive examples in docs
- [ ] Real-world integration examples
- [ ] Migration guide from other libraries

---

## Phase 3: Enhanced Validation & Tools

**Target**: Q2 2025

### Validation Enhancements
- [ ] ONC C-CDA Validator integration (API wrapper)
- [ ] Validation profiles (strict/lenient modes)
- [ ] Batch validation utilities
- [ ] Validation report formatting (HTML, PDF)
- [ ] Pre-processing tool for HL7 Schematron files (fix compatibility issues)

### Developer Tools
- [ ] CLI tool for document generation
- [ ] Document comparison/diff tool
- [ ] Migration utilities (R2.0 → R2.1 converter)
- [ ] Template generator (create custom templates)
- [ ] Code system lookup CLI

### Performance & Optimization
- [ ] Streaming XML generation for large documents
- [ ] Batch generation utilities (process 100s of documents)
- [ ] Memory-efficient builders
- [ ] Performance benchmarking suite
- [ ] Profiling tools and optimization guide

---

## Phase 4: Production Ready (1.0)

**Target**: Q3 2025

### Features
- [ ] Plugin system for custom sections
- [ ] Event hooks system (pre/post build callbacks)
- [ ] Document templates library (common document types)
- [ ] Advanced narrative generation (ML-based?)
- [ ] Multi-format output (JSON, YAML in addition to XML)

### Quality & Security
- [ ] Achieve 100% code coverage
- [ ] Security audit (OWASP, dependency scanning)
- [ ] Load testing (1000s of documents)
- [ ] Thread safety verification
- [ ] Input sanitization hardening

### Documentation
- [ ] Complete API reference for all modules
- [ ] Video tutorial series
- [ ] Interactive documentation with live examples
- [ ] Migration guides from competing libraries
- [ ] Troubleshooting guide

### Release 1.0
- [ ] API stability guarantee
- [ ] Semantic versioning commitment
- [ ] Long-term support (LTS) plan
- [ ] Deprecation policy
- [ ] 1.0.0 release

---

## Beyond 1.0 (Future Ideas)

### Integration & Ecosystem
- [ ] HL7 FHIR conversion utilities (C-CDA ↔ FHIR)
- [ ] FastAPI integration helpers
- [ ] Django ORM support/adapters
- [ ] SQLAlchemy model helpers
- [ ] Pydantic model integration

### Advanced Features
- [ ] AI-powered narrative generation
- [ ] Automatic code mapping (SNOMED → ICD-10, etc.)
- [ ] Multi-language support (i18n)
- [ ] Cloud-native deployment helpers (AWS, GCP, Azure)
- [ ] Document signing/encryption support

### Community & Growth
- [ ] Plugin marketplace
- [ ] Community templates repository
- [ ] Certification program for plugins
- [ ] Regular webinars/workshops
- [ ] Annual conference or summit

---

## Community & Contributions

### Get Involved

We welcome contributions! Here's how to help:

- **Report issues**: [GitHub Issues](https://github.com/Itisfilipe/ccdakit/issues)
- **Request features**: [GitHub Discussions](https://github.com/Itisfilipe/ccdakit/discussions)
- **Contribute code**: See [Contributing Guide](contributing.md)
- **Good first issues**: [Beginner-friendly tasks](https://github.com/Itisfilipe/ccdakit/labels/good%20first%20issue)

### Roadmap Discussion

Vote on features and suggest new ideas:
- [Roadmap Discussion Forum](https://github.com/Itisfilipe/ccdakit/discussions/categories/roadmap)

---

## Success Metrics

We track these metrics to measure project health:

- **Test Coverage**: Target 95%+ (Current: 94%)
- **Section Coverage**: Target 50+ sections (Current: 29/82 = 35.4%)
- **Downloads**: Target 1,000+ monthly (PyPI)
- **GitHub Stars**: Target 500+ (Current: 0 - not yet public)
- **Contributors**: Target 10+ active contributors
- **Issues Response Time**: Target < 48 hours
- **Documentation**: Target 100% API coverage

---

## Versioning Strategy

- **v0.x.x**: Alpha/Beta releases (current)
- **v1.0.0**: First stable release with API guarantee
- **v1.x.x**: Backward-compatible feature additions
- **v2.0.0**: Major version for breaking API changes (if ever needed)

We follow [Semantic Versioning](https://semver.org/).

---

**Questions?** Open a [discussion](https://github.com/Itisfilipe/ccdakit/discussions) or [issue](https://github.com/Itisfilipe/ccdakit/issues).
