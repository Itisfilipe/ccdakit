# Physical Exam Section

**OID:** 2.16.840.1.113883.10.20.2.10
**Version:** 2015-08-01
**Badge:** Specialized Section

## Overview

The Physical Exam Section includes direct observations made by a clinician during physical examination of the patient. The examination may include the use of simple instruments (stethoscope, blood pressure cuff, thermometer) and may also describe simple maneuvers performed directly on the patient's body (palpation, percussion, auscultation).

This section can contain narrative text describing exam findings and/or structured entries for specific observations, particularly wound observations in longitudinal care scenarios.

## Template Details

- **Template ID:** 2.16.840.1.113883.10.20.2.10
- **Extension:** 2015-08-01
- **Conformance:** SHOULD
- **Cardinality:** 0..1 (Optional in documents)
- **LOINC Code:** 29545-1 "Physical Findings"

## Protocol Requirements

### WoundObservationProtocol
```python
from typing import Protocol, Optional
from datetime import datetime

class WoundObservationProtocol(Protocol):
    wound_type: str                 # Type of wound (e.g., "Pressure Ulcer", "Surgical Wound")
    date: datetime                  # Date and time of observation
    location: Optional[str]         # Body location (e.g., "Left heel", "Abdomen")
    laterality: Optional[str]       # Laterality: "Left", "Right", "Bilateral"
```

## Code Example

### With Narrative Text Only
```python
from ccdakit import PhysicalExamSection, CDAVersion

# Create section with narrative text
section = PhysicalExamSection(
    text="GENERAL: Well-developed, well-nourished adult in no acute distress. "
         "VITAL SIGNS: BP 120/80, HR 72, RR 16, Temp 98.6°F. "
         "HEENT: Normocephalic, atraumatic. Pupils equal, round, reactive to light. "
         "NECK: Supple, no lymphadenopathy. "
         "CARDIOVASCULAR: Regular rate and rhythm, no murmurs. "
         "RESPIRATORY: Clear to auscultation bilaterally. "
         "ABDOMEN: Soft, non-tender, non-distended, normal bowel sounds. "
         "EXTREMITIES: No edema, pulses 2+ bilaterally. "
         "SKIN: Warm and dry, no rashes.",
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### With Wound Observations
```python
from ccdakit import PhysicalExamSection, CDAVersion
from datetime import datetime

# Define wound observations
wound_observations = [
    {
        "wound_type": "Pressure Ulcer Stage II",
        "date": datetime(2025, 1, 15, 10, 30),
        "location": "Left heel",
        "laterality": "Left"
    },
    {
        "wound_type": "Surgical Incision",
        "date": datetime(2025, 1, 15, 10, 35),
        "location": "Right lower quadrant abdomen",
        "laterality": "Right"
    }
]

# Create section with wound observations
section = PhysicalExamSection(
    wound_observations=wound_observations,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Combined Narrative and Structured Data
```python
from ccdakit import PhysicalExamSection, CDAVersion
from datetime import datetime

# Create comprehensive physical exam section
section = PhysicalExamSection(
    text="Physical examination reveals a healing surgical wound with no signs of infection. "
         "General appearance: Alert and oriented. "
         "Cardiovascular: Regular rate and rhythm. "
         "Respiratory: Clear lung sounds. "
         "Skin assessment documented below.",
    wound_observations=[
        {
            "wound_type": "Post-operative Surgical Wound",
            "date": datetime(2025, 1, 20, 14, 0),
            "location": "Midline sternum",
            "laterality": None
        }
    ],
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

## Official Reference

[HL7 C-CDA Physical Exam Section Specification](https://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.2.10.html)

## Best Practices

1. **Systematic Organization**: Document findings in a systematic head-to-toe or system-based order (General, HEENT, Neck, Cardiovascular, Respiratory, etc.).

2. **Be Objective**: Record what you observe, not interpretations. Use descriptive terms rather than diagnostic conclusions.

3. **Include Normal Findings**: Document both positive and pertinent negative findings to show completeness of examination.

4. **Use Standard Terminology**: Use standardized medical terminology and abbreviations to ensure clarity.

5. **Document Vital Signs**: Always include vital signs as they are fundamental objective data.

6. **Specify Location**: For abnormal findings (wounds, masses, rashes), always specify the exact body location and laterality.

7. **Measure When Possible**: Include measurements for wounds, masses, or other abnormalities (size in cm, depth, etc.).

8. **Timestamp Observations**: Include date and time of examination, especially for wound assessments that need tracking over time.

9. **Compare to Prior Exams**: When relevant, note changes from previous examinations.

10. **Focus on Relevance**: While being thorough, focus on findings relevant to the patient's current condition and chief complaint.

11. **Wound Documentation**: For wounds, document type, location, size, appearance, drainage, and signs of infection or healing.

12. **Use Body Diagrams**: When supported, reference body diagrams or images for complex or multiple findings.
