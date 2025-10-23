# Discharge Diagnosis Section

**Template ID:** 2.16.840.1.113883.10.20.22.2.24
**Version:** R2.1 (2015-08-01) / R2.0 (2014-06-09)
**Badge:** Hospital Section

## Overview

The Discharge Diagnosis Section represents problems or diagnoses present at the time of discharge that occurred during the hospitalization. This section documents the final clinical assessment of the patient's condition at discharge and includes diagnoses that require ongoing tracking or management after the patient leaves the hospital.

### Clinical Purpose and Context

Discharge diagnoses documented in this section represent:
- The primary and secondary diagnoses established during hospitalization
- Conditions that occurred or were discovered during the hospital stay
- Problems requiring ongoing management or follow-up after discharge
- Final clinical assessment replacing or confirming admission diagnoses

Problems documented here should also be included in the Problems Section if they require ongoing tracking in the patient's longitudinal health record.

### When to Include

The Discharge Diagnosis Section is a key component of:
- **Discharge Summaries** (primary use case)
- **Transfer Summaries**
- **Hospital Episode Documentation**

This section is essential for continuity of care, helping receiving providers understand what conditions were addressed during hospitalization and what requires ongoing attention.

## Template Details

### Official OID
- **Root:** 2.16.840.1.113883.10.20.22.2.24
- **Extension:** 2015-08-01 (R2.1) or 2014-06-09 (R2.0)

### Conformance Level
- **Conformance:** SHALL (Required in Discharge Summary documents)
- **Section Code:** 11535-2 (LOINC - "Hospital Discharge Diagnosis")
- **Translation Code:** 78375-3 (LOINC - "Discharge Diagnosis")

### Cardinality
- **Section:** 0..1 (Optional but recommended)
- **Entries:** 0..* (Hospital Discharge Diagnosis entries)

### Related Templates
- **Hospital Discharge Diagnosis (V3):** 2.16.840.1.113883.10.20.22.4.33:2015-08-01
- **Problem Observation (V4):** 2.16.840.1.113883.10.20.22.4.4:2015-08-01

## Protocol Requirements

The `DischargeDiagnosisProtocol` defines the data contract for discharge diagnosis entries. Each diagnosis must provide:

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Human-readable diagnosis name |
| `code` | `str` | SNOMED CT or ICD-10 diagnosis code |
| `code_system` | `str` | Code system: 'SNOMED' or 'ICD-10' |
| `status` | `str` | Diagnosis status: 'active', 'inactive', 'resolved' |

### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `diagnosis_date` | `Optional[date]` | Date diagnosis was identified |
| `resolved_date` | `Optional[date]` | Date diagnosis was resolved |
| `discharge_disposition` | `Optional[str]` | Patient's discharge disposition |
| `priority` | `Optional[int]` | Priority ranking (1=primary diagnosis) |

### Data Types and Constraints
- **name:** Clear, clinical description of the discharge diagnosis
- **code:** Must be a valid SNOMED CT or ICD-10 code
- **code_system:** 'SNOMED' (preferred) or 'ICD-10'
- **status:** Most discharge diagnoses are 'active' (ongoing)
- **diagnosis_date:** Date diagnosis was identified during hospitalization
- **priority:** Lower numbers = higher priority (1 is primary diagnosis)

## Code Example

Here's a complete working example using ccdakit to create a Discharge Diagnosis Section:

```python
from datetime import date
from ccdakit.builders.sections.discharge_diagnosis import DischargeDiagnosisSection
from ccdakit.core.base import CDAVersion

# Define discharge diagnoses using a class that implements DischargeDiagnosisProtocol
class DischargeDiagnosis:
    def __init__(self, name, code, code_system, status, diagnosis_date=None,
                 resolved_date=None, priority=None):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._status = status
        self._diagnosis_date = diagnosis_date
        self._resolved_date = resolved_date
        self._discharge_disposition = None
        self._priority = priority

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def status(self):
        return self._status

    @property
    def diagnosis_date(self):
        return self._diagnosis_date

    @property
    def resolved_date(self):
        return self._resolved_date

    @property
    def discharge_disposition(self):
        return self._discharge_disposition

    @property
    def priority(self):
        return self._priority

# Create discharge diagnosis instances
diagnoses = [
    DischargeDiagnosis(
        name="ST Elevation Myocardial Infarction",
        code="401314000",
        code_system="SNOMED",
        status="active",
        diagnosis_date=date(2024, 10, 15),
        priority=1  # Primary diagnosis
    ),
    DischargeDiagnosis(
        name="Acute systolic heart failure",
        code="441481004",
        code_system="SNOMED",
        status="active",
        diagnosis_date=date(2024, 10, 16),
        priority=2  # Secondary diagnosis
    ),
    DischargeDiagnosis(
        name="Community acquired pneumonia",
        code="385093006",
        code_system="SNOMED",
        status="resolved",
        diagnosis_date=date(2024, 10, 15),
        resolved_date=date(2024, 10, 20),
        priority=3
    )
]

# Build the Discharge Diagnosis Section
section_builder = DischargeDiagnosisSection(
    diagnoses=diagnoses,
    title="Discharge Diagnosis",
    version=CDAVersion.R2_1
)

# Generate XML element
section_element = section_builder.build()

# Convert to XML string (for demonstration)
from lxml import etree
xml_string = etree.tostring(section_element, pretty_print=True, encoding='unicode')
print(xml_string)
```

## Official Reference

For complete specification details, refer to the official HL7 C-CDA R2.1 documentation:
- [HL7 C-CDA R2.1 Implementation Guide](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=492)
- Section: Discharge Diagnosis Section (V3)
- Conformance IDs: CONF:1198-7979 through CONF:1198-32836

## Best Practices

### Common Patterns

1. **Use Standard Vocabularies**
   - Prefer SNOMED CT for clinical interoperability
   - ICD-10-CM codes are commonly used for billing purposes
   - Consider including both if your system supports it

2. **Prioritize Diagnoses**
   - Use the priority field to rank diagnoses by clinical significance
   - Priority 1 = Primary discharge diagnosis (most significant)
   - Secondary diagnoses help tell the complete clinical story

3. **Track Diagnosis Status**
   - Most discharge diagnoses are 'active' (ongoing management needed)
   - Mark diagnoses as 'resolved' if they were treated and resolved during hospitalization
   - Include resolved_date for resolved diagnoses

4. **Coordinate with Problems Section**
   - Active discharge diagnoses should also appear in the Problems Section
   - This ensures continuity in the patient's longitudinal health record
   - Problems Section tracks ongoing conditions; this section documents the episode

### Validation Tips

1. **Section Code Validation**
   - Ensure section code is 11535-2 (LOINC "Hospital Discharge Diagnosis")
   - Must include translation code 78375-3 (LOINC "Discharge Diagnosis")
   - Both codes are automatically set by the builder

2. **Template ID Validation**
   - Verify template ID includes appropriate extension for version
   - R2.1: extension="2015-08-01"
   - R2.0: extension="2014-06-09"

3. **Entry Structure Validation**
   - Entry contains Hospital Discharge Diagnosis Act (classCode="ACT")
   - Act contains one or more Problem Observations via entryRelationship
   - Each Problem Observation represents a specific diagnosis

4. **Status Consistency**
   - If status is 'resolved', resolved_date should be present
   - If status is 'active', resolved_date should be absent
   - Status drives the Act statusCode in the XML

### Common Pitfalls

1. **Confusing with Admission Diagnosis**
   - Admission diagnoses represent initial assessment at admission
   - Discharge diagnoses represent final assessment at discharge
   - Both sections may be present in the same document

2. **Missing Status Information**
   - Always provide status field ('active', 'inactive', or 'resolved')
   - Status is required and affects document interpretation
   - Default to 'active' if diagnosis requires ongoing management

3. **Inconsistent Date Handling**
   - Diagnosis date should be during the hospitalization period
   - Don't use future dates for diagnosis_date
   - Resolved date must be after or equal to diagnosis date

4. **Empty Diagnosis List**
   - While technically optional, discharge diagnoses are expected
   - If truly no diagnoses, include narrative explaining why
   - Consider whether the document type requires diagnoses

5. **Priority Numbering Issues**
   - Lower numbers = higher priority (1 is most important)
   - Don't skip numbers or use zero
   - Priority is optional but recommended for clarity

6. **Not Synchronizing with Problems**
   - Active discharge diagnoses should appear in Problems Section
   - This ensures they're tracked longitudinally
   - Resolved diagnoses may not need to be in Problems Section

## Related Sections

- **Admission Diagnosis Section:** Documents diagnoses at admission
- **Problems Section:** Tracks ongoing problems longitudinally
- **Hospital Course Section:** Narrative describing the hospitalization
- **Procedures Section:** Documents procedures performed during stay

## Code Systems and Terminologies

### Diagnosis Codes
- **SNOMED CT (Preferred):** OID 2.16.840.1.113883.6.96
  - Provides detailed clinical semantics
  - Better for clinical decision support and interoperability

- **ICD-10-CM:** OID 2.16.840.1.113883.6.90
  - Required for billing and administrative purposes
  - May be used alone or in addition to SNOMED CT

### Section Codes
- **Primary:** 11535-2 - "Hospital Discharge Diagnosis" (LOINC)
- **Translation:** 78375-3 - "Discharge Diagnosis" (LOINC)

### Status Value Set
- **Problem Status:** 2.16.840.1.113883.3.88.12.80.68
  - active: Condition is ongoing
  - inactive: Condition is not currently active
  - resolved: Condition has been resolved

## Implementation Notes

### Narrative Generation
The builder automatically generates an HTML table with:
- Diagnosis name (with content ID for referencing)
- Code and code system
- Status
- Diagnosis date

### Hospital Discharge Diagnosis Act
The section uses a special Act wrapper:
- Acts as a container for related Problem Observations
- Allows grouping multiple diagnoses from the same encounter
- Typically one Act contains all discharge diagnoses

### Diagnosis Priority
While not explicitly encoded in standard C-CDA templates, priority can be:
- Documented in the narrative
- Implied by order in the entry list
- Captured in local extensions if needed

### Integration with Problems Section
Best practice workflow:
1. Document discharge diagnoses in this section
2. Add active discharge diagnoses to Problems Section
3. Ensure consistent coding between sections
4. Use persistent IDs to link related observations

### Discharge Disposition
The discharge_disposition property can capture:
- "Home" - Patient discharged to home
- "Skilled Nursing Facility" - Transferred to SNF
- "Acute Care Hospital" - Transferred to another hospital
- "Hospice" - Discharged to hospice care
- This is optional but provides valuable context

### Clinical Decision Support
Discharge diagnoses are critical for:
- Quality measurement and reporting
- Risk stratification
- Care coordination
- Follow-up care planning
- Billing and reimbursement
