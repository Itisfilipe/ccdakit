"""Tests for PreoperativeDiagnosisSection builder."""

from datetime import date

import pytest
from lxml import etree

from ccdakit.builders.sections.preoperative_diagnosis import (
    PreoperativeDiagnosisSection,
)
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockPreoperativeDiagnosis:
    """Mock preoperative diagnosis for testing."""

    def __init__(
        self,
        name="Acute Appendicitis",
        code="74400008",
        code_system="SNOMED",
        diagnosis_date=date(2024, 3, 15),
        status="active",
        persistent_id=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._diagnosis_date = diagnosis_date
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
    def status(self):
        return self._status

    @property
    def persistent_id(self):
        return self._persistent_id

    # ProblemProtocol compatibility (for ProblemObservation)
    @property
    def onset_date(self):
        return self._diagnosis_date

    @property
    def resolved_date(self):
        return None


class MockPersistentID:
    """Mock persistent ID for testing."""

    def __init__(self, root="2.16.840.1.113883.19", extension="preop-diag-123"):
        self._root = root
        self._extension = extension

    @property
    def root(self):
        return self._root

    @property
    def extension(self):
        return self._extension


class TestPreoperativeDiagnosisSection:
    """Tests for PreoperativeDiagnosisSection builder."""

    def test_section_basic(self):
        """Test basic PreoperativeDiagnosisSection creation."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_has_template_id_r21(self):
        """Test section includes R2.1 template ID (CONF:1198-8097, CONF:1198-10439, CONF:1198-32551)."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.34"
        assert template.get("extension") == "2015-08-01"

    def test_section_has_code(self):
        """Test section includes correct code (CONF:1198-15405, CONF:1198-15406, CONF:1198-30863)."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "10219-4"  # Preoperative Diagnosis
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Preoperative Diagnosis"

    def test_section_has_title(self):
        """Test section includes title (CONF:1198-8099)."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection(
            [diagnosis], title="Surgical Preoperative Diagnosis"
        )
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Surgical Preoperative Diagnosis"

    def test_section_default_title(self):
        """Test section uses default title."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Preoperative Diagnosis"

    def test_section_has_narrative(self):
        """Test section includes narrative text (CONF:1198-8100)."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_narrative_table(self):
        """Test narrative includes HTML table."""
        diagnosis = MockPreoperativeDiagnosis(
            name="Cholelithiasis",
            code="235919008",
            code_system="SNOMED",
            diagnosis_date=date(2024, 2, 20),
            status="active",
        )
        section = PreoperativeDiagnosisSection([diagnosis])
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
        diagnosis = MockPreoperativeDiagnosis(
            name="Acute Appendicitis",
            code="74400008",
            code_system="SNOMED",
            diagnosis_date=date(2024, 3, 15),
            status="active",
        )
        section = PreoperativeDiagnosisSection([diagnosis])
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
        assert content.text == "Acute Appendicitis"
        assert content.get("ID") == "preop-diagnosis-1"

        # Check code
        assert tds[1].text == "74400008 (SNOMED)"

        # Check status
        assert tds[2].text == "Active"

        # Check diagnosis date
        assert tds[3].text == "2024-03-15"

    def test_narrative_without_diagnosis_date(self):
        """Test that R2.1 raises ValueError when diagnosis_date is None.

        R2.1 requires onset_date (diagnosis_date) per C-CDA specification.
        """
        diagnosis = MockPreoperativeDiagnosis(diagnosis_date=None)
        section = PreoperativeDiagnosisSection([diagnosis])

        with pytest.raises(ValueError, match="onset date"):
            section.to_element()

    def test_narrative_multiple_diagnoses(self):
        """Test narrative with multiple diagnoses."""
        diagnoses = [
            MockPreoperativeDiagnosis(
                name="Acute Appendicitis", code="74400008", diagnosis_date=date(2024, 3, 15)
            ),
            MockPreoperativeDiagnosis(
                name="Cholelithiasis", code="235919008", diagnosis_date=date(2024, 3, 10)
            ),
            MockPreoperativeDiagnosis(
                name="Inguinal Hernia", code="396232000", diagnosis_date=date(2024, 3, 5)
            ),
        ]
        section = PreoperativeDiagnosisSection(diagnoses)
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

        assert content1.get("ID") == "preop-diagnosis-1"
        assert content2.get("ID") == "preop-diagnosis-2"
        assert content3.get("ID") == "preop-diagnosis-3"

    def test_narrative_empty(self):
        """Test narrative when no diagnoses."""
        section = PreoperativeDiagnosisSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No preoperative diagnosis"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_section_has_entries(self):
        """Test section includes entry elements (CONF:1198-10096)."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_entry_has_act(self):
        """Test entry contains Preoperative Diagnosis Act (CONF:1198-15504)."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"
        assert act.get("moodCode") == "EVN"

    def test_act_has_template_id(self):
        """Test act has correct template ID (CONF:1198-16770, CONF:1198-16771, CONF:1198-32540)."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis], version=CDAVersion.R2_1)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        template = act.find(f"{{{NS}}}templateId")

        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.65"
        assert template.get("extension") == "2015-08-01"

    def test_act_has_code(self):
        """Test act has correct code (CONF:1198-19155, CONF:1198-19156, CONF:1198-32167)."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        code = act.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "10219-4"  # Preoperative Diagnosis
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Preoperative Diagnosis"

    def test_act_has_entry_relationship(self):
        """Test act contains entryRelationship (CONF:1198-10093, CONF:1198-10094)."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")

        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "SUBJ"

    def test_entry_relationship_has_observation(self):
        """Test entryRelationship contains Problem Observation (CONF:1198-15605)."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")

        assert observation is not None
        assert observation.get("classCode") == "OBS"
        assert observation.get("moodCode") == "EVN"

    def test_observation_has_template_id(self):
        """Test observation has correct template ID."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis], version=CDAVersion.R2_1)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        template = observation.find(f"{{{NS}}}templateId")

        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.4"
        assert template.get("extension") == "2022-06-01"  # V4 template

    def test_observation_has_id(self):
        """Test observation has ID element."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        id_elem = observation.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("root") is not None

    def test_observation_has_code(self):
        """Test observation has problem type code."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "55607006"  # Problem
        assert code.get("displayName") == "Problem"

    def test_observation_has_status_code(self):
        """Test observation has statusCode.

        Per C-CDA specification, Problem Observation statusCode is always "completed"
        because it represents a completed observation of a problem (even if problem is active).
        """
        diagnosis = MockPreoperativeDiagnosis(status="active")
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        status = observation.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "completed"

    def test_observation_has_effective_time(self):
        """Test observation includes effectiveTime."""
        diagnosis = MockPreoperativeDiagnosis(diagnosis_date=date(2024, 3, 15))
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        eff_time = observation.find(f"{{{NS}}}effectiveTime")

        assert eff_time is not None
        low = eff_time.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20240315"

    def test_observation_has_value(self):
        """Test observation includes value with diagnosis code."""
        diagnosis = MockPreoperativeDiagnosis(
            name="Acute Appendicitis",
            code="74400008",
            code_system="SNOMED",
        )
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.get("code") == "74400008"
        assert value.get("displayName") == "Acute Appendicitis"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT OID

    def test_multiple_entries(self):
        """Test section with multiple diagnoses."""
        diagnoses = [
            MockPreoperativeDiagnosis(name="Acute Appendicitis", code="74400008"),
            MockPreoperativeDiagnosis(name="Cholelithiasis", code="235919008"),
        ]
        section = PreoperativeDiagnosisSection(diagnoses)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an act with observation
        for entry in entries:
            act = entry.find(f"{{{NS}}}act")
            assert act is not None
            entry_rel = act.find(f"{{{NS}}}entryRelationship")
            observation = entry_rel.find(f"{{{NS}}}observation")
            assert observation is not None

    def test_section_with_persistent_id(self):
        """Test observation uses persistent ID when provided."""
        persistent_id = MockPersistentID(
            root="2.16.840.1.113883.19",
            extension="preop-diag-123",
        )
        diagnosis = MockPreoperativeDiagnosis(persistent_id=persistent_id)
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        id_elem = observation.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.19"
        assert id_elem.get("extension") == "preop-diag-123"

    def test_section_to_string(self):
        """Test section serialization."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "10219-4" in xml  # Section code
        assert "Preoperative Diagnosis" in xml

    def test_section_structure_order(self):
        """Test that section elements are in correct order."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])
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
        section = PreoperativeDiagnosisSection([])
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
        diagnosis = MockPreoperativeDiagnosis(
            name="Acute appendicitis",
            code="K35.80",
            code_system="ICD-10",
        )
        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.get("code") == "K35.80"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.90"  # ICD-10 OID


class TestPreoperativeDiagnosisSectionIntegration:
    """Integration tests for PreoperativeDiagnosisSection."""

    def test_complete_section(self):
        """Test creating a complete preoperative diagnosis section."""
        diagnoses = [
            MockPreoperativeDiagnosis(
                name="Acute Appendicitis",
                code="74400008",
                code_system="SNOMED",
                diagnosis_date=date(2024, 3, 15),
                status="active",
            ),
            MockPreoperativeDiagnosis(
                name="Cholelithiasis",
                code="235919008",
                code_system="SNOMED",
                diagnosis_date=date(2024, 3, 10),
                status="active",
            ),
            MockPreoperativeDiagnosis(
                name="Inguinal Hernia",
                code="396232000",
                code_system="SNOMED",
                diagnosis_date=date(2024, 3, 5),
                status="active",
            ),
        ]

        section = PreoperativeDiagnosisSection(
            diagnoses,
            title="Surgical Preoperative Diagnosis",
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

        # Verify 3 entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 3

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_with_various_code_systems(self):
        """Test section with diagnoses from different code systems."""
        diagnoses = [
            MockPreoperativeDiagnosis(
                name="Acute Appendicitis",
                code="74400008",
                code_system="SNOMED",
            ),
            MockPreoperativeDiagnosis(
                name="Acute appendicitis",
                code="K35.80",
                code_system="ICD-10",
            ),
        ]

        section = PreoperativeDiagnosisSection(diagnoses)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check first diagnosis (SNOMED)
        act1 = entries[0].find(f"{{{NS}}}act")
        entry_rel1 = act1.find(f"{{{NS}}}entryRelationship")
        obs1 = entry_rel1.find(f"{{{NS}}}observation")
        value1 = obs1.find(f"{{{NS}}}value")
        assert value1.get("codeSystem") == "2.16.840.1.113883.6.96"

        # Check second diagnosis (ICD-10)
        act2 = entries[1].find(f"{{{NS}}}act")
        entry_rel2 = act2.find(f"{{{NS}}}entryRelationship")
        obs2 = entry_rel2.find(f"{{{NS}}}observation")
        value2 = obs2.find(f"{{{NS}}}value")
        assert value2.get("codeSystem") == "2.16.840.1.113883.6.90"

    def test_minimal_diagnosis(self):
        """Test section with minimal diagnosis data.

        Note: diagnosis_date (which maps to onset_date) is required for R2.1.
        """
        diagnosis = MockPreoperativeDiagnosis(
            name="Appendicitis",
            code="74400008",
            code_system="SNOMED",
            diagnosis_date=date(2024, 3, 15),  # Required for R2.1
            status="active",
        )

        section = PreoperativeDiagnosisSection([diagnosis])
        elem = section.to_element()

        # Should create valid section
        assert local_name(elem) == "section"

        # Check narrative shows the date
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")
        assert tds[3].text == "2024-03-15"

    def test_section_r21_version(self):
        """Test section with R2.1 version."""
        diagnosis = MockPreoperativeDiagnosis()
        section = PreoperativeDiagnosisSection([diagnosis], version=CDAVersion.R2_1)
        elem = section.to_element()

        # Check section template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.34"
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
        assert obs_template.get("extension") == "2022-06-01"  # V4 template
