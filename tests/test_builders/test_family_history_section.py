"""Tests for FamilyHistorySection builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.family_history import FamilyHistorySection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"
# SDTC namespace
SDTC_NS = "urn:hl7-org:sdtc"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockFamilyMemberSubject:
    """Mock family member subject for testing."""

    def __init__(
        self,
        administrative_gender_code=None,
        birth_time=None,
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
        condition_name="Diabetes Mellitus",
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


class TestFamilyHistorySection:
    """Tests for FamilyHistorySection builder."""

    def test_family_history_section_basic(self):
        """Test basic FamilyHistorySection creation."""
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_family_history_section_has_template_id_r21(self):
        """Test FamilyHistorySection includes R2.1 template ID."""
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.15"
        assert template.get("extension") == "2015-08-01"

    def test_family_history_section_has_template_id_r20(self):
        """Test FamilyHistorySection includes R2.0 template ID."""
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.15"
        assert template.get("extension") == "2015-08-01"

    def test_family_history_section_has_code(self):
        """Test FamilyHistorySection includes section code."""
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "10157-6"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Family History"

    def test_family_history_section_has_title(self):
        """Test FamilyHistorySection includes title."""
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member], title="My Family History")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Family History"

    def test_family_history_section_default_title(self):
        """Test FamilyHistorySection uses default title."""
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Family History"

    def test_family_history_section_has_narrative(self):
        """Test FamilyHistorySection includes narrative text."""
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_family_history_section_narrative_table(self):
        """Test narrative includes HTML table."""
        observation = MockFamilyHistoryObservation(
            condition_name="Diabetes",
            age_at_onset=45,
        )
        family_member = MockFamilyMemberHistory(
            relationship_code="FTH",
            relationship_display_name="Father",
            observations=[observation],
        )
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        assert table is not None
        assert table.get("border") == "1"

        # Check table header
        thead = table.find(f"{{{NS}}}thead")
        assert thead is not None
        tr = thead.find(f"{{{NS}}}tr")
        ths = tr.findall(f"{{{NS}}}th")
        assert len(ths) == 6  # Family Member, Gender, Relationship, Condition, Age at Onset, Status

    def test_family_history_section_narrative_content(self):
        """Test narrative contains family history data."""
        subject = MockFamilyMemberSubject(
            administrative_gender_code="M",
            birth_time=date(1950, 1, 1),
        )
        observation = MockFamilyHistoryObservation(
            condition_name="Coronary Artery Disease",
            age_at_onset=55,
        )
        family_member = MockFamilyMemberHistory(
            relationship_code="FTH",
            relationship_display_name="Father",
            subject=subject,
            observations=[observation],
        )
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 6

        # Check family member with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Family Member 1"
        assert content.get("ID") == "family-member-1"

        # Check gender
        assert tds[1].text == "Male"

        # Check relationship
        assert tds[2].text == "Father"

        # Check condition
        assert tds[3].text == "Coronary Artery Disease"

        # Check age at onset
        assert tds[4].text == "55 years"

        # Check status
        assert tds[5].text == "Living"

    def test_family_history_section_narrative_deceased_member(self):
        """Test narrative shows deceased status."""
        subject = MockFamilyMemberSubject(
            administrative_gender_code="F",
            deceased_ind=True,
            deceased_time=date(2010, 5, 15),
        )
        observation = MockFamilyHistoryObservation(
            condition_name="Breast Cancer",
        )
        family_member = MockFamilyMemberHistory(
            relationship_code="MTH",
            relationship_display_name="Mother",
            subject=subject,
            observations=[observation],
        )
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check status shows deceased with date
        assert "Deceased" in tds[5].text
        assert "2010-05-15" in tds[5].text

    def test_family_history_section_narrative_multiple_observations(self):
        """Test narrative with multiple observations for one family member."""
        observation1 = MockFamilyHistoryObservation(
            condition_name="Diabetes",
            age_at_onset=45,
        )
        observation2 = MockFamilyHistoryObservation(
            condition_name="Hypertension",
            age_at_onset=50,
        )
        family_member = MockFamilyMemberHistory(
            relationship_code="FTH",
            relationship_display_name="Father",
            observations=[observation1, observation2],
        )
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        # Should have 2 rows for 2 observations
        assert len(trs) == 2

        # First row should have family member info
        tds1 = trs[0].findall(f"{{{NS}}}td")
        assert tds1[2].text == "Father"  # Relationship
        assert tds1[3].text == "Diabetes"  # Condition

        # Second row should have empty family member/relationship cells
        tds2 = trs[1].findall(f"{{{NS}}}td")
        assert tds2[0].text == ""  # Family member
        assert tds2[2].text == ""  # Relationship
        assert tds2[3].text == "Hypertension"  # Condition

    def test_family_history_section_narrative_multiple_family_members(self):
        """Test narrative with multiple family members."""
        obs1 = MockFamilyHistoryObservation(condition_name="Diabetes")
        obs2 = MockFamilyHistoryObservation(condition_name="Breast Cancer")

        family_members = [
            MockFamilyMemberHistory(
                relationship_code="FTH",
                relationship_display_name="Father",
                observations=[obs1],
            ),
            MockFamilyMemberHistory(
                relationship_code="MTH",
                relationship_display_name="Mother",
                observations=[obs2],
            ),
        ]
        section = FamilyHistorySection(family_members)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        assert len(trs) == 2

        # Check IDs are sequential
        content1 = trs[0].find(f".//{{{NS}}}content")
        content2 = trs[1].find(f".//{{{NS}}}content")

        assert content1.get("ID") == "family-member-1"
        assert content2.get("ID") == "family-member-2"

    def test_family_history_section_empty_narrative(self):
        """Test narrative when no family history."""
        section = FamilyHistorySection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No known family history"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_family_history_section_has_entries(self):
        """Test FamilyHistorySection includes entry elements."""
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_family_history_section_entry_has_organizer(self):
        """Test entry contains Family History Organizer element."""
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        organizer = entry.find(f"{{{NS}}}organizer")
        assert organizer is not None
        assert organizer.get("classCode") == "CLUSTER"
        assert organizer.get("moodCode") == "EVN"

        # Check template ID
        template = organizer.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.45"
        assert template.get("extension") == "2015-08-01"

    def test_family_history_section_organizer_has_subject(self):
        """Test organizer contains subject with relationship."""
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(
            relationship_code="FTH",
            relationship_display_name="Father",
            observations=[observation],
        )
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        organizer = entry.find(f"{{{NS}}}organizer")
        subject = organizer.find(f"{{{NS}}}subject")
        assert subject is not None

        related_subject = subject.find(f"{{{NS}}}relatedSubject")
        assert related_subject is not None
        assert related_subject.get("classCode") == "PRS"

        # Check relationship code
        code = related_subject.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "FTH"
        assert code.get("displayName") == "Father"

    def test_family_history_section_organizer_subject_with_details(self):
        """Test organizer subject includes gender and birth time."""
        subject = MockFamilyMemberSubject(
            administrative_gender_code="M",
            birth_time=date(1950, 1, 1),
        )
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(
            subject=subject,
            observations=[observation],
        )
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        organizer = entry.find(f"{{{NS}}}organizer")
        related_subject = organizer.find(f".//{{{NS}}}relatedSubject")
        subject_elem = related_subject.find(f"{{{NS}}}subject")

        assert subject_elem is not None

        # Check gender
        gender = subject_elem.find(f"{{{NS}}}administrativeGenderCode")
        assert gender is not None
        assert gender.get("code") == "M"

        # Check birth time
        birth_time = subject_elem.find(f"{{{NS}}}birthTime")
        assert birth_time is not None
        assert birth_time.get("value") == "19500101"

    def test_family_history_section_organizer_subject_deceased(self):
        """Test organizer subject includes deceased information."""
        subject = MockFamilyMemberSubject(
            deceased_ind=True,
            deceased_time=date(2010, 5, 15),
        )
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(
            subject=subject,
            observations=[observation],
        )
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        organizer = entry.find(f"{{{NS}}}organizer")
        related_subject = organizer.find(f".//{{{NS}}}relatedSubject")
        subject_elem = related_subject.find(f"{{{NS}}}subject")

        # Check deceased indicator (SDTC extension)
        deceased_ind = subject_elem.find(f"{{{SDTC_NS}}}deceasedInd")
        assert deceased_ind is not None
        assert deceased_ind.get("value") == "true"

        # Check deceased time (SDTC extension)
        deceased_time = subject_elem.find(f"{{{SDTC_NS}}}deceasedTime")
        assert deceased_time is not None
        assert deceased_time.get("value") == "20100515"

    def test_family_history_section_organizer_has_component(self):
        """Test organizer contains component with observation."""
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        organizer = entry.find(f"{{{NS}}}organizer")
        component = organizer.find(f"{{{NS}}}component")
        assert component is not None

        obs_elem = component.find(f"{{{NS}}}observation")
        assert obs_elem is not None
        assert obs_elem.get("classCode") == "OBS"
        assert obs_elem.get("moodCode") == "EVN"

    def test_family_history_section_observation_has_code(self):
        """Test observation includes type code."""
        observation = MockFamilyHistoryObservation(
            observation_type_code="64572001",
            observation_type_display_name="Disease",
        )
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        obs_elem = elem.find(f".//{{{NS}}}observation[@classCode='OBS']")
        code = obs_elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "64572001"
        assert code.get("displayName") == "Disease"

        # Check for LOINC translation
        translation = code.find(f"{{{NS}}}translation")
        assert translation is not None
        assert translation.get("code") == "75315-2"

    def test_family_history_section_observation_has_value(self):
        """Test observation includes condition value."""
        observation = MockFamilyHistoryObservation(
            condition_name="Diabetes Mellitus",
            condition_code="73211009",
            condition_code_system="SNOMED",
        )
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        obs_elem = elem.find(f".//{{{NS}}}observation[@classCode='OBS']")
        value = obs_elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "73211009"
        assert value.get("displayName") == "Diabetes Mellitus"
        assert value.get("codeSystemName") == "SNOMED CT"

    def test_family_history_section_observation_with_age(self):
        """Test observation includes age at onset."""
        observation = MockFamilyHistoryObservation(
            condition_name="Hypertension",
            age_at_onset=45,
        )
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        # Find the age observation
        age_entry_rel = elem.find(
            f".//{{{NS}}}entryRelationship[@typeCode='SUBJ'][@inversionInd='true']"
        )
        assert age_entry_rel is not None

        age_obs = age_entry_rel.find(f"{{{NS}}}observation")
        assert age_obs is not None

        # Check template ID
        template = age_obs.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.31"

        # Check value
        value = age_obs.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("value") == "45"
        assert value.get("unit") == "a"

    def test_family_history_section_observation_with_death(self):
        """Test observation includes death information."""
        observation = MockFamilyHistoryObservation(
            condition_name="Heart Disease",
            deceased_age=65,
            deceased_cause_code="22298006",
            deceased_cause_display_name="Myocardial infarction",
        )
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        # Find the death observation
        death_entry_rel = elem.find(f".//{{{NS}}}entryRelationship[@typeCode='CAUS']")
        assert death_entry_rel is not None

        death_obs = death_entry_rel.find(f"{{{NS}}}observation")
        assert death_obs is not None

        # Check template ID
        template = death_obs.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.47"

        # Check cause value
        value = death_obs.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "22298006"
        assert value.get("displayName") == "Myocardial infarction"

    def test_family_history_section_observation_effective_time(self):
        """Test observation includes effective time."""
        observation = MockFamilyHistoryObservation(
            condition_name="Cancer",
            effective_time=date(2015, 3, 10),
        )
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        obs_elem = elem.find(f".//{{{NS}}}observation[@classCode='OBS']")
        eff_time = obs_elem.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None
        assert eff_time.get("value") == "20150310"

    def test_family_history_section_multiple_entries(self):
        """Test FamilyHistorySection with multiple family members."""
        obs1 = MockFamilyHistoryObservation(condition_name="Diabetes")
        obs2 = MockFamilyHistoryObservation(condition_name="Cancer")

        family_members = [
            MockFamilyMemberHistory(
                relationship_code="FTH",
                relationship_display_name="Father",
                observations=[obs1],
            ),
            MockFamilyMemberHistory(
                relationship_code="MTH",
                relationship_display_name="Mother",
                observations=[obs2],
            ),
        ]
        section = FamilyHistorySection(family_members)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an organizer
        for entry in entries:
            organizer = entry.find(f"{{{NS}}}organizer")
            assert organizer is not None

    def test_family_history_section_to_string(self):
        """Test FamilyHistorySection serialization."""
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "10157-6" in xml  # Section code
        assert "Family History" in xml

    def test_family_history_section_structure_order(self):
        """Test that section elements are in correct order."""
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "code" in names
        assert "title" in names
        assert "text" in names
        assert "entry" in names

        # templateId should come before code
        assert names.index("templateId") < names.index("code")
        # code should come before title
        assert names.index("code") < names.index("title")
        # title should come before text
        assert names.index("title") < names.index("text")
        # text should come before entry
        assert names.index("text") < names.index("entry")

    def test_family_history_section_icd10_code_system(self):
        """Test observation with ICD-10 code system."""
        observation = MockFamilyHistoryObservation(
            condition_name="Type 2 Diabetes",
            condition_code="E11",
            condition_code_system="ICD-10",
        )
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        obs_elem = elem.find(f".//{{{NS}}}observation[@classCode='OBS']")
        value = obs_elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "E11"
        assert value.get("codeSystemName") == "ICD-10-CM"

    def test_family_history_section_null_flavor_handling(self):
        """Test handling of missing optional data."""
        observation = MockFamilyHistoryObservation(
            condition_name="Unknown Condition",
            condition_code="64572001",
            condition_code_system="SNOMED",
            # No age_at_onset, no deceased info
        )
        family_member = MockFamilyMemberHistory(
            relationship_code="FTH",
            relationship_display_name="Father",
            subject=None,  # No subject details
            observations=[observation],
        )
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        # Should build without errors
        assert elem is not None

        # Check that age observation is not present
        age_entry_rel = elem.find(
            f".//{{{NS}}}entryRelationship[@typeCode='SUBJ'][@inversionInd='true']"
        )
        assert age_entry_rel is None

        # Check that death observation is not present
        death_entry_rel = elem.find(f".//{{{NS}}}entryRelationship[@typeCode='CAUS']")
        assert death_entry_rel is None


class TestFamilyHistorySectionIntegration:
    """Integration tests for FamilyHistorySection."""

    def test_complete_family_history_section(self):
        """Test creating a complete family history section."""
        father_subject = MockFamilyMemberSubject(
            administrative_gender_code="M",
            birth_time=date(1950, 1, 15),
            deceased_ind=True,
            deceased_time=date(2015, 6, 20),
        )
        father_obs1 = MockFamilyHistoryObservation(
            condition_name="Type 2 Diabetes Mellitus",
            condition_code="44054006",
            condition_code_system="SNOMED",
            age_at_onset=55,
        )
        father_obs2 = MockFamilyHistoryObservation(
            condition_name="Myocardial Infarction",
            condition_code="22298006",
            condition_code_system="SNOMED",
            age_at_onset=64,
            deceased_age=65,
            deceased_cause_code="22298006",
            deceased_cause_display_name="Myocardial infarction",
        )

        mother_subject = MockFamilyMemberSubject(
            administrative_gender_code="F",
            birth_time=date(1952, 8, 10),
        )
        mother_obs = MockFamilyHistoryObservation(
            condition_name="Breast Cancer",
            condition_code="254837009",
            condition_code_system="SNOMED",
            age_at_onset=58,
        )

        family_members = [
            MockFamilyMemberHistory(
                relationship_code="FTH",
                relationship_display_name="Father",
                subject=father_subject,
                observations=[father_obs1, father_obs2],
            ),
            MockFamilyMemberHistory(
                relationship_code="MTH",
                relationship_display_name="Mother",
                subject=mother_subject,
                observations=[mother_obs],
            ),
        ]

        section = FamilyHistorySection(
            family_members, title="Family Medical History"
        )
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify narrative table has 3 rows (2 for father, 1 for mother)
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 3

        # Verify 2 entries (one per family member)
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Verify father's organizer has 2 components
        father_organizer = entries[0].find(f"{{{NS}}}organizer")
        father_components = father_organizer.findall(f"{{{NS}}}component")
        assert len(father_components) == 2

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_empty_family_history_section(self):
        """Test section with no family members."""
        section = FamilyHistorySection([])
        elem = section.to_element()

        # Should have narrative saying no family history
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No known family history"

        # Should have no entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_family_member_with_no_observations(self):
        """Test family member with no observations."""
        family_member = MockFamilyMemberHistory(
            relationship_code="FTH",
            relationship_display_name="Father",
            observations=[],
        )
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        # Should build successfully
        assert elem is not None

        # Should have one entry
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        # Organizer should have no components
        organizer = entries[0].find(f"{{{NS}}}organizer")
        components = organizer.findall(f"{{{NS}}}component")
        assert len(components) == 0

    def test_female_gender_mapping(self):
        """Test female gender code mapping in narrative."""
        subject = MockFamilyMemberSubject(administrative_gender_code="F")
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(
            relationship_code="MTH",
            relationship_display_name="Mother",
            subject=subject,
            observations=[observation],
        )
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check gender shows "Female"
        assert tds[1].text == "Female"

    def test_unknown_gender_handling(self):
        """Test unknown gender code in narrative."""
        subject = MockFamilyMemberSubject(administrative_gender_code="UN")
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(
            subject=subject,
            observations=[observation],
        )
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check gender shows "Undifferentiated"
        assert tds[1].text == "Undifferentiated"

    def test_deceased_without_time(self):
        """Test deceased indicator without deceased time."""
        subject = MockFamilyMemberSubject(
            administrative_gender_code="M",
            deceased_ind=True,
            deceased_time=None,  # Deceased but no date
        )
        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(
            relationship_code="FTH",
            relationship_display_name="Father",
            subject=subject,
            observations=[observation],
        )
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check status shows "Deceased" without date
        assert tds[5].text == "Deceased"

    def test_persistent_id_in_observation(self):
        """Test observation with persistent ID."""

        class MockPersistentID:
            @property
            def root(self):
                return "2.16.840.1.113883.3.1234"

            @property
            def extension(self):
                return "obs-12345"

        observation = MockFamilyHistoryObservation(
            condition_name="Hypertension",
            persistent_id=MockPersistentID(),
        )
        family_member = MockFamilyMemberHistory(observations=[observation])
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        # Find the observation
        obs_elem = elem.find(f".//{{{NS}}}observation[@classCode='OBS']")
        id_elem = obs_elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.3.1234"
        assert id_elem.get("extension") == "obs-12345"

    def test_persistent_id_in_organizer(self):
        """Test organizer with persistent ID."""

        class MockPersistentID:
            @property
            def root(self):
                return "2.16.840.1.113883.3.5678"

            @property
            def extension(self):
                return "org-98765"

        observation = MockFamilyHistoryObservation()
        family_member = MockFamilyMemberHistory(
            observations=[observation],
            persistent_id=MockPersistentID(),
        )
        section = FamilyHistorySection([family_member])
        elem = section.to_element()

        # Find the organizer
        organizer = elem.find(f".//{{{NS}}}organizer")
        id_elem = organizer.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.3.5678"
        assert id_elem.get("extension") == "org-98765"
