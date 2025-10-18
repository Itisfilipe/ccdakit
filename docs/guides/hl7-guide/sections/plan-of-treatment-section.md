# Plan of Treatment Section

**OID:** 2.16.840.1.113883.10.20.22.2.10
**Version:** 2014-06-09
**Badge:** Specialized Section

## Overview

The Plan of Treatment Section contains pending orders, interventions, encounters, services, and procedures for the patient. This section represents the patient's current care plan and includes all prospective activities that are intended to be performed in the future.

All entries in this section use moodCode of INT (intent) or other prospective mood codes to indicate that these are planned activities, not completed ones.

## Template Details

- **Template ID:** 2.16.840.1.113883.10.20.22.2.10
- **Extension:** 2014-06-09
- **Conformance:** SHALL
- **Cardinality:** 0..1 (Optional in documents)
- **LOINC Code:** 18776-5 "Plan of Treatment"

## Protocol Requirements

The Plan of Treatment Section supports multiple types of planned activities. Each type has its own protocol:

### PlannedObservationProtocol
```python
from typing import Protocol, Optional
from datetime import date

class PlannedObservationProtocol(Protocol):
    description: str              # Description of planned observation
    code: str                      # LOINC or SNOMED code
    code_system: str              # Code system (e.g., "LOINC", "SNOMED")
    status: str                   # Status (e.g., "active", "completed")
    planned_date: Optional[date]  # When observation is planned
```

### PlannedProcedureProtocol
```python
class PlannedProcedureProtocol(Protocol):
    description: str              # Description of planned procedure
    code: str                     # CPT or SNOMED code
    code_system: str             # Code system
    status: str                  # Status
    planned_date: Optional[date] # When procedure is planned
```

### PlannedMedicationProtocol
```python
class PlannedMedicationProtocol(Protocol):
    description: str              # Medication name
    code: str                     # RxNorm code
    code_system: str             # "RxNorm"
    status: str                  # Status
    planned_date: Optional[date] # When to start medication
```

### PlannedEncounterProtocol
```python
class PlannedEncounterProtocol(Protocol):
    description: str              # Description of planned encounter
    code: str                     # CPT code
    code_system: str             # Code system
    status: str                  # Status
    planned_date: Optional[date] # Appointment date
```

Other supported protocols: `PlannedActProtocol`, `PlannedSupplyProtocol`, `PlannedImmunizationProtocol`, `InstructionProtocol`.

## Code Example

```python
from ccdakit import PlanOfTreatmentSection, CDAVersion
from datetime import date

# Define planned activities
planned_procedures = [
    {
        "description": "Follow-up colonoscopy",
        "code": "44388",
        "code_system": "CPT",
        "status": "active",
        "planned_date": date(2025, 6, 15)
    }
]

planned_medications = [
    {
        "description": "Start Metformin 500mg",
        "code": "860975",
        "code_system": "RxNorm",
        "status": "active",
        "planned_date": date(2025, 2, 1)
    }
]

planned_observations = [
    {
        "description": "HbA1c measurement",
        "code": "4548-4",
        "code_system": "LOINC",
        "status": "active",
        "planned_date": date(2025, 5, 1)
    }
]

# Create section
section = PlanOfTreatmentSection(
    planned_procedures=planned_procedures,
    planned_medications=planned_medications,
    planned_observations=planned_observations,
    version=CDAVersion.R2_1
)

# Generate XML
xml_element = section.build()
```

## Official Reference

[HL7 C-CDA Plan of Treatment Section Specification](https://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.10.html)

## Best Practices

1. **Use Appropriate Activity Types**: Choose the correct planned activity type (procedure, medication, observation, etc.) based on what is being planned.

2. **Include Planned Dates**: Always provide planned dates when known to help with care coordination and scheduling.

3. **Maintain Status Accuracy**: Use accurate status values (typically "active" for planned activities).

4. **Link to Goals**: When possible, reference associated health goals to provide context for the treatment plan.

5. **Coordinate with Orders**: Ensure planned activities align with actual orders in your system.

6. **Update Regularly**: Keep the plan of treatment current by removing completed activities and adding new ones.

7. **Use Instructions**: Include patient instructions for self-care activities that are part of the treatment plan.

8. **Document Dependencies**: If one planned activity depends on another, consider documenting this relationship.
