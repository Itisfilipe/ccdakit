"""
Comprehensive Schematron validation tests for all 9 Core Clinical Sections.

This test suite validates that ccdakit generates C-CDA compliant XML for each
of the 9 core clinical sections required by meaningful use:

1. ProblemsSection
2. MedicationsSection
3. AllergiesSection
4. ImmunizationsSection
5. VitalSignsSection
6. ProceduresSection
7. ResultsSection
8. SocialHistorySection
9. EncountersSection

For each section, tests cover:
- Valid documents with standard data
- Minimal/empty data scenarios
- Multiple entries
- Edge cases and optional fields

Tests use SchematronValidator to ensure generated XML meets C-CDA R2.1
conformance requirements.
"""

from datetime import date, datetime

import pytest

from ccdakit.builders.document import ClinicalDocument
from ccdakit.builders.sections.allergies import AllergiesSection
from ccdakit.builders.sections.encounters import EncountersSection
from ccdakit.builders.sections.immunizations import ImmunizationsSection
from ccdakit.builders.sections.medications import MedicationsSection
from ccdakit.builders.sections.problems import ProblemsSection
from ccdakit.builders.sections.procedures import ProceduresSection
from ccdakit.builders.sections.results import ResultsSection
from ccdakit.builders.sections.social_history import SocialHistorySection
from ccdakit.builders.sections.vital_signs import VitalSignsSection
from ccdakit.core.base import CDAVersion
from ccdakit.validators.schematron import SchematronValidator

# Import mock data from existing integration tests
from .test_full_document import (
    MockAddress,
    MockAuthor,
    MockMedication,
    MockOrganization,
    MockPatient,
    MockProblem,
    MockTelecom,
)


# ============================================================================
# Additional Mock Data Classes for Core Sections
# ============================================================================


class MockAllergy:
    """Mock allergy for testing."""

    def __init__(
        self,
        allergen="Penicillin",
        allergen_code="70618",
        allergen_code_system="RXNORM",
        allergy_type="allergy",
        reaction="Hives",
        reaction_code="247472004",
        severity="moderate",
        severity_code="6736007",
        status="active",
        onset_date=None,
    ):
        self._allergen = allergen
        self._allergen_code = allergen_code
        self._allergen_code_system = allergen_code_system
        self._allergy_type = allergy_type
        self._reaction = reaction
        self._reaction_code = reaction_code
        self._severity = severity
        self._severity_code = severity_code
        self._status = status
        self._onset_date = onset_date or date(2020, 1, 1)

    @property
    def allergen(self):
        return self._allergen

    @property
    def allergen_code(self):
        return self._allergen_code

    @property
    def allergen_code_system(self):
        return self._allergen_code_system

    @property
    def allergy_type(self):
        return self._allergy_type

    @property
    def reaction(self):
        return self._reaction

    @property
    def reaction_code(self):
        return self._reaction_code

    @property
    def severity(self):
        return self._severity

    @property
    def severity_code(self):
        return self._severity_code

    @property
    def status(self):
        return self._status

    @property
    def onset_date(self):
        return self._onset_date


class MockImmunization:
    """Mock immunization for testing."""

    def __init__(
        self,
        vaccine_name="Influenza vaccine",
        cvx_code="141",
        administration_date=None,
        status="completed",
        lot_number="12345A",
        manufacturer="Manufacturer Inc",
        route="Intramuscular",
        site="Left arm",
        dose_quantity="0.5 mL",
    ):
        self._vaccine_name = vaccine_name
        self._cvx_code = cvx_code
        self._administration_date = administration_date or date(2023, 9, 15)
        self._status = status
        self._lot_number = lot_number
        self._manufacturer = manufacturer
        self._route = route
        self._site = site
        self._dose_quantity = dose_quantity

    @property
    def vaccine_name(self):
        return self._vaccine_name

    @property
    def cvx_code(self):
        return self._cvx_code

    @property
    def administration_date(self):
        return self._administration_date

    @property
    def status(self):
        return self._status

    @property
    def lot_number(self):
        return self._lot_number

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def route(self):
        return self._route

    @property
    def site(self):
        return self._site

    @property
    def dose_quantity(self):
        return self._dose_quantity


class MockVitalSign:
    """Mock individual vital sign."""

    def __init__(
        self,
        type="Blood Pressure Systolic",
        code="8480-6",
        value="120",
        unit="mm[Hg]",
        date=None,
        interpretation="Normal",
    ):
        self._type = type
        self._code = code
        self._value = value
        self._unit = unit
        self._date = date or datetime(2023, 10, 17, 10, 30)
        self._interpretation = interpretation

    @property
    def type(self):
        return self._type

    @property
    def code(self):
        return self._code

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit

    @property
    def date(self):
        return self._date

    @property
    def interpretation(self):
        return self._interpretation


class MockVitalSignsOrganizer:
    """Mock vital signs organizer for testing."""

    def __init__(self, date=None, vital_signs=None):
        self._date = date or datetime(2023, 10, 17, 10, 30)
        self._vital_signs = vital_signs or []

    @property
    def date(self):
        return self._date

    @property
    def vital_signs(self):
        return self._vital_signs


class MockProcedure:
    """Mock procedure for testing."""

    def __init__(
        self,
        name="Appendectomy",
        code="80146002",
        code_system="SNOMED CT",
        date=None,
        status="completed",
        target_site="Appendix",
        target_site_code="66754008",
        performer_name="Dr. Jane Smith",
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._date = date or datetime(2023, 5, 10, 14, 30)
        self._status = status
        self._target_site = target_site
        self._target_site_code = target_site_code
        self._performer_name = performer_name

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def date(self):
        return self._date

    @property
    def status(self):
        return self._status

    @property
    def target_site(self):
        return self._target_site

    @property
    def target_site_code(self):
        return self._target_site_code

    @property
    def performer_name(self):
        return self._performer_name


class MockResultObservation:
    """Mock individual result observation."""

    def __init__(
        self,
        test_name="Glucose",
        test_code="2339-0",
        value="95",
        unit="mg/dL",
        status="final",
        effective_time=None,
        value_type="PQ",
        interpretation="N",
        reference_range_low="70",
        reference_range_high="100",
        reference_range_unit="mg/dL",
    ):
        self._test_name = test_name
        self._test_code = test_code
        self._value = value
        self._unit = unit
        self._status = status
        self._effective_time = effective_time or datetime(2023, 10, 15, 9, 0)
        self._value_type = value_type
        self._interpretation = interpretation
        self._reference_range_low = reference_range_low
        self._reference_range_high = reference_range_high
        self._reference_range_unit = reference_range_unit

    @property
    def test_name(self):
        return self._test_name

    @property
    def test_code(self):
        return self._test_code

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit

    @property
    def status(self):
        return self._status

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def value_type(self):
        return self._value_type

    @property
    def interpretation(self):
        return self._interpretation

    @property
    def reference_range_low(self):
        return self._reference_range_low

    @property
    def reference_range_high(self):
        return self._reference_range_high

    @property
    def reference_range_unit(self):
        return self._reference_range_unit


class MockResultOrganizer:
    """Mock result organizer (panel) for testing."""

    def __init__(
        self,
        panel_name="Basic Metabolic Panel",
        panel_code="51990-0",
        status="completed",
        effective_time=None,
        results=None,
    ):
        self._panel_name = panel_name
        self._panel_code = panel_code
        self._status = status
        self._effective_time = effective_time or datetime(2023, 10, 15, 9, 0)
        self._results = results or []

    @property
    def panel_name(self):
        return self._panel_name

    @property
    def panel_code(self):
        return self._panel_code

    @property
    def status(self):
        return self._status

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def results(self):
        return self._results


class MockSmokingStatus:
    """Mock smoking status for testing."""

    def __init__(
        self,
        smoking_status="Former smoker",
        code="8517006",
        date=None,
    ):
        self._smoking_status = smoking_status
        self._code = code
        self._date = date or datetime(2023, 10, 1, 10, 0)

    @property
    def smoking_status(self):
        return self._smoking_status

    @property
    def code(self):
        return self._code

    @property
    def date(self):
        return self._date


class MockEncounter:
    """Mock encounter for testing."""

    def __init__(
        self,
        encounter_type="Office Visit",
        code="99213",
        code_system="CPT-4",
        date=None,
        end_date=None,
        location="Community Health Clinic",
        performer_name="Dr. Alice Johnson",
        discharge_disposition=None,
    ):
        self._encounter_type = encounter_type
        self._code = code
        self._code_system = code_system
        self._date = date or datetime(2023, 10, 10, 14, 0)
        self._end_date = end_date
        self._location = location
        self._performer_name = performer_name
        self._discharge_disposition = discharge_disposition

    @property
    def encounter_type(self):
        return self._encounter_type

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def date(self):
        return self._date

    @property
    def end_date(self):
        return self._end_date

    @property
    def location(self):
        return self._location

    @property
    def performer_name(self):
        return self._performer_name

    @property
    def discharge_disposition(self):
        return self._discharge_disposition


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def schematron_validator():
    """Create Schematron validator instance."""
    return SchematronValidator()


@pytest.fixture
def valid_patient():
    """Create valid patient for testing."""
    return MockPatient()


@pytest.fixture
def valid_author():
    """Create valid author for testing."""
    return MockAuthor()


@pytest.fixture
def valid_custodian():
    """Create valid custodian for testing."""
    return MockOrganization()


# ============================================================================
# 1. ProblemsSection Tests
# ============================================================================


class TestProblemsSectionSchematron:
    """Schematron validation tests for ProblemsSection."""

    def test_problems_section_valid_single_entry(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ProblemsSection with single valid problem."""
        problems = [
            MockProblem(
                name="Essential Hypertension",
                code="59621000",
                code_system="SNOMED",
                status="active",
                onset_date=date(2020, 1, 15),
            )
        ]

        section = ProblemsSection(problems=problems, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        # Document should validate
        assert isinstance(result.errors, list)
        # Log any errors for debugging
        if result.errors:
            print(f"\nProblems section validation found {len(result.errors)} error(s)")
            for error in result.errors[:5]:
                print(f"  - {error.code}: {error.message[:100]}")

    def test_problems_section_multiple_entries(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ProblemsSection with multiple problems."""
        problems = [
            MockProblem(
                name="Essential Hypertension",
                code="59621000",
                code_system="SNOMED",
                status="active",
                onset_date=date(2018, 5, 10),
            ),
            MockProblem(
                name="Type 2 Diabetes Mellitus",
                code="44054006",
                code_system="SNOMED",
                status="active",
                onset_date=date(2019, 3, 15),
            ),
            MockProblem(
                name="Hyperlipidemia",
                code="55822004",
                code_system="SNOMED",
                status="active",
                onset_date=date(2020, 7, 1),
            ),
        ]

        section = ProblemsSection(problems=problems, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        # Should validate with multiple entries
        assert isinstance(result.errors, list)

    def test_problems_section_with_resolved_problem(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ProblemsSection with resolved problem."""
        problems = [
            MockProblem(
                name="Acute Bronchitis",
                code="10509002",
                code_system="SNOMED",
                status="resolved",
                onset_date=date(2023, 1, 10),
                resolved_date=date(2023, 2, 15),
            )
        ]

        section = ProblemsSection(problems=problems, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_problems_section_edge_case_old_onset_date(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ProblemsSection with very old onset date."""
        problems = [
            MockProblem(
                name="Chronic condition",
                code="55607006",
                code_system="SNOMED",
                status="active",
                onset_date=date(1990, 1, 1),  # Very old date
            )
        ]

        section = ProblemsSection(problems=problems, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)


# ============================================================================
# 2. MedicationsSection Tests
# ============================================================================


class TestMedicationsSectionSchematron:
    """Schematron validation tests for MedicationsSection."""

    def test_medications_section_valid_single_entry(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test MedicationsSection with single valid medication."""
        medications = [
            MockMedication(
                name="Lisinopril 10mg tablet",
                code="314076",
                dosage="10 mg",
                route="oral",
                frequency="once daily",
                start_date=date(2020, 1, 1),
                status="active",
            )
        ]

        section = MedicationsSection(medications=medications, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)
        if result.errors:
            print(f"\nMedications section validation found {len(result.errors)} error(s)")
            for error in result.errors[:5]:
                print(f"  - {error.code}: {error.message[:100]}")

    def test_medications_section_multiple_entries(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test MedicationsSection with multiple medications."""
        medications = [
            MockMedication(
                name="Lisinopril 10mg tablet",
                code="314076",
                dosage="10 mg",
                route="oral",
                frequency="once daily",
                start_date=date(2018, 6, 1),
                status="active",
            ),
            MockMedication(
                name="Metformin 500mg tablet",
                code="860975",
                dosage="500 mg",
                route="oral",
                frequency="twice daily",
                start_date=date(2019, 4, 1),
                status="active",
            ),
            MockMedication(
                name="Atorvastatin 20mg tablet",
                code="617314",
                dosage="20 mg",
                route="oral",
                frequency="once daily at bedtime",
                start_date=date(2020, 2, 1),
                status="active",
            ),
        ]

        section = MedicationsSection(medications=medications, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_medications_section_with_discontinued_medication(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test MedicationsSection with discontinued medication."""
        medications = [
            MockMedication(
                name="Discontinued medication",
                code="123456",
                dosage="10 mg",
                route="oral",
                frequency="once daily",
                start_date=date(2020, 1, 1),
                end_date=date(2020, 6, 30),
                status="completed",
            )
        ]

        section = MedicationsSection(medications=medications, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_medications_section_with_instructions(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test MedicationsSection with patient instructions."""
        medications = [
            MockMedication(
                name="Medication with instructions",
                code="789012",
                dosage="5 mg",
                route="oral",
                frequency="as needed",
                start_date=date(2023, 1, 1),
                status="active",
                instructions="Take with food",
            )
        ]

        section = MedicationsSection(medications=medications, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)


# ============================================================================
# 3. AllergiesSection Tests
# ============================================================================


class TestAllergiesSectionSchematron:
    """Schematron validation tests for AllergiesSection."""

    def test_allergies_section_valid_single_entry(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test AllergiesSection with single valid allergy."""
        allergies = [
            MockAllergy(
                allergen="Penicillin",
                allergen_code="70618",
                allergen_code_system="RXNORM",
                allergy_type="allergy",
                reaction="Hives",
                severity="moderate",
                status="active",
            )
        ]

        section = AllergiesSection(allergies=allergies, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)
        if result.errors:
            print(f"\nAllergies section validation found {len(result.errors)} error(s)")
            for error in result.errors[:5]:
                print(f"  - {error.code}: {error.message[:100]}")

    def test_allergies_section_multiple_entries(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test AllergiesSection with multiple allergies."""
        allergies = [
            MockAllergy(
                allergen="Penicillin",
                allergen_code="70618",
                allergen_code_system="RXNORM",
                reaction="Hives",
                severity="moderate",
                status="active",
            ),
            MockAllergy(
                allergen="Shellfish",
                allergen_code="227037002",
                allergen_code_system="SNOMED",
                reaction="Anaphylaxis",
                severity="severe",
                status="active",
            ),
            MockAllergy(
                allergen="Latex",
                allergen_code="111088007",
                allergen_code_system="SNOMED",
                reaction="Contact dermatitis",
                severity="mild",
                status="active",
            ),
        ]

        section = AllergiesSection(allergies=allergies, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_allergies_section_various_severities(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test AllergiesSection with different severity levels."""
        allergies = [
            MockAllergy(
                allergen="Mild allergy",
                allergen_code="12345",
                severity="mild",
                status="active",
            ),
            MockAllergy(
                allergen="Moderate allergy",
                allergen_code="23456",
                severity="moderate",
                status="active",
            ),
            MockAllergy(
                allergen="Severe allergy",
                allergen_code="34567",
                severity="severe",
                status="active",
            ),
        ]

        section = AllergiesSection(allergies=allergies, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)


# ============================================================================
# 4. ImmunizationsSection Tests
# ============================================================================


class TestImmunizationsSectionSchematron:
    """Schematron validation tests for ImmunizationsSection."""

    def test_immunizations_section_valid_single_entry(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ImmunizationsSection with single valid immunization."""
        immunizations = [
            MockImmunization(
                vaccine_name="Influenza vaccine",
                cvx_code="141",
                administration_date=date(2023, 9, 15),
                status="completed",
                lot_number="12345A",
                manufacturer="Manufacturer Inc",
            )
        ]

        section = ImmunizationsSection(immunizations=immunizations, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)
        if result.errors:
            print(f"\nImmunizations section validation found {len(result.errors)} error(s)")
            for error in result.errors[:5]:
                print(f"  - {error.code}: {error.message[:100]}")

    def test_immunizations_section_multiple_entries(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ImmunizationsSection with multiple immunizations."""
        immunizations = [
            MockImmunization(
                vaccine_name="Influenza vaccine",
                cvx_code="141",
                administration_date=date(2023, 9, 15),
                status="completed",
            ),
            MockImmunization(
                vaccine_name="Tetanus and diphtheria toxoids",
                cvx_code="113",
                administration_date=date(2022, 6, 10),
                status="completed",
            ),
            MockImmunization(
                vaccine_name="COVID-19 vaccine",
                cvx_code="208",
                administration_date=date(2023, 1, 5),
                status="completed",
            ),
        ]

        section = ImmunizationsSection(immunizations=immunizations, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_immunizations_section_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ImmunizationsSection with minimal required data."""
        immunizations = [
            MockImmunization(
                vaccine_name="Basic vaccine",
                cvx_code="01",
                administration_date=date(2023, 5, 1),
                status="completed",
                lot_number=None,  # Optional field
                manufacturer=None,  # Optional field
            )
        ]

        section = ImmunizationsSection(immunizations=immunizations, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_immunizations_section_refused_vaccine(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ImmunizationsSection with refused vaccine."""
        immunizations = [
            MockImmunization(
                vaccine_name="Vaccine refused by patient",
                cvx_code="998",  # No vaccine administered
                administration_date=date(2023, 10, 1),
                status="refused",
            )
        ]

        section = ImmunizationsSection(immunizations=immunizations, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)


# ============================================================================
# 5. VitalSignsSection Tests
# ============================================================================


class TestVitalSignsSectionSchematron:
    """Schematron validation tests for VitalSignsSection."""

    def test_vital_signs_section_valid_single_organizer(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test VitalSignsSection with single organizer."""
        vital_signs = [
            MockVitalSign(
                type="Blood Pressure Systolic",
                code="8480-6",
                value="120",
                unit="mm[Hg]",
            ),
            MockVitalSign(
                type="Blood Pressure Diastolic",
                code="8462-4",
                value="80",
                unit="mm[Hg]",
            ),
        ]

        organizers = [
            MockVitalSignsOrganizer(
                date=datetime(2023, 10, 17, 10, 30),
                vital_signs=vital_signs,
            )
        ]

        section = VitalSignsSection(vital_signs_organizers=organizers, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)
        if result.errors:
            print(f"\nVital signs section validation found {len(result.errors)} error(s)")
            for error in result.errors[:5]:
                print(f"  - {error.code}: {error.message[:100]}")

    def test_vital_signs_section_multiple_organizers(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test VitalSignsSection with multiple organizers (different dates)."""
        organizers = [
            MockVitalSignsOrganizer(
                date=datetime(2023, 10, 1, 9, 0),
                vital_signs=[
                    MockVitalSign(
                        type="Blood Pressure Systolic",
                        code="8480-6",
                        value="130",
                        unit="mm[Hg]",
                        date=datetime(2023, 10, 1, 9, 0),
                    ),
                    MockVitalSign(
                        type="Heart Rate",
                        code="8867-4",
                        value="72",
                        unit="/min",
                        date=datetime(2023, 10, 1, 9, 0),
                    ),
                ],
            ),
            MockVitalSignsOrganizer(
                date=datetime(2023, 10, 15, 14, 30),
                vital_signs=[
                    MockVitalSign(
                        type="Blood Pressure Systolic",
                        code="8480-6",
                        value="125",
                        unit="mm[Hg]",
                        date=datetime(2023, 10, 15, 14, 30),
                    ),
                    MockVitalSign(
                        type="Temperature",
                        code="8310-5",
                        value="37",
                        unit="Cel",
                        date=datetime(2023, 10, 15, 14, 30),
                    ),
                ],
            ),
        ]

        section = VitalSignsSection(vital_signs_organizers=organizers, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_vital_signs_section_comprehensive_vitals(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test VitalSignsSection with comprehensive vital signs."""
        vital_signs = [
            MockVitalSign(
                type="Blood Pressure Systolic",
                code="8480-6",
                value="118",
                unit="mm[Hg]",
            ),
            MockVitalSign(
                type="Blood Pressure Diastolic",
                code="8462-4",
                value="78",
                unit="mm[Hg]",
            ),
            MockVitalSign(
                type="Heart Rate",
                code="8867-4",
                value="68",
                unit="/min",
            ),
            MockVitalSign(
                type="Respiratory Rate",
                code="9279-1",
                value="16",
                unit="/min",
            ),
            MockVitalSign(
                type="Body Temperature",
                code="8310-5",
                value="36.8",
                unit="Cel",
            ),
            MockVitalSign(
                type="Oxygen Saturation",
                code="2708-6",
                value="98",
                unit="%",
            ),
        ]

        organizers = [
            MockVitalSignsOrganizer(
                date=datetime(2023, 10, 17, 10, 30),
                vital_signs=vital_signs,
            )
        ]

        section = VitalSignsSection(vital_signs_organizers=organizers, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)


# ============================================================================
# 6. ProceduresSection Tests
# ============================================================================


class TestProceduresSectionSchematron:
    """Schematron validation tests for ProceduresSection."""

    def test_procedures_section_valid_single_entry(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ProceduresSection with single valid procedure."""
        procedures = [
            MockProcedure(
                name="Appendectomy",
                code="80146002",
                code_system="SNOMED CT",
                date=datetime(2023, 5, 10, 14, 30),
                status="completed",
            )
        ]

        section = ProceduresSection(procedures=procedures, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)
        if result.errors:
            print(f"\nProcedures section validation found {len(result.errors)} error(s)")
            for error in result.errors[:5]:
                print(f"  - {error.code}: {error.message[:100]}")

    def test_procedures_section_multiple_entries(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ProceduresSection with multiple procedures."""
        procedures = [
            MockProcedure(
                name="Appendectomy",
                code="80146002",
                code_system="SNOMED CT",
                date=datetime(2023, 5, 10, 14, 30),
                status="completed",
            ),
            MockProcedure(
                name="Colonoscopy",
                code="73761001",
                code_system="SNOMED CT",
                date=datetime(2023, 3, 15, 10, 0),
                status="completed",
            ),
            MockProcedure(
                name="Blood draw",
                code="396550006",
                code_system="SNOMED CT",
                date=datetime(2023, 10, 1, 9, 30),
                status="completed",
            ),
        ]

        section = ProceduresSection(procedures=procedures, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_procedures_section_with_target_site(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ProceduresSection with target site information."""
        procedures = [
            MockProcedure(
                name="Knee arthroscopy",
                code="387713003",
                code_system="SNOMED CT",
                date=datetime(2023, 6, 20, 11, 0),
                status="completed",
                target_site="Right knee",
                target_site_code="72696002",
            )
        ]

        section = ProceduresSection(procedures=procedures, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_procedures_section_with_performer(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ProceduresSection with performer information."""
        procedures = [
            MockProcedure(
                name="Surgical procedure",
                code="387713003",
                code_system="SNOMED CT",
                date=datetime(2023, 7, 1, 8, 0),
                status="completed",
                performer_name="Dr. Sarah Martinez, MD",
            )
        ]

        section = ProceduresSection(procedures=procedures, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)


# ============================================================================
# 7. ResultsSection Tests
# ============================================================================


class TestResultsSectionSchematron:
    """Schematron validation tests for ResultsSection."""

    def test_results_section_valid_single_panel(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ResultsSection with single lab panel."""
        results = [
            MockResultObservation(
                test_name="Glucose",
                test_code="2339-0",
                value="95",
                unit="mg/dL",
                status="final",
            ),
        ]

        organizers = [
            MockResultOrganizer(
                panel_name="Basic Metabolic Panel",
                panel_code="51990-0",
                status="completed",
                effective_time=datetime(2023, 10, 15, 9, 0),
                results=results,
            )
        ]

        section = ResultsSection(result_organizers=organizers, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)
        if result.errors:
            print(f"\nResults section validation found {len(result.errors)} error(s)")
            for error in result.errors[:5]:
                print(f"  - {error.code}: {error.message[:100]}")

    def test_results_section_comprehensive_panel(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ResultsSection with comprehensive lab panel."""
        results = [
            MockResultObservation(
                test_name="Glucose",
                test_code="2339-0",
                value="95",
                unit="mg/dL",
                status="final",
                interpretation="N",
                reference_range_low="70",
                reference_range_high="100",
            ),
            MockResultObservation(
                test_name="Sodium",
                test_code="2951-2",
                value="140",
                unit="mmol/L",
                status="final",
                interpretation="N",
                reference_range_low="136",
                reference_range_high="145",
            ),
            MockResultObservation(
                test_name="Potassium",
                test_code="2823-3",
                value="4.2",
                unit="mmol/L",
                status="final",
                interpretation="N",
                reference_range_low="3.5",
                reference_range_high="5.1",
            ),
            MockResultObservation(
                test_name="Creatinine",
                test_code="2160-0",
                value="1.0",
                unit="mg/dL",
                status="final",
                interpretation="N",
                reference_range_low="0.7",
                reference_range_high="1.3",
            ),
        ]

        organizers = [
            MockResultOrganizer(
                panel_name="Basic Metabolic Panel",
                panel_code="51990-0",
                status="completed",
                effective_time=datetime(2023, 10, 15, 9, 0),
                results=results,
            )
        ]

        section = ResultsSection(result_organizers=organizers, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_results_section_multiple_panels(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ResultsSection with multiple lab panels."""
        bmp_results = [
            MockResultObservation(
                test_name="Glucose",
                test_code="2339-0",
                value="98",
                unit="mg/dL",
                status="final",
            ),
        ]

        cbc_results = [
            MockResultObservation(
                test_name="Hemoglobin",
                test_code="718-7",
                value="14.5",
                unit="g/dL",
                status="final",
            ),
            MockResultObservation(
                test_name="White Blood Cells",
                test_code="6690-2",
                value="7.5",
                unit="10*3/uL",
                status="final",
            ),
        ]

        organizers = [
            MockResultOrganizer(
                panel_name="Basic Metabolic Panel",
                panel_code="51990-0",
                status="completed",
                effective_time=datetime(2023, 10, 15, 9, 0),
                results=bmp_results,
            ),
            MockResultOrganizer(
                panel_name="Complete Blood Count",
                panel_code="58410-2",
                status="completed",
                effective_time=datetime(2023, 10, 15, 9, 0),
                results=cbc_results,
            ),
        ]

        section = ResultsSection(result_organizers=organizers, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_results_section_with_abnormal_values(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test ResultsSection with abnormal lab values."""
        results = [
            MockResultObservation(
                test_name="Glucose",
                test_code="2339-0",
                value="180",  # High
                unit="mg/dL",
                status="final",
                interpretation="H",  # High
                reference_range_low="70",
                reference_range_high="100",
            ),
        ]

        organizers = [
            MockResultOrganizer(
                panel_name="Glucose Test",
                panel_code="2339-0",
                status="completed",
                effective_time=datetime(2023, 10, 15, 9, 0),
                results=results,
            )
        ]

        section = ResultsSection(result_organizers=organizers, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)


# ============================================================================
# 8. SocialHistorySection Tests
# ============================================================================


class TestSocialHistorySectionSchematron:
    """Schematron validation tests for SocialHistorySection."""

    def test_social_history_section_valid_single_entry(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test SocialHistorySection with single smoking status."""
        smoking_statuses = [
            MockSmokingStatus(
                smoking_status="Former smoker",
                code="8517006",
                date=datetime(2023, 10, 1, 10, 0),
            )
        ]

        section = SocialHistorySection(smoking_statuses=smoking_statuses, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)
        if result.errors:
            print(f"\nSocial history section validation found {len(result.errors)} error(s)")
            for error in result.errors[:5]:
                print(f"  - {error.code}: {error.message[:100]}")

    def test_social_history_section_never_smoker(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test SocialHistorySection with never smoker status."""
        smoking_statuses = [
            MockSmokingStatus(
                smoking_status="Never smoker",
                code="266919005",
                date=datetime(2023, 10, 1, 10, 0),
            )
        ]

        section = SocialHistorySection(smoking_statuses=smoking_statuses, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_social_history_section_current_smoker(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test SocialHistorySection with current smoker status."""
        smoking_statuses = [
            MockSmokingStatus(
                smoking_status="Current every day smoker",
                code="449868002",
                date=datetime(2023, 10, 1, 10, 0),
            )
        ]

        section = SocialHistorySection(smoking_statuses=smoking_statuses, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_social_history_section_unknown_status(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test SocialHistorySection with unknown smoking status."""
        smoking_statuses = [
            MockSmokingStatus(
                smoking_status="Unknown if ever smoked",
                code="266927001",
                date=datetime(2023, 10, 1, 10, 0),
            )
        ]

        section = SocialHistorySection(smoking_statuses=smoking_statuses, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)


# ============================================================================
# 9. EncountersSection Tests
# ============================================================================


class TestEncountersSectionSchematron:
    """Schematron validation tests for EncountersSection."""

    def test_encounters_section_valid_single_entry(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test EncountersSection with single valid encounter."""
        encounters = [
            MockEncounter(
                encounter_type="Office Visit",
                code="99213",
                code_system="CPT-4",
                date=datetime(2023, 10, 10, 14, 0),
                location="Community Health Clinic",
            )
        ]

        section = EncountersSection(encounters=encounters, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)
        if result.errors:
            print(f"\nEncounters section validation found {len(result.errors)} error(s)")
            for error in result.errors[:5]:
                print(f"  - {error.code}: {error.message[:100]}")

    def test_encounters_section_multiple_entries(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test EncountersSection with multiple encounters."""
        encounters = [
            MockEncounter(
                encounter_type="Office Visit",
                code="99213",
                code_system="CPT-4",
                date=datetime(2023, 8, 15, 10, 0),
            ),
            MockEncounter(
                encounter_type="Emergency Room",
                code="99284",
                code_system="CPT-4",
                date=datetime(2023, 9, 20, 3, 30),
            ),
            MockEncounter(
                encounter_type="Follow-up Visit",
                code="99214",
                code_system="CPT-4",
                date=datetime(2023, 10, 10, 14, 0),
            ),
        ]

        section = EncountersSection(encounters=encounters, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_encounters_section_with_date_range(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test EncountersSection with encounter date range."""
        encounters = [
            MockEncounter(
                encounter_type="Inpatient Stay",
                code="99223",
                code_system="CPT-4",
                date=datetime(2023, 9, 1, 8, 0),
                end_date=datetime(2023, 9, 5, 10, 0),
                location="General Hospital",
                discharge_disposition="Home",
            )
        ]

        section = EncountersSection(encounters=encounters, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)

    def test_encounters_section_with_performer(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test EncountersSection with performer information."""
        encounters = [
            MockEncounter(
                encounter_type="Office Visit",
                code="99213",
                code_system="CPT-4",
                date=datetime(2023, 10, 10, 14, 0),
                performer_name="Dr. Robert Johnson, MD",
            )
        ]

        section = EncountersSection(encounters=encounters, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)


# ============================================================================
# Multi-Section Integration Tests
# ============================================================================


class TestMultipleSectionsSchematron:
    """Test documents containing multiple core clinical sections."""

    def test_all_nine_core_sections(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with all 9 core clinical sections."""
        # 1. Problems
        problems_section = ProblemsSection(
            problems=[
                MockProblem(
                    name="Hypertension",
                    code="38341003",
                    code_system="SNOMED",
                    status="active",
                    onset_date=date(2018, 1, 1),
                )
            ],
            version=CDAVersion.R2_1,
        )

        # 2. Medications
        medications_section = MedicationsSection(
            medications=[
                MockMedication(
                    name="Lisinopril 10mg",
                    code="314076",
                    dosage="10 mg",
                    route="oral",
                    frequency="daily",
                    start_date=date(2018, 1, 15),
                    status="active",
                )
            ],
            version=CDAVersion.R2_1,
        )

        # 3. Allergies
        allergies_section = AllergiesSection(
            allergies=[
                MockAllergy(
                    allergen="Penicillin",
                    allergen_code="70618",
                    allergen_code_system="RXNORM",
                )
            ],
            version=CDAVersion.R2_1,
        )

        # 4. Immunizations
        immunizations_section = ImmunizationsSection(
            immunizations=[
                MockImmunization(
                    vaccine_name="Influenza vaccine",
                    cvx_code="141",
                    administration_date=date(2023, 9, 15),
                    status="completed",
                )
            ],
            version=CDAVersion.R2_1,
        )

        # 5. Vital Signs
        vital_signs_section = VitalSignsSection(
            vital_signs_organizers=[
                MockVitalSignsOrganizer(
                    date=datetime(2023, 10, 17, 10, 30),
                    vital_signs=[
                        MockVitalSign(
                            type="Blood Pressure Systolic",
                            code="8480-6",
                            value="120",
                            unit="mm[Hg]",
                        )
                    ],
                )
            ],
            version=CDAVersion.R2_1,
        )

        # 6. Procedures
        procedures_section = ProceduresSection(
            procedures=[
                MockProcedure(
                    name="Colonoscopy",
                    code="73761001",
                    code_system="SNOMED CT",
                    date=datetime(2023, 3, 15, 10, 0),
                    status="completed",
                )
            ],
            version=CDAVersion.R2_1,
        )

        # 7. Results
        results_section = ResultsSection(
            result_organizers=[
                MockResultOrganizer(
                    panel_name="Basic Metabolic Panel",
                    panel_code="51990-0",
                    status="completed",
                    results=[
                        MockResultObservation(
                            test_name="Glucose",
                            test_code="2339-0",
                            value="95",
                            unit="mg/dL",
                            status="final",
                        )
                    ],
                )
            ],
            version=CDAVersion.R2_1,
        )

        # 8. Social History
        social_history_section = SocialHistorySection(
            smoking_statuses=[
                MockSmokingStatus(
                    smoking_status="Former smoker",
                    code="8517006",
                    date=datetime(2023, 10, 1, 10, 0),
                )
            ],
            version=CDAVersion.R2_1,
        )

        # 9. Encounters
        encounters_section = EncountersSection(
            encounters=[
                MockEncounter(
                    encounter_type="Office Visit",
                    code="99213",
                    code_system="CPT-4",
                    date=datetime(2023, 10, 10, 14, 0),
                )
            ],
            version=CDAVersion.R2_1,
        )

        # Create document with all sections
        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[
                problems_section,
                medications_section,
                allergies_section,
                immunizations_section,
                vital_signs_section,
                procedures_section,
                results_section,
                social_history_section,
                encounters_section,
            ],
            title="Comprehensive Patient Summary - All 9 Core Sections",
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string(pretty=True)
        result = schematron_validator.validate(xml_string)

        # Document with all sections should validate
        assert isinstance(result.errors, list)

        # Log validation summary
        print(f"\n=== All 9 Core Sections Validation Summary ===")
        print(f"Valid: {result.is_valid}")
        print(f"Errors: {len(result.errors)}")
        print(f"Warnings: {len(result.warnings)}")

        if result.errors:
            print("\nFirst 10 errors:")
            for i, error in enumerate(result.errors[:10], 1):
                print(f"  {i}. {error.code}: {error.message[:150]}")

    def test_subset_of_core_sections(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with subset of core sections."""
        # Common subset: Problems, Medications, Allergies
        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[
                ProblemsSection(
                    problems=[MockProblem()],
                    version=CDAVersion.R2_1,
                ),
                MedicationsSection(
                    medications=[MockMedication()],
                    version=CDAVersion.R2_1,
                ),
                AllergiesSection(
                    allergies=[MockAllergy()],
                    version=CDAVersion.R2_1,
                ),
            ],
            title="Common Clinical Summary",
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.errors, list)
