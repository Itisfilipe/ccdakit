# Preoperative Diagnosis Section

**Template ID:** 2.16.840.1.113883.10.20.22.2.34
**Version:** R2.1 (2015-08-01)
**Badge:** Surgical Section

## Overview

The Preoperative Diagnosis Section records the surgical diagnosis or diagnoses assigned to the patient before the surgical procedure. This represents the surgeon's clinical assessment that justifies performing the operation. The preoperative diagnosis is, in the surgeon's opinion, the diagnosis that will be confirmed during surgery.

### Clinical Purpose and Context

Preoperative diagnoses documented in this section represent:
- The clinical indication for performing surgery
- The surgeon's pre-surgical assessment
- The working diagnosis that justifies the procedure
- The expected findings based on pre-operative evaluation

The preoperative diagnosis may be confirmed, refined, or changed based on intraoperative findings, which are then documented in the Postoperative Diagnosis Section.

### When to Include

The Preoperative Diagnosis Section is a standard component of:
- **Operative Notes** (primary use case)
- **Surgical Procedure Notes**
- **Pre-operative Assessment Documents**

This section is essential for surgical documentation, providing the clinical rationale for the procedure and supporting medical necessity.

## Template Details

### Official OID
- **Root:** 2.16.840.1.113883.10.20.22.2.34
- **Extension:** 2015-08-01 (R2.1)

### Conformance Level
- **Conformance:** SHALL (Required in Operative Notes)
- **Section Code:** 10219-4 (LOINC - "Preoperative Diagnosis")

### Cardinality
- **Section:** 0..1 (Optional but highly recommended)
- **Entries:** 0..* (Preoperative Diagnosis Act entries)

### Related Templates
- **Preoperative Diagnosis (V3):** 2.16.840.1.113883.10.20.22.4.65:2015-08-01
- **Problem Observation (V3):** 2.16.840.1.113883.10.20.22.4.4:2015-08-01

## Protocol Requirements

The `PreoperativeDiagnosisProtocol` defines the data contract for preoperative diagnosis entries. Each diagnosis must provide:

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Human-readable diagnosis name |
| `code` | `str` | SNOMED CT or ICD-10 diagnosis code |
| `code_system` | `str` | Code system: 'SNOMED' or 'ICD-10' |
| `status` | `str` | Diagnosis status (typically 'active') |

### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `diagnosis_date` | `Optional[date]` | Date diagnosis was made |
| `persistent_id` | `Optional[PersistentIDProtocol]` | Persistent ID across document versions |

### Data Types and Constraints
- **name:** Clear surgical diagnosis description
- **code:** Valid SNOMED CT or ICD-10 code
- **code_system:** 'SNOMED' (preferred) or 'ICD-10'
- **status:** Typically 'active' for preoperative diagnoses
- **diagnosis_date:** Date the surgical diagnosis was determined

## Code Example

Here's a complete working example using ccdakit to create a Preoperative Diagnosis Section:

```python
from datetime import date
from ccdakit.builders.sections.preoperative_diagnosis import PreoperativeDiagnosisSection
from ccdakit.core.base import CDAVersion

# Define preoperative diagnoses using a class that implements PreoperativeDiagnosisProtocol
class PreoperativeDiagnosis:
    def __init__(self, name, code, code_system, status="active", diagnosis_date=None):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._status = status
        self._diagnosis_date = diagnosis_date
        self._persistent_id = None

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
    def persistent_id(self):
        return self._persistent_id

# Example 1: Single preoperative diagnosis
diagnoses = [
    PreoperativeDiagnosis(
        name="Acute appendicitis",
        code="74400008",
        code_system="SNOMED",
        status="active",
        diagnosis_date=date(2024, 10, 15)
    )
]

section_builder = PreoperativeDiagnosisSection(
    diagnoses=diagnoses,
    title="Preoperative Diagnosis",
    version=CDAVersion.R2_1
)

# Example 2: Multiple preoperative diagnoses
diagnoses = [
    PreoperativeDiagnosis(
        name="Symptomatic cholelithiasis",
        code="235919008",
        code_system="SNOMED",
        status="active",
        diagnosis_date=date(2024, 10, 10)
    ),
    PreoperativeDiagnosis(
        name="Acute cholecystitis",
        code="65275009",
        code_system="SNOMED",
        status="active",
        diagnosis_date=date(2024, 10, 14)
    )
]

section_builder = PreoperativeDiagnosisSection(
    diagnoses=diagnoses,
    title="Preoperative Diagnosis",
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
- Section: Preoperative Diagnosis Section (V3)
- Entry: Preoperative Diagnosis (V3)
- Conformance IDs: CONF:1198-8097 through CONF:1198-15504

## Best Practices

### Common Patterns

1. **Use Specific Surgical Terminology**
   - Use precise surgical diagnostic terms
   - Include anatomical location when relevant
   - Specify acute vs chronic when applicable
   - Note severity or stage if known

2. **Document Multiple Diagnoses**
   - List all diagnoses that justify the procedure
   - Order by clinical significance (primary first)
   - Include comorbidities that affect surgical planning

3. **Status is Typically Active**
   - Preoperative diagnoses are usually 'active'
   - They represent current conditions requiring surgery
   - Use consistent status for all preoperative diagnoses

4. **Include Diagnosis Date**
   - Date when surgical diagnosis was made
   - Often during pre-operative evaluation
   - May differ from symptom onset date

### Validation Tips

1. **Section Code Validation**
   - Ensure section code is 10219-4 (LOINC "Preoperative Diagnosis")
   - This is automatically set by the builder

2. **Template ID Validation**
   - Verify template ID includes extension="2015-08-01" for R2.1
   - Multiple template IDs may be present for backward compatibility

3. **Entry Structure Validation**
   - Each entry contains a Preoperative Diagnosis Act
   - Act contains Problem Observations via entryRelationship
   - Problem Observations use standard Problem Observation (V3) template

4. **Code System Validation**
   - 'SNOMED' maps to OID 2.16.840.1.113883.6.96
   - 'ICD-10' maps to OID 2.16.840.1.113883.6.90
   - Builder handles OID conversion automatically

### Common Pitfalls

1. **Confusing with Admission Diagnosis**
   - Admission diagnosis: Why patient was hospitalized
   - Preoperative diagnosis: Why surgery is being performed
   - Different clinical contexts and timing

2. **Not Comparing with Postoperative**
   - Preoperative diagnosis may differ from postoperative findings
   - Both sections should be present in operative notes
   - Document relationship between pre and post-op diagnoses

3. **Too Vague or General**
   - Avoid non-specific diagnoses like "abdominal pain"
   - Use specific surgical diagnoses
   - Include relevant details (location, severity, type)

4. **Missing Diagnosis Date**
   - While optional, diagnosis date provides important context
   - Helps establish timeline of surgical decision-making
   - Include when available

5. **Inconsistent with Procedure**
   - Diagnosis should justify the planned procedure
   - Ensure alignment with procedure documentation
   - Document clear indication for surgery

6. **Status Confusion**
   - Don't use 'resolved' status for preoperative diagnoses
   - Use 'active' for current surgical indications
   - Status reflects pre-surgical state

## Related Sections

- **Postoperative Diagnosis Section:** Final diagnosis after surgery
- **Procedures Section:** The surgical procedure performed
- **Indications Section:** Detailed indications for surgery
- **Assessment and Plan Section:** Clinical reasoning for surgery
- **History of Present Illness:** Timeline leading to surgery

## Code Systems and Terminologies

### Diagnosis Codes
- **SNOMED CT (Preferred):** OID 2.16.840.1.113883.6.96
  - Provides detailed surgical terminology
  - Better for clinical decision support

- **ICD-10-CM:** OID 2.16.840.1.113883.6.90
  - Used for billing and administrative purposes
  - Common in surgical coding

### Common Surgical Diagnosis Codes (SNOMED CT)
- **74400008** - Appendicitis
- **235919008** - Symptomatic cholelithiasis
- **65275009** - Acute cholecystitis
- **39337004** - Inguinal hernia
- **396275006** - Osteoarthritis
- **367498001** - Seasonal allergic rhinitis
- **80146002** - Appendectomy

### Section Codes
- **Primary:** 10219-4 - "Preoperative Diagnosis" (LOINC)
- **Code System:** 2.16.840.1.113883.6.1 (LOINC)

### Status Codes
- **active** - Current condition requiring surgery (most common)
- **inactive** - Condition not currently active (rare for preop)
- **resolved** - Not typically used for preoperative diagnoses

## Implementation Notes

### Narrative Generation

The builder automatically generates an HTML table with:
- Diagnosis name (with content ID for referencing)
- Code and code system
- Status
- Diagnosis date

### Entry Structure

The section uses an Act wrapper (Preoperative Diagnosis Act):
- Acts as container for Problem Observations
- Allows grouping related diagnoses
- Typically one Act contains one or more observations

### Multiple Diagnoses

Multiple preoperative diagnoses are common:
- Primary surgical indication
- Secondary conditions affecting surgery
- Comorbidities requiring surgical consideration

Example:
```python
diagnoses = [
    PreoperativeDiagnosis(
        name="Symptomatic inguinal hernia",  # Primary indication
        code="396232000",
        code_system="SNOMED"
    ),
    PreoperativeDiagnosis(
        name="Chronic obstructive pulmonary disease",  # Comorbidity
        code="13645005",
        code_system="SNOMED"
    )
]
```

### Integration in Operative Note

Standard operative note structure:
1. **Patient Information** - Demographics, identifiers
2. **Preoperative Diagnosis** - This section
3. **Postoperative Diagnosis** - Findings-based diagnosis
4. **Procedure(s) Performed** - What was done
5. **Surgeon/Team** - Who performed it
6. **Anesthesia** - Type and agents used
7. **Indications** - Why procedure was necessary
8. **Findings** - What was observed
9. **Procedure Description** - Step-by-step narrative
10. **Complications** - Any adverse events
11. **Estimated Blood Loss** - Operative details
12. **Specimens** - What was sent to pathology

### Clinical Decision Support

Preoperative diagnosis is used for:
- Justifying medical necessity of procedure
- Surgical planning and preparation
- Anesthesia planning
- Risk assessment and counseling
- Informed consent documentation
- Quality metrics and appropriateness
- Billing and reimbursement

### Coordination with Other Documentation

The preoperative diagnosis should be consistent with:
- **History and Physical:** Clinical evaluation leading to surgery
- **Indications:** Detailed rationale for procedure
- **Pre-operative Testing:** Diagnostic studies supporting diagnosis
- **Consent Forms:** What patient was told

### Suspected vs Confirmed

Preoperative diagnoses may be:
- **Confirmed:** Based on definitive testing (e.g., imaging, biopsy)
- **Suspected:** Based on clinical assessment pending operative confirmation
- **Rule-out:** Exploratory procedures to confirm or exclude diagnosis

Consider qualifying when uncertain:
```python
PreoperativeDiagnosis(
    name="Suspected acute appendicitis",
    code="74400008",
    code_system="SNOMED"
)
```

### Persistent IDs

While optional, persistent IDs are valuable for:
- Tracking diagnosis across multiple documents
- Reconciling pre-operative and post-operative diagnoses
- Longitudinal problem tracking
- Quality measurement and outcomes tracking

### Comparison Pattern

Document the relationship with postoperative diagnosis:

**Scenario 1: Diagnosis Confirmed**
- Preoperative: "Acute appendicitis"
- Postoperative: "Acute appendicitis (confirmed)"

**Scenario 2: Diagnosis Modified**
- Preoperative: "Acute appendicitis"
- Postoperative: "Perforated appendicitis with peritonitis"

**Scenario 3: Diagnosis Changed**
- Preoperative: "Acute appendicitis"
- Postoperative: "Ruptured ovarian cyst; normal appendix"
