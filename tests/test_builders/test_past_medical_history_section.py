"""Tests for PastMedicalHistorySection builder."""

from datetime import date

import pytest
from lxml import etree

from ccdakit.builders.sections.past_medical_history import PastMedicalHistorySection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockProblem:
    """Mock problem for testing."""

    def __init__(
        self,
        name="Hypertension",
        code="38341003",
        code_system="SNOMED CT",
        onset_date=date(2010, 5, 15),
        resolved_date=None,
        status="active",
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


class TestPastMedicalHistorySection:
    """Tests for PastMedicalHistorySection builder."""

    def test_section_basic(self):
        """Test basic PastMedicalHistorySection creation."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_has_template_id_r21(self):
        """Test section includes R2.1 template ID (CONF:1198-7828, CONF:1198-10390, CONF:1198-32536)."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.20"
        assert template.get("extension") == "2015-08-01"

    def test_section_has_template_id_r20(self):
        """Test section includes R2.0 template ID."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.20"
        # R2.0 may not have extension
        assert template.get("extension") is None

    def test_section_has_code(self):
        """Test section includes correct code (CONF:1198-15474, CONF:1198-15475, CONF:1198-30831)."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "11348-0"  # History of Past Illness
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "History of Past Illness"

    def test_section_has_title(self):
        """Test section includes title (CONF:1198-7830)."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem], title="My Past Medical History")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Past Medical History"

    def test_section_default_title(self):
        """Test section uses default title."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Past Medical History"

    def test_section_has_narrative(self):
        """Test section includes narrative text (CONF:1198-7831)."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_narrative_table(self):
        """Test narrative includes HTML table."""
        problem = MockProblem(
            name="Diabetes mellitus type 2",
            code="44054006",
            code_system="SNOMED CT",
            onset_date=date(2015, 3, 10),
            status="active",
        )
        section = PastMedicalHistorySection([problem])
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
        assert len(ths) == 5  # Problem, Code, Status, Onset Date, Resolved Date

    def test_narrative_content(self):
        """Test narrative contains problem data."""
        problem = MockProblem(
            name="Asthma",
            code="195967001",
            code_system="SNOMED CT",
            onset_date=date(2008, 6, 20),
            status="active",
        )
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 5

        # Check problem name with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Asthma"
        assert content.get("ID") == "pmh-problem-1"

        # Check code
        assert tds[1].text == "195967001 (SNOMED CT)"

        # Check status
        assert tds[2].text == "Active"

        # Check onset date
        assert tds[3].text == "2008-06-20"

        # Check resolved date (should show "Ongoing" for active problems)
        assert tds[4].text == "Ongoing"

    def test_narrative_without_onset_date(self):
        """Test narrative shows 'Unknown' for missing onset date.

        Uses R2.0 since R2.1 requires onset_date per specification.
        """
        problem = MockProblem(onset_date=None)
        section = PastMedicalHistorySection([problem], version=CDAVersion.R2_0)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check onset date shows "Unknown"
        assert tds[3].text == "Unknown"

    def test_narrative_resolved_problem(self):
        """Test narrative shows resolved date correctly."""
        problem = MockProblem(
            name="Appendicitis",
            status="resolved",
            onset_date=date(2005, 8, 15),
            resolved_date=date(2005, 8, 20),
        )
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check status
        assert tds[2].text == "Resolved"

        # Check resolved date
        assert tds[4].text == "2005-08-20"

    def test_narrative_resolved_without_date(self):
        """Test narrative shows 'Unknown' for resolved problems without date."""
        problem = MockProblem(
            name="Pneumonia",
            status="resolved",
            onset_date=date(2012, 1, 5),
            resolved_date=None,
        )
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check resolved date shows "Unknown" for resolved problems without date
        assert tds[4].text == "Unknown"

    def test_narrative_multiple_problems(self):
        """Test narrative with multiple problems."""
        problems = [
            MockProblem(name="Hypertension", code="38341003"),
            MockProblem(name="Diabetes", code="73211009"),
            MockProblem(name="Asthma", code="195967001"),
        ]
        section = PastMedicalHistorySection(problems)
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

        assert content1.get("ID") == "pmh-problem-1"
        assert content2.get("ID") == "pmh-problem-2"
        assert content3.get("ID") == "pmh-problem-3"

    def test_narrative_empty(self):
        """Test narrative when no problems."""
        section = PastMedicalHistorySection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No past medical history"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_section_has_entries(self):
        """Test section includes entry elements (CONF:1198-8791)."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_entry_has_observation(self):
        """Test entry contains Problem Observation (CONF:1198-15476)."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"
        assert observation.get("moodCode") == "EVN"

    def test_observation_has_template_id(self):
        """Test observation has correct template ID."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem], version=CDAVersion.R2_1)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        template = observation.find(f"{{{NS}}}templateId")

        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.4"
        assert template.get("extension") == "2022-06-01"  # V4 template

    def test_observation_has_id(self):
        """Test observation has ID element."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        id_elem = observation.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("root") is not None

    def test_observation_has_code(self):
        """Test observation has problem type code."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "55607006"  # Problem
        assert code.get("displayName") == "Problem"

    def test_observation_has_status_code(self):
        """Test observation has statusCode.

        Per C-CDA specification, Problem Observation statusCode is always "completed"
        because it represents a completed observation of a problem (even if problem is active).
        """
        problem = MockProblem(status="active")
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        status = observation.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "completed"

    def test_observation_has_effective_time(self):
        """Test observation includes effectiveTime."""
        problem = MockProblem(
            onset_date=date(2010, 5, 15),
            resolved_date=None,
        )
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        eff_time = observation.find(f"{{{NS}}}effectiveTime")

        assert eff_time is not None
        low = eff_time.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20100515"

    def test_observation_has_value(self):
        """Test observation includes value with problem code."""
        problem = MockProblem(
            name="Hypertension",
            code="38341003",
            code_system="SNOMED CT",
        )
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.get("code") == "38341003"
        assert value.get("displayName") == "Hypertension"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT OID

    def test_multiple_entries(self):
        """Test section with multiple problems."""
        problems = [
            MockProblem(name="Hypertension", code="38341003"),
            MockProblem(name="Diabetes", code="73211009"),
        ]
        section = PastMedicalHistorySection(problems)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an observation
        for entry in entries:
            observation = entry.find(f"{{{NS}}}observation")
            assert observation is not None

    def test_section_with_persistent_id(self):
        """Test observation uses persistent ID when provided."""
        persistent_id = MockPersistentID(
            root="2.16.840.1.113883.19",
            extension="problem-123",
        )
        problem = MockProblem(persistent_id=persistent_id)
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        id_elem = observation.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.19"
        assert id_elem.get("extension") == "problem-123"

    def test_section_to_string(self):
        """Test section serialization."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "11348-0" in xml  # Section code
        assert "Past Medical History" in xml

    def test_section_structure_order(self):
        """Test that section elements are in correct order."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem])
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

    def test_section_empty_problems(self):
        """Test section with empty problem list."""
        section = PastMedicalHistorySection([])
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
        problem = MockProblem(
            name="Essential hypertension",
            code="I10",
            code_system="ICD-10",
        )
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.get("code") == "I10"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.90"  # ICD-10 OID

    def test_observation_resolved_with_high_date(self):
        """Test observation includes high date for resolved problems."""
        problem = MockProblem(
            name="Pneumonia",
            status="resolved",
            onset_date=date(2020, 3, 10),
            resolved_date=date(2020, 3, 25),
        )
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        eff_time = observation.find(f"{{{NS}}}effectiveTime")

        assert eff_time is not None
        low = eff_time.find(f"{{{NS}}}low")
        high = eff_time.find(f"{{{NS}}}high")

        assert low is not None
        assert low.get("value") == "20200310"
        assert high is not None
        assert high.get("value") == "20200325"

    def test_observation_inactive_status(self):
        """Test observation with inactive status.

        Per C-CDA specification, Problem Observation statusCode is always "completed"
        because it represents a completed observation of a problem (even if problem is inactive).
        """
        problem = MockProblem(status="inactive")
        section = PastMedicalHistorySection([problem])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        status = observation.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "completed"


class TestPastMedicalHistorySectionIntegration:
    """Integration tests for PastMedicalHistorySection."""

    def test_complete_section(self):
        """Test creating a complete past medical history section."""
        problems = [
            MockProblem(
                name="Hypertension",
                code="38341003",
                code_system="SNOMED CT",
                onset_date=date(2010, 5, 15),
                status="active",
            ),
            MockProblem(
                name="Type 2 diabetes mellitus",
                code="44054006",
                code_system="SNOMED CT",
                onset_date=date(2012, 8, 20),
                status="active",
            ),
            MockProblem(
                name="Appendicitis",
                code="74400008",
                code_system="SNOMED CT",
                onset_date=date(2005, 3, 10),
                resolved_date=date(2005, 3, 15),
                status="resolved",
            ),
        ]

        section = PastMedicalHistorySection(
            problems,
            title="Patient Past Medical History",
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

        problem = MockProblem()
        section = PastMedicalHistorySection([problem])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_with_various_code_systems(self):
        """Test section with problems from different code systems."""
        problems = [
            MockProblem(
                name="Hypertension",
                code="38341003",
                code_system="SNOMED CT",
            ),
            MockProblem(
                name="Essential hypertension",
                code="I10",
                code_system="ICD-10",
            ),
        ]

        section = PastMedicalHistorySection(problems)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check first problem (SNOMED)
        obs1 = entries[0].find(f"{{{NS}}}observation")
        value1 = obs1.find(f"{{{NS}}}value")
        assert value1.get("codeSystem") == "2.16.840.1.113883.6.96"

        # Check second problem (ICD-10)
        obs2 = entries[1].find(f"{{{NS}}}observation")
        value2 = obs2.find(f"{{{NS}}}value")
        assert value2.get("codeSystem") == "2.16.840.1.113883.6.90"

    def test_section_r20_version(self):
        """Test section with R2.0 version."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem], version=CDAVersion.R2_0)
        elem = section.to_element()

        # Check template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.20"
        assert template.get("extension") is None

        # Check observation template ID
        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        obs_template = observation.find(f"{{{NS}}}templateId")
        assert obs_template.get("extension") == "2014-06-09"

    def test_section_r21_version(self):
        """Test section with R2.1 version."""
        problem = MockProblem()
        section = PastMedicalHistorySection([problem], version=CDAVersion.R2_1)
        elem = section.to_element()

        # Check template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.20"
        assert template.get("extension") == "2015-08-01"

        # Check observation template ID
        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        obs_template = observation.find(f"{{{NS}}}templateId")
        assert obs_template.get("extension") == "2022-06-01"  # V4 template

    def test_section_with_null_flavor_handling(self):
        """Test that R2.1 raises ValueError when onset_date is None.

        R2.1 requires onset_date per C-CDA specification.
        """
        # Problem without onset date
        problem = MockProblem(onset_date=None)
        section = PastMedicalHistorySection([problem])

        with pytest.raises(ValueError, match="onset date"):
            section.to_element()

    def test_section_with_null_flavor_handling_r20(self):
        """Test section handles missing data in R2.0.

        Uses R2.0 since R2.1 requires onset_date per specification.
        When both onset_date and resolved_date are None, effectiveTime
        is created but without low/high children.
        """
        # Problem without onset date
        problem = MockProblem(onset_date=None)
        section = PastMedicalHistorySection([problem], version=CDAVersion.R2_0)
        elem = section.to_element()

        # effectiveTime should be present but empty when no dates are provided
        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        eff_time = observation.find(f"{{{NS}}}effectiveTime")

        # effectiveTime is created but without low/high when both dates are None
        assert eff_time is not None
        low = eff_time.find(f"{{{NS}}}low")
        high = eff_time.find(f"{{{NS}}}high")
        assert low is None
        assert high is None
