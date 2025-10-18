# Social History Section

**Template ID:** 2.16.840.1.113883.10.20.22.2.17
**Version:** R2.1 (2015-08-01)
**Badge:** Core Section

## Overview

The Social History Section documents social and behavioral factors that influence a patient's physical, psychological, or emotional health. This includes smoking status, alcohol use, drug use, occupation, living situation, and other social determinants of health. This implementation focuses primarily on smoking status as required by Meaningful Use.

### Clinical Purpose and Context

The Social History Section records:
- Smoking status (required by Meaningful Use)
- Alcohol and substance use
- Occupation and occupational hazards
- Living situation and social support
- Sexual history and practices
- Education level
- Religious and cultural practices
- Pregnancy status

This information is essential for:
- Comprehensive patient assessment
- Risk stratification and prevention
- Treatment planning and counseling
- Meeting Meaningful Use Stage 2 requirements
- Addressing social determinants of health
- Population health management

### When to Include

The Social History Section is commonly included in:
- Continuity of Care Documents (CCD)
- History and Physical Notes
- Consultation Notes
- Annual wellness visits
- Preventive care visits

Smoking status is **required** by Meaningful Use Stage 2 and must be documented for eligible patients.

## Template Details

### Official OID
- **Root:** 2.16.840.1.113883.10.20.22.2.17
- **Extension:** 2015-08-01 (V3)

### Conformance Level
- **Conformance:** SHOULD (Recommended; SHALL for Meaningful Use compliance)
- **Section Code:** 29762-2 (LOINC - "Social History")

### Cardinality
- **Section:** 0..1 (Optional but highly recommended)
- **Entries:** 0..* (At least one Smoking Status observation is required for Meaningful Use)

### Related Templates
- **Smoking Status - Meaningful Use (V2):** 2.16.840.1.113883.10.20.22.4.78:2014-06-09
- **Social History Observation (V3):** 2.16.840.1.113883.10.20.22.4.38:2015-08-01
- **Pregnancy Observation:** 2.16.840.1.113883.10.20.15.3.8
- **Tobacco Use (V2):** 2.16.840.1.113883.10.20.22.4.85:2014-06-09

## Protocol Requirements

The `SmokingStatusProtocol` defines the data contract for smoking status observations (the primary social history observation type). Each smoking status observation must provide:

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `smoking_status` | `str` | Description of smoking status |
| `code` | `str` | SNOMED CT code from Smoking Status Value Set |
| `date` | `date` or `datetime` | Date when smoking status was observed |

### Data Types and Constraints
- **smoking_status:** Human-readable status (e.g., "Current every day smoker", "Former smoker", "Never smoker")
- **code:** SNOMED CT code from value set 2.16.840.1.113883.11.20.9.38
- **date:** Point-in-time observation (not an interval)

### Common Smoking Status Codes

| Code | Display Name |
|------|-------------|
| 449868002 | Current every day smoker |
| 428041000124106 | Current some day smoker |
| 8517006 | Former smoker |
| 266919005 | Never smoker |
| 266927001 | Unknown if ever smoked |
| 77176002 | Smoker, current status unknown |
| 428071000124103 | Current Heavy tobacco smoker |
| 428061000124105 | Current Light tobacco smoker |

## Code Example

Here's a complete working example using ccdakit to create a Social History Section:

```python
from datetime import date, datetime
from ccdakit.builders.sections.social_history import SocialHistorySection
from ccdakit.core.base import CDAVersion

# Define a smoking status using a simple class that implements SmokingStatusProtocol
class SmokingStatus:
    def __init__(self, smoking_status, code, date):
        self.smoking_status = smoking_status
        self.code = code
        self.date = date

# Create smoking status instance
smoking_statuses = [
    SmokingStatus(
        smoking_status="Former smoker",
        code="8517006",
        date=date(2023, 10, 18)
    )
]

# Build the Social History Section
section_builder = SocialHistorySection(
    smoking_statuses=smoking_statuses,
    title="Social History",
    version=CDAVersion.R2_1
)

# Generate XML element
section_element = section_builder.build()

# Convert to XML string (for demonstration)
from lxml import etree
xml_string = etree.tostring(section_element, pretty_print=True, encoding='unicode')
print(xml_string)
```

### Example with Multiple Observations

```python
from datetime import date
from ccdakit.builders.sections.social_history import SocialHistorySection
from ccdakit.core.base import CDAVersion

class SmokingStatus:
    def __init__(self, smoking_status, code, date):
        self.smoking_status = smoking_status
        self.code = code
        self.date = date

# Track smoking status over time
smoking_statuses = [
    # Current status (most recent)
    SmokingStatus(
        smoking_status="Former smoker",
        code="8517006",
        date=date(2023, 10, 18)
    ),
    # Historical status for reference
    SmokingStatus(
        smoking_status="Current every day smoker",
        code="449868002",
        date=date(2020, 1, 15)
    )
]

section_builder = SocialHistorySection(
    smoking_statuses=smoking_statuses,
    title="Social History",
    version=CDAVersion.R2_1
)

section_element = section_builder.build()
```

## Official Reference

For complete specification details, refer to the official HL7 C-CDA R2.1 documentation:
- [HL7 C-CDA R2.1 Implementation Guide](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=492)
- Section: 5.56 - Social History Section

Additional resources:
- [Meaningful Use Stage 2 Requirements](https://www.cms.gov/regulations-and-guidance/legislation/ehrincentiveprograms)
- [SNOMED CT Smoking Status Value Set](https://vsac.nlm.nih.gov/)

## Best Practices

### Common Patterns

1. **Always Document Smoking Status**
   - Required for Meaningful Use Stage 2
   - Update at each visit or annually
   - Use most current status
   - Document as point-in-time observation, not historical interval

2. **Use Correct SNOMED CT Codes**
   - Use codes from the Smoking Status Value Set
   - Most common: "Never smoker" (266919005), "Former smoker" (8517006), "Current every day smoker" (449868002)
   - Don't use codes outside the value set
   - Unknown status: use "Unknown if ever smoked" (266927001)

3. **Document Current Status**
   - Smoking status represents current status at the time of observation
   - Not a historical summary
   - Update when status changes
   - Most recent observation is considered current

4. **Include Date of Observation**
   - Document when status was assessed
   - Important for determining currency of information
   - Use encounter date or assessment date
   - Can use datetime for precision

5. **Consider Additional Social History**
   - While smoking is required, consider documenting:
     - Alcohol use
     - Substance use
     - Occupation
     - Living situation
     - Sexual activity
   - Use appropriate observation templates for each

### Validation Tips

1. **Section Code Validation**
   - Ensure section code is 29762-2 (LOINC "Social History")
   - This is automatically set by the builder

2. **Template ID Validation**
   - Verify template ID includes extension="2015-08-01"
   - Smoking Status observation uses different template: 2.16.840.1.113883.10.20.22.4.78:2014-06-09

3. **Code Validation**
   - Verify smoking status codes are from the approved value set
   - Value Set OID: 2.16.840.1.113883.11.20.9.38
   - Use VSAC (Value Set Authority Center) for validation

4. **Observation Code Validation**
   - Smoking status observations use code 72166-2 (LOINC "Tobacco smoking status NHIS")
   - This is the required observation code for Meaningful Use

5. **Value Element Validation**
   - The smoking status code goes in the value element, not the code element
   - value element uses SNOMED CT codes
   - code element uses LOINC code 72166-2

### Gotchas to Avoid

1. **Code vs. Value Confusion**
   - observation/code = 72166-2 (LOINC - what is being observed)
   - observation/value = SNOMED CT code (the observed status)
   - Don't put the smoking status code in the code element

2. **Using Wrong Value Set**
   - Must use codes from Smoking Status Value Set (2.16.840.1.113883.11.20.9.38)
   - Don't use generic tobacco use codes
   - Don't create custom codes

3. **Missing Smoking Status**
   - Meaningful Use requires smoking status for eligible patients
   - Don't omit section entirely
   - If unknown, use "Unknown if ever smoked" (266927001)
   - Required for patients 13 years and older

4. **Incorrect Date Interpretation**
   - Date is when status was observed, not when smoking started/stopped
   - Don't use date patient quit smoking
   - Use date of clinical encounter or assessment

5. **Historical vs. Current Status**
   - Document current status, not smoking history
   - "Former smoker" is a current status
   - Don't create multiple entries unless status changed
   - Most recent observation is considered current

6. **Status Changes**
   - When status changes, create new observation
   - Both observations can be included for context
   - Most recent date indicates current status

7. **Pediatric Patients**
   - Meaningful Use applies to patients 13 years and older
   - Consider age-appropriate codes
   - "Never smoker" is common for adolescents
   - Document even if status seems obvious

8. **Pregnancy Status Confusion**
   - Pregnancy is documented separately
   - Uses different observation template
   - Don't confuse with smoking status
   - Both can be in Social History section

9. **Text Description Mismatch**
   - Ensure smoking_status text matches the code
   - Builder uses provided text in narrative
   - Should be consistent with SNOMED CT display name

10. **Empty Social History Section**
    - While section is optional, smoking status is required for MU
    - Include section even if only documenting smoking status
    - Don't rely on other sections for smoking documentation

11. **Substance Use Documentation**
    - If documenting substance use, use appropriate templates
    - Tobacco Use observation (2.16.840.1.113883.10.20.22.4.85) for details
    - Smoking Status observation for MU requirement
    - Different templates serve different purposes

12. **Narrative-Entry Consistency**
    - Ensure narrative matches structured data
    - Builder handles this automatically
    - Include status and date in narrative
    - Important for human readability

13. **Multiple Social History Types**
    - Section can contain multiple observation types
    - Each type uses its own template
    - Current builder implementation focuses on smoking status
    - Extensible for additional social history observations

14. **Point in Time vs. Interval**
    - Smoking status is point in time (effectiveTime with single value)
    - Not a time interval (no low/high)
    - Represents status at observation date
    - Different from habits documented over time

15. **Quality Reporting**
    - Smoking status used in many quality measures
    - Currency matters (within last 24 months typically)
    - Accurate coding essential for quality reporting
    - Impacts meaningful use attestation
