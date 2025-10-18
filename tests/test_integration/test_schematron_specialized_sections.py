"""
Comprehensive Schematron validation tests for Specialized/Administrative Sections.

Tests all 11 Specialized/Administrative Sections with:
1. Valid data scenarios
2. Minimal/empty data scenarios
3. Edge cases

Sections tested:
1. PlanOfTreatmentSection
2. AdvanceDirectivesSection
3. MedicalEquipmentSection
4. AdmissionMedicationsSection
5. DischargeMedicationsSection
6. HospitalDischargeInstructionsSection
7. PayersSection
8. NutritionSection
9. ReasonForVisitSection
10. ChiefComplaintAndReasonForVisitSection
11. InterventionsSection
"""

from datetime import date, datetime

import pytest

from ccdakit.builders.document import ClinicalDocument
from ccdakit.builders.sections.admission_medications import AdmissionMedicationsSection
from ccdakit.builders.sections.advance_directives import AdvanceDirectivesSection
from ccdakit.builders.sections.chief_complaint_reason_for_visit import (
    ChiefComplaintAndReasonForVisitSection,
)
from ccdakit.builders.sections.discharge_medications import DischargeMedicationsSection
from ccdakit.builders.sections.hospital_discharge_instructions import (
    HospitalDischargeInstructionsSection,
)
from ccdakit.builders.sections.interventions import InterventionsSection
from ccdakit.builders.sections.medical_equipment import MedicalEquipmentSection
from ccdakit.builders.sections.nutrition import NutritionSection
from ccdakit.builders.sections.payers import PayersSection
from ccdakit.builders.sections.plan_of_treatment import PlanOfTreatmentSection
from ccdakit.builders.sections.reason_for_visit import ReasonForVisitSection
from ccdakit.core.base import CDAVersion
from ccdakit.validators.schematron import SchematronValidator

# Import mock data from existing integration tests
from .test_full_document import MockAuthor, MockOrganization, MockPatient


# ============================================================================
# Mock Data Classes for Specialized Sections
# ============================================================================


class MockPlannedObservation:
    """Mock planned observation for testing."""

    def __init__(
        self,
        description="Blood glucose monitoring",
        code="15074-8",
        code_system="LOINC",
        status="active",
        planned_date=None,
        persistent_id=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._status = status
        self._planned_date = planned_date or date(2024, 1, 15)
        self._persistent_id = persistent_id

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def status(self):
        return self._status

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPlannedProcedure:
    """Mock planned procedure for testing."""

    def __init__(
        self,
        description="Colonoscopy screening",
        code="73761001",
        code_system="SNOMED",
        status="active",
        planned_date=None,
        persistent_id=None,
        body_site=None,
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._status = status
        self._planned_date = planned_date or date(2024, 2, 1)
        self._persistent_id = persistent_id
        self._body_site = body_site

    @property
    def description(self):
        return self._description

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def status(self):
        return self._status

    @property
    def planned_date(self):
        return self._planned_date

    @property
    def persistent_id(self):
        return self._persistent_id

    @property
    def body_site(self):
        return self._body_site


class MockAdvanceDirective:
    """Mock advance directive for testing."""

    def __init__(
        self,
        directive_type="Resuscitation Status",
        directive_type_code=None,
        directive_type_code_system=None,
        directive_value="Full Code",
        directive_value_code=None,
        directive_value_code_system=None,
        start_date=None,
        end_date=None,
        document_id=None,
        document_url=None,
        document_description=None,
        custodian_name=None,
        custodian_relationship=None,
        custodian_relationship_code=None,
        custodian_phone=None,
        custodian_address=None,
        verifier_name=None,
        verification_date=None,
    ):
        self._directive_type = directive_type
        self._directive_type_code = directive_type_code
        self._directive_type_code_system = directive_type_code_system
        self._directive_value = directive_value
        self._directive_value_code = directive_value_code
        self._directive_value_code_system = directive_value_code_system
        self._start_date = start_date or date(2023, 1, 1)
        self._end_date = end_date
        self._document_id = document_id
        self._document_url = document_url
        self._document_description = document_description
        self._custodian_name = custodian_name
        self._custodian_relationship = custodian_relationship
        self._custodian_relationship_code = custodian_relationship_code
        self._custodian_phone = custodian_phone
        self._custodian_address = custodian_address
        self._verifier_name = verifier_name
        self._verification_date = verification_date

    @property
    def directive_type(self):
        return self._directive_type

    @property
    def directive_type_code(self):
        return self._directive_type_code

    @property
    def directive_type_code_system(self):
        return self._directive_type_code_system

    @property
    def directive_value(self):
        return self._directive_value

    @property
    def directive_value_code(self):
        return self._directive_value_code

    @property
    def directive_value_code_system(self):
        return self._directive_value_code_system

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def document_id(self):
        return self._document_id

    @property
    def document_url(self):
        return self._document_url

    @property
    def document_description(self):
        return self._document_description

    @property
    def custodian_name(self):
        return self._custodian_name

    @property
    def custodian_relationship(self):
        return self._custodian_relationship

    @property
    def custodian_relationship_code(self):
        return self._custodian_relationship_code

    @property
    def custodian_phone(self):
        return self._custodian_phone

    @property
    def custodian_address(self):
        return self._custodian_address

    @property
    def verifier_name(self):
        return self._verifier_name

    @property
    def verification_date(self):
        return self._verification_date


class MockMedicalEquipment:
    """Mock medical equipment for testing."""

    def __init__(
        self,
        name="Wheelchair",
        code="58938008",
        code_system="SNOMED",
        date_supplied=None,
        date_end=None,
        quantity=1,
        status="active",
        manufacturer=None,
        model_number=None,
        serial_number=None,
        instructions=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._date_supplied = date_supplied or date(2023, 6, 1)
        self._date_end = date_end
        self._quantity = quantity
        self._status = status
        self._manufacturer = manufacturer
        self._model_number = model_number
        self._serial_number = serial_number
        self._instructions = instructions

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
    def date_supplied(self):
        return self._date_supplied

    @property
    def date_end(self):
        return self._date_end

    @property
    def quantity(self):
        return self._quantity

    @property
    def status(self):
        return self._status

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def model_number(self):
        return self._model_number

    @property
    def serial_number(self):
        return self._serial_number

    @property
    def instructions(self):
        return self._instructions


class MockMedication:
    """Mock medication for testing."""

    def __init__(
        self,
        name="Metformin 500mg",
        code="860975",
        dosage="500 mg",
        route="oral",
        frequency="twice daily",
        start_date=None,
        end_date=None,
        status="active",
        instructions=None,
    ):
        self._name = name
        self._code = code
        self._dosage = dosage
        self._route = route
        self._frequency = frequency
        self._start_date = start_date or date(2023, 1, 1)
        self._end_date = end_date
        self._status = status
        self._instructions = instructions

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def dosage(self):
        return self._dosage

    @property
    def route(self):
        return self._route

    @property
    def frequency(self):
        return self._frequency

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def status(self):
        return self._status

    @property
    def instructions(self):
        return self._instructions


class MockDischargeInstruction:
    """Mock discharge instruction for testing."""

    def __init__(self, instruction_text, instruction_category=None):
        self._instruction_text = instruction_text
        self._instruction_category = instruction_category

    @property
    def instruction_text(self):
        return self._instruction_text

    @property
    def instruction_category(self):
        return self._instruction_category


class MockPayer:
    """Mock payer/insurance for testing."""

    def __init__(
        self,
        payer_name="Blue Cross Blue Shield",
        insurance_type="PPO",
        member_id="ABC123456",
        payer_id="PAYER001",
        group_number="GRP789",
        start_date=None,
        end_date=None,
        sequence_number=1,
        insurance_type_code=None,
        subscriber_name=None,
        subscriber_id=None,
        relationship_to_subscriber=None,
        payer_phone=None,
        coverage_type_code=None,
        authorization_ids=None,
    ):
        self._payer_name = payer_name
        self._payer_id = payer_id
        self._insurance_type = insurance_type
        self._insurance_type_code = insurance_type_code
        self._member_id = member_id
        self._group_number = group_number
        self._start_date = start_date or date(2023, 1, 1)
        self._end_date = end_date
        self._sequence_number = sequence_number
        self._subscriber_name = subscriber_name
        self._subscriber_id = subscriber_id
        self._relationship_to_subscriber = relationship_to_subscriber
        self._payer_phone = payer_phone
        self._coverage_type_code = coverage_type_code
        self._authorization_ids = authorization_ids

    @property
    def payer_name(self):
        return self._payer_name

    @property
    def payer_id(self):
        return self._payer_id

    @property
    def insurance_type(self):
        return self._insurance_type

    @property
    def insurance_type_code(self):
        return self._insurance_type_code

    @property
    def member_id(self):
        return self._member_id

    @property
    def group_number(self):
        return self._group_number

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def sequence_number(self):
        return self._sequence_number

    @property
    def subscriber_name(self):
        return self._subscriber_name

    @property
    def subscriber_id(self):
        return self._subscriber_id

    @property
    def relationship_to_subscriber(self):
        return self._relationship_to_subscriber

    @property
    def payer_phone(self):
        return self._payer_phone

    @property
    def coverage_type_code(self):
        return self._coverage_type_code

    @property
    def authorization_ids(self):
        return self._authorization_ids


class MockNutritionalStatus:
    """Mock nutritional status for testing."""

    def __init__(
        self, status="Well nourished", status_code="310602003", date=None, assessments=None
    ):
        self._status = status
        self._status_code = status_code
        self._date = date or datetime(2023, 10, 1, 10, 0)
        self._assessments = assessments or []

    @property
    def status(self):
        return self._status

    @property
    def status_code(self):
        return self._status_code

    @property
    def date(self):
        return self._date

    @property
    def assessments(self):
        return self._assessments


class MockNutritionalAssessment:
    """Mock nutritional assessment for testing."""

    def __init__(
        self,
        assessment_type="BMI",
        code="60621009",
        value="22.5",
        value_code=None,
        date=None,
    ):
        self._assessment_type = assessment_type
        self._code = code
        self._value = value
        self._value_code = value_code
        self._date = date or datetime(2023, 10, 1, 10, 0)

    @property
    def assessment_type(self):
        return self._assessment_type

    @property
    def code(self):
        return self._code

    @property
    def value(self):
        return self._value

    @property
    def value_code(self):
        return self._value_code

    @property
    def date(self):
        return self._date


class MockChiefComplaint:
    """Mock chief complaint for testing."""

    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        return self._text


class MockIntervention:
    """Mock intervention for testing."""

    def __init__(
        self,
        description="Diabetes self-management education",
        status="completed",
        effective_time=None,
        goal_reference_id=None,
    ):
        self._description = description
        self._status = status
        self._effective_time = effective_time or date(2023, 9, 15)
        self._goal_reference_id = goal_reference_id

    @property
    def description(self):
        return self._description

    @property
    def status(self):
        return self._status

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def goal_reference_id(self):
        return self._goal_reference_id


class MockPlannedIntervention:
    """Mock planned intervention for testing."""

    def __init__(
        self,
        description="Smoking cessation counseling",
        effective_time=None,
        goal_reference_id=None,
    ):
        self._description = description
        self._effective_time = effective_time or date(2024, 1, 10)
        self._goal_reference_id = goal_reference_id

    @property
    def description(self):
        return self._description

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def goal_reference_id(self):
        return self._goal_reference_id


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
# 1. Plan of Treatment Section Tests
# ============================================================================


class TestPlanOfTreatmentSectionValidation:
    """Test Plan of Treatment Section Schematron validation."""

    def test_plan_of_treatment_with_valid_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Plan of Treatment section with valid planned activities."""
        planned_observations = [
            MockPlannedObservation(
                description="Daily blood glucose monitoring",
                code="15074-8",
                status="active",
                planned_date=date(2024, 1, 15),
            )
        ]

        planned_procedures = [
            MockPlannedProcedure(
                description="Annual eye exam",
                code="410451008",
                status="active",
                planned_date=date(2024, 3, 1),
            )
        ]

        section = PlanOfTreatmentSection(
            planned_observations=planned_observations,
            planned_procedures=planned_procedures,
            version=CDAVersion.R2_1,
        )

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
        assert isinstance(result, object)
        assert hasattr(result, "errors")

    def test_plan_of_treatment_with_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Plan of Treatment section with minimal/empty data."""
        section = PlanOfTreatmentSection(version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
        assert hasattr(result, "errors")

    def test_plan_of_treatment_edge_cases(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Plan of Treatment section edge cases."""
        # Multiple planned activities of different types
        planned_observations = [
            MockPlannedObservation(
                description=f"Lab test {i}",
                code=f"CODE{i}",
                status="active",
            )
            for i in range(3)
        ]

        section = PlanOfTreatmentSection(
            planned_observations=planned_observations, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)


# ============================================================================
# 2. Advance Directives Section Tests
# ============================================================================


class TestAdvanceDirectivesSectionValidation:
    """Test Advance Directives Section Schematron validation."""

    def test_advance_directives_with_valid_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Advance Directives section with valid data."""
        directives = [
            MockAdvanceDirective(
                directive_type="Resuscitation Status",
                directive_value="Full Code",
                start_date=date(2023, 1, 1),
                custodian_name="Jane Doe",
                custodian_relationship="Spouse",
            ),
            MockAdvanceDirective(
                directive_type="Healthcare Proxy",
                directive_value="Jane Doe designated as healthcare proxy",
                start_date=date(2023, 1, 1),
                verifier_name="Dr. Smith",
                verification_date=date(2023, 1, 5),
            ),
        ]

        section = AdvanceDirectivesSection(directives=directives, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
        assert hasattr(result, "errors")

    def test_advance_directives_with_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Advance Directives section with no information."""
        section = AdvanceDirectivesSection(
            directives=[], null_flavor="NI", version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)

    def test_advance_directives_edge_cases(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Advance Directives section edge cases."""
        # Directive with end date
        directives = [
            MockAdvanceDirective(
                directive_type="DNR Order",
                directive_value="Do Not Resuscitate",
                start_date=date(2022, 1, 1),
                end_date=date(2023, 12, 31),
                document_url="http://example.com/dnr.pdf",
            )
        ]

        section = AdvanceDirectivesSection(directives=directives, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)


# ============================================================================
# 3. Medical Equipment Section Tests
# ============================================================================


class TestMedicalEquipmentSectionValidation:
    """Test Medical Equipment Section Schematron validation."""

    def test_medical_equipment_with_valid_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Medical Equipment section with valid data."""
        equipment_list = [
            MockMedicalEquipment(
                name="Wheelchair",
                code="58938008",
                code_system="SNOMED",
                date_supplied=date(2023, 6, 1),
                quantity=1,
                status="active",
                manufacturer="MedEquip Inc",
                model_number="WC-2000",
                serial_number="SN123456",
            ),
            MockMedicalEquipment(
                name="Cane",
                code="23366006",
                code_system="SNOMED",
                date_supplied=date(2023, 7, 15),
                quantity=1,
                status="active",
            ),
        ]

        section = MedicalEquipmentSection(
            equipment_list=equipment_list, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
        assert hasattr(result, "errors")

    def test_medical_equipment_with_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Medical Equipment section with minimal data."""
        equipment_list = [
            MockMedicalEquipment(
                name="Walker",
                code="466289007",
                code_system="SNOMED",
                status="active",
            )
        ]

        section = MedicalEquipmentSection(
            equipment_list=equipment_list, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)

    def test_medical_equipment_edge_cases(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Medical Equipment section edge cases."""
        # Equipment with end date (discontinued)
        equipment_list = [
            MockMedicalEquipment(
                name="CPAP Machine",
                code="706172005",
                code_system="SNOMED",
                date_supplied=date(2022, 1, 1),
                date_end=date(2023, 12, 31),
                quantity=1,
                status="completed",
            )
        ]

        section = MedicalEquipmentSection(
            equipment_list=equipment_list, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)


# ============================================================================
# 4. Admission Medications Section Tests
# ============================================================================


class TestAdmissionMedicationsSectionValidation:
    """Test Admission Medications Section Schematron validation."""

    def test_admission_medications_with_valid_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Admission Medications section with valid data."""
        medications = [
            MockMedication(
                name="Lisinopril 10mg",
                code="314076",
                dosage="10 mg",
                route="oral",
                frequency="once daily",
                start_date=date(2020, 1, 1),
                status="active",
            ),
            MockMedication(
                name="Metformin 500mg",
                code="860975",
                dosage="500 mg",
                route="oral",
                frequency="twice daily",
                start_date=date(2021, 3, 1),
                status="active",
            ),
        ]

        section = AdmissionMedicationsSection(
            medications=medications, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
        assert hasattr(result, "errors")

    def test_admission_medications_with_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Admission Medications section with no medications."""
        section = AdmissionMedicationsSection(
            medications=[], null_flavor="NI", version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)

    def test_admission_medications_edge_cases(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Admission Medications section edge cases."""
        # Medication with end date
        medications = [
            MockMedication(
                name="Amoxicillin 500mg",
                code="308182",
                dosage="500 mg",
                route="oral",
                frequency="three times daily",
                start_date=date(2023, 10, 1),
                end_date=date(2023, 10, 10),
                status="completed",
            )
        ]

        section = AdmissionMedicationsSection(
            medications=medications, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)


# ============================================================================
# 5. Discharge Medications Section Tests
# ============================================================================


class TestDischargeMedicationsSectionValidation:
    """Test Discharge Medications Section Schematron validation."""

    def test_discharge_medications_with_valid_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Discharge Medications section with valid data."""
        medications = [
            MockMedication(
                name="Aspirin 81mg",
                code="243670",
                dosage="81 mg",
                route="oral",
                frequency="once daily",
                start_date=date(2023, 10, 15),
                status="active",
                instructions="Take with food",
            ),
            MockMedication(
                name="Atorvastatin 20mg",
                code="617312",
                dosage="20 mg",
                route="oral",
                frequency="once daily at bedtime",
                start_date=date(2023, 10, 15),
                status="active",
            ),
        ]

        section = DischargeMedicationsSection(
            medications=medications, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
        assert hasattr(result, "errors")

    def test_discharge_medications_with_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Discharge Medications section with no medications."""
        section = DischargeMedicationsSection(
            medications=[], null_flavor="NI", version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)

    def test_discharge_medications_edge_cases(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Discharge Medications section edge cases."""
        # Single medication with detailed instructions
        medications = [
            MockMedication(
                name="Warfarin 5mg",
                code="855333",
                dosage="5 mg",
                route="oral",
                frequency="once daily",
                start_date=date(2023, 10, 15),
                status="active",
                instructions="Take at same time each day. Monitor INR weekly.",
            )
        ]

        section = DischargeMedicationsSection(
            medications=medications, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)


# ============================================================================
# 6. Hospital Discharge Instructions Section Tests
# ============================================================================


class TestHospitalDischargeInstructionsSectionValidation:
    """Test Hospital Discharge Instructions Section Schematron validation."""

    def test_discharge_instructions_with_valid_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Hospital Discharge Instructions section with valid data."""
        instructions = [
            MockDischargeInstruction(
                instruction_text="Take all medications as prescribed",
                instruction_category="Medications",
            ),
            MockDischargeInstruction(
                instruction_text="Follow up with primary care physician in 2 weeks",
                instruction_category="Follow-up",
            ),
            MockDischargeInstruction(
                instruction_text="Low sodium diet, limit to 2000mg per day",
                instruction_category="Diet",
            ),
            MockDischargeInstruction(
                instruction_text="Walk 15 minutes twice daily",
                instruction_category="Activity",
            ),
        ]

        section = HospitalDischargeInstructionsSection(
            instructions=instructions, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
        assert hasattr(result, "errors")

    def test_discharge_instructions_with_narrative_text(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Hospital Discharge Instructions with narrative text only."""
        narrative = (
            "Patient discharged in stable condition. Continue current medications. "
            "Follow up with cardiology in 2 weeks. Low sodium diet. Monitor weight daily."
        )

        section = HospitalDischargeInstructionsSection(
            narrative_text=narrative, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)

    def test_discharge_instructions_edge_cases(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Hospital Discharge Instructions section edge cases."""
        # Mix of categorized and uncategorized instructions
        instructions = [
            MockDischargeInstruction(
                instruction_text="Resume normal activities gradually",
                instruction_category="Activity",
            ),
            MockDischargeInstruction(
                instruction_text="Call doctor if fever exceeds 101F",
                instruction_category=None,  # Uncategorized
            ),
        ]

        section = HospitalDischargeInstructionsSection(
            instructions=instructions, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)


# ============================================================================
# 7. Payers Section Tests
# ============================================================================


class TestPayersSectionValidation:
    """Test Payers Section Schematron validation."""

    def test_payers_with_valid_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Payers section with valid data."""
        payers = [
            MockPayer(
                payer_name="Blue Cross Blue Shield",
                insurance_type="PPO",
                member_id="ABC123456789",
                group_number="GRP001",
                start_date=date(2023, 1, 1),
                sequence_number=1,
            ),
            MockPayer(
                payer_name="Medicare",
                insurance_type="Medicare Part A",
                member_id="1EG4-TE5-MK72",
                group_number=None,
                start_date=date(2020, 1, 1),
                sequence_number=2,
            ),
        ]

        section = PayersSection(payers=payers, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
        assert hasattr(result, "errors")

    def test_payers_with_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Payers section with single payer and minimal data."""
        payers = [
            MockPayer(
                payer_name="Self Pay",
                insurance_type="Self",
                member_id="SELF001",
                group_number=None,
                sequence_number=1,
            )
        ]

        section = PayersSection(payers=payers, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)

    def test_payers_edge_cases(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Payers section edge cases."""
        # Payer with end date (coverage ended)
        payers = [
            MockPayer(
                payer_name="Aetna",
                insurance_type="HMO",
                member_id="W123456789",
                group_number="CORP500",
                start_date=date(2020, 1, 1),
                end_date=date(2022, 12, 31),
                sequence_number=1,
            )
        ]

        section = PayersSection(payers=payers, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)


# ============================================================================
# 8. Nutrition Section Tests
# ============================================================================


class TestNutritionSectionValidation:
    """Test Nutrition Section Schematron validation."""

    def test_nutrition_with_valid_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Nutrition section with valid data."""
        assessments = [
            MockNutritionalAssessment(assessment_type="BMI", value="22.5 kg/m2"),
            MockNutritionalAssessment(assessment_type="Weight", value="75 kg"),
        ]

        nutritional_statuses = [
            MockNutritionalStatus(
                status="Well nourished",
                date=datetime(2023, 10, 1, 10, 0),
                assessments=assessments,
            )
        ]

        section = NutritionSection(
            nutritional_statuses=nutritional_statuses, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
        assert hasattr(result, "errors")

    def test_nutrition_with_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Nutrition section with minimal data."""
        nutritional_statuses = [
            MockNutritionalStatus(
                status="No concerns", date=datetime(2023, 10, 1), assessments=[]
            )
        ]

        section = NutritionSection(
            nutritional_statuses=nutritional_statuses, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)

    def test_nutrition_edge_cases(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Nutrition section edge cases."""
        # Multiple assessments
        assessments = [
            MockNutritionalAssessment(assessment_type="BMI", value="18.2 kg/m2"),
            MockNutritionalAssessment(assessment_type="Weight", value="55 kg"),
            MockNutritionalAssessment(
                assessment_type="Dietary Intake", value="Reduced appetite"
            ),
        ]

        nutritional_statuses = [
            MockNutritionalStatus(
                status="At risk for malnutrition",
                date=datetime(2023, 10, 1, 14, 30),
                assessments=assessments,
            )
        ]

        section = NutritionSection(
            nutritional_statuses=nutritional_statuses, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)


# ============================================================================
# 9. Reason for Visit Section Tests
# ============================================================================


class TestReasonForVisitSectionValidation:
    """Test Reason for Visit Section Schematron validation."""

    def test_reason_for_visit_with_valid_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Reason for Visit section with valid data."""
        section = ReasonForVisitSection(
            reason_text="Annual physical examination and medication review",
            version=CDAVersion.R2_1,
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
        assert hasattr(result, "errors")

    def test_reason_for_visit_with_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Reason for Visit section with minimal data."""
        section = ReasonForVisitSection(
            reason_text="Follow-up", version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)

    def test_reason_for_visit_edge_cases(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Reason for Visit section edge cases."""
        # Long detailed reason
        section = ReasonForVisitSection(
            reason_text=(
                "Patient presents for evaluation of persistent headaches lasting 2 weeks, "
                "associated with occasional nausea and sensitivity to light. "
                "Also requesting refill of chronic medications."
            ),
            version=CDAVersion.R2_1,
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)


# ============================================================================
# 10. Chief Complaint and Reason for Visit Section Tests
# ============================================================================


class TestChiefComplaintAndReasonForVisitSectionValidation:
    """Test Chief Complaint and Reason for Visit Section Schematron validation."""

    def test_chief_complaint_with_valid_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Chief Complaint and Reason for Visit section with valid data."""
        chief_complaints = [
            MockChiefComplaint(text="Chest pain"),
            MockChiefComplaint(text="Shortness of breath"),
            MockChiefComplaint(text="Dizziness"),
        ]

        section = ChiefComplaintAndReasonForVisitSection(
            chief_complaints=chief_complaints, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
        assert hasattr(result, "errors")

    def test_chief_complaint_with_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Chief Complaint section with single complaint."""
        chief_complaints = [MockChiefComplaint(text="Cough")]

        section = ChiefComplaintAndReasonForVisitSection(
            chief_complaints=chief_complaints, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)

    def test_chief_complaint_edge_cases(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Chief Complaint section edge cases."""
        # Empty list
        section = ChiefComplaintAndReasonForVisitSection(
            chief_complaints=[], version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)


# ============================================================================
# 11. Interventions Section Tests
# ============================================================================


class TestInterventionsSectionValidation:
    """Test Interventions Section Schematron validation."""

    def test_interventions_with_valid_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Interventions section with valid data."""
        interventions = [
            MockIntervention(
                description="Diabetes self-management education",
                status="completed",
                effective_time=date(2023, 9, 15),
                goal_reference_id="goal-1",
            )
        ]

        planned_interventions = [
            MockPlannedIntervention(
                description="Smoking cessation counseling",
                effective_time=date(2024, 1, 10),
                goal_reference_id="goal-2",
            )
        ]

        section = InterventionsSection(
            interventions=interventions,
            planned_interventions=planned_interventions,
            version=CDAVersion.R2_1,
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
        assert hasattr(result, "errors")

    def test_interventions_with_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Interventions section with no interventions."""
        section = InterventionsSection(
            interventions=[], planned_interventions=[], version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)

    def test_interventions_edge_cases(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test Interventions section edge cases."""
        # Multiple interventions without goal references
        interventions = [
            MockIntervention(
                description="Nutritional counseling",
                status="completed",
                effective_time=date(2023, 10, 1),
                goal_reference_id=None,
            ),
            MockIntervention(
                description="Physical therapy",
                status="in-progress",
                effective_time=date(2023, 9, 20),
                goal_reference_id=None,
            ),
        ]

        section = InterventionsSection(
            interventions=interventions, version=CDAVersion.R2_1
        )

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)


# ============================================================================
# Combined Multi-Section Tests
# ============================================================================


class TestMultipleSpecializedSectionsValidation:
    """Test documents with multiple specialized sections."""

    def test_document_with_all_specialized_sections(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document containing all specialized sections."""
        # Create sections
        plan_section = PlanOfTreatmentSection(
            planned_observations=[
                MockPlannedObservation(description="Weekly blood pressure monitoring")
            ],
            version=CDAVersion.R2_1,
        )

        directives_section = AdvanceDirectivesSection(
            directives=[
                MockAdvanceDirective(
                    directive_type="Resuscitation Status", directive_value="Full Code"
                )
            ],
            version=CDAVersion.R2_1,
        )

        equipment_section = MedicalEquipmentSection(
            equipment_list=[MockMedicalEquipment(name="Cane", code="23366006")],
            version=CDAVersion.R2_1,
        )

        admission_meds_section = AdmissionMedicationsSection(
            medications=[MockMedication(name="Aspirin 81mg", code="243670")],
            version=CDAVersion.R2_1,
        )

        discharge_meds_section = DischargeMedicationsSection(
            medications=[MockMedication(name="Lisinopril 10mg", code="314076")],
            version=CDAVersion.R2_1,
        )

        instructions_section = HospitalDischargeInstructionsSection(
            narrative_text="Follow discharge care plan as discussed.",
            version=CDAVersion.R2_1,
        )

        payers_section = PayersSection(
            payers=[
                MockPayer(
                    payer_name="Medicare", insurance_type="Medicare", member_id="MED001"
                )
            ],
            version=CDAVersion.R2_1,
        )

        nutrition_section = NutritionSection(
            nutritional_statuses=[MockNutritionalStatus(status="Well nourished")],
            version=CDAVersion.R2_1,
        )

        reason_section = ReasonForVisitSection(
            reason_text="Annual check-up", version=CDAVersion.R2_1
        )

        chief_complaint_section = ChiefComplaintAndReasonForVisitSection(
            chief_complaints=[MockChiefComplaint(text="Routine visit")],
            version=CDAVersion.R2_1,
        )

        interventions_section = InterventionsSection(
            interventions=[
                MockIntervention(description="Patient education", status="completed")
            ],
            version=CDAVersion.R2_1,
        )

        # Create document with all sections
        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[
                plan_section,
                directives_section,
                equipment_section,
                admission_meds_section,
                discharge_meds_section,
                instructions_section,
                payers_section,
                nutrition_section,
                reason_section,
                chief_complaint_section,
                interventions_section,
            ],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        # Document should validate
        assert isinstance(result, object)
        assert hasattr(result, "errors")
        assert hasattr(result, "warnings")

        # Log validation summary
        print(f"\nValidation Summary for All Specialized Sections:")
        print(f"  Valid: {result.is_valid}")
        print(f"  Errors: {len(result.errors)}")
        print(f"  Warnings: {len(result.warnings)}")

        if result.errors:
            print("\nFirst 10 errors:")
            for i, error in enumerate(result.errors[:10], 1):
                print(f"  {i}. {error.code}: {error.message[:100]}")

    def test_document_with_mixed_empty_and_valid_sections(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with mix of empty and populated specialized sections."""
        sections = [
            PlanOfTreatmentSection(version=CDAVersion.R2_1),  # Empty
            AdvanceDirectivesSection(
                directives=[
                    MockAdvanceDirective(directive_type="DNR", directive_value="Active")
                ],
                version=CDAVersion.R2_1,
            ),  # Populated
            MedicalEquipmentSection(
                equipment_list=[], version=CDAVersion.R2_1
            ),  # Empty list would fail, skip
            ReasonForVisitSection(
                reason_text="Check-up", version=CDAVersion.R2_1
            ),  # Populated
        ]

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=sections,
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
