# Mental Status Section

**Template ID:** `2.16.840.1.113883.10.20.22.2.56`
**Version:** 2015-08-01 (R2.1 | R2.0)
**Badge:** Extended Section

## Overview

The **Mental Status Section (V2)** contains observations and evaluations related to a patient's psychological and mental competency. It includes assessments of appearance, attitude, behavior, mood and affect, speech and language, thought process, thought content, perception, cognition, insight, and judgment.

This section is essential for:
- Psychiatric and psychological evaluations
- Cognitive assessments (memory, orientation, attention)
- Documenting mental health conditions
- Tracking mental status changes over time
- Care planning for patients with cognitive or psychiatric conditions

Mental status can be documented as individual observations or grouped into organizers by category (e.g., Cognition, Mood and Affect, Behavior).

## Template Details

### Identifiers
- **Root:** `2.16.840.1.113883.10.20.22.2.56`
- **Extension:** `2015-08-01`
- **LOINC Code:** `10190-7` (Mental Status)

### Conformance Requirements
- **SHALL** contain exactly one [1..1] `templateId` (CONF:1198-28293)
- **SHALL** contain exactly one [1..1] `code` with code="10190-7" from LOINC (CONF:1198-28295)
- **SHALL** contain exactly one [1..1] `title` (CONF:1198-28297)
- **SHALL** contain exactly one [1..1] `text` (narrative block) (CONF:1198-28298)
- **MAY** contain zero or more [0..*] `entry` with Mental Status Organizer (CONF:1198-28301)
- **MAY** contain zero or more [0..*] `entry` with Mental Status Observation (CONF:1198-28305)
- **MAY** contain zero or more [0..*] `entry` with Assessment Scale Observation (CONF:1198-28313)

### Cardinality
- **Section:** Optional
- **Organizers:** Optional (0..*)
- **Observations:** Optional (0..*)
- **Either organizers or observations (or both) should be present**

## Protocol Requirements

The section uses two protocols from `ccdakit.protocols.mental_status`:

### MentalStatusObservationProtocol (individual findings)

```python
@property
def category(self) -> str:
    """Category: 'Mood and Affect', 'Cognition', 'Behavior', etc."""

@property
def category_code(self) -> Optional[str]:
    """Code for category (ICF or LOINC preferred)"""

@property
def category_code_system(self) -> Optional[str]:
    """Code system: 'ICF', 'LOINC', or 'SNOMED'"""

@property
def value(self) -> str:
    """Observed value/finding (e.g., 'Depressed mood', 'Alert and oriented')"""

@property
def value_code(self) -> Optional[str]:
    """SNOMED CT code for the observed value"""

@property
def observation_date(self) -> date | datetime:
    """Date/time when observation was made"""

@property
def status(self) -> str:
    """Status: 'active', 'inactive', 'completed'"""

@property
def persistent_id(self) -> Optional[PersistentIDProtocol]:
    """Persistent ID across document versions"""
```

### MentalStatusOrganizerProtocol (grouped findings)

```python
@property
def category(self) -> str:
    """Category name: 'Cognition', 'Mood and Affect', 'Behavior', etc."""

@property
def category_code(self) -> str:
    """Code for the category (ICF or LOINC preferred)"""

@property
def category_code_system(self) -> str:
    """Code system: 'ICF' or 'LOINC'"""

@property
def observations(self) -> list[MentalStatusObservationProtocol]:
    """List of mental status observations in this category"""

@property
def effective_time_low(self) -> Optional[date | datetime]:
    """Start of time span for observations"""

@property
def effective_time_high(self) -> Optional[date | datetime]:
    """End of time span for observations"""

@property
def persistent_id(self) -> Optional[PersistentIDProtocol]:
    """Persistent ID across document versions"""
```

## Code Example

### Basic Usage with Individual Observations

```python
from datetime import datetime
from ccdakit import MentalStatusSection, CDAVersion

# Define individual mental status observations
observations = [
    {
        "category": "Mood and Affect",
        "value": "Depressed mood",
        "value_code": "366979004",
        "observation_date": datetime(2024, 3, 15, 10, 30),
        "status": "active",
    },
    {
        "category": "Cognition",
        "value": "Alert and oriented x3",
        "value_code": "248234008",
        "observation_date": datetime(2024, 3, 15, 10, 45),
        "status": "completed",
    },
    {
        "category": "Behavior",
        "value": "Cooperative",
        "value_code": "225331004",
        "observation_date": datetime(2024, 3, 15, 11, 0),
        "status": "completed",
    }
]

# Create section
section = MentalStatusSection(
    observations=observations,
    version=CDAVersion.R2_1
)

# Generate XML
xml_element = section.to_element()
```

### Using Organizers to Group Observations

```python
# Define mental status organizers
organizers = [
    {
        "category": "Cognition",
        "category_code": "b1",
        "category_code_system": "ICF",
        "observations": [
            {
                "category": "Cognition",
                "value": "Alert",
                "value_code": "248234008",
                "observation_date": datetime(2024, 3, 20, 9, 0),
                "status": "completed",
            },
            {
                "category": "Cognition",
                "value": "Oriented to person, place, and time",
                "value_code": "285854004",
                "observation_date": datetime(2024, 3, 20, 9, 15),
                "status": "completed",
            },
            {
                "category": "Cognition",
                "value": "Memory intact",
                "value_code": "225488001",
                "observation_date": datetime(2024, 3, 20, 9, 30),
                "status": "completed",
            }
        ]
    },
    {
        "category": "Mood and Affect",
        "category_code": "b152",
        "category_code_system": "ICF",
        "observations": [
            {
                "category": "Mood and Affect",
                "value": "Anxious mood",
                "value_code": "48694002",
                "observation_date": datetime(2024, 3, 20, 10, 0),
                "status": "active",
            },
            {
                "category": "Mood and Affect",
                "value": "Flat affect",
                "value_code": "27268008",
                "observation_date": datetime(2024, 3, 20, 10, 15),
                "status": "active",
            }
        ]
    }
]

section = MentalStatusSection(organizers=organizers)
```

### Combined Observations and Organizers

```python
# Mix standalone observations with grouped organizers
observations = [
    {
        "category": "General",
        "value": "Well-groomed appearance",
        "observation_date": datetime(2024, 3, 18, 14, 0),
        "status": "completed",
    }
]

organizers = [
    {
        "category": "Cognition",
        "category_code": "b1",
        "category_code_system": "ICF",
        "observations": [
            {
                "category": "Cognition",
                "value": "Alert and oriented",
                "observation_date": datetime(2024, 3, 18, 14, 15),
                "status": "completed",
            }
        ]
    }
]

section = MentalStatusSection(
    observations=observations,
    organizers=organizers
)
```

### Empty Section

```python
# Create section with no data
section = MentalStatusSection(
    observations=[],
    organizers=[],
    version=CDAVersion.R2_1
)

# Generates section with narrative: "No mental status observations recorded"
```

### Comprehensive Psychiatric Evaluation

```python
organizers = [
    {
        "category": "Appearance",
        "category_code": "b1801",
        "category_code_system": "ICF",
        "observations": [
            {
                "category": "Appearance",
                "value": "Well-groomed",
                "value_code": "248167002",
                "observation_date": datetime(2024, 2, 10, 9, 0),
                "status": "completed",
            }
        ]
    },
    {
        "category": "Mood and Affect",
        "category_code": "b152",
        "category_code_system": "ICF",
        "observations": [
            {
                "category": "Mood and Affect",
                "value": "Depressed mood",
                "value_code": "366979004",
                "observation_date": datetime(2024, 2, 10, 9, 15),
                "status": "active",
            },
            {
                "category": "Mood and Affect",
                "value": "Blunted affect",
                "value_code": "20602000",
                "observation_date": datetime(2024, 2, 10, 9, 20),
                "status": "active",
            }
        ]
    },
    {
        "category": "Thought Process",
        "category_code": "b1601",
        "category_code_system": "ICF",
        "observations": [
            {
                "category": "Thought Process",
                "value": "Linear and goal-directed",
                "value_code": "225482006",
                "observation_date": datetime(2024, 2, 10, 9, 30),
                "status": "completed",
            }
        ]
    },
    {
        "category": "Cognition",
        "category_code": "b1",
        "category_code_system": "ICF",
        "observations": [
            {
                "category": "Cognition",
                "value": "Alert and oriented x4",
                "value_code": "248234008",
                "observation_date": datetime(2024, 2, 10, 9, 45),
                "status": "completed",
            },
            {
                "category": "Cognition",
                "value": "Memory intact",
                "value_code": "225488001",
                "observation_date": datetime(2024, 2, 10, 10, 0),
                "status": "completed",
            }
        ]
    }
]

section = MentalStatusSection(organizers=organizers)
```

### With Custom Protocol Implementation

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class MentalStatusObs:
    """Custom observation implementation."""
    category: str
    value: str
    observation_date: datetime
    status: str
    category_code: Optional[str] = None
    category_code_system: Optional[str] = None
    value_code: Optional[str] = None
    persistent_id: Optional[object] = None

@dataclass
class MentalStatusOrg:
    """Custom organizer implementation."""
    category: str
    category_code: str
    category_code_system: str
    observations: List[MentalStatusObs]
    effective_time_low: Optional[datetime] = None
    effective_time_high: Optional[datetime] = None
    persistent_id: Optional[object] = None

# Create organizers
organizers = [
    MentalStatusOrg(
        category="Cognition",
        category_code="b1",
        category_code_system="ICF",
        observations=[
            MentalStatusObs(
                category="Cognition",
                value="Short-term memory impaired",
                value_code="247592009",
                observation_date=datetime(2024, 3, 25, 11, 0),
                status="active",
            )
        ]
    )
]

section = MentalStatusSection(organizers=organizers)
```

## Official Reference

For complete specification details, refer to:
- **C-CDA Online:** [Mental Status Section (V2)](http://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.56.html)
- **Local Reference:** `references/C-CDA_2.1/templates/2.16.840.1.113883.10.20.22.2.56.html`

## Best Practices

### 1. Organize by Category
Group related mental status observations into logical categories:

```python
categories = [
    "Appearance",
    "Behavior",
    "Mood and Affect",
    "Speech and Language",
    "Thought Process",
    "Thought Content",
    "Perception",
    "Cognition",
    "Insight",
    "Judgment"
]
```

### 2. Use Standard Code Systems
```python
# ICF (International Classification of Functioning) for categories
"category_code_system": "ICF"

# SNOMED CT for observed values
"value_code_system": "SNOMED"
```

### 3. Complete Mental Status Exam
```python
# Include all key components of MSE
mse_categories = {
    "Appearance": "b1801",           # ICF
    "Behavior": "d7",                # ICF
    "Mood and Affect": "b152",       # ICF
    "Speech": "b3",                  # ICF
    "Thought Process": "b1601",      # ICF
    "Thought Content": "b1602",      # ICF
    "Perception": "b156",            # ICF
    "Cognition": "b1",               # ICF
    "Insight": "b1644",              # ICF
    "Judgment": "b1645",             # ICF
}
```

### 4. Cognitive Assessment Components
```python
cognition_observations = [
    "Alert and oriented x4",
    "Attention and concentration intact",
    "Short-term memory intact",
    "Long-term memory intact",
    "Calculation ability normal",
    "Abstract reasoning intact",
]
```

### 5. Mood and Affect Descriptors
```python
mood_values = [
    "Euthymic",
    "Depressed",
    "Anxious",
    "Irritable",
    "Euphoric",
    "Labile",
]

affect_values = [
    "Full range",
    "Congruent",
    "Flat",
    "Blunted",
    "Restricted",
    "Inappropriate",
]
```

### 6. Temporal Accuracy
```python
# Always include date/time of observation
{
    "observation_date": datetime(2024, 3, 15, 10, 30),
    "status": "completed",  # Or "active" for ongoing conditions
}
```

### 7. Status Management
```python
# Completed: Point-in-time observation
{"status": "completed"}

# Active: Ongoing mental status issue
{"status": "active"}

# Inactive: Previously observed but no longer present
{"status": "inactive"}
```

### 8. Narrative Generation
The section automatically generates an HTML table with:
- Category (grouped by organizer or observation category)
- Finding/Value with unique ID reference
- Date of observation
- Status (capitalized)

### 9. Mini-Mental State Exam (MMSE)
```python
# Document standardized assessment scores
mmse_organizer = {
    "category": "Cognitive Assessment - MMSE",
    "category_code": "72106-8",  # LOINC code for MMSE
    "category_code_system": "LOINC",
    "observations": [
        {
            "category": "MMSE Total Score",
            "value": "24/30",  # Indicates mild cognitive impairment
            "observation_date": datetime(2024, 3, 15, 10, 0),
            "status": "completed",
        }
    ]
}
```

### 10. Clinical Context
```python
# Add relevant clinical observations
{
    "category": "Cognition",
    "value": "Mild short-term memory impairment, consistent with early dementia",
    "observation_date": datetime(2024, 3, 20, 11, 0),
    "status": "active",
}
```

## Common Mental Status Codes

### ICF Category Codes
- `b1` - Mental functions (general)
- `b152` - Emotional functions (mood and affect)
- `b156` - Perceptual functions
- `b1601` - Form of thought (thought process)
- `b1602` - Content of thought
- `b164` - Higher-level cognitive functions

### LOINC Codes
- `10190-7` - Mental status (section code)
- `72106-8` - MMSE total score
- `52491-8` - Brief psychiatric rating scale

### Common SNOMED CT Value Codes
- `248234008` - Alert
- `285854004` - Oriented
- `366979004` - Depressed mood
- `48694002` - Anxious mood
- `27268008` - Flat affect
- `225488001` - Memory intact
- `247592009` - Memory impaired

## Common Pitfalls

1. **Missing Categories:** Don't document only cognition; include mood, behavior, etc.
2. **Incomplete Assessment:** Document all components of mental status exam
3. **Missing Dates:** Always include when observation was made
4. **Vague Descriptions:** Use specific, clinical terminology
5. **No Baseline:** Document baseline mental status for comparison
6. **Mixing Current and Historical:** Keep current mental status separate from history
7. **Static Documentation:** Update mental status as patient condition changes
8. **Missing Standardized Assessments:** Include MMSE, PHQ-9, or other validated tools
9. **Inconsistent Observations:** Use consistent terminology across assessments
10. **Wrong Status:** Use "completed" for point-in-time observations, "active" for ongoing conditions
