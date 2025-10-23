# Postoperative Diagnosis Section

**Template ID:** 2.16.840.1.113883.10.20.22.2.35
**Version:** No specific version extension
**Badge:** Surgical Section

## Overview

The Postoperative Diagnosis Section records the diagnosis or diagnoses discovered or confirmed during surgery. This section documents the surgeon's final assessment after the procedure, which may confirm, refine, or differ from the preoperative diagnosis based on intraoperative findings.

### Clinical Purpose and Context

Postoperative diagnoses documented in this section represent:
- The final surgical diagnosis based on operative findings
- Conditions discovered or confirmed during the procedure
- The surgeon's post-surgical clinical assessment
- Pathological findings noted during surgery

Often the postoperative diagnosis matches the preoperative diagnosis, but it may differ if unexpected findings were discovered during the operation or if the suspected condition was ruled out.

### When to Include

The Postoperative Diagnosis Section is typically included in:
- **Operative Notes** (primary use case)
- **Surgical Procedure Notes**
- **Procedure Reports** for invasive procedures

This section is a standard component of surgical documentation and provides critical information for post-operative care, billing, and quality tracking.

## Template Details

### Official OID
- **Root:** 2.16.840.1.113883.10.20.22.2.35
- **Extension:** None specified

### Conformance Level
- **Conformance:** SHOULD (Recommended in Operative Notes)
- **Section Code:** 10218-6 (LOINC - "Postoperative Diagnosis")

### Cardinality
- **Section:** 0..1 (Optional but recommended for surgical documentation)
- **Entries:** None (Narrative-only section)

### Related Templates
This is a narrative-only section with no structured entries. Related structured data may appear in:
- **Procedures Section:** The surgical procedure performed
- **Findings Section:** Detailed operative findings

## Protocol Requirements

This section uses a simple string for the narrative text:

### Input Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `diagnosis_text` | `str` | The narrative describing the postoperative diagnosis |
| `title` | `str` | Section title (default: "Postoperative Diagnosis") |

### Data Constraints
- **diagnosis_text:** Free-text narrative describing the surgical diagnosis
  - Should be clear and clinically specific
  - May include multiple diagnoses
  - Can reference findings from surgery

## Code Example

Here's a complete working example using ccdakit to create a Postoperative Diagnosis Section:

```python
from ccdakit.builders.sections.postoperative_diagnosis import PostoperativeDiagnosisSection
from ccdakit.core.base import CDAVersion

# Example 1: Single diagnosis that confirms preoperative diagnosis
diagnosis_text = "Acute appendicitis with perforation"

section_builder = PostoperativeDiagnosisSection(
    diagnosis_text=diagnosis_text,
    title="Postoperative Diagnosis",
    version=CDAVersion.R2_1
)

# Example 2: Multiple diagnoses discovered during surgery
diagnosis_text = """1. Acute gangrenous appendicitis with perforation
2. Localized peritonitis
3. Adhesions from previous surgery"""

section_builder = PostoperativeDiagnosisSection(
    diagnosis_text=diagnosis_text,
    title="Postoperative Diagnosis",
    version=CDAVersion.R2_1
)

# Example 3: Diagnosis differs from preoperative assessment
diagnosis_text = """Ruptured ovarian cyst (preoperative diagnosis was acute appendicitis)"""

section_builder = PostoperativeDiagnosisSection(
    diagnosis_text=diagnosis_text,
    title="Postoperative Diagnosis",
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
- Section: Postoperative Diagnosis Section
- Conformance IDs: CONF:81-8101 through CONF:81-8104

## Best Practices

### Common Patterns

1. **Be Specific and Clinical**
   - Use precise surgical terminology
   - Include relevant details from operative findings
   - Describe severity or extent when relevant
   - Reference pathological findings if applicable

2. **Compare with Preoperative Diagnosis**
   - If diagnoses differ, note this explicitly
   - Explain why findings changed the diagnosis
   - This helps with clinical understanding and documentation

3. **Number Multiple Diagnoses**
   - Use numbered list format for multiple diagnoses
   - Order by clinical significance (primary first)
   - Include all significant findings

4. **Include Relevant Details**
   - Stage or grade if applicable
   - Anatomical location specifics
   - Extent of disease or pathology
   - Unexpected findings

### Validation Tips

1. **Section Code Validation**
   - Ensure section code is 10218-6 (LOINC "Postoperative Diagnosis")
   - This is automatically set by the builder

2. **Template ID Validation**
   - Verify template ID is 2.16.840.1.113883.10.20.22.2.35
   - No extension attribute for this template

3. **Narrative Requirements**
   - Section SHALL contain text element
   - Text should be substantive, not placeholder
   - Empty narratives may fail validation

4. **No Structured Entries**
   - This is a narrative-only section
   - Should not contain entry elements
   - Structured diagnosis data goes in other sections (e.g., Postoperative Diagnosis entries in Problems)

### Common Pitfalls

1. **Too Brief or Vague**
   - Avoid minimal text like "As above" or "Same"
   - Even if diagnosis matches preoperative, restate it
   - Provide complete diagnostic statement

2. **Missing Clinical Details**
   - Don't omit important findings discovered during surgery
   - Include extent, severity, or staging information
   - Document unexpected findings

3. **Not Coordinating with Preoperative**
   - Should relate to Preoperative Diagnosis Section
   - If different, explain why
   - If same, still document completely

4. **Confusing with Discharge Diagnosis**
   - Postoperative diagnosis is surgical assessment
   - Discharge diagnosis is overall hospital discharge assessment
   - Both may be present in same document

5. **Using Only Codes**
   - This is a narrative section
   - Don't just list diagnosis codes
   - Provide descriptive text

6. **Inconsistent with Procedure**
   - Should align with procedure performed
   - Diagnosis should match operative findings
   - Ensure consistency across operative note

## Related Sections

- **Preoperative Diagnosis Section:** Initial surgical diagnosis before procedure
- **Procedures Section:** The surgical procedure performed
- **Operative Note Surgical Procedure:** Detailed operative report
- **Findings Section:** Detailed operative findings
- **Complications Section:** Any complications that occurred

## Code Systems and Terminologies

### Section Codes
- **Primary:** 10218-6 - "Postoperative Diagnosis" (LOINC)
- **Code System:** 2.16.840.1.113883.6.1 (LOINC)

### Diagnosis Terminologies
While this is a narrative section, diagnoses mentioned should align with standard terminologies:
- **SNOMED CT** - Preferred for surgical diagnoses
- **ICD-10-CM** - For administrative/billing purposes

Common surgical diagnosis codes (SNOMED CT examples):
- **74400008** - Appendicitis
- **95568003** - Acute appendicitis with perforation
- **235595009** - Gastric ulcer
- **372070002** - Acute cholecystitis

## Implementation Notes

### Narrative-Only Section

This section contains only narrative text:
- No structured entry elements
- No coded diagnoses
- Plain text in paragraph format
- Simple and straightforward

### Text Formatting

The builder handles text formatting:
- Wraps text in a `<paragraph>` element
- Text is placed in the `<text>` element
- Preserves line breaks and formatting in the input text

### Coordination with Structured Data

While this section is narrative-only, consider:
- **Postoperative diagnoses as problems:** Can be captured as Problem Observations in Problems Section
- **Diagnosis codes:** Should be documented in structured sections if needed for data exchange
- **Billing codes:** Often derived from postoperative diagnosis narrative

### Comparison with Preoperative Diagnosis

Document the relationship:

**Case 1: Diagnosis Confirmed**
```
"Acute appendicitis (confirmed at surgery)"
```

**Case 2: Diagnosis Modified**
```
"Perforated appendicitis with abscess formation (preoperative diagnosis was uncomplicated acute appendicitis)"
```

**Case 3: Diagnosis Changed**
```
"Ruptured ovarian cyst. Note: Preoperative diagnosis was acute appendicitis, but intraoperative findings revealed normal appendix and ruptured right ovarian cyst."
```

### Multiple Diagnoses Format

For multiple diagnoses, use clear formatting:

```
1. Primary diagnosis (most significant)
2. Secondary diagnosis
3. Additional findings
```

Example:
```
1. Acute gangrenous appendicitis with perforation
2. Generalized peritonitis
3. Small bowel adhesions, lysed
```

### Integration in Operative Note

The Postoperative Diagnosis Section is part of the standard operative note structure:

1. **Preoperative Diagnosis** - What was suspected
2. **Procedure Performed** - What was done
3. **Postoperative Diagnosis** - What was found (this section)
4. **Indications** - Why procedure was needed
5. **Findings** - Detailed operative findings
6. **Complications** - Any adverse events

### Clinical Decision Support

The postoperative diagnosis is used for:
- Quality measurement and reporting
- Surgical outcomes tracking
- Appropriateness of procedure validation
- Risk stratification for post-operative care
- Billing and reimbursement
- Surgical registry reporting

### Pathology Correlation

If pathology specimens were taken:
- Postoperative diagnosis may be preliminary
- Final diagnosis may come from pathology
- Consider noting "pending pathology" if applicable
- Update diagnosis when final pathology available

Example:
```
"Suspicious right breast mass, clinical stage 2A. Final diagnosis pending pathology examination."
```

### Unexpected Findings

When operative findings differ from expectations:
- Clearly state the unexpected nature
- Explain what was found instead
- Note any change in surgical plan
- Document clinical significance

Example:
```
"Normal appendix with mesenteric adenitis. Appendectomy performed to exclude appendicitis. Preoperative diagnosis of acute appendicitis was not confirmed; symptoms likely due to mesenteric adenitis."
```
