# Family History Section

**Template ID:** `2.16.840.1.113883.10.20.22.2.15`
**Version:** 2015-08-01 (R2.1 | R2.0)
**Badge:** Extended Section

## Overview

The **Family History Section (V3)** contains data defining the patient's genetic relatives in terms of possible or relevant health risk factors that have a potential impact on the patient's healthcare risk profile. Family history provides crucial information for:

- **Risk Assessment:** Identifying hereditary disease risks
- **Preventive Care:** Guiding screening and surveillance recommendations
- **Diagnosis:** Considering familial conditions in differential diagnosis
- **Genetic Counseling:** Supporting decisions about genetic testing
- **Treatment Planning:** Informing medication choices based on family response

Family history includes information about blood relatives' health conditions, age at onset, cause of death, and other clinically relevant factors.

## Template Details

### Identifiers
- **Root:** `2.16.840.1.113883.10.20.22.2.15`
- **Extension:** `2015-08-01`
- **LOINC Code:** `10157-6` (Family History)

### Conformance Requirements
- **SHALL** contain exactly one [1..1] `templateId` (CONF:1198-7932)
- **SHALL** contain exactly one [1..1] `code` with code="10157-6" from LOINC (CONF:1198-15469)
- **SHALL** contain exactly one [1..1] `title` (CONF:1198-7934)
- **SHALL** contain exactly one [1..1] `text` (narrative block) (CONF:1198-7935)
- **MAY** contain zero or more [0..*] `entry` elements (CONF:1198-32430)
- Each `entry` **SHALL** contain exactly one [1..1] Family History Organizer (CONF:1198-32431)

### Cardinality
- **Section:** Optional
- **Entries:** Optional (0..*)
- **Family History Organizers:** One per family member

## Protocol Requirements

The section uses protocols from `ccdakit.protocols.family_history`:

### FamilyMemberHistoryProtocol (organizer for each family member)

```python
@property
def relationship_code(self) -> str:
    """Relationship code: 'FTH'=father, 'MTH'=mother, etc."""

@property
def relationship_display_name(self) -> str:
    """Human-readable relationship: 'Father', 'Mother', etc."""

@property
def subject(self) -> Optional[FamilyMemberSubjectProtocol]:
    """Additional subject details (gender, birth, deceased info)"""

@property
def observations(self) -> list:
    """List of family history observations (conditions)"""

@property
def persistent_id(self) -> Optional[PersistentIDProtocol]:
    """Persistent ID across document versions"""
```

### FamilyMemberSubjectProtocol (demographics)

```python
@property
def administrative_gender_code(self) -> Optional[str]:
    """Gender code: 'M' (Male), 'F' (Female), 'UN' (Undifferentiated)"""

@property
def birth_time(self) -> Optional[date]:
    """Birth date of the family member"""

@property
def deceased_ind(self) -> Optional[bool]:
    """True if deceased, False if living, None if unknown"""

@property
def deceased_time(self) -> Optional[date]:
    """Date when family member died"""
```

### FamilyHistoryObservationProtocol (conditions)

```python
@property
def condition_name(self) -> str:
    """Human-readable condition/problem name"""

@property
def condition_code(self) -> str:
    """SNOMED CT or ICD-10 code for the condition"""

@property
def condition_code_system(self) -> str:
    """Code system: 'SNOMED' or 'ICD-10'"""

@property
def observation_type_code(self) -> Optional[str]:
    """SNOMED CT code for observation type (e.g., 64572001 = Disease)"""

@property
def observation_type_display_name(self) -> Optional[str]:
    """Display name for observation type"""

@property
def effective_time(self) -> Optional[date]:
    """Biologically relevant time for the observation"""

@property
def age_at_onset(self) -> Optional[int]:
    """Age at which condition began (in years)"""

@property
def deceased_age(self) -> Optional[int]:
    """Age at death if deceased (in years)"""

@property
def deceased_cause_code(self) -> Optional[str]:
    """Code for cause of death"""

@property
def deceased_cause_display_name(self) -> Optional[str]:
    """Display name for cause of death"""

@property
def persistent_id(self) -> Optional[PersistentIDProtocol]:
    """Persistent ID across document versions"""
```

## Code Example

### Basic Usage

```python
from datetime import date
from ccdakit import FamilyHistorySection, CDAVersion

# Define family history
family_members = [
    {
        "relationship_code": "FTH",
        "relationship_display_name": "Father",
        "subject": {
            "administrative_gender_code": "M",
            "birth_time": date(1950, 3, 15),
            "deceased_ind": True,
            "deceased_time": date(2015, 8, 22),
        },
        "observations": [
            {
                "condition_name": "Myocardial Infarction",
                "condition_code": "22298006",
                "condition_code_system": "SNOMED",
                "age_at_onset": 58,
                "deceased_age": 65,
                "deceased_cause_code": "22298006",
                "deceased_cause_display_name": "Myocardial Infarction",
            },
            {
                "condition_name": "Type 2 Diabetes Mellitus",
                "condition_code": "44054006",
                "condition_code_system": "SNOMED",
                "age_at_onset": 52,
            }
        ]
    },
    {
        "relationship_code": "MTH",
        "relationship_display_name": "Mother",
        "subject": {
            "administrative_gender_code": "F",
            "birth_time": date(1952, 7, 8),
            "deceased_ind": False,
        },
        "observations": [
            {
                "condition_name": "Breast Cancer",
                "condition_code": "254837009",
                "condition_code_system": "SNOMED",
                "age_at_onset": 62,
            },
            {
                "condition_name": "Hypertension",
                "condition_code": "38341003",
                "condition_code_system": "SNOMED",
                "age_at_onset": 55,
            }
        ]
    }
]

# Create section
section = FamilyHistorySection(
    family_members=family_members,
    version=CDAVersion.R2_1
)

# Generate XML
xml_element = section.to_element()
```

### Empty Section (No Known Family History)

```python
# Create section with no family history
section = FamilyHistorySection(
    family_members=[],
    version=CDAVersion.R2_1
)

# Generates section with narrative: "No known family history"
```

### Family Member with No Documented Conditions

```python
family_members = [
    {
        "relationship_code": "BRO",
        "relationship_display_name": "Brother",
        "subject": {
            "administrative_gender_code": "M",
            "deceased_ind": False,
        },
        "observations": []  # No conditions documented
    }
]

section = FamilyHistorySection(family_members=family_members)
```

### Multiple Siblings

```python
family_members = [
    {
        "relationship_code": "SIS",
        "relationship_display_name": "Sister",
        "subject": {"administrative_gender_code": "F", "deceased_ind": False},
        "observations": [
            {
                "condition_name": "Ovarian Cancer",
                "condition_code": "363443007",
                "condition_code_system": "SNOMED",
                "age_at_onset": 48,
            }
        ]
    },
    {
        "relationship_code": "BRO",
        "relationship_display_name": "Brother",
        "subject": {"administrative_gender_code": "M", "deceased_ind": False},
        "observations": [
            {
                "condition_name": "Coronary Artery Disease",
                "condition_code": "53741008",
                "condition_code_system": "SNOMED",
                "age_at_onset": 52,
            }
        ]
    }
]

section = FamilyHistorySection(family_members=family_members)
```

### Comprehensive Family History

```python
from datetime import date

family_members = [
    # Father - deceased from heart attack
    {
        "relationship_code": "FTH",
        "relationship_display_name": "Father",
        "subject": {
            "administrative_gender_code": "M",
            "birth_time": date(1948, 5, 12),
            "deceased_ind": True,
            "deceased_time": date(2010, 11, 3),
        },
        "observations": [
            {
                "condition_name": "Acute Myocardial Infarction",
                "condition_code": "57054005",
                "condition_code_system": "SNOMED",
                "observation_type_code": "64572001",
                "observation_type_display_name": "Disease",
                "age_at_onset": 62,
                "deceased_age": 62,
                "deceased_cause_code": "57054005",
                "deceased_cause_display_name": "Acute Myocardial Infarction",
            }
        ]
    },

    # Mother - living with diabetes and hypertension
    {
        "relationship_code": "MTH",
        "relationship_display_name": "Mother",
        "subject": {
            "administrative_gender_code": "F",
            "birth_time": date(1951, 9, 25),
            "deceased_ind": False,
        },
        "observations": [
            {
                "condition_name": "Type 2 Diabetes Mellitus",
                "condition_code": "44054006",
                "condition_code_system": "SNOMED",
                "age_at_onset": 58,
            },
            {
                "condition_name": "Essential Hypertension",
                "condition_code": "59621000",
                "condition_code_system": "SNOMED",
                "age_at_onset": 52,
            }
        ]
    },

    # Maternal Grandmother - deceased from stroke
    {
        "relationship_code": "MGRMTH",
        "relationship_display_name": "Maternal Grandmother",
        "subject": {
            "administrative_gender_code": "F",
            "deceased_ind": True,
            "deceased_time": date(1995, 3, 15),
        },
        "observations": [
            {
                "condition_name": "Cerebrovascular Accident (Stroke)",
                "condition_code": "230690007",
                "condition_code_system": "SNOMED",
                "deceased_cause_code": "230690007",
                "deceased_cause_display_name": "Stroke",
            }
        ]
    },

    # Sister - breast cancer survivor
    {
        "relationship_code": "SIS",
        "relationship_display_name": "Sister",
        "subject": {
            "administrative_gender_code": "F",
            "birth_time": date(1978, 2, 14),
            "deceased_ind": False,
        },
        "observations": [
            {
                "condition_name": "Malignant Neoplasm of Breast",
                "condition_code": "254837009",
                "condition_code_system": "SNOMED",
                "age_at_onset": 42,
                "effective_time": date(2020, 6, 1),
            }
        ]
    }
]

section = FamilyHistorySection(family_members=family_members)
```

### With Custom Protocol Implementation

```python
from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List

@dataclass
class FamilyObservation:
    """Custom observation implementation."""
    condition_name: str
    condition_code: str
    condition_code_system: str
    observation_type_code: Optional[str] = None
    observation_type_display_name: Optional[str] = None
    effective_time: Optional[date] = None
    age_at_onset: Optional[int] = None
    deceased_age: Optional[int] = None
    deceased_cause_code: Optional[str] = None
    deceased_cause_display_name: Optional[str] = None
    persistent_id: Optional[object] = None

@dataclass
class FamilySubject:
    """Custom subject implementation."""
    administrative_gender_code: Optional[str] = None
    birth_time: Optional[date] = None
    deceased_ind: Optional[bool] = None
    deceased_time: Optional[date] = None

@dataclass
class FamilyMember:
    """Custom family member implementation."""
    relationship_code: str
    relationship_display_name: str
    observations: List[FamilyObservation] = field(default_factory=list)
    subject: Optional[FamilySubject] = None
    persistent_id: Optional[object] = None

# Create family members
family_members = [
    FamilyMember(
        relationship_code="FTH",
        relationship_display_name="Father",
        subject=FamilySubject(
            administrative_gender_code="M",
            deceased_ind=True,
        ),
        observations=[
            FamilyObservation(
                condition_name="Coronary Artery Disease",
                condition_code="53741008",
                condition_code_system="SNOMED",
                age_at_onset=55,
            )
        ]
    )
]

section = FamilyHistorySection(family_members=family_members)
```

## Official Reference

For complete specification details, refer to:
- **C-CDA Online:** [Family History Section (V3)](http://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.15.html)
- **Local Reference:** `references/C-CDA_2.1/templates/2.16.840.1.113883.10.20.22.2.15.html`

## Best Practices

### 1. Complete Relationship Information
```python
# Use standard relationship codes
relationship_codes = {
    "FTH": "Father",
    "MTH": "Mother",
    "BRO": "Brother",
    "SIS": "Sister",
    "SON": "Son",
    "DAU": "Daughter",
    "GRFTH": "Grandfather",
    "GRMTH": "Grandmother",
    "PGRFTH": "Paternal Grandfather",
    "PGRMTH": "Paternal Grandmother",
    "MGRFTH": "Maternal Grandfather",
    "MGRMTH": "Maternal Grandmother",
    "UNCLE": "Uncle",
    "AUNT": "Aunt",
    "NEPHEW": "Nephew",
    "NIECE": "Niece",
    "COUSN": "Cousin",
}
```

### 2. Age at Onset
```python
# Document age when condition started
{
    "condition_name": "Breast Cancer",
    "age_at_onset": 45,  # Critical for risk assessment
}
```

### 3. Deceased Family Members
```python
# Complete information for deceased relatives
{
    "subject": {
        "deceased_ind": True,
        "deceased_time": date(2010, 6, 15),
    },
    "observations": [
        {
            "deceased_age": 68,
            "deceased_cause_code": "22298006",
            "deceased_cause_display_name": "Myocardial Infarction",
        }
    ]
}
```

### 4. High-Risk Conditions
```python
# Document conditions with hereditary components
hereditary_conditions = [
    "Breast Cancer",
    "Ovarian Cancer",
    "Colon Cancer",
    "Prostate Cancer",
    "Heart Disease",
    "Diabetes",
    "Hypertension",
    "Stroke",
    "Alzheimer's Disease",
    "Mental Illness",
    "Sickle Cell Disease",
    "Hemophilia",
    "BRCA mutations",
]
```

### 5. Multiple Conditions Per Family Member
```python
# One family member can have multiple conditions
{
    "relationship_display_name": "Father",
    "observations": [
        {"condition_name": "Diabetes", "age_at_onset": 52},
        {"condition_name": "Hypertension", "age_at_onset": 48},
        {"condition_name": "Hyperlipidemia", "age_at_onset": 50},
    ]
}
```

### 6. Gender Information
```python
# Always include gender when known
{
    "subject": {
        "administrative_gender_code": "F",  # Female
    }
}
```

### 7. Birth Time for Age Calculation
```python
# Include birth date to calculate current age
{
    "subject": {
        "birth_time": date(1950, 3, 15),
        "deceased_ind": False,
    }
}
```

### 8. Narrative Generation
The section automatically generates an HTML table with:
- Family member identifier
- Gender
- Relationship to patient
- Conditions (one row per condition)
- Age at onset
- Status (Living or Deceased with date)

### 9. Code Systems
```python
# Prefer SNOMED CT for conditions
{
    "condition_code": "254837009",
    "condition_code_system": "SNOMED",
}

# ICD-10 is acceptable alternative
{
    "condition_code": "C50.9",
    "condition_code_system": "ICD-10",
}
```

### 10. Risk Assessment
```python
# Focus on clinically relevant family history
relevant_history = [
    # First-degree relatives (parents, siblings, children)
    # Conditions with hereditary component
    # Early-onset diseases (before age 50-60)
    # Multiple family members with same condition
    # Rare conditions or genetic syndromes
]
```

## Common Relationship Codes

### Immediate Family
- `FTH` - Father
- `MTH` - Mother
- `BRO` - Brother
- `SIS` - Sister
- `SON` - Son
- `DAU` - Daughter
- `TWIN` - Twin
- `TWINBRO` - Twin Brother
- `TWINSIS` - Twin Sister

### Extended Family
- `GRFTH` - Grandfather
- `GRMTH` - Grandmother
- `PGRFTH` - Paternal Grandfather
- `PGRMTH` - Paternal Grandmother
- `MGRFTH` - Maternal Grandfather
- `MGRMTH` - Maternal Grandmother
- `UNCLE` - Uncle
- `AUNT` - Aunt
- `NEPHEW` - Nephew
- `NIECE` - Niece
- `COUSN` - Cousin

## Common Hereditary Conditions

### Cardiovascular
- Coronary Artery Disease (53741008)
- Myocardial Infarction (22298006)
- Hypertension (38341003)
- Stroke (230690007)
- Hyperlipidemia (55822004)

### Cancer
- Breast Cancer (254837009)
- Ovarian Cancer (363443007)
- Colon Cancer (363406005)
- Prostate Cancer (399068003)
- Lung Cancer (93880001)

### Metabolic/Endocrine
- Type 2 Diabetes Mellitus (44054006)
- Type 1 Diabetes Mellitus (46635009)
- Thyroid Disease (14304000)
- Obesity (414915002)

### Neurological/Psychiatric
- Alzheimer's Disease (26929004)
- Parkinson's Disease (49049000)
- Depression (35489007)
- Bipolar Disorder (13746004)
- Schizophrenia (58214004)

## Common Pitfalls

1. **Missing Age at Onset:** Always document when condition started
2. **Incomplete Deceased Info:** Include cause and age at death
3. **Only Listing Parents:** Include siblings, grandparents when relevant
4. **Missing Gender:** Gender affects risk for certain conditions
5. **Vague Conditions:** Use specific diagnoses, not "cancer" or "heart disease"
6. **No Negative History:** Document significant negative family history
7. **Ignoring Maternal vs Paternal:** Distinguish maternal/paternal lineage
8. **Missing Multiple Occurrences:** Note when multiple relatives have same condition
9. **Static Documentation:** Update as family members develop new conditions
10. **No Risk Stratification:** Focus on conditions relevant to patient's risk profile
