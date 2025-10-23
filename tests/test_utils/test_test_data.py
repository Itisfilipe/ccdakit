"""Tests for test data generators."""

from datetime import date, datetime

from ccdakit.utils.test_data import SampleDataGenerator


class TestSampleDataGenerator:
    """Tests for SampleDataGenerator class."""

    def test_init_without_seed(self):
        """Test generator initialization without seed."""
        gen = SampleDataGenerator()
        assert gen.faker is not None
        assert gen.seed is None

    def test_init_with_seed(self):
        """Test generator initialization with seed for reproducibility."""
        gen = SampleDataGenerator(seed=42)
        assert gen.faker is not None
        assert gen.seed == 42

    def test_different_seeds_produce_different_data(self):
        """Test that different seeds produce different data."""
        gen1 = SampleDataGenerator(seed=42)
        gen2 = SampleDataGenerator(seed=43)

        patient1 = gen1.generate_patient()
        patient2 = gen2.generate_patient()

        # Very unlikely to have same name with different seeds
        assert (
            patient1["first_name"] != patient2["first_name"]
            or patient1["last_name"] != patient2["last_name"]
        )


class TestGenerateAddress:
    """Tests for generate_address method."""

    def test_generate_address_structure(self):
        """Test that generated address has correct structure."""
        gen = SampleDataGenerator(seed=42)
        address = gen.generate_address()

        assert "street_lines" in address
        assert "city" in address
        assert "state" in address
        assert "postal_code" in address
        assert "country" in address
        assert "use" in address

    def test_generate_address_types(self):
        """Test that generated address has correct data types."""
        gen = SampleDataGenerator(seed=42)
        address = gen.generate_address()

        assert isinstance(address["street_lines"], list)
        assert len(address["street_lines"]) > 0
        assert isinstance(address["city"], str)
        assert isinstance(address["state"], str)
        assert isinstance(address["postal_code"], str)
        assert address["country"] == "US"
        assert address["use"] in ["HP", "WP"]


class TestGenerateTelecom:
    """Tests for generate_telecom method."""

    def test_generate_telecom_structure(self):
        """Test that generated telecom has correct structure."""
        gen = SampleDataGenerator(seed=42)
        telecom = gen.generate_telecom()

        assert "type" in telecom
        assert "value" in telecom
        assert "use" in telecom

    def test_generate_telecom_types(self):
        """Test that generated telecom has correct types."""
        gen = SampleDataGenerator(seed=42)

        # Generate multiple to test both phone and email
        telecoms = [gen.generate_telecom() for _ in range(10)]

        has_phone = any(t["type"] == "phone" for t in telecoms)
        has_email = any(t["type"] == "email" for t in telecoms)

        assert has_phone or has_email  # At least one type should be generated

        for telecom in telecoms:
            assert telecom["type"] in ["phone", "email"]
            if telecom["type"] == "phone":
                assert telecom["value"].startswith("tel:")
                assert telecom["use"] in ["HP", "WP", "MC"]
            else:
                assert telecom["value"].startswith("mailto:")
                assert telecom["use"] in ["HP", "WP"]


class TestGeneratePatient:
    """Tests for generate_patient method."""

    def test_generate_patient_structure(self):
        """Test that generated patient has correct structure."""
        gen = SampleDataGenerator(seed=42)
        patient = gen.generate_patient()

        required_fields = [
            "first_name",
            "last_name",
            "middle_name",
            "date_of_birth",
            "sex",
            "race",
            "ethnicity",
            "language",
            "ssn",
            "addresses",
            "telecoms",
            "marital_status",
        ]

        for field in required_fields:
            assert field in patient

    def test_generate_patient_types(self):
        """Test that generated patient has correct data types."""
        gen = SampleDataGenerator(seed=42)
        patient = gen.generate_patient()

        assert isinstance(patient["first_name"], str)
        assert isinstance(patient["last_name"], str)
        assert patient["middle_name"] is None or isinstance(patient["middle_name"], str)
        assert isinstance(patient["date_of_birth"], date)
        assert patient["sex"] in ["M", "F"]
        assert isinstance(patient["addresses"], list)
        assert len(patient["addresses"]) > 0
        assert isinstance(patient["telecoms"], list)
        assert len(patient["telecoms"]) > 0

    def test_generate_patient_age_range(self):
        """Test that generated patients are within expected age range."""
        gen = SampleDataGenerator(seed=42)
        today = date.today()

        for _ in range(10):
            patient = gen.generate_patient()
            age = (today - patient["date_of_birth"]).days / 365.25
            assert 18 <= age <= 90


class TestGenerateProblem:
    """Tests for generate_problem method."""

    def test_generate_problem_structure(self):
        """Test that generated problem has correct structure."""
        gen = SampleDataGenerator(seed=42)
        problem = gen.generate_problem()

        required_fields = [
            "name",
            "code",
            "code_system",
            "status",
            "onset_date",
            "resolved_date",
            "persistent_id",
        ]

        for field in required_fields:
            assert field in problem

    def test_generate_problem_types(self):
        """Test that generated problem has correct data types."""
        gen = SampleDataGenerator(seed=42)
        problem = gen.generate_problem()

        assert isinstance(problem["name"], str)
        assert isinstance(problem["code"], str)
        assert problem["code_system"] in ["SNOMED", "ICD-10"]
        assert problem["status"] in ["active", "inactive", "resolved"]
        assert isinstance(problem["onset_date"], date)
        assert problem["resolved_date"] is None or isinstance(problem["resolved_date"], date)

    def test_generate_problem_resolved_logic(self):
        """Test that resolved problems have resolved_date."""
        gen = SampleDataGenerator(seed=42)

        # Generate many to get some resolved ones
        problems = [gen.generate_problem() for _ in range(20)]
        resolved_problems = [p for p in problems if p["status"] == "resolved"]

        if resolved_problems:
            for problem in resolved_problems:
                assert problem["resolved_date"] is not None
                assert problem["resolved_date"] >= problem["onset_date"]

    def test_generate_problem_from_common_list(self):
        """Test that generated problems are from the common list."""
        gen = SampleDataGenerator(seed=42)
        problem = gen.generate_problem()

        problem_names = [p[0] for p in SampleDataGenerator.COMMON_PROBLEMS]
        assert problem["name"] in problem_names


class TestGenerateMedication:
    """Tests for generate_medication method."""

    def test_generate_medication_structure(self):
        """Test that generated medication has correct structure."""
        gen = SampleDataGenerator(seed=42)
        medication = gen.generate_medication()

        required_fields = [
            "name",
            "code",
            "dosage",
            "route",
            "frequency",
            "start_date",
            "end_date",
            "status",
            "instructions",
        ]

        for field in required_fields:
            assert field in medication

    def test_generate_medication_types(self):
        """Test that generated medication has correct data types."""
        gen = SampleDataGenerator(seed=42)
        medication = gen.generate_medication()

        assert isinstance(medication["name"], str)
        assert isinstance(medication["code"], str)
        assert isinstance(medication["dosage"], str)
        assert isinstance(medication["route"], str)
        assert isinstance(medication["frequency"], str)
        assert isinstance(medication["start_date"], date)
        assert medication["end_date"] is None or isinstance(medication["end_date"], date)
        assert medication["status"] in ["active", "completed", "discontinued"]
        assert medication["instructions"] is None or isinstance(medication["instructions"], str)

    def test_generate_medication_completed_has_end_date(self):
        """Test that completed medications have end_date."""
        gen = SampleDataGenerator(seed=42)

        # Generate many to get some completed ones
        medications = [gen.generate_medication() for _ in range(20)]
        completed_meds = [m for m in medications if m["status"] in ["completed", "discontinued"]]

        if completed_meds:
            for med in completed_meds:
                assert med["end_date"] is not None
                assert med["end_date"] >= med["start_date"]


class TestGenerateAllergy:
    """Tests for generate_allergy method."""

    def test_generate_allergy_structure(self):
        """Test that generated allergy has correct structure."""
        gen = SampleDataGenerator(seed=42)
        allergy = gen.generate_allergy()

        required_fields = [
            "allergen",
            "allergen_code",
            "allergen_code_system",
            "allergy_type",
            "reaction",
            "severity",
            "status",
            "onset_date",
        ]

        for field in required_fields:
            assert field in allergy

    def test_generate_allergy_types(self):
        """Test that generated allergy has correct data types."""
        gen = SampleDataGenerator(seed=42)
        allergy = gen.generate_allergy()

        assert isinstance(allergy["allergen"], str)
        assert isinstance(allergy["allergen_code"], str)
        assert allergy["allergen_code_system"] in ["RxNorm", "SNOMED"]
        assert allergy["allergy_type"] in ["allergy", "intolerance"]
        assert isinstance(allergy["reaction"], str)
        assert allergy["severity"] in ["mild", "moderate", "severe"]
        assert allergy["status"] in ["active", "resolved"]
        assert allergy["onset_date"] is None or isinstance(allergy["onset_date"], date)


class TestGenerateVitalSigns:
    """Tests for generate_vital_signs method."""

    def test_generate_vital_signs_structure(self):
        """Test that generated vital signs has correct structure."""
        gen = SampleDataGenerator(seed=42)
        vital_signs = gen.generate_vital_signs()

        assert "date" in vital_signs
        assert "vital_signs" in vital_signs
        assert isinstance(vital_signs["vital_signs"], list)
        assert len(vital_signs["vital_signs"]) > 0

    def test_generate_vital_signs_observation_structure(self):
        """Test that each vital sign observation has correct structure."""
        gen = SampleDataGenerator(seed=42)
        vital_signs = gen.generate_vital_signs()

        for sign in vital_signs["vital_signs"]:
            assert "type" in sign
            assert "code" in sign
            assert "value" in sign
            assert "unit" in sign
            assert "date" in sign
            assert "interpretation" in sign

    def test_generate_vital_signs_types(self):
        """Test that vital signs have correct data types."""
        gen = SampleDataGenerator(seed=42)
        vital_signs = gen.generate_vital_signs()

        assert isinstance(vital_signs["date"], datetime)

        for sign in vital_signs["vital_signs"]:
            assert isinstance(sign["type"], str)
            assert isinstance(sign["code"], str)
            assert isinstance(sign["value"], str)
            assert isinstance(sign["unit"], str)
            assert isinstance(sign["date"], datetime)
            assert sign["interpretation"] is None or sign["interpretation"] in [
                "Normal",
                "High",
                "Low",
            ]

    def test_generate_vital_signs_with_count(self):
        """Test generating specific number of vital signs."""
        gen = SampleDataGenerator(seed=42)
        vital_signs = gen.generate_vital_signs(count=3)

        assert len(vital_signs["vital_signs"]) == 3

    def test_generate_vital_signs_loinc_codes(self):
        """Test that vital signs use valid LOINC codes."""
        gen = SampleDataGenerator(seed=42)
        vital_signs = gen.generate_vital_signs()

        valid_codes = [v[1] for v in SampleDataGenerator.VITAL_SIGNS_TYPES]
        for sign in vital_signs["vital_signs"]:
            assert sign["code"] in valid_codes


class TestGenerateImmunization:
    """Tests for generate_immunization method."""

    def test_generate_immunization_structure(self):
        """Test that generated immunization has correct structure."""
        gen = SampleDataGenerator(seed=42)
        immunization = gen.generate_immunization()

        required_fields = [
            "vaccine_name",
            "cvx_code",
            "administration_date",
            "status",
            "lot_number",
            "manufacturer",
            "route",
            "site",
            "dose_quantity",
        ]

        for field in required_fields:
            assert field in immunization

    def test_generate_immunization_types(self):
        """Test that generated immunization has correct data types."""
        gen = SampleDataGenerator(seed=42)
        immunization = gen.generate_immunization()

        assert isinstance(immunization["vaccine_name"], str)
        assert isinstance(immunization["cvx_code"], str)
        assert isinstance(immunization["administration_date"], date)
        assert immunization["status"] in ["completed", "refused"]
        assert immunization["lot_number"] is None or isinstance(immunization["lot_number"], str)
        assert immunization["manufacturer"] is None or isinstance(immunization["manufacturer"], str)
        assert isinstance(immunization["route"], str)
        assert isinstance(immunization["site"], str)
        assert immunization["dose_quantity"] is None or isinstance(
            immunization["dose_quantity"], str
        )

    def test_generate_immunization_completed_has_details(self):
        """Test that completed immunizations have more details."""
        gen = SampleDataGenerator(seed=42)

        # Generate many to get some completed ones with details
        immunizations = [gen.generate_immunization() for _ in range(20)]
        completed = [i for i in immunizations if i["status"] == "completed"]

        # At least some completed ones should have lot numbers
        has_lot_numbers = any(i["lot_number"] is not None for i in completed)
        assert has_lot_numbers


class TestGenerateCompletePatientRecord:
    """Tests for generate_complete_patient_record method."""

    def test_generate_complete_record_structure(self):
        """Test that complete record has all required sections."""
        gen = SampleDataGenerator(seed=42)
        record = gen.generate_complete_patient_record()

        required_sections = [
            "patient",
            "problems",
            "medications",
            "allergies",
            "vital_signs",
            "immunizations",
        ]

        for section in required_sections:
            assert section in record

    def test_generate_complete_record_types(self):
        """Test that complete record sections have correct types."""
        gen = SampleDataGenerator(seed=42)
        record = gen.generate_complete_patient_record()

        assert isinstance(record["patient"], dict)
        assert isinstance(record["problems"], list)
        assert isinstance(record["medications"], list)
        assert isinstance(record["allergies"], list)
        assert isinstance(record["vital_signs"], list)
        assert isinstance(record["immunizations"], list)

    def test_generate_complete_record_default_counts(self):
        """Test that complete record uses default counts."""
        gen = SampleDataGenerator(seed=42)
        record = gen.generate_complete_patient_record()

        assert len(record["problems"]) == 3
        assert len(record["medications"]) == 2
        assert len(record["allergies"]) == 2
        assert len(record["vital_signs"]) == 1
        assert len(record["immunizations"]) == 3

    def test_generate_complete_record_custom_counts(self):
        """Test that complete record respects custom counts."""
        gen = SampleDataGenerator(seed=42)
        record = gen.generate_complete_patient_record(
            num_problems=5,
            num_medications=4,
            num_allergies=3,
            num_vital_signs_sets=2,
            num_immunizations=6,
        )

        assert len(record["problems"]) == 5
        assert len(record["medications"]) == 4
        assert len(record["allergies"]) == 3
        assert len(record["vital_signs"]) == 2
        assert len(record["immunizations"]) == 6

    def test_generate_complete_record_integration(self):
        """Test that all sections are properly generated with valid data."""
        gen = SampleDataGenerator(seed=42)
        record = gen.generate_complete_patient_record()

        # Verify patient
        assert record["patient"]["first_name"]
        assert record["patient"]["last_name"]

        # Verify problems
        for problem in record["problems"]:
            assert problem["code"]
            assert problem["code_system"] in ["SNOMED", "ICD-10"]

        # Verify medications
        for med in record["medications"]:
            assert med["code"]
            assert med["dosage"]

        # Verify allergies
        for allergy in record["allergies"]:
            assert allergy["allergen"]
            assert allergy["allergen_code"]

        # Verify vital signs
        for vs_set in record["vital_signs"]:
            assert len(vs_set["vital_signs"]) > 0

        # Verify immunizations
        for imm in record["immunizations"]:
            assert imm["vaccine_name"]
            assert imm["cvx_code"]


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_generate_empty_patient_record(self):
        """Test generating a patient record with no clinical data."""
        gen = SampleDataGenerator(seed=42)
        record = gen.generate_complete_patient_record(
            num_problems=0,
            num_medications=0,
            num_allergies=0,
            num_vital_signs_sets=0,
            num_immunizations=0,
        )

        assert record["patient"] is not None
        assert len(record["problems"]) == 0
        assert len(record["medications"]) == 0
        assert len(record["allergies"]) == 0
        assert len(record["vital_signs"]) == 0
        assert len(record["immunizations"]) == 0

    def test_generate_large_patient_record(self):
        """Test generating a patient record with many entries."""
        gen = SampleDataGenerator(seed=42)
        record = gen.generate_complete_patient_record(
            num_problems=20,
            num_medications=15,
            num_allergies=10,
            num_vital_signs_sets=5,
            num_immunizations=15,
        )

        assert len(record["problems"]) == 20
        assert len(record["medications"]) == 15
        assert len(record["allergies"]) == 10
        assert len(record["vital_signs"]) == 5
        assert len(record["immunizations"]) == 15
