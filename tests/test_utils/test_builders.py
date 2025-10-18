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
    SimpleSmokingStatusBuilder,
    SimpleVitalSignBuilder,
    medication_builder,
    patient_builder,
    problem_builder,
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
