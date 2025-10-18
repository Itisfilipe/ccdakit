# Assessment and Plan Section

**Template ID:** `2.16.840.1.113883.10.20.22.2.9`
**Version:** 2014-06-09 (R2.1 | R2.0)
**Badge:** Extended Section

## Overview

The **Assessment and Plan Section (V2)** represents the clinician's conclusions and working assumptions that will guide treatment of the patient. The assessment is the synthesis of subjective and objective evidence, representing the provider's analysis of the patient's condition. The plan describes the intended course of action to address identified problems.

This combined section integrates:
- **Assessment:** Clinical impressions, differential diagnoses, diagnostic conclusions
- **Plan:** Treatment recommendations, planned procedures, medications, referrals, patient education

This section can be used as a combined Assessment and Plan, or the components can be separated into distinct Assessment Section and Plan of Treatment Section according to local policy requirements.

## Template Details

### Identifiers
- **Root:** `2.16.840.1.113883.10.20.22.2.9`
- **Extension:** `2014-06-09`
- **LOINC Code:** `51847-2` (Assessment and Plan)

### Conformance Requirements
- **SHALL** contain exactly one [1..1] `templateId` (CONF:1098-7705)
- **SHALL** contain exactly one [1..1] `code` with code="51847-2" from LOINC (CONF:1098-15353)
- **SHALL** contain exactly one [1..1] `text` (narrative block) (CONF:1098-7707)
- **MAY** contain zero or more [0..*] `entry` elements (CONF:1098-7708)
- Each `entry` **MAY** contain exactly one [1..1] Planned Act (V2) (CONF:1098-15448)

### Cardinality
- **Section:** Optional
- **Entries:** Optional (0..*)
- **Title:** Implied (typically "Assessment and Plan")

## Protocol Requirements

The section uses the `AssessmentAndPlanItemProtocol` from `ccdakit.protocols.assessment_and_plan`:

### AssessmentAndPlanItemProtocol

```python
@property
def text(self) -> str:
    """Assessment or plan narrative text"""

@property
def item_type(self) -> str:
    """Type: 'assessment' or 'plan'"""

@property
def planned_act(self) -> Optional[PlannedActProtocol]:
    """Associated planned act for plan items"""
```

### PlannedActProtocol (for structured plan entries)

```python
@property
def id_root(self) -> str:
    """OID for the ID root (assigning authority)"""

@property
def id_extension(self) -> str:
    """Unique identifier within the root's namespace"""

@property
def code(self) -> str:
    """LOINC or SNOMED CT code for the planned activity"""

@property
def code_system(self) -> str:
    """Code system: 'LOINC' or 'SNOMED'"""

@property
def display_name(self) -> str:
    """Human-readable description of the planned activity"""

@property
def mood_code(self) -> str:
    """Mood code: 'INT' (intent), 'RQO' (request), 'PRMS' (promise), 'PRP' (proposal)"""

@property
def effective_time(self) -> Optional[datetime]:
    """When the activity is intended to take place"""

@property
def instructions(self) -> Optional[str]:
    """Patient or provider instructions"""
```

## Code Example

### Basic Usage (Narrative Only)

```python
from ccdakit import AssessmentAndPlanSection, CDAVersion

# Define assessment and plan items
items = [
    {
        "text": "Type 2 diabetes mellitus with poor glycemic control (HbA1c 9.2%)",
        "item_type": "assessment",
        "planned_act": None,
    },
    {
        "text": "Hypertension, well-controlled on current regimen",
        "item_type": "assessment",
        "planned_act": None,
    },
    {
        "text": "Increase metformin to 1000mg twice daily",
        "item_type": "plan",
        "planned_act": None,
    },
    {
        "text": "Refer to diabetes educator for dietary counseling",
        "item_type": "plan",
        "planned_act": None,
    },
    {
        "text": "Recheck HbA1c in 3 months",
        "item_type": "plan",
        "planned_act": None,
    }
]

# Create section
section = AssessmentAndPlanSection(
    items=items,
    version=CDAVersion.R2_1
)

# Generate XML
xml_element = section.to_element()
```

### Empty Section (Generic Narrative)

```python
# Create section with no items
section = AssessmentAndPlanSection(
    items=[],
    version=CDAVersion.R2_1
)

# Generates section with narrative: "Assessment and plan documented in clinical notes."
```

### With Structured Planned Acts

```python
from datetime import datetime

# Define items with structured plan entries
items = [
    {
        "text": "Acute bronchitis",
        "item_type": "assessment",
        "planned_act": None,
    },
    {
        "text": "Start azithromycin 500mg daily for 5 days",
        "item_type": "plan",
        "planned_act": {
            "id_root": "2.16.840.1.113883.19.5",
            "id_extension": "12345",
            "code": "386617003",
            "code_system": "SNOMED",
            "display_name": "Antibiotic therapy",
            "mood_code": "INT",
            "effective_time": datetime(2024, 3, 20, 0, 0),
            "instructions": "Take with food",
        }
    },
    {
        "text": "Increase fluid intake",
        "item_type": "plan",
        "planned_act": {
            "id_root": "2.16.840.1.113883.19.5",
            "id_extension": "12346",
            "code": "160237006",
            "code_system": "SNOMED",
            "display_name": "Fluid intake therapy",
            "mood_code": "INT",
            "effective_time": None,
            "instructions": "Drink at least 8 glasses of water daily",
        }
    }
]

section = AssessmentAndPlanSection(items=items)
```

### Separate Assessment and Plan Sections

```python
# Assessments only
assessments = [
    {"text": "Acute exacerbation of COPD", "item_type": "assessment"},
    {"text": "Hypoxemia", "item_type": "assessment"},
    {"text": "Community-acquired pneumonia", "item_type": "assessment"},
]

# Plans only
plans = [
    {"text": "Admit to hospital for IV antibiotics", "item_type": "plan"},
    {"text": "Supplemental oxygen to maintain SpO2 >90%", "item_type": "plan"},
    {"text": "Nebulizer treatments q4h", "item_type": "plan"},
    {"text": "Chest X-ray to assess for infiltrates", "item_type": "plan"},
]

# Combine
all_items = assessments + plans

section = AssessmentAndPlanSection(items=all_items)
```

### Custom Title

```python
section = AssessmentAndPlanSection(
    items=items,
    title="Clinical Impression and Treatment Plan",
    version=CDAVersion.R2_1
)
```

### With Custom Protocol Implementation

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class PlannedActivity:
    """Custom planned act implementation."""
    id_root: str
    id_extension: str
    code: str
    code_system: str
    display_name: str
    mood_code: str
    effective_time: Optional[datetime] = None
    instructions: Optional[str] = None

@dataclass
class AssessmentPlanItem:
    """Custom assessment/plan item implementation."""
    text: str
    item_type: str
    planned_act: Optional[PlannedActivity] = None

# Create items
items = [
    AssessmentPlanItem(
        text="Suspected urinary tract infection",
        item_type="assessment",
    ),
    AssessmentPlanItem(
        text="Obtain urine culture and sensitivity",
        item_type="plan",
        planned_act=PlannedActivity(
            id_root="2.16.840.1.113883.19.5",
            id_extension="lab-001",
            code="117010001",
            code_system="SNOMED",
            display_name="Urine culture",
            mood_code="RQO",  # Request
            effective_time=datetime(2024, 3, 21, 8, 0),
        )
    ),
]

section = AssessmentAndPlanSection(items=items)
```

### Problem-Oriented Assessment and Plan

```python
# SOAP format: Assessment and Plan for each problem
items = [
    # Problem 1: Diabetes
    {"text": "Diabetes Type 2 - poorly controlled", "item_type": "assessment"},
    {"text": "Continue metformin 1000mg BID", "item_type": "plan"},
    {"text": "Add glipizide 5mg daily", "item_type": "plan"},
    {"text": "Diabetes education referral", "item_type": "plan"},

    # Problem 2: Hypertension
    {"text": "Hypertension - at goal with current therapy", "item_type": "assessment"},
    {"text": "Continue lisinopril 20mg daily", "item_type": "plan"},

    # Problem 3: Hyperlipidemia
    {"text": "Hyperlipidemia - LDL above goal", "item_type": "assessment"},
    {"text": "Increase atorvastatin from 20mg to 40mg daily", "item_type": "plan"},
    {"text": "Recheck lipid panel in 6 weeks", "item_type": "plan"},
]

section = AssessmentAndPlanSection(items=items)
```

## Official Reference

For complete specification details, refer to:
- **C-CDA Online:** [Assessment and Plan Section (V2)](http://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.9.html)
- **Local Reference:** `references/C-CDA_2.1/templates/2.16.840.1.113883.10.20.22.2.9.html`

## Best Practices

### 1. Separate Assessment from Plan
```python
# Clear distinction between what was found and what will be done
assessments = [
    "Acute sinusitis based on symptoms and physical exam",
    "No evidence of bacterial infection"
]

plans = [
    "Symptomatic treatment with decongestants",
    "Return if symptoms worsen or persist >10 days"
]
```

### 2. Problem-Oriented Format
```python
# Organize by problem for complex patients
# Problem 1
assessment_1 = "Type 2 diabetes - HbA1c 8.5%, above goal"
plan_1a = "Increase metformin dose"
plan_1b = "Diabetes self-management education"

# Problem 2
assessment_2 = "Hypertension - BP 145/92, above goal"
plan_2a = "Add amlodipine 5mg daily"
plan_2b = "Home BP monitoring"
```

### 3. Include Differential Diagnosis
```python
{
    "text": "Chest pain - likely musculoskeletal vs cardiac vs GI etiology. "
           "EKG unremarkable, troponin pending. Will observe in ED.",
    "item_type": "assessment"
}
```

### 4. Specific, Actionable Plans
```python
# Good: Specific and actionable
{"text": "Start lisinopril 10mg PO daily for hypertension", "item_type": "plan"}
{"text": "Schedule colonoscopy within 2 weeks", "item_type": "plan"}
{"text": "Patient education on diabetic foot care provided", "item_type": "plan"}

# Less effective: Vague
{"text": "Manage hypertension", "item_type": "plan"}
{"text": "Follow up", "item_type": "plan"}
```

### 5. Mood Codes for Planned Acts
```python
# INT (intent): General intention to perform
{"mood_code": "INT"}

# RQO (request/order): Formal order or request
{"mood_code": "RQO"}

# PRMS (promise): Commitment to perform
{"mood_code": "PRMS"}

# PRP (proposal): Suggestion or recommendation
{"mood_code": "PRP"}
```

### 6. Timing in Plans
```python
# Include when activities should occur
{
    "text": "Recheck CBC in 1 week",
    "item_type": "plan",
    "planned_act": {
        ...
        "effective_time": datetime(2024, 3, 27, 0, 0),
    }
}
```

### 7. Patient Instructions
```python
# Include patient-specific instructions
{
    "planned_act": {
        ...
        "display_name": "Wound care",
        "instructions": "Clean wound with soap and water daily. "
                       "Apply antibiotic ointment and change dressing. "
                       "Return if increased redness, swelling, or drainage."
    }
}
```

### 8. Narrative Generation
The section automatically generates narrative with:
- **Assessment** heading with bulleted list of assessment items
- **Plan** heading with bulleted list of plan items
- Each item with unique ID reference for linking

### 9. Clinical Decision-Making
```python
# Document rationale for decisions
{
    "text": "Acute appendicitis - Given clinical presentation and imaging findings, "
           "surgery is indicated. Discussed risks/benefits with patient.",
    "item_type": "assessment"
},
{
    "text": "Schedule emergent appendectomy",
    "item_type": "plan"
}
```

### 10. Follow-up Plans
```python
# Always include follow-up
plans = [
    {"text": "Follow up in clinic in 2 weeks"},
    {"text": "Call with lab results within 48 hours"},
    {"text": "Return precautions discussed: fever >101F, worsening pain, vomiting"},
]
```

## Common Plan Activities

### Medications
```python
{"text": "Start metformin 500mg PO BID with meals"}
{"text": "Discontinue hydrochlorothiazide"}
{"text": "Increase lisinopril from 10mg to 20mg daily"}
```

### Diagnostic Tests
```python
{"text": "Order CBC, CMP, HbA1c"}
{"text": "Schedule CT abdomen/pelvis with contrast"}
{"text": "Obtain urine culture before starting antibiotics"}
```

### Procedures
```python
{"text": "Schedule colonoscopy for colon cancer screening"}
{"text": "Incision and drainage of abscess in ED"}
{"text": "Referral to cardiology for stress test"}
```

### Referrals
```python
{"text": "Refer to physical therapy for knee rehabilitation"}
{"text": "Endocrinology consult for difficult-to-control diabetes"}
{"text": "Social work referral for home safety assessment"}
```

### Patient Education
```python
{"text": "Diabetes education on carbohydrate counting provided"}
{"text": "Smoking cessation counseling completed"}
{"text": "Fall prevention strategies discussed"}
```

## Common Pitfalls

1. **Mixing Assessment and Plan:** Keep findings (assessment) separate from actions (plan)
2. **Vague Assessments:** Be specific about diagnoses and clinical reasoning
3. **Non-Actionable Plans:** Plans should be concrete and implementable
4. **Missing Follow-up:** Always include when patient should return
5. **Incomplete Plans:** Address all identified problems
6. **No Timeline:** Specify when planned activities should occur
7. **Missing Instructions:** Include patient-specific guidance
8. **Inconsistent with Problems:** Ensure plan addresses documented problems
9. **Too Much Detail:** Keep narrative focused; detailed orders go in specific sections
10. **No Clinical Reasoning:** Document why specific plans were chosen

## Alternative Sections

Depending on local policy, you may use:
- **Assessment Section** (Template 2.16.840.1.113883.10.20.22.2.8): Assessment only
- **Plan of Treatment Section** (Template 2.16.840.1.113883.10.20.22.2.10): Plan only
- **Assessment and Plan Section** (this template): Combined approach
