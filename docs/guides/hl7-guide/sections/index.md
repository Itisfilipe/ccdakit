# C-CDA Sections Overview

## Introduction to C-CDA Sections

Sections are the fundamental building blocks of C-CDA documents. Each section represents a specific category of clinical information and contains:

- **Narrative text** - Human-readable HTML table or formatted text
- **Structured entries** - Machine-processable coded data
- **Template IDs** - Conformance identifiers
- **Section metadata** - Title, code, and author information

### Section Structure

Every C-CDA section follows this pattern:

```xml
<section>
  <templateId root="2.16.840.1.113883.10.20.22.2.5.1"/>
  <code code="11450-4" codeSystem="2.16.840.1.113883.6.1" displayName="Problem List"/>
  <title>Problems</title>
  <text>
    <!-- Narrative HTML content -->
    <table>
      <thead><tr><th>Problem</th><th>Status</th><th>Date</th></tr></thead>
      <tbody><tr><td>Type 2 Diabetes</td><td>Active</td><td>2020-03-15</td></tr></tbody>
    </table>
  </text>
  <entry>
    <!-- Structured clinical data -->
    <observation classCode="OBS" moodCode="EVN">...</observation>
  </entry>
</section>
```

## All 39 C-CDA Sections

ccdakit implements 39 sections from C-CDA Release 2.1. Sections are organized into four categories based on their clinical purpose and usage patterns.

---

## Core Clinical Sections

These 9 sections form the backbone of most clinical documents. They contain essential patient information required for care coordination and continuity.

### 1. [Problems Section](problems-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.5.1
**LOINC Code:** 11450-4

Active and historical diagnoses, conditions, and health concerns.

**Use Cases:** Current problem list, chronic conditions, active diagnoses
**Key Data:** Problem name, SNOMED/ICD-10 codes, onset date, status
**Common In:** CCD, Consultation Notes, Discharge Summaries

### 2. [Medications Section](medications-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.1.1
**LOINC Code:** 10160-0

Current and historical medication therapy including prescriptions and over-the-counter medications.

**Use Cases:** Medication list, drug therapy documentation
**Key Data:** Medication name, RxNorm code, dosage, route, frequency, status
**Common In:** CCD, Progress Notes, Discharge Summaries

### 3. [Allergies Section](allergies-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.6.1
**LOINC Code:** 48765-2

Allergies, adverse reactions, and intolerances to medications, foods, and environmental factors.

**Use Cases:** Allergy documentation, contraindication tracking
**Key Data:** Allergen, reaction, severity, status, onset date
**Common In:** CCD, Pre-procedure documentation, Medication reconciliation

### 4. [Immunizations Section](immunizations-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.2.1
**LOINC Code:** 11369-6

Vaccination history including administered vaccines and refusals.

**Use Cases:** Immunization records, vaccine compliance
**Key Data:** Vaccine name, CVX code, administration date, status, lot number
**Common In:** CCD, School health records, Travel medicine

### 5. [Vital Signs Section](vital-signs-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.4.1
**LOINC Code:** 8716-3

Clinical measurements including blood pressure, temperature, pulse, respiratory rate, height, weight, and BMI.

**Use Cases:** Vital signs documentation, trending, monitoring
**Key Data:** Observation type, value, unit, timestamp
**Common In:** Progress Notes, Emergency Department Notes, All encounters

### 6. [Procedures Section](procedures-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.7.1
**LOINC Code:** 47519-4

Surgical and diagnostic procedures performed or planned.

**Use Cases:** Procedure history, surgical documentation
**Key Data:** Procedure name, CPT/SNOMED code, date, status, provider
**Common In:** Operative Notes, Procedure Notes, CCD

### 7. [Results Section](results-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.3.1
**LOINC Code:** 30954-2

Laboratory, radiology, and other diagnostic test results organized into panels.

**Use Cases:** Lab results, diagnostic imaging findings
**Key Data:** Test name, LOINC code, result value, reference range, interpretation
**Common In:** Lab Reports, CCD, Diagnostic Reports

### 8. [Social History Section](social-history-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.17
**LOINC Code:** 29762-2

Social determinants of health including smoking status, occupation, education, and living situation.

**Use Cases:** Social history documentation, risk assessment
**Key Data:** Smoking status, alcohol use, occupation, social circumstances
**Common In:** History and Physical, CCD, Comprehensive assessments

### 9. [Encounters Section](encounters-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.22.1
**LOINC Code:** 46240-8

Healthcare encounters including visits, admissions, and telehealth sessions.

**Use Cases:** Encounter history, visit documentation
**Key Data:** Encounter type, date, location, providers, diagnoses
**Common In:** CCD, Transfer Summaries, Care summaries

---

## Extended Clinical Sections

These 9 sections provide additional clinical detail for comprehensive patient documentation.

### 10. [Past Medical History Section](past-medical-history-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.20
**LOINC Code:** 11348-0

Historical diagnoses, conditions, and significant past illnesses.

**Use Cases:** Historical problem documentation, baseline health status
**Key Data:** Past conditions, resolution dates, historical context
**Common In:** History and Physical, Consultation Notes

### 11. [Family History Section](family-history-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.15
**LOINC Code:** 10157-6

Family member health conditions and genetic risk factors.

**Use Cases:** Hereditary risk assessment, genetic counseling
**Key Data:** Relationship, age, conditions, age at onset
**Common In:** History and Physical, Genetic counseling notes

### 12. [Functional Status Section](functional-status-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.14
**LOINC Code:** 47420-5

Physical abilities, activities of daily living (ADLs), and functional assessments.

**Use Cases:** Disability assessment, rehabilitation planning
**Key Data:** ADL status, IADL status, mobility, self-care abilities
**Common In:** Rehabilitation notes, Long-term care documentation

### 13. [Mental Status Section](mental-status-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.56
**LOINC Code:** 10190-7

Cognitive function, psychological state, and mental competency observations.

**Use Cases:** Cognitive assessment, mental health documentation
**Key Data:** Cognitive status, affect, orientation, memory
**Common In:** Psychiatric evaluations, Geriatric assessments

### 14. [Goals Section](goals-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.60
**LOINC Code:** 61146-7

Patient health goals and treatment objectives.

**Use Cases:** Care planning, patient engagement, outcome tracking
**Key Data:** Goal description, target date, priority, status
**Common In:** Care plans, Chronic disease management

### 15. [Health Concerns Section](health-concerns-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.58
**LOINC Code:** 75310-3

Clinical concerns requiring attention and ongoing management.

**Use Cases:** Problem tracking, care coordination
**Key Data:** Concern description, status, related observations
**Common In:** Care plans, Consultation notes

### 16. [Medical Equipment Section](medical-equipment-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.23
**LOINC Code:** 46264-8

Implanted devices and durable medical equipment.

**Use Cases:** Device tracking, equipment documentation
**Key Data:** Device name, UDI, implant date, status
**Common In:** CCD, Operative notes, Device registries

### 17. [Advance Directives Section](advance-directives-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.21.1
**LOINC Code:** 42348-3

Living wills, healthcare proxies, and resuscitation preferences.

**Use Cases:** End-of-life planning, legal directives
**Key Data:** Directive type, custodian, effective dates
**Common In:** CCD, Admission documentation, Care plans

### 18. [Plan of Treatment Section](plan-of-treatment-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.10
**LOINC Code:** 18776-5

Planned procedures, medications, observations, and interventions.

**Use Cases:** Treatment planning, pending orders
**Key Data:** Planned activities, intent, scheduling
**Common In:** Care plans, Consultation notes, Progress notes

---

## Specialized/Administrative Sections

These 11 sections support specific clinical scenarios and administrative requirements.

### 19. [Assessment and Plan Section](assessment-and-plan-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.9
**LOINC Code:** 51847-2

Clinical assessment and treatment plan combined.

**Use Cases:** SOAP note documentation, clinical reasoning
**Key Data:** Assessment findings, plan items, clinical reasoning
**Common In:** Progress Notes, SOAP notes, Outpatient visits

### 20. [Chief Complaint and Reason for Visit Section](chief-complaint-reason-for-visit-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.13
**LOINC Code:** 46239-0

Patient's presenting complaint and provider's reason for visit.

**Use Cases:** Visit documentation, chief complaint capture
**Key Data:** Complaint text, reason for visit
**Common In:** Emergency Department notes, Urgent care visits

### 21. [Reason for Visit Section](reason-for-visit-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.12
**LOINC Code:** 29299-5

Provider's documentation of visit purpose.

**Use Cases:** Visit justification, billing support
**Key Data:** Reason text (narrative only)
**Common In:** Consultation notes, Specialty visits

### 22. [Physical Exam Section](physical-exam-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.27
**LOINC Code:** 29545-1

Physical examination findings organized by body system.

**Use Cases:** Exam documentation, clinical assessment
**Key Data:** System findings, wound observations, exam results
**Common In:** History and Physical, Progress notes

### 23. [Nutrition Section](nutrition-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.57
**LOINC Code:** 61144-2

Dietary requirements, nutritional status, and diet orders.

**Use Cases:** Diet planning, nutritional assessment
**Key Data:** Nutritional status, diet orders, restrictions
**Common In:** Nutrition assessments, Hospital orders

### 24. [Interventions Section](interventions-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.60
**LOINC Code:** 62387-6

Actions taken to address health concerns and achieve goals.

**Use Cases:** Care coordination, barrier removal
**Key Data:** Intervention type, status, effective time
**Common In:** Care plans, Social work notes

### 25. [Health Status Evaluations and Outcomes Section](health-status-evaluations-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.61
**LOINC Code:** 11383-7

Patient health status and outcomes of interventions.

**Use Cases:** Outcome tracking, quality measurement
**Key Data:** Status codes, outcome values, effectiveness
**Common In:** Quality reports, Outcome assessments

### 26. [Payers Section](payers-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.18
**LOINC Code:** 48768-6

Insurance coverage and payer information.

**Use Cases:** Billing, insurance verification
**Key Data:** Payer name, member ID, coverage dates
**Common In:** CCD, Registration documents

### 27. [Hospital Discharge Instructions Section](hospital-discharge-instructions-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.41
**LOINC Code:** 8653-8

Instructions provided to patient at hospital discharge.

**Use Cases:** Discharge planning, patient education
**Key Data:** Instruction text, categories, follow-up
**Common In:** Discharge Summaries, Hospital discharge documentation

### 28. [Discharge Medications Section](discharge-medications-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.11.1
**LOINC Code:** 10183-2

Medications prescribed or discontinued at discharge.

**Use Cases:** Medication reconciliation, discharge orders
**Key Data:** Same as Medications Section
**Common In:** Discharge Summaries, Transfer documentation

### 29. [Admission Medications Section](admission-medications-section.md)
**Template ID:** 2.16.840.1.113883.10.20.22.2.44
**LOINC Code:** 42346-7

Medications patient was taking at admission.

**Use Cases:** Medication reconciliation, admission documentation
**Key Data:** Same as Medications Section
**Common In:** History and Physical, Admission notes

---

## Hospital and Surgical Sections

These 10 sections are specifically designed for hospital workflows, surgical documentation, and discharge summaries.

### 30. Admission Diagnosis Section
**Template ID:** 2.16.840.1.113883.10.20.22.2.43
**LOINC Code:** 46241-6

Diagnoses identified at hospital admission.

**Use Cases:** Hospital admission documentation, diagnosis reconciliation
**Key Data:** Diagnosis name, SNOMED/ICD-10 codes, admission date, diagnosis date
**Common In:** Discharge Summaries, Hospital admission notes

### 31. Discharge Diagnosis Section
**Template ID:** 2.16.840.1.113883.10.20.22.2.24
**LOINC Code:** 11535-2

Final diagnoses at hospital discharge.

**Use Cases:** Discharge documentation, billing, diagnosis reconciliation
**Key Data:** Diagnosis name, SNOMED/ICD-10 codes, status, discharge disposition, priority
**Common In:** Discharge Summaries, Hospital discharge notes

### 32. Hospital Course Section
**Template ID:** 1.3.6.1.4.1.19376.1.5.3.1.3.5
**LOINC Code:** 8648-8

Narrative description of patient's hospital stay from admission to discharge.

**Use Cases:** Hospital stay documentation, handoff communication
**Key Data:** Narrative text describing daily hospital course, events, interventions
**Common In:** Discharge Summaries, Transfer summaries

### 33. Instructions Section
**Template ID:** 2.16.840.1.113883.10.20.22.2.45
**LOINC Code:** 69730-0

General patient instructions and education materials.

**Use Cases:** Patient education, instruction documentation
**Key Data:** Instruction text, instruction type codes, patient education materials
**Common In:** Discharge Summaries, Procedure notes, Patient education documents

### 34. Anesthesia Section
**Template ID:** 2.16.840.1.113883.10.20.22.2.25
**LOINC Code:** 59774-0

Anesthesia procedures and medications administered during surgery.

**Use Cases:** Operative documentation, anesthesia records
**Key Data:** Anesthesia type, agents used, route, start/end times, performer
**Common In:** Operative Notes, Procedure Notes

### 35. Postoperative Diagnosis Section
**Template ID:** 2.16.840.1.113883.10.20.22.2.35
**LOINC Code:** 10218-6

Diagnoses identified or confirmed during surgery.

**Use Cases:** Surgical documentation, operative findings
**Key Data:** Postoperative diagnosis narrative text
**Common In:** Operative Notes, Surgical procedure notes

### 36. Preoperative Diagnosis Section
**Template ID:** 2.16.840.1.113883.10.20.22.2.34
**LOINC Code:** 10219-4

Diagnoses assigned before surgery.

**Use Cases:** Surgical planning, operative documentation
**Key Data:** Diagnosis name, SNOMED/ICD-10 codes, status, diagnosis date
**Common In:** Operative Notes, Pre-procedure documentation

### 37. Complications Section
**Template ID:** 2.16.840.1.113883.10.20.22.2.37
**LOINC Code:** 55109-3

Complications that occurred during or after procedures.

**Use Cases:** Complication tracking, quality monitoring
**Key Data:** Complication name, severity, onset date, status, related procedure
**Common In:** Operative Notes, Procedure Notes, Discharge Summaries

### 38. Hospital Discharge Studies Summary Section
**Template ID:** 2.16.840.1.113883.10.20.22.2.16
**LOINC Code:** 11493-4

Summary of diagnostic studies performed during hospitalization.

**Use Cases:** Discharge documentation, test result summary
**Key Data:** Study panels, individual studies, results, interpretations, reference ranges
**Common In:** Discharge Summaries, Hospital documentation

### 39. Medications Administered Section
**Template ID:** 2.16.840.1.113883.10.20.22.2.38
**LOINC Code:** 29549-3

Medications actually administered during an encounter or procedure.

**Use Cases:** Medication administration records, procedure documentation
**Key Data:** Medication name, dose, route, administration time, rate, site, performer
**Common In:** Operative Notes, Procedure Notes, Medication administration records

---

## Section Categories Explained

### Core Clinical Sections
The essential information needed for continuity of care. These sections appear in most document types and form the foundation of the CCD (Continuity of Care Document).

**Typical documents:** CCD, Consultation Notes, Transfer Summaries

### Extended Clinical Sections
Additional clinical detail that provides comprehensive patient context. Used when more complete documentation is required.

**Typical documents:** History and Physical, Comprehensive assessments, Care plans

### Specialized/Administrative Sections
Context-specific sections for particular clinical scenarios or administrative requirements. Not all documents need these sections.

**Typical documents:** Discharge Summaries, SOAP notes, Specific note types

### Hospital and Surgical Sections
Sections specifically designed for hospital workflows, surgical procedures, and discharge documentation. Essential for operative notes and discharge summaries.

**Typical documents:** Discharge Summaries, Operative Notes, Procedure Notes, Hospital documentation

---

## How Sections Fit Into Documents

### Document Structure Hierarchy

```
ClinicalDocument (root)
├── Header (patient, providers, metadata)
└── Body
    └── structuredBody
        ├── Section (e.g., Problems)
        │   ├── Narrative text
        │   └── Entries (structured data)
        ├── Section (e.g., Medications)
        │   ├── Narrative text
        │   └── Entries
        └── [Additional sections...]
```

### Document Type Requirements

Different C-CDA document types require different section combinations:

**Continuity of Care Document (CCD):**
- REQUIRED: Allergies, Medications, Problems, Results (if available)
- RECOMMENDED: Immunizations, Vital Signs, Procedures, Social History

**Discharge Summary:**
- REQUIRED: Hospital Discharge Diagnosis, Discharge Medications
- RECOMMENDED: Chief Complaint, Hospital Course, Discharge Instructions

**History and Physical:**
- REQUIRED: Chief Complaint, History of Present Illness, Physical Exam
- RECOMMENDED: Past Medical History, Family History, Social History

Consult the Document Type Matrix (see [Document Types guide](../05-document-types.md) for details) for complete requirements.

---

## Common Section Patterns

### Narrative + Entries Pattern
Most sections follow this pattern:
- Human-readable narrative (HTML)
- Machine-processable entries (XML)
- Both must represent the same information

```python
from ccdakit import ProblemsSection

section = ProblemsSection(
    problems=problem_list,  # Generates both narrative and entries
    version=CDAVersion.R2_1
)
```

### Narrative-Only Sections
Some sections contain only narrative text:
- Reason for Visit
- Chief Complaint and Reason for Visit (when simple)

### Organizer-Based Sections
Some sections use organizers to group related observations:
- Results (lab panels)
- Vital Signs (vital sign sets)
- Functional Status (ADL assessments)

### Timeline Sections
Sections documenting events over time:
- Encounters
- Procedures
- Immunizations

---

## Implementation Guide

### Getting Started

1. **Identify required sections** for your document type
2. **Prepare your data** according to protocol requirements
3. **Create section instances** using ccdakit builders
4. **Add sections to document** in recommended order
5. **Validate output** against C-CDA specifications

### Best Practices

**Section Ordering:**
- Follow conventional ordering (Problems, Medications, Allergies first)
- Group related sections together
- Place administrative sections last

**Data Quality:**
- Use proper code systems (SNOMED, LOINC, RxNorm)
- Include dates and times with appropriate precision
- Provide narrative that matches structured data

**Validation:**
- Test with NIST validator
- Verify template IDs match specification version
- Check narrative/entry consistency

### Common Pitfalls

1. **Missing required data elements** - Each section has specific requirements
2. **Incorrect code systems** - Use specified terminologies (LOINC for sections, SNOMED for problems)
3. **Narrative/entry mismatches** - Narrative must reflect structured entries
4. **Wrong template versions** - Use 2.1 template IDs for C-CDA 2.1 documents
5. **Empty sections** - Include only sections with actual data

---

## Next Steps

**Explore Individual Sections:**
- Browse sections by category above
- Each section page includes implementation details and examples

**Learn Common Patterns:**
- [Code Systems](../04-code-systems-and-terminologies.md) - Terminologies reference
- [Template IDs](../appendices/oid-reference.md) - Complete template directory

**See Complete Examples:**
- [All Sections Example](../../../examples/all-sections.md) - Working code for all 39 sections
- [Complete Document](../../../examples/complete-document.md) - Full CCD implementation

**Back to Guide Home:**
- [HL7/C-CDA Guide](../index.md) - Return to main guide page

---

**Need help?** Each section page includes detailed implementation guidance, code examples, and common patterns. Start with the sections most relevant to your use case.
