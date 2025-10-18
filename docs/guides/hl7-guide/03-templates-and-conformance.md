# Templates and Conformance: The Rules of C-CDA

## Introduction

Imagine if everyone who wrote a resume used completely different formats - some started with hobbies, others with education, some included photos, others didn't. It would be chaos for employers trying to compare candidates. That's why resume templates exist - they provide a consistent structure while allowing customization.

CDA templates work the same way. They define consistent structures for clinical information so that systems can reliably find and interpret data. This chapter explains what templates are, how they work, and how conformance requirements ensure interoperability.

## What Are Templates?

### The Basic Concept

A **template** is a set of constraints and rules applied to the base CDA architecture. It specifies:

- **Which elements are required**: You MUST include these
- **Which elements are optional**: You MAY include these
- **Which elements are prohibited**: You SHALL NOT include these
- **Cardinality**: How many times an element can appear
- **Data types**: What type of data is allowed
- **Code bindings**: Which code systems and value sets to use
- **Nested templates**: Which other templates must be used within this one

**Think of it as**: A recipe. The base CDA is your kitchen with all possible ingredients. A template is a specific recipe that tells you exactly which ingredients to use, how much, in what order, and which ones you must never combine.

### Why Templates Matter

**Without templates**:
- Each vendor implements CDA differently
- Receiving systems don't know where to find information
- Same data represented different ways
- Interoperability fails

**With templates**:
- Consistent structure across implementations
- Predictable location of information
- Standardized representation
- True interoperability

### Template Types

C-CDA defines three main types of templates:

#### 1. Document Templates

Define entire document types.

**Examples**:
- Continuity of Care Document (CCD)
- Discharge Summary
- Progress Note
- Consultation Note

**What they specify**:
- Required header elements
- Required and optional sections
- Document-level constraints

#### 2. Section Templates

Define sections within documents.

**Examples**:
- Allergies and Intolerances Section
- Medications Section
- Problems Section
- Results Section

**What they specify**:
- Section code and title
- Required narrative elements
- Required and optional entries
- Entry template requirements

#### 3. Entry Templates

Define structured clinical statements within sections.

**Examples**:
- Allergy Intolerance Observation
- Medication Activity
- Problem Observation
- Result Observation

**What they specify**:
- Act class and mood
- Required codes and value sets
- Relationships to other entries
- Data element requirements

## Template IDs (OIDs) Explained

### What is an OID?

OID stands for **Object Identifier**. It's a globally unique identifier assigned by registration authorities. Think of it like a telephone number - the format is standard, and no two should be the same.

**Format**: A series of numbers separated by dots
**Example**: `2.16.840.1.113883.10.20.22.4.7`

### Breaking Down an OID

Let's decode `2.16.840.1.113883.10.20.22.4.7`:

```
2                    = ISO (International Organization for Standardization)
2.16                 = ISO member body
2.16.840             = United States
2.16.840.1           = US organizations
2.16.840.1.113883    = HL7
2.16.840.1.113883.10 = HL7 Templates
2.16.840.1.113883.10.20 = CDA
2.16.840.1.113883.10.20.22 = Consolidated CDA
2.16.840.1.113883.10.20.22.4 = Entry Templates
2.16.840.1.113883.10.20.22.4.7 = Allergy Intolerance Observation
```

### How Template IDs Appear in Documents

Template IDs are declared using `<templateId>` elements:

```xml
<observation classCode="OBS" moodCode="EVN">
  <!-- Template ID without version -->
  <templateId root="2.16.840.1.113883.10.20.22.4.7"/>

  <!-- Template ID with version extension -->
  <templateId root="2.16.840.1.113883.10.20.22.4.7" extension="2014-06-09"/>

  <!-- Rest of observation -->
</observation>
```

### Multiple Template IDs

Elements often declare conformance to multiple templates:

```xml
<ClinicalDocument>
  <!-- General CDA template -->
  <templateId root="2.16.840.1.113883.10.20.22.1.1"/>

  <!-- Versioned US Realm Header template -->
  <templateId root="2.16.840.1.113883.10.20.22.1.1" extension="2015-08-01"/>

  <!-- More specific document template -->
  <templateId root="2.16.840.1.113883.10.20.22.1.2" extension="2015-08-01"/>
</ClinicalDocument>
```

**Why multiple?**
- Inheritance hierarchy (more on this later)
- Different versions of the same template
- Conformance to multiple specifications

## Template Versioning

### The Versioning Problem

Templates evolve over time:
- New requirements added
- Bugs fixed
- Clarifications made
- Code bindings updated

How do you know which version a document conforms to?

### Versioning Solutions

#### Pre-R2.1: No Explicit Versioning

Early C-CDA versions didn't have explicit template versioning:

```xml
<templateId root="2.16.840.1.113883.10.20.22.4.7"/>
```

**Problem**: No way to distinguish between different template versions

#### R2.1 and Later: Extension Attribute

R2.1 introduced the `extension` attribute with a date:

```xml
<templateId root="2.16.840.1.113883.10.20.22.4.7" extension="2014-06-09"/>
```

**The date**: Typically the ballot or publication date, not when the document was created

### Version Dating Format

Template version dates use `YYYY-MM-DD` format:

- `2014-06-09`: June 9, 2014
- `2015-08-01`: August 1, 2015

**Important**: This is the template version date, not the document creation date.

### Backward Compatibility

Templates often include both versioned and unversioned IDs:

```xml
<!-- Unversioned - for backward compatibility -->
<templateId root="2.16.840.1.113883.10.20.22.4.7"/>

<!-- Versioned - specific conformance -->
<templateId root="2.16.840.1.113883.10.20.22.4.7" extension="2014-06-09"/>
```

This allows:
- Older systems to recognize the template (unversioned)
- Newer systems to validate exact conformance (versioned)

## Conformance Levels: SHALL, SHOULD, MAY, SHALL NOT

### The Conformance Verbs

C-CDA uses specific keywords from RFC 2119 to indicate requirement levels:

#### SHALL (Required)

**Meaning**: Absolute requirement

**Interpretation**: You MUST do this or you don't conform

**Example**: "The section SHALL contain exactly one code element"

```xml
<!-- CORRECT: Code is present -->
<section>
  <code code="48765-2" codeSystem="2.16.840.1.113883.6.1"/>
  <!-- ... -->
</section>

<!-- INCORRECT: Missing code - not conformant -->
<section>
  <!-- ... -->
</section>
```

#### SHOULD (Recommended)

**Meaning**: Strong recommendation, but not absolute

**Interpretation**: You should do this unless you have a good reason not to. Deviation should be documented.

**Example**: "The observation SHOULD contain a performer"

**Valid cases**:
- Include performer (recommended)
- Omit performer if truly unknown (acceptable with justification)

#### MAY (Optional)

**Meaning**: Truly optional

**Interpretation**: You can include this or not, based on your needs

**Example**: "The observation MAY contain interpretationCode"

Both are valid:
```xml
<!-- With optional element -->
<observation>
  <interpretationCode code="N" codeSystem="2.16.840.1.113883.5.83"/>
</observation>

<!-- Without optional element -->
<observation>
</observation>
```

#### SHALL NOT (Prohibited)

**Meaning**: Absolute prohibition

**Interpretation**: You MUST NOT include this

**Example**: "The observation SHALL NOT contain component elements"

```xml
<!-- INCORRECT: Contains prohibited component -->
<observation>
  <component>...</component>
</observation>

<!-- CORRECT: No component -->
<observation>
</observation>
```

### Conformance in Context

Conformance statements often combine requirements:

**Example**: "The section SHALL contain at least one entry element. Each entry SHALL contain exactly one observation that conforms to the Allergy Intolerance Observation template."

This means:
- At least one `<entry>` (SHALL, 1..*)
- Each entry has one observation (SHALL, 1..1)
- Each observation conforms to specific template (SHALL)

## Cardinality Notation: Understanding 0..1, 1..1, 1..*, 0..*

### What is Cardinality?

Cardinality specifies how many times an element can or must appear. It's written as `minimum..maximum`.

### The Four Common Patterns

#### 0..1 (Zero or One)

**Meaning**: Optional, but if present, only one

**Example**: "The observation SHALL contain zero or one effectiveTime"

```xml
<!-- Valid: effectiveTime present -->
<observation>
  <effectiveTime value="20240315"/>
</observation>

<!-- Valid: effectiveTime absent -->
<observation>
</observation>

<!-- INVALID: Multiple effectiveTimes -->
<observation>
  <effectiveTime value="20240315"/>
  <effectiveTime value="20240316"/>
</observation>
```

#### 1..1 (Exactly One)

**Meaning**: Required, exactly one

**Example**: "The observation SHALL contain exactly one code"

```xml
<!-- Valid: One code -->
<observation>
  <code code="8480-6" codeSystem="2.16.840.1.113883.6.1"/>
</observation>

<!-- INVALID: No code -->
<observation>
</observation>

<!-- INVALID: Multiple codes -->
<observation>
  <code code="8480-6" codeSystem="2.16.840.1.113883.6.1"/>
  <code code="8462-4" codeSystem="2.16.840.1.113883.6.1"/>
</observation>
```

#### 1..* (One or More)

**Meaning**: Required, at least one, no upper limit

**Example**: "The section SHALL contain at least one entry"

```xml
<!-- Valid: One entry -->
<section>
  <entry>...</entry>
</section>

<!-- Valid: Multiple entries -->
<section>
  <entry>...</entry>
  <entry>...</entry>
  <entry>...</entry>
</section>

<!-- INVALID: No entries -->
<section>
</section>
```

#### 0..* (Zero or More)

**Meaning**: Optional, any number including zero

**Example**: "The observation MAY contain zero or more participant elements"

```xml
<!-- Valid: No participants -->
<observation>
</observation>

<!-- Valid: One participant -->
<observation>
  <participant>...</participant>
</observation>

<!-- Valid: Multiple participants -->
<observation>
  <participant>...</participant>
  <participant>...</participant>
</observation>
```

### Cardinality and Conformance Together

Requirements combine cardinality with conformance verbs:

| Cardinality | With SHALL | With SHOULD | With MAY |
|-------------|------------|-------------|----------|
| 0..1 | SHALL contain zero or one | SHOULD contain zero or one | MAY contain (same as 0..1) |
| 1..1 | SHALL contain exactly one | SHOULD contain exactly one | Doesn't make sense |
| 1..* | SHALL contain at least one | SHOULD contain at least one | Doesn't make sense |
| 0..* | SHALL contain zero or more | SHOULD contain zero or more | MAY contain (same as 0..*) |

## Template Inheritance and Constraints

### Template Hierarchies

Templates build on each other through inheritance:

```
US Realm Header (General)
  └─ Continuity of Care Document (More Specific)
      └─ My Organization's CCD Template (Most Specific)
```

**Each level adds constraints** - it never loosens them.

### The Constraint Principle

A child template can:
- ✅ Make optional elements required
- ✅ Reduce cardinality (1..* → 1..3)
- ✅ Restrict code bindings (SNOMED CT → SNOMED CT Problem subset)
- ✅ Add new requirements

A child template cannot:
- ❌ Make required elements optional
- ❌ Increase cardinality (1..1 → 1..*)
- ❌ Loosen code bindings
- ❌ Remove requirements

### Example: Section Template Hierarchy

**Base CDA Section** (Minimal requirements):
```xml
<section>
  <title>...</title>
  <text>...</text>
</section>
```

**C-CDA Allergies Section Template** (Adds constraints):
```xml
<section>
  <templateId root="2.16.840.1.113883.10.20.22.2.6.1" extension="2015-08-01"/>
  <code code="48765-2" codeSystem="2.16.840.1.113883.6.1"/> <!-- REQUIRED -->
  <title>...</title>
  <text>...</text>
  <entry> <!-- At least one REQUIRED -->
    <act><!-- Allergy Concern Act --></act>
  </entry>
</section>
```

**My Hospital's Allergies Section** (Even more constraints):
```xml
<section>
  <templateId root="2.16.840.1.113883.10.20.22.2.6.1" extension="2015-08-01"/>
  <templateId root="1.2.3.4.5.6.7.8.9"/> <!-- My hospital's template -->
  <code code="48765-2" codeSystem="2.16.840.1.113883.6.1"/>
  <title>Allergies and Adverse Reactions</title> <!-- REQUIRED specific text -->
  <text>...</text>
  <entry> <!-- Exactly 1 required -->
    <act><!-- Must use my hospital's Allergy Act template --></act>
  </entry>
</section>
```

### Multiple Inheritance

An element can conform to multiple templates:

```xml
<observation classCode="OBS" moodCode="EVN">
  <!-- Conforms to Problem Observation -->
  <templateId root="2.16.840.1.113883.10.20.22.4.4" extension="2015-08-01"/>

  <!-- ALSO conforms to Social Determinant of Health Problem Observation -->
  <templateId root="2.16.840.1.113883.10.20.22.4.4.2"/>
</observation>
```

**Interpretation**: This observation must satisfy ALL constraints from ALL declared templates.

## Open vs Closed Templates

### Open Templates (Extensible)

**Definition**: You can include additional elements beyond what the template specifies

**Characteristics**:
- Template specifies minimum requirements
- You can add more data
- Common in C-CDA

**Example**:
Template requires: code, statusCode, effectiveTime

You can include:
```xml
<observation>
  <!-- Required by template -->
  <code code="8480-6" codeSystem="2.16.840.1.113883.6.1"/>
  <statusCode code="completed"/>
  <effectiveTime value="20240315"/>

  <!-- Additional elements allowed -->
  <methodCode code="..." codeSystem="..."/>
  <targetSiteCode code="..." codeSystem="..."/>
  <performer>...</performer>
</observation>
```

### Closed Templates (Strict)

**Definition**: You can ONLY include elements explicitly allowed by the template

**Characteristics**:
- Template specifies exact structure
- No additional elements permitted
- Less common, used for strict conformance

**Example**:
Template specifies exactly: code, statusCode, value

```xml
<!-- CORRECT -->
<observation>
  <code code="8480-6" codeSystem="2.16.840.1.113883.6.1"/>
  <statusCode code="completed"/>
  <value xsi:type="PQ" value="120" unit="mm[Hg]"/>
</observation>

<!-- INCORRECT: Additional element not allowed -->
<observation>
  <code code="8480-6" codeSystem="2.16.840.1.113883.6.1"/>
  <statusCode code="completed"/>
  <value xsi:type="PQ" value="120" unit="mm[Hg]"/>
  <methodCode code="..." codeSystem="..."/> <!-- Not allowed! -->
</observation>
```

### How to Tell the Difference

Template specifications usually state:
- **Open**: "This template constrains..." or "SHALL contain..."
- **Closed**: "This template defines the complete structure..." or "SHALL contain ONLY..."

**Most C-CDA templates are open**, allowing implementers to include additional data as needed.

## Contained vs Referenced Templates

### Contained Templates

**Definition**: Template requirements satisfied by elements directly within the parent

**Example**: Entry contains observation that conforms to template

```xml
<entry>
  <observation> <!-- Template contained here -->
    <templateId root="2.16.840.1.113883.10.20.22.4.7" extension="2014-06-09"/>
    <!-- Full observation content -->
  </observation>
</entry>
```

### Referenced Templates

**Definition**: Template points to content elsewhere in the document or external

**Example**: Using an internal reference

```xml
<!-- Define the organization once -->
<author>
  <assignedAuthor>
    <representedOrganization>
      <id root="2.16.840.1.113883.19.5.99999.1"/>
      <name>General Hospital</name>
    </representedOrganization>
  </assignedAuthor>
</author>

<!-- Reference it elsewhere -->
<performer>
  <assignedEntity>
    <representedOrganization>
      <!-- Reference to the organization defined above -->
      <id root="2.16.840.1.113883.19.5.99999.1"/>
    </representedOrganization>
  </assignedEntity>
</performer>
```

## Template Conformance in Practice

### Reading Template Specifications

Template specifications typically include:

#### 1. Context

What the template applies to:
```
Template: Allergy Intolerance Observation
Context: observation (Act Class: OBS, Mood: EVN)
```

#### 2. Conformance Statements

Numbered requirements:
```
1. SHALL contain exactly one [1..1] @classCode="OBS"
2. SHALL contain exactly one [1..1] @moodCode="EVN"
3. SHALL contain at least one [1..*] id
4. SHALL contain exactly one [1..1] code="ASSERTION"
5. SHALL contain exactly one [1..1] statusCode="completed"
6. SHALL contain exactly one [1..1] value with @xsi:type="CD"
7. SHALL contain exactly one [1..1] participant
```

#### 3. Vocabulary Bindings

Required code systems:
```
value: Allergy/Adverse Reaction Type (ValueSet 2.16.840.1.113883.3.88.12.3221.6.2)
  Binding: DYNAMIC
```

#### 4. Nested Templates

Templates that must be used within:
```
8. SHALL contain at least one [1..*] entryRelationship
   a. SHALL contain exactly one [1..1] Reaction Observation (templateId: 2.16.840.1.113883.10.20.22.4.9)
```

### Validating Conformance

To check if an element conforms:

1. **Check structure**: Are required elements present?
2. **Check cardinality**: Right number of each element?
3. **Check codes**: Correct code systems and values?
4. **Check nested templates**: Do contained elements conform to their templates?
5. **Check data types**: Correct data type for values?

### Common Conformance Patterns

#### Pattern 1: Wrapper with Nested Content

```xml
<act classCode="ACT" moodCode="EVN">
  <!-- Wrapper template -->
  <templateId root="2.16.840.1.113883.10.20.22.4.3" extension="2015-08-01"/>

  <!-- Nested template in entryRelationship -->
  <entryRelationship typeCode="SUBJ">
    <observation classCode="OBS" moodCode="EVN">
      <templateId root="2.16.840.1.113883.10.20.22.4.4" extension="2015-08-01"/>
      <!-- Content -->
    </observation>
  </entryRelationship>
</act>
```

#### Pattern 2: Multiple Components

```xml
<observation classCode="OBS" moodCode="EVN">
  <templateId root="2.16.840.1.113883.10.20.22.4.27" extension="2014-06-09"/>
  <code code="85354-9" displayName="Blood Pressure"/>

  <!-- Component 1 -->
  <entryRelationship typeCode="COMP">
    <observation>
      <templateId root="..." />
      <code code="8480-6" displayName="Systolic"/>
      <value xsi:type="PQ" value="120" unit="mm[Hg]"/>
    </observation>
  </entryRelationship>

  <!-- Component 2 -->
  <entryRelationship typeCode="COMP">
    <observation>
      <templateId root="..." />
      <code code="8462-4" displayName="Diastolic"/>
      <value xsi:type="PQ" value="80" unit="mm[Hg]"/>
    </observation>
  </entryRelationship>
</observation>
```

#### Pattern 3: Optional Extensions

```xml
<observation classCode="OBS" moodCode="EVN">
  <templateId root="2.16.840.1.113883.10.20.22.4.7" extension="2014-06-09"/>

  <!-- Required elements -->
  <id root="..."/>
  <code code="ASSERTION"/>
  <statusCode code="completed"/>
  <value xsi:type="CD" code="..."/>

  <!-- Optional severity (MAY contain) -->
  <entryRelationship typeCode="SUBJ" inversionInd="true">
    <observation classCode="OBS" moodCode="EVN">
      <templateId root="2.16.840.1.113883.10.20.22.4.8"/>
      <code code="SEV"/>
      <value xsi:type="CD" code="6736007" displayName="Moderate"/>
    </observation>
  </entryRelationship>
</observation>
```

## Template Design Principles

### Why These Rules?

Template design follows key principles:

#### 1. Interoperability First

**Goal**: Any conformant system can process the document

**How**: Strict requirements for essential elements

#### 2. Backward Compatibility

**Goal**: Older systems can still process newer documents

**How**: Careful evolution, versioning, optional enhancements

#### 3. Clinical Safety

**Goal**: Critical information is never lost or misinterpreted

**How**: Required elements for safety-critical data (allergies, active meds)

#### 4. Flexibility Where Possible

**Goal**: Support diverse clinical workflows

**How**: Open templates, optional elements for non-critical data

#### 5. Coded Data for Processing

**Goal**: Enable decision support and analytics

**How**: Required code bindings for key concepts

## Common Template Mistakes

### Mistake 1: Wrong Cardinality

```xml
<!-- WRONG: Multiple statusCodes when only 1..1 allowed -->
<observation>
  <statusCode code="completed"/>
  <statusCode code="final"/>
</observation>

<!-- CORRECT: Single statusCode -->
<observation>
  <statusCode code="completed"/>
</observation>
```

### Mistake 2: Missing Required Elements

```xml
<!-- WRONG: Missing required code element -->
<section>
  <templateId root="2.16.840.1.113883.10.20.22.2.6.1"/>
  <title>Allergies</title>
  <text>...</text>
</section>

<!-- CORRECT: Includes required code -->
<section>
  <templateId root="2.16.840.1.113883.10.20.22.2.6.1"/>
  <code code="48765-2" codeSystem="2.16.840.1.113883.6.1"/>
  <title>Allergies</title>
  <text>...</text>
</section>
```

### Mistake 3: Wrong Template Version

```xml
<!-- WRONG: Using old template version in R2.1 document -->
<observation>
  <templateId root="2.16.840.1.113883.10.20.22.4.7"/> <!-- No extension -->
</observation>

<!-- CORRECT: Using current template version -->
<observation>
  <templateId root="2.16.840.1.113883.10.20.22.4.7" extension="2014-06-09"/>
</observation>
```

### Mistake 4: Incorrect Nesting

```xml
<!-- WRONG: Direct observation in section -->
<section>
  <observation>...</observation>
</section>

<!-- CORRECT: Observation wrapped in entry -->
<section>
  <entry>
    <observation>...</observation>
  </entry>
</section>
```

### Mistake 5: Missing Nested Templates

```xml
<!-- WRONG: Generic observation instead of required template -->
<entryRelationship typeCode="MFST">
  <observation classCode="OBS" moodCode="EVN">
    <code code="..."/>
    <value xsi:type="CD" code="..."/>
  </observation>
</entryRelationship>

<!-- CORRECT: Includes required Reaction Observation template -->
<entryRelationship typeCode="MFST">
  <observation classCode="OBS" moodCode="EVN">
    <templateId root="2.16.840.1.113883.10.20.22.4.9" extension="2014-06-09"/>
    <code code="..."/>
    <value xsi:type="CD" code="..."/>
  </observation>
</entryRelationship>
```

## Tools for Template Validation

### Available Validators

1. **NIST MDHT Validator**: Official validator from NIST
2. **HL7 Schematron**: Rule-based validation
3. **SITE Validator**: ONC's validator for certification
4. **Commercial EHR Validators**: Built into many EHR systems

### What Validators Check

- ✅ Schema compliance (XML structure)
- ✅ Template presence (required templateIds)
- ✅ Cardinality (correct number of elements)
- ✅ Code system bindings (correct vocabularies)
- ✅ Data types (PQ, CD, TS, etc.)
- ✅ Required elements present
- ✅ Business rules (if coded in Schematron)

### What Validators May Miss

- ❌ Clinical accuracy (is the diagnosis correct?)
- ❌ Semantic meaning (does this make clinical sense?)
- ❌ Completeness (is all relevant data included?)
- ❌ Custom business rules (organization-specific requirements)

**Bottom line**: Validation ensures conformance to the standard, not clinical quality.

## Key Takeaways

- **Templates define constraints** on the base CDA architecture
- **Template IDs (OIDs)** uniquely identify each template version
- **Conformance verbs** (SHALL, SHOULD, MAY, SHALL NOT) indicate requirement levels
- **Cardinality** (0..1, 1..1, 1..*, 0..*) specifies how many times elements can appear
- **Templates inherit** and add constraints, never loosen them
- **Open templates** allow additional elements; closed templates don't
- **Template hierarchies** build from general to specific
- **Multiple templateIds** indicate conformance to multiple specifications
- **Validation tools** check conformance but not clinical quality
- **Understanding templates** is essential for creating and consuming C-CDA documents

## What's Next

Templates tell you **what** structure to use and **how many** times. The next chapter covers **which specific codes** to use - the terminologies and code systems that give C-CDA its semantic meaning and enable true interoperability.

You now understand the grammar and structure. Next, we'll learn the vocabulary.
