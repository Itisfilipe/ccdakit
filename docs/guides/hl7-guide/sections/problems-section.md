# Problems Section

**Template ID:** 2.16.840.1.113883.10.20.22.2.5.1
**Version:** R2.1 (2015-08-01)
**Badge:** Core Section

## Overview

The Problems Section contains a list of a patient's current and historical health problems, conditions, and diagnoses. This section is fundamental to clinical documentation as it provides a comprehensive view of a patient's active medical issues and their clinical status over time.

### Clinical Purpose and Context

Problems documented in this section represent conditions that:
- Require ongoing clinical management or monitoring
- Have been diagnosed or are under investigation
- May impact treatment decisions or patient outcomes
- Include both acute conditions and chronic diseases

Common examples include diabetes, hypertension, asthma, depression, and any other diagnosed medical conditions that affect patient care.

### When to Include

The Problems Section is a **required section** in most C-CDA document types, including:
- Continuity of Care Documents (CCD)
- Consultation Notes
- Discharge Summaries
- Progress Notes
- Transfer Summaries

Even if a patient has no known problems, the section should be included with narrative text stating "No known problems."

## Template Details

### Official OID
- **Root:** 2.16.840.1.113883.10.20.22.2.5.1
- **Extension:** 2015-08-01 (R2.1)

### Conformance Level
- **Conformance:** SHALL (Required in entries-required variant)
- **Section Code:** 11450-4 (LOINC - "Problem List")

### Cardinality
- **Section:** 1..1 (Required in most C-CDA document types)
- **Entries:** 1..* (At least one Problem Concern Act entry is required for entries-required variant)

### Related Templates
- **Problem Concern Act (V3):** 2.16.840.1.113883.10.20.22.4.3:2015-08-01
- **Problem Observation (V3):** 2.16.840.1.113883.10.20.22.4.4:2015-08-01

## Protocol Requirements

The `ProblemProtocol` defines the data contract for problem entries. Each problem must provide:

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Human-readable problem name |
| `code` | `str` | SNOMED CT or ICD-10 code |
| `code_system` | `str` | Code system: 'SNOMED' or 'ICD-10' |
| `status` | `str` | Status: 'active', 'inactive', 'resolved' |

### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `onset_date` | `Optional[date]` | Date problem was identified/started |
| `resolved_date` | `Optional[date]` | Date problem was resolved (None if ongoing) |
| `persistent_id` | `Optional[PersistentIDProtocol]` | Persistent ID across document versions |

### Data Types and Constraints
- **name:** Free-text description of the problem
- **code:** Must be a valid code from the specified code system
- **code_system:** Currently supports 'SNOMED' (SNOMED CT) or 'ICD-10'
- **status:** Determines the concern act's statusCode ('active' -> active, others -> completed)
- **onset_date:** Formatted as YYYYMMDD in CDA XML
- **resolved_date:** Only used when status is not 'active'

## Code Example

Here's a complete working example using ccdakit to create a Problems Section:

```python
from datetime import date
from ccdakit.builders.sections.problems import ProblemsSection
from ccdakit.core.base import CDAVersion

# Define a problem using a simple class that implements ProblemProtocol
class Problem:
    def __init__(self, name, code, code_system, status, onset_date=None, resolved_date=None):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._status = status
        self._onset_date = onset_date
        self._resolved_date = resolved_date
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
    def onset_date(self):
        return self._onset_date

    @property
    def resolved_date(self):
        return self._resolved_date

    @property
    def persistent_id(self):
        return self._persistent_id

# Create problem instances
problems = [
    Problem(
        name="Type 2 Diabetes Mellitus",
        code="44054006",
        code_system="SNOMED",
        status="active",
        onset_date=date(2020, 3, 15)
    ),
    Problem(
        name="Essential Hypertension",
        code="59621000",
        code_system="SNOMED",
        status="active",
        onset_date=date(2019, 6, 1)
    ),
    Problem(
        name="Acute Bronchitis",
        code="10509002",
        code_system="SNOMED",
        status="resolved",
        onset_date=date(2023, 1, 10),
        resolved_date=date(2023, 1, 24)
    )
]

# Build the Problems Section
section_builder = ProblemsSection(
    problems=problems,
    title="Problems",
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
- Section: 5.39 - Problems Section (entries required)

## Best Practices

### Common Patterns

1. **Use Standard Vocabularies**
   - Prefer SNOMED CT codes for better interoperability
   - ICD-10 codes are acceptable but may have less granularity
   - Use the most specific code available

2. **Maintain Problem Status Accurately**
   - Active problems should use status='active'
   - Resolved problems should use status='resolved' with a resolved_date
   - Use status='inactive' for problems that are not currently being managed but may recur

3. **Include Onset Dates When Known**
   - Onset dates provide important clinical context
   - Use nullFlavor="UNK" if the date is truly unknown (handled automatically by the builder)

4. **Group Related Problems Appropriately**
   - Each problem becomes a separate Problem Concern Act
   - The concern act wraps one or more problem observations
   - Related problems can be grouped in the same concern act if needed

### Validation Tips

1. **Section Code Validation**
   - Ensure section code is 11450-4 (LOINC "Problem List")
   - This is automatically set by the builder

2. **Template ID Validation**
   - Verify the template ID includes both root and extension attributes
   - R2.1 uses extension="2015-08-01"

3. **Entry Structure Validation**
   - Each entry must contain a Problem Concern Act (classCode="ACT", moodCode="EVN")
   - Problem Concern Act must contain at least one Problem Observation via entryRelationship

4. **Status Code Consistency**
   - Concern Act statusCode should be 'active' for active problems
   - Concern Act statusCode should be 'completed' for resolved/inactive problems
   - Problem Observation statusCode should always be 'completed' (observation is complete)

### Gotchas to Avoid

1. **Missing Required Elements**
   - Always include at least one problem entry in entries-required variant
   - If no problems exist, use entries-optional variant or include a "no known problems" statement

2. **Incorrect Code Systems**
   - code_system should be 'SNOMED' or 'ICD-10', not the OID
   - The builder automatically converts these to the appropriate OIDs

3. **Date Format Issues**
   - Use Python date objects, not strings
   - The builder handles formatting to CDA TS format (YYYYMMDD)

4. **Status Mismatch**
   - Don't mark a problem as 'active' if it has a resolved_date
   - Don't provide a resolved_date for 'active' problems

5. **Empty Problem Lists**
   - An empty problem list may fail validation in entries-required contexts
   - Consider using the entries-optional variant (2.16.840.1.113883.10.20.22.2.5) if no problems exist

6. **Persistent IDs**
   - While optional, persistent IDs are valuable for tracking problems across documents
   - If not provided, problems will receive new UUIDs in each document

7. **Narrative-Entry Mismatch**
   - Ensure narrative table content matches structured entries
   - The builder handles this automatically but be aware when customizing
