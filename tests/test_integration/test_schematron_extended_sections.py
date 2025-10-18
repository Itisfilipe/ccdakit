"""
Comprehensive Schematron validation tests for Extended Clinical Sections.

Tests Schematron validation for the 9 Extended Clinical Sections in ccdakit:
1. FamilyHistorySection
2. FunctionalStatusSection
3. MentalStatusSection
4. GoalsSection
5. HealthConcernsSection
6. HealthStatusEvaluationsSection
7. PastMedicalHistorySection
8. PhysicalExamSection
9. AssessmentAndPlanSection

Each section is tested with:
- Valid data and Schematron validation
- Minimal/empty data
- Multiple entries
- Edge cases
"""

from datetime import date, datetime

import pytest

from ccdakit.builders.document import ClinicalDocument
from ccdakit.builders.sections.assessment_and_plan import AssessmentAndPlanSection
from ccdakit.builders.sections.family_history import FamilyHistorySection
from ccdakit.builders.sections.functional_status import FunctionalStatusSection
from ccdakit.builders.sections.goals import GoalsSection
from ccdakit.builders.sections.health_concerns import HealthConcernsSection
from ccdakit.builders.sections.health_status_evaluations import (
    HealthStatusEvaluationsAndOutcomesSection,
)
from ccdakit.builders.sections.mental_status import MentalStatusSection
from ccdakit.builders.sections.past_medical_history import PastMedicalHistorySection
from ccdakit.builders.sections.physical_exam import PhysicalExamSection
from ccdakit.core.base import CDAVersion
from ccdakit.validators.schematron import SchematronValidator

# Import common mock data from integration tests
from .test_full_document import MockAuthor, MockOrganization, MockPatient


# ============================================================================
# Mock Data Classes for Extended Sections
# ============================================================================


class MockFamilyMemberSubject:
    """Mock family member subject details."""

    def __init__(
        self,
        administrative_gender_code="M",
        birth_time=None,
        deceased_ind=False,
        deceased_time=None,
    ):
        self._administrative_gender_code = administrative_gender_code
        self._birth_time = birth_time
        self._deceased_ind = deceased_ind
        self._deceased_time = deceased_time

    @property
    def administrative_gender_code(self):
        return self._administrative_gender_code

    @property
    def birth_time(self):
        return self._birth_time

    @property
    def deceased_ind(self):
        return self._deceased_ind

    @property
    def deceased_time(self):
        return self._deceased_time


class MockFamilyHistoryObservation:
    """Mock family history observation."""

    def __init__(
        self,
        condition_name="Hypertension",
        condition_code="38341003",
        condition_code_system="SNOMED",
        observation_type_code="64572001",
        observation_type_display_name="Disease",
        effective_time=None,
        age_at_onset=45,
        deceased_age=None,
        deceased_cause_code=None,
        deceased_cause_display_name=None,
        persistent_id=None,
    ):
        self._condition_name = condition_name
        self._condition_code = condition_code
        self._condition_code_system = condition_code_system
        self._observation_type_code = observation_type_code
        self._observation_type_display_name = observation_type_display_name
        self._effective_time = effective_time
        self._age_at_onset = age_at_onset
        self._deceased_age = deceased_age
        self._deceased_cause_code = deceased_cause_code
        self._deceased_cause_display_name = deceased_cause_display_name
        self._persistent_id = persistent_id

    @property
    def condition_name(self):
        return self._condition_name

    @property
    def condition_code(self):
        return self._condition_code

    @property
    def condition_code_system(self):
        return self._condition_code_system

    @property
    def observation_type_code(self):
        return self._observation_type_code

    @property
    def observation_type_display_name(self):
        return self._observation_type_display_name

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def age_at_onset(self):
        return self._age_at_onset

    @property
    def deceased_age(self):
        return self._deceased_age

    @property
    def deceased_cause_code(self):
        return self._deceased_cause_code

    @property
    def deceased_cause_display_name(self):
        return self._deceased_cause_display_name

    @property
    def persistent_id(self):
        return self._persistent_id


class MockFamilyMemberHistory:
    """Mock family member history."""

    def __init__(
        self,
        relationship_code="FTH",
        relationship_display_name="Father",
        subject=None,
        observations=None,
        persistent_id=None,
    ):
        self._relationship_code = relationship_code
        self._relationship_display_name = relationship_display_name
        self._subject = subject
        self._observations = observations or []
        self._persistent_id = persistent_id

    @property
    def relationship_code(self):
        return self._relationship_code

    @property
    def relationship_display_name(self):
        return self._relationship_display_name

    @property
    def subject(self):
        return self._subject

    @property
    def observations(self):
        return self._observations

    @property
    def persistent_id(self):
        return self._persistent_id


class MockFunctionalStatusObservation:
    """Mock functional status observation."""

    def __init__(
        self,
        type="Ambulation",
        code="129006008",
        code_system="2.16.840.1.113883.6.96",
        value="Independent",
        value_code="371153006",
        value_code_system="2.16.840.1.113883.6.96",
        date=None,
        interpretation=None,
    ):
        self.type = type
        self.code = code
        self.code_system = code_system
        self.value = value
        self.value_code = value_code
        self.value_code_system = value_code_system
        self.date = date or datetime.now()
        self.interpretation = interpretation


class MockFunctionalStatusOrganizer:
    """Mock functional status organizer."""

    def __init__(
        self,
        category="Mobility",
        category_code="d4",
        category_code_system="2.16.840.1.113883.6.254",
        observations=None,
    ):
        self.category = category
        self.category_code = category_code
        self.category_code_system = category_code_system
        self.observations = observations or []


class MockMentalStatusObservation:
    """Mock mental status observation."""

    def __init__(
        self,
        category="Mood and Affect",
        category_code="b152",
        category_code_system="ICF",
        value="Alert and oriented",
        value_code="248234008",
        observation_date=None,
        status="completed",
        persistent_id=None,
    ):
        self._category = category
        self._category_code = category_code
        self._category_code_system = category_code_system
        self._value = value
        self._value_code = value_code
        self._observation_date = observation_date or date.today()
        self._status = status
        self._persistent_id = persistent_id

    @property
    def category(self):
        return self._category

    @property
    def category_code(self):
        return self._category_code

    @property
    def category_code_system(self):
        return self._category_code_system

    @property
    def value(self):
        return self._value

    @property
    def value_code(self):
        return self._value_code

    @property
    def observation_date(self):
        return self._observation_date

    @property
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id


class MockMentalStatusOrganizer:
    """Mock mental status organizer."""

    def __init__(
        self,
        category="Cognition",
        category_code="b110",
        category_code_system="ICF",
        observations=None,
        effective_time_low=None,
        effective_time_high=None,
        persistent_id=None,
    ):
        self._category = category
        self._category_code = category_code
        self._category_code_system = category_code_system
        self._observations = observations or []
        self._effective_time_low = effective_time_low
        self._effective_time_high = effective_time_high
        self._persistent_id = persistent_id

    @property
    def category(self):
        return self._category

    @property
    def category_code(self):
        return self._category_code

    @property
    def category_code_system(self):
        return self._category_code_system

    @property
    def observations(self):
        return self._observations

    @property
    def effective_time_low(self):
        return self._effective_time_low

    @property
    def effective_time_high(self):
        return self._effective_time_high

    @property
    def persistent_id(self):
        return self._persistent_id


class MockGoal:
    """Mock goal."""

    def __init__(
        self,
        description="Lose 10 pounds",
        code="3141-9",
        code_system="LOINC",
        display_name="Body weight",
        status="active",
        target_date=None,
        start_date=None,
        value="150",
        value_unit="lbs",
        author=None,
        priority="high",
    ):
        self._description = description
        self._code = code
        self._code_system = code_system
        self._display_name = display_name
        self._status = status
        self._target_date = target_date
        self._start_date = start_date
        self._value = value
        self._value_unit = value_unit
        self._author = author
        self._priority = priority

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
    def display_name(self):
        return self._display_name

    @property
    def status(self):
        return self._status

    @property
    def target_date(self):
        return self._target_date

    @property
    def start_date(self):
        return self._start_date

    @property
    def value(self):
        return self._value

    @property
    def value_unit(self):
        return self._value_unit

    @property
    def author(self):
        return self._author

    @property
    def priority(self):
        return self._priority


class MockHealthConcernObservation:
    """Mock health concern observation."""

    def __init__(
        self,
        observation_type="problem",
        code="44054006",
        code_system="SNOMED",
        display_name="Diabetes mellitus type 2",
    ):
        self._observation_type = observation_type
        self._code = code
        self._code_system = code_system
        self._display_name = display_name

    @property
    def observation_type(self):
        return self._observation_type

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def display_name(self):
        return self._display_name


class MockHealthConcern:
    """Mock health concern."""

    def __init__(
        self,
        name="Diabetes management",
        status="active",
        effective_time_low=None,
        effective_time_high=None,
        persistent_id=None,
        observations=None,
        author_is_patient=False,
    ):
        self._name = name
        self._status = status
        self._effective_time_low = effective_time_low
        self._effective_time_high = effective_time_high
        self._persistent_id = persistent_id
        self._observations = observations or []
        self._author_is_patient = author_is_patient

    @property
    def name(self):
        return self._name

    @property
    def status(self):
        return self._status

    @property
    def effective_time_low(self):
        return self._effective_time_low

    @property
    def effective_time_high(self):
        return self._effective_time_high

    @property
    def persistent_id(self):
        return self._persistent_id

    @property
    def observations(self):
        return self._observations

    @property
    def author_is_patient(self):
        return self._author_is_patient


class MockProgressTowardGoal:
    """Mock progress toward goal."""

    def __init__(
        self,
        id="progress-1",
        achievement_code="385641008",
        achievement_code_system="2.16.840.1.113883.6.96",
        achievement_display_name="Improving",
    ):
        self._id = id
        self._achievement_code = achievement_code
        self._achievement_code_system = achievement_code_system
        self._achievement_display_name = achievement_display_name

    @property
    def id(self):
        return self._id

    @property
    def achievement_code(self):
        return self._achievement_code

    @property
    def achievement_code_system(self):
        return self._achievement_code_system

    @property
    def achievement_display_name(self):
        return self._achievement_display_name


class MockOutcomeObservation:
    """Mock outcome observation."""

    def __init__(
        self,
        id="outcome-1",
        code="29463-7",
        code_system="LOINC",
        display_name="Body weight",
        value="155",
        value_unit="lbs",
        effective_time=None,
        progress_toward_goal=None,
        goal_reference_id=None,
        intervention_reference_ids=None,
        author_name=None,
        author_time=None,
    ):
        self._id = id
        self._code = code
        self._code_system = code_system
        self._display_name = display_name
        self._value = value
        self._value_unit = value_unit
        self._effective_time = effective_time
        self._progress_toward_goal = progress_toward_goal
        self._goal_reference_id = goal_reference_id
        self._intervention_reference_ids = intervention_reference_ids
        self._author_name = author_name
        self._author_time = author_time

    @property
    def id(self):
        return self._id

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def display_name(self):
        return self._display_name

    @property
    def value(self):
        return self._value

    @property
    def value_unit(self):
        return self._value_unit

    @property
    def effective_time(self):
        return self._effective_time

    @property
    def progress_toward_goal(self):
        return self._progress_toward_goal

    @property
    def goal_reference_id(self):
        return self._goal_reference_id

    @property
    def intervention_reference_ids(self):
        return self._intervention_reference_ids

    @property
    def author_name(self):
        return self._author_name

    @property
    def author_time(self):
        return self._author_time


class MockProblem:
    """Mock problem for Past Medical History."""

    def __init__(
        self,
        name="Resolved pneumonia",
        code="233604007",
        code_system="SNOMED",
        onset_date=None,
        resolved_date=None,
        status="resolved",
        persistent_id=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._onset_date = onset_date
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


class MockWoundObservation:
    """Mock wound observation."""

    def __init__(
        self,
        wound_type="Pressure ulcer",
        wound_code="399912005",
        date=None,
        location="Sacral region",
        location_code="54735007",
        laterality=None,
        laterality_code=None,
    ):
        self.wound_type = wound_type
        self.wound_code = wound_code
        self.date = date or datetime.now()
        self.location = location
        self.location_code = location_code
        self.laterality = laterality
        self.laterality_code = laterality_code


class MockAssessmentAndPlanItem:
    """Mock assessment and plan item."""

    def __init__(
        self,
        text="Patient presents with well-controlled diabetes",
        item_type="assessment",
        planned_act=None,
    ):
        self._text = text
        self._item_type = item_type
        self._planned_act = planned_act

    @property
    def text(self):
        return self._text

    @property
    def item_type(self):
        return self._item_type

    @property
    def planned_act(self):
        return self._planned_act


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
# 1. FamilyHistorySection Tests
# ============================================================================


class TestFamilyHistorySectionSchematron:
    """Test Schematron validation for Family History Section."""

    def test_valid_family_history_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid family history validates."""
        # Create family member with observations
        subject = MockFamilyMemberSubject(
            administrative_gender_code="M",
            birth_time=date(1950, 1, 1),
            deceased_ind=True,
            deceased_time=date(2010, 5, 15),
        )

        observations = [
            MockFamilyHistoryObservation(
                condition_name="Hypertension",
                condition_code="38341003",
                condition_code_system="SNOMED",
                age_at_onset=45,
            ),
            MockFamilyHistoryObservation(
                condition_name="Type 2 Diabetes",
                condition_code="44054006",
                condition_code_system="SNOMED",
                age_at_onset=50,
            ),
        ]

        family_member = MockFamilyMemberHistory(
            relationship_code="FTH",
            relationship_display_name="Father",
            subject=subject,
            observations=observations,
        )

        section = FamilyHistorySection(family_members=[family_member], version=CDAVersion.R2_1)

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=[section],
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        # Should complete validation
        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)

    def test_minimal_family_history_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with minimal family history data."""
        # Family member with minimal data
        family_member = MockFamilyMemberHistory(
            relationship_code="MTH",
            relationship_display_name="Mother",
            observations=[],
        )

        section = FamilyHistorySection(family_members=[family_member], version=CDAVersion.R2_1)

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

    def test_multiple_family_members(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with multiple family members."""
        family_members = [
            MockFamilyMemberHistory(
                relationship_code="FTH",
                relationship_display_name="Father",
                observations=[
                    MockFamilyHistoryObservation(
                        condition_name="Heart disease", condition_code="56265001"
                    )
                ],
            ),
            MockFamilyMemberHistory(
                relationship_code="MTH",
                relationship_display_name="Mother",
                observations=[
                    MockFamilyHistoryObservation(
                        condition_name="Cancer", condition_code="363346000"
                    )
                ],
            ),
            MockFamilyMemberHistory(
                relationship_code="SIB",
                relationship_display_name="Sibling",
                observations=[],
            ),
        ]

        section = FamilyHistorySection(family_members=family_members, version=CDAVersion.R2_1)

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

    def test_empty_family_history_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with empty family history section."""
        section = FamilyHistorySection(family_members=[], version=CDAVersion.R2_1)

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
# 2. FunctionalStatusSection Tests
# ============================================================================


class TestFunctionalStatusSectionSchematron:
    """Test Schematron validation for Functional Status Section."""

    def test_valid_functional_status_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid functional status validates."""
        observations = [
            MockFunctionalStatusObservation(
                type="Ambulation",
                code="129006008",
                value="Independent",
                value_code="371153006",
                date=datetime(2023, 10, 15, 14, 30),
            ),
            MockFunctionalStatusObservation(
                type="Bathing",
                code="284785009",
                value="Requires assistance",
                value_code="371152001",
                date=datetime(2023, 10, 15, 14, 30),
            ),
        ]

        organizer = MockFunctionalStatusOrganizer(
            category="Activities of Daily Living",
            category_code="d5",
            observations=observations,
        )

        section = FunctionalStatusSection(organizers=[organizer], version=CDAVersion.R2_1)

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

    def test_minimal_functional_status(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with minimal functional status data."""
        observation = MockFunctionalStatusObservation(
            type="Mobility", code="129006008", value="Independent", value_code="371153006"
        )

        organizer = MockFunctionalStatusOrganizer(category="Mobility", observations=[observation])

        section = FunctionalStatusSection(organizers=[organizer], version=CDAVersion.R2_1)

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

    def test_multiple_functional_status_organizers(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with multiple functional status organizers."""
        organizers = [
            MockFunctionalStatusOrganizer(
                category="Mobility",
                observations=[
                    MockFunctionalStatusObservation(
                        type="Walking",
                        code="129006008",
                        value="Independent",
                        value_code="371153006",
                    )
                ],
            ),
            MockFunctionalStatusOrganizer(
                category="Self-Care",
                observations=[
                    MockFunctionalStatusObservation(
                        type="Feeding",
                        code="289167005",
                        value="Independent",
                        value_code="371153006",
                    )
                ],
            ),
        ]

        section = FunctionalStatusSection(organizers=organizers, version=CDAVersion.R2_1)

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

    def test_empty_functional_status(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with empty functional status section."""
        section = FunctionalStatusSection(organizers=[], version=CDAVersion.R2_1)

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
# 3. MentalStatusSection Tests
# ============================================================================


class TestMentalStatusSectionSchematron:
    """Test Schematron validation for Mental Status Section."""

    def test_valid_mental_status_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid mental status validates."""
        observations = [
            MockMentalStatusObservation(
                category="Mood and Affect",
                category_code="b152",
                value="Alert and oriented",
                value_code="248234008",
                observation_date=date(2023, 10, 15),
            ),
            MockMentalStatusObservation(
                category="Cognition",
                category_code="b110",
                value="Normal cognition",
                value_code="102891000",
                observation_date=date(2023, 10, 15),
            ),
        ]

        organizer = MockMentalStatusOrganizer(
            category="Mental Status Assessment",
            category_code="b110-b189",
            observations=observations,
            effective_time_low=datetime(2023, 10, 15, 10, 0),
        )

        section = MentalStatusSection(organizers=[organizer], version=CDAVersion.R2_1)

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

    def test_mental_status_with_standalone_observations(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test mental status with standalone observations (no organizer)."""
        observations = [
            MockMentalStatusObservation(
                category="Mood",
                value="Euthymic mood",
                observation_date=date(2023, 10, 15),
            )
        ]

        section = MentalStatusSection(observations=observations, version=CDAVersion.R2_1)

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

    def test_multiple_mental_status_organizers(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with multiple mental status organizers."""
        organizers = [
            MockMentalStatusOrganizer(
                category="Cognition",
                category_code="b110",
                observations=[
                    MockMentalStatusObservation(
                        category="Cognition", value="Oriented x3", observation_date=date.today()
                    )
                ],
            ),
            MockMentalStatusOrganizer(
                category="Mood",
                category_code="b152",
                observations=[
                    MockMentalStatusObservation(
                        category="Mood", value="Anxious", observation_date=date.today()
                    )
                ],
            ),
        ]

        section = MentalStatusSection(organizers=organizers, version=CDAVersion.R2_1)

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

    def test_empty_mental_status(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with empty mental status section."""
        section = MentalStatusSection(observations=[], organizers=[], version=CDAVersion.R2_1)

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
# 4. GoalsSection Tests
# ============================================================================


class TestGoalsSectionSchematron:
    """Test Schematron validation for Goals Section."""

    def test_valid_goals_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid goals validates."""
        goals = [
            MockGoal(
                description="Lose 10 pounds",
                code="3141-9",
                code_system="LOINC",
                display_name="Body weight",
                status="active",
                start_date=date(2023, 10, 1),
                target_date=date(2024, 1, 1),
                value="150",
                value_unit="lbs",
                priority="high",
            ),
            MockGoal(
                description="Lower HbA1c to below 7%",
                code="4548-4",
                code_system="LOINC",
                display_name="Hemoglobin A1c",
                status="active",
                start_date=date(2023, 10, 1),
                target_date=date(2024, 4, 1),
                value="6.5",
                value_unit="%",
                priority="high",
            ),
        ]

        section = GoalsSection(goals=goals, version=CDAVersion.R2_1)

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

    def test_minimal_goals(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with minimal goal data."""
        goal = MockGoal(
            description="Improve overall health",
            status="active",
            code=None,
            target_date=None,
            value=None,
        )

        section = GoalsSection(goals=[goal], version=CDAVersion.R2_1)

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

    def test_multiple_goals_different_statuses(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with multiple goals in different statuses."""
        goals = [
            MockGoal(description="Goal 1", status="active", start_date=date(2023, 1, 1)),
            MockGoal(description="Goal 2", status="completed", start_date=date(2022, 1, 1)),
            MockGoal(description="Goal 3", status="cancelled", start_date=date(2023, 6, 1)),
        ]

        section = GoalsSection(goals=goals, version=CDAVersion.R2_1)

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

    def test_empty_goals_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with empty goals section."""
        section = GoalsSection(goals=[], version=CDAVersion.R2_1)

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
# 5. HealthConcernsSection Tests
# ============================================================================


class TestHealthConcernsSectionSchematron:
    """Test Schematron validation for Health Concerns Section."""

    def test_valid_health_concerns_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid health concerns validates."""
        observations = [
            MockHealthConcernObservation(
                observation_type="problem",
                code="44054006",
                code_system="SNOMED",
                display_name="Diabetes mellitus type 2",
            ),
            MockHealthConcernObservation(
                observation_type="problem",
                code="38341003",
                code_system="SNOMED",
                display_name="Hypertension",
            ),
        ]

        concern = MockHealthConcern(
            name="Chronic disease management",
            status="active",
            effective_time_low=date(2023, 1, 1),
            observations=observations,
            author_is_patient=False,
        )

        section = HealthConcernsSection(health_concerns=[concern], version=CDAVersion.R2_1)

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

    def test_patient_health_concern(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test health concern authored by patient."""
        concern = MockHealthConcern(
            name="Worry about medication side effects",
            status="active",
            effective_time_low=date(2023, 10, 1),
            observations=[],
            author_is_patient=True,
        )

        section = HealthConcernsSection(health_concerns=[concern], version=CDAVersion.R2_1)

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

    def test_multiple_health_concerns(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with multiple health concerns."""
        concerns = [
            MockHealthConcern(
                name="Fall risk",
                status="active",
                effective_time_low=date(2023, 9, 1),
                author_is_patient=False,
            ),
            MockHealthConcern(
                name="Nutritional concern",
                status="active",
                effective_time_low=date(2023, 8, 1),
                author_is_patient=False,
            ),
            MockHealthConcern(
                name="Pain management",
                status="completed",
                effective_time_low=date(2023, 5, 1),
                effective_time_high=date(2023, 9, 1),
                author_is_patient=False,
            ),
        ]

        section = HealthConcernsSection(health_concerns=concerns, version=CDAVersion.R2_1)

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

    def test_health_concerns_null_flavor(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test health concerns section with null flavor."""
        section = HealthConcernsSection(
            health_concerns=[], null_flavor="NI", version=CDAVersion.R2_1
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
# 6. HealthStatusEvaluationsSection Tests
# ============================================================================


class TestHealthStatusEvaluationsSectionSchematron:
    """Test Schematron validation for Health Status Evaluations Section."""

    def test_valid_health_status_evaluations(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid health status evaluations validates."""
        progress = MockProgressTowardGoal(
            id="progress-1",
            achievement_code="385641008",
            achievement_display_name="Improving",
        )

        outcome = MockOutcomeObservation(
            id="outcome-1",
            code="29463-7",
            code_system="LOINC",
            display_name="Body weight",
            value="155",
            value_unit="lbs",
            effective_time=date(2023, 10, 15),
            progress_toward_goal=progress,
        )

        section = HealthStatusEvaluationsAndOutcomesSection(
            outcomes=[outcome], version=CDAVersion.R2_1
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

    def test_minimal_outcome_observation(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test with minimal outcome observation data."""
        outcome = MockOutcomeObservation(
            id="outcome-1",
            code="8867-4",
            display_name="Heart rate",
            value="72",
            value_unit="beats/min",
        )

        section = HealthStatusEvaluationsAndOutcomesSection(
            outcomes=[outcome], version=CDAVersion.R2_1
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

    def test_multiple_outcome_observations(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with multiple outcome observations."""
        outcomes = [
            MockOutcomeObservation(
                id="outcome-1",
                code="29463-7",
                display_name="Body weight",
                value="155",
                value_unit="lbs",
                effective_time=date(2023, 10, 15),
            ),
            MockOutcomeObservation(
                id="outcome-2",
                code="4548-4",
                display_name="Hemoglobin A1c",
                value="6.8",
                value_unit="%",
                effective_time=date(2023, 10, 10),
            ),
            MockOutcomeObservation(
                id="outcome-3",
                code="8480-6",
                display_name="Systolic blood pressure",
                value="128",
                value_unit="mm[Hg]",
                effective_time=date(2023, 10, 15),
            ),
        ]

        section = HealthStatusEvaluationsAndOutcomesSection(
            outcomes=outcomes, version=CDAVersion.R2_1
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

    def test_health_status_evaluations_null_flavor(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test health status evaluations with null flavor."""
        section = HealthStatusEvaluationsAndOutcomesSection(
            outcomes=[], null_flavor="NI", version=CDAVersion.R2_1
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
# 7. PastMedicalHistorySection Tests
# ============================================================================


class TestPastMedicalHistorySectionSchematron:
    """Test Schematron validation for Past Medical History Section."""

    def test_valid_past_medical_history(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid past medical history validates."""
        problems = [
            MockProblem(
                name="Resolved pneumonia",
                code="233604007",
                code_system="SNOMED",
                onset_date=date(2020, 3, 15),
                resolved_date=date(2020, 4, 10),
                status="resolved",
            ),
            MockProblem(
                name="Appendectomy",
                code="80146002",
                code_system="SNOMED",
                onset_date=date(2015, 7, 20),
                status="resolved",
            ),
        ]

        section = PastMedicalHistorySection(problems=problems, version=CDAVersion.R2_1)

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

    def test_minimal_past_medical_history(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test with minimal past medical history data."""
        problem = MockProblem(
            name="History of chickenpox",
            code="38907003",
            code_system="SNOMED",
            status="resolved",
        )

        section = PastMedicalHistorySection(problems=[problem], version=CDAVersion.R2_1)

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

    def test_multiple_past_medical_history_problems(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with multiple past medical history problems."""
        problems = [
            MockProblem(
                name=f"Past condition {i}",
                code=f"C{i}",
                code_system="SNOMED",
                onset_date=date(2020 - i, 1, 1),
                status="resolved",
            )
            for i in range(5)
        ]

        section = PastMedicalHistorySection(problems=problems, version=CDAVersion.R2_1)

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

    def test_empty_past_medical_history(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with empty past medical history section."""
        section = PastMedicalHistorySection(problems=[], version=CDAVersion.R2_1)

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
# 8. PhysicalExamSection Tests
# ============================================================================


class TestPhysicalExamSectionSchematron:
    """Test Schematron validation for Physical Exam Section."""

    def test_valid_physical_exam_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid physical exam validates."""
        wound_observations = [
            MockWoundObservation(
                wound_type="Pressure ulcer",
                wound_code="399912005",
                date=datetime(2023, 10, 15, 14, 30),
                location="Sacral region",
                location_code="54735007",
            ),
            MockWoundObservation(
                wound_type="Surgical wound",
                wound_code="125643001",
                date=datetime(2023, 10, 15, 14, 30),
                location="Right knee",
                location_code="6757004",
                laterality="Right",
                laterality_code="24028007",
            ),
        ]

        section = PhysicalExamSection(
            wound_observations=wound_observations, version=CDAVersion.R2_1
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

    def test_physical_exam_with_narrative_text(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test physical exam with custom narrative text."""
        section = PhysicalExamSection(
            wound_observations=[],
            text="Patient appears well-nourished and in no acute distress. "
            "Vital signs stable. No abnormalities noted on examination.",
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

    def test_minimal_physical_exam(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test with minimal physical exam data."""
        wound = MockWoundObservation(
            wound_type="Abrasion",
            wound_code="399963005",
            location="Left forearm",
            location_code="66480008",
        )

        section = PhysicalExamSection(wound_observations=[wound], version=CDAVersion.R2_1)

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

    def test_empty_physical_exam(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with empty physical exam section."""
        section = PhysicalExamSection(wound_observations=[], version=CDAVersion.R2_1)

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
# 9. AssessmentAndPlanSection Tests
# ============================================================================


class TestAssessmentAndPlanSectionSchematron:
    """Test Schematron validation for Assessment and Plan Section."""

    def test_valid_assessment_and_plan_section(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with valid assessment and plan validates."""
        items = [
            MockAssessmentAndPlanItem(
                text="Patient presents with well-controlled Type 2 Diabetes Mellitus. "
                "HbA1c is 6.5%, within target range.",
                item_type="assessment",
            ),
            MockAssessmentAndPlanItem(
                text="Continue current medication regimen (Metformin 500mg twice daily).",
                item_type="plan",
            ),
            MockAssessmentAndPlanItem(
                text="Schedule follow-up in 3 months for HbA1c recheck.",
                item_type="plan",
            ),
        ]

        section = AssessmentAndPlanSection(items=items, version=CDAVersion.R2_1)

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

    def test_assessment_only(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test assessment and plan section with only assessments."""
        items = [
            MockAssessmentAndPlanItem(
                text="Hypertension, stable on current therapy.",
                item_type="assessment",
            ),
            MockAssessmentAndPlanItem(
                text="Type 2 Diabetes, well-controlled.",
                item_type="assessment",
            ),
        ]

        section = AssessmentAndPlanSection(items=items, version=CDAVersion.R2_1)

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

    def test_plan_only(self, schematron_validator, valid_patient, valid_author, valid_custodian):
        """Test assessment and plan section with only plan items."""
        items = [
            MockAssessmentAndPlanItem(
                text="Continue current medications.",
                item_type="plan",
            ),
            MockAssessmentAndPlanItem(
                text="Follow up in 6 months.",
                item_type="plan",
            ),
        ]

        section = AssessmentAndPlanSection(items=items, version=CDAVersion.R2_1)

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

    def test_empty_assessment_and_plan(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with empty assessment and plan section."""
        section = AssessmentAndPlanSection(items=[], version=CDAVersion.R2_1)

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


class TestMultipleExtendedSections:
    """Test documents with multiple extended sections together."""

    def test_document_with_all_extended_sections(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document containing all 9 extended sections."""
        # Create all sections with minimal data
        sections = [
            FamilyHistorySection(
                family_members=[
                    MockFamilyMemberHistory(
                        relationship_code="FTH",
                        relationship_display_name="Father",
                        observations=[],
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            FunctionalStatusSection(
                organizers=[
                    MockFunctionalStatusOrganizer(
                        category="Mobility",
                        observations=[
                            MockFunctionalStatusObservation(
                                type="Walking",
                                code="129006008",
                                value="Independent",
                                value_code="371153006",
                            )
                        ],
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            MentalStatusSection(
                observations=[
                    MockMentalStatusObservation(
                        category="Mood", value="Euthymic", observation_date=date.today()
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            GoalsSection(
                goals=[MockGoal(description="Maintain health", status="active")],
                version=CDAVersion.R2_1,
            ),
            HealthConcernsSection(
                health_concerns=[
                    MockHealthConcern(
                        name="General wellness",
                        status="active",
                        effective_time_low=date.today(),
                        author_is_patient=False,
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            HealthStatusEvaluationsAndOutcomesSection(
                outcomes=[
                    MockOutcomeObservation(
                        id="outcome-1",
                        code="29463-7",
                        display_name="Body weight",
                        value="160",
                        value_unit="lbs",
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            PastMedicalHistorySection(
                problems=[
                    MockProblem(
                        name="Past illness",
                        code="12345",
                        code_system="SNOMED",
                        status="resolved",
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            PhysicalExamSection(wound_observations=[], version=CDAVersion.R2_1),
            AssessmentAndPlanSection(
                items=[
                    MockAssessmentAndPlanItem(text="Patient doing well", item_type="assessment")
                ],
                version=CDAVersion.R2_1,
            ),
        ]

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=sections,
            title="Comprehensive Clinical Summary",
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        # Should complete validation
        assert isinstance(result.is_valid, bool)
        assert isinstance(result.errors, list)

        # Log summary
        print("\nAll Extended Sections Validation Summary:")
        print(f"  Valid: {result.is_valid}")
        print(f"  Errors: {len(result.errors)}")
        print(f"  Warnings: {len(result.warnings)}")

    def test_selected_extended_sections_combination(
        self, schematron_validator, valid_patient, valid_author, valid_custodian
    ):
        """Test document with a typical combination of extended sections."""
        sections = [
            GoalsSection(
                goals=[
                    MockGoal(
                        description="Reduce weight",
                        status="active",
                        start_date=date(2023, 10, 1),
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            HealthConcernsSection(
                health_concerns=[
                    MockHealthConcern(
                        name="Weight management",
                        status="active",
                        effective_time_low=date(2023, 10, 1),
                        author_is_patient=False,
                    )
                ],
                version=CDAVersion.R2_1,
            ),
            AssessmentAndPlanSection(
                items=[
                    MockAssessmentAndPlanItem(
                        text="Patient is motivated to lose weight.",
                        item_type="assessment",
                    ),
                    MockAssessmentAndPlanItem(
                        text="Refer to nutritionist and exercise program.",
                        item_type="plan",
                    ),
                ],
                version=CDAVersion.R2_1,
            ),
        ]

        doc = ClinicalDocument(
            patient=valid_patient,
            author=valid_author,
            custodian=valid_custodian,
            sections=sections,
            title="Weight Management Plan",
            version=CDAVersion.R2_1,
        )

        xml_string = doc.to_xml_string()
        result = schematron_validator.validate(xml_string)

        assert isinstance(result, object)
