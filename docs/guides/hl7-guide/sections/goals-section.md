# Goals Section

**Template ID:** `2.16.840.1.113883.10.20.22.2.60`
**Version:** R2.1 | R2.0
**Badge:** Extended Section

## Overview

The **Goals Section** describes clinical goals or targets for a patient. Goals can be established by the patient, provider, or through shared decision-making. This section helps track treatment objectives, patient health targets, and desired outcomes over time.

Goals can include specific measurable targets (e.g., "HbA1c below 7%"), behavioral objectives (e.g., "Walk 30 minutes daily"), or general wellness aims (e.g., "Maintain healthy weight"). They provide a roadmap for care and enable tracking of progress toward desired health outcomes.

## Template Details

### Identifiers
- **Root:** `2.16.840.1.113883.10.20.22.2.60`
- **Extension:** None
- **LOINC Code:** `61146-7` (Goals)

### Conformance Requirements
- **MAY** contain `@nullFlavor="NI"` if no information available (CONF:1098-32819)
- **SHALL** contain exactly one [1..1] `templateId` (CONF:1098-29584)
- **SHALL** contain exactly one [1..1] `code` with code="61146-7" from LOINC (CONF:1098-29586)
- **SHALL** contain exactly one [1..1] `title` (CONF:1098-30721)
- **SHALL** contain exactly one [1..1] `text` (narrative block) (CONF:1098-30722)
- **SHOULD** contain at least one [1..*] `entry` (CONF:1098-30719)
- Each `entry` **SHALL** contain exactly one [1..1] Goal Observation (CONF:1098-30720)

### Cardinality
- **Section:** Optional
- **Entries:** Recommended (1..*)
- **Goal Observations:** One per entry

## Protocol Requirements

The section uses the `GoalProtocol` from `ccdakit.protocols.goal`:

### Required Properties
```python
@property
def description(self) -> str:
    """Human-readable goal description"""

@property
def status(self) -> str:
    """Goal status: 'active', 'cancelled', 'completed', 'on-hold'"""
```

### Optional Properties
```python
@property
def code(self) -> Optional[str]:
    """Goal code (typically from LOINC)"""

@property
def code_system(self) -> Optional[str]:
    """Code system: typically 'LOINC' or 'SNOMED'"""

@property
def display_name(self) -> Optional[str]:
    """Display name for the goal code"""

@property
def start_date(self) -> Optional[date]:
    """Date goal was established"""

@property
def target_date(self) -> Optional[date]:
    """Target date for goal achievement"""

@property
def value(self) -> Optional[str]:
    """Goal value/observation value (e.g., target weight, BP)"""

@property
def value_unit(self) -> Optional[str]:
    """Unit of measure for goal value"""

@property
def author(self) -> Optional[str]:
    """Author of the goal (patient, provider, or negotiated)"""

@property
def priority(self) -> Optional[str]:
    """Priority: 'low', 'medium', 'high'"""
```

## Code Example

### Basic Usage

```python
from datetime import date
from ccdakit import GoalsSection, CDAVersion

# Define patient goals
goals = [
    {
        "description": "Reduce HbA1c to below 7%",
        "status": "active",
        "start_date": date(2024, 1, 15),
        "target_date": date(2024, 7, 15),
        "value": "7.0",
        "value_unit": "%",
    },
    {
        "description": "Walk 30 minutes per day, 5 days per week",
        "status": "active",
        "start_date": date(2024, 2, 1),
        "target_date": date(2024, 6, 1),
    },
    {
        "description": "Lose 15 pounds",
        "status": "on-hold",
        "start_date": date(2024, 1, 1),
        "target_date": date(2024, 12, 31),
        "value": "15",
        "value_unit": "lb",
    },
]

# Create section
section = GoalsSection(
    goals=goals,
    version=CDAVersion.R2_1
)

# Generate XML
xml_element = section.to_element()
```

### Empty Section (No Goals)

```python
# Create section with no goals
section = GoalsSection(
    goals=[],
    version=CDAVersion.R2_1
)

# Generates section with narrative: "No goals documented"
```

### Section with Null Flavor

```python
# When no information is available
section = GoalsSection(
    goals=[],
    null_flavor="NI",  # No information
    version=CDAVersion.R2_1
)
```

### Completed Goals

```python
goals = [
    {
        "description": "Complete smoking cessation program",
        "status": "completed",
        "start_date": date(2023, 6, 1),
        "target_date": date(2023, 12, 1),
    },
    {
        "description": "Attend diabetes education classes",
        "status": "completed",
        "start_date": date(2023, 8, 15),
        "target_date": date(2023, 10, 15),
    },
]

section = GoalsSection(goals=goals)
```

### With Custom Protocol Implementation

```python
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class PatientGoal:
    """Custom goal implementation."""
    description: str
    status: str
    code: Optional[str] = None
    code_system: Optional[str] = None
    display_name: Optional[str] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    value: Optional[str] = None
    value_unit: Optional[str] = None
    author: Optional[str] = None
    priority: Optional[str] = None

# Create goals
goals = [
    PatientGoal(
        description="Maintain blood pressure below 130/80",
        status="active",
        start_date=date(2024, 3, 1),
        target_date=date(2025, 3, 1),
        value="130/80",
        value_unit="mmHg",
        priority="high",
    )
]

section = GoalsSection(goals=goals)
```

### Structured Goals with LOINC Codes

```python
goals = [
    {
        "description": "HbA1c goal",
        "code": "4548-4",  # LOINC code for HbA1c
        "code_system": "LOINC",
        "display_name": "Hemoglobin A1c/Hemoglobin.total in Blood",
        "status": "active",
        "value": "7.0",
        "value_unit": "%",
        "start_date": date(2024, 1, 1),
        "target_date": date(2024, 6, 30),
    }
]

section = GoalsSection(goals=goals)
```

## Official Reference

For complete specification details, refer to:
- **C-CDA Online:** [Goals Section](http://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.60.html)
- **Local Reference:** `references/C-CDA_2.1/templates/2.16.840.1.113883.10.20.22.2.60.html`

## Best Practices

### 1. SMART Goals
Create Specific, Measurable, Achievable, Relevant, and Time-bound goals:

```python
# Good: SMART goal
{
    "description": "Reduce HbA1c from 8.5% to below 7% within 6 months",
    "status": "active",
    "start_date": date(2024, 1, 1),
    "target_date": date(2024, 6, 30),
    "value": "7.0",
    "value_unit": "%",
}

# Less effective: Vague goal
{
    "description": "Improve diabetes control",
    "status": "active",
}
```

### 2. Status Management
```python
# Active: Currently working toward
{"description": "Walk 10,000 steps daily", "status": "active"}

# Completed: Successfully achieved
{"description": "Complete cardiac rehab", "status": "completed"}

# On-hold: Temporarily suspended
{"description": "Return to work full-time", "status": "on-hold"}

# Cancelled: Abandoned or no longer appropriate
{"description": "Train for marathon", "status": "cancelled"}
```

### 3. Measurable Targets
```python
# Include specific values and units
goals = [
    {
        "description": "Achieve target weight",
        "value": "180",
        "value_unit": "lb",
        "status": "active",
    },
    {
        "description": "Reduce systolic BP",
        "value": "130",
        "value_unit": "mmHg",
        "status": "active",
    }
]
```

### 4. Realistic Timeframes
```python
# Short-term goal (3-6 months)
{
    "description": "Lose 10 pounds",
    "start_date": date(2024, 1, 1),
    "target_date": date(2024, 4, 1),
}

# Long-term goal (1 year+)
{
    "description": "Maintain A1c below 7% for 1 year",
    "start_date": date(2024, 1, 1),
    "target_date": date(2025, 1, 1),
}
```

### 5. Patient-Centered Goals
```python
# Include patient's own goals and priorities
goals = [
    {
        "description": "Be able to play with grandchildren without fatigue",
        "status": "active",
        "author": "patient",
    },
    {
        "description": "Return to gardening activities",
        "status": "active",
        "author": "patient",
    }
]
```

### 6. Clinical Goals
```python
# Provider-driven clinical targets
goals = [
    {
        "description": "Titrate insulin to achieve fasting glucose 80-130 mg/dL",
        "status": "active",
        "value": "80-130",
        "value_unit": "mg/dL",
        "author": "provider",
    }
]
```

### 7. Narrative Generation
The section automatically generates an HTML table with:
- Goal description with unique ID reference
- Status (formatted with proper capitalization)
- Start date
- Target date
- Value with unit (if specified)

```python
# Empty section generates: "No goals documented"
# Non-empty sections generate complete HTML table
```

### 8. Priority Levels
```python
# Indicate goal importance
goals = [
    {
        "description": "Prevent diabetic complications",
        "priority": "high",
        "status": "active",
    },
    {
        "description": "Improve exercise tolerance",
        "priority": "medium",
        "status": "active",
    }
]
```

### 9. Goal Categories
```python
# Organize goals by type
behavioral_goals = [
    {"description": "Quit smoking", "status": "active"},
    {"description": "Exercise 30 min daily", "status": "active"},
]

clinical_goals = [
    {"description": "HbA1c < 7%", "value": "7.0", "value_unit": "%", "status": "active"},
    {"description": "LDL < 100", "value": "100", "value_unit": "mg/dL", "status": "active"},
]

# Combine in section
all_goals = behavioral_goals + clinical_goals
section = GoalsSection(goals=all_goals)
```

### 10. Progress Tracking
```python
# Document goal evolution over time
goals_initial = [
    {
        "description": "Lose 30 pounds",
        "status": "active",
        "start_date": date(2024, 1, 1),
        "target_date": date(2024, 12, 31),
        "value": "30",
        "value_unit": "lb",
    }
]

# After partial achievement, revise goal
goals_updated = [
    {
        "description": "Lose 30 pounds (15 lb achieved)",
        "status": "active",
        "start_date": date(2024, 1, 1),
        "target_date": date(2024, 12, 31),
        "value": "15",  # Remaining amount
        "value_unit": "lb",
    }
]
```

## Common Pitfalls

1. **Vague Goals:** Avoid non-specific goals without measurable outcomes
2. **Missing Dates:** Always include start and target dates when establishing goals
3. **Unrealistic Targets:** Set achievable goals appropriate for patient circumstances
4. **Ignoring Patient Input:** Include patient-identified goals alongside clinical targets
5. **Status Not Updated:** Keep goal status current (mark completed goals as complete)
6. **Missing Units:** Always specify units for quantitative goals (lb, %, mg/dL, etc.)
7. **Too Many Goals:** Focus on 3-5 key priorities rather than overwhelming list
8. **No Follow-up Plan:** Link goals to specific interventions in Plan of Treatment section
