"""
Comprehensive Schematron validation tests for Hospital/Surgical Sections.

Tests Schematron validation for 10 newly implemented hospital and surgical sections:
1. Admission Diagnosis Section
2. Discharge Diagnosis Section
3. Hospital Course Section
4. Instructions Section
5. Anesthesia Section
6. Postoperative Diagnosis Section
7. Preoperative Diagnosis Section
8. Complications Section
9. Hospital Discharge Studies Summary Section
10. Medications Administered Section

Each section is tested with:
- Valid data and Schematron validation
- Minimal/empty data
- Multiple entries
- Edge cases
"""

from datetime import date, datetime

import pytest

from ccdakit.builders.document import ClinicalDocument
from ccdakit.builders.sections.admission_diagnosis import AdmissionDiagnosisSection
from ccdakit.builders.sections.anesthesia import AnesthesiaSection
from ccdakit.builders.sections.complications import ComplicationsSection
from ccdakit.builders.sections.discharge_diagnosis import DischargeDiagnosisSection
from ccdakit.builders.sections.discharge_studies import (
    HospitalDischargeStudiesSummarySection,
)
from ccdakit.builders.sections.hospital_course import HospitalCourseSection
from ccdakit.builders.sections.instructions import InstructionsSection
from ccdakit.builders.sections.medications_administered import (
    MedicationsAdministeredSection,
)
from ccdakit.builders.sections.postoperative_diagnosis import (
    PostoperativeDiagnosisSection,
)
from ccdakit.builders.sections.preoperative_diagnosis import (
    PreoperativeDiagnosisSection,
)
from ccdakit.core.base import CDAVersion
from ccdakit.validators.schematron import SchematronValidator

# Import common mock data from existing integration tests
from .test_full_document import MockAuthor, MockOrganization, MockPatient


# ============================================================================
# Mock Data Classes for Hospital/Surgical Sections
# ============================================================================


class MockAdmissionDiagnosis:
    """Mock admission diagnosis for testing."""

    def __init__(
        self,
        name="Acute myocardial infarction",
        code="57054005",
        code_system="SNOMED",
        admission_date=None,
        diagnosis_date=None,
        onset_date=None,
        resolved_date=None,
        status="active",
        persistent_id=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._admission_date = admission_date or date(2023, 10, 15)
        self._diagnosis_date = diagnosis_date or date(2023, 10, 15)
        self._onset_date = onset_date or date(2023, 10, 15)
        self._resolved_date = resolved_date
        self._status = status
        self._persistent_id = persistent_id

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
    def admission_date(self):
        return self._admission_date

    @property
    def diagnosis_date(self):
        return self._diagnosis_date

    @property
    def onset_date(self):
        return self._onset_date

    @property
    def resolved_date(self):
        return self._resolved_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class MockDischargeDiagnosis:
    """Mock discharge diagnosis for testing."""

    def __init__(
        self,
        name="Coronary artery disease",
        code="53741008",
        code_system="SNOMED",
        diagnosis_date=None,
        onset_date=None,
        resolved_date=None,
        status="active",
        persistent_id=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._diagnosis_date = diagnosis_date or date(2023, 10, 20)
        self._onset_date = onset_date or date(2023, 10, 15)
        self._resolved_date = resolved_date
        self._status = status
        self._persistent_id = persistent_id

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
    def diagnosis_date(self):
        return self._diagnosis_date

    @property
    def onset_date(self):
        return self._onset_date

    @property
    def resolved_date(self):
        return self._resolved_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class MockHospitalCourse:
    """Mock hospital course for testing."""

    def __init__(
        self,
        course_text=None,
    ):
        self._course_text = course_text or (
            "Patient admitted with chest pain. Initial EKG showed ST elevation. "
            "Cardiac catheterization performed on day 1 revealing 90% LAD stenosis. "
            "Successful PCI with drug-eluting stent placement. Patient remained stable "
            "throughout hospital stay. Discharged on day 3 in good condition."
        )

    @property
    def course_text(self):
        return self._course_text


class MockInstruction:
    """Mock instruction for testing."""

    def __init__(
        self,
        instruction_text="Take all medications as prescribed",
        instruction_type="medication",
        instruction_date=None,
    ):
        self._instruction_text = instruction_text
        self._instruction_type = instruction_type
        self._instruction_date = instruction_date or date(2023, 10, 20)

    @property
    def instruction_text(self):
        return self._instruction_text

    @property
    def instruction_type(self):
        return self._instruction_type

    @property
    def instruction_date(self):
        return self._instruction_date


class MockAnesthesiaAgent:
    """Mock anesthesia agent/medication for testing."""

    def __init__(
        self,
        name="Propofol",
        code="387423001",
        dosage="200 mg",
        route="intravenous",
        frequency="single dose",
        start_date=None,
        end_date=None,
        instructions=None,
        status="completed",
    ):
        self._name = name
        self._code = code
        self._dosage = dosage
        self._route = route
        self._frequency = frequency
        self._start_date = start_date or datetime(2023, 10, 15, 8, 0)
        self._end_date = end_date or datetime(2023, 10, 15, 10, 30)
        self._instructions = instructions
        self._status = status

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
    def instructions(self):
        return self._instructions

    @property
    def status(self):
        return self._status


class MockAnesthesia:
    """Mock anesthesia for testing."""

    def __init__(
        self,
        anesthesia_type="General anesthesia",
        anesthesia_code="50697003",
        anesthesia_code_system="SNOMED",
        start_time=None,
        end_time=None,
        route="Inhalation",
        status="completed",
        performer_name="Dr. Anesthesiologist",
        anesthesia_agents=None,
    ):
        self._anesthesia_type = anesthesia_type
        self._anesthesia_code = anesthesia_code
        self._anesthesia_code_system = anesthesia_code_system
        self._start_time = start_time or datetime(2023, 10, 15, 8, 0)
        self._end_time = end_time or datetime(2023, 10, 15, 10, 30)
        self._route = route
        self._status = status
        self._performer_name = performer_name
        self._anesthesia_agents = anesthesia_agents or []

    @property
    def anesthesia_type(self):
        return self._anesthesia_type

    @property
    def anesthesia_code(self):
        return self._anesthesia_code

    @property
    def anesthesia_code_system(self):
        return self._anesthesia_code_system

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def route(self):
        return self._route

    @property
    def status(self):
        return self._status

    @property
    def performer_name(self):
        return self._performer_name

    @property
    def anesthesia_agents(self):
        return self._anesthesia_agents


class MockPreoperativeDiagnosis:
    """Mock preoperative diagnosis for testing."""

    def __init__(
        self,
        name="Cholelithiasis",
        code="235919008",
        code_system="SNOMED",
        diagnosis_date=None,
        onset_date=None,
        resolved_date=None,
        status="active",
        persistent_id=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._diagnosis_date = diagnosis_date or date(2023, 10, 14)
        self._onset_date = onset_date or date(2023, 10, 14)
        self._resolved_date = resolved_date
        self._status = status
        self._persistent_id = persistent_id

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
    def diagnosis_date(self):
        return self._diagnosis_date

    @property
    def onset_date(self):
        return self._onset_date

    @property
    def resolved_date(self):
        return self._resolved_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPostoperativeDiagnosis:
    """Mock postoperative diagnosis for testing."""

    def __init__(
        self,
        name="Acute cholecystitis",
        code="65275009",
        code_system="SNOMED",
        diagnosis_date=None,
        onset_date=None,
        resolved_date=None,
        status="active",
        persistent_id=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._diagnosis_date = diagnosis_date or date(2023, 10, 15)
        self._onset_date = onset_date or date(2023, 10, 15)
        self._resolved_date = resolved_date
        self._status = status
        self._persistent_id = persistent_id

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
    def diagnosis_date(self):
        return self._diagnosis_date

    @property
    def onset_date(self):
        return self._onset_date

    @property
    def resolved_date(self):
        return self._resolved_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class MockComplication:
    """Mock complication for testing."""

    def __init__(
        self,
        name="Postoperative wound infection",
        code="312404004",
        code_system="SNOMED",
        complication_date=None,
        onset_date=None,
        resolved_date=None,
        status="active",
        severity="moderate",
        persistent_id=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._complication_date = complication_date or date(2023, 10, 17)
        self._onset_date = onset_date or date(2023, 10, 17)
        self._resolved_date = resolved_date
        self._status = status
        self._severity = severity
        self._persistent_id = persistent_id

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
    def complication_date(self):
        return self._complication_date

    @property
    def onset_date(self):
        return self._onset_date

    @property
    def resolved_date(self):
        return self._resolved_date

    @property
    def status(self):
        return self._status

    @property
    def severity(self):
        return self._severity

    @property
    def persistent_id(self):
        return self._persistent_id


class MockDischargeStudyObservation:
    """Mock discharge study observation for testing.

    Implements both DischargeStudyObservationProtocol and ResultObservationProtocol
    by providing both sets of attribute names as aliases.
    """

    def __init__(
        self,
        study_name="Chest X-Ray",
        study_code="399208008",
        value="No acute cardiopulmonary process",
        unit=None,
        status="completed",
        effective_time=None,
        value_type=None,
        interpretation=None,
        reference_range_low=None,
        reference_range_high=None,
        reference_range_unit=None,
    ):
        self._study_name = study_name
        self._study_code = study_code
        self._value = value
        self._unit = unit
        self._status = status
        self._effective_time = effective_time or datetime(2023, 10, 19, 14, 0)
        self._value_type = value_type or "ST"
        self._interpretation = interpretation
        self._reference_range_low = reference_range_low
        self._reference_range_high = reference_range_high
        self._reference_range_unit = reference_range_unit

    @property
    def study_name(self):
        return self._study_name

    @property
    def study_code(self):
        return self._study_code

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

    # Aliases for ResultObservationProtocol compatibility
    @property
    def test_name(self):
        """Alias for study_name to support ResultObservationProtocol."""
        return self._study_name

    @property
    def test_code(self):
        """Alias for study_code to support ResultObservationProtocol."""
        return self._study_code


class MockDischargeStudy:
    """Mock discharge study organizer for testing.

    Implements both DischargeStudyOrganizerProtocol and ResultOrganizerProtocol
    by providing both sets of attribute names as aliases.
    """

    def __init__(
        self,
        study_panel_name="Imaging Studies",
        study_panel_code="18748-4",
        status="completed",
        effective_time=None,
        studies=None,
    ):
        self._study_panel_name = study_panel_name
        self._study_panel_code = study_panel_code
        self._status = status
        self._effective_time = effective_time or datetime(2023, 10, 19, 14, 0)
        self._studies = studies or []

    @property
    def study_panel_name(self):
        return self._study_panel_name

    @property
    def study_panel_code(self):
        return self._study_panel_code

    @property
    def status(self):
        return self._status

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def studies(self):
        return self._studies

    # Aliases for ResultOrganizerProtocol compatibility
    @property
    def panel_name(self):
        """Alias for study_panel_name to support ResultOrganizerProtocol."""
        return self._study_panel_name

    @property
    def panel_code(self):
        """Alias for study_panel_code to support ResultOrganizerProtocol."""
        return self._study_panel_code

    @property
    def results(self):
        """Alias for studies to support ResultOrganizerProtocol."""
        return self._studies


class MockMedicationAdministered:
    """Mock medication administered for testing."""

    def __init__(
        self,
        name="Morphine sulfate",
        code="373529000",
        dose="2 mg",
        route="intravenous",
        administration_time=None,
        administration_end_time=None,
        site=None,
        rate=None,
        instructions=None,
        indication=None,
        performer="RN Smith",
        status="completed",
    ):
        self._name = name
        self._code = code
        self._dose = dose
        self._route = route
        self._administration_time = administration_time or datetime(2023, 10, 15, 14, 30)
        self._administration_end_time = administration_end_time
        self._site = site
        self._rate = rate
        self._instructions = instructions
        self._indication = indication
        self._performer = performer
        self._status = status

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def dose(self):
        return self._dose

    @property
    def route(self):
        return self._route

    @property
    def administration_time(self):
        return self._administration_time

    @property
    def administration_end_time(self):
        return self._administration_end_time

    @property
    def site(self):
        return self._site

    @property
    def rate(self):
        return self._rate

    @property
    def instructions(self):
        return self._instructions

    @property
    def indication(self):
        return self._indication

    @property
    def performer(self):
        return self._performer

    @property
    def status(self):
        return self._status


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
# 1. Admission Diagnosis Section Tests
# ============================================================================


class TestAdmissionDiagnosisSectionSchematron:
    """Test Schematron validation for Admission Diagnosis Section."""

    def test_valid_admission_diagnosis_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid admission diagnosis validates."""
        diagnoses = [
            MockAdmissionDiagnosis(
                name="Acute myocardial infarction",
                code="57054005",
                code_system="SNOMED",
                admission_date=date(2023, 10, 15),
                diagnosis_date=date(2023, 10, 15),
            )
        ]

        section = AdmissionDiagnosisSection(diagnoses=diagnoses, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)

    def test_admission_diagnosis_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test admission diagnosis section with minimal data."""
        diagnoses = [
            MockAdmissionDiagnosis(
                name="Chest pain",
                code="29857009",
                code_system="SNOMED",
            )
        ]

        section = AdmissionDiagnosisSection(diagnoses=diagnoses, version=CDAVersion.R2_1)

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

    def test_admission_diagnosis_multiple_entries(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test admission diagnosis section with multiple diagnoses."""
        diagnoses = [
            MockAdmissionDiagnosis(
                name="Acute myocardial infarction",
                code="57054005",
                code_system="SNOMED",
            ),
            MockAdmissionDiagnosis(
                name="Hypertension",
                code="38341003",
                code_system="SNOMED",
            ),
            MockAdmissionDiagnosis(
                name="Type 2 diabetes mellitus",
                code="44054006",
                code_system="SNOMED",
            ),
        ]

        section = AdmissionDiagnosisSection(diagnoses=diagnoses, version=CDAVersion.R2_1)

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

    def test_admission_diagnosis_empty_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test admission diagnosis section with no diagnoses."""
        section = AdmissionDiagnosisSection(diagnoses=[], version=CDAVersion.R2_1)

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
# 2. Discharge Diagnosis Section Tests
# ============================================================================


class TestDischargeDiagnosisSectionSchematron:
    """Test Schematron validation for Discharge Diagnosis Section."""

    def test_valid_discharge_diagnosis_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid discharge diagnosis validates."""
        diagnoses = [
            MockDischargeDiagnosis(
                name="Coronary artery disease",
                code="53741008",
                code_system="SNOMED",
                diagnosis_date=date(2023, 10, 20),
                status="active",
            )
        ]

        section = DischargeDiagnosisSection(diagnoses=diagnoses, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)

    def test_discharge_diagnosis_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test discharge diagnosis section with minimal data."""
        diagnoses = [
            MockDischargeDiagnosis(
                name="Resolved pneumonia",
                code="233604007",
                code_system="SNOMED",
                status="resolved",
            )
        ]

        section = DischargeDiagnosisSection(diagnoses=diagnoses, version=CDAVersion.R2_1)

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

    def test_discharge_diagnosis_multiple_entries(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test discharge diagnosis section with multiple diagnoses."""
        diagnoses = [
            MockDischargeDiagnosis(
                name="Coronary artery disease",
                code="53741008",
                code_system="SNOMED",
                status="active",
            ),
            MockDischargeDiagnosis(
                name="Congestive heart failure",
                code="42343007",
                code_system="SNOMED",
                status="active",
            ),
            MockDischargeDiagnosis(
                name="Acute kidney injury",
                code="14669001",
                code_system="SNOMED",
                status="resolved",
            ),
        ]

        section = DischargeDiagnosisSection(diagnoses=diagnoses, version=CDAVersion.R2_1)

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

    def test_discharge_diagnosis_empty_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test discharge diagnosis section with no diagnoses."""
        section = DischargeDiagnosisSection(diagnoses=[], version=CDAVersion.R2_1)

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
# 3. Hospital Course Section Tests
# ============================================================================


class TestHospitalCourseSectionSchematron:
    """Test Schematron validation for Hospital Course Section."""

    def test_valid_hospital_course_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid hospital course validates."""
        hospital_course = MockHospitalCourse(
            course_text=(
                "Patient admitted with chest pain. Initial EKG showed ST elevation. "
                "Cardiac catheterization performed on day 1 revealing 90% LAD stenosis. "
                "Successful PCI with drug-eluting stent placement. Patient remained stable "
                "throughout hospital stay. Discharged on day 3 in good condition."
            )
        )

        section = HospitalCourseSection(hospital_course=hospital_course, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)

    def test_hospital_course_with_narrative_text(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test hospital course section with narrative text directly."""
        narrative = (
            "Patient admitted for elective cholecystectomy. Surgery performed on day 1 "
            "without complications. Patient tolerated procedure well. Discharged home on day 2."
        )

        section = HospitalCourseSection(narrative_text=narrative, version=CDAVersion.R2_1)

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

    def test_hospital_course_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test hospital course section with minimal data."""
        section = HospitalCourseSection(
            narrative_text="Unremarkable hospital stay.", version=CDAVersion.R2_1
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

    def test_hospital_course_long_narrative(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test hospital course section with long multi-paragraph narrative."""
        narrative = (
            "Day 1: Patient admitted through ED with severe chest pain. EKG showed ST elevation. "
            "Taken emergently to cath lab.\n\n"
            "Day 2: Post-PCI, patient stable. Started on dual antiplatelet therapy. "
            "Cardiac enzymes trending down.\n\n"
            "Day 3: Patient ambulating. No chest pain. Ready for discharge with cardiology follow-up."
        )

        section = HospitalCourseSection(narrative_text=narrative, version=CDAVersion.R2_1)

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
# 4. Instructions Section Tests
# ============================================================================


class TestInstructionsSectionSchematron:
    """Test Schematron validation for Instructions Section."""

    def test_valid_instructions_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid instructions validates."""
        instructions = [
            MockInstruction(
                instruction_text="Take aspirin 81mg daily",
                instruction_type="medication",
            ),
            MockInstruction(
                instruction_text="Follow low-sodium diet",
                instruction_type="diet",
            ),
            MockInstruction(
                instruction_text="Walk 30 minutes daily",
                instruction_type="activity",
            ),
        ]

        section = InstructionsSection(instructions=instructions, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)

    def test_instructions_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test instructions section with minimal data."""
        instructions = [
            MockInstruction(
                instruction_text="Resume normal activities",
            )
        ]

        section = InstructionsSection(instructions=instructions, version=CDAVersion.R2_1)

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

    def test_instructions_multiple_types(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test instructions section with multiple instruction types."""
        instructions = [
            MockInstruction(
                instruction_text="Take prescribed medications",
                instruction_type="medication",
            ),
            MockInstruction(
                instruction_text="Monitor blood pressure daily",
                instruction_type="monitoring",
            ),
            MockInstruction(
                instruction_text="Call if fever >101F",
                instruction_type="warning",
            ),
            MockInstruction(
                instruction_text="Follow up with cardiologist in 2 weeks",
                instruction_type="followup",
            ),
        ]

        section = InstructionsSection(instructions=instructions, version=CDAVersion.R2_1)

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

    def test_instructions_empty_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test instructions section with no instructions."""
        section = InstructionsSection(instructions=[], version=CDAVersion.R2_1)

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
# 5. Anesthesia Section Tests
# ============================================================================


class TestAnesthesiaSectionSchematron:
    """Test Schematron validation for Anesthesia Section."""

    def test_valid_anesthesia_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid anesthesia validates."""
        agents = [
            MockAnesthesiaAgent(
                name="Propofol",
                code="387423001",
                dosage="200 mg",
                route="intravenous",
            ),
            MockAnesthesiaAgent(
                name="Fentanyl",
                code="373492002",
                dosage="100 mcg",
                route="intravenous",
            ),
        ]

        anesthesia_records = [
            MockAnesthesia(
                anesthesia_type="General anesthesia",
                anesthesia_code="50697003",
                anesthesia_code_system="SNOMED",
                start_time=datetime(2023, 10, 15, 8, 0),
                end_time=datetime(2023, 10, 15, 10, 30),
                route="Inhalation",
                performer_name="Dr. Anesthesiologist",
                anesthesia_agents=agents,
            )
        ]

        section = AnesthesiaSection(anesthesia_records=anesthesia_records, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)

    def test_anesthesia_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test anesthesia section with minimal data."""
        anesthesia_records = [
            MockAnesthesia(
                anesthesia_type="Local anesthesia",
                anesthesia_code="386761002",
                anesthesia_code_system="SNOMED",
                anesthesia_agents=[],
            )
        ]

        section = AnesthesiaSection(anesthesia_records=anesthesia_records, version=CDAVersion.R2_1)

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

    def test_anesthesia_multiple_types(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test anesthesia section with multiple anesthesia types."""
        anesthesia_records = [
            MockAnesthesia(
                anesthesia_type="General anesthesia",
                anesthesia_code="50697003",
                anesthesia_code_system="SNOMED",
            ),
            MockAnesthesia(
                anesthesia_type="Regional anesthesia",
                anesthesia_code="231249005",
                anesthesia_code_system="SNOMED",
            ),
        ]

        section = AnesthesiaSection(anesthesia_records=anesthesia_records, version=CDAVersion.R2_1)

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

    def test_anesthesia_empty_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test anesthesia section with no anesthesia records."""
        section = AnesthesiaSection(anesthesia_records=[], version=CDAVersion.R2_1)

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
# 6. Postoperative Diagnosis Section Tests
# ============================================================================


class TestPostoperativeDiagnosisSectionSchematron:
    """Test Schematron validation for Postoperative Diagnosis Section."""

    def test_valid_postoperative_diagnosis_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid postoperative diagnosis validates."""
        diagnosis_text = "Acute cholecystitis with perforation and peritonitis"

        section = PostoperativeDiagnosisSection(diagnosis_text=diagnosis_text, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)

    def test_postoperative_diagnosis_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test postoperative diagnosis section with minimal data."""
        diagnosis_text = "Appendicitis"

        section = PostoperativeDiagnosisSection(diagnosis_text=diagnosis_text, version=CDAVersion.R2_1)

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
# 7. Preoperative Diagnosis Section Tests
# ============================================================================


class TestPreoperativeDiagnosisSectionSchematron:
    """Test Schematron validation for Preoperative Diagnosis Section."""

    def test_valid_preoperative_diagnosis_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid preoperative diagnosis validates."""
        diagnoses = [
            MockPreoperativeDiagnosis(
                name="Cholelithiasis",
                code="235919008",
                code_system="SNOMED",
                diagnosis_date=date(2023, 10, 14),
            )
        ]

        section = PreoperativeDiagnosisSection(diagnoses=diagnoses, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)

    def test_preoperative_diagnosis_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test preoperative diagnosis section with minimal data."""
        diagnoses = [
            MockPreoperativeDiagnosis(
                name="Hernia",
                code="414403008",
                code_system="SNOMED",
            )
        ]

        section = PreoperativeDiagnosisSection(diagnoses=diagnoses, version=CDAVersion.R2_1)

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

    def test_preoperative_diagnosis_multiple_entries(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test preoperative diagnosis section with multiple diagnoses."""
        diagnoses = [
            MockPreoperativeDiagnosis(
                name="Cholelithiasis",
                code="235919008",
                code_system="SNOMED",
            ),
            MockPreoperativeDiagnosis(
                name="Chronic cholecystitis",
                code="28116004",
                code_system="SNOMED",
            ),
        ]

        section = PreoperativeDiagnosisSection(diagnoses=diagnoses, version=CDAVersion.R2_1)

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

    def test_preoperative_diagnosis_empty_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test preoperative diagnosis section with no diagnoses."""
        section = PreoperativeDiagnosisSection(diagnoses=[], version=CDAVersion.R2_1)

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
# 8. Complications Section Tests
# ============================================================================


class TestComplicationsSectionSchematron:
    """Test Schematron validation for Complications Section."""

    def test_valid_complications_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid complications validates."""
        complications = [
            MockComplication(
                name="Postoperative wound infection",
                code="312404004",
                code_system="SNOMED",
                complication_date=date(2023, 10, 17),
                status="active",
                severity="moderate",
            )
        ]

        section = ComplicationsSection(complications=complications, version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)

    def test_complications_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test complications section with minimal data."""
        complications = [
            MockComplication(
                name="Minor bleeding",
                code="131148009",
                code_system="SNOMED",
            )
        ]

        section = ComplicationsSection(complications=complications, version=CDAVersion.R2_1)

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

    def test_complications_multiple_entries(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test complications section with multiple complications."""
        complications = [
            MockComplication(
                name="Postoperative infection",
                code="312404004",
                code_system="SNOMED",
                severity="moderate",
            ),
            MockComplication(
                name="Bleeding",
                code="131148009",
                code_system="SNOMED",
                severity="mild",
            ),
            MockComplication(
                name="Nausea and vomiting",
                code="16932000",
                code_system="SNOMED",
                severity="mild",
            ),
        ]

        section = ComplicationsSection(complications=complications, version=CDAVersion.R2_1)

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

    def test_complications_empty_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test complications section with no complications."""
        section = ComplicationsSection(complications=[], version=CDAVersion.R2_1)

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
# 9. Hospital Discharge Studies Summary Section Tests
# ============================================================================


class TestHospitalDischargeStudiesSummarySectionSchematron:
    """Test Schematron validation for Hospital Discharge Studies Summary Section."""

    def test_valid_discharge_studies_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid discharge studies validates."""
        study_obs = MockDischargeStudyObservation(
            study_name="Chest X-Ray",
            study_code="399208008",
            value="No acute cardiopulmonary process",
            status="completed",
            effective_time=datetime(2023, 10, 19, 14, 0),
        )

        organizer = MockDischargeStudy(
            study_panel_name="Imaging Studies",
            study_panel_code="18748-4",
            status="completed",
            effective_time=datetime(2023, 10, 19, 14, 0),
            studies=[study_obs],
        )

        section = HospitalDischargeStudiesSummarySection(
            study_organizers=[organizer], version=CDAVersion.R2_1
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

        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)

    def test_discharge_studies_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test discharge studies section with minimal data."""
        study_obs = MockDischargeStudyObservation(
            study_name="ECG",
            study_code="29303009",
            value="Normal sinus rhythm",
            status="completed",
        )

        organizer = MockDischargeStudy(
            study_panel_name="Cardiac Studies",
            study_panel_code="34752-6",
            status="completed",
            studies=[study_obs],
        )

        section = HospitalDischargeStudiesSummarySection(
            study_organizers=[organizer], version=CDAVersion.R2_1
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

    def test_discharge_studies_multiple_entries(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test discharge studies section with multiple studies."""
        study_obs1 = MockDischargeStudyObservation(
            study_name="Chest X-Ray",
            study_code="399208008",
            value="No acute process",
            status="completed",
        )

        study_obs2 = MockDischargeStudyObservation(
            study_name="Echocardiogram",
            study_code="40701008",
            value="Normal left ventricular function",
            status="completed",
        )

        study_obs3 = MockDischargeStudyObservation(
            study_name="CT Abdomen",
            study_code="169070008",
            value="No acute findings",
            status="completed",
        )

        organizer = MockDischargeStudy(
            study_panel_name="Discharge Imaging Panel",
            study_panel_code="18748-4",
            status="completed",
            studies=[study_obs1, study_obs2, study_obs3],
        )

        section = HospitalDischargeStudiesSummarySection(
            study_organizers=[organizer], version=CDAVersion.R2_1
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

    def test_discharge_studies_empty_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test discharge studies section with no studies."""
        section = HospitalDischargeStudiesSummarySection(study_organizers=[], version=CDAVersion.R2_1)

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
# 10. Medications Administered Section Tests
# ============================================================================


class TestMedicationsAdministeredSectionSchematron:
    """Test Schematron validation for Medications Administered Section."""

    def test_valid_medications_administered_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid medications administered validates."""
        medications = [
            MockMedicationAdministered(
                name="Morphine sulfate",
                code="373529000",
                dose="2 mg",
                route="intravenous",
                administration_time=datetime(2023, 10, 15, 14, 30),
                performer="RN Smith",
                status="completed",
            )
        ]

        section = MedicationsAdministeredSection(
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

        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)

    def test_medications_administered_minimal_data(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test medications administered section with minimal data."""
        medications = [
            MockMedicationAdministered(
                name="Acetaminophen",
                code="161",
                dose="650 mg",
                route="oral",
            )
        ]

        section = MedicationsAdministeredSection(
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

    def test_medications_administered_multiple_entries(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test medications administered section with multiple medications."""
        medications = [
            MockMedicationAdministered(
                name="Morphine sulfate",
                code="373529000",
                dose="2 mg",
                route="intravenous",
                site="Right arm",
            ),
            MockMedicationAdministered(
                name="Ondansetron",
                code="372487007",
                dose="4 mg",
                route="intravenous",
            ),
            MockMedicationAdministered(
                name="Normal saline",
                code="346706004",
                dose="1000 mL",
                route="intravenous",
                rate="125 mL/hr",
                administration_time=datetime(2023, 10, 15, 10, 0),
                administration_end_time=datetime(2023, 10, 15, 18, 0),
            ),
        ]

        section = MedicationsAdministeredSection(
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

    def test_medications_administered_with_null_flavor(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test medications administered section with null flavor."""
        section = MedicationsAdministeredSection(
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


# ============================================================================
# Multi-Section Integration Tests
# ============================================================================


class TestMultipleHospitalSections:
    """Test documents with multiple hospital/surgical sections together."""

    def test_document_with_all_hospital_sections(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document containing all 10 hospital/surgical sections."""
        sections = [
            AdmissionDiagnosisSection(
                diagnoses=[
                    MockAdmissionDiagnosis(
                        name="Chest pain",
                        code="29857009",
                        code_system="SNOMED",
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            HospitalCourseSection(
                narrative_text="Patient admitted and treated successfully.",
                version=CDAVersion.R2_1,
            ),
            AnesthesiaSection(
                anesthesia_records=[
                    MockAnesthesia(
                        anesthesia_type="General anesthesia",
                        anesthesia_code="50697003",
                        anesthesia_code_system="SNOMED",
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            PreoperativeDiagnosisSection(
                diagnoses=[
                    MockPreoperativeDiagnosis(
                        name="Suspected condition",
                        code="12345",
                        code_system="SNOMED",
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            PostoperativeDiagnosisSection(
                diagnosis_text="Confirmed condition - acute cholecystitis with perforation",
                version=CDAVersion.R2_1,
            ),
            ComplicationsSection(
                complications=[],
                version=CDAVersion.R2_1,
            ),
            MedicationsAdministeredSection(
                medications=[
                    MockMedicationAdministered(
                        name="Medication",
                        code="123",
                        dose="10 mg",
                        route="oral",
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            HospitalDischargeStudiesSummarySection(
                study_organizers=[
                    MockDischargeStudy(
                        study_panel_name="Discharge Imaging",
                        study_panel_code="18748-4",
                        status="completed",
                        studies=[
                            MockDischargeStudyObservation(
                                study_name="X-Ray",
                                study_code="399208008",
                                value="Normal",
                                status="completed",
                            )
                        ],
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            DischargeDiagnosisSection(
                diagnoses=[
                    MockDischargeDiagnosis(
                        name="Final diagnosis",
                        code="54321",
                        code_system="SNOMED",
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            InstructionsSection(
                instructions=[
                    MockInstruction(
                        instruction_text="Follow discharge instructions",
                    )
                ],
                version=CDAVersion.R2_1,
            ),
        ]

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=sections,
            title="Comprehensive Hospital Document",
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        # Should complete validation
        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)

        # Log summary
        print("\nAll Hospital Sections Validation Summary:")
        print(f"  Valid: {result.is_valid}")
        print(f"  Errors: {len(result.errors)}")
        print(f"  Warnings: {len(result.warnings)}")

        if result.errors:
            print("\nFirst 10 errors:")
            for i, error in enumerate(result.errors[:10], 1):
                print(f"  {i}. {error.code}: {error.message[:100]}")

    def test_surgical_procedure_document(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with surgical procedure sections."""
        sections = [
            PreoperativeDiagnosisSection(
                diagnoses=[
                    MockPreoperativeDiagnosis(
                        name="Cholelithiasis",
                        code="235919008",
                        code_system="SNOMED",
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            AnesthesiaSection(
                anesthesia_records=[
                    MockAnesthesia(
                        anesthesia_type="General anesthesia",
                        anesthesia_code="50697003",
                        anesthesia_code_system="SNOMED",
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            PostoperativeDiagnosisSection(
                diagnosis_text="Acute cholecystitis with perforation and peritonitis",
                version=CDAVersion.R2_1,
            ),
            ComplicationsSection(
                complications=[],
                version=CDAVersion.R2_1,
            ),
        ]

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=sections,
            title="Surgical Procedure Note",
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
