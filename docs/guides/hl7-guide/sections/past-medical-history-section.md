# Past Medical History Section

**Template ID:** `2.16.840.1.113883.10.20.22.2.20`
**Version:** 2015-08-01 (R2.1) | R2.0
**Badge:** Extended Section

## Overview

The **Past Medical History Section** contains a record of the patient's past complaints, problems, and diagnoses. It includes data from the patient's medical past up to the current complaint or reason for seeking medical care. This section helps clinicians understand the patient's historical health conditions that may impact current care decisions.

This section differs from the Problem List Section in that it focuses on **historical conditions** rather than current active problems. It provides essential context for understanding the patient's overall health trajectory.

## Template Details

### Identifiers
- **Root:** `2.16.840.1.113883.10.20.22.2.20`
- **Extension:** `2015-08-01` (R2.1)
- **LOINC Code:** `11348-0` (History of Past Illness)

### Conformance Requirements
- **SHALL** contain exactly one [1..1] `templateId` (CONF:1198-7828)
- **SHALL** contain exactly one [1..1] `code` with code="11348-0" from LOINC (CONF:1198-15474)
- **SHALL** contain exactly one [1..1] `title` (CONF:1198-7830)
- **SHALL** contain exactly one [1..1] `text` (narrative block) (CONF:1198-7831)
- **MAY** contain zero or more [0..*] `entry` elements (CONF:1198-8791)
- Each `entry` **SHALL** contain exactly one [1..1] Problem Observation (CONF:1198-15476)

### Cardinality
- **Section:** Required if documenting past medical history
- **Entries:** Optional (0..*)
- **Problem Observations:** Optional per entry

## Protocol Requirements

The section uses the `ProblemProtocol` from `ccdakit.protocols.problem`:

### Required Properties
```python
@property
def name(self) -> str:
    """Problem/condition name (e.g., 'Type 2 Diabetes Mellitus')"""

@property
def code(self) -> str:
    """SNOMED CT or ICD-10 code for the problem"""

@property
def code_system(self) -> str:
    """Code system: 'SNOMED' or 'ICD-10'"""

@property
def status(self) -> str:
    """Problem status: 'active', 'inactive', 'resolved'"""
```

### Optional Properties
```python
@property
def onset_date(self) -> Optional[date]:
    """Date when the problem started"""

@property
def resolved_date(self) -> Optional[date]:
    """Date when the problem was resolved (if applicable)"""

@property
def display_name(self) -> Optional[str]:
    """Human-readable display name for the code"""
```

## Code Example

### Basic Usage

```python
from datetime import date
from ccdakit import PastMedicalHistorySection, CDAVersion

# Define past medical history problems
problems = [
    {
        "name": "Type 2 Diabetes Mellitus",
        "code": "44054006",
        "code_system": "SNOMED",
        "status": "resolved",
        "onset_date": date(2015, 3, 15),
        "resolved_date": date(2023, 6, 20),
    },
    {
        "name": "Hypertension",
        "code": "38341003",
        "code_system": "SNOMED",
        "status": "active",
        "onset_date": date(2010, 8, 12),
    },
    {
        "name": "Appendectomy",
        "code": "80146002",
        "code_system": "SNOMED",
        "status": "resolved",
        "onset_date": date(2008, 5, 3),
    },
]

# Create section
section = PastMedicalHistorySection(
    problems=problems,
    version=CDAVersion.R2_1
)

# Generate XML
xml_element = section.to_element()
```

### Empty Section (No Past Medical History)

```python
# Create section with no problems
section = PastMedicalHistorySection(
    problems=[],
    version=CDAVersion.R2_1
)

# Generates section with narrative: "No past medical history"
```

### Custom Title

```python
section = PastMedicalHistorySection(
    problems=problems,
    title="Medical History Prior to Current Illness",
    version=CDAVersion.R2_1
)
```

### With Custom Protocol Implementation

```python
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class HistoricalProblem:
    """Custom problem implementation."""
    name: str
    code: str
    code_system: str
    status: str
    onset_date: Optional[date] = None
    resolved_date: Optional[date] = None
    display_name: Optional[str] = None

# Use custom implementation
problems = [
    HistoricalProblem(
        name="Pneumonia",
        code="233604007",
        code_system="SNOMED",
        status="resolved",
        onset_date=date(2019, 12, 5),
        resolved_date=date(2020, 1, 15),
    )
]

section = PastMedicalHistorySection(problems=problems)
```

## Official Reference

For complete specification details, refer to:
- **C-CDA Online:** [Past Medical History Section (V3)](http://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.20.html)
- **Local Reference:** `references/C-CDA_2.1/templates/2.16.840.1.113883.10.20.22.2.20.html`

## Best Practices

### 1. Distinguish from Current Problems
- Use this section for **historical** conditions that are not currently active concerns
- Current active problems should appear in the Problem List Section
- Resolved conditions that still have clinical relevance belong here

### 2. Status Management
```python
# Good: Clear status differentiation
{
    "name": "Gestational Diabetes",
    "status": "resolved",  # No longer applicable
    "resolved_date": date(2020, 8, 15),
}

# Also valid: Historically active but now inactive
{
    "name": "Childhood Asthma",
    "status": "inactive",  # Not currently requiring treatment
    "onset_date": date(2005, 3, 1),
}
```

### 3. Include Relevant Surgical History
```python
# Include past procedures as problems
{
    "name": "Total Knee Replacement",
    "code": "609588000",
    "code_system": "SNOMED",
    "status": "resolved",
    "onset_date": date(2018, 9, 22),
}
```

### 4. Code System Selection
```python
# Prefer SNOMED CT for clinical conditions
{
    "code": "44054006",  # SNOMED CT
    "code_system": "SNOMED",
}

# ICD-10 is acceptable but less granular
{
    "code": "E11.9",  # ICD-10
    "code_system": "ICD-10",
}
```

### 5. Narrative Generation
The section automatically generates an HTML table with:
- Problem name with unique ID reference
- Code and code system
- Status (Active/Inactive/Resolved)
- Onset date
- Resolved date (or "Ongoing" for active problems)

```python
# Empty section generates:
# "No past medical history"

# Non-empty sections generate:
# Complete HTML table with all problem details
```

### 6. Temporal Clarity
```python
# Always provide onset dates when known
problems = [
    {
        "name": "Major Depression",
        "code": "370143000",
        "code_system": "SNOMED",
        "status": "resolved",
        "onset_date": date(2016, 1, 15),  # When it started
        "resolved_date": date(2022, 3, 10),  # When resolved
    }
]
```

### 7. Unknown Dates
```python
# Handle unknown dates appropriately
{
    "name": "Childhood Chicken Pox",
    "code": "38907003",
    "code_system": "SNOMED",
    "status": "resolved",
    "onset_date": None,  # Unknown - will show "Unknown" in narrative
}
```

### 8. Version Compatibility
```python
# R2.1 uses extension
section = PastMedicalHistorySection(
    problems=problems,
    version=CDAVersion.R2_1  # Uses 2015-08-01 extension
)

# R2.0 may not have extension
section = PastMedicalHistorySection(
    problems=problems,
    version=CDAVersion.R2_0  # No extension
)
```

### 9. Integration with Problem List
```python
# Coordinate with Problem List Section
past_problems = [...]  # Historical, resolved conditions
current_problems = [...]  # Active, current concerns

# Use Past Medical History for historical context
past_history = PastMedicalHistorySection(problems=past_problems)

# Use Problem List for current issues
problem_list = ProblemsSection(problems=current_problems)
```

### 10. Clinical Context
```python
# Include conditions that impact current care
problems = [
    {
        "name": "Previous Myocardial Infarction",  # Impacts treatment decisions
        "code": "22298006",
        "code_system": "SNOMED",
        "status": "resolved",
        "onset_date": date(2015, 6, 8),
    },
    {
        "name": "Penicillin Allergy (historical)",  # Critical for drug selection
        "code": "91936005",
        "code_system": "SNOMED",
        "status": "active",  # Still relevant
        "onset_date": date(2000, 1, 1),
    }
]
```

## Common Pitfalls

1. **Mixing Current and Past Problems:** Keep current active problems in the Problem List Section
2. **Missing Status Information:** Always specify whether conditions are active, inactive, or resolved
3. **Inadequate Documentation:** Include both onset and resolved dates when available
4. **Code System Confusion:** Use appropriate code systems (prefer SNOMED CT over ICD-10)
5. **Ignoring Clinical Relevance:** Include only conditions that have bearing on current/future care
