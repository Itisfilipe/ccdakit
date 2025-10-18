# Hospital Discharge Instructions Section

**OID:** 2.16.840.1.113883.10.20.22.2.41
**Version:** (No extension)
**Badge:** Administrative Section

## Overview

The Hospital Discharge Instructions Section records instructions provided to the patient at hospital discharge. This narrative-only section contains guidance for patient self-care after leaving the hospital, including medication instructions, dietary restrictions, activity limitations, follow-up appointments, and warning signs to watch for.

This section contains only narrative text - no structured entries are required or typically used. Instructions can be provided as general text or organized by category (e.g., Medications, Diet, Activity, Follow-up Care).

## Template Details

- **Template ID:** 2.16.840.1.113883.10.20.22.2.41
- **Extension:** None
- **Conformance:** SHALL
- **Cardinality:** 0..1 (Optional in documents)
- **LOINC Code:** 8653-8 "Hospital Discharge Instructions"

## Protocol Requirements

### DischargeInstructionProtocol
```python
from typing import Protocol, Optional

class DischargeInstructionProtocol(Protocol):
    instruction_text: str                   # The instruction content
    instruction_category: Optional[str]     # Category (e.g., "Medications", "Diet", "Activity", "Follow-up")
```

## Code Example

### Simple Narrative Text
```python
from ccdakit import HospitalDischargeInstructionsSection, CDAVersion

# Create section with simple narrative
section = HospitalDischargeInstructionsSection(
    narrative_text="Follow discharge care plan. Take all medications as prescribed. "
                   "Follow up with your primary care physician within 7 days. "
                   "Call 911 if you experience chest pain or difficulty breathing.",
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Categorized Instructions
```python
from ccdakit import HospitalDischargeInstructionsSection, CDAVersion

# Define categorized instructions
instructions = [
    {
        "instruction_text": "Take Lisinopril 10mg once daily in the morning",
        "instruction_category": "Medications"
    },
    {
        "instruction_text": "Take Aspirin 81mg once daily with food",
        "instruction_category": "Medications"
    },
    {
        "instruction_text": "Follow a low-sodium diet (less than 2000mg per day)",
        "instruction_category": "Diet"
    },
    {
        "instruction_text": "Avoid heavy lifting for 2 weeks",
        "instruction_category": "Activity"
    },
    {
        "instruction_text": "Walk for 10-15 minutes twice daily",
        "instruction_category": "Activity"
    },
    {
        "instruction_text": "Schedule appointment with Dr. Smith within 7 days",
        "instruction_category": "Follow-up"
    },
    {
        "instruction_text": "Call 911 if you experience chest pain or shortness of breath",
        "instruction_category": "Warning Signs"
    }
]

# Create section with categorized instructions
section = HospitalDischargeInstructionsSection(
    instructions=instructions,
    narrative_text="The following instructions should be followed after discharge:",
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Combined Approach
```python
from ccdakit import HospitalDischargeInstructionsSection, CDAVersion

# Use both narrative preamble and structured instructions
section = HospitalDischargeInstructionsSection(
    narrative_text="You are being discharged after successful treatment. "
                   "Please follow these important instructions:",
    instructions=[
        {"instruction_text": "Take all medications exactly as prescribed", "instruction_category": None},
        {"instruction_text": "Monitor your blood pressure daily", "instruction_category": None},
        {"instruction_text": "Return to emergency department if symptoms worsen", "instruction_category": None}
    ],
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

## Official Reference

[HL7 C-CDA Hospital Discharge Instructions Section Specification](https://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.41.html)

## Best Practices

1. **Be Specific and Clear**: Write instructions in plain language that patients can easily understand. Avoid medical jargon.

2. **Organize by Category**: Group related instructions together (Medications, Diet, Activity, Follow-up, Warning Signs).

3. **Include Key Information**: Always cover medications, activity restrictions, dietary guidance, follow-up appointments, and emergency warning signs.

4. **Make It Actionable**: Use clear action verbs (Take, Avoid, Call, Schedule, Monitor).

5. **Specify Timing**: Include specific timeframes (e.g., "within 7 days", "for 2 weeks").

6. **Highlight Critical Items**: Emphasize important warning signs and when to seek immediate medical attention.

7. **Include Contact Information**: Provide phone numbers for follow-up appointments and questions.

8. **Keep It Concise**: While being thorough, keep instructions concise and easy to follow.

9. **Patient-Centered Language**: Use "you" and "your" to make instructions personal and direct.

10. **Verify Understanding**: Instructions should be written at a 5th-8th grade reading level for best patient comprehension.
