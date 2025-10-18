# Allergies and Intolerances Section

**Template ID:** 2.16.840.1.113883.10.20.22.2.6.1
**Version:** R2.1 (2015-08-01)
**Badge:** Core Section

## Overview

The Allergies and Intolerances Section documents a patient's allergic reactions and non-allergic adverse reactions to substances. This critical safety information helps prevent exposure to allergens and substances that could cause harm to the patient.

### Clinical Purpose and Context

The Allergies and Intolerances Section records:
- Documented allergies to medications, foods, and environmental substances
- Drug intolerances and adverse reactions
- Severity of allergic reactions
- Types of reactions experienced (e.g., rash, anaphylaxis)
- Current status of the allergy (active or resolved)

This information is essential for:
- Preventing adverse drug events
- Informing prescribing decisions
- Guiding treatment planning
- Ensuring patient safety across care settings
- Meeting Meaningful Use requirements

### When to Include

The Allergies Section is a **required section** in virtually all C-CDA document types, including:
- Continuity of Care Documents (CCD)
- Discharge Summaries
- Transfer Summaries
- Consultation Notes
- Progress Notes
- History and Physical Notes

Even if a patient has no known allergies, the section **must** be included with narrative text stating "No known allergies."

## Template Details

### Official OID
- **Root:** 2.16.840.1.113883.10.20.22.2.6.1
- **Extension:** 2015-08-01 (R2.1)

### Conformance Level
- **Conformance:** SHALL (Required in all standard C-CDA documents)
- **Section Code:** 48765-2 (LOINC - "Allergies and adverse reactions Document")

### Cardinality
- **Section:** 1..1 (Required)
- **Entries:** 1..* (At least one Allergy Concern Act entry is required)

### Related Templates
- **Allergy Concern Act (V3):** 2.16.840.1.113883.10.20.22.4.30:2015-08-01
- **Allergy Observation (V2):** 2.16.840.1.113883.10.20.22.4.7:2014-06-09

## Protocol Requirements

The `AllergyProtocol` defines the data contract for allergy entries. Each allergy must provide:

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `allergen` | `str` | Human-readable allergen name |
| `allergy_type` | `str` | Type: 'allergy' or 'intolerance' |
| `status` | `str` | Status: 'active' or 'resolved' |

### Optional Properties

| Property | Type | Description |
|----------|------|-------------|
| `allergen_code` | `Optional[str]` | RxNorm, UNII, or SNOMED CT code |
| `allergen_code_system` | `Optional[str]` | Code system: 'RxNorm', 'UNII', 'SNOMED CT' |
| `reaction` | `Optional[str]` | Reaction/manifestation description |
| `severity` | `Optional[str]` | Severity: 'mild', 'moderate', 'severe', 'fatal' |
| `onset_date` | `Optional[date]` | Date when allergy was first identified |

### Data Types and Constraints
- **allergen:** Free-text name (e.g., "Penicillin", "Peanuts", "Latex")
- **allergen_code:** Preferred code systems are RxNorm (drugs), UNII (substances), SNOMED CT
- **allergy_type:** Distinguishes true allergies from intolerances
- **reaction:** Clinical manifestation (e.g., "Hives", "Anaphylaxis", "Nausea")
- **severity:** Clinical severity assessment
- **status:** Determines the concern act's statusCode
- **onset_date:** When the allergy was first identified or occurred

## Code Example

Here's a complete working example using ccdakit to create an Allergies Section:

```python
from datetime import date
from ccdakit.builders.sections.allergies import AllergiesSection
from ccdakit.core.base import CDAVersion

# Define an allergy using a simple class that implements AllergyProtocol
class Allergy:
    def __init__(self, allergen, allergy_type, status, allergen_code=None,
                 allergen_code_system=None, reaction=None, severity=None, onset_date=None):
        self._allergen = allergen
        self._allergen_code = allergen_code
        self._allergen_code_system = allergen_code_system
        self._allergy_type = allergy_type
        self._reaction = reaction
        self._severity = severity
        self._status = status
        self._onset_date = onset_date

    @property
    def allergen(self):
        return self._allergen

    @property
    def allergen_code(self):
        return self._allergen_code

    @property
    def allergen_code_system(self):
        return self._allergen_code_system

    @property
    def allergy_type(self):
        return self._allergy_type

    @property
    def reaction(self):
        return self._reaction

    @property
    def severity(self):
        return self._severity

    @property
    def status(self):
        return self._status

    @property
    def onset_date(self):
        return self._onset_date

# Create allergy instances
allergies = [
    Allergy(
        allergen="Penicillin",
        allergen_code="7980",
        allergen_code_system="RxNorm",
        allergy_type="allergy",
        reaction="Hives",
        severity="moderate",
        status="active",
        onset_date=date(2015, 6, 10)
    ),
    Allergy(
        allergen="Peanuts",
        allergen_code="256349004",
        allergen_code_system="SNOMED CT",
        allergy_type="allergy",
        reaction="Anaphylaxis",
        severity="severe",
        status="active",
        onset_date=date(2010, 3, 22)
    ),
    Allergy(
        allergen="Latex",
        allergen_code="111088007",
        allergen_code_system="SNOMED CT",
        allergy_type="allergy",
        reaction="Contact dermatitis",
        severity="mild",
        status="active"
    ),
    Allergy(
        allergen="Aspirin",
        allergen_code="1191",
        allergen_code_system="RxNorm",
        allergy_type="intolerance",
        reaction="Nausea",
        severity="mild",
        status="active",
        onset_date=date(2018, 9, 5)
    )
]

# Build the Allergies Section
section_builder = AllergiesSection(
    allergies=allergies,
    title="Allergies and Intolerances",
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
- Section: 5.5 - Allergies and Intolerances Section (entries required)

## Best Practices

### Common Patterns

1. **Always Document "No Known Allergies"**
   - Never omit the Allergies section
   - If no allergies exist, include the section with "No known allergies" narrative
   - Use a special "No Known Allergies" observation if required by your implementation

2. **Use Appropriate Code Systems**
   - RxNorm for medication allergies
   - UNII for chemical substance allergies
   - SNOMED CT for broader allergen categories (foods, environmental)

3. **Distinguish Allergies from Intolerances**
   - True allergies involve immune system response
   - Intolerances are adverse reactions without immune involvement
   - This distinction affects clinical decision-making

4. **Document Severity Accurately**
   - Severity should reflect the worst known reaction
   - 'severe' or 'fatal' reactions require special clinical attention
   - Document even if historical or suspected

5. **Include Reaction Details**
   - Specific reactions help clinicians assess risk
   - Multiple reactions can be documented for a single allergen
   - Use clinical terminology for reactions

### Validation Tips

1. **Section Code Validation**
   - Ensure section code is 48765-2 (LOINC)
   - This is automatically set by the builder

2. **Template ID Validation**
   - Verify the template ID includes extension="2015-08-01"
   - R2.1 requires this specific version

3. **Required Allergy Observation Elements**
   - Each allergy must have a participant (allergen)
   - Value element indicates allergy or intolerance
   - At least one reaction observation or severity observation is recommended

4. **Status Code Consistency**
   - Concern Act statusCode: 'active' for current allergies
   - Concern Act statusCode: 'completed' for resolved allergies
   - Allergy Observation statusCode: always 'completed'

### Gotchas to Avoid

1. **Empty Allergy Sections**
   - NEVER create a document without an Allergies section
   - Always include at least one entry or "No Known Allergies"
   - This is a critical safety requirement

2. **Missing Allergen Codes**
   - While allergen codes are optional in the protocol, they're highly recommended
   - Codes enable automated decision support and allergy checking
   - Use nullFlavor if a suitable code cannot be found

3. **Incorrect Code Systems**
   - Different allergen types require different code systems
   - RxNorm OID: 2.16.840.1.113883.6.88
   - UNII OID: 2.16.840.1.113883.4.9
   - SNOMED CT OID: 2.16.840.1.113883.6.96

4. **Reaction vs. Allergen Confusion**
   - Allergen is what the patient is allergic to (Penicillin)
   - Reaction is what happens (Hives, Anaphylaxis)
   - Don't confuse these in documentation

5. **Severity Coding**
   - Use standard severity codes from ObservationValue value set
   - 'mild', 'moderate', 'severe' map to specific SNOMED codes
   - Severity affects clinical alerting systems

6. **Historical Data Quality**
   - Patient-reported allergies may lack detail
   - Document what's known and use nullFlavor for unknowns
   - Severity and reaction may be "UNK" for old allergies

7. **Status Management**
   - Be cautious marking allergies as 'resolved'
   - Many institutions keep all allergies as 'active' for safety
   - Document resolution date if marked resolved

8. **Cross-Reactivity**
   - Document related allergen cross-sensitivities
   - Example: Penicillin allergy may indicate cephalosporin sensitivity
   - Consider including notes about related substances

9. **Food vs. Drug Allergies**
   - Both types should be documented
   - Food allergies can affect medication excipients
   - Use appropriate code systems for each type

10. **Narrative-Entry Consistency**
    - Ensure narrative table matches structured data
    - The builder handles this automatically
    - Critical for human readers and validators

11. **Duplicate Entries**
    - Avoid documenting the same allergy multiple times
    - If reaction changed, update existing allergy rather than adding new
    - Use persistent IDs to track allergies across documents
