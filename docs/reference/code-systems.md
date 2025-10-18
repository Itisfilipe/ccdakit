# Code Systems Reference

**Last Updated**: 2025-10-17
**Version**: v0.1.0-alpha
**Total Systems**: 51

This document provides a comprehensive reference of all code systems supported by ccdakit, including their OIDs, descriptions, and usage guidelines.

---

## Overview

ccdakit supports 51 healthcare code systems commonly used in C-CDA documents. These systems are organized into categories and provide automatic OID lookup, format validation, and metadata retrieval through the `CodeSystemRegistry` utility class.

---

## Quick Reference

### Using Code Systems

```python
from ccdakit.builders.common import Code
from ccdakit.utils.code_systems import CodeSystemRegistry

# Create a code using system name (automatic OID lookup)
code = Code(
    code="8867-4",
    system="LOINC",
    display_name="Heart rate"
)

# Get OID for a system
oid = CodeSystemRegistry.get_oid("LOINC")  # Returns "2.16.840.1.113883.6.1"

# Get system name from OID
name = CodeSystemRegistry.get_name("2.16.840.1.113883.6.1")  # Returns "LOINC"

# Validate code format
is_valid = CodeSystemRegistry.validate_code_format("8867-4", "LOINC")  # Returns True

# Get system metadata
info = CodeSystemRegistry.get_system_info("LOINC")
# Returns: {
#     "oid": "2.16.840.1.113883.6.1",
#     "name": "Logical Observation Identifiers Names and Codes",
#     "description": "...",
#     "url": "https://loinc.org",
#     "format_pattern": r"^\d{1,5}-\d$"
# }

# List all systems
systems = CodeSystemRegistry.list_systems()

# Get systems grouped by category
categories = CodeSystemRegistry.get_systems_by_category()
```

---

## Clinical Terminology Systems

### LOINC
- **OID**: `2.16.840.1.113883.6.1`
- **Full Name**: Logical Observation Identifiers Names and Codes
- **Description**: International standard for identifying medical laboratory observations
- **URL**: https://loinc.org
- **Format**: `#####-#` (e.g., `8867-4`)
- **Common Uses**: Lab results, vital signs, clinical observations
- **Example**: `8867-4` (Heart rate)

### SNOMED CT
- **OID**: `2.16.840.1.113883.6.96`
- **Full Name**: Systematized Nomenclature of Medicine Clinical Terms
- **Description**: Comprehensive clinical terminology covering diseases, findings, procedures, microorganisms, substances, etc.
- **URL**: https://www.snomed.org
- **Format**: 6-18 digit numeric code (e.g., `73211009`)
- **Common Uses**: Problems, diagnoses, procedures, body sites, allergies
- **Example**: `73211009` (Diabetes mellitus)

### RxNorm
- **OID**: `2.16.840.1.113883.6.88`
- **Full Name**: RxNorm
- **Description**: Normalized naming system for generic and branded drugs
- **URL**: https://www.nlm.nih.gov/research/umls/rxnorm
- **Format**: Numeric (e.g., `197361`)
- **Common Uses**: Medications, drug products, clinical drugs
- **Example**: `197361` (Aspirin 81 MG Oral Tablet)

### ICD-10
- **OID**: `2.16.840.1.113883.6.90`
- **Full Name**: International Classification of Diseases, 10th Revision
- **Description**: WHO's classification of diseases and health conditions
- **URL**: https://www.who.int/classifications/icd
- **Format**: Letter followed by 2 digits, optional decimal and 1-4 more digits (e.g., `I10`, `E11.9`)
- **Common Uses**: Diagnoses, conditions, mortality reporting
- **Example**: `I10` (Essential hypertension)

### ICD-10-CM
- **OID**: `2.16.840.1.113883.6.90`
- **Full Name**: International Classification of Diseases, 10th Revision, Clinical Modification
- **Description**: US clinical modification of ICD-10 for morbidity classification
- **URL**: https://www.cdc.gov/nchs/icd/icd10cm.htm
- **Format**: Same as ICD-10 (e.g., `E11.65`)
- **Common Uses**: Diagnoses in US healthcare settings
- **Example**: `E11.65` (Type 2 diabetes with hyperglycemia)

### ICD-10-PCS
- **OID**: `2.16.840.1.113883.6.4`
- **Full Name**: International Classification of Diseases, 10th Revision, Procedure Coding System
- **Description**: US procedural classification for inpatient procedures
- **URL**: https://www.cms.gov/Medicare/Coding/ICD10
- **Format**: 7 alphanumeric characters (excludes I and O) (e.g., `0W9G30Z`)
- **Common Uses**: Inpatient procedures
- **Example**: `0DT60ZZ` (Resection of stomach)

### ICD-9-CM
- **OID**: `2.16.840.1.113883.6.103`
- **Full Name**: International Classification of Diseases, 9th Revision, Clinical Modification
- **Description**: Legacy diagnosis coding system (replaced by ICD-10-CM in 2015)
- **URL**: https://www.cdc.gov/nchs/icd/icd9cm.htm
- **Format**: 3-5 characters (e.g., `250.00`, `V01.0`, `E800`)
- **Common Uses**: Historical diagnoses
- **Example**: `250.00` (Diabetes mellitus without mention of complication)

### ICD-9-PCS
- **OID**: `2.16.840.1.113883.6.104`
- **Full Name**: International Classification of Diseases, 9th Revision, Procedure Coding System
- **Description**: Legacy procedure coding system
- **URL**: https://www.cms.gov/Medicare/Coding/ICD9ProviderDiagnosticCodes
- **Format**: 2-4 digits with optional decimal (e.g., `01.23`)
- **Common Uses**: Historical procedures
- **Example**: `99.04` (Transfusion of packed cells)

### CPT
- **OID**: `2.16.840.1.113883.6.12`
- **Full Name**: Current Procedural Terminology
- **Description**: Medical procedure coding system maintained by AMA
- **URL**: https://www.ama-assn.org/practice-management/cpt
- **Format**: 5 digits, optional letter suffix (e.g., `99213`, `99213F`)
- **Common Uses**: Procedures, services, evaluation and management
- **Example**: `99213` (Office visit, established patient)

### CVX
- **OID**: `2.16.840.1.113883.12.292`
- **Full Name**: CVX - Vaccines Administered
- **Description**: CDC code set for vaccines
- **URL**: https://www2.cdc.gov/vaccines/iis/iisstandards/vaccines.asp
- **Format**: 1-3 digit numeric (e.g., `08`, `140`)
- **Common Uses**: Immunizations
- **Example**: `08` (Hepatitis B vaccine)

### NDC
- **OID**: `2.16.840.1.113883.6.69`
- **Full Name**: National Drug Code
- **Description**: FDA code identifying drug products
- **URL**: https://www.fda.gov/drugs/development-approval-process-drugs/national-drug-code-directory
- **Format**: Segmented numeric (e.g., `0002-1234-01`)
- **Common Uses**: Drug identification, pharmacy claims
- **Example**: `0002-1234-01` (Specific drug package)

### HCPCS
- **OID**: `2.16.840.1.113883.6.285`
- **Full Name**: Healthcare Common Procedure Coding System
- **Description**: Codes for medical procedures, supplies, and services
- **URL**: https://www.cms.gov/Medicare/Coding/MedHCPCSGenInfo
- **Format**: Letter followed by 4 digits (e.g., `J1234`)
- **Common Uses**: DME, drugs, supplies, Level II procedures
- **Example**: `J1234` (Injection, drug name)

### NCI Thesaurus
- **OID**: `2.16.840.1.113883.3.26.1.1`
- **Full Name**: National Cancer Institute Thesaurus
- **Description**: Cancer-focused terminology
- **URL**: https://ncithesaurus.nci.nih.gov
- **Format**: Letter C followed by digits (e.g., `C1234`)
- **Common Uses**: Cancer-related concepts, dose forms
- **Example**: `C42998` (Tablet)

### UNII
- **OID**: `2.16.840.1.113883.4.9`
- **Full Name**: Unique Ingredient Identifier
- **Description**: FDA unique identifier for substance ingredients
- **URL**: https://www.fda.gov/industry/structured-product-labeling-resources/unique-ingredient-identifier-unii
- **Format**: 10 alphanumeric characters (e.g., `ABC1234DEF`)
- **Common Uses**: Drug ingredients, substances
- **Example**: `R16CO5Y76E` (Aspirin)

---

## Units of Measure

### UCUM
- **OID**: `2.16.840.1.113883.6.8`
- **Full Name**: Unified Code for Units of Measure
- **Description**: Standard for representing units of measure
- **URL**: https://ucum.org
- **Format**: Variable (e.g., `mg`, `mL`, `kg/m2`)
- **Common Uses**: Lab results, vital signs, measurements
- **Example**: `mg/dL` (Milligrams per deciliter)

---

## HL7 Vocabulary Systems

### HL7
- **OID**: `2.16.840.1.113883.5.1`
- **Description**: HL7 Vocabulary Domain
- **Common Uses**: Base HL7 vocabulary

### ActClass
- **OID**: `2.16.840.1.113883.5.6`
- **Description**: HL7 Act Class
- **Common Uses**: Categorizing acts (observations, encounters, procedures)
- **Example**: `OBS` (Observation), `ENC` (Encounter)

### ActCode
- **OID**: `2.16.840.1.113883.5.4`
- **Description**: HL7 Act Code
- **Common Uses**: Specific act types
- **Example**: `AMB` (Ambulatory)

### ActMood
- **OID**: `2.16.840.1.113883.5.1001`
- **Description**: HL7 Act Mood
- **Common Uses**: Intent or mode of an act
- **Example**: `EVN` (Event), `INT` (Intent)

### ActStatus
- **OID**: `2.16.840.1.113883.5.14`
- **Description**: HL7 Act Status
- **Common Uses**: Status of clinical acts
- **Example**: `active`, `completed`, `aborted`

### ObservationInterpretation
- **OID**: `2.16.840.1.113883.5.83`
- **Description**: HL7 Observation Interpretation
- **Common Uses**: Lab result interpretations
- **Example**: `H` (High), `L` (Low), `N` (Normal)

### ParticipationType
- **OID**: `2.16.840.1.113883.5.90`
- **Description**: HL7 Participation Type
- **Common Uses**: Role of participants in acts
- **Example**: `AUT` (Author), `PRF` (Performer)

### RoleClass
- **OID**: `2.16.840.1.113883.5.110`
- **Description**: HL7 Role Class
- **Common Uses**: Categorizing roles
- **Example**: `PAT` (Patient), `PROV` (Provider)

### EntityNameUse
- **OID**: `2.16.840.1.113883.5.45`
- **Description**: HL7 Entity Name Use
- **Common Uses**: Purpose of a name
- **Example**: `L` (Legal), `C` (License), `P` (Pseudonym)

### PostalAddressUse
- **OID**: `2.16.840.1.113883.5.1119`
- **Description**: HL7 Postal Address Use
- **Common Uses**: Type of address
- **Example**: `H` (Home), `WP` (Work Place)

### TelecomAddressUse
- **OID**: `2.16.840.1.113883.5.1119`
- **Description**: HL7 Telecom Address Use
- **Common Uses**: Type of telecommunication address
- **Example**: `HP` (Primary Home), `WP` (Work Place)

### MaritalStatus
- **OID**: `2.16.840.1.113883.5.2`
- **Description**: HL7 Marital Status
- **Common Uses**: Patient marital status
- **Example**: `M` (Married), `S` (Single)

### ReligiousAffiliation
- **OID**: `2.16.840.1.113883.5.1076`
- **Description**: HL7 Religious Affiliation
- **Common Uses**: Patient religious affiliation
- **Example**: `1001` (Adventist), `1013` (Christian)

### AdministrativeGender
- **OID**: `2.16.840.1.113883.5.1`
- **Description**: HL7 Administrative Gender
- **Common Uses**: Patient administrative gender
- **Example**: `M` (Male), `F` (Female), `UN` (Undifferentiated)

### NullFlavor
- **OID**: `2.16.840.1.113883.5.1008`
- **Description**: HL7 Null Flavor
- **Common Uses**: Indicating missing or unavailable data
- **Example**: `UNK` (Unknown), `NA` (Not Applicable), `ASKU` (Asked but Unknown)

### RouteOfAdministration
- **OID**: `2.16.840.1.113883.5.112`
- **Description**: HL7 Route of Administration
- **Common Uses**: Medication administration routes
- **Example**: `PO` (Oral), `IV` (Intravenous)

### Confidentiality
- **OID**: `2.16.840.1.113883.5.25`
- **Description**: HL7 Confidentiality
- **Common Uses**: Document confidentiality level
- **Example**: `N` (Normal), `R` (Restricted)

---

## CDC and Demographic Systems

### Race
- **OID**: `2.16.840.1.113883.6.238`
- **Full Name**: CDC Race and Ethnicity Code Set
- **Description**: CDC standardized race codes
- **URL**: https://www.cdc.gov/nchs/data/dvs/Race_Ethnicity_CodeSet.pdf
- **Format**: 4 digits, hyphen, 1 digit (e.g., `2054-5`)
- **Common Uses**: Patient demographics
- **Example**: `2054-5` (Black or African American)

### Ethnicity
- **OID**: `2.16.840.1.113883.6.238`
- **Full Name**: CDC Race and Ethnicity Code Set
- **Description**: CDC standardized ethnicity codes
- **URL**: https://www.cdc.gov/nchs/data/dvs/Race_Ethnicity_CodeSet.pdf
- **Format**: 4 digits, hyphen, 1 digit (e.g., `2135-2`)
- **Common Uses**: Patient demographics
- **Example**: `2135-2` (Hispanic or Latino)

---

## International Standards

### Language
- **OID**: `2.16.840.1.113883.6.121`
- **Full Name**: ISO 639-2 Language Codes
- **Description**: International standard for language codes
- **URL**: https://www.loc.gov/standards/iso639-2/
- **Format**: 3 lowercase letters (e.g., `eng`)
- **Common Uses**: Patient language preferences
- **Example**: `eng` (English), `spa` (Spanish)

### ISO3166
- **OID**: `1.0.3166.1.2.2`
- **Full Name**: ISO 3166 Country Codes
- **Description**: International standard for country codes
- **URL**: https://www.iso.org/iso-3166-country-codes.html
- **Format**: 2 uppercase letters (e.g., `US`)
- **Common Uses**: Country identification in addresses
- **Example**: `US` (United States), `CA` (Canada)

---

## Healthcare Facility and Billing

### NUBC
- **OID**: `2.16.840.1.113883.6.301`
- **Full Name**: National Uniform Billing Committee Revenue Codes
- **Description**: Revenue codes for hospital billing
- **URL**: https://www.nubc.org
- **Format**: 4 digits (e.g., `0450`)
- **Common Uses**: Hospital billing, revenue reporting
- **Example**: `0450` (Emergency room)

### DischargeDisposition
- **OID**: `2.16.840.1.113883.12.112`
- **Full Name**: HL7 Discharge Disposition
- **Description**: Patient discharge disposition codes
- **URL**: https://www.hl7.org/fhir/v2/0112/index.html
- **Format**: 2 digits (e.g., `01`)
- **Common Uses**: Encounter discharge status
- **Example**: `01` (Discharged to home)

### AdmitSource
- **OID**: `2.16.840.1.113883.12.23`
- **Full Name**: HL7 Admit Source
- **Description**: Patient admission source codes
- **URL**: https://www.hl7.org/fhir/v2/0023/index.html
- **Format**: 1-2 digits (e.g., `7`)
- **Common Uses**: Encounter admission source
- **Example**: `7` (Emergency room)

---

## Clinical Domain Specific

### ProcedureCode
- **OID**: `2.16.840.1.113883.6.96`
- **Description**: SNOMED CT codes for procedures
- **Common Uses**: Procedures section
- **Example**: `80146002` (Appendectomy)

### DoseForm
- **OID**: `2.16.840.1.113883.3.26.1.1`
- **Description**: NCI Thesaurus dose form codes
- **Common Uses**: Medication dose forms
- **Example**: `C42998` (Tablet)

### BodySite
- **OID**: `2.16.840.1.113883.6.96`
- **Description**: SNOMED CT body site codes
- **Common Uses**: Anatomical locations
- **Example**: `368209003` (Right arm)

### EncounterType
- **OID**: `2.16.840.1.113883.5.4`
- **Description**: HL7 Act Code encounter types
- **Common Uses**: Encounter classification
- **Example**: `AMB` (Ambulatory), `IMP` (Inpatient)

### ProblemType
- **OID**: `2.16.840.1.113883.3.88.12.3221.7.2`
- **Description**: HITSP problem type value set
- **Common Uses**: Categorizing problems
- **Example**: `55607006` (Problem), `404684003` (Finding)

### AllergyCategory
- **OID**: `2.16.840.1.113883.3.88.12.3221.6.2`
- **Description**: HITSP allergy category value set
- **Common Uses**: Categorizing allergies
- **Example**: `416098002` (Drug allergy), `414285001` (Food allergy)

### AllergySeverity
- **OID**: `2.16.840.1.113883.6.96`
- **Description**: SNOMED CT allergy severity codes
- **Common Uses**: Allergy severity
- **Example**: `255604002` (Mild), `6736007` (Moderate), `24484000` (Severe)

### ReactionSeverity
- **OID**: `2.16.840.1.113883.6.96`
- **Description**: SNOMED CT reaction severity codes
- **Common Uses**: Allergic reaction severity
- **Example**: `255604002` (Mild)

### MedicationStatus
- **OID**: `2.16.840.1.113883.3.88.12.80.20`
- **Description**: HITSP medication status value set
- **Common Uses**: Medication status
- **Example**: `55561003` (Active), `73425007` (Inactive)

### VitalSignResult
- **OID**: `2.16.840.1.113883.6.1`
- **Description**: LOINC vital sign result codes
- **Common Uses**: Vital signs observations
- **Example**: `8867-4` (Heart rate), `8480-6` (Systolic blood pressure)

### LabResultStatus
- **OID**: `2.16.840.1.113883.5.14`
- **Description**: HL7 Act Status for lab results
- **Common Uses**: Lab result status
- **Example**: `completed`, `active`, `aborted`

### ResultInterpretation
- **OID**: `2.16.840.1.113883.5.83`
- **Description**: HL7 Observation Interpretation for results
- **Common Uses**: Lab result interpretation flags
- **Example**: `H` (High), `L` (Low), `N` (Normal)

### SpecimenType
- **OID**: `2.16.840.1.113883.6.96`
- **Description**: SNOMED CT specimen type codes
- **Common Uses**: Laboratory specimens
- **Example**: `119297000` (Blood specimen)

---

## Code System Statistics

| Category | Count |
|----------|-------|
| Clinical terminology systems | 14 |
| Units of measure | 1 |
| HL7 vocabulary systems | 18 |
| CDC and demographic systems | 2 |
| International standards | 2 |
| Healthcare facility and billing | 3 |
| Clinical domain specific | 14 |
| **Total** | **54** |

Note: Some systems appear in multiple categories due to overlapping OIDs or usage contexts.

---

## Format Validation

ccdakit provides automatic format validation for many code systems. Systems with defined format patterns will validate codes according to their specification:

```python
from ccdakit.utils.code_systems import CodeSystemRegistry

# Valid LOINC code
CodeSystemRegistry.validate_code_format("8867-4", "LOINC")  # True

# Invalid LOINC code (missing check digit)
CodeSystemRegistry.validate_code_format("8867", "LOINC")  # False

# Valid ICD-10 code
CodeSystemRegistry.validate_code_format("I10", "ICD-10")  # True

# Invalid ICD-10 code (wrong format)
CodeSystemRegistry.validate_code_format("123", "ICD-10")  # False
```

Systems without defined format patterns (primarily HL7 vocabulary systems) will accept any code value.

---

## Integration with Code Builder

The `Code` builder class automatically looks up OIDs from system names:

```python
from ccdakit.builders.common import Code

# Using system name - OID is looked up automatically
code = Code(
    code="8867-4",
    system="LOINC",  # Automatically converts to OID 2.16.840.1.113883.6.1
    display_name="Heart rate"
)

# Using OID directly (also supported)
code = Code(
    code="8867-4",
    system="2.16.840.1.113883.6.1",
    display_name="Heart rate"
)
```

---

## Migration from Previous Versions

### v0.1.0-alpha to Current

Previous version supported 9 code systems. This update adds 42 additional systems:

**New Systems Added**:
- ICD-10-PCS, ICD-9-CM, ICD-9-PCS (Legacy coding)
- NDC, HCPCS (Drug and procedure coding)
- NCI Thesaurus, UNII (Substance identification)
- 15 additional HL7 vocabulary systems
- Race, Ethnicity (CDC demographics)
- Language, ISO3166 (International standards)
- NUBC, DischargeDisposition, AdmitSource (Facility and billing)
- 14 clinical domain-specific systems

**Breaking Changes**: None. All existing code systems remain supported with the same OIDs.

---

## Additional Resources

- [HL7 C-CDA Implementation Guide](http://www.hl7.org/implement/standards/product_brief.cfm?product_id=492)
- [HL7 Vocabulary Services](https://www.hl7.org/fhir/terminologies.html)
- [ONC Code Systems](https://www.healthit.gov/isa/terminology-standards)
- [VSAC Value Set Authority Center](https://vsac.nlm.nih.gov/)

---

## Contributing

To add a new code system:

1. Add entry to `SYSTEMS` dict in `ccdakit/utils/code_systems.py`
2. Add entry to `SYSTEM_OIDS` dict in `ccdakit/builders/common.py`
3. Add format validation pattern (if applicable)
4. Add test cases in `tests/test_utils/test_code_systems.py`
5. Update this documentation
6. Add to appropriate category in `get_systems_by_category()`

---

**Maintained by**: ccdakit Development Team
**Questions?**: See [CONTRIBUTING.md](./CONTRIBUTING.md)
