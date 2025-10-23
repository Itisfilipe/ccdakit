"""Tests for Family Member History entry builders."""

from datetime import date

from lxml import etree

from ccdakit.builders.entries.family_member_history import (
    FamilyHistoryObservation,
    FamilyHistoryOrganizer,
)
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"
SDTC_NS = "urn:hl7-org:sdtc"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockPersistentID:
    """Mock persistent ID for testing."""

    def __init__(self, root="2.16.840.1.113883.19", extension="obs-123"):
        self._root = root
        self._extension = extension

    @property
    def root(self):
        return self._root

    @property
    def extension(self):
        return self._extension


class MockFamilyMemberSubject:
    """Mock family member subject details for testing."""

    def __init__(
        self,
        administrative_gender_code="M",
        birth_time=date(1950, 5, 15),
        deceased_ind=None,
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
    """Mock family history observation for testing."""

    def __init__(
        self,
        condition_name="Diabetes",
        condition_code="73211009",
        condition_code_system="SNOMED",
        observation_type_code=None,
        observation_type_display_name=None,
        effective_time=None,
        age_at_onset=None,
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
    """Mock family member history for testing."""

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


class TestFamilyHistoryObservation:
    """Tests for FamilyHistoryObservation builder."""

    def test_observation_basic(self):
        """Test basic FamilyHistoryObservation creation."""
        obs = MockFamilyHistoryObservation()
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        assert local_name(elem) == "observation"
        assert elem.get("classCode") == "OBS"
        assert elem.get("moodCode") == "EVN"

    def test_observation_has_template_id_r21(self):
        """Test FamilyHistoryObservation includes R2.1 template ID."""
        obs = MockFamilyHistoryObservation()
        builder = FamilyHistoryObservation(obs, version=CDAVersion.R2_1)
        elem = builder.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.46"
        assert template.get("extension") == "2015-08-01"

    def test_observation_has_template_id_r20(self):
        """Test FamilyHistoryObservation includes R2.0 template ID."""
        obs = MockFamilyHistoryObservation()
        builder = FamilyHistoryObservation(obs, version=CDAVersion.R2_0)
        elem = builder.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.46"
        assert template.get("extension") == "2015-08-01"

    def test_observation_has_id(self):
        """Test FamilyHistoryObservation has ID element."""
        obs = MockFamilyHistoryObservation()
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_observation_has_persistent_id(self):
        """Test FamilyHistoryObservation with persistent ID."""
        persistent_id = MockPersistentID(
            root="2.16.840.1.113883.19",
            extension="obs-123",
        )
        obs = MockFamilyHistoryObservation(persistent_id=persistent_id)
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.19"
        assert id_elem.get("extension") == "obs-123"

    def test_observation_has_code(self):
        """Test FamilyHistoryObservation has code element with translation."""
        obs = MockFamilyHistoryObservation()
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "64572001"  # Default: Disease
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"

        # Check translation
        translation = code.find(f"{{{NS}}}translation")
        assert translation is not None
        assert translation.get("code") == "75315-2"
        assert translation.get("codeSystem") == "2.16.840.1.113883.6.1"

    def test_observation_has_status_code(self):
        """Test FamilyHistoryObservation has statusCode=completed."""
        obs = MockFamilyHistoryObservation()
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_observation_effective_time(self):
        """Test FamilyHistoryObservation with effectiveTime."""
        obs = MockFamilyHistoryObservation(effective_time=date(2020, 5, 15))
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None
        assert time_elem.get("value") == "20200515"

    def test_observation_no_effective_time(self):
        """Test FamilyHistoryObservation without effectiveTime."""
        obs = MockFamilyHistoryObservation(effective_time=None)
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is None

    def test_observation_value_snomed(self):
        """Test FamilyHistoryObservation value with SNOMED CT code."""
        obs = MockFamilyHistoryObservation(
            condition_name="Diabetes",
            condition_code="73211009",
            condition_code_system="SNOMED",
        )
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        xsi_type = value.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        assert xsi_type == "CD"
        assert value.get("code") == "73211009"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"
        assert value.get("displayName") == "Diabetes"

    def test_observation_value_icd10(self):
        """Test FamilyHistoryObservation value with ICD-10 code."""
        obs = MockFamilyHistoryObservation(
            condition_name="Type 2 Diabetes",
            condition_code="E11",
            condition_code_system="ICD-10",
        )
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "E11"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.90"
        assert value.get("codeSystemName") == "ICD-10-CM"

    def test_observation_value_unknown_code_system(self):
        """Test FamilyHistoryObservation value with unknown code system."""
        obs = MockFamilyHistoryObservation(
            condition_name="Diabetes",
            condition_code="123",
            condition_code_system="CustomCodeSystem",
        )
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "123"
        # Should default to SNOMED OID
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"
        # Should use the provided code system name
        assert value.get("codeSystemName") == "CustomCodeSystem"

    def test_observation_age_at_onset(self):
        """Test FamilyHistoryObservation with age at onset."""
        obs = MockFamilyHistoryObservation(age_at_onset=45)
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        # Find age observation entryRelationship
        entry_rel = elem.find(f"{{{NS}}}entryRelationship[@typeCode='SUBJ']")
        assert entry_rel is not None
        assert entry_rel.get("inversionInd") == "true"

        # Check age observation
        age_obs = entry_rel.find(f"{{{NS}}}observation")
        assert age_obs is not None
        assert age_obs.get("classCode") == "OBS"
        assert age_obs.get("moodCode") == "EVN"

        # Check template ID
        template = age_obs.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.31"

        # Check code
        code = age_obs.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "445518008"

        # Check status
        status = age_obs.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

        # Check value
        value = age_obs.find(f"{{{NS}}}value")
        assert value is not None
        xsi_type = value.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        assert xsi_type == "PQ"
        assert value.get("value") == "45"
        assert value.get("unit") == "a"

    def test_observation_no_age_at_onset(self):
        """Test FamilyHistoryObservation without age at onset."""
        obs = MockFamilyHistoryObservation(age_at_onset=None)
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        entry_rel = elem.find(f"{{{NS}}}entryRelationship[@typeCode='SUBJ']")
        assert entry_rel is None

    def test_observation_death_with_cause(self):
        """Test FamilyHistoryObservation with death observation and cause."""
        obs = MockFamilyHistoryObservation(
            deceased_age=70,
            deceased_cause_code="22298006",
            deceased_cause_display_name="Myocardial infarction",
        )
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        # Find death observation entryRelationship
        entry_rel = elem.find(f"{{{NS}}}entryRelationship[@typeCode='CAUS']")
        assert entry_rel is not None

        # Check death observation
        death_obs = entry_rel.find(f"{{{NS}}}observation")
        assert death_obs is not None

        # Check template ID
        template = death_obs.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.47"

        # Check code
        code = death_obs.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "ASSERTION"

        # Check value with cause
        value = death_obs.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "22298006"
        assert value.get("displayName") == "Myocardial infarction"

        # Check age at death entryRelationship
        age_entry_rel = death_obs.find(f"{{{NS}}}entryRelationship[@typeCode='SUBJ']")
        assert age_entry_rel is not None

        age_obs = age_entry_rel.find(f"{{{NS}}}observation")
        assert age_obs is not None

        age_value = age_obs.find(f"{{{NS}}}value")
        assert age_value is not None
        assert age_value.get("value") == "70"
        assert age_value.get("unit") == "a"

    def test_observation_death_without_cause(self):
        """Test FamilyHistoryObservation with death observation but no cause."""
        obs = MockFamilyHistoryObservation(
            deceased_age=70,
            deceased_cause_code=None,
        )
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        # Find death observation
        entry_rel = elem.find(f"{{{NS}}}entryRelationship[@typeCode='CAUS']")
        assert entry_rel is not None

        death_obs = entry_rel.find(f"{{{NS}}}observation")
        assert death_obs is not None

        # Should not have value element when no cause
        value = death_obs.find(f"{{{NS}}}value")
        assert value is None

    def test_observation_no_death(self):
        """Test FamilyHistoryObservation without death observation."""
        obs = MockFamilyHistoryObservation(
            deceased_age=None,
            deceased_cause_code=None,
        )
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        entry_rel = elem.find(f"{{{NS}}}entryRelationship[@typeCode='CAUS']")
        assert entry_rel is None

    def test_observation_complete(self):
        """Test FamilyHistoryObservation with all optional elements."""
        persistent_id = MockPersistentID()
        obs = MockFamilyHistoryObservation(
            condition_name="Diabetes",
            condition_code="73211009",
            condition_code_system="SNOMED",
            effective_time=date(2020, 5, 15),
            age_at_onset=45,
            deceased_age=70,
            deceased_cause_code="22298006",
            deceased_cause_display_name="Myocardial infarction",
            persistent_id=persistent_id,
        )
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        # Verify all elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}value") is not None

        # Check both entryRelationships
        entry_rels = elem.findall(f"{{{NS}}}entryRelationship")
        assert len(entry_rels) == 2  # age at onset + death

    def test_observation_minimal(self):
        """Test FamilyHistoryObservation with minimal required elements."""
        obs = MockFamilyHistoryObservation(
            condition_name="Diabetes",
            condition_code="73211009",
            condition_code_system="SNOMED",
            effective_time=None,
            age_at_onset=None,
            deceased_age=None,
        )
        builder = FamilyHistoryObservation(obs)
        elem = builder.to_element()

        # Verify required elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}value") is not None

        # Verify optional elements are absent
        assert elem.find(f"{{{NS}}}effectiveTime") is None
        assert len(elem.findall(f"{{{NS}}}entryRelationship")) == 0


class TestFamilyHistoryOrganizer:
    """Tests for FamilyHistoryOrganizer builder."""

    def test_organizer_basic(self):
        """Test basic FamilyHistoryOrganizer creation."""
        obs = MockFamilyHistoryObservation()
        member = MockFamilyMemberHistory(observations=[obs])
        organizer = FamilyHistoryOrganizer(member)
        elem = organizer.to_element()

        assert local_name(elem) == "organizer"
        assert elem.get("classCode") == "CLUSTER"
        assert elem.get("moodCode") == "EVN"

    def test_organizer_has_template_id_r21(self):
        """Test FamilyHistoryOrganizer includes R2.1 template ID."""
        obs = MockFamilyHistoryObservation()
        member = MockFamilyMemberHistory(observations=[obs])
        organizer = FamilyHistoryOrganizer(member, version=CDAVersion.R2_1)
        elem = organizer.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.45"
        assert template.get("extension") == "2015-08-01"

    def test_organizer_has_id(self):
        """Test FamilyHistoryOrganizer has ID element."""
        obs = MockFamilyHistoryObservation()
        member = MockFamilyMemberHistory(observations=[obs])
        organizer = FamilyHistoryOrganizer(member)
        elem = organizer.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_organizer_has_persistent_id(self):
        """Test FamilyHistoryOrganizer with persistent ID."""
        persistent_id = MockPersistentID(
            root="2.16.840.1.113883.19",
            extension="org-456",
        )
        obs = MockFamilyHistoryObservation()
        member = MockFamilyMemberHistory(observations=[obs], persistent_id=persistent_id)
        organizer = FamilyHistoryOrganizer(member)
        elem = organizer.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.19"
        assert id_elem.get("extension") == "org-456"

    def test_organizer_has_status_code(self):
        """Test FamilyHistoryOrganizer has statusCode=completed."""
        obs = MockFamilyHistoryObservation()
        member = MockFamilyMemberHistory(observations=[obs])
        organizer = FamilyHistoryOrganizer(member)
        elem = organizer.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_organizer_subject_relationship(self):
        """Test FamilyHistoryOrganizer subject with relationship."""
        obs = MockFamilyHistoryObservation()
        member = MockFamilyMemberHistory(
            relationship_code="FTH",
            relationship_display_name="Father",
            observations=[obs],
        )
        organizer = FamilyHistoryOrganizer(member)
        elem = organizer.to_element()

        subject = elem.find(f"{{{NS}}}subject")
        assert subject is not None

        related_subject = subject.find(f"{{{NS}}}relatedSubject")
        assert related_subject is not None
        assert related_subject.get("classCode") == "PRS"

        # Check relationship code
        code = related_subject.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "FTH"
        assert code.get("codeSystem") == "2.16.840.1.113883.5.111"
        assert code.get("displayName") == "Father"

    def test_organizer_subject_with_details(self):
        """Test FamilyHistoryOrganizer subject with detailed information."""
        subject_data = MockFamilyMemberSubject(
            administrative_gender_code="M",
            birth_time=date(1950, 5, 15),
            deceased_ind=True,
            deceased_time=date(2020, 10, 1),
        )
        obs = MockFamilyHistoryObservation()
        member = MockFamilyMemberHistory(
            relationship_code="FTH",
            relationship_display_name="Father",
            subject=subject_data,
            observations=[obs],
        )
        organizer = FamilyHistoryOrganizer(member)
        elem = organizer.to_element()

        subject = elem.find(f"{{{NS}}}subject")
        related_subject = subject.find(f"{{{NS}}}relatedSubject")
        subject_elem = related_subject.find(f"{{{NS}}}subject")

        assert subject_elem is not None

        # Check gender
        gender = subject_elem.find(f"{{{NS}}}administrativeGenderCode")
        assert gender is not None
        assert gender.get("code") == "M"
        assert gender.get("codeSystem") == "2.16.840.1.113883.5.1"

        # Check birth time
        birth_time = subject_elem.find(f"{{{NS}}}birthTime")
        assert birth_time is not None
        assert birth_time.get("value") == "19500515"

        # Check deceased indicator (SDTC extension)
        deceased_ind = subject_elem.find(f"{{{SDTC_NS}}}deceasedInd")
        assert deceased_ind is not None
        assert deceased_ind.get("value") == "true"

        # Check deceased time (SDTC extension)
        deceased_time = subject_elem.find(f"{{{SDTC_NS}}}deceasedTime")
        assert deceased_time is not None
        assert deceased_time.get("value") == "20201001"

    def test_organizer_subject_deceased_false(self):
        """Test FamilyHistoryOrganizer subject with deceased_ind=false."""
        subject_data = MockFamilyMemberSubject(deceased_ind=False)
        obs = MockFamilyHistoryObservation()
        member = MockFamilyMemberHistory(
            subject=subject_data,
            observations=[obs],
        )
        organizer = FamilyHistoryOrganizer(member)
        elem = organizer.to_element()

        subject = elem.find(f"{{{NS}}}subject")
        related_subject = subject.find(f"{{{NS}}}relatedSubject")
        subject_elem = related_subject.find(f"{{{NS}}}subject")

        deceased_ind = subject_elem.find(f"{{{SDTC_NS}}}deceasedInd")
        assert deceased_ind is not None
        assert deceased_ind.get("value") == "false"

    def test_organizer_subject_without_details(self):
        """Test FamilyHistoryOrganizer subject without detailed information."""
        obs = MockFamilyHistoryObservation()
        member = MockFamilyMemberHistory(
            subject=None,
            observations=[obs],
        )
        organizer = FamilyHistoryOrganizer(member)
        elem = organizer.to_element()

        subject = elem.find(f"{{{NS}}}subject")
        related_subject = subject.find(f"{{{NS}}}relatedSubject")
        subject_elem = related_subject.find(f"{{{NS}}}subject")

        assert subject_elem is None

    def test_organizer_with_multiple_observations(self):
        """Test FamilyHistoryOrganizer with multiple observations."""
        obs1 = MockFamilyHistoryObservation(
            condition_name="Diabetes",
            condition_code="73211009",
        )
        obs2 = MockFamilyHistoryObservation(
            condition_name="Hypertension",
            condition_code="38341003",
        )
        member = MockFamilyMemberHistory(observations=[obs1, obs2])
        organizer = FamilyHistoryOrganizer(member)
        elem = organizer.to_element()

        components = elem.findall(f"{{{NS}}}component")
        assert len(components) == 2

        # Check first component
        obs_elem1 = components[0].find(f"{{{NS}}}observation")
        assert obs_elem1 is not None
        value1 = obs_elem1.find(f"{{{NS}}}value")
        assert value1.get("code") == "73211009"

        # Check second component
        obs_elem2 = components[1].find(f"{{{NS}}}observation")
        assert obs_elem2 is not None
        value2 = obs_elem2.find(f"{{{NS}}}value")
        assert value2.get("code") == "38341003"

    def test_organizer_component_contains_observation(self):
        """Test FamilyHistoryOrganizer component contains FamilyHistoryObservation."""
        obs = MockFamilyHistoryObservation(condition_name="Diabetes")
        member = MockFamilyMemberHistory(observations=[obs])
        organizer = FamilyHistoryOrganizer(member)
        elem = organizer.to_element()

        component = elem.find(f"{{{NS}}}component")
        assert component is not None

        observation = component.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"
        assert observation.get("moodCode") == "EVN"

    def test_organizer_complete(self):
        """Test FamilyHistoryOrganizer with all optional elements."""
        persistent_id = MockPersistentID()
        subject_data = MockFamilyMemberSubject(
            administrative_gender_code="M",
            birth_time=date(1950, 5, 15),
            deceased_ind=True,
            deceased_time=date(2020, 10, 1),
        )
        obs1 = MockFamilyHistoryObservation(
            condition_name="Diabetes",
            condition_code="73211009",
            age_at_onset=45,
        )
        obs2 = MockFamilyHistoryObservation(
            condition_name="Heart Disease",
            condition_code="56265001",
            deceased_age=70,
            deceased_cause_code="22298006",
        )
        member = MockFamilyMemberHistory(
            relationship_code="FTH",
            relationship_display_name="Father",
            subject=subject_data,
            observations=[obs1, obs2],
            persistent_id=persistent_id,
        )
        organizer = FamilyHistoryOrganizer(member)
        elem = organizer.to_element()

        # Verify all elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}subject") is not None

        # Verify subject details
        subject = elem.find(f"{{{NS}}}subject")
        related_subject = subject.find(f"{{{NS}}}relatedSubject")
        subject_elem = related_subject.find(f"{{{NS}}}subject")
        assert subject_elem is not None

        # Verify components
        components = elem.findall(f"{{{NS}}}component")
        assert len(components) == 2

    def test_organizer_minimal(self):
        """Test FamilyHistoryOrganizer with minimal required elements."""
        obs = MockFamilyHistoryObservation(
            condition_name="Diabetes",
            condition_code="73211009",
            condition_code_system="SNOMED",
        )
        member = MockFamilyMemberHistory(
            relationship_code="MTH",
            relationship_display_name="Mother",
            subject=None,
            observations=[obs],
        )
        organizer = FamilyHistoryOrganizer(member)
        elem = organizer.to_element()

        # Verify required elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}subject") is not None
        assert len(elem.findall(f"{{{NS}}}component")) == 1

        # Verify subject details are absent
        subject = elem.find(f"{{{NS}}}subject")
        related_subject = subject.find(f"{{{NS}}}relatedSubject")
        subject_elem = related_subject.find(f"{{{NS}}}subject")
        assert subject_elem is None

    def test_organizer_to_string(self):
        """Test FamilyHistoryOrganizer serialization."""
        obs = MockFamilyHistoryObservation()
        member = MockFamilyMemberHistory(observations=[obs])
        organizer = FamilyHistoryOrganizer(member)
        xml = organizer.to_string(pretty=False)

        assert "<organizer" in xml or ":organizer" in xml
        assert "classCode" in xml
        assert "CLUSTER" in xml

    def test_organizer_element_order(self):
        """Test that elements are in correct order."""
        subject_data = MockFamilyMemberSubject()
        obs = MockFamilyHistoryObservation()
        member = MockFamilyMemberHistory(
            subject=subject_data,
            observations=[obs],
        )
        organizer = FamilyHistoryOrganizer(member)
        elem = organizer.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "id" in names
        assert "statusCode" in names
        assert "subject" in names
        assert "component" in names
