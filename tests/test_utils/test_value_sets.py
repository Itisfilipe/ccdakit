"""Tests for value set registry and utilities."""

import json
import tempfile
from pathlib import Path

import pytest

from ccdakit.utils.value_sets import ValueSetRegistry


class TestValueSetRegistry:
    """Test ValueSetRegistry class."""

    def test_validate_code_valid(self):
        """Test validating a valid code."""
        assert ValueSetRegistry.validate_code("PROBLEM_STATUS", "55561003") is True
        assert ValueSetRegistry.validate_code("ALLERGY_STATUS", "55561003") is True
        assert ValueSetRegistry.validate_code("ADMINISTRATIVE_GENDER", "M") is True

    def test_validate_code_invalid(self):
        """Test validating an invalid code."""
        assert ValueSetRegistry.validate_code("PROBLEM_STATUS", "invalid") is False
        assert ValueSetRegistry.validate_code("ALLERGY_STATUS", "99999999") is False
        assert ValueSetRegistry.validate_code("ADMINISTRATIVE_GENDER", "X") is False

    def test_validate_code_unknown_value_set(self):
        """Test validating code in unknown value set."""
        assert ValueSetRegistry.validate_code("UNKNOWN_VALUE_SET", "55561003") is False

    def test_get_display_name_valid(self):
        """Test getting display name for valid code."""
        assert ValueSetRegistry.get_display_name("PROBLEM_STATUS", "55561003") == "Active"
        assert ValueSetRegistry.get_display_name("PROBLEM_STATUS", "73425007") == "Inactive"
        assert ValueSetRegistry.get_display_name("PROBLEM_STATUS", "413322009") == "Resolved"

    def test_get_display_name_invalid(self):
        """Test getting display name for invalid code."""
        assert ValueSetRegistry.get_display_name("PROBLEM_STATUS", "invalid") is None
        assert ValueSetRegistry.get_display_name("UNKNOWN_VALUE_SET", "55561003") is None

    def test_get_code_system_valid(self):
        """Test getting code system for valid code."""
        assert ValueSetRegistry.get_code_system("PROBLEM_STATUS", "55561003") == "SNOMED"
        assert (
            ValueSetRegistry.get_code_system("ADMINISTRATIVE_GENDER", "M") == "AdministrativeGender"
        )
        assert ValueSetRegistry.get_code_system("VITAL_SIGN_RESULT_TYPE", "8310-5") == "LOINC"

    def test_get_code_system_invalid(self):
        """Test getting code system for invalid code."""
        assert ValueSetRegistry.get_code_system("PROBLEM_STATUS", "invalid") is None
        assert ValueSetRegistry.get_code_system("UNKNOWN_VALUE_SET", "55561003") is None

    def test_get_code_info_valid(self):
        """Test getting complete code information."""
        info = ValueSetRegistry.get_code_info("PROBLEM_STATUS", "55561003")
        assert info is not None
        assert info["display"] == "Active"
        assert info["system"] == "SNOMED"

    def test_get_code_info_invalid(self):
        """Test getting code info for invalid code."""
        assert ValueSetRegistry.get_code_info("PROBLEM_STATUS", "invalid") is None
        assert ValueSetRegistry.get_code_info("UNKNOWN_VALUE_SET", "55561003") is None

    def test_get_value_set_valid(self):
        """Test getting value set definition."""
        vs = ValueSetRegistry.get_value_set("PROBLEM_STATUS")
        assert vs is not None
        assert vs["oid"] == "2.16.840.1.113883.1.11.15933"
        assert vs["name"] == "Problem Status"
        assert "codes" in vs
        assert len(vs["codes"]) == 3

    def test_get_value_set_invalid(self):
        """Test getting unknown value set."""
        assert ValueSetRegistry.get_value_set("UNKNOWN_VALUE_SET") is None

    def test_get_value_set_by_oid_valid(self):
        """Test getting value set by OID."""
        vs = ValueSetRegistry.get_value_set_by_oid("2.16.840.1.113883.1.11.15933")
        assert vs is not None
        assert vs["name"] == "Problem Status"

    def test_get_value_set_by_oid_invalid(self):
        """Test getting value set with invalid OID."""
        assert ValueSetRegistry.get_value_set_by_oid("1.2.3.4.5") is None

    def test_list_value_sets(self):
        """Test listing all value sets."""
        value_sets = ValueSetRegistry.list_value_sets()
        assert isinstance(value_sets, list)
        assert len(value_sets) == 18
        assert "PROBLEM_STATUS" in value_sets
        assert "ALLERGY_STATUS" in value_sets
        assert "MEDICATION_STATUS" in value_sets
        assert "OBSERVATION_INTERPRETATION" in value_sets
        assert "SMOKING_STATUS" in value_sets
        assert "ADMINISTRATIVE_GENDER" in value_sets

    def test_get_codes_valid(self):
        """Test getting all codes for a value set."""
        codes = ValueSetRegistry.get_codes("PROBLEM_STATUS")
        assert isinstance(codes, list)
        assert len(codes) == 3
        assert "55561003" in codes
        assert "73425007" in codes
        assert "413322009" in codes

    def test_get_codes_administrative_gender(self):
        """Test getting administrative gender codes."""
        codes = ValueSetRegistry.get_codes("ADMINISTRATIVE_GENDER")
        assert "M" in codes
        assert "F" in codes
        assert "UN" in codes

    def test_get_codes_invalid(self):
        """Test getting codes for unknown value set."""
        codes = ValueSetRegistry.get_codes("UNKNOWN_VALUE_SET")
        assert codes == []

    def test_search_by_display_exact(self):
        """Test searching by exact display name."""
        codes = ValueSetRegistry.search_by_display("PROBLEM_STATUS", "Active")
        assert "55561003" in codes

    def test_search_by_display_partial(self):
        """Test searching by partial display name."""
        codes = ValueSetRegistry.search_by_display("PROBLEM_STATUS", "act")
        assert "55561003" in codes  # "Active"
        assert "73425007" in codes  # "Inactive"

    def test_search_by_display_case_insensitive(self):
        """Test case-insensitive search."""
        codes = ValueSetRegistry.search_by_display("PROBLEM_STATUS", "ACTIVE", case_sensitive=False)
        assert "55561003" in codes

    def test_search_by_display_case_sensitive(self):
        """Test case-sensitive search."""
        # "active" in lowercase will match "Inactive" (contains "active")
        codes = ValueSetRegistry.search_by_display("PROBLEM_STATUS", "active", case_sensitive=True)
        assert "73425007" in codes  # Matches "Inactive"
        assert "55561003" not in codes  # Doesn't match "Active"

        # "Active" will match "Active" in case-sensitive mode
        codes = ValueSetRegistry.search_by_display("PROBLEM_STATUS", "Active", case_sensitive=True)
        assert "55561003" in codes
        assert len(codes) == 1  # Only matches "Active", not "Inactive"

        # "Inactive" matches exactly
        codes = ValueSetRegistry.search_by_display(
            "PROBLEM_STATUS", "Inactive", case_sensitive=True
        )
        assert "73425007" in codes

    def test_search_by_display_no_results(self):
        """Test search with no results."""
        codes = ValueSetRegistry.search_by_display("PROBLEM_STATUS", "xyz123")
        assert codes == []

    def test_search_by_display_invalid_value_set(self):
        """Test search in unknown value set."""
        codes = ValueSetRegistry.search_by_display("UNKNOWN_VALUE_SET", "Active")
        assert codes == []

    def test_observation_interpretation_codes(self):
        """Test observation interpretation value set."""
        assert ValueSetRegistry.validate_code("OBSERVATION_INTERPRETATION", "N")
        assert ValueSetRegistry.validate_code("OBSERVATION_INTERPRETATION", "H")
        assert ValueSetRegistry.validate_code("OBSERVATION_INTERPRETATION", "L")
        assert ValueSetRegistry.validate_code("OBSERVATION_INTERPRETATION", "HH")
        assert ValueSetRegistry.validate_code("OBSERVATION_INTERPRETATION", "LL")

        assert ValueSetRegistry.get_display_name("OBSERVATION_INTERPRETATION", "N") == "Normal"
        assert ValueSetRegistry.get_display_name("OBSERVATION_INTERPRETATION", "H") == "High"
        assert ValueSetRegistry.get_display_name("OBSERVATION_INTERPRETATION", "L") == "Low"

    def test_smoking_status_codes(self):
        """Test smoking status value set."""
        assert ValueSetRegistry.validate_code("SMOKING_STATUS", "449868002")
        assert ValueSetRegistry.validate_code("SMOKING_STATUS", "8517006")
        assert ValueSetRegistry.validate_code("SMOKING_STATUS", "266919005")

        assert (
            ValueSetRegistry.get_display_name("SMOKING_STATUS", "449868002")
            == "Current every day smoker"
        )
        assert ValueSetRegistry.get_display_name("SMOKING_STATUS", "8517006") == "Former smoker"
        assert ValueSetRegistry.get_display_name("SMOKING_STATUS", "266919005") == "Never smoker"

    def test_vital_sign_result_type_codes(self):
        """Test vital sign result type value set."""
        assert ValueSetRegistry.validate_code(
            "VITAL_SIGN_RESULT_TYPE", "8310-5"
        )  # Body temperature
        assert ValueSetRegistry.validate_code("VITAL_SIGN_RESULT_TYPE", "8867-4")  # Heart rate
        assert ValueSetRegistry.validate_code("VITAL_SIGN_RESULT_TYPE", "8480-6")  # Systolic BP
        assert ValueSetRegistry.validate_code("VITAL_SIGN_RESULT_TYPE", "8462-4")  # Diastolic BP

        assert (
            ValueSetRegistry.get_display_name("VITAL_SIGN_RESULT_TYPE", "8310-5")
            == "Body temperature"
        )
        assert ValueSetRegistry.get_display_name("VITAL_SIGN_RESULT_TYPE", "8867-4") == "Heart rate"

    def test_encounter_type_codes(self):
        """Test encounter type value set."""
        assert ValueSetRegistry.validate_code("ENCOUNTER_TYPE", "AMB")
        assert ValueSetRegistry.validate_code("ENCOUNTER_TYPE", "EMER")
        assert ValueSetRegistry.validate_code("ENCOUNTER_TYPE", "IMP")

        assert ValueSetRegistry.get_display_name("ENCOUNTER_TYPE", "AMB") == "Ambulatory"
        assert ValueSetRegistry.get_display_name("ENCOUNTER_TYPE", "EMER") == "Emergency"
        assert ValueSetRegistry.get_display_name("ENCOUNTER_TYPE", "IMP") == "Inpatient encounter"

    def test_marital_status_codes(self):
        """Test marital status value set."""
        assert ValueSetRegistry.validate_code("MARITAL_STATUS", "M")
        assert ValueSetRegistry.validate_code("MARITAL_STATUS", "S")
        assert ValueSetRegistry.validate_code("MARITAL_STATUS", "D")

        assert ValueSetRegistry.get_display_name("MARITAL_STATUS", "M") == "Married"
        assert ValueSetRegistry.get_display_name("MARITAL_STATUS", "S") == "Never Married"
        assert ValueSetRegistry.get_display_name("MARITAL_STATUS", "D") == "Divorced"

    def test_null_flavor_codes(self):
        """Test null flavor value set."""
        assert ValueSetRegistry.validate_code("NULL_FLAVOR", "NI")
        assert ValueSetRegistry.validate_code("NULL_FLAVOR", "UNK")
        assert ValueSetRegistry.validate_code("NULL_FLAVOR", "NA")

        assert ValueSetRegistry.get_display_name("NULL_FLAVOR", "NI") == "No information"
        assert ValueSetRegistry.get_display_name("NULL_FLAVOR", "UNK") == "Unknown"
        assert ValueSetRegistry.get_display_name("NULL_FLAVOR", "NA") == "Not applicable"

    def test_medication_status_codes(self):
        """Test medication status value set."""
        assert ValueSetRegistry.validate_code("MEDICATION_STATUS", "55561003")
        assert ValueSetRegistry.validate_code("MEDICATION_STATUS", "completed")
        assert ValueSetRegistry.validate_code("MEDICATION_STATUS", "aborted")

        assert ValueSetRegistry.get_display_name("MEDICATION_STATUS", "55561003") == "Active"
        assert ValueSetRegistry.get_display_name("MEDICATION_STATUS", "completed") == "Completed"
        assert ValueSetRegistry.get_display_name("MEDICATION_STATUS", "aborted") == "Discontinued"

    def test_allergy_severity_codes(self):
        """Test allergy severity value set."""
        assert ValueSetRegistry.validate_code("ALLERGY_SEVERITY", "255604002")
        assert ValueSetRegistry.validate_code("ALLERGY_SEVERITY", "6736007")
        assert ValueSetRegistry.validate_code("ALLERGY_SEVERITY", "24484000")

        assert ValueSetRegistry.get_display_name("ALLERGY_SEVERITY", "255604002") == "Mild"
        assert ValueSetRegistry.get_display_name("ALLERGY_SEVERITY", "6736007") == "Moderate"
        assert ValueSetRegistry.get_display_name("ALLERGY_SEVERITY", "24484000") == "Severe"

    def test_procedure_status_codes(self):
        """Test procedure status value set."""
        assert ValueSetRegistry.validate_code("PROCEDURE_STATUS", "completed")
        assert ValueSetRegistry.validate_code("PROCEDURE_STATUS", "active")
        assert ValueSetRegistry.validate_code("PROCEDURE_STATUS", "aborted")

        assert ValueSetRegistry.get_display_name("PROCEDURE_STATUS", "completed") == "Completed"
        assert ValueSetRegistry.get_display_name("PROCEDURE_STATUS", "active") == "Active"

    def test_discharge_disposition_codes(self):
        """Test discharge disposition value set."""
        assert ValueSetRegistry.validate_code("DISCHARGE_DISPOSITION", "01")
        assert ValueSetRegistry.validate_code("DISCHARGE_DISPOSITION", "03")
        assert ValueSetRegistry.validate_code("DISCHARGE_DISPOSITION", "07")

        assert (
            ValueSetRegistry.get_display_name("DISCHARGE_DISPOSITION", "01")
            == "Discharged to home or self care"
        )
        assert (
            ValueSetRegistry.get_display_name("DISCHARGE_DISPOSITION", "07")
            == "Left against medical advice"
        )

    def test_load_from_json(self):
        """Test loading value set from JSON file."""
        # Create a temporary JSON file
        test_data = {
            "oid": "1.2.3.4.5",
            "name": "Test Value Set",
            "description": "Test description",
            "codes": {
                "code1": {"display": "Code 1", "system": "TEST"},
                "code2": {"display": "Code 2", "system": "TEST"},
            },
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            temp_file = f.name

        try:
            loaded_data = ValueSetRegistry.load_from_json(temp_file)
            assert loaded_data["oid"] == "1.2.3.4.5"
            assert loaded_data["name"] == "Test Value Set"
            assert len(loaded_data["codes"]) == 2
            assert "code1" in loaded_data["codes"]
            assert loaded_data["codes"]["code1"]["display"] == "Code 1"
        finally:
            Path(temp_file).unlink()

    def test_load_from_json_file_not_found(self):
        """Test loading from non-existent file."""
        with pytest.raises(FileNotFoundError):
            ValueSetRegistry.load_from_json("/nonexistent/file.json")

    def test_save_to_json(self):
        """Test saving value set to JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "problem_status.json"

            ValueSetRegistry.save_to_json("PROBLEM_STATUS", str(output_file))

            # Verify file was created
            assert output_file.exists()

            # Load and verify contents
            with open(output_file, encoding="utf-8") as f:
                data = json.load(f)

            assert data["oid"] == "2.16.840.1.113883.1.11.15933"
            assert data["name"] == "Problem Status"
            assert len(data["codes"]) == 3
            assert "55561003" in data["codes"]

    def test_save_to_json_unknown_value_set(self):
        """Test saving unknown value set."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "unknown.json"

            with pytest.raises(ValueError, match="Value set not found"):
                ValueSetRegistry.save_to_json("UNKNOWN_VALUE_SET", str(output_file))

    def test_save_to_json_creates_directory(self):
        """Test that save_to_json creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "subdir" / "nested" / "problem_status.json"

            ValueSetRegistry.save_to_json("PROBLEM_STATUS", str(output_file))

            assert output_file.exists()
            assert output_file.parent.exists()

    def test_all_value_sets_have_required_fields(self):
        """Test that all value sets have required fields."""
        for vs_name in ValueSetRegistry.list_value_sets():
            vs = ValueSetRegistry.get_value_set(vs_name)
            assert vs is not None, f"{vs_name} not found"
            assert "oid" in vs, f"{vs_name} missing oid"
            assert "name" in vs, f"{vs_name} missing name"
            assert "description" in vs, f"{vs_name} missing description"
            assert "codes" in vs, f"{vs_name} missing codes"
            assert isinstance(vs["codes"], dict), f"{vs_name} codes not a dict"

    def test_all_codes_have_required_fields(self):
        """Test that all codes have required fields."""
        for vs_name in ValueSetRegistry.list_value_sets():
            vs = ValueSetRegistry.get_value_set(vs_name)
            assert vs is not None, f"{vs_name} not found"
            codes = vs["codes"]

            for code, info in codes.items():
                assert "display" in info, f"{vs_name} code {code} missing display"
                assert "system" in info, f"{vs_name} code {code} missing system"
                assert isinstance(info["display"], str), f"{vs_name} code {code} display not string"
                assert isinstance(info["system"], str), f"{vs_name} code {code} system not string"

    def test_value_set_completeness(self):
        """Test that all expected value sets are present."""
        expected_value_sets = [
            "PROBLEM_STATUS",
            "ALLERGY_STATUS",
            "MEDICATION_STATUS",
            "OBSERVATION_INTERPRETATION",
            "PROBLEM_TYPE",
            "ALLERGY_SEVERITY",
            "ALLERGY_REACTION_TYPE",
            "SMOKING_STATUS",
            "ENCOUNTER_TYPE",
            "LAB_RESULT_STATUS",
            "PROCEDURE_STATUS",
            "IMMUNIZATION_STATUS",
            "VITAL_SIGN_RESULT_TYPE",
            "ADMINISTRATIVE_GENDER",
            "MARITAL_STATUS",
            "NULL_FLAVOR",
            "ROUTE_OF_ADMINISTRATION",
            "DISCHARGE_DISPOSITION",
        ]

        value_sets = ValueSetRegistry.list_value_sets()
        for expected in expected_value_sets:
            assert expected in value_sets, f"Missing value set: {expected}"

    def test_route_of_administration_codes(self):
        """Test route of administration value set."""
        assert ValueSetRegistry.validate_code("ROUTE_OF_ADMINISTRATION", "C38304")  # Oral
        assert ValueSetRegistry.validate_code("ROUTE_OF_ADMINISTRATION", "C38279")  # Intravenous
        assert ValueSetRegistry.validate_code("ROUTE_OF_ADMINISTRATION", "C38276")  # Intramuscular

        assert ValueSetRegistry.get_display_name("ROUTE_OF_ADMINISTRATION", "C38304") == "Oral"
        assert (
            ValueSetRegistry.get_display_name("ROUTE_OF_ADMINISTRATION", "C38279") == "Intravenous"
        )

    def test_problem_type_codes(self):
        """Test problem type value set."""
        assert ValueSetRegistry.validate_code("PROBLEM_TYPE", "55607006")  # Problem
        assert ValueSetRegistry.validate_code("PROBLEM_TYPE", "282291009")  # Diagnosis

        assert ValueSetRegistry.get_display_name("PROBLEM_TYPE", "55607006") == "Problem"
        assert ValueSetRegistry.get_display_name("PROBLEM_TYPE", "282291009") == "Diagnosis"
