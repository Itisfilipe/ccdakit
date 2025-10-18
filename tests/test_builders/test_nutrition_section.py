"""Tests for NutritionSection builder."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.sections.nutrition import NutritionSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockNutritionAssessment:
    """Mock nutrition assessment for testing."""

    def __init__(
        self,
        assessment_type="Diet followed",
        code="226234005",
        value="Low sodium diet",
        value_code="160670007",
        date=date(2023, 10, 1),
    ):
        self._assessment_type = assessment_type
        self._code = code
        self._value = value
        self._value_code = value_code
        self._date = date

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


class MockNutritionalStatus:
    """Mock nutritional status for testing."""

    def __init__(
        self,
        status="Well nourished",
        status_code="17621005",
        date=date(2023, 10, 1),
        assessments=None,
    ):
        self._status = status
        self._status_code = status_code
        self._date = date
        self._assessments = assessments or [MockNutritionAssessment()]

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


class TestNutritionSection:
    """Tests for NutritionSection builder."""

    def test_nutrition_section_basic(self):
        """Test basic NutritionSection creation."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_nutrition_section_has_template_id_r21(self):
        """Test NutritionSection includes R2.1 template ID."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses, version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.57"
        # No extension for this template

    def test_nutrition_section_has_template_id_r20(self):
        """Test NutritionSection includes R2.0 template ID."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses, version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.57"

    def test_nutrition_section_has_code(self):
        """Test NutritionSection includes section code."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "61144-2"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Diet and nutrition"

    def test_nutrition_section_has_title(self):
        """Test NutritionSection includes title."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses, title="Patient Nutrition")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Patient Nutrition"

    def test_nutrition_section_default_title(self):
        """Test NutritionSection uses default title."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Nutrition"

    def test_nutrition_section_has_narrative(self):
        """Test NutritionSection includes narrative text."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_nutrition_section_narrative_table(self):
        """Test narrative includes HTML table."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
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
        assert len(ths) == 4  # Nutritional Status, Date Observed, Assessment, Value

    def test_nutrition_section_narrative_content(self):
        """Test narrative contains nutrition data."""
        assessments = [
            MockNutritionAssessment(
                assessment_type="Diet followed",
                value="Low sodium diet",
                date=date(2023, 10, 15),
            )
        ]
        statuses = [
            MockNutritionalStatus(
                status="Well nourished",
                status_code="17621005",
                date=date(2023, 10, 15),
                assessments=assessments,
            )
        ]
        section = NutritionSection(statuses)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 4

        # Check nutritional status with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Well nourished"
        assert content.get("ID") == "nutrition-status-1"

        # Check date observed
        assert tds[1].text == "2023-10-15"

        # Check assessment
        assert tds[2].text == "Diet followed"

        # Check value
        assert tds[3].text == "Low sodium diet"

    def test_nutrition_section_narrative_content_with_datetime(self):
        """Test narrative shows date with time when datetime provided."""
        assessments = [MockNutritionAssessment(date=datetime(2023, 10, 15, 14, 30))]
        statuses = [
            MockNutritionalStatus(
                status="Well nourished",
                status_code="17621005",
                date=datetime(2023, 10, 15, 14, 30),
                assessments=assessments,
            )
        ]
        section = NutritionSection(statuses)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check date shows time
        assert tds[1].text == "2023-10-15 14:30"

    def test_nutrition_section_narrative_multiple_assessments(self):
        """Test narrative with multiple assessments for one status."""
        assessments = [
            MockNutritionAssessment(
                assessment_type="Diet followed",
                value="Low sodium diet",
            ),
            MockNutritionAssessment(
                assessment_type="Nutrition intake",
                value="Adequate oral intake",
            ),
        ]
        statuses = [
            MockNutritionalStatus(
                status="Well nourished",
                date=date(2023, 10, 1),
                assessments=assessments,
            )
        ]
        section = NutritionSection(statuses)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        # Should have 2 rows for 2 assessments
        assert len(trs) == 2

        # First row should have status with rowspan
        tds1 = trs[0].findall(f"{{{NS}}}td")
        assert len(tds1) == 4  # status, date, assessment, value
        assert tds1[0].get("rowspan") == "2"
        assert tds1[1].get("rowspan") == "2"

        # Second row should only have assessment and value
        tds2 = trs[1].findall(f"{{{NS}}}td")
        assert len(tds2) == 2  # only assessment, value

        # Verify assessment values
        assert tds1[2].text == "Diet followed"
        assert tds1[3].text == "Low sodium diet"
        assert tds2[0].text == "Nutrition intake"
        assert tds2[1].text == "Adequate oral intake"

    def test_nutrition_section_narrative_multiple_statuses(self):
        """Test narrative with multiple nutritional statuses."""
        statuses = [
            MockNutritionalStatus(
                status="Well nourished",
                status_code="17621005",
                date=date(2023, 10, 1),
            ),
            MockNutritionalStatus(
                status="Malnourished",
                status_code="248325000",
                date=date(2023, 10, 15),
            ),
        ]
        section = NutritionSection(statuses)
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        assert len(trs) == 2

        # Check IDs are sequential
        content1 = trs[0].find(f".//{{{NS}}}content")
        content2 = trs[1].find(f".//{{{NS}}}content")

        assert content1.get("ID") == "nutrition-status-1"
        assert content2.get("ID") == "nutrition-status-2"

        # Check status display names
        assert content1.text == "Well nourished"
        assert content2.text == "Malnourished"

    def test_nutrition_section_empty_narrative(self):
        """Test narrative when no nutritional statuses."""
        section = NutritionSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No nutrition information available"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_nutrition_section_has_entries(self):
        """Test NutritionSection includes entry elements."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_nutrition_section_entry_has_observation(self):
        """Test entry contains observation element."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        assert obs is not None
        assert obs.get("classCode") == "OBS"
        assert obs.get("moodCode") == "EVN"

    def test_nutrition_section_observation_has_template_id(self):
        """Test observation has correct template ID."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        template = obs.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.124"

    def test_nutrition_section_observation_has_code(self):
        """Test observation has correct code."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        code = obs.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "75305-3"  # Nutrition status
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC

    def test_nutrition_section_observation_has_value(self):
        """Test observation has value with status code."""
        statuses = [
            MockNutritionalStatus(
                status="Well nourished",
                status_code="17621005",
            )
        ]
        section = NutritionSection(statuses)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        value = obs.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "17621005"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT
        assert value.get("displayName") == "Well nourished"

    def test_nutrition_section_observation_has_entry_relationship(self):
        """Test observation has entryRelationship with assessment."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        entry_rel = obs.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "SUBJ"

        # Should contain Nutrition Assessment observation
        assessment_obs = entry_rel.find(f"{{{NS}}}observation")
        assert assessment_obs is not None
        assert assessment_obs.get("classCode") == "OBS"
        assert assessment_obs.get("moodCode") == "EVN"

    def test_nutrition_section_assessment_has_template_id(self):
        """Test assessment observation has correct template ID."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        entry_rel = obs.find(f"{{{NS}}}entryRelationship")
        assessment_obs = entry_rel.find(f"{{{NS}}}observation")
        template = assessment_obs.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.138"

    def test_nutrition_section_assessment_has_code(self):
        """Test assessment observation has correct code."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        entry_rel = obs.find(f"{{{NS}}}entryRelationship")
        assessment_obs = entry_rel.find(f"{{{NS}}}observation")
        code = assessment_obs.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "75303-8"  # Nutrition assessment
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC

    def test_nutrition_section_assessment_has_value_with_code(self):
        """Test assessment has value with code."""
        assessments = [
            MockNutritionAssessment(
                value="Low sodium diet",
                value_code="160670007",
            )
        ]
        statuses = [MockNutritionalStatus(assessments=assessments)]
        section = NutritionSection(statuses)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        entry_rel = obs.find(f"{{{NS}}}entryRelationship")
        assessment_obs = entry_rel.find(f"{{{NS}}}observation")
        value = assessment_obs.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("code") == "160670007"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT
        assert value.get("displayName") == "Low sodium diet"

    def test_nutrition_section_assessment_has_value_as_text(self):
        """Test assessment has value as text when no code."""
        assessments = [
            MockNutritionAssessment(
                value="Custom diet plan",
                value_code=None,
            )
        ]
        statuses = [MockNutritionalStatus(assessments=assessments)]
        section = NutritionSection(statuses)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        entry_rel = obs.find(f"{{{NS}}}entryRelationship")
        assessment_obs = entry_rel.find(f"{{{NS}}}observation")
        value = assessment_obs.find(f"{{{NS}}}value")
        assert value is not None
        assert value.text == "Custom diet plan"
        # Should not have code attribute
        assert value.get("code") is None

    def test_nutrition_section_multiple_entries(self):
        """Test NutritionSection with multiple statuses."""
        statuses = [
            MockNutritionalStatus(),
            MockNutritionalStatus(
                status="Malnourished",
                status_code="248325000",
            ),
        ]
        section = NutritionSection(statuses)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an observation
        for entry in entries:
            obs = entry.find(f"{{{NS}}}observation")
            assert obs is not None

    def test_nutrition_section_multiple_assessments_in_entry(self):
        """Test observation with multiple assessments."""
        assessments = [
            MockNutritionAssessment(
                assessment_type="Diet followed",
                value="Low sodium diet",
            ),
            MockNutritionAssessment(
                assessment_type="Nutrition intake",
                value="Adequate oral intake",
            ),
        ]
        statuses = [MockNutritionalStatus(assessments=assessments)]
        section = NutritionSection(statuses)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        entry_rels = obs.findall(f"{{{NS}}}entryRelationship")
        assert len(entry_rels) == 2

        # Each should contain an assessment observation
        for entry_rel in entry_rels:
            assert entry_rel.get("typeCode") == "SUBJ"
            assessment_obs = entry_rel.find(f"{{{NS}}}observation")
            assert assessment_obs is not None

    def test_nutrition_section_to_string(self):
        """Test NutritionSection serialization."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "61144-2" in xml  # Section code
        assert "Nutrition" in xml

    def test_nutrition_section_structure_order(self):
        """Test that section elements are in correct order."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
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

    def test_nutrition_section_observation_structure_order(self):
        """Test observation elements are in correct order."""
        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        obs = entry.find(f"{{{NS}}}observation")
        children = list(obs)
        names = [local_name(child) for child in children]

        # Check required elements are present
        assert "templateId" in names
        assert "id" in names
        assert "code" in names
        assert "statusCode" in names
        assert "effectiveTime" in names
        assert "value" in names
        assert "entryRelationship" in names

        # Verify order
        assert names.index("templateId") < names.index("id")
        assert names.index("id") < names.index("code")
        assert names.index("code") < names.index("statusCode")
        assert names.index("statusCode") < names.index("effectiveTime")
        assert names.index("effectiveTime") < names.index("value")
        assert names.index("value") < names.index("entryRelationship")


class TestNutritionSectionIntegration:
    """Integration tests for NutritionSection."""

    def test_complete_nutrition_section(self):
        """Test creating a complete nutrition section."""
        assessments1 = [
            MockNutritionAssessment(
                assessment_type="Diet followed",
                value="Low sodium diet",
                value_code="160670007",
                date=date(2023, 10, 1),
            ),
            MockNutritionAssessment(
                assessment_type="Nutrition intake",
                value="Adequate oral intake",
                value_code="289141003",
                date=date(2023, 10, 1),
            ),
        ]
        assessments2 = [
            MockNutritionAssessment(
                assessment_type="Diet followed",
                value="Diabetic diet",
                value_code="160679008",
                date=date(2023, 9, 15),
            )
        ]
        statuses = [
            MockNutritionalStatus(
                status="Well nourished",
                status_code="17621005",
                date=date(2023, 10, 1),
                assessments=assessments1,
            ),
            MockNutritionalStatus(
                status="At risk for malnutrition",
                status_code="102636007",
                date=date(2023, 9, 15),
                assessments=assessments2,
            ),
        ]

        section = NutritionSection(statuses, title="Patient Nutrition")
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify narrative table has 3 rows (2 for first status, 1 for second)
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 3

        # Verify 2 entries (2 nutritional status observations)
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Verify each entry has correct structure
        for entry in entries:
            obs = entry.find(f"{{{NS}}}observation")
            assert obs is not None
            assert obs.get("classCode") == "OBS"
            assert obs.get("moodCode") == "EVN"

            # Verify observation has required elements
            assert obs.find(f"{{{NS}}}templateId") is not None
            assert obs.find(f"{{{NS}}}id") is not None
            assert obs.find(f"{{{NS}}}code") is not None
            assert obs.find(f"{{{NS}}}statusCode") is not None
            assert obs.find(f"{{{NS}}}effectiveTime") is not None
            assert obs.find(f"{{{NS}}}value") is not None
            assert obs.find(f"{{{NS}}}entryRelationship") is not None

        # Verify first entry has 2 assessments
        obs1 = entries[0].find(f"{{{NS}}}observation")
        entry_rels1 = obs1.findall(f"{{{NS}}}entryRelationship")
        assert len(entry_rels1) == 2

        # Verify second entry has 1 assessment
        obs2 = entries[1].find(f"{{{NS}}}observation")
        entry_rels2 = obs2.findall(f"{{{NS}}}entryRelationship")
        assert len(entry_rels2) == 1

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        statuses = [MockNutritionalStatus()]
        section = NutritionSection(statuses)

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_with_various_nutritional_statuses(self):
        """Test section with various common nutritional status types."""
        statuses = [
            MockNutritionalStatus(
                status="Well nourished",
                status_code="17621005",
                date=date(2023, 10, 1),
            ),
            MockNutritionalStatus(
                status="Malnourished",
                status_code="248325000",
                date=date(2023, 9, 15),
            ),
            MockNutritionalStatus(
                status="At risk for malnutrition",
                status_code="102636007",
                date=date(2023, 8, 1),
            ),
            MockNutritionalStatus(
                status="Overweight",
                status_code="238131007",
                date=date(2023, 7, 1),
            ),
        ]

        section = NutritionSection(statuses, version=CDAVersion.R2_1)
        elem = section.to_element()

        # Verify all 4 statuses are in narrative
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 4

        # Verify all 4 statuses are in entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 4

        # Verify all status codes are present
        observations = [entry.find(f"{{{NS}}}observation") for entry in entries]
        values = [obs.find(f"{{{NS}}}value") for obs in observations]
        codes = [val.get("code") for val in values]

        assert "17621005" in codes  # Well nourished
        assert "248325000" in codes  # Malnourished
        assert "102636007" in codes  # At risk for malnutrition
        assert "238131007" in codes  # Overweight

    def test_section_empty(self):
        """Test section with no nutritional statuses."""
        section = NutritionSection([])
        elem = section.to_element()

        # Should have section structure
        assert local_name(elem) == "section"
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None

        # Should have text with paragraph, no entries
        text = elem.find(f"{{{NS}}}text")
        assert text is not None
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_section_r21_vs_r20(self):
        """Test section works for both R2.1 and R2.0."""
        statuses = [MockNutritionalStatus()]

        section_r21 = NutritionSection(statuses, version=CDAVersion.R2_1)
        elem_r21 = section_r21.to_element()

        section_r20 = NutritionSection(statuses, version=CDAVersion.R2_0)
        elem_r20 = section_r20.to_element()

        # Both should have same template root
        template_r21 = elem_r21.find(f"{{{NS}}}templateId")
        template_r20 = elem_r20.find(f"{{{NS}}}templateId")

        assert template_r21.get("root") == "2.16.840.1.113883.10.20.22.2.57"
        assert template_r20.get("root") == "2.16.840.1.113883.10.20.22.2.57"

        # Both should have same structure
        assert elem_r21.find(f"{{{NS}}}code") is not None
        assert elem_r20.find(f"{{{NS}}}code") is not None
        assert elem_r21.find(f"{{{NS}}}title") is not None
        assert elem_r20.find(f"{{{NS}}}title") is not None
        assert elem_r21.find(f"{{{NS}}}text") is not None
        assert elem_r20.find(f"{{{NS}}}text") is not None
