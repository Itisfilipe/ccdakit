# Basic Concepts

## Protocol-Oriented Design

ccdakit uses Python's Protocol types for structural subtyping. Your existing data models work automatically - no inheritance required.

```python
from typing import Protocol

# ccdakit protocol
class ProblemProtocol(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def code(self) -> str: ...

    @property
    def status(self) -> str: ...

# Your class automatically satisfies it
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
```

## Architecture

```
Your Application (EHR, HIE, etc.)
         ↓
Your Data Models (implement protocols)
         ↓
ccdakit Library (Protocols → Builders → Validators → XML)
```

## CDA Versions

```python
from ccdakit import CDAVersion

CDAVersion.R2_1  # C-CDA R2.1 (2015) - recommended
CDAVersion.R2_0  # C-CDA R2.0 (2014)
```

## Clinical Sections

39 complete sections available (9 core sections shown below, see guides/sections.md for all):

- ProblemsSection (SNOMED, ICD-10)
- MedicationsSection (RxNorm)
- AllergiesSection (RxNorm, UNII, SNOMED)
- ImmunizationsSection (CVX)
- VitalSignsSection (LOINC)
- ProceduresSection (CPT, SNOMED)
- ResultsSection (LOINC)
- SocialHistorySection (SNOMED)
- EncountersSection (CPT)

## Configuration

```python
from ccdakit import configure, CDAConfig, OrganizationInfo

config = CDAConfig(
    organization=OrganizationInfo(
        name="My Medical Center",
        npi="1234567890",
        oid_root="2.16.840.1.113883.3.EXAMPLE",
    ),
    version=CDAVersion.R2_1,
)
configure(config)
```

## Next Steps

- [Working with Sections](../guides/sections.md)
- [Protocols Reference](../guides/protocols.md)
- [Examples](../examples/complete-document.md)
