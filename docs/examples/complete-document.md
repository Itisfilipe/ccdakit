# Complete Document Example

Full example showing all features.

## Complete C-CDA Document

```python
from ccdakit import (
    configure,
    CDAConfig,
    OrganizationInfo,
    ClinicalDocument,
    ProblemsSection,
    MedicationsSection,
    AllergiesSection,
    ImmunizationsSection,
    VitalSignsSection,
    CDAVersion,
)
from datetime import date

# 1. Configure (once at startup)
config = CDAConfig(
    organization=OrganizationInfo(
        name="Example Medical Center",
        npi="1234567890",
        oid_root="2.16.840.1.113883.3.EXAMPLE",
        address="123 Main St",
        city="Boston",
        state="MA",
        postal_code="02101",
        country="US",
        telecom="tel:617-555-1234",
    ),
    version=CDAVersion.R2_1,
)
configure(config)

# 2. Define your data models
class Patient:
    @property
    def first_name(self):
        return "John"

    @property
    def last_name(self):
        return "Doe"

    @property
    def date_of_birth(self):
        return date(1970, 5, 15)

    @property
    def sex(self):
        return "M"

class Problem:
    def __init__(self, name, code, status, onset):
        self._name = name
        self._code = code
        self._status = status
        self._onset = onset

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return "SNOMED"

    @property
    def status(self):
        return self._status

    @property
    def onset_date(self):
        return self._onset

# 3. Create your data
patient = Patient()

problems = [
    Problem("Type 2 Diabetes Mellitus", "44054006", "active", date(2020, 1, 15)),
    Problem("Essential Hypertension", "59621000", "active", date(2019, 3, 10)),
    Problem("Seasonal Allergic Rhinitis", "367498001", "active", date(2018, 9, 5)),
]

# 4. Build the document
doc = ClinicalDocument(
    patient=patient,
    sections=[
        ProblemsSection(problems=problems, version=CDAVersion.R2_1),
        # Add more sections...
    ],
    version=CDAVersion.R2_1,
)

# 5. Generate XML
xml = doc.to_string(pretty=True)

# 6. Save to file
with open("patient_ccda.xml", "w") as f:
    f.write(xml)

print(f"Generated C-CDA document: {len(xml)} bytes")
```

## Output

The generated XML includes:

- Complete C-CDA R2.1 header
- Patient demographics
- Provider information
- Problems section with narrative table
- All required template IDs
- Valid OIDs and codes

## Next Steps

- [All Sections Example](all-sections.md)
- [Builder API](builder-api.md)
- [Custom Models](custom-models.md)
