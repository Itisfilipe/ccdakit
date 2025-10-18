# User Guide Overview

Comprehensive guides for using ccdakit effectively.

## Contents

### Core Concepts

- **[HL7/C-CDA Comprehensive Guide](hl7-guide/index.md)** - Complete HL7 and C-CDA primer with detailed section documentation
- **[Working with Sections](sections.md)** - All 29 clinical sections
- **[Protocols](protocols.md)** - Protocol reference and adapting your data
- **[Configuration](configuration.md)** - Global and document configuration
- **[Validation](validation.md)** - XSD and Schematron validation
- **[Terminologies](terminologies.md)** - Code systems and value sets

## Quick Navigation

### Creating Documents

1. Define your data models (or use existing ones)
2. Ensure they satisfy required protocols
3. Create sections from your data
4. Build the clinical document
5. Generate XML output

### Common Tasks

**Add a new section**:
```python
from ccdakit import ProblemsSection, CDAVersion

section = ProblemsSection(
    problems=my_problems,
    version=CDAVersion.R2_1
)
```

**Configure globally**:
```python
from ccdakit import configure, CDAConfig, OrganizationInfo

configure(CDAConfig(
    organization=OrganizationInfo(name="My Clinic", npi="123456789")
))
```

**Validate output**:
```python
from ccdakit.validators import XSDValidator

validator = XSDValidator()
result = validator.validate(xml)
```

## Learning Path

1. Start with [Quick Start](../getting-started/quickstart.md)
2. Understand [Basic Concepts](../getting-started/concepts.md)
3. Read [Working with Sections](sections.md)
4. Review [Examples](../examples/complete-document.md)
5. Explore [API Reference](../api/core.md)
