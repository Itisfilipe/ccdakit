# Procedures Section

**Template ID:** 2.16.840.1.113883.10.20.22.2.7.1
**Version:** R2.1 (2014-06-09)
**Badge:** Core Section

## Overview

The Procedures Section documents surgical, diagnostic, and therapeutic procedures performed on or for the patient. This section provides a comprehensive record of interventions and procedures that are clinically significant for patient care.

### Clinical Purpose and Context

The Procedures Section records:
- Surgical procedures (e.g., appendectomy, knee replacement)
- Diagnostic procedures (e.g., colonoscopy, cardiac catheterization)
- Therapeutic procedures (e.g., physical therapy, dialysis)
- Procedure dates and status
- Performing provider information
- Body sites and laterality

This information is essential for:
- Understanding patient's surgical history
- Identifying procedures relevant to current conditions
- Coordinating post-procedure care
- Supporting billing and coding
- Meeting quality reporting requirements
- Care planning and clinical decision-making

### When to Include

The Procedures Section is commonly included in:
- Continuity of Care Documents (CCD)
- Discharge Summaries
- Operative Notes
- Consultation Notes
- Transfer Summaries
- History and Physical Notes

The section may be optional in some document types but is highly recommended when procedures have been performed or are clinically relevant to the patient's history.

## Template Details

### Official OID
- **Root:** 2.16.840.1.113883.10.20.22.2.7.1
- **Extension:** 2014-06-09 (R2.1 and R2.0)

### Conformance Level
- **Conformance:** MAY or SHOULD (depending on document type; SHALL in operative notes)
- **Section Code:** 47519-4 (LOINC - "History of Procedures")

### Cardinality
- **Section:** 0..1 (Optional in most document types, required in operative notes)
- **Entries:** 1..* (If section is present, at least one Procedure Activity entry is required)

### Related Templates
- **Procedure Activity Procedure (V2):** 2.16.840.1.113883.10.20.22.4.14:2014-06-09
- **Procedure Activity Observation (V2):** 2.16.840.1.113883.10.20.22.4.13:2014-06-09
- **Procedure Activity Act (V2):** 2.16.840.1.113883.10.20.22.4.12:2014-06-09

## Protocol Requirements

The `ProcedureProtocol` defines the data contract for procedure entries. Each procedure must provide:

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Procedure name/description |
| `code` | `str` | Procedure code |
| `code_system` | `str` | Code system: 'SNOMED CT', 'CPT-4', 'LOINC', 'ICD10 PCS', etc. |
| `status` | `str` | Status: 'completed', 'active', 'aborted', 'cancelled' |

### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `date` | `Optional[date \| datetime]` | Date/time when procedure was performed |
| `target_site` | `Optional[str]` | Target body site description |
| `target_site_code` | `Optional[str]` | SNOMED CT code for target body site |
| `performer_name` | `Optional[str]` | Name of person/entity who performed procedure |

### Data Types and Constraints
- **name:** Free-text procedure description (e.g., "Appendectomy", "Colonoscopy")
- **code:** Must be from an appropriate code system (LOINC, SNOMED CT, CPT-4, ICD10 PCS, HCPCS, CDT-2)
- **code_system:** Name of the code system
- **status:** Reflects completion state of the procedure
- **date:** Can be date or datetime; use datetime for surgical procedures with specific timing
- **target_site:** Body location where procedure was performed (e.g., "Right knee", "Abdomen")
- **target_site_code:** SNOMED CT anatomical site code
- **performer_name:** Provider who performed the procedure

## Code Example

Here's a complete working example using ccdakit to create a Procedures Section:

```python
from datetime import date, datetime
from ccdakit.builders.sections.procedures import ProceduresSection
from ccdakit.core.base import CDAVersion

# Define a procedure using a simple class that implements ProcedureProtocol
class Procedure:
    def __init__(self, name, code, code_system, status, date=None,
                 target_site=None, target_site_code=None, performer_name=None):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._status = status
        self._date = date
        self._target_site = target_site
        self._target_site_code = target_site_code
        self._performer_name = performer_name

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
    def date(self):
        return self._date

    @property
    def target_site(self):
        return self._target_site

    @property
    def target_site_code(self):
        return self._target_site_code

    @property
    def performer_name(self):
        return self._performer_name

# Create procedure instances
procedures = [
    Procedure(
        name="Appendectomy",
        code="80146002",
        code_system="SNOMED CT",
        status="completed",
        date=datetime(2022, 5, 15, 10, 30),
        target_site="Abdomen",
        target_site_code="818983003",
        performer_name="Dr. Sarah Johnson"
    ),
    Procedure(
        name="Colonoscopy",
        code="73761001",
        code_system="SNOMED CT",
        status="completed",
        date=date(2023, 8, 20),
        target_site="Colon",
        target_site_code="71854001",
        performer_name="Dr. Michael Chen"
    ),
    Procedure(
        name="Total knee replacement",
        code="609588000",
        code_system="SNOMED CT",
        status="completed",
        date=date(2021, 3, 10),
        target_site="Right knee",
        target_site_code="72696002",
        performer_name="Dr. Emily Rodriguez"
    ),
    Procedure(
        name="Cardiac catheterization",
        code="41976001",
        code_system="SNOMED CT",
        status="completed",
        date=datetime(2023, 1, 5, 14, 0),
        target_site="Heart",
        target_site_code="80891009",
        performer_name="Dr. James Williams"
    )
]

# Build the Procedures Section
section_builder = ProceduresSection(
    procedures=procedures,
    title="Procedures",
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
- Section: 5.44 - Procedures Section (entries required)

## Best Practices

### Common Patterns

1. **Use Appropriate Code Systems**
   - SNOMED CT: Broad coverage of clinical procedures
   - CPT-4: US billing and administrative codes
   - LOINC: Laboratory and diagnostic procedures
   - ICD10 PCS: Inpatient hospital procedures (US)
   - Choose based on use case and regional requirements

2. **Document Clinically Significant Procedures**
   - Include procedures relevant to current care
   - Major surgical procedures
   - Diagnostic procedures with significant findings
   - Therapeutic procedures affecting treatment plan
   - Consider excluding routine minor procedures unless relevant

3. **Specify Target Sites with Laterality**
   - Include body site when relevant
   - Specify laterality (left/right) when applicable
   - Use SNOMED CT codes for consistency
   - Example: "Right knee" not just "knee"

4. **Include Performer Information**
   - Document performing provider when known
   - Important for care coordination
   - Supports follow-up and consultation
   - May be required for billing

5. **Use Precise Date/Time When Available**
   - Surgical procedures: use datetime with time
   - Historical procedures: date may be sufficient
   - Precision supports timeline reconstruction
   - Important for perioperative care

### Validation Tips

1. **Section Code Validation**
   - Ensure section code is 47519-4 (LOINC "History of Procedures")
   - This is automatically set by the builder

2. **Template ID Validation**
   - Verify template ID includes extension="2014-06-09"
   - Same extension used for both R2.1 and R2.0

3. **Procedure Activity Type Selection**
   - Three templates available: Procedure, Observation, Act
   - Most surgical/diagnostic procedures use Procedure template
   - Educational activities may use Act template
   - Choose appropriate template for procedure type

4. **Code System OID Mapping**
   - Verify code system OIDs are correct:
     - SNOMED CT: 2.16.840.1.113883.6.96
     - CPT-4: 2.16.840.1.113883.6.12
     - LOINC: 2.16.840.1.113883.6.1
     - ICD10 PCS: 2.16.840.1.113883.6.4

5. **Status Code Validation**
   - Use appropriate status codes
   - 'completed' for finished procedures
   - 'active' for ongoing procedures (rare)
   - 'aborted' for procedures started but not completed
   - 'cancelled' for procedures cancelled before starting

### Gotchas to Avoid

1. **Missing Procedure Dates**
   - While optional in protocol, dates are highly recommended
   - Procedures without dates have limited clinical value
   - Use nullFlavor only when date is truly unknown

2. **Incorrect Code System Selection**
   - Don't use ICD-10-CM for procedures (diagnosis codes)
   - Use ICD10 PCS for inpatient procedures
   - CPT-4 for outpatient/professional services
   - SNOMED CT works across settings

3. **Incomplete Body Site Information**
   - Specify laterality when applicable
   - "Knee replacement" → "Right knee replacement"
   - Missing laterality can lead to errors
   - Use target_site_code for structured representation

4. **Overly Broad Procedure Descriptions**
   - Use specific codes when available
   - "Surgery" is too vague
   - "Laparoscopic appendectomy" better than "abdominal surgery"
   - Specificity supports quality measurement

5. **Confusing Procedure Status**
   - Most historical procedures should be 'completed'
   - 'active' is for ongoing procedures (e.g., chemotherapy series)
   - Don't use 'active' for planned future procedures
   - Use Care Plan section for future procedures

6. **Date Format Inconsistencies**
   - Use Python date or datetime objects
   - Builder handles CDA formatting
   - Don't mix dates and datetimes inconsistently
   - Consider clinical context for precision needs

7. **Missing Performer for Significant Procedures**
   - Document surgeon for major procedures
   - Supports follow-up care
   - May be required for specific document types
   - Can use organization if individual unknown

8. **Duplicate Procedure Entries**
   - Avoid documenting same procedure multiple times
   - If procedure has multiple stages, consider using episode ID
   - Consolidate when reconciling from multiple sources

9. **Including Non-Procedures**
   - Don't include observations as procedures
   - Lab tests go in Results section, not Procedures
   - Physical exam findings go in Physical Exam section
   - Medication administration goes in Medications section

10. **Implant Information**
    - For procedures involving implants, consider using device observation
    - UDI (Unique Device Identifier) may be required
    - Important for recalls and tracking

11. **Procedure Context**
    - Consider documenting indication/reason for procedure
    - Can use entryRelationship with indication observation
    - Links procedure to problem/condition

12. **Historical Data Quality**
    - Patient-reported procedures may lack detail
    - Document information source
    - May need to verify with medical records
    - Use appropriate nullFlavors for missing data

13. **Narrative-Entry Consistency**
    - Ensure narrative table matches structured entries
    - Builder handles this automatically
    - Include key details: date, site, performer in narrative

14. **Procedure Complications**
    - Consider documenting significant complications
    - Can use entryRelationship with problem observation
    - Important for complete clinical picture
