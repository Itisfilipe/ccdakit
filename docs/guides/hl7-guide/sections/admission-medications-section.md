# Admission Medications Section

**OID:** 2.16.840.1.113883.10.20.22.2.44
**Version:** 2015-08-01
**Badge:** Specialized Section

## Overview

The Admission Medications Section contains the medications taken by the patient prior to and at the time of admission to the facility. This is a critical medication reconciliation component that helps prevent medication errors and adverse drug events during transitions of care.

Documenting admission medications allows providers to understand the patient's medication regimen before hospitalization and make informed decisions about continuing, modifying, or discontinuing medications during the hospital stay.

## Template Details

- **Template ID:** 2.16.840.1.113883.10.20.22.2.44
- **Extension:** 2015-08-01
- **Conformance:** SHOULD
- **Cardinality:** 0..1 (Optional in documents)
- **LOINC Code:** 42346-7 "Medications on Admission"

## Protocol Requirements

### MedicationProtocol
```python
from typing import Protocol, Optional
from datetime import date

class MedicationProtocol(Protocol):
    name: str                      # Medication name
    code: str                      # RxNorm code
    dosage: str                    # Dosage amount (e.g., "10 mg")
    route: str                     # Route of administration (e.g., "oral")
    frequency: str                 # Frequency (e.g., "twice daily")
    start_date: date              # Start date
    end_date: Optional[date]      # End date (None if ongoing)
    status: str                   # Status: "active", "completed", "discontinued"
```

## Code Example

### Basic Admission Medications
```python
from ccdakit import AdmissionMedicationsSection, CDAVersion
from datetime import date

# Define medications patient was taking at admission
admission_medications = [
    {
        "name": "Lisinopril 10 MG Oral Tablet",
        "code": "314076",
        "dosage": "10 mg",
        "route": "oral",
        "frequency": "once daily",
        "start_date": date(2023, 6, 1),
        "end_date": None,
        "status": "active"
    },
    {
        "name": "Metformin 500 MG Oral Tablet",
        "code": "860975",
        "dosage": "500 mg",
        "route": "oral",
        "frequency": "twice daily",
        "start_date": date(2023, 1, 15),
        "end_date": None,
        "status": "active"
    },
    {
        "name": "Aspirin 81 MG Oral Tablet",
        "code": "243670",
        "dosage": "81 mg",
        "route": "oral",
        "frequency": "once daily",
        "start_date": date(2022, 3, 10),
        "end_date": None,
        "status": "active"
    }
]

section = AdmissionMedicationsSection(
    medications=admission_medications,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Admission Medications with Discontinued Meds
```python
from ccdakit import AdmissionMedicationsSection, CDAVersion
from datetime import date

# Include both active and recently discontinued medications
admission_medications = [
    {
        "name": "Atorvastatin 40 MG Oral Tablet",
        "code": "617318",
        "dosage": "40 mg",
        "route": "oral",
        "frequency": "once daily at bedtime",
        "start_date": date(2022, 1, 1),
        "end_date": None,
        "status": "active"
    },
    {
        "name": "Hydrochlorothiazide 25 MG Oral Tablet",
        "code": "310798",
        "dosage": "25 mg",
        "route": "oral",
        "frequency": "once daily",
        "start_date": date(2021, 6, 1),
        "end_date": date(2024, 12, 15),
        "status": "discontinued"
    },
    {
        "name": "Omeprazole 20 MG Oral Capsule",
        "code": "312080",
        "dosage": "20 mg",
        "route": "oral",
        "frequency": "once daily before breakfast",
        "start_date": date(2023, 8, 1),
        "end_date": None,
        "status": "active"
    }
]

section = AdmissionMedicationsSection(
    medications=admission_medications,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Using Null Flavor (No Information Available)
```python
from ccdakit import AdmissionMedicationsSection, CDAVersion

# When medication information is not available
section = AdmissionMedicationsSection(
    medications=[],
    null_flavor="NI",  # No Information
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Complex Medication Regimen
```python
from ccdakit import AdmissionMedicationsSection, CDAVersion
from datetime import date

# Patient with multiple chronic conditions on multiple medications
admission_medications = [
    # Cardiovascular
    {
        "name": "Metoprolol Succinate 50 MG Extended Release Tablet",
        "code": "866436",
        "dosage": "50 mg",
        "route": "oral",
        "frequency": "once daily",
        "start_date": date(2022, 3, 1),
        "end_date": None,
        "status": "active"
    },
    {
        "name": "Lisinopril 20 MG Oral Tablet",
        "code": "314077",
        "dosage": "20 mg",
        "route": "oral",
        "frequency": "once daily",
        "start_date": date(2021, 9, 1),
        "end_date": None,
        "status": "active"
    },
    # Anticoagulation
    {
        "name": "Warfarin Sodium 5 MG Oral Tablet",
        "code": "855333",
        "dosage": "5 mg",
        "route": "oral",
        "frequency": "once daily in evening",
        "start_date": date(2023, 4, 15),
        "end_date": None,
        "status": "active"
    },
    # Diabetes
    {
        "name": "Insulin Glargine 100 UNT/ML Injectable Solution",
        "code": "274783",
        "dosage": "20 units",
        "route": "subcutaneous",
        "frequency": "once daily at bedtime",
        "start_date": date(2022, 11, 1),
        "end_date": None,
        "status": "active"
    },
    # Other
    {
        "name": "Levothyroxine Sodium 0.1 MG Oral Tablet",
        "code": "966224",
        "dosage": "100 mcg",
        "route": "oral",
        "frequency": "once daily on empty stomach",
        "start_date": date(2020, 5, 1),
        "end_date": None,
        "status": "active"
    }
]

section = AdmissionMedicationsSection(
    medications=admission_medications,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

## Official Reference

[HL7 C-CDA Admission Medications Section Specification](https://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.44.html)

## Best Practices

1. **Complete Medication Reconciliation**: Conduct thorough medication reconciliation at admission using multiple sources (patient interview, family, pharmacy records, medication bottles).

2. **Use RxNorm Codes**: Always use RxNorm codes for standardized medication identification and exchange.

3. **Include All Medications**: Document all medications including prescription, over-the-counter, herbal supplements, vitamins, and "as needed" medications.

4. **Verify Dosages**: Confirm exact dosages and frequencies with the patient or reliable sources.

5. **Document Recent Changes**: Include recently discontinued medications and note when they were stopped.

6. **Note Compliance Issues**: If patient reports non-adherence, document the actual medication regimen being followed.

7. **Include Administration Details**: Document specific administration instructions (e.g., "with food", "on empty stomach", "at bedtime").

8. **Cross-Reference Bottles**: When possible, verify medications against actual medication bottles brought by patient.

9. **Update During Stay**: Use this section to establish baseline; medication changes during stay go in active medications.

10. **Coordinate with Discharge**: Compare admission medications with discharge medications to identify changes.

## Medication Reconciliation Sources

- **Patient Interview**: Direct questioning about medications
- **Medication Bottles**: Physical medication containers
- **Pharmacy Records**: Electronic pharmacy dispensing records
- **Prior Medical Records**: Previous discharge summaries or clinic notes
- **Family Members**: Caregiver or family information
- **Medication Lists**: Patient-maintained medication lists
- **Home Health Records**: Records from home health agencies
- **Outpatient Providers**: Information from primary care or specialists

## Common Documentation Scenarios

### New Admission - Complete List Available
Document all home medications with accurate dosages and frequencies.

### Emergency Admission - Limited Information
Use null_flavor="NI" or document partial list with note about incomplete information.

### Planned Admission - Pre-verified List
Document comprehensive list verified during pre-admission testing or clinic visit.

### Transfer from Another Facility
Document medications from transfer documentation, noting any discrepancies.

## Status Values

- **active**: Patient currently taking medication
- **completed**: Finished course of medication (e.g., completed antibiotic course)
- **discontinued**: Medication stopped before admission
- **suspended**: Temporarily not taking medication
- **on hold**: Medication held pending evaluation

## Coordination with Other Sections

- **Discharge Medications**: Compare to identify medication changes
- **Active Medications**: Update based on inpatient orders
- **Medication Allergies**: Cross-check for potential allergies
- **Problem List**: Correlate medications with documented conditions
