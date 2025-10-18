# Core Sections Example

Complete example using the 9 core clinical sections.

> **Note:** This library supports 29 total C-CDA sections. This example demonstrates the 9 most commonly used core sections. For a complete list of available sections, see the [Sections Reference](../reference/sections.md).

## Full Implementation

```python
from ccdakit import (
    ClinicalDocument,
    ProblemsSection,
    MedicationsSection,
    AllergiesSection,
    ImmunizationsSection,
    VitalSignsSection,
    ProceduresSection,
    ResultsSection,
    SocialHistorySection,
    EncountersSection,
    CDAVersion,
)
from datetime import date, datetime

# Patient data
class Patient:
    @property
    def first_name(self):
        return "Sarah"

    @property
    def last_name(self):
        return "Johnson"

    @property
    def date_of_birth(self):
        return date(1985, 7, 12)

    @property
    def sex(self):
        return "F"

# Problems
problems = [
    create_problem("Type 2 Diabetes", "44054006", "active", date(2020, 1, 15)),
    create_problem("Hypertension", "59621000", "active", date(2019, 3, 10)),
]

# Medications
medications = [
    create_medication("Metformin 500mg", "860975", "active", "500 mg", "oral", "twice daily"),
    create_medication("Lisinopril 10mg", "314076", "active", "10 mg", "oral", "once daily"),
]

# Allergies
allergies = [
    create_allergy("Penicillin", "7980", "allergy", "active", "Rash", "moderate"),
]

# Immunizations
immunizations = [
    create_immunization("Influenza vaccine", "88", date(2023, 10, 15), "completed"),
    create_immunization("COVID-19 vaccine", "213", date(2023, 9, 1), "completed"),
]

# Vital Signs
vital_organizers = [
    create_vital_organizer(
        date=datetime(2024, 1, 15, 10, 30),
        vitals=[
            ("Blood Pressure Systolic", "8480-6", "120", "mm[Hg]"),
            ("Blood Pressure Diastolic", "8462-4", "80", "mm[Hg]"),
            ("Heart Rate", "8867-4", "72", "bpm"),
            ("Body Temperature", "8310-5", "98.6", "degF"),
        ]
    )
]

# Procedures
procedures = [
    create_procedure("Colonoscopy", "73761001", "SNOMED", date(2023, 5, 20), "completed"),
]

# Results (Lab panels)
result_organizers = [
    create_result_organizer(
        "Complete Blood Count",
        "58410-2",
        datetime(2024, 1, 10),
        [
            ("White Blood Cell Count", "6690-2", "7.5", "10*3/uL", "Normal"),
            ("Red Blood Cell Count", "789-8", "4.8", "10*6/uL", "Normal"),
            ("Hemoglobin", "718-7", "14.2", "g/dL", "Normal"),
        ]
    )
]

# Social History
social_history = [
    create_smoking_status("Former smoker", "8517006", date(2015, 1, 1)),
]

# Encounters
encounters = [
    create_encounter(
        "Office Visit",
        "99213",
        date(2024, 1, 15),
        "Dr. Smith",
        "Example Clinic"
    ),
]

# Build complete document
doc = ClinicalDocument(
    patient=Patient(),
    sections=[
        ProblemsSection(problems=problems, version=CDAVersion.R2_1),
        MedicationsSection(medications=medications, version=CDAVersion.R2_1),
        AllergiesSection(allergies=allergies, version=CDAVersion.R2_1),
        ImmunizationsSection(immunizations=immunizations, version=CDAVersion.R2_1),
        VitalSignsSection(organizers=vital_organizers, version=CDAVersion.R2_1),
        ProceduresSection(procedures=procedures, version=CDAVersion.R2_1),
        ResultsSection(organizers=result_organizers, version=CDAVersion.R2_1),
        SocialHistorySection(smoking_statuses=social_history, version=CDAVersion.R2_1),
        EncountersSection(encounters=encounters, version=CDAVersion.R2_1),
    ],
    version=CDAVersion.R2_1,
)

# Generate XML
xml = doc.to_string(pretty=True)

# Save
with open("complete_ccda.xml", "w") as f:
    f.write(xml)

print(f"Generated complete C-CDA: {len(xml):,} bytes")
print(f"Core Sections: 9 (29 total available)")
print("✅ All core sections included!")
```

## Using Test Data Generator

Easier approach using built-in test data:

```python
from ccdakit.utils import TestDataGenerator
from ccdakit import ClinicalDocument, CDAVersion
from ccdakit.builders.sections import *

# Generate test data
gen = TestDataGenerator()

patient = gen.generate_patient()
problems = gen.generate_problems(count=3)
medications = gen.generate_medications(count=5)
allergies = gen.generate_allergies(count=2)
immunizations = gen.generate_immunizations(count=3)
vitals = gen.generate_vital_signs_organizers(count=2)
procedures = gen.generate_procedures(count=2)
results = gen.generate_result_organizers(count=1)
smoking = [gen.generate_smoking_status()]
encounters = gen.generate_encounters(count=2)

# Build document
doc = ClinicalDocument(
    patient=patient,
    sections=[
        ProblemsSection(problems=problems, version=CDAVersion.R2_1),
        MedicationsSection(medications=medications, version=CDAVersion.R2_1),
        AllergiesSection(allergies=allergies, version=CDAVersion.R2_1),
        ImmunizationsSection(immunizations=immunizations, version=CDAVersion.R2_1),
        VitalSignsSection(organizers=vitals, version=CDAVersion.R2_1),
        ProceduresSection(procedures=procedures, version=CDAVersion.R2_1),
        ResultsSection(organizers=results, version=CDAVersion.R2_1),
        SocialHistorySection(smoking_statuses=smoking, version=CDAVersion.R2_1),
        EncountersSection(encounters=encounters, version=CDAVersion.R2_1),
    ],
    version=CDAVersion.R2_1,
)

xml = doc.to_string(pretty=True)
```

## Next Steps

- [Builder API](builder-api.md)
- [Custom Models](custom-models.md)
- [Validation](validation.md)
