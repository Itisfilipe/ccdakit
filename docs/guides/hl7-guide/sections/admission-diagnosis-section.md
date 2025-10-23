# Admission Diagnosis Section

**Template ID:** 2.16.840.1.113883.10.20.22.2.43
**Version:** R2.1 (2015-08-01)
**Badge:** Hospital Section

## Overview

The Admission Diagnosis Section contains a narrative description of the problems or diagnoses identified by the clinician at the time of the patient's admission to a hospital facility. This section documents the clinical reasoning for admission and may contain coded entries representing the admitting diagnoses.

### Clinical Purpose and Context

Admission diagnoses documented in this section represent:
- The primary reason(s) for hospital admission
- Clinical conditions identified at admission that require inpatient management
- Suspected diagnoses that warrant hospital-level observation or treatment
- Problems that necessitate the level of care provided in a hospital setting

Common examples include acute myocardial infarction, pneumonia, acute exacerbation of chronic conditions, or traumatic injuries requiring immediate hospital care.

### When to Include

The Admission Diagnosis Section is typically included in:
- **Discharge Summaries** (primary use case)
- **Transfer Summaries**
- **Hospital Course Documentation**

This section provides important context for understanding why the patient required hospitalization and helps establish the baseline clinical picture at the time of admission.

## Template Details

### Official OID
- **Root:** 2.16.840.1.113883.10.20.22.2.43
- **Extension:** 2015-08-01 (R2.1)

### Conformance Level
- **Conformance:** SHOULD (Recommended in Discharge Summary documents)
- **Section Code:** 46241-6 (LOINC - "Hospital Admission diagnosis")
- **Translation Code:** 42347-5 (LOINC - "Admission Diagnosis")

### Cardinality
- **Section:** 0..1 (Optional but recommended)
- **Entries:** 0..* (Hospital Admission Diagnosis entries)

### Related Templates
- **Hospital Admission Diagnosis (V3):** 2.16.840.1.113883.10.20.22.4.34:2015-08-01
- **Problem Observation (V3):** 2.16.840.1.113883.10.20.22.4.4:2015-08-01

## Protocol Requirements

The `AdmissionDiagnosisProtocol` defines the data contract for admission diagnosis entries. Each diagnosis must provide:

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Human-readable diagnosis name |
| `code` | `str` | SNOMED CT or ICD-10 diagnosis code |
| `code_system` | `str` | Code system: 'SNOMED' or 'ICD-10' |

### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `admission_date` | `Optional[date]` | Date of hospital admission |
| `diagnosis_date` | `Optional[date]` | Date diagnosis was identified |
| `persistent_id` | `Optional[PersistentIDProtocol]` | Persistent ID across document versions |

### Data Types and Constraints
- **name:** Clear, clinical description of the admission diagnosis
- **code:** Must be a valid SNOMED CT or ICD-10 code
- **code_system:** 'SNOMED' (preferred) or 'ICD-10'
- **admission_date:** Date patient was admitted to hospital (YYYYMMDD format)
- **diagnosis_date:** Date this specific diagnosis was identified (may differ from admission date)

## Code Example

Here's a complete working example using ccdakit to create an Admission Diagnosis Section:

```python
from datetime import date
from ccdakit.builders.sections.admission_diagnosis import AdmissionDiagnosisSection
from ccdakit.core.base import CDAVersion

# Define admission diagnoses using a class that implements AdmissionDiagnosisProtocol
class AdmissionDiagnosis:
    def __init__(self, name, code, code_system, admission_date=None, diagnosis_date=None):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._admission_date = admission_date
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
    def admission_date(self):
        return self._admission_date

    @property
    def diagnosis_date(self):
        return self._diagnosis_date

    @property
    def persistent_id(self):
        return self._persistent_id

# Create admission diagnosis instances
diagnoses = [
    AdmissionDiagnosis(
        name="Acute Myocardial Infarction",
        code="57054005",
        code_system="SNOMED",
        admission_date=date(2024, 10, 15),
        diagnosis_date=date(2024, 10, 15)
    ),
    AdmissionDiagnosis(
        name="Type 2 Diabetes Mellitus",
        code="44054006",
        code_system="SNOMED",
        admission_date=date(2024, 10, 15),
        diagnosis_date=date(2024, 10, 15)
    )
]

# Build the Admission Diagnosis Section
section_builder = AdmissionDiagnosisSection(
    diagnoses=diagnoses,
    title="Hospital Admission Diagnosis",
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
- Section: Admission Diagnosis Section (V3)
- Conformance IDs: CONF:1198-9930 through CONF:1198-32750

## Best Practices

### Common Patterns

1. **Use Standard Vocabularies**
   - Prefer SNOMED CT codes for better semantic interoperability
   - ICD-10 codes are acceptable and commonly used for billing-related documentation
   - Use the most specific code available that accurately represents the diagnosis

2. **Document Admission Context**
   - Include the admission date to provide temporal context
   - The diagnosis date may be the same as or earlier than the admission date
   - Document suspected diagnoses that warranted admission even if later ruled out

3. **Distinguish from Discharge Diagnoses**
   - Admission diagnoses represent what was known/suspected at admission
   - May differ from discharge diagnoses based on findings during hospitalization
   - Both sections may be present in the same Discharge Summary document

4. **Handle Multiple Diagnoses**
   - List primary admission diagnosis first if multiple diagnoses are present
   - Include all significant conditions that contributed to the admission decision
   - Each diagnosis becomes a separate Problem Observation within the entry

### Validation Tips

1. **Section Code Validation**
   - Ensure section code is 46241-6 (LOINC "Hospital Admission diagnosis")
   - Must include translation code 42347-5 (LOINC "Admission Diagnosis")
   - Both codes are automatically set by the builder

2. **Template ID Validation**
   - Verify template ID includes extension="2015-08-01" for R2.1
   - Multiple template IDs may be present for backward compatibility

3. **Entry Structure Validation**
   - Each entry contains a Hospital Admission Diagnosis Act (classCode="ACT")
   - Act contains Problem Observations via entryRelationship
   - Problem Observations use standard Problem Observation (V3) template

4. **Code System Mapping**
   - 'SNOMED' maps to OID 2.16.840.1.113883.6.96
   - 'ICD-10' maps to OID 2.16.840.1.113883.6.90
   - Builder handles OID mapping automatically

### Common Pitfalls

1. **Confusing with Discharge Diagnosis**
   - Don't use this section for final/discharge diagnoses
   - Admission diagnoses may be tentative or rule-out diagnoses
   - Use Discharge Diagnosis Section (2.16.840.1.113883.10.20.22.2.24) for discharge

2. **Missing Admission Date**
   - While optional, admission date provides critical context
   - Include whenever available for complete documentation
   - Helps establish timeline of care

3. **Inconsistent Dates**
   - Diagnosis date should not be after admission date
   - If diagnosis was made prior to admission, use the actual diagnosis date
   - Admission date should match the hospital admission timestamp

4. **Code System Format**
   - Use 'SNOMED' or 'ICD-10' as string values
   - Don't use OIDs directly (builder converts them)
   - Ensure codes are valid for the specified system

5. **Empty Section Handling**
   - If no admission diagnosis is documented, consider omitting the section
   - Alternatively, include narrative text stating "No admission diagnosis documented"
   - Empty entries may fail validation in some contexts

6. **Problem vs. Diagnosis Terminology**
   - C-CDA uses Problem Observation template for diagnoses
   - This is standard and correct per the specification
   - Don't be confused by "problem" terminology - it includes diagnoses

## Related Sections

- **Discharge Diagnosis Section:** Documents final diagnoses at discharge
- **Problems Section:** Documents ongoing/chronic problems
- **Hospital Course Section:** Narrative describing the hospitalization
- **Chief Complaint and Reason for Visit:** Documents presenting symptoms

## Code Systems and Terminologies

### Diagnosis Codes
- **SNOMED CT (Preferred):** OID 2.16.840.1.113883.6.96
  - Provides detailed clinical terminology
  - Better for interoperability and clinical decision support

- **ICD-10-CM:** OID 2.16.840.1.113883.6.90
  - Commonly used for billing and administrative purposes
  - May be required by some systems

### Section Codes
- **Primary:** 46241-6 - "Hospital Admission diagnosis" (LOINC)
- **Translation:** 42347-5 - "Admission Diagnosis" (LOINC)

### Status Codes
- Admission diagnoses are typically documented as "active" at time of admission
- Use Problem Status value set (2.16.840.1.113883.3.88.12.80.68) for status values

## Implementation Notes

### Narrative Generation
The builder automatically generates an HTML table in the narrative section with:
- Diagnosis name (with content ID for referencing)
- Code and code system
- Admission date
- Diagnosis date

### Multiple Diagnoses
Multiple admission diagnoses are common and fully supported:
- Each diagnosis becomes a separate entry
- Each entry contains a Hospital Admission Diagnosis Act
- Acts contain Problem Observations representing the specific diagnoses

### Persistent IDs
While optional, persistent IDs are valuable for:
- Tracking diagnoses across multiple documents
- Reconciling admission vs discharge diagnoses
- Supporting continuity of care across episodes

### Integration with Other Sections
Consider coordinating with:
- **Problems Section:** May include same diagnoses as ongoing problems
- **Discharge Diagnosis Section:** Compare admission vs discharge diagnoses
- **Hospital Course:** Narrative explanation of how diagnoses evolved
