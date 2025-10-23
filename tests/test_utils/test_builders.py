"""Comprehensive tests for simplified data model builders."""

from datetime import date, datetime

from ccdakit.utils.builders import (
    SimpleAllergyBuilder,
    SimpleEncounterBuilder,
    SimpleImmunizationBuilder,
    SimpleMedicationBuilder,
    SimplePatientBuilder,
    SimpleProblemBuilder,
    SimpleProcedureBuilder,
    SimpleResultObservationBuilder,
    SimpleResultOrganizerBuilder,
    SimpleSmokingStatusBuilder,
    SimpleVitalSignBuilder,
    SimpleVitalSignsOrganizerBuilder,
    allergy_builder,
    encounter_builder,
    immunization_builder,
    medication_builder,
    patient_builder,
    problem_builder,
    procedure_builder,
    result_observation_builder,
    result_organizer_builder,
    smoking_status_builder,
    vital_sign_builder,
    vital_signs_organizer_builder,
)


class TestSimplePatientBuilder:
    """Test cases for SimplePatientBuilder."""

    def test_minimal_patient(self):
        """Test building minimal patient data."""
        patient = (
            SimplePatientBuilder()
            .name("John", "Doe")
            .birth_date(date(1970, 5, 15))
            .gender("M")
            .build()
        )

        assert patient["first_name"] == "John"
        assert patient["last_name"] == "Doe"
        assert patient["date_of_birth"] == date(1970, 5, 15)
        assert patient["sex"] == "M"
        assert patient["addresses"] == []
        assert patient["telecoms"] == []

    def test_complete_patient(self):
        """Test building complete patient data with all fields."""
        patient = (
            SimplePatientBuilder()
            .name("John", "Doe", "Q")
            .birth_date(date(1970, 5, 15))
            .gender("M")
            .race("2106-3")
            .ethnicity("2186-5")
            .language("eng")
            .ssn("123-45-6789")
            .marital_status("M")
            .address("123 Main St", "Boston", "MA", "02101", "US", "Apt 4B")
            .phone("617-555-1234", "home")
            .email("john.doe@example.com", "home")
            .build()
        )

        assert patient["first_name"] == "John"
        assert patient["middle_name"] == "Q"
        assert len(patient["addresses"]) == 1
        assert len(patient["telecoms"]) == 2


class TestSimpleProblemBuilder:
    """Test cases for SimpleProblemBuilder."""

    def test_minimal_problem(self):
        """Test building minimal problem data."""
        problem = (
            SimpleProblemBuilder()
            .name("Essential Hypertension")
            .code("59621000", "SNOMED")
            .status("active")
            .build()
        )

        assert problem["name"] == "Essential Hypertension"
        assert problem["code"] == "59621000"
        assert problem["code_system"] == "SNOMED"
        assert problem["status"] == "active"

    def test_problem_with_onset_date(self):
        """Test building problem with onset date."""
        problem = (
            SimpleProblemBuilder()
            .name("Type 2 Diabetes")
            .code("44054006", "SNOMED")
            .status("active")
            .onset_date(date(2020, 1, 15))
            .build()
        )

        assert problem["onset_date"] == date(2020, 1, 15)

    def test_problem_with_resolved_date(self):
        """Test building problem with resolved date."""
        problem = (
            SimpleProblemBuilder()
            .name("Pneumonia")
            .code("233604007", "SNOMED")
            .status("resolved")
            .onset_date(date(2022, 3, 1))
            .resolved_date(date(2022, 3, 15))
            .build()
        )

        assert problem["resolved_date"] == date(2022, 3, 15)

    def test_problem_with_persistent_id(self):
        """Test building problem with persistent ID."""
        problem = (
            SimpleProblemBuilder()
            .name("Asthma")
            .code("195967001", "SNOMED")
            .status("active")
            .persistent_id("2.16.840.1.113883.19", "prob-12345")
            .build()
        )

        assert problem["persistent_id"]["root"] == "2.16.840.1.113883.19"
        assert problem["persistent_id"]["extension"] == "prob-12345"


class TestSimpleMedicationBuilder:
    """Test cases for SimpleMedicationBuilder."""

    def test_minimal_medication(self):
        """Test building minimal medication data."""
        medication = (
            SimpleMedicationBuilder()
            .name("Lisinopril 10mg oral tablet")
            .code("314076")
            .dosage("10 mg")
            .route("oral")
            .frequency("once daily")
            .start_date(date(2018, 6, 1))
            .status("active")
            .build()
        )

        assert medication["name"] == "Lisinopril 10mg oral tablet"
        assert medication["code"] == "314076"
        assert medication["dosage"] == "10 mg"

    def test_medication_with_end_date(self):
        """Test building medication with end date."""
        medication = (
            SimpleMedicationBuilder()
            .name("Amoxicillin 500mg")
            .code("308182")
            .dosage("500 mg")
            .route("oral")
            .frequency("three times daily")
            .start_date(date(2023, 1, 1))
            .end_date(date(2023, 1, 10))
            .status("completed")
            .build()
        )

        assert medication["end_date"] == date(2023, 1, 10)

    def test_medication_with_instructions(self):
        """Test building medication with patient instructions."""
        medication = (
            SimpleMedicationBuilder()
            .name("Metformin 500mg")
            .code("860975")
            .dosage("500 mg")
            .route("oral")
            .frequency("twice daily")
            .start_date(date(2023, 5, 1))
            .status("active")
            .instructions("Take with food to reduce stomach upset")
            .build()
        )

        assert medication["instructions"] == "Take with food to reduce stomach upset"


class TestSimpleAllergyBuilder:
    """Test cases for SimpleAllergyBuilder."""

    def test_complete_allergy(self):
        """Test building complete allergy data with all fields."""
        allergy = (
            SimpleAllergyBuilder()
            .allergen("Penicillin")
            .allergen_code("7980", "RxNorm")
            .allergy_type("allergy")
            .reaction("Hives")
            .severity("moderate")
            .status("active")
            .onset_date(date(2010, 3, 15))
            .build()
        )

        assert allergy["allergen"] == "Penicillin"
        assert allergy["allergen_code"] == "7980"
        assert allergy["severity"] == "moderate"


class TestSimpleImmunizationBuilder:
    """Test cases for SimpleImmunizationBuilder."""

    def test_complete_immunization(self):
        """Test building complete immunization data."""
        immunization = (
            SimpleImmunizationBuilder()
            .vaccine("Influenza vaccine, seasonal", "141")
            .administration_date(date(2023, 9, 15))
            .status("completed")
            .lot_number("ABC123456")
            .manufacturer("Sanofi Pasteur")
            .route("intramuscular")
            .site("left deltoid")
            .dose_quantity("0.5 mL")
            .build()
        )

        assert immunization["lot_number"] == "ABC123456"
        assert immunization["manufacturer"] == "Sanofi Pasteur"


class TestSimpleVitalSignBuilder:
    """Test cases for SimpleVitalSignBuilder."""

    def test_complete_vital_sign(self):
        """Test building complete vital sign data."""
        vital_sign = (
            SimpleVitalSignBuilder()
            .observation("Heart Rate", "8867-4")
            .value("72", "bpm")
            .date(datetime(2023, 10, 15, 10, 30))
            .interpretation("Normal")
            .build()
        )

        assert vital_sign["type"] == "Heart Rate"
        assert vital_sign["code"] == "8867-4"
        assert vital_sign["interpretation"] == "Normal"


class TestSimpleVitalSignsOrganizerBuilder:
    """Test cases for SimpleVitalSignsOrganizerBuilder."""

    def test_vital_signs_organizer_with_date(self):
        """Test building vital signs organizer with date."""
        organizer = (
            SimpleVitalSignsOrganizerBuilder()
            .date(datetime(2023, 10, 15, 10, 30))
            .build()
        )

        assert organizer["date"] == datetime(2023, 10, 15, 10, 30)
        assert organizer["vital_signs"] == []

    def test_vital_signs_organizer_with_vital_signs(self):
        """Test building vital signs organizer with vital signs."""
        vital_sign1 = {"type": "Heart Rate", "code": "8867-4", "value": "72", "unit": "bpm"}
        vital_sign2 = {"type": "Blood Pressure", "code": "55284-4", "value": "120/80", "unit": "mmHg"}

        organizer = (
            SimpleVitalSignsOrganizerBuilder()
            .date(datetime(2023, 10, 15, 10, 30))
            .add_vital_sign(vital_sign1)
            .add_vital_sign(vital_sign2)
            .build()
        )

        assert len(organizer["vital_signs"]) == 2
        assert organizer["vital_signs"][0]["type"] == "Heart Rate"
        assert organizer["vital_signs"][1]["type"] == "Blood Pressure"


class TestSimpleProcedureBuilder:
    """Test cases for SimpleProcedureBuilder."""

    def test_complete_procedure(self):
        """Test building complete procedure data."""
        procedure = (
            SimpleProcedureBuilder()
            .name("Appendectomy")
            .code("80146002", "SNOMED")
            .date(date(2022, 6, 15))
            .status("completed")
            .target_site("Abdomen", "113345001")
            .performer("Dr. Jane Smith")
            .build()
        )

        assert procedure["name"] == "Appendectomy"
        assert procedure["target_site"] == "Abdomen"
        assert procedure["performer_name"] == "Dr. Jane Smith"


class TestSimpleResultObservationBuilder:
    """Test cases for SimpleResultObservationBuilder."""

    def test_complete_result(self):
        """Test building complete result observation."""
        result = (
            SimpleResultObservationBuilder()
            .test("Glucose", "2339-0")
            .value("95", "mg/dL")
            .status("final")
            .effective_time(datetime(2023, 10, 15, 8, 0))
            .value_type("PQ")
            .interpretation("N")
            .reference_range("70", "100", "mg/dL")
            .build()
        )

        assert result["test_name"] == "Glucose"
        assert result["interpretation"] == "N"
        assert result["reference_range_low"] == "70"


class TestSimpleResultOrganizerBuilder:
    """Test cases for SimpleResultOrganizerBuilder."""

    def test_result_organizer_with_panel(self):
        """Test building result organizer with panel information."""
        organizer = (
            SimpleResultOrganizerBuilder()
            .panel("Comprehensive Metabolic Panel", "24323-8")
            .status("final")
            .effective_time(datetime(2023, 10, 15, 8, 0))
            .build()
        )

        assert organizer["panel_name"] == "Comprehensive Metabolic Panel"
        assert organizer["panel_code"] == "24323-8"
        assert organizer["status"] == "final"
        assert organizer["effective_time"] == datetime(2023, 10, 15, 8, 0)
        assert organizer["results"] == []

    def test_result_organizer_with_results(self):
        """Test building result organizer with results."""
        result1 = {"test_name": "Glucose", "test_code": "2339-0", "value": "95", "unit": "mg/dL"}
        result2 = {"test_name": "Sodium", "test_code": "2951-2", "value": "140", "unit": "mmol/L"}

        organizer = (
            SimpleResultOrganizerBuilder()
            .panel("Basic Metabolic Panel", "51990-0")
            .status("final")
            .effective_time(datetime(2023, 10, 15, 8, 0))
            .add_result(result1)
            .add_result(result2)
            .build()
        )

        assert len(organizer["results"]) == 2
        assert organizer["results"][0]["test_name"] == "Glucose"
        assert organizer["results"][1]["test_name"] == "Sodium"


class TestSimpleEncounterBuilder:
    """Test cases for SimpleEncounterBuilder."""

    def test_complete_encounter(self):
        """Test building complete encounter data."""
        encounter = (
            SimpleEncounterBuilder()
            .encounter_type("Office Visit", "99213", "CPT-4")
            .date(datetime(2023, 10, 15, 9, 0))
            .end_date(datetime(2023, 10, 15, 10, 0))
            .location("Community Health Hospital")
            .performer("Dr. John Smith")
            .build()
        )

        assert encounter["encounter_type"] == "Office Visit"
        assert encounter["location"] == "Community Health Hospital"

    def test_encounter_with_discharge_disposition(self):
        """Test building encounter with discharge disposition."""
        encounter = (
            SimpleEncounterBuilder()
            .encounter_type("Inpatient", "IMP", "ActCode")
            .date(datetime(2023, 10, 10, 8, 0))
            .end_date(datetime(2023, 10, 15, 14, 0))
            .location("General Hospital")
            .performer("Dr. Jane Doe")
            .discharge_disposition("Home")
            .build()
        )

        assert encounter["discharge_disposition"] == "Home"


class TestSimpleSmokingStatusBuilder:
    """Test cases for SimpleSmokingStatusBuilder."""

    def test_smoking_status(self):
        """Test building smoking status data."""
        smoking_status = (
            SimpleSmokingStatusBuilder()
            .status("Current every day smoker", "449868002")
            .date(datetime(2023, 10, 15))
            .build()
        )

        assert smoking_status["smoking_status"] == "Current every day smoker"
        assert smoking_status["code"] == "449868002"


class TestConvenienceFunctions:
    """Test convenience builder functions."""

    def test_patient_builder_function(self):
        """Test patient_builder() convenience function."""
        builder = patient_builder()
        assert isinstance(builder, SimplePatientBuilder)

    def test_problem_builder_function(self):
        """Test problem_builder() convenience function."""
        builder = problem_builder()
        assert isinstance(builder, SimpleProblemBuilder)

    def test_medication_builder_function(self):
        """Test medication_builder() convenience function."""
        builder = medication_builder()
        assert isinstance(builder, SimpleMedicationBuilder)

    def test_allergy_builder_function(self):
        """Test allergy_builder() convenience function."""
        builder = allergy_builder()
        assert isinstance(builder, SimpleAllergyBuilder)

    def test_immunization_builder_function(self):
        """Test immunization_builder() convenience function."""
        builder = immunization_builder()
        assert isinstance(builder, SimpleImmunizationBuilder)

    def test_vital_sign_builder_function(self):
        """Test vital_sign_builder() convenience function."""
        builder = vital_sign_builder()
        assert isinstance(builder, SimpleVitalSignBuilder)

    def test_vital_signs_organizer_builder_function(self):
        """Test vital_signs_organizer_builder() convenience function."""
        builder = vital_signs_organizer_builder()
        assert isinstance(builder, SimpleVitalSignsOrganizerBuilder)

    def test_procedure_builder_function(self):
        """Test procedure_builder() convenience function."""
        builder = procedure_builder()
        assert isinstance(builder, SimpleProcedureBuilder)

    def test_result_observation_builder_function(self):
        """Test result_observation_builder() convenience function."""
        builder = result_observation_builder()
        assert isinstance(builder, SimpleResultObservationBuilder)

    def test_result_organizer_builder_function(self):
        """Test result_organizer_builder() convenience function."""
        builder = result_organizer_builder()
        assert isinstance(builder, SimpleResultOrganizerBuilder)

    def test_encounter_builder_function(self):
        """Test encounter_builder() convenience function."""
        builder = encounter_builder()
        assert isinstance(builder, SimpleEncounterBuilder)

    def test_smoking_status_builder_function(self):
        """Test smoking_status_builder() convenience function."""
        builder = smoking_status_builder()
        assert isinstance(builder, SimpleSmokingStatusBuilder)
