# Quick Start

Create your first C-CDA document in minutes.

## Minimal Example

```python
from ccdakit import ClinicalDocument, ProblemsSection, CDAVersion
from datetime import date

# Your patient data
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

# Your problem data
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

# Create document
patient = MyPatient()
problems = [MyProblem()]

doc = ClinicalDocument(
    patient=patient,
    sections=[
        ProblemsSection(problems=problems, version=CDAVersion.R2_1),
    ],
    version=CDAVersion.R2_1,
)

# Generate XML
xml = doc.to_string(pretty=True)
with open("patient_ccda.xml", "w") as f:
    f.write(xml)
```

## With Configuration

```python
from ccdakit import configure, CDAConfig, OrganizationInfo, CDAVersion

config = CDAConfig(
    organization=OrganizationInfo(
        name="Example Medical Center",
        npi="1234567890",
        oid_root="2.16.840.1.113883.3.EXAMPLE",
    ),
    version=CDAVersion.R2_1,
)
configure(config)
```

## Multiple Sections

```python
from ccdakit import (
    ClinicalDocument,
    ProblemsSection,
    MedicationsSection,
    AllergiesSection,
    CDAVersion,
)

doc = ClinicalDocument(
    patient=patient_data,
    sections=[
        ProblemsSection(problems=problems_list, version=CDAVersion.R2_1),
        MedicationsSection(medications=meds_list, version=CDAVersion.R2_1),
        AllergiesSection(allergies=allergies_list, version=CDAVersion.R2_1),
    ],
    version=CDAVersion.R2_1,
)
```

## Next Steps

- [Basic Concepts](concepts.md)
- [Working with Sections](../guides/sections.md)
- [HL7/C-CDA Comprehensive Guide](../guides/hl7-guide/index.md)
- [Examples](../examples/complete-document.md)
