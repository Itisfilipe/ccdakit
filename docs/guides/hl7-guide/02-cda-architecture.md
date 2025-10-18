# CDA Architecture: Understanding the Document Structure

## Introduction

Think of a Clinical Document Architecture (CDA) document as a well-organized house. The structure has a clear hierarchy: the house (document) contains rooms (sections) which contain furniture (entries). Everything is built on a solid foundation (the RIM - Reference Information Model). Understanding this architecture is essential to working with C-CDA documents.

This chapter explains the fundamental architecture of CDA documents and the underlying concepts that make them work.

## The Reference Information Model (RIM)

### What is the RIM?

The HL7 Reference Information Model is the foundational data model for HL7 v3 standards, including CDA. Think of it as the "periodic table of healthcare information" - a small set of core building blocks that can be combined to represent any healthcare concept.

### The Six Core RIM Classes

The RIM defines six backbone classes. Three are primary:

#### 1. Act

**What it represents**: Any intentional action or event in healthcare

**Examples**:
- An observation (recording a blood pressure)
- A procedure (performing surgery)
- An encounter (an office visit)
- A medication administration (giving a dose of medicine)
- A diagnosis (identifying a problem)

**Key attributes**:
- `classCode`: Type of act (observation, procedure, encounter)
- `moodCode`: Intent (event that happened, plan to happen, goal)
- `code`: What was done
- `statusCode`: Current state (completed, active, aborted)
- `effectiveTime`: When it occurred or applies

**Think of Acts as**: Verbs - they represent things that happen or are done

#### 2. Entity

**What it represents**: Physical things or people that exist

**Examples**:
- A patient
- A physician
- An organization (hospital, clinic)
- A place (operating room, clinic location)
- A manufactured product (a medication bottle)
- A device (pacemaker, glucose monitor)

**Key attributes**:
- `classCode`: Type of entity (person, organization, place, material)
- `determinerCode`: Specific instance vs. kind of thing
- `code`: What it is
- `name`: The entity's name
- `addr`: Address
- `telecom`: Contact information

**Think of Entities as**: Nouns - they represent people, places, and things

#### 3. Role

**What it represents**: The function or capacity in which an entity participates

**Examples**:
- Patient (a person in the role of receiving care)
- Healthcare provider (a person in the role of providing care)
- Employee (a person in the role of working for an organization)
- Manufactured product (a material in the role of a medication)

**Key concept**: The same entity can have different roles. Dr. Smith is a provider when treating patients, but a patient when receiving care herself.

**Key attributes**:
- `classCode`: Type of role (patient, provider, employee)
- `code`: Specific role classification
- `id`: Identifiers for the role

**Think of Roles as**: Hats that entities wear - the same person wears different hats in different contexts

### The Three Connecting Classes

Three additional classes connect the primary classes:

#### 4. Participation

**What it represents**: The involvement of a Role in an Act

**Examples**:
- A patient is the subject of an observation
- A doctor is the performer of a procedure
- A nurse is the author of a nursing note
- A location is where an encounter took place

**Key attributes**:
- `typeCode`: How the role participates (performer, author, location)
- `time`: When the participation occurred

#### 5. ActRelationship

**What it represents**: How acts relate to each other

**Examples**:
- A medication order causes medication administrations (has component)
- A problem is the reason for a procedure (has reason)
- A procedure is documented by an observation (has documentation)

**Key attributes**:
- `typeCode`: Type of relationship (has component, has reason, has support)

#### 6. RoleLink

**What it represents**: How roles relate to each other

**Examples**:
- A provider is an employee of an organization
- A patient is a contact for another patient (emergency contact)

### How These Fit Together

Here's a simple example using all three primary classes:

**Scenario**: Dr. Jane Smith performs a blood pressure measurement on patient John Doe

**In RIM terms**:
- **Act**: Blood pressure observation (the measurement event)
- **Entity (Person)**: Dr. Jane Smith (a human being)
- **Entity (Person)**: John Doe (another human being)
- **Role**: Healthcare Provider (Dr. Smith in her professional capacity)
- **Role**: Patient (John Doe as recipient of care)
- **Participation**: Provider performs observation
- **Participation**: Patient is subject of observation

**Why this matters**: This model allows precise representation of who did what, to whom, when, and why.

## CDA Document Structure Overview

A CDA document has two main parts, much like a web page has HEAD and BODY tags:

### High-Level Structure

```
ClinicalDocument (the document itself)
├── Header (metadata about the document)
│   ├── Document type
│   ├── Patient information
│   ├── Author(s)
│   ├── Custodian (who maintains the record)
│   └── Other participants
└── Body (the clinical content)
    ├── Structured Body (most C-CDA documents)
    │   └── Sections (organized clinical content)
    │       └── Entries (structured clinical statements)
    └── OR Nonstructured Body (narrative text only)
```

### The Two Approaches to the Body

#### Structured Body

Contains organized sections with both narrative text and structured, coded entries.

**Advantages**:
- Machine-processable
- Enables decision support
- Supports data integration
- Required for most C-CDA documents

**Use when**: Exchanging data that receiving systems need to process

#### Nonstructured Body

Contains only narrative text (like a scanned document converted to text).

**Advantages**:
- Simple to create
- Preserves original formatting
- No complex coding required

**Use when**: Converting legacy documents or when structured data isn't available

**Most C-CDA documents use Structured Body**, so we'll focus on that.

## The CDA Header

### Purpose

The header contains metadata - information about the document itself rather than the clinical content. Think of it like the front page of a report that tells you what the report is, who wrote it, when, and who it's about.

### Key Header Components

#### 1. Document Identifiers and Type

```xml
<ClinicalDocument>
  <!-- Realm Code: US realm -->
  <realmCode code="US"/>

  <!-- Type of document -->
  <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>

  <!-- Template IDs: What standards this follows -->
  <templateId root="2.16.840.1.113883.10.20.22.1.1" extension="2015-08-01"/>

  <!-- Unique document ID -->
  <id root="2.16.840.1.113883.19.5.99999.1" extension="20240315001"/>

  <!-- Document code: Continuity of Care Document -->
  <code code="34133-9" codeSystem="2.16.840.1.113883.6.1"
        displayName="Summarization of Episode Note"/>

  <!-- Document title -->
  <title>Continuity of Care Document</title>

  <!-- Creation time -->
  <effectiveTime value="20240315120000-0500"/>
</ClinicalDocument>
```

#### 2. Confidentiality

```xml
<!-- Confidentiality level -->
<confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25"
                     displayName="Normal"/>
```

#### 3. Patient (recordTarget)

The subject of the document - who it's about:

```xml
<recordTarget>
  <patientRole>
    <!-- Patient ID -->
    <id root="2.16.840.1.113883.19.5.99999.2" extension="12345"/>

    <!-- Address -->
    <addr use="HP">
      <streetAddressLine>123 Main Street</streetAddressLine>
      <city>Boston</city>
      <state>MA</state>
      <postalCode>02134</postalCode>
    </addr>

    <!-- Phone -->
    <telecom use="HP" value="tel:+1(555)555-1234"/>

    <!-- Patient demographics -->
    <patient>
      <name use="L">
        <given>John</given>
        <family>Doe</family>
      </name>
      <administrativeGenderCode code="M" codeSystem="2.16.840.1.113883.5.1"/>
      <birthTime value="19800115"/>
      <maritalStatusCode code="M" codeSystem="2.16.840.1.113883.5.2"/>
      <raceCode code="2106-3" codeSystem="2.16.840.1.113883.6.238"
                displayName="White"/>
      <ethnicGroupCode code="2186-5" codeSystem="2.16.840.1.113883.6.238"
                       displayName="Not Hispanic or Latino"/>
    </patient>
  </patientRole>
</recordTarget>
```

#### 4. Author(s)

Who created the document:

```xml
<author>
  <time value="20240315120000-0500"/>
  <assignedAuthor>
    <id root="2.16.840.1.113883.19.5.99999.456" extension="789"/>
    <addr>
      <streetAddressLine>456 Medical Plaza</streetAddressLine>
      <city>Boston</city>
      <state>MA</state>
      <postalCode>02134</postalCode>
    </addr>
    <telecom use="WP" value="tel:+1(555)555-9876"/>
    <assignedPerson>
      <name>
        <given>Jane</given>
        <family>Smith</family>
        <suffix>MD</suffix>
      </name>
    </assignedPerson>
  </assignedAuthor>
</author>
```

#### 5. Custodian

The organization responsible for maintaining the document:

```xml
<custodian>
  <assignedCustodian>
    <representedCustodianOrganization>
      <id root="2.16.840.1.113883.19.5.99999.1"/>
      <name>Boston Medical Center</name>
      <telecom use="WP" value="tel:+1(555)555-0000"/>
      <addr>
        <streetAddressLine>789 Hospital Drive</streetAddressLine>
        <city>Boston</city>
        <state>MA</state>
        <postalCode>02134</postalCode>
      </addr>
    </representedCustodianOrganization>
  </assignedCustodian>
</custodian>
```

#### 6. Document Relationships

References to related documents:

```xml
<!-- This document replaces a previous version -->
<relatedDocument typeCode="RPLC">
  <parentDocument>
    <id root="2.16.840.1.113883.19.5.99999.1" extension="20240301001"/>
  </parentDocument>
</relatedDocument>
```

## The CDA Body: Sections

### What is a Section?

A section is a major organizational unit within a document. Think of sections like chapters in a book - each covers a specific topic.

### Standard C-CDA Sections

Common sections include:
- Allergies and Intolerances
- Medications
- Problems
- Procedures
- Results (lab results)
- Vital Signs
- Immunizations
- Social History
- Family History
- Functional Status
- Plan of Treatment

### Section Structure

Every section has three required components:

```xml
<section>
  <!-- 1. Template ID: What template this follows -->
  <templateId root="2.16.840.1.113883.10.20.22.2.6.1" extension="2015-08-01"/>

  <!-- 2. Code: What type of section this is -->
  <code code="48765-2" codeSystem="2.16.840.1.113883.6.1"
        displayName="Allergies and Adverse Reactions"/>

  <!-- 3. Title: Human-readable section name -->
  <title>Allergies and Adverse Reactions</title>

  <!-- 4. Narrative text: Human-readable content (REQUIRED) -->
  <text>
    <table>
      <thead>
        <tr>
          <th>Allergen</th>
          <th>Reaction</th>
          <th>Severity</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Penicillin</td>
          <td>Hives</td>
          <td>Moderate</td>
          <td>Active</td>
        </tr>
      </tbody>
    </table>
  </text>

  <!-- 5. Entries: Structured clinical statements (OPTIONAL but common) -->
  <entry typeCode="DRIV">
    <!-- Entry content goes here -->
  </entry>
</section>
```

### The Narrative Block

The narrative text is **REQUIRED** and must be human-readable. It uses a restricted set of HTML-like tags:

**Allowed tags**:
- `<content>`: Inline content with styling
- `<paragraph>`: Paragraphs
- `<list>`: Lists (ordered or unordered)
- `<table>`: Tables (most common for structured sections)
- `<linkHtml>`: Hyperlinks
- `<br/>`: Line breaks

**Key principle**: The narrative text is the **legally binding** content. Structured entries support the narrative but don't replace it.

### Section Nesting

Sections can contain other sections:

```xml
<section>
  <templateId root="2.16.840.1.113883.10.20.22.2.10" extension="2015-08-01"/>
  <code code="18776-5" displayName="Plan of Treatment"/>
  <title>Plan of Treatment</title>
  <text>...</text>

  <!-- Nested section -->
  <section>
    <templateId root="2.16.840.1.113883.10.20.22.2.60" extension="2015-08-01"/>
    <code code="61146-7" displayName="Goals"/>
    <title>Goals</title>
    <text>...</text>
    <entry>...</entry>
  </section>
</section>
```

## The CDA Body: Entries

### What is an Entry?

An entry is a structured clinical statement within a section. While the narrative text is for humans, entries are for machines - they contain coded, structured data that can be processed, queried, and reasoned about.

**Think of it this way**:
- **Narrative**: "Patient has a penicillin allergy causing hives"
- **Entry**: Structured representation with codes for penicillin (RxNorm), hives (SNOMED CT), allergy type, severity, status, dates

### Entry Structure

Entries use RIM classes (remember those?):

```xml
<entry typeCode="DRIV">
  <act classCode="ACT" moodCode="EVN">
    <!-- This is an Act Concern Entry wrapper -->
    <templateId root="2.16.840.1.113883.10.20.22.4.30" extension="2015-08-01"/>
    <id root="36e3e930-7b14-11db-9fe1-0800200c9a66"/>
    <code code="CONC" codeSystem="2.16.840.1.113883.5.6"/>
    <statusCode code="active"/>
    <effectiveTime>
      <low value="20150101"/>
    </effectiveTime>

    <!-- The actual allergy observation -->
    <entryRelationship typeCode="SUBJ">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.22.4.7" extension="2014-06-09"/>
        <id root="4adc1020-7b14-11db-9fe1-0800200c9a66"/>
        <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4"/>
        <statusCode code="completed"/>

        <!-- What they're allergic to -->
        <participant typeCode="CSM">
          <participantRole classCode="MANU">
            <playingEntity classCode="MMAT">
              <code code="7980" codeSystem="2.16.840.1.113883.6.88"
                    displayName="Penicillin"/>
            </playingEntity>
          </participantRole>
        </participant>

        <!-- The reaction -->
        <entryRelationship typeCode="MFST">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.22.4.9" extension="2014-06-09"/>
            <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4"/>
            <value xsi:type="CD" code="247472004"
                   codeSystem="2.16.840.1.113883.6.96"
                   displayName="Hives"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>
  </act>
</entry>
```

### Key Entry Attributes

#### classCode (Act Class)

Defines what type of act this is:

- `ACT`: General act (often used for wrappers)
- `OBS`: Observation
- `PROC`: Procedure
- `SBADM`: Substance administration (medication)
- `ENC`: Encounter
- `SUPPLY`: Supply event

#### moodCode (Mood)

Defines the intent or state:

- `EVN`: Event (something that happened)
- `INT`: Intent (something planned)
- `PRMS`: Promise (something committed)
- `RQO`: Request (something ordered)
- `GOL`: Goal (something to achieve)

**Example**: A completed blood pressure reading is `moodCode="EVN"`. A planned procedure is `moodCode="INT"`.

#### typeCode (Relationship Type)

For entry relationships:

- `COMP`: Has component
- `SUBJ`: Has subject
- `MFST`: Is manifestation of
- `RSON`: Has reason
- `CAUS`: Has cause

## RIM Classes in Action

### The Clinical Statement Pattern

CDA entries follow a consistent pattern based on RIM:

1. **Wrapper Act**: Often an Act Concern that tracks status over time
2. **Core Clinical Statement**: The main observation, procedure, or substance administration
3. **Related Information**: Connected via entry relationships

**Example - Problem Entry**:

```
Act (Concern)
  └─ entryRelationship (SUBJ) ─> Observation (Problem)
                                    ├─ code: Problem type
                                    ├─ value: Specific problem
                                    ├─ effectiveTime: When it exists
                                    └─ entryRelationship (REFR) ─> Observation (Status)
```

### Acts: Representing Events and Observations

**Observation Example** - Blood Pressure:

```xml
<observation classCode="OBS" moodCode="EVN">
  <templateId root="2.16.840.1.113883.10.20.22.4.27" extension="2014-06-09"/>
  <id root="c6f88320-67ad-11db-bd13-0800200c9a66"/>
  <code code="85354-9" codeSystem="2.16.840.1.113883.6.1"
        displayName="Blood Pressure"/>
  <statusCode code="completed"/>
  <effectiveTime value="20240315100000-0500"/>

  <!-- Systolic component -->
  <entryRelationship typeCode="COMP">
    <observation classCode="OBS" moodCode="EVN">
      <code code="8480-6" codeSystem="2.16.840.1.113883.6.1"
            displayName="Systolic"/>
      <value xsi:type="PQ" value="120" unit="mm[Hg]"/>
    </observation>
  </entryRelationship>

  <!-- Diastolic component -->
  <entryRelationship typeCode="COMP">
    <observation classCode="OBS" moodCode="EVN">
      <code code="8462-4" codeSystem="2.16.840.1.113883.6.1"
            displayName="Diastolic"/>
      <value xsi:type="PQ" value="80" unit="mm[Hg]"/>
    </observation>
  </entryRelationship>
</observation>
```

**Procedure Example** - Appendectomy:

```xml
<procedure classCode="PROC" moodCode="EVN">
  <templateId root="2.16.840.1.113883.10.20.22.4.14" extension="2014-06-09"/>
  <id root="d68b7e32-7810-11db-9fe1-0800200c9a66"/>
  <code code="44950" codeSystem="2.16.840.1.113883.6.12"
        displayName="Appendectomy"/>
  <statusCode code="completed"/>
  <effectiveTime value="20240201"/>

  <!-- Who performed it -->
  <performer>
    <assignedEntity>
      <id root="2.16.840.1.113883.19.5.99999.456" extension="123"/>
      <assignedPerson>
        <name>
          <given>Robert</given>
          <family>Johnson</family>
          <suffix>MD</suffix>
        </name>
      </assignedPerson>
    </assignedEntity>
  </performer>
</procedure>
```

### Entities and Roles: Representing Participants

**Medication as Entity and Role**:

```xml
<substanceAdministration classCode="SBADM" moodCode="EVN">
  <templateId root="2.16.840.1.113883.10.20.22.4.16" extension="2014-06-09"/>
  <id root="cdbd33f0-6cde-11db-9fe1-0800200c9a66"/>
  <statusCode code="active"/>

  <!-- Consumable: The medication -->
  <consumable>
    <manufacturedProduct classCode="MANU">
      <templateId root="2.16.840.1.113883.10.20.22.4.23" extension="2014-06-09"/>
      <manufacturedMaterial>
        <!-- Entity: The actual medication -->
        <code code="197381" codeSystem="2.16.840.1.113883.6.88"
              displayName="Lisinopril 10mg oral tablet"/>
      </manufacturedMaterial>
    </manufacturedProduct>
  </consumable>
</substanceAdministration>
```

### Participations: Connecting Roles to Acts

**Author Participation**:

```xml
<author>
  <time value="20240315120000-0500"/>
  <assignedAuthor>
    <id root="2.16.840.1.113883.19.5.99999.456" extension="789"/>
    <assignedPerson>
      <name>
        <given>Jane</given>
        <family>Smith</family>
        <suffix>MD</suffix>
      </name>
    </assignedPerson>
  </assignedAuthor>
</author>
```

**Performer Participation**:

```xml
<performer typeCode="PRF">
  <time value="20240201"/>
  <assignedEntity>
    <id root="2.16.840.1.113883.19.5.99999.456" extension="123"/>
    <assignedPerson>
      <name>
        <given>Robert</given>
        <family>Johnson</family>
        <suffix>MD</suffix>
      </name>
    </assignedPerson>
  </assignedEntity>
</performer>
```

### Relationships: Connecting Acts

**entryRelationship Examples**:

```xml
<!-- Problem is the reason for medication -->
<entryRelationship typeCode="RSON">
  <observation classCode="OBS" moodCode="EVN">
    <!-- Problem observation -->
  </observation>
</entryRelationship>

<!-- Observation has a component -->
<entryRelationship typeCode="COMP">
  <observation classCode="OBS" moodCode="EVN">
    <!-- Component observation -->
  </observation>
</entryRelationship>

<!-- Observation caused a reaction -->
<entryRelationship typeCode="CAUS">
  <observation classCode="OBS" moodCode="EVN">
    <!-- Causal observation -->
  </observation>
</entryRelationship>
```

## XML Representation

### XML Basics for CDA

CDA documents are XML. Here are the key XML concepts:

#### Elements

```xml
<element>content</element>
```

#### Attributes

```xml
<element attribute="value"/>
```

#### Namespaces

CDA uses XML namespaces to avoid naming conflicts:

```xml
<ClinicalDocument xmlns="urn:hl7-org:v3"
                  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                  xmlns:sdtc="urn:hl7-org:sdtc">
```

- Default namespace (`xmlns`): CDA elements
- `xsi`: XML Schema instance (for data types)
- `sdtc`: Structured Data Capture extensions

#### Data Types

CDA uses HL7 data types:

**CD (Concept Descriptor)** - Coded values:
```xml
<code code="8480-6" codeSystem="2.16.840.1.113883.6.1"
      displayName="Systolic Blood Pressure"/>
```

**PQ (Physical Quantity)** - Measurements with units:
```xml
<value xsi:type="PQ" value="120" unit="mm[Hg]"/>
```

**TS (TimeStamp)** - Dates and times:
```xml
<effectiveTime value="20240315120000-0500"/>
```

**IVL_TS (Interval of Time)** - Time ranges:
```xml
<effectiveTime>
  <low value="20240101"/>
  <high value="20240315"/>
</effectiveTime>
```

**ST (String)** - Text:
```xml
<title>Allergies</title>
```

## Putting It All Together

### Document Flow

1. **Header**: Identifies document type, patient, author, dates
2. **Body**: Contains structured sections
3. **Sections**: Organize content by topic with narrative
4. **Entries**: Provide coded, structured clinical statements
5. **RIM classes**: Act, Entity, Role model the healthcare domain
6. **Relationships**: Connect acts, entities, and roles

### A Complete Mini-Example

```xml
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <!-- HEADER -->
  <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.1" extension="2015-08-01"/>
  <id root="2.16.840.1.113883.19.5.99999.1" extension="20240315001"/>
  <code code="34133-9" codeSystem="2.16.840.1.113883.6.1"/>
  <title>Continuity of Care Document</title>
  <effectiveTime value="20240315120000-0500"/>
  <confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25"/>

  <!-- Patient -->
  <recordTarget>
    <patientRole>
      <id root="2.16.840.1.113883.19.5.99999.2" extension="12345"/>
      <patient>
        <name><given>John</given><family>Doe</family></name>
        <administrativeGenderCode code="M" codeSystem="2.16.840.1.113883.5.1"/>
        <birthTime value="19800115"/>
      </patient>
    </patientRole>
  </recordTarget>

  <!-- Author -->
  <author>
    <time value="20240315120000-0500"/>
    <assignedAuthor>
      <id root="2.16.840.1.113883.19.5.99999.456" extension="789"/>
      <assignedPerson>
        <name><given>Jane</given><family>Smith</family><suffix>MD</suffix></name>
      </assignedPerson>
    </assignedAuthor>
  </author>

  <!-- Custodian -->
  <custodian>
    <assignedCustodian>
      <representedCustodianOrganization>
        <id root="2.16.840.1.113883.19.5.99999.1"/>
        <name>General Hospital</name>
      </representedCustodianOrganization>
    </assignedCustodian>
  </custodian>

  <!-- BODY -->
  <component>
    <structuredBody>
      <!-- Problems Section -->
      <component>
        <section>
          <templateId root="2.16.840.1.113883.10.20.22.2.5.1" extension="2015-08-01"/>
          <code code="11450-4" codeSystem="2.16.840.1.113883.6.1"
                displayName="Problem List"/>
          <title>Problems</title>
          <text>
            <table>
              <thead><tr><th>Problem</th><th>Status</th></tr></thead>
              <tbody><tr><td>Hypertension</td><td>Active</td></tr></tbody>
            </table>
          </text>

          <!-- Problem Entry -->
          <entry>
            <act classCode="ACT" moodCode="EVN">
              <templateId root="2.16.840.1.113883.10.20.22.4.3" extension="2015-08-01"/>
              <id root="ec8a6ff8-ed4b-4f7e-82c3-e98e58b45de7"/>
              <code code="CONC" codeSystem="2.16.840.1.113883.5.6"/>
              <statusCode code="active"/>
              <effectiveTime><low value="20230101"/></effectiveTime>

              <entryRelationship typeCode="SUBJ">
                <observation classCode="OBS" moodCode="EVN">
                  <templateId root="2.16.840.1.113883.10.20.22.4.4" extension="2015-08-01"/>
                  <id root="ab1791b0-5c71-11db-b0de-0800200c9a66"/>
                  <code code="55607006" codeSystem="2.16.840.1.113883.6.96"
                        displayName="Problem"/>
                  <statusCode code="completed"/>
                  <effectiveTime><low value="20230101"/></effectiveTime>
                  <value xsi:type="CD" code="59621000"
                         codeSystem="2.16.840.1.113883.6.96"
                         displayName="Hypertension"/>
                </observation>
              </entryRelationship>
            </act>
          </entry>
        </section>
      </component>
    </structuredBody>
  </component>
</ClinicalDocument>
```

## Key Takeaways

- **RIM provides the foundation**: Act, Entity, and Role are the building blocks
- **CDA documents have two parts**: Header (metadata) and Body (clinical content)
- **Sections organize content**: Each section has narrative text and optional entries
- **Narrative is required**: Human-readable text is legally binding
- **Entries provide structure**: Machine-processable coded clinical statements
- **XML is the format**: Understanding XML structure is essential
- **Relationships matter**: entryRelationships, participations, and act relationships connect information
- **Template IDs everywhere**: They identify which templates elements conform to

## What's Next

Now that you understand the architecture, the next chapter will dive into templates and conformance - how C-CDA uses templates to define specific constraints and requirements for different types of documents, sections, and entries.

Understanding the architecture is like understanding the grammar of a language. Templates are like the specific vocabulary and rules for different contexts (business letter vs. poem vs. text message). Both are essential for effective communication.
