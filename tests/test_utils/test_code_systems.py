"""Tests for code system registry and utilities."""

from ccdakit.utils.code_systems import CodeSystemRegistry


class TestCodeSystemRegistry:
    """Test suite for CodeSystemRegistry class."""

    def test_get_oid_valid_system(self):
        """Test getting OID for valid system name."""
        oid = CodeSystemRegistry.get_oid("LOINC")
        assert oid == "2.16.840.1.113883.6.1"

        oid = CodeSystemRegistry.get_oid("SNOMED")
        assert oid == "2.16.840.1.113883.6.96"

        oid = CodeSystemRegistry.get_oid("RxNorm")
        assert oid == "2.16.840.1.113883.6.88"

    def test_get_oid_invalid_system(self):
        """Test getting OID for invalid system name returns None."""
        oid = CodeSystemRegistry.get_oid("INVALID_SYSTEM")
        assert oid is None

    def test_get_oid_all_systems(self):
        """Test getting OID for all registered systems."""
        for system_name in CodeSystemRegistry.SYSTEMS.keys():
            oid = CodeSystemRegistry.get_oid(system_name)
            assert oid is not None
            assert isinstance(oid, str)
            assert len(oid) > 0

    def test_get_name_valid_oid(self):
        """Test getting system name for valid OID."""
        name = CodeSystemRegistry.get_name("2.16.840.1.113883.6.1")
        assert name == "LOINC"

        name = CodeSystemRegistry.get_name("2.16.840.1.113883.6.96")
        assert name == "SNOMED"

        name = CodeSystemRegistry.get_name("2.16.840.1.113883.6.88")
        assert name == "RxNorm"

    def test_get_name_invalid_oid(self):
        """Test getting system name for invalid OID returns None."""
        name = CodeSystemRegistry.get_name("9.9.9.9.9.9")
        assert name is None

    def test_get_name_all_oids(self):
        """Test getting system name for all registered OIDs."""
        for system_name, system_info in CodeSystemRegistry.SYSTEMS.items():
            oid = system_info["oid"]
            retrieved_name = CodeSystemRegistry.get_name(oid)
            # Note: Some systems may share OIDs (e.g., ICD-10 and ICD-10-CM)
            assert retrieved_name is not None
            assert isinstance(retrieved_name, str)

    def test_validate_code_format_loinc_valid(self):
        """Test validating valid LOINC codes."""
        assert CodeSystemRegistry.validate_code_format("12345-6", "LOINC")
        assert CodeSystemRegistry.validate_code_format("8867-4", "LOINC")
        assert CodeSystemRegistry.validate_code_format("1-0", "LOINC")

    def test_validate_code_format_loinc_invalid(self):
        """Test validating invalid LOINC codes."""
        assert not CodeSystemRegistry.validate_code_format("12345", "LOINC")
        assert not CodeSystemRegistry.validate_code_format("INVALID", "LOINC")
        assert not CodeSystemRegistry.validate_code_format("123456-7", "LOINC")

    def test_validate_code_format_snomed_valid(self):
        """Test validating valid SNOMED codes."""
        assert CodeSystemRegistry.validate_code_format("123456", "SNOMED")
        assert CodeSystemRegistry.validate_code_format("73211009", "SNOMED")
        assert CodeSystemRegistry.validate_code_format("123456789012345678", "SNOMED")

    def test_validate_code_format_snomed_invalid(self):
        """Test validating invalid SNOMED codes."""
        assert not CodeSystemRegistry.validate_code_format("12345", "SNOMED")
        assert not CodeSystemRegistry.validate_code_format("INVALID", "SNOMED")
        assert not CodeSystemRegistry.validate_code_format("1234567890123456789", "SNOMED")

    def test_validate_code_format_icd10_valid(self):
        """Test validating valid ICD-10 codes."""
        assert CodeSystemRegistry.validate_code_format("A00", "ICD-10")
        assert CodeSystemRegistry.validate_code_format("A00.0", "ICD-10")
        assert CodeSystemRegistry.validate_code_format("Z99.89", "ICD-10")
        assert CodeSystemRegistry.validate_code_format("I10", "ICD-10")

    def test_validate_code_format_icd10_invalid(self):
        """Test validating invalid ICD-10 codes."""
        assert not CodeSystemRegistry.validate_code_format("00", "ICD-10")
        assert not CodeSystemRegistry.validate_code_format("A", "ICD-10")
        assert not CodeSystemRegistry.validate_code_format("AAA", "ICD-10")
        assert not CodeSystemRegistry.validate_code_format("123", "ICD-10")

    def test_validate_code_format_icd9_cm_valid(self):
        """Test validating valid ICD-9-CM codes."""
        assert CodeSystemRegistry.validate_code_format("250", "ICD-9-CM")
        assert CodeSystemRegistry.validate_code_format("250.00", "ICD-9-CM")
        assert CodeSystemRegistry.validate_code_format("E800", "ICD-9-CM")
        assert CodeSystemRegistry.validate_code_format("V01.0", "ICD-9-CM")

    def test_validate_code_format_icd9_cm_invalid(self):
        """Test validating invalid ICD-9-CM codes."""
        assert not CodeSystemRegistry.validate_code_format("25", "ICD-9-CM")
        assert not CodeSystemRegistry.validate_code_format("2500", "ICD-9-CM")
        assert not CodeSystemRegistry.validate_code_format("X00", "ICD-9-CM")

    def test_validate_code_format_cpt_valid(self):
        """Test validating valid CPT codes."""
        assert CodeSystemRegistry.validate_code_format("99213", "CPT")
        assert CodeSystemRegistry.validate_code_format("99213F", "CPT")
        assert CodeSystemRegistry.validate_code_format("12345", "CPT")

    def test_validate_code_format_cpt_invalid(self):
        """Test validating invalid CPT codes."""
        assert not CodeSystemRegistry.validate_code_format("9921", "CPT")
        assert not CodeSystemRegistry.validate_code_format("992130", "CPT")
        assert not CodeSystemRegistry.validate_code_format("99213FF", "CPT")

    def test_validate_code_format_ndc_valid(self):
        """Test validating valid NDC codes."""
        assert CodeSystemRegistry.validate_code_format("0002-1234-01", "NDC")
        assert CodeSystemRegistry.validate_code_format("12345-123-12", "NDC")
        assert CodeSystemRegistry.validate_code_format("1234-1234-1", "NDC")

    def test_validate_code_format_ndc_invalid(self):
        """Test validating invalid NDC codes."""
        assert not CodeSystemRegistry.validate_code_format("123456", "NDC")
        assert not CodeSystemRegistry.validate_code_format("12-34-56", "NDC")
        assert not CodeSystemRegistry.validate_code_format("INVALID", "NDC")

    def test_validate_code_format_cvx_valid(self):
        """Test validating valid CVX codes."""
        assert CodeSystemRegistry.validate_code_format("1", "CVX")
        assert CodeSystemRegistry.validate_code_format("10", "CVX")
        assert CodeSystemRegistry.validate_code_format("100", "CVX")

    def test_validate_code_format_cvx_invalid(self):
        """Test validating invalid CVX codes."""
        assert not CodeSystemRegistry.validate_code_format("1000", "CVX")
        assert not CodeSystemRegistry.validate_code_format("INVALID", "CVX")
        assert not CodeSystemRegistry.validate_code_format("", "CVX")

    def test_validate_code_format_hcpcs_valid(self):
        """Test validating valid HCPCS codes."""
        assert CodeSystemRegistry.validate_code_format("A0021", "HCPCS")
        assert CodeSystemRegistry.validate_code_format("J1234", "HCPCS")
        assert CodeSystemRegistry.validate_code_format("Z9999", "HCPCS")

    def test_validate_code_format_hcpcs_invalid(self):
        """Test validating invalid HCPCS codes."""
        assert not CodeSystemRegistry.validate_code_format("12345", "HCPCS")
        assert not CodeSystemRegistry.validate_code_format("A123", "HCPCS")
        assert not CodeSystemRegistry.validate_code_format("A12345", "HCPCS")

    def test_validate_code_format_nci_valid(self):
        """Test validating valid NCI Thesaurus codes."""
        assert CodeSystemRegistry.validate_code_format("C1234", "NCI")
        assert CodeSystemRegistry.validate_code_format("C12345678", "NCI")
        assert CodeSystemRegistry.validate_code_format("C1", "NCI")

    def test_validate_code_format_nci_invalid(self):
        """Test validating invalid NCI Thesaurus codes."""
        assert not CodeSystemRegistry.validate_code_format("1234", "NCI")
        assert not CodeSystemRegistry.validate_code_format("INVALID", "NCI")
        assert not CodeSystemRegistry.validate_code_format("c1234", "NCI")

    def test_validate_code_format_unii_valid(self):
        """Test validating valid UNII codes."""
        assert CodeSystemRegistry.validate_code_format("ABC1234DEF", "UNII")
        assert CodeSystemRegistry.validate_code_format("0123456789", "UNII")
        assert CodeSystemRegistry.validate_code_format("ABCDEFGHIJ", "UNII")

    def test_validate_code_format_unii_invalid(self):
        """Test validating invalid UNII codes."""
        assert not CodeSystemRegistry.validate_code_format("ABC123", "UNII")
        assert not CodeSystemRegistry.validate_code_format("ABC1234DEF1", "UNII")
        assert not CodeSystemRegistry.validate_code_format("abc1234def", "UNII")

    def test_validate_code_format_race_valid(self):
        """Test validating valid Race codes."""
        assert CodeSystemRegistry.validate_code_format("1002-5", "Race")
        assert CodeSystemRegistry.validate_code_format("2054-5", "Race")

    def test_validate_code_format_race_invalid(self):
        """Test validating invalid Race codes."""
        assert not CodeSystemRegistry.validate_code_format("1002", "Race")
        assert not CodeSystemRegistry.validate_code_format("10025", "Race")
        assert not CodeSystemRegistry.validate_code_format("INVALID", "Race")

    def test_validate_code_format_language_valid(self):
        """Test validating valid Language codes."""
        assert CodeSystemRegistry.validate_code_format("eng", "Language")
        assert CodeSystemRegistry.validate_code_format("spa", "Language")
        assert CodeSystemRegistry.validate_code_format("fra", "Language")

    def test_validate_code_format_language_invalid(self):
        """Test validating invalid Language codes."""
        assert not CodeSystemRegistry.validate_code_format("en", "Language")
        assert not CodeSystemRegistry.validate_code_format("english", "Language")
        assert not CodeSystemRegistry.validate_code_format("ENG", "Language")

    def test_validate_code_format_iso3166_valid(self):
        """Test validating valid ISO 3166 country codes."""
        assert CodeSystemRegistry.validate_code_format("US", "ISO3166")
        assert CodeSystemRegistry.validate_code_format("GB", "ISO3166")
        assert CodeSystemRegistry.validate_code_format("CA", "ISO3166")

    def test_validate_code_format_iso3166_invalid(self):
        """Test validating invalid ISO 3166 country codes."""
        assert not CodeSystemRegistry.validate_code_format("USA", "ISO3166")
        assert not CodeSystemRegistry.validate_code_format("us", "ISO3166")
        assert not CodeSystemRegistry.validate_code_format("1", "ISO3166")

    def test_validate_code_format_nubc_valid(self):
        """Test validating valid NUBC revenue codes."""
        assert CodeSystemRegistry.validate_code_format("0100", "NUBC")
        assert CodeSystemRegistry.validate_code_format("0450", "NUBC")

    def test_validate_code_format_nubc_invalid(self):
        """Test validating invalid NUBC revenue codes."""
        assert not CodeSystemRegistry.validate_code_format("100", "NUBC")
        assert not CodeSystemRegistry.validate_code_format("01000", "NUBC")
        assert not CodeSystemRegistry.validate_code_format("INVALID", "NUBC")

    def test_validate_code_format_no_pattern(self):
        """Test validating codes for systems without format patterns."""
        # Systems without patterns should return True
        assert CodeSystemRegistry.validate_code_format("ANY", "ActClass")
        assert CodeSystemRegistry.validate_code_format("ANYTHING", "ActCode")
        assert CodeSystemRegistry.validate_code_format("123", "ActMood")

    def test_validate_code_format_invalid_system(self):
        """Test validating codes for invalid system returns False."""
        assert not CodeSystemRegistry.validate_code_format("12345", "INVALID_SYSTEM")

    def test_get_system_info_valid(self):
        """Test getting system info for valid systems."""
        info = CodeSystemRegistry.get_system_info("LOINC")
        assert info is not None
        assert info["oid"] == "2.16.840.1.113883.6.1"
        assert info["name"] == "Logical Observation Identifiers Names and Codes"
        assert "description" in info
        assert "url" in info
        assert "format_pattern" in info

    def test_get_system_info_invalid(self):
        """Test getting system info for invalid system returns None."""
        info = CodeSystemRegistry.get_system_info("INVALID_SYSTEM")
        assert info is None

    def test_get_system_info_all_systems(self):
        """Test getting system info for all registered systems."""
        for system_name in CodeSystemRegistry.SYSTEMS.keys():
            info = CodeSystemRegistry.get_system_info(system_name)
            assert info is not None
            assert "oid" in info
            assert "name" in info
            assert "description" in info
            assert "url" in info
            assert "format_pattern" in info

    def test_list_systems(self):
        """Test listing all code systems."""
        systems = CodeSystemRegistry.list_systems()
        assert isinstance(systems, list)
        assert len(systems) > 0
        assert "LOINC" in systems
        assert "SNOMED" in systems
        assert "RxNorm" in systems
        assert "ICD-10" in systems

    def test_list_systems_count(self):
        """Test that list_systems returns expected count."""
        systems = CodeSystemRegistry.list_systems()
        # Should have 50+ systems
        assert len(systems) >= 50

    def test_get_systems_by_category(self):
        """Test getting systems grouped by category."""
        categories = CodeSystemRegistry.get_systems_by_category()
        assert isinstance(categories, dict)
        assert "Clinical terminology systems" in categories
        assert "HL7 vocabulary systems" in categories
        assert "CDC and demographic systems" in categories

    def test_get_systems_by_category_clinical(self):
        """Test clinical terminology systems category."""
        categories = CodeSystemRegistry.get_systems_by_category()
        clinical = categories["Clinical terminology systems"]
        assert "LOINC" in clinical
        assert "SNOMED" in clinical
        assert "RxNorm" in clinical
        assert "ICD-10" in clinical
        assert "ICD-10-CM" in clinical
        assert "ICD-10-PCS" in clinical
        assert "NDC" in clinical

    def test_get_systems_by_category_hl7(self):
        """Test HL7 vocabulary systems category."""
        categories = CodeSystemRegistry.get_systems_by_category()
        hl7 = categories["HL7 vocabulary systems"]
        assert "ActClass" in hl7
        assert "ActCode" in hl7
        assert "ActMood" in hl7
        assert "ActStatus" in hl7
        assert "ObservationInterpretation" in hl7

    def test_get_systems_by_category_cdc(self):
        """Test CDC and demographic systems category."""
        categories = CodeSystemRegistry.get_systems_by_category()
        cdc = categories["CDC and demographic systems"]
        assert "Race" in cdc
        assert "Ethnicity" in cdc

    def test_get_systems_by_category_international(self):
        """Test international standards category."""
        categories = CodeSystemRegistry.get_systems_by_category()
        international = categories["International standards"]
        assert "Language" in international
        assert "ISO3166" in international

    def test_get_systems_by_category_billing(self):
        """Test healthcare facility and billing category."""
        categories = CodeSystemRegistry.get_systems_by_category()
        billing = categories["Healthcare facility and billing"]
        assert "NUBC" in billing
        assert "DischargeDisposition" in billing
        assert "AdmitSource" in billing

    def test_get_systems_by_category_clinical_domain(self):
        """Test clinical domain specific category."""
        categories = CodeSystemRegistry.get_systems_by_category()
        clinical_domain = categories["Clinical domain specific"]
        assert "ProcedureCode" in clinical_domain
        assert "VitalSignResult" in clinical_domain
        assert "MedicationStatus" in clinical_domain

    def test_systems_metadata_completeness(self):
        """Test that all systems have complete metadata."""
        for system_name, system_info in CodeSystemRegistry.SYSTEMS.items():
            assert "oid" in system_info, f"{system_name} missing 'oid'"
            assert "name" in system_info, f"{system_name} missing 'name'"
            assert "description" in system_info, f"{system_name} missing 'description'"
            assert "url" in system_info, f"{system_name} missing 'url'"
            assert "format_pattern" in system_info, f"{system_name} missing 'format_pattern'"

            assert isinstance(system_info["oid"], str)
            assert len(system_info["oid"]) > 0
            assert isinstance(system_info["name"], str)
            assert len(system_info["name"]) > 0
            assert isinstance(system_info["description"], str)
            assert len(system_info["description"]) > 0
            assert isinstance(system_info["url"], str)
            assert len(system_info["url"]) > 0

    def test_oid_uniqueness_check(self):
        """Test that OIDs are properly mapped (some may be shared intentionally)."""
        oid_to_systems = {}
        for system_name, system_info in CodeSystemRegistry.SYSTEMS.items():
            oid = system_info["oid"]
            if oid not in oid_to_systems:
                oid_to_systems[oid] = []
            oid_to_systems[oid].append(system_name)

        # Check that shared OIDs are intentional (e.g., ICD-10 and ICD-10-CM)
        shared_oids = {oid: systems for oid, systems in oid_to_systems.items() if len(systems) > 1}

        # These are expected to share OIDs
        expected_shared = {
            "2.16.840.1.113883.6.90": {"ICD-10", "ICD-10-CM"},
            "2.16.840.1.113883.6.238": {"Race", "Ethnicity"},
            "2.16.840.1.113883.5.1119": {"PostalAddressUse", "TelecomAddressUse"},
            # SNOMED CT OID is used for multiple domain-specific purposes
            "2.16.840.1.113883.6.96": {
                "SNOMED",
                "ProcedureCode",
                "BodySite",
                "AllergySeverity",
                "ReactionSeverity",
                "SpecimenType",
            },
            # LOINC OID is used for general LOINC and VitalSignResult
            "2.16.840.1.113883.6.1": {"LOINC", "VitalSignResult"},
            # NCI Thesaurus OID is used for general NCI and DoseForm
            "2.16.840.1.113883.3.26.1.1": {"NCI", "DoseForm"},
            # HL7 base OID is used for HL7 vocabulary and AdministrativeGender
            "2.16.840.1.113883.5.1": {"HL7", "AdministrativeGender"},
            # HL7 ActCode is used for multiple purposes
            "2.16.840.1.113883.5.4": {"ActCode", "EncounterType"},
            # HL7 ActStatus is used for general ActStatus and LabResultStatus
            "2.16.840.1.113883.5.14": {"ActStatus", "LabResultStatus"},
            # HL7 ObservationInterpretation is used for general and ResultInterpretation
            "2.16.840.1.113883.5.83": {"ObservationInterpretation", "ResultInterpretation"},
        }

        for oid, systems in shared_oids.items():
            assert oid in expected_shared, f"Unexpected shared OID: {oid} for systems: {systems}"
            # Check that the systems match what we expect
            assert set(systems) == expected_shared[oid], (
                f"OID {oid}: expected {expected_shared[oid]}, got {set(systems)}"
            )

    def test_rxnorm_format_validation(self):
        """Test RxNorm code format validation."""
        assert CodeSystemRegistry.validate_code_format("123", "RxNorm")
        assert CodeSystemRegistry.validate_code_format("123456", "RxNorm")
        assert not CodeSystemRegistry.validate_code_format("ABC", "RxNorm")
        assert not CodeSystemRegistry.validate_code_format("12.34", "RxNorm")

    def test_icd10_pcs_format_validation(self):
        """Test ICD-10-PCS code format validation."""
        assert CodeSystemRegistry.validate_code_format("0W9G30Z", "ICD-10-PCS")
        assert CodeSystemRegistry.validate_code_format("0DT60ZZ", "ICD-10-PCS")
        # Invalid: contains I or O (excluded characters)
        assert not CodeSystemRegistry.validate_code_format("0W9G30I", "ICD-10-PCS")
        assert not CodeSystemRegistry.validate_code_format("0DT60ZO", "ICD-10-PCS")
        # Invalid: wrong length
        assert not CodeSystemRegistry.validate_code_format("0W9G30", "ICD-10-PCS")
        assert not CodeSystemRegistry.validate_code_format("0W9G30ZZ", "ICD-10-PCS")

    def test_icd9_pcs_format_validation(self):
        """Test ICD-9-PCS code format validation."""
        assert CodeSystemRegistry.validate_code_format("01", "ICD-9-PCS")
        assert CodeSystemRegistry.validate_code_format("01.0", "ICD-9-PCS")
        assert CodeSystemRegistry.validate_code_format("99.99", "ICD-9-PCS")
        assert not CodeSystemRegistry.validate_code_format("1", "ICD-9-PCS")
        assert not CodeSystemRegistry.validate_code_format("001", "ICD-9-PCS")

    def test_discharge_disposition_format_validation(self):
        """Test DischargeDisposition code format validation."""
        assert CodeSystemRegistry.validate_code_format("01", "DischargeDisposition")
        assert CodeSystemRegistry.validate_code_format("99", "DischargeDisposition")
        assert not CodeSystemRegistry.validate_code_format("1", "DischargeDisposition")
        assert not CodeSystemRegistry.validate_code_format("100", "DischargeDisposition")

    def test_admit_source_format_validation(self):
        """Test AdmitSource code format validation."""
        assert CodeSystemRegistry.validate_code_format("1", "AdmitSource")
        assert CodeSystemRegistry.validate_code_format("99", "AdmitSource")
        assert not CodeSystemRegistry.validate_code_format("100", "AdmitSource")
        assert not CodeSystemRegistry.validate_code_format("A", "AdmitSource")
