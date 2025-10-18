# Discharge Medications Section

**OID:** 2.16.840.1.113883.10.20.22.2.11.1
**Version:** 2015-08-01
**Badge:** Specialized Section

## Overview

The Discharge Medications Section contains the medications the patient is intended to take (or stop taking) after hospital discharge. This is a critical safety component of the discharge process, as medication discrepancies are a common cause of adverse events post-discharge.

Current, active medications must be listed. The section may also include the patient's prescription history and indicate the source of the medication list. This is an entries-required section, meaning at least one medication entry must be present unless nullFlavor is used.

## Template Details

- **Template ID:** 2.16.840.1.113883.10.20.22.2.11.1
- **Extension:** 2015-08-01
- **Conformance:** SHALL
- **Cardinality:** 0..1 (Optional in documents)
- **LOINC Code:** 10183-2 "Hospital Discharge Medications"
- **Translation Code:** 75311-1 "Discharge Medications"

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
    instructions: Optional[str]   # Additional instructions
```

## Code Example

```python
from ccdakit import DischargeMedicationsSection, CDAVersion
from datetime import date

# Define discharge medications
discharge_medications = [
    {
        "name": "Lisinopril 10 MG Oral Tablet",
        "code": "314076",
        "dosage": "10 mg",
        "route": "oral",
        "frequency": "once daily",
        "start_date": date(2025, 1, 20),
        "end_date": None,
        "status": "active",
        "instructions": "Take in the morning with water"
    },
    {
        "name": "Aspirin 81 MG Oral Tablet",
        "code": "243670",
        "dosage": "81 mg",
        "route": "oral",
        "frequency": "once daily",
        "start_date": date(2025, 1, 20),
        "end_date": None,
        "status": "active",
        "instructions": "Take with food"
    },
    {
        "name": "Metformin 500 MG Oral Tablet",
        "code": "860975",
        "dosage": "500 mg",
        "route": "oral",
        "frequency": "twice daily",
        "start_date": date(2025, 1, 20),
        "end_date": None,
        "status": "active",
        "instructions": "Take with meals"
    },
    {
        "name": "Amoxicillin 500 MG Oral Capsule",
        "code": "308182",
        "dosage": "500 mg",
        "route": "oral",
        "frequency": "three times daily",
        "start_date": date(2025, 1, 20),
        "end_date": date(2025, 1, 30),
        "status": "active",
        "instructions": "Complete full course of antibiotics"
    }
]

# Create section
section = DischargeMedicationsSection(
    medications=discharge_medications,
    version=CDAVersion.R2_1
)

# Generate XML
xml_element = section.build()
```

### Using Null Flavor (No Information Available)
```python
from ccdakit import DischargeMedicationsSection, CDAVersion

# When no medication information is available
section = DischargeMedicationsSection(
    medications=[],
    null_flavor="NI",  # No Information
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

## Official Reference

[HL7 C-CDA Discharge Medications Section Specification](https://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.11.1.html)

## Best Practices

1. **Reconcile Medications**: Ensure discharge medications are reconciled with pre-admission medications and accurately reflect what the patient should take at home.

2. **Use RxNorm Codes**: Always use RxNorm codes for medications to ensure accurate electronic exchange and e-prescribing.

3. **Include Complete Instructions**: Provide clear, patient-friendly instructions for each medication including timing, food interactions, and special precautions.

4. **Document Changes**: Clearly indicate new medications, discontinued medications, and dose changes from pre-admission medications.

5. **Specify End Dates**: For short-term medications (antibiotics, pain medications), always include the end date.

6. **Status Accuracy**: Use "active" for ongoing medications, "discontinued" for stopped medications, and "completed" for finished courses.

7. **Coordinate with Discharge Instructions**: Ensure discharge medications align with the Hospital Discharge Instructions section.

8. **Address Compliance**: Include information about why medications are prescribed to improve patient understanding and compliance.

9. **Include All Medications**: Document all discharge medications including over-the-counter, herbal supplements, and "as needed" medications.

10. **Verify with Patient**: Confirm the discharge medication list with the patient before discharge to ensure understanding and identify potential barriers.

11. **Follow-up Planning**: Note which medications require monitoring or follow-up lab work in the instructions.

12. **Pharmacy Integration**: Coordinate with pharmacy to ensure prescriptions are ready and affordable for the patient.
