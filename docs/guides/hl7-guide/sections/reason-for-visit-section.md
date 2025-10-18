# Reason for Visit Section

**OID:** 2.16.840.1.113883.10.20.22.2.12
**Version:** (No extension)
**Badge:** Administrative Section

## Overview

The Reason for Visit Section records the patient's reason for the healthcare visit as documented by the provider. This is the provider's perspective of why the patient is seeking care, which may differ from the patient's own description (Chief Complaint).

Local policy determines whether Reason for Visit and Chief Complaint are documented in separate sections or combined into a single Chief Complaint and Reason for Visit section.

This is a simple narrative-only section without structured entries.

## Template Details

- **Template ID:** 2.16.840.1.113883.10.20.22.2.12
- **Extension:** None
- **Conformance:** SHOULD
- **Cardinality:** 0..1 (Optional in documents)
- **LOINC Code:** 29299-5 "Reason for Visit"

## Protocol Requirements

This section does not use a protocol as it only contains narrative text. Simply provide the reason text as a string parameter.

## Code Example

### Simple Reason for Visit
```python
from ccdakit import ReasonForVisitSection, CDAVersion

# Create section with reason text
section = ReasonForVisitSection(
    reason_text="Annual physical examination",
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Specific Medical Reason
```python
from ccdakit import ReasonForVisitSection, CDAVersion

section = ReasonForVisitSection(
    reason_text="Follow-up for hypertension management and medication review",
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Acute Visit Reason
```python
from ccdakit import ReasonForVisitSection, CDAVersion

section = ReasonForVisitSection(
    reason_text="Evaluation of chest pain and shortness of breath",
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

### Custom Title
```python
from ccdakit import ReasonForVisitSection, CDAVersion

section = ReasonForVisitSection(
    reason_text="Pre-operative evaluation for scheduled knee replacement surgery",
    title="Visit Reason",
    version=CDAVersion.R2_1
)

xml_element = section.build()
```

## Official Reference

[HL7 C-CDA Reason for Visit Section Specification](https://www.hl7.org/ccdasearch/templates/2.16.840.1.113883.10.20.22.2.12.html)

## Best Practices

1. **Provider's Perspective**: Document the clinical reason from the provider's viewpoint, not necessarily the patient's exact words.

2. **Be Concise**: Keep the reason brief but specific enough to understand the purpose of the visit.

3. **Use Clinical Language**: Use appropriate medical terminology while maintaining clarity.

4. **Differentiate from Chief Complaint**: If using separate sections, ensure this reflects the provider's documentation, while Chief Complaint reflects the patient's own words.

5. **Include Context**: For follow-up visits, reference what is being followed up (e.g., "Follow-up for diabetes management").

6. **Specify Type of Visit**: Indicate if it's a routine visit, follow-up, acute visit, or pre-operative evaluation.

7. **Multiple Reasons**: When there are multiple reasons, list all relevant concerns (e.g., "Hypertension follow-up and foot pain evaluation").

8. **Link to Assessment**: The reason for visit should align with the assessment and plan documented later in the note.

9. **Distinguish from Diagnosis**: This is the reason for seeking care, not the diagnosis or conclusion.

10. **Consistency Across Systems**: Maintain consistent formatting and terminology across your organization for similar visit types.

## Difference from Chief Complaint

- **Reason for Visit**: Provider's documentation of the clinical reason for the encounter
  - Example: "Follow-up for type 2 diabetes mellitus with recent hyperglycemia"

- **Chief Complaint**: Patient's own description in their words
  - Example: "My sugar has been high lately and I need my medications checked"

Many organizations combine these into the Chief Complaint and Reason for Visit section rather than maintaining separate sections.
