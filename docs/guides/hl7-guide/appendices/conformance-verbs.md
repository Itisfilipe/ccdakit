# Conformance Verbs

Understanding conformance requirements in C-CDA specifications.

## Overview

The C-CDA specification uses precise language to indicate the level of conformance required for each element. These "conformance verbs" define what implementers must, should, or may do when creating or processing C-CDA documents.

## The Four Core Verbs

### SHALL (Required)

**Definition**: An absolute requirement. Must be implemented exactly as specified.

**When to use**: For elements critical to document validity, interoperability, or patient safety.

**Consequences of non-conformance**: Document is invalid and will fail validation.

**Examples**:

```xml
<!-- SHALL: ClinicalDocument must have an id -->
<ClinicalDocument>
    <id root="2.16.840.1.113883.19.5.99999.1" extension="12345"/>
    <!-- This is mandatory - documents without an id are invalid -->
</ClinicalDocument>

<!-- SHALL: Allergy observation must include allergen identification -->
<observation classCode="OBS" moodCode="EVN">
    <templateId root="2.16.840.1.113883.10.20.22.4.7"/>
    <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4"/>
    <!-- The participant element with allergen is required -->
    <participant typeCode="CSM">
        <participantRole classCode="MANU">
            <playingEntity classCode="MMAT">
                <code code="70618" codeSystem="2.16.840.1.113883.6.88"
                      displayName="Penicillin"/>
            </playingEntity>
        </participantRole>
    </participant>
</observation>
```

**In ccdakit**: SHALL requirements are enforced through required parameters and validation.

```python
from ccdakit.models.sections import AllergiesSection
from ccdakit.models.entries import AllergyIntolerance

# The allergen code is a required parameter (SHALL)
allergy = AllergyIntolerance(
    allergen_code="70618",  # Required - will error if omitted
    allergen_code_system="2.16.840.1.113883.6.88",
    allergen_display_name="Penicillin"
)
```

---

### SHOULD (Recommended)

**Definition**: Strong recommendation. Should be implemented unless there's a documented reason not to.

**When to use**: For elements that significantly improve quality or usefulness but aren't strictly required.

**Consequences of non-conformance**: Document is still valid but may have reduced quality or usefulness. Some validators issue warnings.

**Examples**:

```xml
<!-- SHOULD: Problem observation should include onset date -->
<observation classCode="OBS" moodCode="EVN">
    <templateId root="2.16.840.1.113883.10.20.22.4.4"/>
    <code code="55607006" codeSystem="2.16.840.1.113883.6.96"
          displayName="Problem"/>
    <!-- The effectiveTime/low is strongly recommended -->
    <effectiveTime>
        <low value="20230115"/>  <!-- When did problem start? -->
    </effectiveTime>
</observation>

<!-- SHOULD: Medication should include sig (dosing instructions) -->
<substanceAdministration classCode="SBADM" moodCode="EVN">
    <text>
        <reference value="#med1"/>
    </text>
    <!-- Including narrative text is strongly recommended -->
    <doseQuantity value="1"/>
    <rateQuantity value="1" unit="1"/>
</substanceAdministration>
```

**In ccdakit**: SHOULD requirements are optional parameters with validation warnings.

```python
from ccdakit.models.entries import ProblemObservation

# Onset date is optional but recommended
problem = ProblemObservation(
    code="55607006",
    code_system="2.16.840.1.113883.6.96",
    display_name="Problem",
    onset_date="20230115"  # Optional but SHOULD include
)
```

---

### MAY (Optional)

**Definition**: Truly optional. Implementer's choice based on use case.

**When to use**: For elements that add value in some contexts but aren't needed in all situations.

**Consequences of non-conformance**: None. Completely at implementer's discretion.

**Examples**:

```xml
<!-- MAY: Social history observation may include interpretation -->
<observation classCode="OBS" moodCode="EVN">
    <code code="72166-2" codeSystem="2.16.840.1.113883.6.1"
          displayName="Tobacco smoking status"/>
    <value xsi:type="CD" code="8517006"
           codeSystem="2.16.840.1.113883.6.96"
           displayName="Former smoker"/>
    <!-- This interpretation code is optional -->
    <interpretationCode code="N" codeSystem="2.16.840.1.113883.5.83"
                       displayName="Normal"/>
</observation>

<!-- MAY: Document may include version number -->
<ClinicalDocument>
    <id root="2.16.840.1.113883.19.5" extension="12345"/>
    <versionNumber value="1"/>  <!-- Optional -->
</ClinicalDocument>
```

**In ccdakit**: MAY elements are optional parameters with no warnings.

```python
from ccdakit.models.entries import SocialHistoryObservation

# Interpretation is completely optional
observation = SocialHistoryObservation(
    code="72166-2",
    code_system="2.16.840.1.113883.6.1",
    value="8517006",
    interpretation_code="N"  # Optional, MAY include
)
```

---

### SHALL NOT (Prohibited)

**Definition**: Absolute prohibition. Must not be present or implemented.

**When to use**: For elements that would cause errors, safety issues, or contradict the specification.

**Consequences of non-conformance**: Document is invalid. May cause processing errors or safety issues.

**Examples**:

```xml
<!-- SHALL NOT: nullFlavor SHALL NOT be used on required elements -->
<ClinicalDocument>
    <!-- This is INVALID - id is required (SHALL) -->
    <id nullFlavor="UNK"/>  <!-- SHALL NOT do this -->
</ClinicalDocument>

<!-- SHALL NOT: Multiple values in single-value elements -->
<observation>
    <value xsi:type="CD" code="normal"/>
    <!-- SHALL NOT have multiple value elements when cardinality is 1..1 -->
    <value xsi:type="CD" code="abnormal"/>  <!-- INVALID -->
</observation>

<!-- SHALL NOT: Use deprecated templates -->
<observation>
    <!-- SHALL NOT use obsolete template IDs -->
    <templateId root="2.16.840.1.113883.10.20.22.4.7" extension="2012-06-01"/>
    <!-- Must use current version (2014-06-09 or later) -->
</observation>
```

**In ccdakit**: SHALL NOT constraints are prevented by design or raise errors.

```python
from ccdakit.models.document import ClinicalDocument

# This would raise an error - document_id is required
try:
    doc = ClinicalDocument(
        document_id=None  # SHALL NOT omit - will error
    )
except ValueError as e:
    print("Error: document_id is required")
```

## Conformance Hierarchy

```
SHALL
  |
  v
SHOULD
  |
  v
MAY
  |
  v
(Not specified)
  |
  v
SHALL NOT
```

**Strictness decreases as you go down, except for SHALL NOT which is absolute.**

## Context Matters

Conformance verbs can have different requirements based on context:

### Example: effectiveTime

```xml
<!-- Context 1: In ClinicalDocument -->
<ClinicalDocument>
    <!-- SHALL have effectiveTime -->
    <effectiveTime value="20231018120000-0500"/>
</ClinicalDocument>

<!-- Context 2: In Problem Observation -->
<observation>
    <!-- SHOULD have effectiveTime/low (onset) -->
    <!-- MAY have effectiveTime/high (resolution) -->
    <effectiveTime>
        <low value="20230115"/>
        <high value="20230301"/>  <!-- Optional -->
    </effectiveTime>
</observation>
```

## How ccdakit Handles Conformance

### 1. Required Fields (SHALL)

```python
from ccdakit.models.document import ClinicalDocument

# Required parameters must be provided
doc = ClinicalDocument(
    document_id="12345",           # Required
    document_id_root="2.16...",    # Required
    code="34133-9",                # Required
    title="Consultation Note",     # Required
    effective_time="20231018"      # Required
)
```

### 2. Optional Fields (SHOULD/MAY)

```python
# Optional parameters can be omitted
doc = ClinicalDocument(
    document_id="12345",
    document_id_root="2.16...",
    code="34133-9",
    title="Consultation Note",
    effective_time="20231018",
    version_number="1"  # Optional (MAY)
)
```

### 3. Validation Levels

```python
from ccdakit.validation import validate_document

# Strict validation checks ALL conformance (SHALL + SHOULD)
result = validate_document(doc, level="strict")

# Standard validation checks required conformance (SHALL only)
result = validate_document(doc, level="standard")

# Lenient validation checks critical conformance only
result = validate_document(doc, level="lenient")
```

### 4. Warnings vs Errors

```python
# SHALL violations = Errors (document invalid)
# SHOULD violations = Warnings (document valid but not optimal)
# MAY omissions = No feedback (completely fine)

if result.errors:
    print("Document is INVALID - fix SHALL violations")
if result.warnings:
    print("Document is valid but has SHOULD violations")
```

## Conformance in Templates

Templates can add additional conformance requirements:

```xml
<!-- Base CDA: participant is MAY -->
<!-- C-CDA Allergy Template: participant SHALL be present -->
<observation classCode="OBS" moodCode="EVN">
    <templateId root="2.16.840.1.113883.10.20.22.4.7"/>
    <!-- Because of the template, this participant is now required -->
    <participant typeCode="CSM">
        <!-- ... allergen details ... -->
    </participant>
</observation>
```

**Key Point**: Templates can make optional elements required, but cannot relax requirements.

## Best Practices

1. **Always implement SHALL** - No exceptions. These are non-negotiable.

2. **Implement SHOULD unless there's a reason not to** - Document why if you don't.

3. **Evaluate MAY based on use case** - Include if it adds value to your users.

4. **Never violate SHALL NOT** - These exist to prevent errors.

5. **Understand context** - Same element may have different conformance in different places.

6. **Use validation tools** - Automated checking catches conformance issues.

7. **Document decisions** - Keep track of why you included or excluded SHOULD/MAY elements.

## Common Conformance Patterns

### Pattern 1: Required Element with Optional Details

```xml
<!-- The observation SHALL exist -->
<observation>
    <!-- Code SHALL be present -->
    <code code="1234"/>

    <!-- Value SHALL be present -->
    <value xsi:type="CD" code="5678"/>

    <!-- InterpretationCode MAY be present -->
    <interpretationCode code="N"/>
</observation>
```

### Pattern 2: Either/Or Requirements

```xml
<!-- SHALL have either effectiveTime OR nullFlavor, but not both -->
<observation>
    <effectiveTime value="20231018"/>
    <!-- OR -->
    <effectiveTime nullFlavor="UNK"/>
</observation>
```

### Pattern 3: Conditional Requirements

```xml
<!-- IF status is 'completed', THEN effectiveTime/high SHALL be present -->
<observation>
    <statusCode code="completed"/>
    <effectiveTime>
        <low value="20230115"/>
        <high value="20230301"/>  <!-- Required because status=completed -->
    </effectiveTime>
</observation>
```

## Quick Reference Table

| Verb | Meaning | Implementation | Validation Failure |
|------|---------|----------------|-------------------|
| SHALL | Must implement | Required parameter | Error - Invalid |
| SHOULD | Strongly recommended | Optional parameter | Warning - Valid |
| MAY | Optional | Optional parameter | No feedback |
| SHALL NOT | Prohibited | Prevented/blocked | Error - Invalid |

## Reading the Specification

When reading C-CDA specifications:

1. Look for conformance verbs (SHALL, SHOULD, MAY, SHALL NOT)
2. Check cardinality (0..1, 1..1, 0..*, 1..*)
3. Note conditional requirements (IF...THEN...)
4. Understand template constraints vs base CDA
5. Check for specific value set bindings

## Summary

- **SHALL** = Required (must do)
- **SHOULD** = Recommended (ought to do)
- **MAY** = Optional (can do)
- **SHALL NOT** = Prohibited (must not do)

Understanding and correctly implementing conformance requirements ensures your C-CDA documents are valid, interoperable, and useful across the healthcare ecosystem.
