"""Tests for AdmissionDiagnosisSection builder."""

from datetime import date

import pytest
from lxml import etree

from ccdakit.builders.sections.admission_diagnosis import AdmissionDiagnosisSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockPersistentID:
    """Mock persistent ID for testing."""

    def __init__(self, root="2.16.840.1.113883.3.TEST", extension="ADM-001"):
        self._root = root
        self._extension = extension

    @property
    def root(self):
        return self._root

    @property
    def extension(self):
        return self._extension


class MockAdmissionDiagnosis:
    """Mock admission diagnosis for testing."""

    def __init__(
        self,
        name="Acute Myocardial Infarction",
        code="57054005",
        code_system="SNOMED",
        admission_date=None,
        diagnosis_date=date(2024, 1, 15),
        persistent_id=None,
    ):
        self._name = name
        self._code = code
        self._code_system = code_system
        self._admission_date = admission_date
        self._diagnosis_date = diagnosis_date
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
    def persistent_id(self):
        return self._persistent_id

    # Properties required by ProblemProtocol (since Hospital Admission Diagnosis uses it)
    @property
    def status(self):
        return "active"

    @property
    def onset_date(self):
        return self._diagnosis_date

    @property
    def resolved_date(self):
        return None


class TestAdmissionDiagnosisSection:
    """Tests for AdmissionDiagnosisSection builder."""

    # Basic Section Tests

    def test_section_basic(self):
        """Test basic AdmissionDiagnosisSection creation."""
        section = AdmissionDiagnosisSection()
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_with_diagnoses(self):
        """Test AdmissionDiagnosisSection with diagnoses."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        assert local_name(elem) == "section"

    # Template ID Tests

    def test_has_template_id_r21(self):
        """Test section includes R2.1 template ID (CONF:1198-9930, 10391, 32563)."""
        section = AdmissionDiagnosisSection(version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.43"
        assert template.get("extension") == "2015-08-01"

    # Section Code Tests

    def test_has_code(self):
        """Test section includes required code (CONF:1198-15479, 15480)."""
        section = AdmissionDiagnosisSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "46241-6"

    def test_code_system(self):
        """Test section code system is LOINC (CONF:1198-30865)."""
        section = AdmissionDiagnosisSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"

    def test_code_display_name(self):
        """Test section code has display name."""
        section = AdmissionDiagnosisSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code.get("displayName") == "Hospital Admission diagnosis"

    def test_code_has_translation(self):
        """Test section code has required translation (CONF:1198-32749)."""
        section = AdmissionDiagnosisSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        translation = code.find(f"{{{NS}}}translation")
        assert translation is not None

    def test_translation_code(self):
        """Test translation has correct code (CONF:1198-32750)."""
        section = AdmissionDiagnosisSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        translation = code.find(f"{{{NS}}}translation")
        assert translation.get("code") == "42347-5"

    def test_translation_code_system(self):
        """Test translation has correct codeSystem (CONF:1198-32751)."""
        section = AdmissionDiagnosisSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        translation = code.find(f"{{{NS}}}translation")
        assert translation.get("codeSystem") == "2.16.840.1.113883.6.1"

    def test_translation_display_name(self):
        """Test translation has display name."""
        section = AdmissionDiagnosisSection()
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        translation = code.find(f"{{{NS}}}translation")
        assert translation.get("displayName") == "Admission Diagnosis"

    # Title Tests

    def test_has_title(self):
        """Test section includes title (CONF:1198-9932)."""
        section = AdmissionDiagnosisSection()
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Hospital Admission Diagnosis"

    def test_custom_title(self):
        """Test section with custom title."""
        section = AdmissionDiagnosisSection(title="Admission Diagnoses")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Admission Diagnoses"

    # Narrative Text Tests

    def test_has_narrative(self):
        """Test section includes narrative text (CONF:1198-9933)."""
        section = AdmissionDiagnosisSection()
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_narrative_empty_diagnoses(self):
        """Test narrative with no diagnoses shows placeholder."""
        section = AdmissionDiagnosisSection()
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert "No admission diagnosis documented" in paragraph.text

    def test_narrative_table_structure(self):
        """Test narrative creates proper table structure."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        assert table is not None
        assert table.get("border") == "1"
        assert table.get("width") == "100%"

    def test_narrative_table_headers(self):
        """Test narrative table has correct headers."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        thead = table.find(f"{{{NS}}}thead")
        tr = thead.find(f"{{{NS}}}tr")
        headers = tr.findall(f"{{{NS}}}th")

        assert len(headers) == 4
        header_texts = [h.text for h in headers]
        assert "Diagnosis" in header_texts
        assert "Code" in header_texts
        assert "Admission Date" in header_texts
        assert "Diagnosis Date" in header_texts

    def test_narrative_diagnosis_name(self):
        """Test narrative includes diagnosis name with ID."""
        diagnosis = MockAdmissionDiagnosis(name="Pneumonia")
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        content = text.find(f".//{{{NS}}}content[@ID='admission-diagnosis-1']")
        assert content is not None
        assert content.text == "Pneumonia"

    def test_narrative_diagnosis_code(self):
        """Test narrative includes diagnosis code."""
        diagnosis = MockAdmissionDiagnosis(code="233604007", code_system="SNOMED")
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        tbody = text.find(f".//{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")
        code_td = tds[1]  # Second column is code

        assert "233604007" in code_td.text
        assert "SNOMED" in code_td.text

    def test_narrative_with_dates(self):
        """Test narrative includes admission and diagnosis dates."""
        diagnosis = MockAdmissionDiagnosis(
            admission_date=date(2024, 1, 15),
            diagnosis_date=date(2024, 1, 15),
        )
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        tbody = text.find(f".//{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        admission_td = tds[2]  # Third column
        diagnosis_td = tds[3]  # Fourth column

        assert admission_td.text == "2024-01-15"
        assert diagnosis_td.text == "2024-01-15"

    def test_narrative_without_dates(self):
        """Test that R2.1 raises ValueError when diagnosis_date is None.

        R2.1 requires onset_date (diagnosis_date) per C-CDA specification.
        """
        diagnosis = MockAdmissionDiagnosis(
            admission_date=None,
            diagnosis_date=None,
        )
        section = AdmissionDiagnosisSection([diagnosis])

        with pytest.raises(ValueError, match="onset date"):
            section.to_element()

    def test_narrative_multiple_diagnoses(self):
        """Test narrative with multiple diagnoses."""
        diagnoses = [
            MockAdmissionDiagnosis(name="Acute MI", code="57054005"),
            MockAdmissionDiagnosis(name="Heart Failure", code="84114007"),
            MockAdmissionDiagnosis(name="Hypertension", code="38341003"),
        ]
        section = AdmissionDiagnosisSection(diagnoses)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        tbody = text.find(f".//{{{NS}}}tbody")
        rows = tbody.findall(f"{{{NS}}}tr")

        assert len(rows) == 3

        # Check each diagnosis has unique ID
        for idx in range(1, 4):
            content = text.find(
                f".//{{{NS}}}content[@ID='admission-diagnosis-{idx}']"
            )
            assert content is not None

    # Entry Tests

    def test_has_entry(self):
        """Test section contains entry (CONF:1198-9934)."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_entry_contains_act(self):
        """Test entry contains Hospital Admission Diagnosis act (CONF:1198-15481)."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"
        assert act.get("moodCode") == "EVN"

    def test_multiple_entries(self):
        """Test section with multiple diagnosis entries."""
        diagnoses = [
            MockAdmissionDiagnosis(name="Diagnosis 1", code="12345"),
            MockAdmissionDiagnosis(name="Diagnosis 2", code="67890"),
        ]
        section = AdmissionDiagnosisSection(diagnoses)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_no_entries_when_empty(self):
        """Test section with no diagnoses has no entries."""
        section = AdmissionDiagnosisSection()
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    # Hospital Admission Diagnosis Act Tests

    def test_act_has_template_id(self):
        """Test Hospital Admission Diagnosis act has template ID (CONF:1198-16747, 16748)."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        template = act.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.34"
        assert template.get("extension") == "2015-08-01"

    def test_act_has_code(self):
        """Test Hospital Admission Diagnosis act has code (CONF:1198-19145, 19146)."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        code = act.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "46241-6"

    def test_act_code_system(self):
        """Test Hospital Admission Diagnosis act code system (CONF:1198-32162)."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        code = act.find(f"{{{NS}}}code")
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"

    def test_act_has_entry_relationship(self):
        """Test Hospital Admission Diagnosis act has entryRelationship (CONF:1198-7674, 7675)."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "SUBJ"

    def test_act_contains_problem_observation(self):
        """Test Hospital Admission Diagnosis contains Problem Observation (CONF:1198-15535)."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        act = elem.find(f".//{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        observation = entry_rel.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"
        assert observation.get("moodCode") == "EVN"

    # Problem Observation Tests

    def test_problem_observation_has_template_id(self):
        """Test Problem Observation has correct template ID."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        observation = elem.find(f".//{{{NS}}}observation")
        template = observation.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.4"
        assert template.get("extension") == "2022-06-01"  # V4 template

    def test_problem_observation_has_code(self):
        """Test Problem Observation has correct code (55607006 = Problem)."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        observation = elem.find(f".//{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "55607006"

    def test_problem_observation_has_value(self):
        """Test Problem Observation has value with diagnosis code."""
        diagnosis = MockAdmissionDiagnosis(
            name="Acute MI",
            code="57054005",
            code_system="SNOMED",
        )
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        observation = elem.find(f".//{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "57054005"
        assert value.get("displayName") == "Acute MI"

    def test_problem_observation_snomed_code(self):
        """Test Problem Observation with SNOMED code."""
        diagnosis = MockAdmissionDiagnosis(
            code="233604007",
            code_system="SNOMED",
        )
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        observation = elem.find(f".//{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"

    def test_problem_observation_icd10_code(self):
        """Test Problem Observation with ICD-10 code."""
        diagnosis = MockAdmissionDiagnosis(
            code="I21.9",
            code_system="ICD-10",
        )
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        observation = elem.find(f".//{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")
        assert value.get("codeSystem") == "2.16.840.1.113883.6.90"

    # Code System Tests

    def test_snomed_code_system_oid(self):
        """Test SNOMED code system uses correct OID."""
        diagnosis = MockAdmissionDiagnosis(code_system="SNOMED")
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        value = elem.find(f".//{{{NS}}}value")
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"

    def test_icd10_code_system_oid(self):
        """Test ICD-10 code system uses correct OID."""
        diagnosis = MockAdmissionDiagnosis(code_system="ICD-10")
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        value = elem.find(f".//{{{NS}}}value")
        assert value.get("codeSystem") == "2.16.840.1.113883.6.90"

    # Edge Cases and Corner Cases

    def test_empty_diagnoses_list(self):
        """Test section with empty diagnoses list."""
        section = AdmissionDiagnosisSection(diagnoses=[])
        elem = section.to_element()

        assert local_name(elem) == "section"
        text = elem.find(f"{{{NS}}}text")
        assert text is not None
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_none_diagnoses_list(self):
        """Test section with None diagnoses list."""
        section = AdmissionDiagnosisSection(diagnoses=None)
        elem = section.to_element()

        assert local_name(elem) == "section"
        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_diagnosis_with_persistent_id(self):
        """Test diagnosis with persistent ID."""
        persistent_id = MockPersistentID()
        diagnosis = MockAdmissionDiagnosis(persistent_id=persistent_id)
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        observation = elem.find(f".//{{{NS}}}observation")
        id_elem = observation.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.3.TEST"
        assert id_elem.get("extension") == "ADM-001"

    def test_diagnosis_without_persistent_id(self):
        """Test diagnosis without persistent ID generates UUID."""
        diagnosis = MockAdmissionDiagnosis(persistent_id=None)
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        observation = elem.find(f".//{{{NS}}}observation")
        id_elem = observation.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.19"
        assert id_elem.get("extension") is not None

    # XML Structure Validation Tests

    def test_element_order(self):
        """Test elements appear in correct order per CDA schema."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        # Check order: templateId, code, title, text, entry
        children = list(elem)
        child_names = [local_name(c) for c in children]

        template_idx = child_names.index("templateId")
        code_idx = child_names.index("code")
        title_idx = child_names.index("title")
        text_idx = child_names.index("text")

        assert template_idx < code_idx < title_idx < text_idx

        # Entry should be after text if present
        if "entry" in child_names:
            entry_idx = child_names.index("entry")
            assert text_idx < entry_idx

    def test_namespace_consistency(self):
        """Test all elements use correct namespace."""
        diagnosis = MockAdmissionDiagnosis()
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        # Check section namespace
        assert elem.tag == f"{{{NS}}}section"

        # Check all descendants have namespace
        for descendant in elem.iter():
            assert descendant.tag.startswith(f"{{{NS}}}")

    # Integration Tests

    def test_complete_section_with_all_features(self):
        """Test complete section with all features enabled."""
        persistent_id = MockPersistentID(
            root="2.16.840.1.113883.3.HOSPITAL",
            extension="ADM-2024-001",
        )

        diagnoses = [
            MockAdmissionDiagnosis(
                name="Acute ST-elevation myocardial infarction",
                code="57054005",
                code_system="SNOMED",
                admission_date=date(2024, 1, 15),
                diagnosis_date=date(2024, 1, 15),
                persistent_id=persistent_id,
            ),
            MockAdmissionDiagnosis(
                name="Congestive heart failure",
                code="84114007",
                code_system="SNOMED",
                admission_date=date(2024, 1, 15),
                diagnosis_date=date(2024, 1, 15),
                persistent_id=None,
            ),
        ]

        section = AdmissionDiagnosisSection(
            diagnoses=diagnoses,
            title="Hospital Admission Diagnoses",
            version=CDAVersion.R2_1,
        )
        elem = section.to_element()

        # Verify section structure
        assert local_name(elem) == "section"
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title").text == "Hospital Admission Diagnoses"
        assert elem.find(f"{{{NS}}}text") is not None

        # Verify narrative table
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        assert table is not None
        tbody = table.find(f"{{{NS}}}tbody")
        rows = tbody.findall(f"{{{NS}}}tr")
        assert len(rows) == 2

        # Verify entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Verify first diagnosis has persistent ID
        first_observation = entries[0].find(f".//{{{NS}}}observation")
        first_id = first_observation.find(f"{{{NS}}}id")
        assert first_id.get("root") == "2.16.840.1.113883.3.HOSPITAL"
        assert first_id.get("extension") == "ADM-2024-001"

        # Verify second diagnosis has generated ID
        second_observation = entries[1].find(f".//{{{NS}}}observation")
        second_id = second_observation.find(f"{{{NS}}}id")
        assert second_id.get("root") == "2.16.840.1.113883.19"

    def test_minimal_section(self):
        """Test minimal valid section with required data only."""
        diagnosis = MockAdmissionDiagnosis(
            name="Chest pain",
            code="29857009",
            code_system="SNOMED",
            admission_date=None,
            diagnosis_date=date(2024, 1, 15),  # Required for R2.1
            persistent_id=None,
        )
        section = AdmissionDiagnosisSection([diagnosis])
        elem = section.to_element()

        # Should still be valid with all required elements
        assert local_name(elem) == "section"
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None
        assert len(elem.findall(f"{{{NS}}}entry")) == 1

        # Check narrative shows "Unknown" for missing admission_date
        text = elem.find(f"{{{NS}}}text")
        tbody = text.find(f".//{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")
        assert tds[2].text == "Unknown"  # Admission date (optional)
        assert tds[3].text == "2024-01-15"  # Diagnosis date (required)
