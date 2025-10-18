# Chief Complaint and Reason for Visit Section

**OID:** 2.16.840.1.113883.10.20.22.2.13
**Version:** (No extension)
**Badge:** Administrative Section

## Overview

The Chief Complaint and Reason for Visit Section combines the patient's chief complaint (the patient's own description of their concern) with the reason for the patient's visit (the provider's documentation of why the patient is seeking care).

Local policy determines whether this information is divided into two separate sections (Chief Complaint and Reason for Visit) or recorded in one combined section serving both purposes. This combined approach is common in many healthcare settings.

This section contains only narrative text - no structured entries are required.

## Template Details

- **Template ID:** 2.16.840.1.113883.10.20.22.2.13
- **Extension:** None
- **Conformance:** SHOULD
- **Cardinality:** 0..1 (Optional in documents)
- **LOINC Code:** 46239-0 "Chief Complaint and Reason for Visit"

## Protocol Requirements

### ChiefComplaintProtocol
```python
from typing import Protocol

class ChiefComplaintProtocol(Protocol):
    text: str  # The chief complaint or reason for visit text
```

## Code Example

### Single Chief Complaint
```python
from ccdakit import ChiefComplaintAndReasonForVisitSection, CDAVersion

# Single complaint as simple text
complaints = [
    {"text": "Patient presents with chest pain and shortness of breath for the past 2 hours"}
]

section = ChiefComplaintAndReasonForVisitSection(
    chief_complaints=complaints,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Multiple Complaints
```python
from ccdakit import ChiefComplaintAndReasonForVisitSection, CDAVersion

# Multiple chief complaints/reasons
complaints = [
    {"text": "Persistent cough for 3 weeks"},
    {"text": "Medication refill needed for blood pressure medications"},
    {"text": "Follow-up on recent lab results"}
]

section = ChiefComplaintAndReasonForVisitSection(
    chief_complaints=complaints,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Patient's Own Words
```python
from ccdakit import ChiefComplaintAndReasonForVisitSection, CDAVersion

# Document in patient's own language
complaints = [
    {"text": "Patient states: 'My knee has been killing me for the past week and I can barely walk on it'"}
]

section = ChiefComplaintAndReasonForVisitSection(
    chief_complaints=complaints,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Combined Patient and Provider Perspective
```python
from ccdakit import ChiefComplaintAndReasonForVisitSection, CDAVersion

# Include both patient complaint and provider reason
complaints = [
    {"text": "Chief Complaint: Patient reports 'I have a terrible headache that won't go away'"},
    {"text": "Reason for Visit: Evaluation of persistent headache with associated photophobia and nausea"}
]

section = ChiefComplaintAndReasonForVisitSection(
    chief_complaints=complaints,
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### No Complaint Documented
```python
from ccdakit import ChiefComplaintAndReasonForVisitSection, CDAVersion

# When no complaint is documented
section = ChiefComplaintAndReasonForVisitSection(
    chief_complaints=[],  # Empty list shows default message
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

## Official Reference

[HL7 C-CDA Chief Complaint and Reason for Visit Section Specification](https://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.13.html)

## Best Practices

1. **Use Patient's Words**: When documenting chief complaint, capture the patient's description in their own words when possible, using quotation marks.

2. **Be Specific**: Include relevant details like duration, severity, and associated symptoms.

3. **Separate Components**: When using the combined section, clearly distinguish between the patient's complaint and provider's reason for visit.

4. **Prioritize by Importance**: List multiple complaints in order of clinical priority or severity.

5. **Include Time Context**: Document when symptoms started and any progression or changes.

6. **Avoid Diagnostic Language**: Chief complaint should describe symptoms, not diagnoses (e.g., "chest pain" not "myocardial infarction").

7. **Context Matters**: For follow-up visits, include relevant history (e.g., "Follow-up for diabetes diagnosed 3 months ago").

8. **Maintain Objectivity**: While using patient's words, maintain appropriate clinical objectivity in documentation.

9. **Link to HPI**: The chief complaint should align with and lead into the History of Present Illness.

10. **Consistency**: Use consistent formatting across your organization for similar types of visits.

## Examples by Visit Type

### Acute Care Visit
```python
complaints = [
    {"text": "Patient presents with acute onset severe abdominal pain radiating to the back, nausea, and vomiting beginning 6 hours ago"}
]
```

### Preventive Care Visit
```python
complaints = [
    {"text": "Annual wellness examination and health maintenance"}
]
```

### Follow-up Visit
```python
complaints = [
    {"text": "Follow-up evaluation of hypertension; patient reports improved blood pressure readings at home"}
]
```

### Emergency Department
```python
complaints = [
    {"text": "Chief Complaint: 'I fell and hurt my wrist'"},
    {"text": "Mechanism: Fall from standing height landing on outstretched right hand"}
]
```

## Combining with Separate Sections

Some organizations use this combined section when both patient and provider perspectives are similar, but use separate Chief Complaint and Reason for Visit sections when they differ significantly or when organizational policy requires it.
