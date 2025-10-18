# Document Types: Choosing the Right C-CDA Document

## Introduction

Just as you wouldn't use a birthday card template to write a business proposal, you shouldn't use a discharge summary template when you need a continuity of care document. C-CDA defines several document types, each optimized for specific clinical scenarios and use cases.

This chapter explains the different C-CDA document types, their purposes, required sections, and when to use each one.

## Understanding Document Types

### What Makes a Document Type?

Each C-CDA document type is defined by:

1. **Template ID**: Unique identifier for the document type
2. **LOINC code**: Standardized document type code
3. **Required sections**: Which sections must be present
4. **Optional sections**: Which sections may be included
5. **Use case**: The clinical scenario it's designed for
6. **Target audience**: Who will read/use the document

### Document Type Hierarchy

All C-CDA documents inherit from base templates:

```
CDA R2 Document
  └─ US Realm Header
      ├─ Continuity of Care Document (CCD)
      ├─ Discharge Summary
      ├─ Progress Note
      ├─ Consultation Note
      ├─ History and Physical
      ├─ Operative Note
      ├─ Procedure Note
      ├─ Care Plan
      ├─ Referral Note
      └─ Transfer Summary
```

**US Realm Header** provides common elements all documents share:
- Patient demographics
- Author information
- Custodian
- Document metadata

**Specific document types** add requirements for sections and clinical content.

## The Major Document Types

### Quick Reference Table

| Document Type | Primary Use | Key Sections | Typical Trigger |
|---------------|-------------|--------------|-----------------|
| CCD | Comprehensive summary | All major sections | Referral, portal download |
| Discharge Summary | Hospital discharge | Discharge info, hospital course | Patient leaving hospital |
| Progress Note | Ongoing care documentation | Assessment, plan, subjective | Regular office visit |
| Consultation Note | Specialist consultation | Reason, findings, recommendations | Referral to specialist |
| History and Physical | Initial assessment | History, physical exam, assessment | Hospital admission, annual exam |
| Care Plan | Treatment planning | Problems, goals, interventions | Care coordination |
| Referral Note | Sending patient to specialist | Reason, relevant history | Making referral |
| Transfer Summary | Moving between facilities | Current status, care needs | Transfer to nursing home, rehab |

## Continuity of Care Document (CCD)

### Purpose

The **CCD** is the comprehensive summary document - the "greatest hits" of a patient's medical record. It provides everything a new provider needs to understand the patient's health status.

**Think of it as**: A medical passport - comprehensive information for continuity of care.

### When to Use CCD

- **Care transitions**: Patient seeing new provider
- **Patient portal downloads**: Patients accessing their records
- **Referrals**: Comprehensive information for specialist
- **Health information exchange**: Sharing between systems
- **Emergency care**: Background for ED providers

### Template Information

**Template ID**: `2.16.840.1.113883.10.20.22.1.2`
**Template ID (R2.1)**: `2.16.840.1.113883.10.20.22.1.2` extension `2015-08-01`
**LOINC Code**: `34133-9` - Summarization of Episode Note

### Required Sections

1. **Allergies and Intolerances** (`48765-2`)
2. **Medications** (`10160-0`)
3. **Problems** (`11450-4`)
4. **Results** (`30954-2`) - Lab results

**Note**: Even if patient has no allergies, medications, or problems, sections are still required with appropriate "no known" entries.

### Recommended Sections

- **Procedures** (`47519-4`)
- **Vital Signs** (`8716-3`)
- **Immunizations** (`11369-6`)
- **Social History** (`29762-2`)
- **Family History** (`10157-6`)
- **Functional Status** (`47420-5`)
- **Plan of Treatment** (`18776-5`)
- **Mental Status** (`10190-7`)
- **Encounters** (`46240-8`)

### CCD Structure Example

```xml
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <!-- US Realm Header -->
  <realmCode code="US"/>
  <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.1" extension="2015-08-01"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.2" extension="2015-08-01"/>

  <id root="2.16.840.1.113883.19.5.99999.1" extension="CCD-20240315-001"/>
  <code code="34133-9" codeSystem="2.16.840.1.113883.6.1"
        displayName="Summarization of Episode Note"/>
  <title>Continuity of Care Document</title>
  <effectiveTime value="20240315120000-0500"/>
  <confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25"/>

  <!-- Patient, Author, Custodian, etc. -->
  <recordTarget>...</recordTarget>
  <author>...</author>
  <custodian>...</custodian>

  <!-- Body with sections -->
  <component>
    <structuredBody>
      <component><section><!-- Allergies --></section></component>
      <component><section><!-- Medications --></section></component>
      <component><section><!-- Problems --></section></component>
      <component><section><!-- Results --></section></component>
      <component><section><!-- Procedures --></section></component>
      <component><section><!-- Vital Signs --></section></component>
      <!-- Additional sections as appropriate -->
    </structuredBody>
  </component>
</ClinicalDocument>
```

### CCD Best Practices

1. **Include all relevant active information**: Current medications, active problems, recent labs
2. **Historical context**: Include significant past history
3. **Time-based filtering**: Don't include every historical detail - focus on clinically relevant
4. **Section ordering**: Use standard order (allergies first is convention)
5. **Complete even if empty**: Include required sections with "no known" entries

### CCD Example Scenario

**Situation**: Mrs. Johnson is moving and will see a new primary care physician.

**CCD Contents**:
- Active medications (5 current prescriptions)
- Active problems (hypertension, diabetes, osteoarthritis)
- Recent labs (lipid panel, A1c from last month)
- Recent vital signs
- Immunization history
- Known allergies (penicillin)
- Relevant procedures (knee replacement 2 years ago)
- Social history (non-smoker, lives independently)

**Result**: New physician has comprehensive picture before first visit.

## Discharge Summary

### Purpose

The **Discharge Summary** documents a patient's hospital stay and provides essential information for post-discharge care.

**Think of it as**: The hospital stay wrap-up report.

### When to Use

- **Inpatient discharge**: Patient leaving hospital
- **ED discharge**: Patient leaving emergency department
- **Observation discharge**: Patient leaving after observation stay
- **Post-acute care**: Sending to skilled nursing facility, rehab

### Template Information

**Template ID**: `2.16.840.1.113883.10.20.22.1.8` extension `2015-08-01`
**LOINC Code**: `18842-5` - Discharge Summary

### Required Sections

1. **Allergies and Intolerances** (`48765-2`)
2. **Hospital Course** (`8648-8`) - Narrative of hospital stay
3. **Hospital Discharge Diagnosis** (`11535-2`)
4. **Discharge Medications** (`10183-2`)
5. **Plan of Treatment** (`18776-5`) - Post-discharge plan

### Recommended Sections

- **Chief Complaint and Reason for Visit** (`46239-0`, `29299-5`)
- **Hospital Admission Diagnosis** (`46241-6`)
- **Hospital Discharge Physical** (`10184-0`)
- **Hospital Discharge Studies Summary** (`11493-4`)
- **Procedures** (`47519-4`)
- **Immunizations** (`11369-6`)
- **Problem List** (`11450-4`)
- **Hospital Discharge Instructions** (`8653-8`)
- **Functional Status** (`47420-5`)
- **Reason for Visit** (`29299-5`)

### Discharge Summary Structure

```xml
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <templateId root="2.16.840.1.113883.10.20.22.1.1" extension="2015-08-01"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.8" extension="2015-08-01"/>

  <code code="18842-5" codeSystem="2.16.840.1.113883.6.1"
        displayName="Discharge Summary"/>
  <title>Discharge Summary</title>

  <!-- ... header elements ... -->

  <component>
    <structuredBody>
      <component><section><!-- Allergies --></section></component>
      <component><section><!-- Hospital Admission Diagnosis --></section></component>
      <component><section><!-- Hospital Course --></section></component>
      <component><section><!-- Hospital Discharge Diagnosis --></section></component>
      <component><section><!-- Procedures --></section></component>
      <component><section><!-- Discharge Medications --></section></component>
      <component><section><!-- Plan of Treatment --></section></component>
      <component><section><!-- Hospital Discharge Instructions --></section></component>
    </structuredBody>
  </component>
</ClinicalDocument>
```

### Discharge Summary Best Practices

1. **Complete hospital narrative**: Clear story from admission through discharge
2. **Transition focus**: Emphasize what happens next
3. **Medication reconciliation**: Discharge meds vs. home meds - explain changes
4. **Clear instructions**: What patient/caregivers need to do
5. **Follow-up appointments**: When and with whom
6. **Pending results**: Labs or studies not yet complete

### Discharge Summary Example Scenario

**Situation**: Mr. Brown admitted for pneumonia, treated with IV antibiotics, now ready for discharge.

**Discharge Summary Contents**:
- **Chief complaint**: Shortness of breath, fever
- **Hospital course**: Admitted with pneumonia, treated with ceftriaxone, improved
- **Discharge diagnosis**: Community-acquired pneumonia
- **Procedures**: Chest X-ray, blood cultures
- **Discharge medications**: Oral antibiotics, existing medications
- **Instructions**: Complete antibiotic course, rest, return if fever returns
- **Follow-up**: See PCP in 1 week

**Recipients**:
- Primary care physician (for follow-up)
- Patient (understanding discharge plan)
- Home health (if needed)

## Progress Note

### Purpose

The **Progress Note** documents ongoing care for established patients, typically during office visits or hospital rounds.

**Think of it as**: The regular check-in documentation.

### When to Use

- **Outpatient office visits**: Follow-up appointments
- **Hospital rounds**: Daily inpatient notes
- **Chronic disease management**: Diabetes, hypertension follow-ups
- **Regular check-ins**: Monitoring ongoing conditions

### Template Information

**Template ID**: `2.16.840.1.113883.10.20.22.1.9` extension `2015-08-01`
**LOINC Code**: `11506-3` - Progress Note

### Required Sections

1. **Assessment and Plan** (`51847-2`) - Combined section, OR separate:
   - **Assessment** (`51848-0`)
   - **Plan of Treatment** (`18776-5`)

**Note**: Must have either combined Assessment and Plan, OR separate Assessment and Plan sections.

### Recommended Sections

- **Chief Complaint** (`10154-3`)
- **Allergies and Intolerances** (`48765-2`)
- **Medications** (`10160-0`)
- **Problem List** (`11450-4`)
- **Results** (`30954-2`)
- **Vital Signs** (`8716-3`)
- **Review of Systems** (`10187-3`)
- **Physical Exam** (`29545-1`)
- **Subjective** (`61150-9`)
- **Objective** (`61149-1`)

### Progress Note Structure

```xml
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <templateId root="2.16.840.1.113883.10.20.22.1.1" extension="2015-08-01"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.9" extension="2015-08-01"/>

  <code code="11506-3" codeSystem="2.16.840.1.113883.6.1"
        displayName="Progress Note"/>
  <title>Progress Note</title>

  <component>
    <structuredBody>
      <component><section><!-- Chief Complaint --></section></component>
      <component><section><!-- Subjective --></section></component>
      <component><section><!-- Objective --></section></component>
      <component><section><!-- Assessment and Plan --></section></component>
      <!-- Or separate Assessment and Plan sections -->
    </structuredBody>
  </component>
</ClinicalDocument>
```

### Progress Note Patterns

#### SOAP Format

Many progress notes follow **SOAP** (Subjective, Objective, Assessment, Plan):

```xml
<component>
  <structuredBody>
    <!-- S: Subjective -->
    <component>
      <section>
        <code code="61150-9" codeSystem="2.16.840.1.113883.6.1"
              displayName="Subjective"/>
        <title>Subjective</title>
        <text>Patient reports improved blood pressure control...</text>
      </section>
    </component>

    <!-- O: Objective -->
    <component>
      <section>
        <code code="61149-1" codeSystem="2.16.840.1.113883.6.1"
              displayName="Objective"/>
        <title>Objective</title>
        <text>BP: 128/82, HR: 72...</text>
      </section>
    </component>

    <!-- A & P: Assessment and Plan -->
    <component>
      <section>
        <code code="51847-2" codeSystem="2.16.840.1.113883.6.1"
              displayName="Assessment and Plan"/>
        <title>Assessment and Plan</title>
        <text>HTN well controlled. Continue current medications...</text>
      </section>
    </component>
  </structuredBody>
</component>
```

### Progress Note Example Scenario

**Situation**: Mrs. Davis returns for 3-month diabetes follow-up.

**Progress Note Contents**:
- **Chief complaint**: Diabetes follow-up
- **Subjective**: Blood sugars running 100-130, no hypoglycemia
- **Objective**: Weight stable, BP 130/84, no edema
- **Results**: A1c 6.8% (improved from 7.5%)
- **Assessment**: Type 2 diabetes, good control
- **Plan**: Continue metformin, increase exercise, return in 3 months

**Focus**: Changes since last visit, current status, adjustments to plan.

## Consultation Note

### Purpose

The **Consultation Note** documents a specialist's evaluation and recommendations in response to a referral.

**Think of it as**: The specialist's expert opinion letter.

### When to Use

- **Specialist evaluations**: Cardiologist, endocrinologist, etc.
- **Second opinions**: Another physician's assessment
- **Pre-operative consultations**: Surgeon's evaluation
- **Complex case reviews**: Expert guidance requested

### Template Information

**Template ID**: `2.16.840.1.113883.10.20.22.1.4` extension `2015-08-01`
**LOINC Code**: `11488-4` - Consultation Note

### Required Sections

1. **Assessment and Plan** (`51847-2`) OR separate:
   - **Assessment** (`51848-0`)
   - **Plan of Treatment** (`18776-5`)

### Recommended Sections

- **Chief Complaint and Reason for Visit** (`10154-3`, `29299-5`)
- **History of Present Illness** (`10164-2`)
- **Past Medical History** (`11348-0`)
- **Medications** (`10160-0`)
- **Allergies and Intolerances** (`48765-2`)
- **Social History** (`29762-2`)
- **Family History** (`10157-6`)
- **Review of Systems** (`10187-3`)
- **Physical Exam** (`29545-1`)
- **Results** (`30954-2`)
- **Vital Signs** (`8716-3`)
- **Recommendations** (no specific LOINC, use Assessment and Plan)

### Consultation Note Structure

```xml
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <templateId root="2.16.840.1.113883.10.20.22.1.1" extension="2015-08-01"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.4" extension="2015-08-01"/>

  <code code="11488-4" codeSystem="2.16.840.1.113883.6.1"
        displayName="Consultation Note"/>
  <title>Cardiology Consultation Note</title>

  <component>
    <structuredBody>
      <component><section><!-- Reason for Consultation --></section></component>
      <component><section><!-- History of Present Illness --></section></component>
      <component><section><!-- Past Medical History --></section></component>
      <component><section><!-- Medications --></section></component>
      <component><section><!-- Physical Exam --></section></component>
      <component><section><!-- Results --></section></component>
      <component><section><!-- Assessment and Plan --></section></component>
    </structuredBody>
  </component>
</ClinicalDocument>
```

### Consultation Note Best Practices

1. **Clear reason for consultation**: Why was specialist asked to see patient?
2. **Focused assessment**: Address the consultation question
3. **Explicit recommendations**: What should referring provider do?
4. **Communication**: Sent back to referring provider
5. **Specialist expertise**: Demonstrate specialized knowledge

### Consultation Note Example Scenario

**Situation**: PCP refers Mr. Martinez to cardiologist for evaluation of chest pain.

**Consultation Note Contents**:
- **Reason**: Evaluate atypical chest pain
- **History**: 58-year-old with HTN, chest discomfort with exertion
- **Exam**: Regular rhythm, no murmurs
- **Results**: EKG normal, stress test shows mild ischemia
- **Assessment**: Coronary artery disease, stable angina
- **Recommendations**:
  - Start aspirin and statin
  - Consider cardiac catheterization
  - Will follow in cardiology clinic
  - Return to PCP for HTN management

**Recipients**:
- Referring PCP (primary audience)
- Specialist's own records
- Patient (copy)

## History and Physical (H&P)

### Purpose

The **History and Physical** is a comprehensive initial assessment, often performed at hospital admission or for annual exams.

**Think of it as**: The comprehensive baseline evaluation.

### When to Use

- **Hospital admission**: Initial assessment on admission
- **Pre-operative evaluation**: Before surgery
- **Annual physical exam**: Comprehensive check-up
- **New patient visit**: First visit to new provider
- **Comprehensive evaluation**: Detailed assessment needed

### Template Information

**Template ID**: `2.16.840.1.113883.10.20.22.1.3` extension `2015-08-01`
**LOINC Code**: `34117-2` - History and Physical Note

### Required Sections

1. **Assessment and Plan** (`51847-2`) OR separate sections
2. **Chief Complaint and Reason for Visit** (`10154-3`, `29299-5`)
3. **Past Medical History** (`11348-0`)
4. **Medications** (`10160-0`)
5. **Allergies and Intolerances** (`48765-2`)
6. **Social History** (`29762-2`)
7. **Family History** (`10157-6`)
8. **Review of Systems** (`10187-3`)
9. **Physical Exam** (`29545-1`)

### H&P Structure

```xml
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <templateId root="2.16.840.1.113883.10.20.22.1.1" extension="2015-08-01"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.3" extension="2015-08-01"/>

  <code code="34117-2" codeSystem="2.16.840.1.113883.6.1"
        displayName="History and Physical Note"/>
  <title>History and Physical</title>

  <component>
    <structuredBody>
      <component><section><!-- Chief Complaint --></section></component>
      <component><section><!-- History of Present Illness --></section></component>
      <component><section><!-- Past Medical History --></section></component>
      <component><section><!-- Medications --></section></component>
      <component><section><!-- Allergies --></section></component>
      <component><section><!-- Social History --></section></component>
      <component><section><!-- Family History --></section></component>
      <component><section><!-- Review of Systems --></section></component>
      <component><section><!-- Vital Signs --></section></component>
      <component><section><!-- Physical Exam --></section></component>
      <component><section><!-- Results --></section></component>
      <component><section><!-- Assessment and Plan --></section></component>
    </structuredBody>
  </component>
</ClinicalDocument>
```

### H&P Best Practices

1. **Comprehensive**: More detailed than progress note
2. **Systematic**: Complete review of systems
3. **Baseline establishment**: Create reference point for future comparison
4. **Problem formulation**: Synthesize findings into problem list
5. **Diagnostic reasoning**: Show clinical thinking

## Care Plan

### Purpose

The **Care Plan** documents goals and planned interventions for managing health conditions.

**Think of it as**: The roadmap for managing health problems.

### When to Use

- **Chronic disease management**: Diabetes, CHF, COPD plans
- **Care coordination**: Team-based care planning
- **Transitional care**: Post-discharge planning
- **Patient-centered planning**: Collaborative goal setting
- **Value-based care**: Demonstrating care management

### Template Information

**Template ID**: `2.16.840.1.113883.10.20.22.1.15` extension `2015-08-01`
**LOINC Code**: `52521-2` - Overall Plan of Care/Advance Care Directives

### Required Sections

1. **Health Concerns** (`75310-3`)
2. **Goals** (`61146-7`)
3. **Interventions** (`62387-6`)

### Recommended Sections

- **Health Status Evaluations and Outcomes** (`11383-7`)
- **Outcomes** (nested in Interventions)
- **Problem List** (`11450-4`)
- **Medications** (`10160-0`)

### Care Plan Structure

```xml
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <templateId root="2.16.840.1.113883.10.20.22.1.1" extension="2015-08-01"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.15" extension="2015-08-01"/>

  <code code="52521-2" codeSystem="2.16.840.1.113883.6.1"
        displayName="Overall Plan of Care/Advance Care Directives"/>
  <title>Care Plan</title>

  <component>
    <structuredBody>
      <component><section><!-- Health Concerns --></section></component>
      <component><section><!-- Goals --></section></component>
      <component><section><!-- Interventions --></section></component>
      <component><section><!-- Health Status Outcomes --></section></component>
    </structuredBody>
  </component>
</ClinicalDocument>
```

### Care Plan Example Scenario

**Situation**: Mrs. Thompson has CHF, diabetes, and requires coordinated management.

**Care Plan Contents**:
- **Health Concerns**:
  - CHF with recent exacerbation
  - Poorly controlled diabetes
- **Goals**:
  - Reduce CHF readmissions
  - A1c < 7% within 6 months
  - Lose 10 pounds in 3 months
- **Interventions**:
  - Daily weights, call if gain > 2 lbs
  - Dietary counseling
  - Medication adjustments
  - Home health visits weekly
  - Diabetes education

**Key feature**: Forward-looking, goal-oriented.

## Referral Note

### Purpose

The **Referral Note** is created when sending a patient to another provider, providing relevant context.

**Think of it as**: The introduction letter to another provider.

### When to Use

- **Specialist referral**: Sending to specialist
- **Service referral**: Referring to PT, OT, social work
- **Facility referral**: Sending to imaging center, lab

### Template Information

**Template ID**: `2.16.840.1.113883.10.20.22.1.14` extension `2015-08-01`
**LOINC Code**: `57133-1` - Referral Note

### Required Sections

1. **Plan of Treatment** (`18776-5`) - Including referral reason and expectations

### Recommended Sections

- **Reason for Referral** (`42349-1`)
- **Problem List** (`11450-4`)
- **Medications** (`10160-0`)
- **Allergies** (`48765-2`)
- **Results** (`30954-2`)
- **Vital Signs** (`8716-3`)

### Referral Note Best Practices

1. **Clear question**: What do you want the specialist to address?
2. **Relevant history**: Context for the referral
3. **Prior workup**: What's already been done
4. **Urgency**: How soon should patient be seen
5. **Communication expectations**: What feedback do you need

## Transfer Summary

### Purpose

The **Transfer Summary** documents patient status when transferring between care settings.

**Think of it as**: The patient hand-off document.

### When to Use

- **Hospital to SNF**: Transferring to skilled nursing facility
- **Hospital to rehab**: Moving to rehabilitation facility
- **Hospital to hospital**: Transferring to another hospital
- **ED to floor**: Moving within facility (less common for C-CDA)

### Template Information

**Template ID**: `2.16.840.1.113883.10.20.22.1.13` extension `2015-08-01`
**LOINC Code**: `18761-7` - Transfer Summary Note

### Required Sections

1. **Allergies** (`48765-2`)
2. **Medications** (`10160-0`)
3. **Problem List** (`11450-4`)
4. **Results** (`30954-2`)
5. **Plan of Treatment** (`18776-5`)
6. **Reason for Referral** (`42349-1`)

### Transfer Summary Best Practices

1. **Current status**: Where patient is right now clinically
2. **Outstanding issues**: What still needs attention
3. **Pending results**: Tests not yet resulted
4. **Care needs**: What receiving facility must provide
5. **Anticipatory guidance**: What might happen next

## Document Type Selection Guide

### Decision Tree

**Question 1**: Is this during a hospital stay?

- **Admission** → History and Physical
- **Daily update** → Progress Note
- **Discharge** → Discharge Summary

**Question 2**: Is this outpatient?

- **Regular follow-up** → Progress Note
- **Specialist evaluation** → Consultation Note
- **Comprehensive exam** → History and Physical
- **Summary for another provider** → CCD
- **Making referral** → Referral Note

**Question 3**: Is this care coordination?

- **Care management plan** → Care Plan
- **Transferring facilities** → Transfer Summary
- **Summary of current status** → CCD

### Use Case Matrix

| Scenario | Best Document Type | Rationale |
|----------|-------------------|-----------|
| Patient moving, needs records | CCD | Comprehensive summary |
| Discharged from hospital | Discharge Summary | Documents hospital stay |
| Routine office visit | Progress Note | Ongoing care documentation |
| Sending to cardiologist | Referral Note | Context for specialist |
| Cardiologist's findings | Consultation Note | Specialist response |
| Annual physical | H&P | Comprehensive evaluation |
| Hospital admission | H&P | Initial comprehensive assessment |
| CHF care management | Care Plan | Goals and interventions |
| Moving to nursing home | Transfer Summary | Hand-off document |
| Patient portal download | CCD | Comprehensive portable record |

## Section Requirements Comparison

### Core Sections Across Document Types

| Section | CCD | Discharge | Progress | Consult | H&P | Care Plan |
|---------|-----|-----------|----------|---------|-----|-----------|
| Allergies | Required | Required | Recommended | Recommended | Required | Recommended |
| Medications | Required | Required | Recommended | Recommended | Required | Recommended |
| Problems | Required | Recommended | Recommended | Recommended | Required | Recommended |
| Results | Required | Recommended | Recommended | Recommended | Recommended | - |
| Vital Signs | Recommended | Recommended | Recommended | Recommended | Recommended | - |
| Procedures | Recommended | Recommended | Recommended | Recommended | Recommended | - |
| Assessment & Plan | - | Required | Required | Required | Required | - |
| Goals | - | - | - | - | - | Required |
| Interventions | - | - | - | - | - | Required |

**Key insight**: Requirements reflect document purpose.

## Multi-Document Scenarios

### When to Create Multiple Documents

Sometimes one document isn't enough:

#### Scenario 1: Hospital Stay

1. **Admission**: H&P (comprehensive initial assessment)
2. **Daily**: Progress Notes (daily updates)
3. **Procedure**: Operative Note (if surgery performed)
4. **Discharge**: Discharge Summary (wrap-up)
5. **Follow-up**: Consultation Note to PCP

#### Scenario 2: Complex Outpatient

1. **PCP Visit**: Progress Note (identifies issue)
2. **Referral**: Referral Note (sends to specialist)
3. **Specialist**: Consultation Note (specialist's evaluation)
4. **Care Coordination**: Care Plan (ongoing management)
5. **Patient Request**: CCD (comprehensive summary for patient)

### Document Relationships

C-CDA supports linking related documents:

```xml
<relatedDocument typeCode="APND">
  <parentDocument>
    <id root="2.16.840.1.113883.19.5.99999.1" extension="PREVIOUS-DOC-001"/>
  </parentDocument>
</relatedDocument>
```

**Relationship types**:
- `APND`: Appends to (adds to previous)
- `RPLC`: Replaces (supersedes previous)
- `XFRM`: Transforms (format change of same content)

## Best Practices Across All Document Types

### 1. Choose the Right Type

- Match document type to clinical scenario
- Don't force-fit wrong type
- When in doubt, CCD is safest but may be overkill

### 2. Complete Required Sections

- Even if "no information" - include with appropriate null flavors or "no known"
- Don't skip required sections
- Use "Unknown" rather than omitting

### 3. Narrative Quality

- Human-readable narrative is primary
- Structured entries support but don't replace narrative
- Write for the intended reader

### 4. Appropriate Detail

- Match detail level to document purpose
- Progress note: Recent changes
- H&P: Comprehensive baseline
- Discharge: Hospital events

### 5. Section Ordering

Standard order (not required but conventional):
1. Allergies (safety-critical)
2. Medications (safety-critical)
3. Problems
4. History sections (HPI, PMH, etc.)
5. Exam/Objective sections
6. Results
7. Assessment/Diagnostic sections
8. Plan sections

### 6. Timeliness

- Create documents when clinically indicated
- Don't delay for perfection
- Update as needed (with proper versioning)

### 7. Audience Awareness

- **CCD**: Another provider or patient
- **Discharge Summary**: Next caregiver
- **Progress Note**: Continuity within practice
- **Consultation**: Referring provider
- Write for the reader

## Common Mistakes

### Mistake 1: Wrong Document Type

```
❌ Using Progress Note for comprehensive patient summary
✅ Use CCD for comprehensive summary
```

### Mistake 2: Missing Required Sections

```
❌ Discharge Summary without Hospital Course section
✅ Include all required sections, even if brief
```

### Mistake 3: Inappropriate Detail

```
❌ Including every historical detail in Progress Note
✅ Focus on current visit and relevant recent history
```

### Mistake 4: Wrong LOINC Code

```xml
<!-- WRONG: Using CCD LOINC for Discharge Summary -->
<code code="34133-9" codeSystem="2.16.840.1.113883.6.1"/>

<!-- CORRECT: Use Discharge Summary LOINC -->
<code code="18842-5" codeSystem="2.16.840.1.113883.6.1"
      displayName="Discharge Summary"/>
```

### Mistake 5: Inconsistent templateId and code

```xml
<!-- WRONG: CCD templateId with Discharge Summary code -->
<templateId root="2.16.840.1.113883.10.20.22.1.2"/>
<code code="18842-5" codeSystem="2.16.840.1.113883.6.1"/>

<!-- CORRECT: Matching templateId and code -->
<templateId root="2.16.840.1.113883.10.20.22.1.8" extension="2015-08-01"/>
<code code="18842-5" codeSystem="2.16.840.1.113883.6.1"/>
```

## Document Type Resources

### Specifications

- **C-CDA R2.1 Implementation Guide**: Full template specifications
- **C-CDA Companion Guide**: Additional guidance and examples
- **HL7 CDA R2 Standard**: Base standard

### Sample Documents

- **HL7 C-CDA Examples**: Official example documents
- **ONC SITE Validator**: Includes sample documents
- **Vendor examples**: Many EHR vendors publish samples

### Validation

- **NIST MDHT Validator**: Validates document types
- **SITE Validator**: ONC certification validator
- **Schematron files**: Rule-based validation

## Key Takeaways

- **Document type matches use case**: Choose based on clinical scenario
- **CCD is comprehensive**: Use for patient summaries
- **Discharge Summary for transitions**: Hospital to next care setting
- **Progress Note for ongoing care**: Regular visits and updates
- **Consultation Note for specialists**: Specialist evaluations and recommendations
- **H&P for comprehensive assessment**: Baseline evaluations
- **Care Plan for care management**: Goals and interventions
- **Required sections vary by type**: Check specifications for each
- **Section ordering is conventional**: Follow common patterns
- **Write for the reader**: Consider document audience

## What's Next

You now understand:
1. HL7 and C-CDA foundations
2. CDA architecture
3. Templates and conformance
4. Code systems and terminologies
5. Document types and their uses

The next chapters will dive into specific sections and entries, showing you how to implement each component in detail. You'll learn to build complete, conformant C-CDA documents from the ground up.

Think of it this way: You've learned what types of documents exist (business letter, thank-you note, etc.). Next, you'll learn to write each paragraph and sentence within those documents.
