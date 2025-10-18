# Glossary

Comprehensive A-Z glossary of C-CDA and HL7 terminology.

## A

### Act
A record of something that is done, is being done, can be done, or is intended to be done. In the HL7 RIM, Act is the root class representing clinical actions, observations, procedures, and other healthcare activities. Examples include medication administrations, observations, encounters, and procedures.

### Act Mood
Indicates the "intent" of an act. Common moods include:
- **EVN (Event)**: Something that has happened or is happening
- **INT (Intent)**: Something planned or intended
- **PRMS (Promise)**: A commitment to do something
- **RQO (Request)**: A request for something to be done

### Act Relationship
Defines how one act is related to another. Common relationships include components (has part), causes, fulfills, or follows.

### Administrative Gender
A person's gender for administrative purposes. Standard HL7 codes include M (Male), F (Female), UN (Undifferentiated). OID: `2.16.840.1.113883.5.1`

### Advance Directive
Legal document that specifies a patient's wishes for medical treatment in case they become unable to communicate their decisions. Documented in the Advance Directives Section.

### Allergy Intolerance
An adverse reaction to a substance, including true allergies and other intolerances. Documented as Allergy Intolerance Observation in C-CDA.

### Author
A person or system that created or significantly modified the content. Every C-CDA document must have at least one author. Can be a person, device, or organization.

## B

### Base CDA
The foundational CDA Release 2.0 standard upon which C-CDA is built. Defines the basic XML structure and semantics but does not specify templates or constraints.

### Binary Data
Non-textual data encoded within an XML document, typically using base64 encoding. Used for embedded images, PDFs, or other file types in C-CDA documents.

### Birth Time
A person's date and time of birth, recorded in HL7 timestamp format (YYYYMMDDHHMMSS).

## C

### C-CDA (Consolidated CDA)
Consolidated Clinical Document Architecture. The US standard for structured clinical documents, combining multiple earlier CDA implementation guides into a single specification. Current version is Release 2.1.

### Cardinality
Specifies how many times an element can appear. Common cardinalities:
- **0..1**: Optional, at most one
- **1..1**: Required, exactly one
- **0..***: Optional, any number
- **1..***: Required, at least one

### Care Plan
A document type that defines goals and treatment plans for a patient's healthcare. Template OID: `2.16.840.1.113883.10.20.22.1.15`

### CCD (Continuity of Care Document)
The most common C-CDA document type, providing a snapshot of a patient's health status and care. Contains all core sections. Template OID: `2.16.840.1.113883.10.20.22.1.2`

### CD (Concept Descriptor)
A data type representing a coded concept with code, codeSystem, displayName, and optionally originalText. Used throughout C-CDA for coded values.

### CDA (Clinical Document Architecture)
HL7's standard for clinical document structure based on XML. Defines six characteristics: persistence, stewardship, potential for authentication, context, wholeness, and human readability.

### Chief Complaint
The patient's primary reason for seeking care, typically in the patient's own words. Recorded in Chief Complaint Section.

### Class Code
Indicates the category or classification of an act, entity, or role. Examples: OBS (Observation), PROC (Procedure), ENC (Encounter).

### Clinical Document
An electronic health record document that meets CDA's six key characteristics. It is complete, persistent, authenticated, and can stand alone.

### Clinical Statement
A structured representation of clinical information using the HL7 RIM pattern. Consists of an Act (what) with Participations (who) and ActRelationships (how connected).

### Code
A symbol or identifier from a terminology system representing a concept. Must reference a code system via OID.

### Code System
A standardized terminology or vocabulary. Examples: SNOMED CT, LOINC, RxNorm, ICD-10-CM. Each has a unique OID.

### Component
A structural relationship indicating one thing contains another. CDA documents use nested `<component>` elements to contain sections and entries.

### Conformance
The degree to which an implementation follows specification requirements. Expressed through SHALL, SHOULD, MAY, and SHALL NOT requirements.

### Conformance Verb
Keywords indicating requirement levels: SHALL (required), SHOULD (recommended), MAY (optional), SHALL NOT (prohibited).

### Consultation Note
A document type capturing a consulting provider's assessment and recommendations. Template OID: `2.16.840.1.113883.10.20.22.1.4`

### Context Conduction
HL7 concept where contextual information (like author, time, subject) flows down through nested structures unless explicitly overridden.

### Custodian
The organization responsible for maintaining and securing the clinical document. Every C-CDA document must have exactly one custodian.

## D

### Data Type
Defines the structure and semantics of a value. C-CDA uses HL7 V3 data types like CD, PQ, TS, ED, etc.

### Discharge Summary
A document type summarizing a patient's hospital stay. Template OID: `2.16.840.1.113883.10.20.22.1.8`

### Display Name
Human-readable text associated with a code, describing what the code means.

### Document ID
Unique identifier for a clinical document instance. Uses the II (Instance Identifier) data type with root (OID) and extension.

### Document Type
The category of clinical document being represented (e.g., CCD, Consultation Note, Progress Note). Identified by template OID.

## E

### ED (Encapsulated Data)
Data type for embedding multimedia content like images, PDFs, or other binary data within XML.

### Effective Time
The clinically relevant time for an act. Can be a point in time (value) or an interval (low/high).

### EHR (Electronic Health Record)
Digital version of a patient's health record. C-CDA is commonly used for exchanging EHR data.

### Encounter
An interaction between a patient and healthcare provider. Documented in the Encounters Section.

### Encompassing Encounter
The clinical context (visit, admission, etc.) within which the document was created. Part of the document header.

### Entity
In HL7 RIM, something with physical existence. Examples: Person, Organization, Place, Material (like a medication or allergen).

### Entry
Structured clinical content within a section. Entries contain clinical statements like observations, procedures, and medications.

### Entry Relationship
Connection between two entry-level acts, showing how they relate (e.g., cause, component, support).

## F

### Family History
Information about health conditions in a patient's family members. Documented in Family History Section.

### FHIR (Fast Healthcare Interoperability Resources)
Newer HL7 standard using RESTful APIs and JSON/XML. C-CDA on FHIR provides mapping between C-CDA and FHIR.

### Functional Status
A patient's ability to perform activities of daily living. Documented in Functional Status Section.

## G

### General Header Constraints
Common requirements that apply across all C-CDA document types, defined in the US Realm Header template.

### Goals Section
Documents a patient's health and treatment goals. Template OID: `2.16.840.1.113883.10.20.22.2.60`

## H

### Health Concerns Section
Documents patient health issues that require ongoing attention. Template OID: `2.16.840.1.113883.10.20.22.2.58`

### History and Physical (H&P)
A document type containing patient history and physical examination findings. Template OID: `2.16.840.1.113883.10.20.22.1.3`

### History of Past Illness
Documents significant past medical conditions. Part of History of Past Illness Section.

### History of Present Illness (HPI)
Narrative description of the development of the patient's current illness. Documented in HPI Section.

### HL7 (Health Level Seven International)
International standards development organization for healthcare information exchange. Develops CDA, FHIR, V2, V3, and other standards.

## I

### ICD-10-CM (International Classification of Diseases)
Standard diagnosis coding system. OID: `2.16.840.1.113883.6.90`

### II (Instance Identifier)
Data type for unique identifiers, consisting of a root (OID or UUID) and optional extension.

### Immunization
A vaccination or immunization administration. Documented in Immunizations Section using Immunization Activity.

### Implementation Guide (IG)
A specification that defines how a base standard should be used in a specific context. C-CDA is an implementation guide of base CDA.

### Informant
A person or entity that provided information for the document, but is not the author. Can be the patient, a family member, or other source.

### Instructions Section
Contains patient instructions for care, medications, or procedures. Template OID: `2.16.840.1.113883.10.20.22.2.45`

### Interoperability
The ability of different systems to exchange and use health information. C-CDA is a key interoperability standard.

### Interventions Section
Documents interventions such as education, counseling, or care coordination. Template OID: `2.16.840.1.113883.10.20.21.2.3`

## L

### Legal Authenticator
Person who legally authenticates the document content. Legally responsible for the document.

### LOINC (Logical Observation Identifiers Names and Codes)
Terminology system for lab tests, vital signs, and document types. OID: `2.16.840.1.113883.6.1`

## M

### Marital Status
A person's legal marital status (married, single, divorced, etc.). Uses HL7 MaritalStatus vocabulary. OID: `2.16.840.1.113883.5.2`

### Meaningful Use
Federal program (now Promoting Interoperability) requiring certified EHR technology including C-CDA exchange capabilities.

### Medical Equipment Section
Documents durable medical equipment, implants, and devices. Template OID: `2.16.840.1.113883.10.20.22.2.23`

### Medication
A pharmaceutical substance. Documented in Medications Section using Medication Activity.

### Mental Status Section
Documents a patient's mental and cognitive status. Template OID: `2.16.840.1.113883.10.20.22.2.56`

### Mood Code
See Act Mood. Indicates whether an act is an event, intent, request, etc.

## N

### Narrative Block
Human-readable text within a section, using a subset of HTML. Required in all C-CDA sections for human readability.

### Narrative Text
The human-readable portion of a section. Must be present even when structured entries exist.

### Negation Indicator
Boolean flag indicating an act did not occur (e.g., "medication not taken", "procedure not performed").

### NIST (National Institute of Standards and Technology)
Provides C-CDA validation tools and test procedures for ONC certification.

### NPI (National Provider Identifier)
Unique identifier for healthcare providers in the US. OID: `2.16.840.1.113883.4.6`

### Null Flavor
Indicates why data is absent or unavailable. Values include UNK (unknown), ASKU (asked but unknown), NA (not applicable), etc. OID: `2.16.840.1.113883.5.1008`

### Nutrition Section
Documents nutritional assessments and plans. Template OID: `2.16.840.1.113883.10.20.22.2.57`

## O

### Observation
An act of monitoring or measuring. The most common clinical statement pattern in C-CDA. Class code is "OBS".

### OID (Object Identifier)
Globally unique identifier used to identify code systems, templates, and organizations. Format: dot-separated numbers (e.g., `2.16.840.1.113883.6.96`).

### ONC (Office of the National Coordinator for Health IT)
Federal agency overseeing health IT adoption and interoperability. Manages EHR certification program requiring C-CDA.

### Operative Note
Document type capturing details of a surgical procedure. Template OID: `2.16.840.1.113883.10.20.22.1.7`

### Organizer
A collection of related clinical statements grouped together (e.g., battery of lab tests, allergy list).

### Original Text
The text from the narrative block that represents coded data, linked via `<reference>` element.

## P

### Participant
An entity playing a role in an act. Types include subject (patient), performer (provider), location, product (medication/device).

### Participation Type
Code indicating how an entity participated in an act (e.g., AUT=author, PRF=performer, LOC=location).

### Patient
The subject of care. Every clinical document has a `<recordTarget>` identifying the patient.

### Payers Section
Documents insurance and payment sources. Template OID: `2.16.840.1.113883.10.20.22.2.18`

### Performer
Entity that carried out an act (e.g., provider who performed procedure, administered medication).

### Physical Exam Section
Documents findings from physical examination. Template OID: `2.16.840.1.113883.10.20.2.10`

### Plan of Treatment Section
Documents planned procedures, encounters, and other future activities. Template OID: `2.16.840.1.113883.10.20.22.2.10`

### PQ (Physical Quantity)
Data type representing a measured quantity with value and unit. Used for vital signs, lab results, medication doses.

### Precondition
A condition that must be true for an act to occur (e.g., "take medication if fever > 101°F").

### Problem
A health condition, diagnosis, or concern. Documented in Problem Section using Problem Observation.

### Problem Section
Core section documenting active and resolved health problems. Template OID: `2.16.840.1.113883.10.20.22.2.5.1`

### Procedure
An activity performed on a patient (surgical procedure, diagnostic procedure, therapy). Documented in Procedures Section.

### Procedures Section
Documents past and current procedures. Template OID: `2.16.840.1.113883.10.20.22.2.7.1`

### Procedure Note
Document type capturing details of a procedure. Template OID: `2.16.840.1.113883.10.20.22.1.6`

### Progress Note
Document type recording patient's progress during care. Template OID: `2.16.840.1.113883.10.20.22.1.9`

## Q

### QRDA (Quality Reporting Document Architecture)
CDA-based standard for quality measure reporting. Uses many C-CDA templates.

## R

### Race
A person's race according to US categories. Uses CDC Race and Ethnicity vocabulary. OID: `2.16.840.1.113883.6.238`

### Record Target
The patient who is the subject of the clinical document. Required in every CDA document.

### Reason for Visit Section
Documents why the patient sought care. Template OID: `2.16.840.1.113883.10.20.22.2.12`

### Referral Note
Document type for referring a patient to another provider. Template OID: `2.16.840.1.113883.10.20.22.1.14`

### Reference
Link from structured data to text in the narrative block, or to external resources.

### Representation Code
Indicates data format (TXT for text, B64 for base64 binary).

### Results Section
Documents laboratory and diagnostic test results. Template OID: `2.16.840.1.113883.10.20.22.2.3.1`

### Review of Systems (ROS)
Systematic review of body systems. Documented in Review of Systems Section. Template OID: `2.16.840.1.113883.10.20.22.2.40`

### RIM (Reference Information Model)
HL7's abstract model of healthcare information. Foundation for CDA's structure. Consists of six core classes: Act, Entity, Role, Participation, ActRelationship, RoleLink.

### Role
In HL7 RIM, a function or position played by an entity. Examples: Patient, Provider, Manufacturer.

### Root
The OID or UUID portion of an Instance Identifier (II data type).

### RxNorm
Terminology for medications and drugs. OID: `2.16.840.1.113883.6.88`

## S

### Schematron
Rule-based validation language for XML. C-CDA uses Schematron to express conformance rules beyond XML Schema.

### Section
Major subdivision of a clinical document containing related information (e.g., Medications Section, Allergies Section). Identified by template OID.

### Service Event
An activity documented by the clinical document (e.g., the hospital stay documented in a discharge summary).

### SHALL
Conformance verb meaning mandatory/required. Must be implemented as specified.

### SHALL NOT
Conformance verb meaning prohibited. Must not be implemented.

### SHOULD
Conformance verb meaning recommended. Should be implemented unless there's a documented reason not to.

### SNOMED CT (Systematized Nomenclature of Medicine -- Clinical Terms)
Comprehensive clinical terminology. OID: `2.16.840.1.113883.6.96`

### Social History
Information about social determinants of health (smoking, alcohol, occupation, etc.). Documented in Social History Section.

### Social History Section
Documents lifestyle and social factors affecting health. Template OID: `2.16.840.1.113883.10.20.22.2.17`

### Status Code
Indicates the state of an act (active, completed, aborted, etc.).

### Structured Body
The structured portion of a CDA document, containing sections and entries (as opposed to unstructured text-only documents).

### Subject
The person or thing the act is about. Usually the patient.

## T

### Telecom
Contact information (phone, email, fax, etc.) using the TEL data type.

### Template
A pattern or constraint on CDA structure defining how to represent specific types of information. Identified by OID.

### Template ID
Element containing template OID and optional version date, indicating document conforms to that template.

### Text Reference
Link from coded entry back to corresponding text in narrative block using `<reference value="#id"/>`.

### Transfer Summary
Document summarizing a patient's status when transferring between care settings. Template OID: `2.16.840.1.113883.10.20.22.1.13`

### TS (Timestamp)
Data type for dates and times in HL7 format (YYYYMMDDHHMMSS with optional timezone).

## U

### UCUM (Unified Code for Units of Measure)
Standard for representing units of measure. OID: `2.16.840.1.113883.6.8`

### Unstructured Document
C-CDA document type containing only narrative text, no structured entries. Template OID: `2.16.840.1.113883.10.20.22.1.10`

### US Realm
United States-specific implementation of CDA. C-CDA is the US Realm implementation guide.

### US Realm Header
Base template for all US C-CDA documents. Defines common header requirements. Template OID: `2.16.840.1.113883.10.20.22.1.1`

## V

### Value
The actual measurement, observation, or result. Data type varies by context (CD for coded values, PQ for quantities, etc.).

### Value Set
A collection of codes from one or more code systems, defining allowed values for a specific use. Identified by OID.

### Value Set Authority Center (VSAC)
NIH service providing official US value sets for C-CDA and other standards.

### Version Number
Optional document version indicator. CDA allows documents to be versioned.

### Vital Signs
Basic physiological measurements (blood pressure, temperature, pulse, etc.). Documented in Vital Signs Section.

### Vital Signs Section
Documents vital sign measurements. Template OID: `2.16.840.1.113883.10.20.22.2.4.1`

### Vital Sign Observation
Entry template for individual vital sign measurements. Template OID: `2.16.840.1.113883.10.20.22.4.27`

### Vocabulary
See Code System. A collection of concepts with codes and definitions.

## W

### Working Group (WG)
HL7 committees that develop and maintain standards. Structured Documents WG maintains C-CDA.

## X

### XML (Extensible Markup Language)
The format used for CDA documents. Text-based markup language with tags, attributes, and nested structure.

### XML Schema
Formal definition of XML structure. CDA has an XML Schema (CDA.xsd) defining valid structure.

### XPath
Query language for navigating XML documents. Used in Schematron rules to identify elements.

### XSLT (Extensible Stylesheet Language Transformations)
Language for transforming XML documents. Often used to render CDA documents as HTML for human viewing.

## Numbers

### 21st Century Cures Act
US federal law requiring healthcare interoperability and patient access to health information, including C-CDA exchange.

## Acronyms Quick Reference

- **C-CDA**: Consolidated Clinical Document Architecture
- **CCD**: Continuity of Care Document
- **CDA**: Clinical Document Architecture
- **CD**: Concept Descriptor
- **ED**: Encapsulated Data
- **EHR**: Electronic Health Record
- **FHIR**: Fast Healthcare Interoperability Resources
- **HL7**: Health Level Seven International
- **ICD**: International Classification of Diseases
- **II**: Instance Identifier
- **IG**: Implementation Guide
- **LOINC**: Logical Observation Identifiers Names and Codes
- **NIST**: National Institute of Standards and Technology
- **NPI**: National Provider Identifier
- **OID**: Object Identifier
- **ONC**: Office of the National Coordinator for Health IT
- **PQ**: Physical Quantity
- **QRDA**: Quality Reporting Document Architecture
- **RIM**: Reference Information Model
- **ROS**: Review of Systems
- **TS**: Timestamp
- **UCUM**: Unified Code for Units of Measure
- **VSAC**: Value Set Authority Center

---

This glossary is maintained to help developers, implementers, and healthcare professionals understand C-CDA and HL7 terminology. Terms are defined in the context of C-CDA implementation.
