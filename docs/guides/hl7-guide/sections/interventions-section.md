# Interventions Section

**OID:** 2.16.840.1.113883.10.20.21.2.3
**Version:** 2015-08-01
**Badge:** Specialized Section

## Overview

The Interventions Section represents interventions - actions taken to maximize the prospects of achieving the goals of care for the patient, including removal of barriers to success. Interventions can be planned, ordered, or historical (already performed).

Interventions include actions that may be ongoing (such as maintenance medications and monitoring health status). This section documents both completed interventions and those that are planned for the future. Instructions may be nested within interventions and can include self-care instructions.

## Template Details

- **Template ID:** 2.16.840.1.113883.10.20.21.2.3
- **Extension:** 2015-08-01
- **Conformance:** MAY
- **Cardinality:** 0..1 (Optional in documents)
- **LOINC Code:** 62387-6 "Interventions Provided"

## Protocol Requirements

### InterventionProtocol (Completed Interventions)
```python
from typing import Protocol, Optional
from datetime import datetime

class InterventionProtocol(Protocol):
    description: str                    # Description of the intervention
    status: str                        # Status (e.g., "completed", "active", "in-progress")
    effective_time: Optional[datetime] # When intervention was performed
    goal_reference_id: Optional[str]   # Reference to related goal
```

### PlannedInterventionProtocol (Future Interventions)
```python
class PlannedInterventionProtocol(Protocol):
    description: str                    # Description of planned intervention
    status: str                        # Status (typically "active" for planned)
    effective_time: Optional[datetime] # When intervention is planned
    goal_reference_id: Optional[str]   # Reference to related goal
```

## Code Example

### Completed Interventions
```python
from ccdakit import InterventionsSection, CDAVersion
from datetime import datetime

# Define completed interventions
interventions = [
    {
        "description": "Patient education on diabetes self-management",
        "status": "completed",
        "effective_time": datetime(2025, 1, 15, 10, 30),
        "goal_reference_id": "goal-1"
    },
    {
        "description": "Home safety assessment completed",
        "status": "completed",
        "effective_time": datetime(2025, 1, 10, 14, 0),
        "goal_reference_id": None
    },
    {
        "description": "Smoking cessation counseling provided",
        "status": "completed",
        "effective_time": datetime(2025, 1, 12, 11, 15),
        "goal_reference_id": "goal-2"
    }
]

section = InterventionsSection(
    interventions=interventions,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Planned Interventions
```python
from ccdakit import InterventionsSection, CDAVersion
from datetime import datetime

# Define planned interventions
planned_interventions = [
    {
        "description": "Physical therapy evaluation scheduled",
        "status": "active",
        "effective_time": datetime(2025, 2, 1, 9, 0),
        "goal_reference_id": "goal-mobility"
    },
    {
        "description": "Nutritional counseling appointment",
        "status": "active",
        "effective_time": datetime(2025, 1, 25, 14, 30),
        "goal_reference_id": "goal-weight"
    }
]

section = InterventionsSection(
    planned_interventions=planned_interventions,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Combined Completed and Planned Interventions
```python
from ccdakit import InterventionsSection, CDAVersion
from datetime import datetime

# Both completed and planned interventions
interventions = [
    {
        "description": "Medication adherence counseling provided",
        "status": "completed",
        "effective_time": datetime(2025, 1, 18, 10, 0),
        "goal_reference_id": "goal-medication-adherence"
    },
    {
        "description": "Chronic pain management education completed",
        "status": "completed",
        "effective_time": datetime(2025, 1, 18, 10, 30),
        "goal_reference_id": "goal-pain-control"
    }
]

planned_interventions = [
    {
        "description": "Follow-up phone call for medication adherence",
        "status": "active",
        "effective_time": datetime(2025, 2, 1, 10, 0),
        "goal_reference_id": "goal-medication-adherence"
    },
    {
        "description": "Social work consult for transportation assistance",
        "status": "active",
        "effective_time": datetime(2025, 1, 22, 13, 0),
        "goal_reference_id": None
    }
]

section = InterventionsSection(
    interventions=interventions,
    planned_interventions=planned_interventions,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Comprehensive Care Coordination Example
```python
from ccdakit import InterventionsSection, CDAVersion
from datetime import datetime

# Complex care coordination interventions
interventions = [
    {
        "description": "Care coordination meeting with primary care provider",
        "status": "completed",
        "effective_time": datetime(2025, 1, 15, 14, 0),
        "goal_reference_id": None
    },
    {
        "description": "Medical equipment evaluation and ordering (walker)",
        "status": "completed",
        "effective_time": datetime(2025, 1, 16, 11, 0),
        "goal_reference_id": "goal-mobility"
    },
    {
        "description": "Referral to diabetes educator",
        "status": "completed",
        "effective_time": datetime(2025, 1, 15, 15, 30),
        "goal_reference_id": "goal-diabetes-control"
    }
]

planned_interventions = [
    {
        "description": "Home health nursing assessment scheduled",
        "status": "active",
        "effective_time": datetime(2025, 1, 25, 10, 0),
        "goal_reference_id": None
    },
    {
        "description": "Caregiver training on wound care",
        "status": "active",
        "effective_time": datetime(2025, 1, 23, 14, 0),
        "goal_reference_id": "goal-wound-healing"
    }
]

section = InterventionsSection(
    interventions=interventions,
    planned_interventions=planned_interventions,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

## Official Reference

[HL7 C-CDA Interventions Section Specification](https://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.21.2.3.html)

## Best Practices

1. **Link to Goals**: Always reference related health goals when interventions are goal-directed to show care coordination.

2. **Be Specific**: Describe interventions in detail so other providers understand exactly what was done.

3. **Document Outcomes**: When possible, note the outcome or effectiveness of completed interventions.

4. **Include All Disciplines**: Document interventions from all care team members (nursing, PT, OT, social work, pharmacy, etc.).

5. **Track Planned Items**: Use planned interventions to document future actions that are part of the care plan.

6. **Timestamp Accurately**: Include specific dates and times for both completed and planned interventions.

7. **Update Status**: Keep intervention status current as they progress from planned to in-progress to completed.

8. **Address Barriers**: Document interventions specifically aimed at removing barriers to care (transportation, finances, health literacy).

9. **Self-Care Instructions**: Include patient education and self-care instructions as interventions.

10. **Care Coordination**: Document care coordination activities and referrals to other providers or services.

## Common Intervention Types

### Patient Education
- Disease-specific education (diabetes, heart failure, COPD)
- Medication management education
- Lifestyle modification counseling
- Symptom management instruction
- Self-monitoring techniques

### Care Coordination
- Referrals to specialists
- Home health arrangements
- Medical equipment ordering
- Care transition planning
- Follow-up appointment scheduling

### Behavioral Health
- Smoking cessation counseling
- Alcohol and substance abuse counseling
- Mental health counseling
- Stress management techniques
- Sleep hygiene education

### Nutritional Support
- Dietary counseling
- Meal planning assistance
- Nutritional supplements
- Enteral/parenteral nutrition management

### Rehabilitation Services
- Physical therapy
- Occupational therapy
- Speech therapy
- Cardiac rehabilitation
- Pulmonary rehabilitation

### Social Services
- Financial assistance programs
- Transportation arrangements
- Housing assistance
- Community resource connection
- Caregiver support services

### Barrier Removal
- Health literacy interventions
- Language interpretation services
- Transportation assistance
- Financial counseling
- Medication affordability programs

## Status Values

- **active**: Intervention is ongoing or planned
- **completed**: Intervention has been finished
- **in-progress**: Intervention is currently being performed
- **suspended**: Intervention temporarily on hold
- **cancelled**: Planned intervention was cancelled
- **aborted**: Intervention started but not completed

## Linking Interventions to Goals

When interventions are tied to specific health goals, use the goal_reference_id field to create the link:

```python
# Example showing intervention-goal relationship
interventions = [
    {
        "description": "Daily walking program initiated",
        "status": "active",
        "effective_time": datetime(2025, 1, 15),
        "goal_reference_id": "goal-increase-activity"  # Links to mobility goal
    }
]
```

This creates a clear connection between the action taken (intervention) and the desired outcome (goal), demonstrating coordinated, goal-directed care.
