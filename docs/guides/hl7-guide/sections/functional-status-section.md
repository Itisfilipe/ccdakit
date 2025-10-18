# Functional Status Section

**Template ID:** `2.16.840.1.113883.10.20.22.2.14`
**Version:** 2014-06-09 (R2.1 | R2.0)
**Badge:** Extended Section

## Overview

The **Functional Status Section** contains observations and assessments of a patient's physical abilities and limitations. It captures information about Activities of Daily Living (ADLs), Instrumental Activities of Daily Living (IADLs), mobility, self-care capabilities, and functional problems that impact the patient's independence and quality of life.

This section is essential for:
- Care planning and rehabilitation
- Assessing need for assistance or adaptive equipment
- Tracking functional improvement or decline over time
- Post-acute care planning and discharge planning
- Determining appropriate level of care

## Template Details

### Identifiers
- **Root:** `2.16.840.1.113883.10.20.22.2.14`
- **Extension:** `2014-06-09`
- **LOINC Code:** `47420-5` (Functional Status)

### Conformance Requirements
- **SHALL** contain exactly one [1..1] `templateId` (CONF:1098-7920)
- **SHALL** contain exactly one [1..1] `code` with code="47420-5" from LOINC (CONF:1098-14578)
- **SHALL** contain exactly one [1..1] `title` (CONF:1098-7922)
- **SHALL** contain exactly one [1..1] `text` (narrative block) (CONF:1098-7923)
- **MAY** contain zero or more [0..*] `entry` elements (CONF:1098-14414)
- Each `entry` **SHALL** contain exactly one [1..1] Functional Status Organizer (CONF:1098-14415)

### Cardinality
- **Section:** Optional
- **Entries:** Optional (0..*)
- **Functional Status Organizers:** One per entry

## Protocol Requirements

The section uses two protocols from `ccdakit.protocols.functional_status`:

### FunctionalStatusOrganizerProtocol (groups observations by category)

```python
@property
def category(self) -> str:
    """Category: 'Mobility', 'Self-Care', 'Communication', etc."""

@property
def category_code(self) -> str:
    """Code for the category (ICF or LOINC recommended)"""

@property
def category_code_system(self) -> Optional[str]:
    """Code system OID for category"""

@property
def observations(self) -> Sequence[FunctionalStatusObservationProtocol]:
    """List of functional status observations in this category"""
```

### FunctionalStatusObservationProtocol (individual assessment)

```python
@property
def type(self) -> str:
    """Type/description: 'Ambulation', 'Bathing', 'Feeding', etc."""

@property
def code(self) -> str:
    """Code for the functional status (SNOMED CT recommended)"""

@property
def code_system(self) -> Optional[str]:
    """Code system OID (default: SNOMED CT)"""

@property
def value(self) -> str:
    """Coded value representing the functional status"""

@property
def value_code(self) -> str:
    """Code for the value (SNOMED CT recommended)"""

@property
def value_code_system(self) -> Optional[str]:
    """Code system OID for value"""

@property
def date(self) -> date | datetime:
    """Date and time the observation was made"""

@property
def interpretation(self) -> Optional[str]:
    """Optional interpretation of the status"""
```

## Code Example

### Basic Usage

```python
from datetime import datetime
from ccdakit import FunctionalStatusSection, CDAVersion

# Define functional status assessments organized by category
organizers = [
    {
        "category": "Mobility",
        "category_code": "d4",
        "category_code_system": "ICF",
        "observations": [
            {
                "type": "Ambulation",
                "code": "284003005",
                "code_system": "SNOMED",
                "value": "Independent",
                "value_code": "371153006",
                "value_code_system": "SNOMED",
                "date": datetime(2024, 3, 15, 10, 30),
            },
            {
                "type": "Transfer",
                "code": "282290006",
                "code_system": "SNOMED",
                "value": "Requires minimal assistance",
                "value_code": "371154000",
                "value_code_system": "SNOMED",
                "date": datetime(2024, 3, 15, 10, 45),
            }
        ]
    },
    {
        "category": "Self-Care",
        "category_code": "d5",
        "category_code_system": "ICF",
        "observations": [
            {
                "type": "Bathing",
                "code": "284003006",
                "code_system": "SNOMED",
                "value": "Requires assistance",
                "value_code": "371152001",
                "value_code_system": "SNOMED",
                "date": datetime(2024, 3, 15, 11, 0),
            },
            {
                "type": "Dressing",
                "code": "165235000",
                "code_system": "SNOMED",
                "value": "Independent",
                "value_code": "371153006",
                "value_code_system": "SNOMED",
                "date": datetime(2024, 3, 15, 11, 15),
            }
        ]
    }
]

# Create section
section = FunctionalStatusSection(
    organizers=organizers,
    version=CDAVersion.R2_1
)

# Generate XML
xml_element = section.to_element()
```

### Empty Section (No Functional Status Data)

```python
# Create section with no data
section = FunctionalStatusSection(
    organizers=[],
    version=CDAVersion.R2_1
)

# Generates section with narrative: "No functional status recorded"
```

### Activities of Daily Living (ADLs)

```python
adl_organizer = {
    "category": "Activities of Daily Living",
    "category_code": "57255-8",
    "category_code_system": "LOINC",
    "observations": [
        {
            "type": "Eating",
            "code": "288844009",
            "code_system": "SNOMED",
            "value": "Independent",
            "value_code": "371153006",
            "value_code_system": "SNOMED",
            "date": datetime(2024, 3, 20, 9, 0),
        },
        {
            "type": "Toileting",
            "code": "284880004",
            "code_system": "SNOMED",
            "value": "Requires supervision",
            "value_code": "371154000",
            "value_code_system": "SNOMED",
            "date": datetime(2024, 3, 20, 9, 15),
        },
        {
            "type": "Grooming",
            "code": "284003007",
            "code_system": "SNOMED",
            "value": "Independent",
            "value_code": "371153006",
            "value_code_system": "SNOMED",
            "date": datetime(2024, 3, 20, 9, 30),
        }
    ]
}

section = FunctionalStatusSection(organizers=[adl_organizer])
```

### Instrumental Activities of Daily Living (IADLs)

```python
iadl_organizer = {
    "category": "Instrumental Activities of Daily Living",
    "category_code": "57256-6",
    "category_code_system": "LOINC",
    "observations": [
        {
            "type": "Meal preparation",
            "code": "284006004",
            "code_system": "SNOMED",
            "value": "Unable to perform",
            "value_code": "371150009",
            "value_code_system": "SNOMED",
            "date": datetime(2024, 3, 18, 14, 0),
        },
        {
            "type": "Managing medications",
            "code": "284007008",
            "code_system": "SNOMED",
            "value": "Requires assistance",
            "value_code": "371152001",
            "value_code_system": "SNOMED",
            "date": datetime(2024, 3, 18, 14, 15),
        },
        {
            "type": "Using telephone",
            "code": "284008003",
            "code_system": "SNOMED",
            "value": "Independent",
            "value_code": "371153006",
            "value_code_system": "SNOMED",
            "date": datetime(2024, 3, 18, 14, 30),
        }
    ]
}

section = FunctionalStatusSection(organizers=[iadl_organizer])
```

### With Custom Protocol Implementation

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Sequence

@dataclass
class FunctionalObservation:
    """Custom observation implementation."""
    type: str
    code: str
    code_system: Optional[str]
    value: str
    value_code: str
    value_code_system: Optional[str]
    date: datetime
    interpretation: Optional[str] = None

@dataclass
class FunctionalOrganizer:
    """Custom organizer implementation."""
    category: str
    category_code: str
    category_code_system: Optional[str]
    observations: Sequence[FunctionalObservation]

# Create organizers
organizers = [
    FunctionalOrganizer(
        category="Mobility",
        category_code="d4",
        category_code_system="ICF",
        observations=[
            FunctionalObservation(
                type="Walking",
                code="228439009",
                code_system="SNOMED",
                value="Walks with walker",
                value_code="371154000",
                value_code_system="SNOMED",
                date=datetime(2024, 3, 25, 10, 0),
            )
        ]
    )
]

section = FunctionalStatusSection(organizers=organizers)
```

### Post-Stroke Functional Assessment

```python
post_stroke_organizer = {
    "category": "Mobility and Self-Care Post-Stroke",
    "category_code": "d4",
    "category_code_system": "ICF",
    "observations": [
        {
            "type": "Upper extremity function - Right",
            "code": "249912004",
            "code_system": "SNOMED",
            "value": "Severely impaired",
            "value_code": "24484000",
            "value_code_system": "SNOMED",
            "date": datetime(2024, 2, 10, 9, 0),
        },
        {
            "type": "Lower extremity function - Right",
            "code": "249913009",
            "code_system": "SNOMED",
            "value": "Moderately impaired",
            "value_code": "371152001",
            "value_code_system": "SNOMED",
            "date": datetime(2024, 2, 10, 9, 15),
        },
        {
            "type": "Gait",
            "code": "228439009",
            "code_system": "SNOMED",
            "value": "Requires walker",
            "value_code": "371154000",
            "value_code_system": "SNOMED",
            "date": datetime(2024, 2, 10, 9, 30),
        }
    ]
}

section = FunctionalStatusSection(organizers=[post_stroke_organizer])
```

## Official Reference

For complete specification details, refer to:
- **C-CDA Online:** [Functional Status Section](http://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.14.html)
- **Local Reference:** `references/C-CDA_2.1/templates/2.16.840.1.113883.10.20.22.2.14.html`

## Best Practices

### 1. Organize by Category
Group related functional assessments into logical categories:

```python
# Good: Organized by functional domain
mobility_organizer = {
    "category": "Mobility",
    "observations": [walking, transfers, stairs, ...]
}

self_care_organizer = {
    "category": "Self-Care",
    "observations": [bathing, dressing, grooming, ...]
}
```

### 2. Use Standard Code Systems
```python
# Prefer ICF (International Classification of Functioning) for categories
"category_code_system": "ICF"

# Use SNOMED CT for observations and values
"code_system": "SNOMED"
"value_code_system": "SNOMED"
```

### 3. Standard Independence Levels
```python
# Common functional status values
independence_levels = {
    "Independent": "371153006",
    "Requires minimal assistance": "371154000",
    "Requires moderate assistance": "371152001",
    "Requires maximal assistance": "371151008",
    "Unable to perform": "371150009",
    "Dependent": "371149003",
}
```

### 4. Complete ADL Assessment
```python
# Include all basic ADLs
basic_adls = [
    "Eating/Feeding",
    "Bathing",
    "Dressing",
    "Toileting",
    "Transferring",
    "Walking/Mobility",
]
```

### 5. Complete IADL Assessment
```python
# Include instrumental ADLs for community-dwelling patients
instrumental_adls = [
    "Meal preparation",
    "Housekeeping",
    "Managing medications",
    "Managing finances",
    "Shopping",
    "Using transportation",
    "Using telephone",
    "Laundry",
]
```

### 6. Temporal Accuracy
```python
# Always include date/time of assessment
{
    "date": datetime(2024, 3, 15, 10, 30),  # Specific date/time
}

# For tracking changes over time
initial_assessment = datetime(2024, 1, 15, 9, 0)
follow_up_assessment = datetime(2024, 3, 15, 9, 0)
```

### 7. Clinical Context
```python
# Add interpretation when relevant
{
    "type": "Ambulation",
    "value": "Requires walker",
    "interpretation": "Patient has improved from wheelchair to walker since admission"
}
```

### 8. Narrative Generation
The section automatically generates an HTML table with:
- Category (grouped observations)
- Functional status type with unique ID reference
- Value (functional level)
- Date/Time of assessment

### 9. Assistive Devices
```python
# Document use of assistive devices
observations = [
    {
        "type": "Ambulation",
        "value": "Independent with walker",
        "value_code": "371153006",
        ...
    },
    {
        "type": "Bathing",
        "value": "Independent with shower chair and grab bars",
        "value_code": "371153006",
        ...
    }
]
```

### 10. Comprehensive Assessment
```python
# Include multiple functional domains
organizers = [
    mobility_organizer,      # Walking, transfers, stairs
    self_care_organizer,     # ADLs
    iadl_organizer,          # IADLs
    communication_organizer, # Speech, hearing, vision
    cognition_organizer,     # Memory, decision-making
]

section = FunctionalStatusSection(organizers=organizers)
```

## Common Functional Status Codes

### ICF Category Codes
- `d4` - Mobility
- `d5` - Self-care
- `d3` - Communication
- `d1` - Learning and applying knowledge

### LOINC Category Codes
- `57255-8` - Activities of Daily Living (ADLs)
- `57256-6` - Instrumental Activities of Daily Living (IADLs)
- `83254-3` - Mobility assessment

### SNOMED CT Value Codes
- `371153006` - Independent
- `371154000` - Requires minimal assistance
- `371152001` - Requires moderate assistance
- `371151008` - Requires maximal assistance
- `371150009` - Unable to perform
- `371149003` - Totally dependent

## Common Pitfalls

1. **Missing Categories:** Don't lump all observations together; organize by functional domain
2. **Incomplete Assessment:** Include all relevant ADLs and IADLs
3. **Missing Dates:** Always include when assessment was performed
4. **Vague Values:** Use standardized independence levels rather than free text
5. **No Baseline:** Document baseline functional status for comparison
6. **Ignoring Assistive Devices:** Note when patient uses equipment or adaptations
7. **Static Documentation:** Update functional status as patient condition changes
8. **Missing Clinical Context:** Explain changes in functional status
9. **Inconsistent Units:** Use consistent scales across assessments
10. **Wrong Code System:** Use appropriate code systems (ICF for categories, SNOMED for observations)
