# Code Systems and Terminologies: The Vocabulary of Healthcare

## Introduction

Imagine two doctors from different hospitals discussing a patient. One says "the patient has HTN" and the other says "the patient has high blood pressure." They're talking about the same condition, but using different terms. Now imagine trying to do this electronically with thousands of conditions, medications, and procedures. That's where standardized terminologies come in.

This chapter explains the code systems and terminologies used in C-CDA, why they matter, and how to use them correctly.

## Why Standardized Codes Matter

### The Problem: Free Text

Before standardized coding:

```xml
<value xsi:type="ST">high blood pressure</value>
<value xsi:type="ST">hypertension</value>
<value xsi:type="ST">HTN</value>
<value xsi:type="ST">elevated BP</value>
```

**All mean the same thing**, but a computer can't tell:
- Can't aggregate data (how many patients have hypertension?)
- Can't trigger alerts (patient with HTN prescribed contraindicated med)
- Can't do research (outcomes for hypertension treatment)
- Can't exchange meaningfully (receiving system doesn't recognize variant terms)

### The Solution: Coded Concepts

With standardized codes:

```xml
<value xsi:type="CD" code="59621000"
       codeSystem="2.16.840.1.113883.6.96"
       displayName="Essential hypertension"/>
```

**Now computers can**:
- ✅ Recognize the same concept regardless of display text
- ✅ Aggregate data across systems
- ✅ Trigger clinical decision support
- ✅ Support research and quality measurement
- ✅ Enable semantic interoperability

### The Three Components of a Coded Value

Every coded value in C-CDA has three parts:

1. **code**: The unique identifier (e.g., "59621000")
2. **codeSystem**: The OID identifying which coding system (e.g., "2.16.840.1.113883.6.96" for SNOMED CT)
3. **displayName**: Human-readable text (e.g., "Essential hypertension")

**The code and codeSystem together** uniquely identify the concept. The displayName is for humans, but the code is authoritative.

## Overview of Major Code Systems

C-CDA uses different code systems for different purposes. Think of them as specialized dictionaries:

| Code System | Primary Use | Who Maintains | Example |
|-------------|-------------|---------------|---------|
| SNOMED CT | Problems, procedures, findings | SNOMED International | 59621000 = Essential hypertension |
| LOINC | Lab tests, vital signs, documents | Regenstrief Institute | 8480-6 = Systolic blood pressure |
| RxNorm | Medications | NLM (National Library of Medicine) | 197381 = Lisinopril 10 MG Oral Tablet |
| CVX | Vaccines | CDC | 207 = COVID-19 mRNA vaccine |
| ICD-10-CM | Diagnoses (billing) | CMS/WHO | I10 = Essential hypertension |
| CPT | Procedures (billing) | AMA (American Medical Association) | 99213 = Office visit |
| NDC | Medication products | FDA | 00093-1098-01 = Lisinopril 10mg tablet |

**Key insight**: Different code systems serve different purposes. C-CDA templates specify which to use where.

## SNOMED CT: Clinical Concepts

### What is SNOMED CT?

**SNOMED CT** (Systematized Nomenclature of Medicine -- Clinical Terms) is the most comprehensive clinical terminology in healthcare. It covers:

- Diseases and findings
- Procedures
- Body structures
- Organisms
- Substances
- Pharmaceutical products
- And much more

**Think of it as**: The clinical encyclopedia - incredibly detailed and precise.

### SNOMED CT Structure

SNOMED CT isn't just a list of codes - it's a sophisticated ontology with:

#### Concepts

Unique clinical ideas, each with a unique identifier:
- `59621000`: Essential hypertension
- `73211009`: Diabetes mellitus
- `22298006`: Myocardial infarction

#### Relationships

Concepts relate to each other:
- "Essential hypertension" **IS A** "Hypertensive disorder"
- "Myocardial infarction" **Finding site** "Heart structure"

#### Hierarchy

Concepts are organized in hierarchies:
```
Disorder
  └─ Cardiovascular disorder
      └─ Vascular disorder
          └─ Hypertensive disorder
              └─ Essential hypertension
```

This enables:
- Finding related concepts
- Querying by category
- Clinical reasoning

### SNOMED CT in C-CDA

**Code System OID**: `2.16.840.1.113883.6.96`

**Common uses in C-CDA**:

#### Problem/Diagnosis Values

```xml
<observation classCode="OBS" moodCode="EVN">
  <code code="55607006" codeSystem="2.16.840.1.113883.6.96"
        displayName="Problem"/>
  <value xsi:type="CD"
         code="44054006"
         codeSystem="2.16.840.1.113883.6.96"
         displayName="Type 2 diabetes mellitus"/>
</observation>
```

#### Procedure Codes

```xml
<procedure classCode="PROC" moodCode="EVN">
  <code code="80146002"
        codeSystem="2.16.840.1.113883.6.96"
        displayName="Appendectomy"/>
</procedure>
```

#### Allergy Substances

```xml
<participant typeCode="CSM">
  <participantRole classCode="MANU">
    <playingEntity classCode="MMAT">
      <code code="387207008"
            codeSystem="2.16.840.1.113883.6.96"
            displayName="Penicillin"/>
    </playingEntity>
  </participantRole>
</participant>
```

#### Reactions

```xml
<observation classCode="OBS" moodCode="EVN">
  <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4"/>
  <value xsi:type="CD"
         code="247472004"
         codeSystem="2.16.840.1.113883.6.96"
         displayName="Urticaria"/>
</observation>
```

### SNOMED CT Challenges

**Size**: Over 350,000 active concepts - overwhelming

**Complexity**: Rich relationships and hierarchies require understanding

**License**: Requires membership in participating countries (free in US through UMLS)

**Post-coordination**: Can combine concepts for precision (less common in C-CDA)

## LOINC: Lab Results and Observations

### What is LOINC?

**LOINC** (Logical Observation Identifiers Names and Codes) is the standard for identifying laboratory and clinical observations. It covers:

- Laboratory tests
- Clinical observations (vital signs, assessments)
- Document types
- Survey instruments

**Think of it as**: The test catalog - standardizes what's being measured.

### LOINC Structure

Each LOINC code has six dimensions:

1. **Component**: What's being measured (glucose, blood pressure)
2. **Property**: What property (mass, volume, time)
3. **Timing**: When measured (fasting, random)
4. **System**: Where measured (blood, urine)
5. **Scale**: Type of result (quantitative, qualitative)
6. **Method**: How measured (if relevant)

**Example**: `2339-0` = Glucose [Mass/volume] in Blood

### LOINC in C-CDA

**Code System OID**: `2.16.840.1.113883.6.1`

**Common uses**:

#### Document Types

```xml
<code code="34133-9"
      codeSystem="2.16.840.1.113883.6.1"
      displayName="Summarization of Episode Note"/>
```

#### Section Codes

```xml
<section>
  <code code="48765-2"
        codeSystem="2.16.840.1.113883.6.1"
        displayName="Allergies and adverse reactions"/>
</section>
```

#### Lab Test Codes

```xml
<observation classCode="OBS" moodCode="EVN">
  <code code="2339-0"
        codeSystem="2.16.840.1.113883.6.1"
        displayName="Glucose [Mass/volume] in Blood"/>
  <value xsi:type="PQ" value="95" unit="mg/dL"/>
</observation>
```

#### Vital Signs

```xml
<!-- Blood Pressure Panel -->
<observation classCode="OBS" moodCode="EVN">
  <code code="85354-9"
        codeSystem="2.16.840.1.113883.6.1"
        displayName="Blood pressure panel"/>

  <!-- Systolic Component -->
  <entryRelationship typeCode="COMP">
    <observation classCode="OBS" moodCode="EVN">
      <code code="8480-6"
            codeSystem="2.16.840.1.113883.6.1"
            displayName="Systolic blood pressure"/>
      <value xsi:type="PQ" value="120" unit="mm[Hg]"/>
    </observation>
  </entryRelationship>

  <!-- Diastolic Component -->
  <entryRelationship typeCode="COMP">
    <observation classCode="OBS" moodCode="EVN">
      <code code="8462-4"
            codeSystem="2.16.840.1.113883.6.1"
            displayName="Diastolic blood pressure"/>
      <value xsi:type="PQ" value="80" unit="mm[Hg]"/>
    </observation>
  </entryRelationship>
</observation>
```

### Key LOINC Codes for C-CDA

#### Common Vital Signs

- `8480-6`: Systolic blood pressure
- `8462-4`: Diastolic blood pressure
- `8867-4`: Heart rate
- `8310-5`: Body temperature
- `9279-1`: Respiratory rate
- `59408-5`: Oxygen saturation
- `29463-7`: Body weight
- `8302-2`: Body height
- `39156-5`: Body mass index

#### Common Document Types

- `34133-9`: Summarization of Episode Note (CCD)
- `18842-5`: Discharge Summary
- `11488-4`: Consultation Note
- `11506-3`: Progress Note

#### Common Section Codes

- `48765-2`: Allergies and adverse reactions
- `10160-0`: Medications
- `11450-4`: Problem list
- `47519-4`: Procedures
- `30954-2`: Results
- `8716-3`: Vital signs

## RxNorm: Medications

### What is RxNorm?

**RxNorm** is the standard for clinical drugs. It provides:

- Normalized names for medications
- Relationships between drug concepts
- Mappings to other drug vocabularies (NDC, etc.)

**Maintained by**: National Library of Medicine (NLM)

**Think of it as**: The medication dictionary - standardizes drug names at various levels.

### RxNorm Concept Hierarchy

RxNorm has multiple levels of specificity:

```
Ingredient: Lisinopril
  └─ Clinical Drug: Lisinopril 10 MG Oral Tablet
      └─ Branded Drug: Prinivil 10 MG Oral Tablet
          └─ Clinical Pack: Lisinopril 10 MG Oral Tablet [30 tablets]
              └─ Branded Pack: Prinivil 10 MG Oral Tablet [30 tablets]
```

**C-CDA typically uses**: Clinical Drug level (generic formulation)

### RxNorm in C-CDA

**Code System OID**: `2.16.840.1.113883.6.88`

**Usage in Medication Activities**:

```xml
<substanceAdministration classCode="SBADM" moodCode="EVN">
  <templateId root="2.16.840.1.113883.10.20.22.4.16" extension="2014-06-09"/>

  <statusCode code="active"/>

  <!-- Consumable: The medication -->
  <consumable>
    <manufacturedProduct classCode="MANU">
      <templateId root="2.16.840.1.113883.10.20.22.4.23" extension="2014-06-09"/>
      <manufacturedMaterial>
        <!-- RxNorm code -->
        <code code="197381"
              codeSystem="2.16.840.1.113883.6.88"
              displayName="Lisinopril 10 MG Oral Tablet">
          <!-- Optional translation to NDC -->
          <translation code="00093-1098-01"
                      codeSystem="2.16.840.1.113883.6.69"
                      displayName="Lisinopril 10mg tablet"/>
        </code>
      </manufacturedMaterial>
    </manufacturedProduct>
  </consumable>
</substanceAdministration>
```

### RxNorm Best Practices

1. **Use Clinical Drug level** when possible (e.g., "Lisinopril 10 MG Oral Tablet")
2. **Include strength and form** (tablet, capsule, solution)
3. **Use generic names** rather than branded (unless brand matters)
4. **Provide translations** to NDC if available

### Common RxNorm Examples

- `197381`: Lisinopril 10 MG Oral Tablet
- `314076`: Metformin 500 MG Oral Tablet
- `308136`: Atorvastatin 20 MG Oral Tablet
- `748796`: Amoxicillin 500 MG Oral Capsule
- `153165`: Aspirin 81 MG Oral Tablet

## CVX: Vaccines

### What is CVX?

**CVX** (Vaccines Administered) is the standard for vaccine types and administration.

**Maintained by**: CDC (Centers for Disease Control and Prevention)

**Code System OID**: `2.16.840.1.113883.12.292`

**Think of it as**: The immunization catalog.

### CVX in C-CDA

```xml
<substanceAdministration classCode="SBADM" moodCode="EVN">
  <templateId root="2.16.840.1.113883.10.20.22.4.52" extension="2015-08-01"/>

  <statusCode code="completed"/>
  <effectiveTime value="20240115"/>

  <!-- Vaccine product -->
  <consumable>
    <manufacturedProduct classCode="MANU">
      <templateId root="2.16.840.1.113883.10.20.22.4.54" extension="2014-06-09"/>
      <manufacturedMaterial>
        <!-- CVX code -->
        <code code="208"
              codeSystem="2.16.840.1.113883.12.292"
              displayName="COVID-19, mRNA, bivalent, original/Omicron BA.4/BA.5"/>
      </manufacturedMaterial>
    </manufacturedProduct>
  </consumable>
</substanceAdministration>
```

### Common CVX Codes

- `208`: COVID-19, mRNA, bivalent
- `141`: Influenza, seasonal
- `115`: Tdap (tetanus, diphtheria, pertussis)
- `03`: MMR (measles, mumps, rubella)
- `21`: Varicella (chickenpox)
- `113`: Td (tetanus, diphtheria)
- `08`: Hepatitis B
- `106`: DTaP (pediatric)

### CVX and MVX

CVX is often paired with **MVX** (Manufacturers of Vaccines):

**MVX Code System OID**: `2.16.840.1.113883.12.227`

```xml
<manufacturedMaterial>
  <code code="208"
        codeSystem="2.16.840.1.113883.12.292"
        displayName="COVID-19, mRNA, bivalent">
    <!-- Manufacturer -->
    <translation code="PFR"
                codeSystem="2.16.840.1.113883.12.227"
                displayName="Pfizer"/>
  </code>
</manufacturedMaterial>
```

## ICD-10-CM: Diagnosis Codes

### What is ICD-10-CM?

**ICD-10-CM** (International Classification of Diseases, 10th Revision, Clinical Modification) is the standard for diagnosis coding, primarily for billing and administrative purposes.

**Maintained by**: CMS (Centers for Medicare & Medicaid Services) and WHO

**Code System OID**: `2.16.840.1.113883.6.90`

**Think of it as**: The billing diagnosis system.

### ICD-10-CM vs SNOMED CT

| Aspect | SNOMED CT | ICD-10-CM |
|--------|-----------|-----------|
| Purpose | Clinical documentation | Billing/reimbursement |
| Detail | Highly detailed | Less granular |
| Concepts | 350,000+ | 70,000+ |
| Use in C-CDA | Preferred for clinical | Used for billing info |
| Example | 59621000 = Essential hypertension | I10 = Essential hypertension |

### ICD-10-CM in C-CDA

**Common use**: Encounter diagnosis, billing information

```xml
<observation classCode="OBS" moodCode="EVN">
  <templateId root="2.16.840.1.113883.10.20.22.4.4" extension="2015-08-01"/>
  <code code="29308-4" codeSystem="2.16.840.1.113883.6.1"
        displayName="Diagnosis"/>

  <!-- SNOMED CT for clinical -->
  <value xsi:type="CD"
         code="59621000"
         codeSystem="2.16.840.1.113883.6.96"
         displayName="Essential hypertension">

    <!-- ICD-10-CM translation for billing -->
    <translation code="I10"
                codeSystem="2.16.840.1.113883.6.90"
                displayName="Essential (primary) hypertension"/>
  </value>
</observation>
```

### ICD-10-CM Structure

ICD-10-CM codes are alphanumeric:

- **Format**: Letter + 2-3 digits + optional decimal + 1-4 more digits
- **Example**: `E11.9` = Type 2 diabetes mellitus without complications

**Categories**:
- `A00-B99`: Infectious diseases
- `C00-D49`: Neoplasms
- `E00-E89`: Endocrine, nutritional, metabolic
- `I00-I99`: Circulatory system
- `J00-J99`: Respiratory system
- And 16 more chapters...

### Common ICD-10-CM Codes

- `I10`: Essential hypertension
- `E11.9`: Type 2 diabetes without complications
- `E78.5`: Hyperlipidemia
- `J44.9`: COPD
- `I25.10`: Coronary artery disease
- `F41.9`: Anxiety disorder

## CPT: Procedure Codes

### What is CPT?

**CPT** (Current Procedural Terminology) is the standard for procedure codes, used primarily for billing.

**Maintained by**: AMA (American Medical Association)

**Code System OID**: `2.16.840.1.113883.6.12`

**Think of it as**: The procedure billing system.

### CPT Categories

- **Category I**: Common procedures (99201-99607)
- **Category II**: Performance measurement (0001F-9007F)
- **Category III**: Emerging technology (0001T-0999T)

### CPT in C-CDA

**Common use**: Billing for office visits and procedures

```xml
<procedure classCode="PROC" moodCode="EVN">
  <templateId root="2.16.840.1.113883.10.20.22.4.14" extension="2014-06-09"/>

  <!-- CPT code for procedure -->
  <code code="44950"
        codeSystem="2.16.840.1.113883.6.12"
        displayName="Appendectomy">

    <!-- SNOMED translation for clinical -->
    <translation code="80146002"
                codeSystem="2.16.840.1.113883.6.96"
                displayName="Appendectomy"/>
  </code>

  <statusCode code="completed"/>
  <effectiveTime value="20240201"/>
</procedure>
```

### Common CPT Codes

**Office Visits**:
- `99213`: Office visit, established patient, moderate complexity
- `99214`: Office visit, established patient, detailed
- `99215`: Office visit, established patient, comprehensive
- `99203`: Office visit, new patient, moderate complexity

**Common Procedures**:
- `44950`: Appendectomy
- `45378`: Colonoscopy
- `93000`: Electrocardiogram
- `80053`: Comprehensive metabolic panel

## Value Sets vs Code Systems

### Code Systems

A **code system** is a collection of all possible codes:

- SNOMED CT: All clinical concepts
- LOINC: All observations and tests
- RxNorm: All medications

**Think of it as**: The entire dictionary.

### Value Sets

A **value set** is a specific subset of codes from one or more code systems for a particular use:

**Example**: "Problem Type Value Set"
- Contains codes from SNOMED CT
- Only codes relevant to problems
- Excludes procedures, findings, etc.

**Think of it as**: A vocabulary list for a specific topic.

### Value Set Bindings

C-CDA templates specify value set bindings:

```
observation/value
  Binding: Problem Type (STATIC 2014-09-02)
  Value Set: 2.16.840.1.113883.3.88.12.3221.7.4
  Code System: SNOMED CT
```

**Binding types**:

#### STATIC

Value set is fixed to a specific version:
- Doesn't change
- Predictable validation
- May become outdated

#### DYNAMIC

Value set can be updated:
- Current at time of use
- May include new codes
- Less predictable

### Using Value Sets

**Example**: Allergy type value set

```xml
<observation classCode="OBS" moodCode="EVN">
  <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4"/>

  <!-- Value must be from Allergy Type value set -->
  <value xsi:type="CD"
         code="419511003"
         codeSystem="2.16.840.1.113883.6.96"
         displayName="Propensity to adverse reactions to drug"/>
</observation>
```

**Valid codes in this value set** (examples):
- `419511003`: Propensity to adverse reactions to drug
- `418471000`: Propensity to adverse reactions to food
- `419199007`: Allergy to substance
- `232347008`: Dander allergy

### Where to Find Value Sets

**VSAC** (Value Set Authority Center):
- https://vsac.nlm.nih.gov
- Requires UMLS account (free)
- Search by value set OID or name
- Download expansion (list of codes)

## Null Flavors: When Information is Missing

### What are Null Flavors?

Sometimes information is unknown, not applicable, or can't be provided. **Null flavors** are standardized codes for expressing this.

**Code System**: HL7 NullFlavor (2.16.840.1.113883.5.1008)

**Think of it as**: Standard ways to say "I don't know" or "not applicable."

### Common Null Flavors

| Code | Display Name | Use When |
|------|--------------|----------|
| `NI` | No information | Not available, no reason why |
| `UNK` | Unknown | Information exists but is unknown |
| `ASKU` | Asked but unknown | Patient was asked but doesn't know |
| `NAV` | Temporarily unavailable | Will be available later |
| `NASK` | Not asked | Question wasn't asked |
| `MSK` | Masked | Hidden for privacy/security |
| `NA` | Not applicable | Question doesn't apply |
| `OTH` | Other | Known but not in vocabulary |

### Using Null Flavors

#### Example 1: Unknown Allergy

```xml
<observation classCode="OBS" moodCode="EVN">
  <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4"/>

  <!-- Don't know what they're allergic to -->
  <value xsi:type="CD" nullFlavor="UNK"/>
</observation>
```

#### Example 2: No Known Allergies

This is different - you DO know: they have NO allergies:

```xml
<observation classCode="OBS" moodCode="EVN">
  <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4"/>

  <!-- Positive assertion of no allergies -->
  <value xsi:type="CD"
         code="160244002"
         codeSystem="2.16.840.1.113883.6.96"
         displayName="No known allergies"/>
</observation>
```

#### Example 3: Unknown Birth Date

```xml
<patient>
  <name>
    <given>John</given>
    <family>Doe</family>
  </name>
  <birthTime nullFlavor="UNK"/>
</patient>
```

#### Example 4: Not Applicable

```xml
<!-- If documenting a device observation with no performer -->
<performer nullFlavor="NA"/>
```

### Null Flavor Best Practices

1. **Use the most specific null flavor**: `ASKU` is better than `UNK` if you asked
2. **Don't overuse**: If you can provide real data, do
3. **No Known X** is not a null flavor: Use specific codes like "No known allergies"
4. **Document why**: Some systems add text explaining the null flavor

## Translation Codes: Mapping Between Systems

### What are Translations?

Sometimes you want to provide codes from multiple systems for the same concept. Use `<translation>` elements:

```xml
<code code="59621000"
      codeSystem="2.16.840.1.113883.6.96"
      displayName="Essential hypertension">

  <!-- ICD-10-CM translation -->
  <translation code="I10"
              codeSystem="2.16.840.1.113883.6.90"
              displayName="Essential (primary) hypertension"/>
</code>
```

### Why Use Translations?

1. **Multiple purposes**: SNOMED for clinical, ICD-10 for billing
2. **Legacy support**: Old system uses different vocabulary
3. **Additional context**: Provide multiple perspectives
4. **Interoperability**: Receiving system may prefer different code system

### Translation Examples

#### Medication: RxNorm to NDC

```xml
<manufacturedMaterial>
  <code code="197381"
        codeSystem="2.16.840.1.113883.6.88"
        displayName="Lisinopril 10 MG Oral Tablet">

    <!-- NDC for the specific product -->
    <translation code="00093-1098-01"
                codeSystem="2.16.840.1.113883.6.69"
                displayName="Lisinopril 10mg tablet, 100 count bottle"/>
  </code>
</manufacturedMaterial>
```

#### Procedure: SNOMED to CPT

```xml
<procedure classCode="PROC" moodCode="EVN">
  <code code="80146002"
        codeSystem="2.16.840.1.113883.6.96"
        displayName="Appendectomy">

    <!-- CPT for billing -->
    <translation code="44950"
                codeSystem="2.16.840.1.113883.6.12"
                displayName="Appendectomy"/>
  </code>
</procedure>
```

#### Lab Test: Local Code to LOINC

```xml
<observation classCode="OBS" moodCode="EVN">
  <!-- Local lab code -->
  <code code="GLU"
        codeSystem="2.16.840.1.113883.19.5.99999.1"
        displayName="Glucose">

    <!-- Standard LOINC -->
    <translation code="2339-0"
                codeSystem="2.16.840.1.113883.6.1"
                displayName="Glucose [Mass/volume] in Blood"/>
  </code>
</observation>
```

## originalText: Linking Codes to Narrative

### What is originalText?

The `<originalText>` element links coded values to specific text in the narrative section:

```xml
<text>
  <paragraph>
    The patient has <content ID="problem1">type 2 diabetes</content>.
  </paragraph>
</text>

<!-- In the entry -->
<observation classCode="OBS" moodCode="EVN">
  <code code="55607006" codeSystem="2.16.840.1.113883.6.96"
        displayName="Problem"/>

  <value xsi:type="CD"
         code="44054006"
         codeSystem="2.16.840.1.113883.6.96"
         displayName="Type 2 diabetes mellitus">

    <!-- Link to narrative -->
    <originalText>
      <reference value="#problem1"/>
    </originalText>
  </value>
</observation>
```

### Why Use originalText?

1. **Provenance**: Shows what text the code came from
2. **Context**: Preserves original clinical language
3. **Validation**: Ensures entry supports narrative
4. **Human review**: Readers can verify code accuracy

### originalText Best Practices

```xml
<!-- In narrative -->
<text>
  <table>
    <tbody>
      <tr>
        <td><content ID="med1">lisinopril 10mg tablet</content></td>
        <td>Once daily</td>
      </tr>
    </tbody>
  </table>
</text>

<!-- In entry -->
<consumable>
  <manufacturedProduct>
    <manufacturedMaterial>
      <code code="197381"
            codeSystem="2.16.840.1.113883.6.88"
            displayName="Lisinopril 10 MG Oral Tablet">
        <originalText>
          <reference value="#med1"/>
        </originalText>
      </code>
    </manufacturedMaterial>
  </manufacturedProduct>
</consumable>
```

## Common Coding Mistakes

### Mistake 1: Wrong Code System

```xml
<!-- WRONG: Using LOINC code with SNOMED OID -->
<value xsi:type="CD"
       code="2339-0"
       codeSystem="2.16.840.1.113883.6.96"
       displayName="Glucose"/>

<!-- CORRECT: LOINC code with LOINC OID -->
<value xsi:type="CD"
       code="2339-0"
       codeSystem="2.16.840.1.113883.6.1"
       displayName="Glucose [Mass/volume] in Blood"/>
```

### Mistake 2: Missing Code System

```xml
<!-- WRONG: Code without codeSystem -->
<code code="8480-6" displayName="Systolic blood pressure"/>

<!-- CORRECT: Include codeSystem -->
<code code="8480-6"
      codeSystem="2.16.840.1.113883.6.1"
      displayName="Systolic blood pressure"/>
```

### Mistake 3: Invalid Code

```xml
<!-- WRONG: Code doesn't exist in the code system -->
<value xsi:type="CD"
       code="99999999"
       codeSystem="2.16.840.1.113883.6.96"
       displayName="Fake Problem"/>

<!-- CORRECT: Use valid code -->
<value xsi:type="CD"
       code="59621000"
       codeSystem="2.16.840.1.113883.6.96"
       displayName="Essential hypertension"/>
```

### Mistake 4: Code Not in Value Set

```xml
<!-- WRONG: Using procedure code where problem code expected -->
<observation classCode="OBS" moodCode="EVN">
  <code code="55607006" codeSystem="2.16.840.1.113883.6.96"/>
  <value xsi:type="CD"
         code="80146002"
         codeSystem="2.16.840.1.113883.6.96"
         displayName="Appendectomy"/> <!-- This is a procedure, not problem -->
</observation>

<!-- CORRECT: Use problem/disorder code -->
<observation classCode="OBS" moodCode="EVN">
  <code code="55607006" codeSystem="2.16.840.1.113883.6.96"/>
  <value xsi:type="CD"
         code="74400008"
         codeSystem="2.16.840.1.113883.6.96"
         displayName="Appendicitis"/> <!-- This is a problem -->
</observation>
```

### Mistake 5: Using Free Text Instead of Code

```xml
<!-- WRONG: Free text value when code required -->
<value xsi:type="ST">high blood pressure</value>

<!-- CORRECT: Coded value -->
<value xsi:type="CD"
       code="59621000"
       codeSystem="2.16.840.1.113883.6.96"
       displayName="Essential hypertension"/>
```

## Tools and Resources

### Finding Codes

**SNOMED CT Browser**:
- https://browser.ihtsdotools.org
- Search for concepts
- Explore hierarchies

**LOINC Search**:
- https://loinc.org
- Search tool
- Documentation

**RxNorm Browser**:
- https://mor.nlm.nih.gov/RxNav
- Search medications
- Explore relationships

**UMLS Metathesaurus**:
- https://uts.nlm.nih.gov
- Requires account (free)
- Cross-terminology mapping
- Value set authority center (VSAC)

### Validation Tools

**Code System Validators**:
- Check if code exists in system
- Verify code-to-display-name mapping
- Validate value set membership

**C-CDA Validators**:
- NIST MDHT validator
- SITE validator
- Check terminology bindings

### Reference Materials

**Code System OID Registry**:
- HL7 OID Registry
- Know which OID maps to which system

**Value Set Catalog**:
- VSAC (Value Set Authority Center)
- Browse and download value sets

## Key Takeaways

- **Standardized codes enable interoperability** - computers can understand meaning
- **Different code systems serve different purposes** - SNOMED for clinical, LOINC for tests, RxNorm for meds
- **Code + codeSystem + displayName** form a complete coded concept
- **Value sets** constrain codes to specific contexts
- **Null flavors** standardize expressing missing information
- **Translations** allow multiple perspectives on same concept
- **originalText** links codes to narrative
- **Using correct codes in correct contexts** is essential for conformance
- **Resources exist** to find, validate, and map codes
- **Code quality matters** - wrong codes can harm patients

## What's Next

You now understand the vocabulary (terminologies) and grammar (templates) of C-CDA. The next chapter covers the different types of documents you can create - when to use each one and what sections they require.

Think of it this way: You've learned the words and sentence structure. Now you'll learn how to write different types of letters - business letters, thank-you notes, formal reports - each with its own purpose and format.
