# Health Concerns Section

**Template ID:** `2.16.840.1.113883.10.20.22.2.58`
**Version:** 2015-08-01 (R2.1 | R2.0)
**Badge:** Extended Section

## Overview

The **Health Concerns Section (V2)** contains data that describes an interest or worry about a health state or process that could possibly require attention, intervention, or management. A Health Concern is a health-related matter that is of interest, importance, or worry to someone who may be the patient, patient's family or patient's health care provider.

Health concerns are more comprehensive than problems. A health concern can include:
- Current problems (e.g., diabetes, hypertension)
- Past problems that continue to require monitoring
- Risk factors (e.g., family history of breast cancer)
- Social determinants of health (e.g., food insecurity, housing instability)
- Patient worries (e.g., fear of falling, anxiety about diagnosis)

This section enables a holistic view of factors affecting patient health beyond traditional diagnoses.

## Template Details

### Identifiers
- **Root:** `2.16.840.1.113883.10.20.22.2.58`
- **Extension:** `2015-08-01`
- **LOINC Code:** `75310-3` (Health concerns document)

### Conformance Requirements
- **MAY** contain `@nullFlavor="NI"` if no information available (CONF:1198-32802)
- **SHALL** contain exactly one [1..1] `templateId` (CONF:1198-28804)
- **SHALL** contain exactly one [1..1] `code` with code="75310-3" from LOINC (CONF:1198-28806)
- **SHALL** contain exactly one [1..1] `title` (CONF:1198-28809)
- **SHALL** contain exactly one [1..1] `text` (narrative block) (CONF:1198-28810)
- If `@nullFlavor` is not present, **SHALL** contain at least one [1..*] `entry` (CONF:1198-30768)
- Each `entry` **SHALL** contain exactly one [1..1] Health Concern Act (V2) (CONF:1198-30768)

### Cardinality
- **Section:** Optional
- **Entries:** Required if not using nullFlavor (1..*)
- **Health Concern Acts:** One per entry

## Protocol Requirements

The section uses the `HealthConcernProtocol` from `ccdakit.protocols.health_concern`:

### Required Properties
```python
@property
def name(self) -> str:
    """Human-readable health concern name/description"""

@property
def status(self) -> str:
    """Status: 'active', 'suspended', 'aborted', 'completed'"""
```

### Optional Properties
```python
@property
def effective_time_low(self) -> Optional[date]:
    """Date when concern started"""

@property
def effective_time_high(self) -> Optional[date]:
    """Date when concern ended (None if ongoing)"""

@property
def persistent_id(self) -> Optional[PersistentIDProtocol]:
    """Persistent ID across document versions"""

@property
def observations(self) -> Sequence[HealthConcernObservationProtocol]:
    """Related observations (problems, allergies, etc.)"""

@property
def author_is_patient(self) -> bool:
    """Whether this is a patient concern (vs. provider concern)"""
```

### Observation Protocol (for related observations)
```python
@property
def observation_type(self) -> str:
    """Type: 'problem', 'allergy', 'social_history', etc."""

@property
def code(self) -> str:
    """Observation code (SNOMED, LOINC, etc.)"""

@property
def code_system(self) -> str:
    """Code system identifier"""

@property
def display_name(self) -> str:
    """Human-readable display name"""
```

## Code Example

### Basic Usage

```python
from datetime import date
from ccdakit import HealthConcernsSection, CDAVersion

# Define health concerns
concerns = [
    {
        "name": "Risk of falls due to balance issues",
        "status": "active",
        "effective_time_low": date(2024, 1, 15),
        "observations": [
            {
                "observation_type": "problem",
                "code": "282299006",
                "code_system": "SNOMED",
                "display_name": "Difficulty walking",
            }
        ],
        "author_is_patient": False,
    },
    {
        "name": "Food insecurity affecting diabetes management",
        "status": "active",
        "effective_time_low": date(2023, 11, 1),
        "observations": [
            {
                "observation_type": "social_history",
                "code": "733423003",
                "code_system": "SNOMED",
                "display_name": "Food insecurity",
            }
        ],
        "author_is_patient": True,
    },
]

# Create section
section = HealthConcernsSection(
    health_concerns=concerns,
    version=CDAVersion.R2_1
)

# Generate XML
xml_element = section.to_element()
```

### Empty Section (No Health Concerns)

```python
# Create section with no concerns
section = HealthConcernsSection(
    health_concerns=[],
    version=CDAVersion.R2_1
)

# Generates section with narrative: "No health concerns"
```

### Section with Null Flavor

```python
# When no information is available
section = HealthConcernsSection(
    health_concerns=[],
    null_flavor="NI",  # No information
    version=CDAVersion.R2_1
)
```

### Complex Health Concern with Multiple Observations

```python
concerns = [
    {
        "name": "Cardiovascular risk management",
        "status": "active",
        "effective_time_low": date(2024, 1, 1),
        "observations": [
            {
                "observation_type": "problem",
                "code": "38341003",
                "code_system": "SNOMED",
                "display_name": "Hypertension",
            },
            {
                "observation_type": "problem",
                "code": "44054006",
                "code_system": "SNOMED",
                "display_name": "Type 2 Diabetes Mellitus",
            },
            {
                "observation_type": "social_history",
                "code": "77176002",
                "code_system": "SNOMED",
                "display_name": "Smoker",
            }
        ],
        "author_is_patient": False,
    }
]

section = HealthConcernsSection(health_concerns=concerns)
```

### Resolved Health Concern

```python
concerns = [
    {
        "name": "Post-surgical infection risk",
        "status": "completed",  # No longer a concern
        "effective_time_low": date(2023, 8, 15),
        "effective_time_high": date(2023, 9, 30),
        "observations": [],
        "author_is_patient": False,
    }
]

section = HealthConcernsSection(health_concerns=concerns)
```

### With Custom Protocol Implementation

```python
from dataclasses import dataclass
from datetime import date
from typing import Optional, Sequence

@dataclass
class HealthConcernObservation:
    """Custom observation implementation."""
    observation_type: str
    code: str
    code_system: str
    display_name: str

@dataclass
class HealthConcern:
    """Custom health concern implementation."""
    name: str
    status: str
    effective_time_low: Optional[date] = None
    effective_time_high: Optional[date] = None
    persistent_id: Optional[object] = None
    observations: Sequence[HealthConcernObservation] = None
    author_is_patient: bool = False

    def __post_init__(self):
        if self.observations is None:
            self.observations = []

# Create concerns
concerns = [
    HealthConcern(
        name="Concern about medication adherence",
        status="active",
        effective_time_low=date(2024, 2, 1),
        observations=[
            HealthConcernObservation(
                observation_type="social_history",
                code="182834008",
                code_system="SNOMED",
                display_name="Drug compliance poor"
            )
        ],
        author_is_patient=True,
    )
]

section = HealthConcernsSection(health_concerns=concerns)
```

### Patient-Identified Concerns

```python
# Patient's own worries and concerns
concerns = [
    {
        "name": "Worried about memory problems",
        "status": "active",
        "effective_time_low": date(2024, 1, 5),
        "observations": [],
        "author_is_patient": True,  # Patient-identified
    },
    {
        "name": "Concerned about family history of cancer",
        "status": "active",
        "effective_time_low": date(2023, 6, 1),
        "observations": [],
        "author_is_patient": True,
    }
]

section = HealthConcernsSection(health_concerns=concerns)
```

## Official Reference

For complete specification details, refer to:
- **C-CDA Online:** [Health Concerns Section (V2)](http://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.58.html)
- **Local Reference:** `references/C-CDA_2.1/templates/2.16.840.1.113883.10.20.22.2.58.html`

## Best Practices

### 1. Distinguish from Problem List
```python
# Problem List: Diagnosed conditions
problems = ["Type 2 Diabetes Mellitus", "Hypertension"]

# Health Concerns: Broader issues requiring attention
concerns = [
    "Diabetes management complicated by food insecurity",
    "Fall risk due to multiple medications",
    "Depression affecting diabetes self-care"
]
```

### 2. Include Social Determinants
```python
# Document social factors affecting health
concerns = [
    {
        "name": "Housing instability affecting medication storage",
        "status": "active",
        "observations": [
            {
                "observation_type": "social_history",
                "code": "32911000",
                "code_system": "SNOMED",
                "display_name": "Homeless",
            }
        ],
        "author_is_patient": False,
    }
]
```

### 3. Patient vs Provider Concerns
```python
# Provider-identified concern
{
    "name": "Declining renal function requiring monitoring",
    "author_is_patient": False,  # Provider concern
}

# Patient-identified concern
{
    "name": "Anxiety about upcoming surgery",
    "author_is_patient": True,  # Patient concern
}
```

### 4. Status Management
```python
# Active: Current concern requiring attention
{"status": "active"}

# Completed: No longer a concern
{"status": "completed", "effective_time_high": date(2024, 3, 1)}

# Suspended: Temporarily not being addressed
{"status": "suspended"}

# Aborted: Abandoned or invalidated
{"status": "aborted"}
```

### 5. Link to Related Observations
```python
# Connect concern to specific clinical findings
{
    "name": "Cardiovascular disease risk",
    "status": "active",
    "observations": [
        {"observation_type": "problem", "display_name": "Hypertension", ...},
        {"observation_type": "problem", "display_name": "Hyperlipidemia", ...},
        {"observation_type": "social_history", "display_name": "Current smoker", ...},
    ]
}
```

### 6. Temporal Clarity
```python
# Document when concern started
{
    "effective_time_low": date(2024, 1, 15),  # When identified
    "effective_time_high": None,  # Ongoing
}

# Document when concern resolved
{
    "effective_time_low": date(2023, 6, 1),
    "effective_time_high": date(2024, 2, 15),  # No longer concerning
}
```

### 7. Narrative Generation
The section automatically generates an HTML table with:
- Health concern name with unique ID reference
- Status (capitalized)
- Effective time range
- Related observations (as a list)
- Concern type (Patient or Provider)

### 8. Comprehensive Care Planning
```python
# Link concerns to goals and plans
health_concerns = [
    {
        "name": "Risk of diabetic foot ulcer",
        "status": "active",
        ...
    }
]

goals = [
    {"description": "Maintain intact skin on feet", ...}
]

plan = [
    {"text": "Daily foot inspections", ...}
]
```

### 9. Risk Factors
```python
# Document risk factors as concerns
concerns = [
    {
        "name": "High risk for osteoporotic fracture",
        "status": "active",
        "observations": [
            {
                "observation_type": "problem",
                "display_name": "Osteoporosis",
                "code": "64859006",
                "code_system": "SNOMED",
            }
        ],
        "author_is_patient": False,
    }
]
```

### 10. Family History Concerns
```python
# Include family history concerns
concerns = [
    {
        "name": "Family history of breast cancer - requires surveillance",
        "status": "active",
        "effective_time_low": date(2024, 1, 1),
        "observations": [],
        "author_is_patient": False,
    }
]
```

## Common Pitfalls

1. **Confusing with Problem List:** Health concerns are broader than diagnoses
2. **Missing Context:** Always link concerns to specific observations when applicable
3. **Ignoring Patient Input:** Include patient-identified concerns alongside clinical ones
4. **Incomplete Status:** Update status when concerns are resolved or change
5. **Missing Social Factors:** Don't overlook social determinants of health
6. **No Timeline:** Document when concerns were identified
7. **Too Granular:** Focus on overarching concerns, not individual symptoms
8. **Disconnected from Care Plan:** Link concerns to goals and interventions
9. **Author Attribution:** Clearly identify whether concern is patient- or provider-identified
10. **Static Documentation:** Update health concerns as patient situation changes
