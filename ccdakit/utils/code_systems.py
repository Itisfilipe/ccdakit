"""Code system registry and utilities for C-CDA code systems."""

import re
from typing import Optional


class CodeSystemRegistry:
    """
    Central registry for code systems with metadata.

    This class provides utilities for working with healthcare code systems,
    including OID lookup, reverse lookup, format validation, and metadata retrieval.
    """

    # Complete registry of code systems with OIDs and metadata
    SYSTEMS = {
        # Clinical terminology systems
        "LOINC": {
            "oid": "2.16.840.1.113883.6.1",
            "name": "Logical Observation Identifiers Names and Codes",
            "description": "International standard for identifying medical laboratory observations",
            "url": "https://loinc.org",
            "format_pattern": r"^\d{1,5}-\d$",
        },
        "SNOMED": {
            "oid": "2.16.840.1.113883.6.96",
            "name": "SNOMED CT",
            "description": "Systematized Nomenclature of Medicine Clinical Terms",
            "url": "https://www.snomed.org",
            "format_pattern": r"^\d{6,18}$",
        },
        "RxNorm": {
            "oid": "2.16.840.1.113883.6.88",
            "name": "RxNorm",
            "description": "Normalized naming system for generic and branded drugs",
            "url": "https://www.nlm.nih.gov/research/umls/rxnorm",
            "format_pattern": r"^\d+$",
        },
        "ICD-10": {
            "oid": "2.16.840.1.113883.6.90",
            "name": "ICD-10",
            "description": "International Classification of Diseases, 10th Revision",
            "url": "https://www.who.int/classifications/icd",
            "format_pattern": r"^[A-Z]\d{2}(\.\d{1,4})?$",
        },
        "ICD-10-CM": {
            "oid": "2.16.840.1.113883.6.90",
            "name": "ICD-10-CM",
            "description": "International Classification of Diseases, 10th Revision, Clinical Modification",
            "url": "https://www.cdc.gov/nchs/icd/icd10cm.htm",
            "format_pattern": r"^[A-Z]\d{2}(\.\d{1,4})?$",
        },
        "ICD-10-PCS": {
            "oid": "2.16.840.1.113883.6.4",
            "name": "ICD-10-PCS",
            "description": "International Classification of Diseases, 10th Revision, Procedure Coding System",
            "url": "https://www.cms.gov/Medicare/Coding/ICD10",
            "format_pattern": r"^[0-9A-HJ-NP-Z]{7}$",
        },
        "ICD-9-CM": {
            "oid": "2.16.840.1.113883.6.103",
            "name": "ICD-9-CM",
            "description": "International Classification of Diseases, 9th Revision, Clinical Modification",
            "url": "https://www.cdc.gov/nchs/icd/icd9cm.htm",
            "format_pattern": r"^(\d{3}(\.\d{1,2})?|[EV]\d{2,3}(\.\d{1,2})?)$",
        },
        "ICD-9-PCS": {
            "oid": "2.16.840.1.113883.6.104",
            "name": "ICD-9-PCS",
            "description": "International Classification of Diseases, 9th Revision, Procedure Coding System",
            "url": "https://www.cms.gov/Medicare/Coding/ICD9ProviderDiagnosticCodes",
            "format_pattern": r"^\d{2}(\.\d{1,2})?$",
        },
        "CPT": {
            "oid": "2.16.840.1.113883.6.12",
            "name": "CPT",
            "description": "Current Procedural Terminology",
            "url": "https://www.ama-assn.org/practice-management/cpt",
            "format_pattern": r"^\d{5}[A-Z]?$",
        },
        "CVX": {
            "oid": "2.16.840.1.113883.12.292",
            "name": "CVX",
            "description": "CDC Vaccine Administered Code Set",
            "url": "https://www2.cdc.gov/vaccines/iis/iisstandards/vaccines.asp",
            "format_pattern": r"^\d{1,3}$",
        },
        "NDC": {
            "oid": "2.16.840.1.113883.6.69",
            "name": "NDC",
            "description": "National Drug Code",
            "url": "https://www.fda.gov/drugs/development-approval-process-drugs/national-drug-code-directory",
            "format_pattern": r"^\d{4,5}-\d{3,4}-\d{1,2}$",
        },
        "HCPCS": {
            "oid": "2.16.840.1.113883.6.285",
            "name": "HCPCS",
            "description": "Healthcare Common Procedure Coding System",
            "url": "https://www.cms.gov/Medicare/Coding/MedHCPCSGenInfo",
            "format_pattern": r"^[A-Z]\d{4}$",
        },
        "NCI": {
            "oid": "2.16.840.1.113883.3.26.1.1",
            "name": "NCI Thesaurus",
            "description": "National Cancer Institute Thesaurus",
            "url": "https://ncithesaurus.nci.nih.gov",
            "format_pattern": r"^C\d+$",
        },
        "UNII": {
            "oid": "2.16.840.1.113883.4.9",
            "name": "UNII",
            "description": "Unique Ingredient Identifier",
            "url": "https://www.fda.gov/industry/structured-product-labeling-resources/unique-ingredient-identifier-unii",
            "format_pattern": r"^[A-Z0-9]{10}$",
        },
        # Units of measure
        "UCUM": {
            "oid": "2.16.840.1.113883.6.8",
            "name": "UCUM",
            "description": "Unified Code for Units of Measure",
            "url": "https://ucum.org",
            "format_pattern": None,  # Complex format, not easily validated with regex
        },
        # HL7 vocabulary systems
        "HL7": {
            "oid": "2.16.840.1.113883.5.1",
            "name": "HL7 Vocabulary",
            "description": "HL7 Vocabulary Domain",
            "url": "https://www.hl7.org/fhir/terminologies.html",
            "format_pattern": None,
        },
        "ActClass": {
            "oid": "2.16.840.1.113883.5.6",
            "name": "ActClass",
            "description": "HL7 Act Class",
            "url": "https://www.hl7.org/fhir/v3/ActClass/vs.html",
            "format_pattern": None,
        },
        "ActCode": {
            "oid": "2.16.840.1.113883.5.4",
            "name": "ActCode",
            "description": "HL7 Act Code",
            "url": "https://www.hl7.org/fhir/v3/ActCode/vs.html",
            "format_pattern": None,
        },
        "ActMood": {
            "oid": "2.16.840.1.113883.5.1001",
            "name": "ActMood",
            "description": "HL7 Act Mood",
            "url": "https://www.hl7.org/fhir/v3/ActMood/vs.html",
            "format_pattern": None,
        },
        "ActStatus": {
            "oid": "2.16.840.1.113883.5.14",
            "name": "ActStatus",
            "description": "HL7 Act Status",
            "url": "https://www.hl7.org/fhir/v3/ActStatus/vs.html",
            "format_pattern": None,
        },
        "ObservationInterpretation": {
            "oid": "2.16.840.1.113883.5.83",
            "name": "ObservationInterpretation",
            "description": "HL7 Observation Interpretation",
            "url": "https://www.hl7.org/fhir/v3/ObservationInterpretation/vs.html",
            "format_pattern": None,
        },
        "ParticipationType": {
            "oid": "2.16.840.1.113883.5.90",
            "name": "ParticipationType",
            "description": "HL7 Participation Type",
            "url": "https://www.hl7.org/fhir/v3/ParticipationType/vs.html",
            "format_pattern": None,
        },
        "RoleClass": {
            "oid": "2.16.840.1.113883.5.110",
            "name": "RoleClass",
            "description": "HL7 Role Class",
            "url": "https://www.hl7.org/fhir/v3/RoleClass/vs.html",
            "format_pattern": None,
        },
        "EntityNameUse": {
            "oid": "2.16.840.1.113883.5.45",
            "name": "EntityNameUse",
            "description": "HL7 Entity Name Use",
            "url": "https://www.hl7.org/fhir/v3/EntityNameUse/vs.html",
            "format_pattern": None,
        },
        "PostalAddressUse": {
            "oid": "2.16.840.1.113883.5.1119",
            "name": "PostalAddressUse",
            "description": "HL7 Postal Address Use",
            "url": "https://www.hl7.org/fhir/v3/AddressUse/vs.html",
            "format_pattern": None,
        },
        "TelecomAddressUse": {
            "oid": "2.16.840.1.113883.5.1119",
            "name": "TelecomAddressUse",
            "description": "HL7 Telecom Address Use",
            "url": "https://www.hl7.org/fhir/v3/AddressUse/vs.html",
            "format_pattern": None,
        },
        "MaritalStatus": {
            "oid": "2.16.840.1.113883.5.2",
            "name": "MaritalStatus",
            "description": "HL7 Marital Status",
            "url": "https://www.hl7.org/fhir/v3/MaritalStatus/vs.html",
            "format_pattern": None,
        },
        "ReligiousAffiliation": {
            "oid": "2.16.840.1.113883.5.1076",
            "name": "ReligiousAffiliation",
            "description": "HL7 Religious Affiliation",
            "url": "https://www.hl7.org/fhir/v3/ReligiousAffiliation/vs.html",
            "format_pattern": None,
        },
        "AdministrativeGender": {
            "oid": "2.16.840.1.113883.5.1",
            "name": "AdministrativeGender",
            "description": "HL7 Administrative Gender",
            "url": "https://www.hl7.org/fhir/v3/AdministrativeGender/vs.html",
            "format_pattern": None,
        },
        "NullFlavor": {
            "oid": "2.16.840.1.113883.5.1008",
            "name": "NullFlavor",
            "description": "HL7 Null Flavor",
            "url": "https://www.hl7.org/fhir/v3/NullFlavor/vs.html",
            "format_pattern": None,
        },
        # CDC and demographic systems
        "Race": {
            "oid": "2.16.840.1.113883.6.238",
            "name": "CDC Race and Ethnicity",
            "description": "CDC Race and Ethnicity Code Set",
            "url": "https://www.cdc.gov/nchs/data/dvs/Race_Ethnicity_CodeSet.pdf",
            "format_pattern": r"^\d{4}-\d$",
        },
        "Ethnicity": {
            "oid": "2.16.840.1.113883.6.238",
            "name": "CDC Race and Ethnicity",
            "description": "CDC Race and Ethnicity Code Set",
            "url": "https://www.cdc.gov/nchs/data/dvs/Race_Ethnicity_CodeSet.pdf",
            "format_pattern": r"^\d{4}-\d$",
        },
        # International standards
        "Language": {
            "oid": "2.16.840.1.113883.6.121",
            "name": "ISO 639-2",
            "description": "ISO 639-2 Language Codes",
            "url": "https://www.loc.gov/standards/iso639-2/",
            "format_pattern": r"^[a-z]{3}$",
        },
        "ISO3166": {
            "oid": "1.0.3166.1.2.2",
            "name": "ISO 3166",
            "description": "ISO 3166 Country Codes",
            "url": "https://www.iso.org/iso-3166-country-codes.html",
            "format_pattern": r"^[A-Z]{2}$",
        },
        # Healthcare facility and billing
        "NUBC": {
            "oid": "2.16.840.1.113883.6.301",
            "name": "NUBC Revenue Codes",
            "description": "National Uniform Billing Committee Revenue Codes",
            "url": "https://www.nubc.org",
            "format_pattern": r"^\d{4}$",
        },
        "DischargeDisposition": {
            "oid": "2.16.840.1.113883.12.112",
            "name": "Discharge Disposition",
            "description": "HL7 Discharge Disposition",
            "url": "https://www.hl7.org/fhir/v2/0112/index.html",
            "format_pattern": r"^\d{2}$",
        },
        "AdmitSource": {
            "oid": "2.16.840.1.113883.12.23",
            "name": "Admit Source",
            "description": "HL7 Admit Source",
            "url": "https://www.hl7.org/fhir/v2/0023/index.html",
            "format_pattern": r"^\d{1,2}$",
        },
        "ProcedureCode": {
            "oid": "2.16.840.1.113883.6.96",
            "name": "SNOMED CT Procedure Codes",
            "description": "SNOMED CT codes for procedures",
            "url": "https://www.snomed.org",
            "format_pattern": r"^\d{6,18}$",
        },
        # Additional HL7 vocabulary
        "RouteOfAdministration": {
            "oid": "2.16.840.1.113883.5.112",
            "name": "RouteOfAdministration",
            "description": "HL7 Route of Administration",
            "url": "https://www.hl7.org/fhir/v3/RouteOfAdministration/vs.html",
            "format_pattern": None,
        },
        "DoseForm": {
            "oid": "2.16.840.1.113883.3.26.1.1",
            "name": "Dose Form",
            "description": "NCI Thesaurus Dose Form codes",
            "url": "https://ncithesaurus.nci.nih.gov",
            "format_pattern": r"^C\d+$",
        },
        "BodySite": {
            "oid": "2.16.840.1.113883.6.96",
            "name": "Body Site",
            "description": "SNOMED CT Body Site codes",
            "url": "https://www.snomed.org",
            "format_pattern": r"^\d{6,18}$",
        },
        "Confidentiality": {
            "oid": "2.16.840.1.113883.5.25",
            "name": "Confidentiality",
            "description": "HL7 Confidentiality",
            "url": "https://www.hl7.org/fhir/v3/Confidentiality/vs.html",
            "format_pattern": None,
        },
        "EncounterType": {
            "oid": "2.16.840.1.113883.5.4",
            "name": "Encounter Type",
            "description": "HL7 Act Code - Encounter Types",
            "url": "https://www.hl7.org/fhir/v3/ActCode/vs.html",
            "format_pattern": None,
        },
        "ProblemType": {
            "oid": "2.16.840.1.113883.3.88.12.3221.7.2",
            "name": "Problem Type",
            "description": "HITSP Problem Type Value Set",
            "url": "http://www.hl7.org/implement/standards/product_brief.cfm?product_id=6",
            "format_pattern": None,
        },
        "AllergyCategory": {
            "oid": "2.16.840.1.113883.3.88.12.3221.6.2",
            "name": "Allergy Category",
            "description": "HITSP Allergy Category Value Set",
            "url": "http://www.hl7.org/implement/standards/product_brief.cfm?product_id=6",
            "format_pattern": None,
        },
        "AllergySeverity": {
            "oid": "2.16.840.1.113883.6.96",
            "name": "Allergy Severity",
            "description": "SNOMED CT Allergy Severity codes",
            "url": "https://www.snomed.org",
            "format_pattern": r"^\d{6,18}$",
        },
        "ReactionSeverity": {
            "oid": "2.16.840.1.113883.6.96",
            "name": "Reaction Severity",
            "description": "SNOMED CT Reaction Severity codes",
            "url": "https://www.snomed.org",
            "format_pattern": r"^\d{6,18}$",
        },
        "MedicationStatus": {
            "oid": "2.16.840.1.113883.3.88.12.80.20",
            "name": "Medication Status",
            "description": "HITSP Medication Status Value Set",
            "url": "http://www.hl7.org/implement/standards/product_brief.cfm?product_id=6",
            "format_pattern": None,
        },
        "VitalSignResult": {
            "oid": "2.16.840.1.113883.6.1",
            "name": "Vital Sign Result",
            "description": "LOINC Vital Sign Result codes",
            "url": "https://loinc.org",
            "format_pattern": r"^\d{1,5}-\d$",
        },
        "LabResultStatus": {
            "oid": "2.16.840.1.113883.5.14",
            "name": "Lab Result Status",
            "description": "HL7 Act Status for Lab Results",
            "url": "https://www.hl7.org/fhir/v3/ActStatus/vs.html",
            "format_pattern": None,
        },
        "ResultInterpretation": {
            "oid": "2.16.840.1.113883.5.83",
            "name": "Result Interpretation",
            "description": "HL7 Observation Interpretation for Results",
            "url": "https://www.hl7.org/fhir/v3/ObservationInterpretation/vs.html",
            "format_pattern": None,
        },
        "SpecimenType": {
            "oid": "2.16.840.1.113883.6.96",
            "name": "Specimen Type",
            "description": "SNOMED CT Specimen Type codes",
            "url": "https://www.snomed.org",
            "format_pattern": r"^\d{6,18}$",
        },
    }

    @staticmethod
    def get_oid(name: str) -> Optional[str]:
        """
        Get OID for code system name.

        Args:
            name: Code system name (e.g., "LOINC", "SNOMED")

        Returns:
            OID string if found, None otherwise

        Example:
            >>> CodeSystemRegistry.get_oid("LOINC")
            '2.16.840.1.113883.6.1'
        """
        system = CodeSystemRegistry.SYSTEMS.get(name)
        return system["oid"] if system else None

    @staticmethod
    def get_name(oid: str) -> Optional[str]:
        """
        Get code system name from OID.

        Args:
            oid: OID string (e.g., "2.16.840.1.113883.6.1")

        Returns:
            Code system name if found, None otherwise

        Example:
            >>> CodeSystemRegistry.get_name("2.16.840.1.113883.6.1")
            'LOINC'
        """
        for name, info in CodeSystemRegistry.SYSTEMS.items():
            if info["oid"] == oid:
                return name
        return None

    @staticmethod
    def validate_code_format(code: str, system: str) -> bool:
        """
        Validate code format for specific system.

        Args:
            code: Code value to validate
            system: Code system name

        Returns:
            True if code matches expected format, False otherwise
            Returns True if no format pattern is defined for the system

        Example:
            >>> CodeSystemRegistry.validate_code_format("12345-6", "LOINC")
            True
            >>> CodeSystemRegistry.validate_code_format("invalid", "LOINC")
            False
        """
        system_info = CodeSystemRegistry.SYSTEMS.get(system)
        if not system_info:
            return False

        pattern = system_info.get("format_pattern")
        if pattern is None:
            # No pattern defined, consider valid
            return True

        return bool(re.match(pattern, code))

    @staticmethod
    def get_system_info(system: str) -> Optional[dict]:
        """
        Get metadata about a code system.

        Args:
            system: Code system name

        Returns:
            Dictionary with system metadata (oid, name, description, url, format_pattern)
            Returns None if system not found

        Example:
            >>> info = CodeSystemRegistry.get_system_info("LOINC")
            >>> info["description"]
            'International standard for identifying medical laboratory observations'
        """
        return CodeSystemRegistry.SYSTEMS.get(system)

    @staticmethod
    def list_systems() -> "list[str]":
        """
        Get list of all supported code system names.

        Returns:
            List of code system names

        Example:
            >>> systems = CodeSystemRegistry.list_systems()
            >>> "LOINC" in systems
            True
        """
        return list(CodeSystemRegistry.SYSTEMS.keys())

    @staticmethod
    def get_systems_by_category() -> "dict[str, list[str]]":
        """
        Get code systems grouped by category.

        Returns:
            Dictionary mapping category names to lists of system names

        Example:
            >>> categories = CodeSystemRegistry.get_systems_by_category()
            >>> "LOINC" in categories["Clinical terminology systems"]
            True
        """
        categories = {
            "Clinical terminology systems": [
                "LOINC",
                "SNOMED",
                "RxNorm",
                "ICD-10",
                "ICD-10-CM",
                "ICD-10-PCS",
                "ICD-9-CM",
                "ICD-9-PCS",
                "CPT",
                "CVX",
                "NDC",
                "HCPCS",
                "NCI",
                "UNII",
            ],
            "Units of measure": ["UCUM"],
            "HL7 vocabulary systems": [
                "HL7",
                "ActClass",
                "ActCode",
                "ActMood",
                "ActStatus",
                "ObservationInterpretation",
                "ParticipationType",
                "RoleClass",
                "EntityNameUse",
                "PostalAddressUse",
                "TelecomAddressUse",
                "MaritalStatus",
                "ReligiousAffiliation",
                "AdministrativeGender",
                "NullFlavor",
                "RouteOfAdministration",
                "Confidentiality",
            ],
            "CDC and demographic systems": ["Race", "Ethnicity"],
            "International standards": ["Language", "ISO3166"],
            "Healthcare facility and billing": [
                "NUBC",
                "DischargeDisposition",
                "AdmitSource",
            ],
            "Clinical domain specific": [
                "ProcedureCode",
                "DoseForm",
                "BodySite",
                "EncounterType",
                "ProblemType",
                "AllergyCategory",
                "AllergySeverity",
                "ReactionSeverity",
                "MedicationStatus",
                "VitalSignResult",
                "LabResultStatus",
                "ResultInterpretation",
                "SpecimenType",
            ],
        }
        return categories
