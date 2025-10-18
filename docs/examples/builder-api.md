# Builder API Examples

Using the fluent builder API for cleaner code.

## Simple Builders

ccdakit provides simple builder classes for common data types:

### Patient Builder

```python
from ccdakit.utils.builders import SimplePatientBuilder
from datetime import date

patient = (
    SimplePatientBuilder()
    .name("John", "Doe", middle="M")
    .birth_date(date(1970, 1, 1))
    .sex("M")
    .ssn("123-45-6789")
    .address("123 Main St", "Boston", "MA", "02101")
    .phone("617-555-1234")
    .build()
)
```

### Problem Builder

```python
from ccdakit.utils.builders import SimpleProblemBuilder
from datetime import date

problem = (
    SimpleProblemBuilder()
    .name("Type 2 Diabetes Mellitus")
    .code("44054006", "SNOMED")
    .status("active")
    .onset_date(date(2020, 1, 15))
    .build()
)
```

### Medication Builder

```python
from ccdakit.utils.builders import SimpleMedicationBuilder

medication = (
    SimpleMedicationBuilder()
    .name("Metformin 500mg Tablet")
    .code("860975", "RxNorm")
    .status("active")
    .dosage("500 mg")
    .route("oral")
    .frequency("twice daily")
    .build()
)
```

### Allergy Builder

```python
from ccdakit.utils.builders import SimpleAllergyBuilder

allergy = (
    SimpleAllergyBuilder()
    .allergen("Penicillin")
    .code("7980", "RxNorm")
    .type("allergy")
    .status("active")
    .reaction("Rash")
    .severity("moderate")
    .build()
)
```

## Complete Example

```python
from ccdakit import ClinicalDocument, ProblemsSection, CDAVersion
from ccdakit.utils.builders import (
    SimplePatientBuilder,
    SimpleProblemBuilder,
    SimpleMedicationBuilder,
)
from datetime import date

# Build patient
patient = (
    SimplePatientBuilder()
    .name("Sarah", "Johnson", middle="Marie")
    .birth_date(date(1985, 7, 12))
    .sex("F")
    .address("456 Oak Ave", "Seattle", "WA", "98101")
    .phone("206-555-9876")
    .email("sarah.johnson@example.com")
    .build()
)

# Build problems
problems = [
    SimpleProblemBuilder()
    .name("Type 2 Diabetes")
    .code("44054006", "SNOMED")
    .status("active")
    .onset_date(date(2020, 1, 15))
    .build(),

    SimpleProblemBuilder()
    .name("Essential Hypertension")
    .code("59621000", "SNOMED")
    .status("active")
    .onset_date(date(2019, 3, 10))
    .build(),
]

# Build medications
medications = [
    SimpleMedicationBuilder()
    .name("Metformin 500mg")
    .code("860975", "RxNorm")
    .status("active")
    .dosage("500 mg")
    .route("oral")
    .frequency("twice daily")
    .build(),

    SimpleMedicationBuilder()
    .name("Lisinopril 10mg")
    .code("314076", "RxNorm")
    .status("active")
    .dosage("10 mg")
    .route("oral")
    .frequency("once daily")
    .build(),
]

# Create document
doc = ClinicalDocument(
    patient=patient,
    sections=[
        ProblemsSection(problems=problems, version=CDAVersion.R2_1),
        MedicationsSection(medications=medications, version=CDAVersion.R2_1),
    ],
    version=CDAVersion.R2_1,
)

xml = doc.to_string(pretty=True)
```

## Benefits

1. **Fluent API**: Chainable methods
2. **Less verbose**: No need to create classes
3. **Type-safe**: Parameters are validated
4. **Clear intent**: Self-documenting code
5. **IDE support**: Better autocomplete

## Next Steps

- [Complete Document](complete-document.md)
- [All Sections](all-sections.md)
- [API Reference](../api/utilities.md)
