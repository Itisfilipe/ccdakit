# OID Reference

Quick reference guide for Object Identifiers (OIDs) commonly used in C-CDA documents.

## What is an OID?

An Object Identifier (OID) is a globally unique identifier used in HL7 standards to identify templates, code systems, and other healthcare data elements. OIDs follow the ISO/ITU-T standard format (e.g., `2.16.840.1.113883.10.20.22.1.1`).

## Document Type OIDs

### C-CDA R2.1 Document Templates

| Document Type | OID | Template ID |
|--------------|-----|-------------|
| US Realm Header | `2.16.840.1.113883.10.20.22.1.1` | 2015-08-01 |
| Continuity of Care Document (CCD) | `2.16.840.1.113883.10.20.22.1.2` | 2015-08-01 |
| Consultation Note | `2.16.840.1.113883.10.20.22.1.4` | 2015-08-01 |
| Discharge Summary | `2.16.840.1.113883.10.20.22.1.8` | 2015-08-01 |
| History and Physical | `2.16.840.1.113883.10.20.22.1.3` | 2015-08-01 |
| Progress Note | `2.16.840.1.113883.10.20.22.1.9` | 2015-08-01 |
| Procedure Note | `2.16.840.1.113883.10.20.22.1.6` | 2015-08-01 |
| Operative Note | `2.16.840.1.113883.10.20.22.1.7` | 2015-08-01 |
| Care Plan | `2.16.840.1.113883.10.20.22.1.15` | 2015-08-01 |
| Transfer Summary | `2.16.840.1.113883.10.20.22.1.13` | 2015-08-01 |
| Referral Note | `2.16.840.1.113883.10.20.22.1.14` | 2015-08-01 |
| Unstructured Document | `2.16.840.1.113883.10.20.22.1.10` | 2015-08-01 |

## Section Template OIDs

### All 29 C-CDA R2.1 Sections

| Section Name | OID | Template ID |
|-------------|-----|-------------|
| Advance Directives Section | `2.16.840.1.113883.10.20.22.2.21` | 2015-08-01 |
| Allergies and Intolerances Section | `2.16.840.1.113883.10.20.22.2.6.1` | 2015-08-01 |
| Assessment Section | `2.16.840.1.113883.10.20.22.2.8` | 2014-06-09 |
| Assessment and Plan Section | `2.16.840.1.113883.10.20.22.2.9` | 2014-06-09 |
| Chief Complaint Section | `2.16.840.1.113883.10.20.22.2.13` | 2014-06-09 |
| Chief Complaint and Reason for Visit Section | `2.16.840.1.113883.10.20.22.2.13` | 2014-06-09 |
| Encounters Section | `2.16.840.1.113883.10.20.22.2.22.1` | 2015-08-01 |
| Family History Section | `2.16.840.1.113883.10.20.22.2.15` | 2015-08-01 |
| Functional Status Section | `2.16.840.1.113883.10.20.22.2.14` | 2014-06-09 |
| General Status Section | `2.16.840.1.113883.10.20.22.2.45` | 2015-08-01 |
| Goals Section | `2.16.840.1.113883.10.20.22.2.60` | 2015-08-01 |
| Health Concerns Section | `2.16.840.1.113883.10.20.22.2.58` | 2015-08-01 |
| History of Past Illness Section | `2.16.840.1.113883.10.20.22.2.20` | 2015-08-01 |
| History of Present Illness Section | `2.16.840.1.113883.10.20.22.2.33` | 2015-08-01 |
| Immunizations Section | `2.16.840.1.113883.10.20.22.2.2.1` | 2015-08-01 |
| Instructions Section | `2.16.840.1.113883.10.20.22.2.45` | 2014-06-09 |
| Interventions Section | `2.16.840.1.113883.10.20.21.2.3` | 2015-08-01 |
| Medical Equipment Section | `2.16.840.1.113883.10.20.22.2.23` | 2014-06-09 |
| Medications Section | `2.16.840.1.113883.10.20.22.2.1.1` | 2014-06-09 |
| Mental Status Section | `2.16.840.1.113883.10.20.22.2.56` | 2015-08-01 |
| Nutrition Section | `2.16.840.1.113883.10.20.22.2.57` | 2015-08-01 |
| Payers Section | `2.16.840.1.113883.10.20.22.2.18` | 2015-08-01 |
| Physical Exam Section | `2.16.840.1.113883.10.20.2.10` | 2015-08-01 |
| Plan of Treatment Section | `2.16.840.1.113883.10.20.22.2.10` | 2014-06-09 |
| Problem Section | `2.16.840.1.113883.10.20.22.2.5.1` | 2015-08-01 |
| Procedures Section | `2.16.840.1.113883.10.20.22.2.7.1` | 2014-06-09 |
| Reason for Visit Section | `2.16.840.1.113883.10.20.22.2.12` | 2014-06-09 |
| Results Section | `2.16.840.1.113883.10.20.22.2.3.1` | 2015-08-01 |
| Review of Systems Section | `2.16.840.1.113883.10.20.22.2.40` | 2015-08-01 |
| Social History Section | `2.16.840.1.113883.10.20.22.2.17` | 2015-08-01 |
| Vital Signs Section | `2.16.840.1.113883.10.20.22.2.4.1` | 2015-08-01 |

## Code System OIDs

### Standard Terminologies

| Code System | OID | Usage |
|------------|-----|-------|
| SNOMED CT | `2.16.840.1.113883.6.96` | Clinical terms, problems, procedures |
| LOINC | `2.16.840.1.113883.6.1` | Lab results, document types, vital signs |
| RxNorm | `2.16.840.1.113883.6.88` | Medications and drugs |
| CPT-4 | `2.16.840.1.113883.6.12` | Procedures and services |
| ICD-10-CM | `2.16.840.1.113883.6.90` | Diagnosis codes |
| ICD-10-PCS | `2.16.840.1.113883.6.4` | Procedure codes |
| ICD-9-CM | `2.16.840.1.113883.6.103` | Legacy diagnosis codes |
| CVX | `2.16.840.1.113883.12.292` | Vaccine codes |
| NDC | `2.16.840.1.113883.6.69` | National Drug Codes |
| UCUM | `2.16.840.1.113883.6.8` | Units of measure |
| NCI Thesaurus | `2.16.840.1.113883.3.26.1.1` | Cancer and research terms |
| HL7 ActCode | `2.16.840.1.113883.5.4` | HL7-defined act codes |
| HL7 RoleCode | `2.16.840.1.113883.5.111` | HL7-defined role codes |
| HL7 ParticipationType | `2.16.840.1.113883.5.90` | Participation types |
| HL7 AdministrativeGender | `2.16.840.1.113883.5.1` | Gender codes |
| HL7 MaritalStatus | `2.16.840.1.113883.5.2` | Marital status codes |
| HL7 RaceCategory | `2.16.840.1.113883.6.238` | Race and ethnicity |
| HL7 NullFlavor | `2.16.840.1.113883.5.1008` | Null/missing value reasons |

## Entry Template OIDs

### Common Entry Templates

| Entry Template | OID | Template ID |
|---------------|-----|-------------|
| Allergy Intolerance Observation | `2.16.840.1.113883.10.20.22.4.7` | 2014-06-09 |
| Medication Activity | `2.16.840.1.113883.10.20.22.4.16` | 2014-06-09 |
| Problem Observation | `2.16.840.1.113883.10.20.22.4.4` | 2015-08-01 |
| Procedure Activity | `2.16.840.1.113883.10.20.22.4.14` | 2014-06-09 |
| Result Observation | `2.16.840.1.113883.10.20.22.4.2` | 2015-08-01 |
| Vital Sign Observation | `2.16.840.1.113883.10.20.22.4.27` | 2014-06-09 |
| Immunization Activity | `2.16.840.1.113883.10.20.22.4.52` | 2015-08-01 |
| Encounter Activity | `2.16.840.1.113883.10.20.22.4.49` | 2015-08-01 |
| Social History Observation | `2.16.840.1.113883.10.20.22.4.38` | 2014-06-09 |
| Family History Observation | `2.16.840.1.113883.10.20.22.4.46` | 2015-08-01 |

## Value Set OIDs

### Commonly Used Value Sets

| Value Set | OID | Purpose |
|----------|-----|---------|
| Problem Type | `2.16.840.1.113883.3.88.12.3221.7.2` | Classify problem types |
| Allergy/Adverse Event Type | `2.16.840.1.113883.3.88.12.3221.6.2` | Allergy classification |
| Medication Route FDA | `2.16.840.1.113883.3.88.12.3221.8.7` | Drug administration routes |
| Body Site Value Set | `2.16.840.1.113883.3.88.12.3221.8.9` | Anatomical locations |
| Problem Severity | `2.16.840.1.113883.3.88.12.3221.6.8` | Problem severity levels |
| Vital Sign Result Type | `2.16.840.1.113883.3.88.12.80.62` | Types of vital signs |

## Organization and Provider OIDs

### Identity System OIDs

| System | OID | Usage |
|--------|-----|-------|
| NPI (National Provider Identifier) | `2.16.840.1.113883.4.6` | Provider identification |
| TIN (Tax ID Number) | `2.16.840.1.113883.4.2` | Organization identification |
| SSN (Social Security Number) | `2.16.840.1.113883.4.1` | Patient identification (avoid) |
| State License | `2.16.840.1.113883.4.3.{state}` | State-issued IDs |
| DEA Number | `2.16.840.1.113883.4.814` | Drug prescriber ID |

## Using OIDs in ccdakit

### In Python Code

```python
from ccdakit.models.sections import AllergiesSection

# OID is automatically included when building sections
section = AllergiesSection()
# The template OID 2.16.840.1.113883.10.20.22.2.6.1 is added automatically

# For code systems in observations
from ccdakit.models.datatypes import CD

code = CD(
    code="1234567",
    code_system="2.16.840.1.113883.6.96",  # SNOMED CT OID
    display_name="Example Finding"
)
```

### Verifying OIDs

When validating C-CDA documents, validators check that:
- Template OIDs match declared conformance level
- Template IDs (dates) are correct for the version
- Code system OIDs are valid and appropriate for the context
- Referenced value sets are from approved OIDs

## Quick Lookup Tips

1. **Document Level**: Always starts with `2.16.840.1.113883.10.20.22.1.x`
2. **Section Level**: Usually `2.16.840.1.113883.10.20.22.2.x`
3. **Entry Level**: Usually `2.16.840.1.113883.10.20.22.4.x`
4. **Code Systems**: All start with `2.16.840.1.113883.6.x`
5. **HL7 Vocabulary**: `2.16.840.1.113883.5.x` for HL7 tables

## Additional Resources

- [HL7 OID Registry](http://www.hl7.org/oid/index.cfm)
- [Art-Decor Template Browser](https://art-decor.org/art-decor/decor-templates)
- [Value Set Authority Center (VSAC)](https://vsac.nlm.nih.gov/)

## Notes

- OIDs must be globally unique
- Never create your own OIDs for standard elements
- Template IDs (dates) indicate the version of the template
- Code system OIDs are stable, but value sets can evolve
- Always use official OIDs from HL7 specifications
