"""Tests for data validation utilities."""

from datetime import date, datetime

from ccdakit.utils.validators import DataValidator


class TestValidatePatientData:
    """Tests for validate_patient_data."""

    def test_valid_patient(self):
        """Test validation of valid patient data."""
        patient = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": date(1980, 1, 15),
            "sex": "M",
        }
        result = DataValidator.validate_patient_data(patient)
        assert result.is_valid
        assert len(result.errors) == 0

    def test_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        patient = {"first_name": "John"}
        result = DataValidator.validate_patient_data(patient)
        assert not result.is_valid
        assert len(result.errors) == 3  # Missing: last_name, date_of_birth, sex

    def test_invalid_date_of_birth_type(self):
        """Test validation fails for invalid date_of_birth type."""
        patient = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1980-01-15",  # Should be date object
            "sex": "M",
        }
        result = DataValidator.validate_patient_data(patient)
        assert not result.is_valid
        assert any("date_of_birth must be a date object" in e.message for e in result.errors)

    def test_future_date_of_birth(self):
        """Test validation fails for future date_of_birth."""
        patient = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": date(2030, 1, 1),
            "sex": "M",
        }
        result = DataValidator.validate_patient_data(patient)
        assert not result.is_valid
        assert any("cannot be in the future" in e.message for e in result.errors)

    def test_ancient_date_of_birth_warning(self):
        """Test warning for very old date_of_birth."""
        patient = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": date(1850, 1, 1),
            "sex": "M",
        }
        result = DataValidator.validate_patient_data(patient)
        assert result.is_valid  # Valid but with warning
        assert result.has_warnings
        assert any("before 1900" in w.message for w in result.warnings)

    def test_invalid_sex(self):
        """Test validation fails for invalid sex value."""
        patient = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": date(1980, 1, 1),
            "sex": "X",  # Invalid
        }
        result = DataValidator.validate_patient_data(patient)
        assert not result.is_valid
        assert any("sex must be one of" in e.message for e in result.errors)

    def test_invalid_addresses_type(self):
        """Test validation fails for invalid addresses type."""
        patient = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": date(1980, 1, 1),
            "sex": "M",
            "addresses": "not a list",
        }
        result = DataValidator.validate_patient_data(patient)
        assert not result.is_valid
        assert any("addresses must be a list" in e.message for e in result.errors)

    def test_valid_with_addresses(self):
        """Test validation with valid addresses."""
        patient = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": date(1980, 1, 1),
            "sex": "M",
            "addresses": [
                {
                    "street_lines": ["123 Main St"],
                    "city": "Boston",
                    "state": "MA",
                    "postal_code": "02101",
                    "country": "US",
                }
            ],
        }
        result = DataValidator.validate_patient_data(patient)
        assert result.is_valid

    def test_invalid_address_missing_fields(self):
        """Test validation fails for address missing required fields."""
        patient = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": date(1980, 1, 1),
            "sex": "M",
            "addresses": [{"city": "Boston"}],  # Missing state, postal_code, country
        }
        result = DataValidator.validate_patient_data(patient)
        assert not result.is_valid
        assert any("Address 0" in e.message for e in result.errors)

    def test_valid_with_telecoms(self):
        """Test validation with valid telecoms."""
        patient = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": date(1980, 1, 1),
            "sex": "M",
            "telecoms": [{"type": "phone", "value": "617-555-1234", "use": "HP"}],
        }
        result = DataValidator.validate_patient_data(patient)
        assert result.is_valid

    def test_invalid_telecom_type(self):
        """Test validation fails for invalid telecom type."""
        patient = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": date(1980, 1, 1),
            "sex": "M",
            "telecoms": [{"type": "invalid", "value": "617-555-1234"}],
        }
        result = DataValidator.validate_patient_data(patient)
        assert not result.is_valid
        assert any("Telecom 0" in e.message for e in result.errors)


class TestValidateProblemData:
    """Tests for validate_problem_data."""

    def test_valid_problem(self):
        """Test validation of valid problem data."""
        problem = {
            "name": "Essential Hypertension",
            "code": "59621000",
            "code_system": "SNOMED",
            "status": "active",
        }
        result = DataValidator.validate_problem_data(problem)
        assert result.is_valid

    def test_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        problem = {"name": "Essential Hypertension"}
        result = DataValidator.validate_problem_data(problem)
        assert not result.is_valid
        assert len(result.errors) >= 3  # Missing code, code_system, status

    def test_invalid_status(self):
        """Test validation fails for invalid status."""
        problem = {
            "name": "Essential Hypertension",
            "code": "59621000",
            "code_system": "SNOMED",
            "status": "invalid",
        }
        result = DataValidator.validate_problem_data(problem)
        assert not result.is_valid
        assert any("status must be one of" in e.message for e in result.errors)

    def test_invalid_date_types(self):
        """Test validation fails for invalid date types."""
        problem = {
            "name": "Essential Hypertension",
            "code": "59621000",
            "code_system": "SNOMED",
            "status": "active",
            "onset_date": "2020-01-01",  # Should be date object
        }
        result = DataValidator.validate_problem_data(problem)
        assert not result.is_valid
        assert any("onset_date must be a date object" in e.message for e in result.errors)

    def test_invalid_date_range(self):
        """Test validation fails when resolved_date before onset_date."""
        problem = {
            "name": "Essential Hypertension",
            "code": "59621000",
            "code_system": "SNOMED",
            "status": "resolved",
            "onset_date": date(2020, 6, 1),
            "resolved_date": date(2020, 1, 1),  # Before onset
        }
        result = DataValidator.validate_problem_data(problem)
        assert not result.is_valid
        assert any("resolved_date must be after onset_date" in e.message for e in result.errors)

    def test_resolved_without_date_warning(self):
        """Test warning when problem is resolved but no resolved_date."""
        problem = {
            "name": "Essential Hypertension",
            "code": "59621000",
            "code_system": "SNOMED",
            "status": "resolved",
            "onset_date": date(2020, 1, 1),
        }
        result = DataValidator.validate_problem_data(problem)
        assert result.is_valid
        assert result.has_warnings
        assert any("resolved but no resolved_date" in w.message for w in result.warnings)

    def test_resolved_date_without_status_warning(self):
        """Test warning when resolved_date present but status not resolved."""
        problem = {
            "name": "Essential Hypertension",
            "code": "59621000",
            "code_system": "SNOMED",
            "status": "active",
            "onset_date": date(2020, 1, 1),
            "resolved_date": date(2020, 6, 1),
        }
        result = DataValidator.validate_problem_data(problem)
        assert result.is_valid
        assert result.has_warnings
        assert any("status is not 'resolved'" in w.message for w in result.warnings)

    def test_invalid_code_format_warning(self):
        """Test warning for invalid code format."""
        problem = {
            "name": "Essential Hypertension",
            "code": "invalid-code",
            "code_system": "SNOMED",
            "status": "active",
        }
        result = DataValidator.validate_problem_data(problem)
        assert result.is_valid  # Valid but with warning
        assert result.has_warnings
        assert any("does not match expected format" in w.message for w in result.warnings)


class TestValidateMedicationData:
    """Tests for validate_medication_data."""

    def test_valid_medication(self):
        """Test validation of valid medication data."""
        medication = {
            "name": "Lisinopril 10mg",
            "code": "314076",
            "dosage": "10 mg",
            "route": "oral",
            "frequency": "once daily",
            "start_date": date(2020, 1, 1),
            "status": "active",
        }
        result = DataValidator.validate_medication_data(medication)
        assert result.is_valid

    def test_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        medication = {"name": "Lisinopril"}
        result = DataValidator.validate_medication_data(medication)
        assert not result.is_valid
        assert len(result.errors) >= 6

    def test_invalid_status(self):
        """Test validation fails for invalid status."""
        medication = {
            "name": "Lisinopril 10mg",
            "code": "314076",
            "dosage": "10 mg",
            "route": "oral",
            "frequency": "once daily",
            "start_date": date(2020, 1, 1),
            "status": "invalid",
        }
        result = DataValidator.validate_medication_data(medication)
        assert not result.is_valid
        assert any("status must be one of" in e.message for e in result.errors)

    def test_invalid_date_range(self):
        """Test validation fails when end_date before start_date."""
        medication = {
            "name": "Lisinopril 10mg",
            "code": "314076",
            "dosage": "10 mg",
            "route": "oral",
            "frequency": "once daily",
            "start_date": date(2020, 6, 1),
            "end_date": date(2020, 1, 1),
            "status": "completed",
        }
        result = DataValidator.validate_medication_data(medication)
        assert not result.is_valid
        assert any("end_date must be after start_date" in e.message for e in result.errors)

    def test_completed_without_end_date_warning(self):
        """Test warning when medication completed but no end_date."""
        medication = {
            "name": "Lisinopril 10mg",
            "code": "314076",
            "dosage": "10 mg",
            "route": "oral",
            "frequency": "once daily",
            "start_date": date(2020, 1, 1),
            "status": "completed",
        }
        result = DataValidator.validate_medication_data(medication)
        assert result.is_valid
        assert result.has_warnings
        assert any("completed" in w.message and "no end_date" in w.message for w in result.warnings)


class TestValidateAllergyData:
    """Tests for validate_allergy_data."""

    def test_valid_allergy(self):
        """Test validation of valid allergy data."""
        allergy = {
            "allergen": "Penicillin",
            "allergy_type": "allergy",
            "status": "active",
        }
        result = DataValidator.validate_allergy_data(allergy)
        assert result.is_valid

    def test_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        allergy = {"allergen": "Penicillin"}
        result = DataValidator.validate_allergy_data(allergy)
        assert not result.is_valid
        assert len(result.errors) >= 2

    def test_invalid_allergy_type(self):
        """Test validation fails for invalid allergy_type."""
        allergy = {
            "allergen": "Penicillin",
            "allergy_type": "invalid",
            "status": "active",
        }
        result = DataValidator.validate_allergy_data(allergy)
        assert not result.is_valid
        assert any("allergy_type must be one of" in e.message for e in result.errors)

    def test_invalid_status(self):
        """Test validation fails for invalid status."""
        allergy = {
            "allergen": "Penicillin",
            "allergy_type": "allergy",
            "status": "invalid",
        }
        result = DataValidator.validate_allergy_data(allergy)
        assert not result.is_valid
        assert any("status must be one of" in e.message for e in result.errors)

    def test_invalid_severity_warning(self):
        """Test warning for invalid severity."""
        allergy = {
            "allergen": "Penicillin",
            "allergy_type": "allergy",
            "status": "active",
            "severity": "super-severe",
        }
        result = DataValidator.validate_allergy_data(allergy)
        assert result.is_valid
        assert result.has_warnings
        assert any("severity should be one of" in w.message for w in result.warnings)

    def test_code_without_system_warning(self):
        """Test warning when allergen_code provided without code_system."""
        allergy = {
            "allergen": "Penicillin",
            "allergen_code": "7980",
            "allergy_type": "allergy",
            "status": "active",
        }
        result = DataValidator.validate_allergy_data(allergy)
        assert result.is_valid
        assert result.has_warnings
        assert any(
            "allergen_code provided but allergen_code_system is missing" in w.message
            for w in result.warnings
        )

    def test_future_onset_date_warning(self):
        """Test warning for future onset_date."""
        allergy = {
            "allergen": "Penicillin",
            "allergy_type": "allergy",
            "status": "active",
            "onset_date": date(2030, 1, 1),
        }
        result = DataValidator.validate_allergy_data(allergy)
        assert result.is_valid
        assert result.has_warnings
        assert any("onset_date is in the future" in w.message for w in result.warnings)


class TestValidateImmunizationData:
    """Tests for validate_immunization_data."""

    def test_valid_immunization(self):
        """Test validation of valid immunization data."""
        immunization = {
            "vaccine_name": "Influenza vaccine",
            "cvx_code": "141",
            "administration_date": date(2023, 10, 1),
            "status": "completed",
        }
        result = DataValidator.validate_immunization_data(immunization)
        assert result.is_valid

    def test_valid_immunization_with_datetime(self):
        """Test validation with datetime administration_date."""
        immunization = {
            "vaccine_name": "Influenza vaccine",
            "cvx_code": "141",
            "administration_date": datetime(2023, 10, 1, 10, 30),
            "status": "completed",
        }
        result = DataValidator.validate_immunization_data(immunization)
        assert result.is_valid

    def test_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        immunization = {"vaccine_name": "Influenza vaccine"}
        result = DataValidator.validate_immunization_data(immunization)
        assert not result.is_valid
        assert len(result.errors) >= 3

    def test_invalid_status(self):
        """Test validation fails for invalid status."""
        immunization = {
            "vaccine_name": "Influenza vaccine",
            "cvx_code": "141",
            "administration_date": date(2023, 10, 1),
            "status": "invalid",
        }
        result = DataValidator.validate_immunization_data(immunization)
        assert not result.is_valid
        assert any("status must be one of" in e.message for e in result.errors)

    def test_invalid_administration_date_type(self):
        """Test validation fails for invalid administration_date type."""
        immunization = {
            "vaccine_name": "Influenza vaccine",
            "cvx_code": "141",
            "administration_date": "2023-10-01",
            "status": "completed",
        }
        result = DataValidator.validate_immunization_data(immunization)
        assert not result.is_valid
        assert any(
            "administration_date must be a date or datetime object" in e.message
            for e in result.errors
        )


class TestValidateVitalSignsData:
    """Tests for validate_vital_signs_data."""

    def test_valid_vital_signs(self):
        """Test validation of valid vital signs data."""
        vital_signs = {
            "date": datetime(2023, 10, 1, 10, 30),
            "vital_signs": [
                {
                    "type": "Blood Pressure Systolic",
                    "code": "8480-6",
                    "value": "120",
                    "unit": "mm[Hg]",
                }
            ],
        }
        result = DataValidator.validate_vital_signs_data(vital_signs)
        assert result.is_valid

    def test_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        vital_signs = {"date": datetime(2023, 10, 1)}
        result = DataValidator.validate_vital_signs_data(vital_signs)
        assert not result.is_valid

    def test_empty_vital_signs_list_warning(self):
        """Test warning for empty vital signs list."""
        vital_signs = {"date": datetime(2023, 10, 1), "vital_signs": []}
        result = DataValidator.validate_vital_signs_data(vital_signs)
        assert result.is_valid
        assert result.has_warnings
        assert any("vital_signs list is empty" in w.message for w in result.warnings)

    def test_invalid_vital_sign_missing_fields(self):
        """Test validation fails for vital sign missing required fields."""
        vital_signs = {
            "date": datetime(2023, 10, 1),
            "vital_signs": [{"type": "Blood Pressure"}],
        }
        result = DataValidator.validate_vital_signs_data(vital_signs)
        assert not result.is_valid
        assert any("Vital sign 0" in e.message for e in result.errors)

    def test_blood_pressure_out_of_range_warning(self):
        """Test warning for blood pressure out of typical range."""
        vital_signs = {
            "date": datetime(2023, 10, 1),
            "vital_signs": [
                {
                    "type": "Blood Pressure Systolic",
                    "code": "8480-6",
                    "value": "350",  # Too high
                    "unit": "mm[Hg]",
                }
            ],
        }
        result = DataValidator.validate_vital_signs_data(vital_signs)
        assert result.is_valid
        assert result.has_warnings
        assert any("outside typical range" in w.message for w in result.warnings)

    def test_heart_rate_out_of_range_warning(self):
        """Test warning for heart rate out of typical range."""
        vital_signs = {
            "date": datetime(2023, 10, 1),
            "vital_signs": [
                {
                    "type": "Heart Rate",
                    "code": "8867-4",
                    "value": "300",  # Too high
                    "unit": "bpm",
                }
            ],
        }
        result = DataValidator.validate_vital_signs_data(vital_signs)
        assert result.is_valid
        assert result.has_warnings
        assert any("outside typical range" in w.message for w in result.warnings)

    def test_temperature_celsius_out_of_range_warning(self):
        """Test warning for temperature (Celsius) out of typical range."""
        vital_signs = {
            "date": datetime(2023, 10, 1),
            "vital_signs": [
                {
                    "type": "Body Temperature",
                    "code": "8310-5",
                    "value": "50",  # Too high
                    "unit": "Cel",
                }
            ],
        }
        result = DataValidator.validate_vital_signs_data(vital_signs)
        assert result.is_valid
        assert result.has_warnings
        assert any("outside typical range" in w.message for w in result.warnings)


class TestValidateProcedureData:
    """Tests for validate_procedure_data."""

    def test_valid_procedure(self):
        """Test validation of valid procedure data."""
        procedure = {
            "name": "Appendectomy",
            "code": "80146002",
            "code_system": "SNOMED",
            "status": "completed",
        }
        result = DataValidator.validate_procedure_data(procedure)
        assert result.is_valid

    def test_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        procedure = {"name": "Appendectomy"}
        result = DataValidator.validate_procedure_data(procedure)
        assert not result.is_valid
        assert len(result.errors) >= 3

    def test_invalid_status(self):
        """Test validation fails for invalid status."""
        procedure = {
            "name": "Appendectomy",
            "code": "80146002",
            "code_system": "SNOMED",
            "status": "invalid",
        }
        result = DataValidator.validate_procedure_data(procedure)
        assert not result.is_valid
        assert any("status must be one of" in e.message for e in result.errors)

    def test_future_date_warning(self):
        """Test warning for future procedure date."""
        procedure = {
            "name": "Appendectomy",
            "code": "80146002",
            "code_system": "SNOMED",
            "status": "completed",
            "date": date(2030, 1, 1),
        }
        result = DataValidator.validate_procedure_data(procedure)
        assert result.is_valid
        assert result.has_warnings
        assert any("Procedure date is in the future" in w.message for w in result.warnings)

    def test_target_site_code_without_name_warning(self):
        """Test warning when target_site_code without target_site name."""
        procedure = {
            "name": "Appendectomy",
            "code": "80146002",
            "code_system": "SNOMED",
            "status": "completed",
            "target_site_code": "72696002",
        }
        result = DataValidator.validate_procedure_data(procedure)
        assert result.is_valid
        assert result.has_warnings
        assert any(
            "target_site_code provided but target_site name is missing" in w.message
            for w in result.warnings
        )


class TestValidateResultData:
    """Tests for validate_result_data."""

    def test_valid_result(self):
        """Test validation of valid result data."""
        result_data = {
            "panel_name": "Complete Blood Count",
            "panel_code": "58410-2",
            "status": "completed",
            "effective_time": datetime(2023, 10, 1),
            "results": [
                {
                    "test_name": "Hemoglobin",
                    "test_code": "718-7",
                    "value": "14.5",
                    "unit": "g/dL",
                    "status": "final",
                    "effective_time": datetime(2023, 10, 1),
                }
            ],
        }
        result = DataValidator.validate_result_data(result_data)
        assert result.is_valid

    def test_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        result_data = {"panel_name": "Complete Blood Count"}
        result = DataValidator.validate_result_data(result_data)
        assert not result.is_valid
        assert len(result.errors) >= 4

    def test_invalid_status(self):
        """Test validation fails for invalid status."""
        result_data = {
            "panel_name": "Complete Blood Count",
            "panel_code": "58410-2",
            "status": "invalid",
            "effective_time": datetime(2023, 10, 1),
            "results": [],
        }
        result = DataValidator.validate_result_data(result_data)
        assert not result.is_valid
        assert any("status must be one of" in e.message for e in result.errors)

    def test_empty_results_list_warning(self):
        """Test warning for empty results list."""
        result_data = {
            "panel_name": "Complete Blood Count",
            "panel_code": "58410-2",
            "status": "completed",
            "effective_time": datetime(2023, 10, 1),
            "results": [],
        }
        result = DataValidator.validate_result_data(result_data)
        assert result.is_valid
        assert result.has_warnings
        assert any("results list is empty" in w.message for w in result.warnings)

    def test_invalid_result_observation(self):
        """Test validation fails for invalid result observation."""
        result_data = {
            "panel_name": "Complete Blood Count",
            "panel_code": "58410-2",
            "status": "completed",
            "effective_time": datetime(2023, 10, 1),
            "results": [{"test_name": "Hemoglobin"}],  # Missing required fields
        }
        result = DataValidator.validate_result_data(result_data)
        assert not result.is_valid
        assert any("Result 0" in e.message for e in result.errors)

    def test_invalid_value_type(self):
        """Test validation fails for invalid value_type."""
        result_data = {
            "panel_name": "Complete Blood Count",
            "panel_code": "58410-2",
            "status": "completed",
            "effective_time": datetime(2023, 10, 1),
            "results": [
                {
                    "test_name": "Hemoglobin",
                    "test_code": "718-7",
                    "value": "14.5",
                    "unit": "g/dL",
                    "status": "final",
                    "effective_time": datetime(2023, 10, 1),
                    "value_type": "INVALID",
                }
            ],
        }
        result = DataValidator.validate_result_data(result_data)
        assert not result.is_valid
        assert any("value_type must be one of" in e.message for e in result.errors)

    def test_invalid_reference_range(self):
        """Test validation fails for invalid reference range."""
        result_data = {
            "panel_name": "Complete Blood Count",
            "panel_code": "58410-2",
            "status": "completed",
            "effective_time": datetime(2023, 10, 1),
            "results": [
                {
                    "test_name": "Hemoglobin",
                    "test_code": "718-7",
                    "value": "14.5",
                    "unit": "g/dL",
                    "status": "final",
                    "effective_time": datetime(2023, 10, 1),
                    "reference_range_low": "20",
                    "reference_range_high": "10",  # Lower than low
                    "reference_range_unit": "g/dL",
                }
            ],
        }
        result = DataValidator.validate_result_data(result_data)
        assert not result.is_valid
        assert any(
            "reference_range_low" in e.message and "must be less than" in e.message
            for e in result.errors
        )


class TestValidateEncounterData:
    """Tests for validate_encounter_data."""

    def test_valid_encounter(self):
        """Test validation of valid encounter data."""
        encounter = {
            "encounter_type": "Office Visit",
            "code": "99213",
            "code_system": "CPT",
        }
        result = DataValidator.validate_encounter_data(encounter)
        assert result.is_valid

    def test_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        encounter = {"encounter_type": "Office Visit"}
        result = DataValidator.validate_encounter_data(encounter)
        assert not result.is_valid
        assert len(result.errors) >= 2

    def test_invalid_date_range(self):
        """Test validation fails when end_date before date."""
        encounter = {
            "encounter_type": "Office Visit",
            "code": "99213",
            "code_system": "CPT",
            "date": date(2023, 6, 1),
            "end_date": date(2023, 1, 1),
        }
        result = DataValidator.validate_encounter_data(encounter)
        assert not result.is_valid
        assert any("end_date must be after date" in e.message for e in result.errors)


class TestValidateSmokingStatusData:
    """Tests for validate_smoking_status_data."""

    def test_valid_smoking_status(self):
        """Test validation of valid smoking status data."""
        smoking_status = {
            "smoking_status": "Current every day smoker",
            "code": "449868002",
            "date": date(2023, 10, 1),
        }
        result = DataValidator.validate_smoking_status_data(smoking_status)
        assert result.is_valid

    def test_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        smoking_status = {"smoking_status": "Never smoker"}
        result = DataValidator.validate_smoking_status_data(smoking_status)
        assert not result.is_valid
        assert len(result.errors) >= 2

    def test_future_date_warning(self):
        """Test warning for future smoking status date."""
        smoking_status = {
            "smoking_status": "Never smoker",
            "code": "266919005",
            "date": date(2030, 1, 1),
        }
        result = DataValidator.validate_smoking_status_data(smoking_status)
        assert result.is_valid
        assert result.has_warnings
        assert any("Smoking status date is in the future" in w.message for w in result.warnings)


class TestHelperMethods:
    """Tests for helper methods."""

    def test_validate_code_valid(self):
        """Test validate_code with valid code."""
        assert DataValidator.validate_code("12345-6", "LOINC")

    def test_validate_code_invalid(self):
        """Test validate_code with invalid code."""
        assert not DataValidator.validate_code("invalid", "LOINC")

    def test_validate_date_range_valid(self):
        """Test validate_date_range with valid range."""
        start = date(2020, 1, 1)
        end = date(2020, 12, 31)
        assert DataValidator.validate_date_range(start, end)

    def test_validate_date_range_invalid(self):
        """Test validate_date_range with invalid range."""
        start = date(2020, 12, 31)
        end = date(2020, 1, 1)
        assert not DataValidator.validate_date_range(start, end)

    def test_validate_date_range_none_end(self):
        """Test validate_date_range with None end date."""
        start = date(2020, 1, 1)
        assert DataValidator.validate_date_range(start, None)

    def test_validate_date_range_with_datetime(self):
        """Test validate_date_range with datetime objects."""
        start = datetime(2020, 1, 1, 10, 0)
        end = datetime(2020, 1, 1, 12, 0)
        assert DataValidator.validate_date_range(start, end)

    def test_validate_code_system_valid(self):
        """Test validate_code_system with valid system."""
        assert DataValidator.validate_code_system("LOINC")

    def test_validate_code_system_invalid(self):
        """Test validate_code_system with invalid system."""
        assert not DataValidator.validate_code_system("INVALID_SYSTEM")

    def test_validate_required_fields_all_present(self):
        """Test validate_required_fields with all fields present."""
        data = {"field1": "value1", "field2": "value2"}
        required = ["field1", "field2"]
        missing = DataValidator.validate_required_fields(data, required)
        assert len(missing) == 0

    def test_validate_required_fields_some_missing(self):
        """Test validate_required_fields with some fields missing."""
        data = {"field1": "value1"}
        required = ["field1", "field2", "field3"]
        missing = DataValidator.validate_required_fields(data, required)
        assert len(missing) == 2
        assert "field2" in missing
        assert "field3" in missing

    def test_validate_required_fields_none_values(self):
        """Test validate_required_fields treats None as missing."""
        data = {"field1": "value1", "field2": None}
        required = ["field1", "field2"]
        missing = DataValidator.validate_required_fields(data, required)
        assert len(missing) == 1
        assert "field2" in missing

    def test_validate_required_fields_empty_string(self):
        """Test validate_required_fields treats empty string as missing."""
        data = {"field1": "value1", "field2": ""}
        required = ["field1", "field2"]
        missing = DataValidator.validate_required_fields(data, required)
        assert len(missing) == 1
        assert "field2" in missing


class TestAddressValidation:
    """Tests for _validate_address helper."""

    def test_valid_address(self):
        """Test validation of valid address."""
        address = {
            "street_lines": ["123 Main St"],
            "city": "Boston",
            "state": "MA",
            "postal_code": "02101",
            "country": "US",
        }
        result = DataValidator._validate_address(address)
        assert result.is_valid

    def test_missing_fields(self):
        """Test validation fails for missing required fields."""
        address = {"city": "Boston"}
        result = DataValidator._validate_address(address)
        assert not result.is_valid
        assert len(result.errors) == 3  # Missing state, postal_code, country

    def test_invalid_street_lines_type(self):
        """Test validation fails for invalid street_lines type."""
        address = {
            "street_lines": "not a list",
            "city": "Boston",
            "state": "MA",
            "postal_code": "02101",
            "country": "US",
        }
        result = DataValidator._validate_address(address)
        assert not result.is_valid
        assert any("street_lines must be a list" in e.message for e in result.errors)

    def test_too_many_street_lines(self):
        """Test validation fails for more than 4 street lines."""
        address = {
            "street_lines": ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"],
            "city": "Boston",
            "state": "MA",
            "postal_code": "02101",
            "country": "US",
        }
        result = DataValidator._validate_address(address)
        assert not result.is_valid
        assert any("at most 4 lines" in e.message for e in result.errors)


class TestTelecomValidation:
    """Tests for _validate_telecom helper."""

    def test_valid_telecom(self):
        """Test validation of valid telecom."""
        telecom = {"type": "phone", "value": "617-555-1234"}
        result = DataValidator._validate_telecom(telecom)
        assert result.is_valid

    def test_missing_fields(self):
        """Test validation fails for missing required fields."""
        telecom = {"type": "phone"}
        result = DataValidator._validate_telecom(telecom)
        assert not result.is_valid

    def test_invalid_type(self):
        """Test validation fails for invalid type."""
        telecom = {"type": "invalid", "value": "617-555-1234"}
        result = DataValidator._validate_telecom(telecom)
        assert not result.is_valid
        assert any("type must be one of" in e.message for e in result.errors)

    def test_invalid_use_warning(self):
        """Test warning for invalid use."""
        telecom = {"type": "phone", "value": "617-555-1234", "use": "INVALID"}
        result = DataValidator._validate_telecom(telecom)
        assert result.is_valid
        assert result.has_warnings
        assert any("use should be one of" in w.message for w in result.warnings)
