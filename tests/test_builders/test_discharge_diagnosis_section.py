"""Tests for DischargeDiagnosisSection builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.discharge_diagnosis import DischargeDiagnosisSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockDischargeDiagnosis:
    """Mock discharge diagnosis for testing."""

    def __init__(
        self,
        name="Acute Myocardial Infarction",
        code="57054005",
        code_system="SNOMED CT",
        diagnosis_date=date(2024, 10, 15),
        resolved_date=None,
        status="active",
        discharge_disposition=None,
        priority=None,
        persistent_id=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._diagnosis_date = diagnosis_date
        self._resolved_date = resolved_date
        self._status = status
        self._discharge_disposition = discharge_disposition
        self._priority = priority
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
        """Alias for diagnosis_date to satisfy ProblemProtocol."""
        return self._diagnosis_date

    @property
    def resolved_date(self):
        return self._resolved_date

    @property
    def status(self):
        return self._status

    @property
    def discharge_disposition(self):
        return self._discharge_disposition

    @property
    def priority(self):
        return self._priority

    @property
    def persistent_id(self):
        return self._persistent_id


class MockPersistentID:
    """Mock persistent ID for testing."""

    def __init__(self, root="2.16.840.1.113883.19", extension="test-123"):
        self._root = root
        self._extension = extension

    @property
    def root(self):
        return self._root

    @property
    def extension(self):
        return self._extension


class TestDischargeDiagnosisSection:
    """Tests for DischargeDiagnosisSection builder."""

    def test_section_basic(self):
        """Test basic DischargeDiagnosisSection creation."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_has_template_id_r21(self):
        """Test section includes R2.1 template ID (CONF:1198-7979, CONF:1198-10394, CONF:1198-32549)."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.24"
        assert template.get("extension") == "2015-08-01"

    def test_section_has_template_id_r20(self):
        """Test section includes R2.0 template ID."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.24"
        assert template.get("extension") == "2014-06-09"

    def test_section_has_code(self):
        """Test section includes correct code (CONF:1198-15355, CONF:1198-15356, CONF:1198-30861)."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "11535-2"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert code.get("displayName") == "Hospital Discharge Diagnosis"

    def test_section_code_has_translation(self):
        """Test section code includes translation (CONF:1198-32834, CONF:1198-32835, CONF:1198-32836)."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        translation = code.find(f"{{{NS}}}translation")
        assert translation is not None
        assert translation.get("code") == "78375-3"
        assert translation.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert translation.get("displayName") == "Discharge Diagnosis"

    def test_section_has_title(self):
        """Test section includes title (CONF:1198-7981)."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis], title="My Discharge Diagnoses")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Discharge Diagnoses"

    def test_section_default_title(self):
        """Test section uses default title."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Discharge Diagnosis"

    def test_section_has_narrative(self):
        """Test section includes narrative text (CONF:1198-7982)."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_narrative_table(self):
        """Test narrative includes HTML table."""
        diagnosis = MockDischargeDiagnosis(
            name="Acute Myocardial Infarction",
            code="57054005",
            code_system="SNOMED CT",
            diagnosis_date=date(2024, 10, 15),
            status="active",
        )
        section = DischargeDiagnosisSection([diagnosis])
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
        assert len(ths) == 4  # Diagnosis, Code, Status, Diagnosis Date

    def test_narrative_content(self):
        """Test narrative contains diagnosis data."""
        diagnosis = MockDischargeDiagnosis(
            name="Acute Myocardial Infarction",
            code="57054005",
            code_system="SNOMED CT",
            diagnosis_date=date(2024, 10, 15),
            status="active",
        )
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 4

        # Check diagnosis name with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Acute Myocardial Infarction"
        assert content.get("ID") == "discharge-diagnosis-1"

        # Check code
        assert tds[1].text == "57054005 (SNOMED CT)"

        # Check status
        assert tds[2].text == "Active"

        # Check diagnosis date
        assert tds[3].text == "2024-10-15"

    def test_narrative_without_diagnosis_date(self):
        """Test narrative shows 'Unknown' for missing diagnosis date."""
        diagnosis = MockDischargeDiagnosis(diagnosis_date=None)
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check diagnosis date shows "Unknown"
        assert tds[3].text == "Unknown"

    def test_narrative_multiple_diagnoses(self):
        """Test narrative with multiple discharge diagnoses."""
        diagnoses = [
            MockDischargeDiagnosis(
                name="Acute Myocardial Infarction", code="57054005"
            ),
            MockDischargeDiagnosis(name="Congestive Heart Failure", code="42343007"),
            MockDischargeDiagnosis(name="Acute Respiratory Failure", code="65710008"),
        ]
        section = DischargeDiagnosisSection(diagnoses)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        assert len(trs) == 3

        # Check IDs are sequential
        content1 = trs[0].find(f".//{{{NS}}}content")
        content2 = trs[1].find(f".//{{{NS}}}content")
        content3 = trs[2].find(f".//{{{NS}}}content")

        assert content1.get("ID") == "discharge-diagnosis-1"
        assert content2.get("ID") == "discharge-diagnosis-2"
        assert content3.get("ID") == "discharge-diagnosis-3"

    def test_narrative_empty(self):
        """Test narrative when no diagnoses."""
        section = DischargeDiagnosisSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No discharge diagnoses"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_section_has_entry(self):
        """Test section includes entry element (CONF:1198-7983)."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_section_no_entry_when_empty(self):
        """Test section has no entry when diagnoses list is empty."""
        section = DischargeDiagnosisSection([])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_entry_has_discharge_diagnosis_act(self):
        """Test entry contains Hospital Discharge Diagnosis act (CONF:1198-15489)."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"
        assert act.get("moodCode") == "EVN"

    def test_discharge_diagnosis_act_has_template_id(self):
        """Test Hospital Discharge Diagnosis act has correct template ID (CONF:1198-16764, CONF:1198-16765, CONF:1198-32534)."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis], version=CDAVersion.R2_1)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        template = act.find(f"{{{NS}}}templateId")

        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.33"
        assert template.get("extension") == "2015-08-01"

    def test_discharge_diagnosis_act_has_code(self):
        """Test Hospital Discharge Diagnosis act has correct code (CONF:1198-19147, CONF:1198-19148, CONF:1198-32163)."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        code = act.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "11535-2"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert code.get("displayName") == "Hospital discharge diagnosis"

    def test_discharge_diagnosis_act_has_entry_relationship(self):
        """Test Hospital Discharge Diagnosis act has entryRelationship (CONF:1198-7666, CONF:1198-7667)."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")

        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "SUBJ"

    def test_discharge_diagnosis_act_has_problem_observation(self):
        """Test entryRelationship contains Problem Observation (CONF:1198-15536)."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")

        assert observation is not None
        assert observation.get("classCode") == "OBS"
        assert observation.get("moodCode") == "EVN"

    def test_problem_observation_has_template_id(self):
        """Test Problem Observation has correct template ID."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis], version=CDAVersion.R2_1)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        template = observation.find(f"{{{NS}}}templateId")

        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.4"
        assert template.get("extension") == "2015-08-01"

    def test_problem_observation_has_code(self):
        """Test Problem Observation has problem type code."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "55607006"
        assert code.get("displayName") == "Problem"

    def test_problem_observation_has_value(self):
        """Test Problem Observation has value with diagnosis code."""
        diagnosis = MockDischargeDiagnosis(
            name="Acute Myocardial Infarction",
            code="57054005",
            code_system="SNOMED CT",
        )
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.get("code") == "57054005"
        assert value.get("displayName") == "Acute Myocardial Infarction"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"

    def test_multiple_diagnoses_in_single_act(self):
        """Test multiple diagnoses are included in single Hospital Discharge Diagnosis act."""
        diagnoses = [
            MockDischargeDiagnosis(
                name="Acute Myocardial Infarction", code="57054005"
            ),
            MockDischargeDiagnosis(name="Congestive Heart Failure", code="42343007"),
        ]
        section = DischargeDiagnosisSection(diagnoses)
        elem = section.to_element()

        # Should have single entry
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        # Entry should have single act
        entry = entries[0]
        act = entry.find(f"{{{NS}}}act")
        assert act is not None

        # Act should have multiple entryRelationships (one per diagnosis)
        entry_rels = act.findall(f"{{{NS}}}entryRelationship")
        assert len(entry_rels) == 2

        # Check each entryRelationship has an observation
        for entry_rel in entry_rels:
            observation = entry_rel.find(f"{{{NS}}}observation")
            assert observation is not None

    def test_section_with_persistent_id(self):
        """Test observation uses persistent ID when provided."""
        persistent_id = MockPersistentID(
            root="2.16.840.1.113883.19",
            extension="diagnosis-123",
        )
        diagnosis = MockDischargeDiagnosis(persistent_id=persistent_id)
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        id_elem = observation.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.19"
        assert id_elem.get("extension") == "diagnosis-123"

    def test_section_to_string(self):
        """Test section serialization."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "11535-2" in xml  # Section code
        assert "Discharge Diagnosis" in xml

    def test_section_structure_order(self):
        """Test that section elements are in correct order."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])
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

    def test_section_empty_diagnoses(self):
        """Test section with empty diagnosis list."""
        section = DischargeDiagnosisSection([])
        elem = section.to_element()

        # Should still have all required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Should not have any entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_observation_with_icd10_code(self):
        """Test observation with ICD-10 code."""
        diagnosis = MockDischargeDiagnosis(
            name="Acute myocardial infarction",
            code="I21.9",
            code_system="ICD-10",
        )
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.get("code") == "I21.9"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.90"

    def test_observation_resolved_diagnosis(self):
        """Test observation with resolved diagnosis."""
        diagnosis = MockDischargeDiagnosis(
            name="Pneumonia",
            status="resolved",
            diagnosis_date=date(2024, 10, 10),
            resolved_date=date(2024, 10, 20),
        )
        section = DischargeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        status = observation.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "completed"

        # Check effective time has high date
        eff_time = observation.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None
        high = eff_time.find(f"{{{NS}}}high")
        assert high is not None
        assert high.get("value") == "20241020"


class TestDischargeDiagnosisSectionIntegration:
    """Integration tests for DischargeDiagnosisSection."""

    def test_complete_section(self):
        """Test creating a complete discharge diagnosis section."""
        diagnoses = [
            MockDischargeDiagnosis(
                name="Acute Myocardial Infarction",
                code="57054005",
                code_system="SNOMED CT",
                diagnosis_date=date(2024, 10, 15),
                status="active",
            ),
            MockDischargeDiagnosis(
                name="Congestive Heart Failure",
                code="42343007",
                code_system="SNOMED CT",
                diagnosis_date=date(2024, 10, 15),
                status="active",
            ),
            MockDischargeDiagnosis(
                name="Acute Respiratory Failure",
                code="65710008",
                code_system="SNOMED CT",
                diagnosis_date=date(2024, 10, 15),
                status="active",
            ),
        ]

        section = DischargeDiagnosisSection(
            diagnoses,
            title="Hospital Discharge Diagnoses",
        )
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify narrative table has 3 rows
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 3

        # Verify single entry with multiple observations
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        entry = entries[0]
        act = entry.find(f"{{{NS}}}act")
        entry_rels = act.findall(f"{{{NS}}}entryRelationship")
        assert len(entry_rels) == 3

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_with_various_code_systems(self):
        """Test section with diagnoses from different code systems."""
        diagnoses = [
            MockDischargeDiagnosis(
                name="Acute Myocardial Infarction",
                code="57054005",
                code_system="SNOMED CT",
            ),
            MockDischargeDiagnosis(
                name="Acute myocardial infarction",
                code="I21.9",
                code_system="ICD-10",
            ),
        ]

        section = DischargeDiagnosisSection(diagnoses)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rels = act.findall(f"{{{NS}}}entryRelationship")
        assert len(entry_rels) == 2

        # Check first diagnosis (SNOMED)
        obs1 = entry_rels[0].find(f"{{{NS}}}observation")
        value1 = obs1.find(f"{{{NS}}}value")
        assert value1.get("codeSystem") == "2.16.840.1.113883.6.96"

        # Check second diagnosis (ICD-10)
        obs2 = entry_rels[1].find(f"{{{NS}}}observation")
        value2 = obs2.find(f"{{{NS}}}value")
        assert value2.get("codeSystem") == "2.16.840.1.113883.6.90"

    def test_section_r20_version(self):
        """Test section with R2.0 version."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis], version=CDAVersion.R2_0)
        elem = section.to_element()

        # Check section template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.24"
        assert template.get("extension") == "2014-06-09"

        # Check act template ID
        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        act_template = act.find(f"{{{NS}}}templateId")
        assert act_template.get("extension") == "2014-06-09"

        # Check observation template ID
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        obs_template = observation.find(f"{{{NS}}}templateId")
        assert obs_template.get("extension") == "2014-06-09"

    def test_section_r21_version(self):
        """Test section with R2.1 version."""
        diagnosis = MockDischargeDiagnosis()
        section = DischargeDiagnosisSection([diagnosis], version=CDAVersion.R2_1)
        elem = section.to_element()

        # Check section template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.24"
        assert template.get("extension") == "2015-08-01"

        # Check act template ID
        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        act_template = act.find(f"{{{NS}}}templateId")
        assert act_template.get("extension") == "2015-08-01"

        # Check observation template ID
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        obs_template = observation.find(f"{{{NS}}}templateId")
        assert obs_template.get("extension") == "2015-08-01"

    def test_section_with_mixed_statuses(self):
        """Test section with active and resolved diagnoses."""
        diagnoses = [
            MockDischargeDiagnosis(
                name="Acute Myocardial Infarction",
                code="57054005",
                status="active",
                diagnosis_date=date(2024, 10, 15),
            ),
            MockDischargeDiagnosis(
                name="Pneumonia",
                code="233604007",
                status="resolved",
                diagnosis_date=date(2024, 10, 10),
                resolved_date=date(2024, 10, 20),
            ),
        ]

        section = DischargeDiagnosisSection(diagnoses)
        elem = section.to_element()

        # Verify narrative shows correct statuses
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        # First diagnosis should be Active
        tds1 = trs[0].findall(f"{{{NS}}}td")
        assert tds1[2].text == "Active"

        # Second diagnosis should be Resolved
        tds2 = trs[1].findall(f"{{{NS}}}td")
        assert tds2[2].text == "Resolved"

        # Verify observations have correct status codes
        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rels = act.findall(f"{{{NS}}}entryRelationship")

        obs1 = entry_rels[0].find(f"{{{NS}}}observation")
        status1 = obs1.find(f"{{{NS}}}statusCode")
        assert status1.get("code") == "active"

        obs2 = entry_rels[1].find(f"{{{NS}}}observation")
        status2 = obs2.find(f"{{{NS}}}statusCode")
        assert status2.get("code") == "completed"
