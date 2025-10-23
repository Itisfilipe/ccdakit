"""Tests for Hospital Discharge Studies Summary Section builder."""

from datetime import date, datetime
from typing import Sequence

from lxml import etree

from ccdakit.builders.sections.discharge_studies import (
    HospitalDischargeStudiesSummarySection,
)
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockDischargeStudy:
    """Mock discharge study observation for testing."""

    def __init__(
        self,
        study_name="Chest X-Ray",
        study_code="36643-5",
        value="Normal",
        unit=None,
        status="completed",
        effective_time=date(2023, 10, 1),
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
        self._effective_time = effective_time
        self._value_type = value_type
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

    # Add these properties for compatibility with ResultObservationProtocol
    @property
    def test_name(self):
        return self._study_name

    @property
    def test_code(self):
        return self._study_code


class MockDischargeStudyOrganizer:
    """Mock discharge study organizer for testing."""

    def __init__(
        self,
        study_panel_name="Imaging Studies",
        study_panel_code="72170-4",
        status="completed",
        effective_time=datetime(2023, 10, 1, 10, 30),
        studies=None,
    ):
        self._study_panel_name = study_panel_name
        self._study_panel_code = study_panel_code
        self._status = status
        self._effective_time = effective_time
        self._studies = studies or []

    @property
    def study_panel_name(self) -> str:
        return self._study_panel_name

    @property
    def study_panel_code(self) -> str:
        return self._study_panel_code

    @property
    def status(self) -> str:
        return self._status

    @property
    def effective_time(self) -> datetime:
        return self._effective_time

    @property
    def studies(self) -> Sequence[MockDischargeStudy]:
        return self._studies

    # Add these properties for compatibility with ResultOrganizerProtocol
    @property
    def panel_name(self) -> str:
        return self._study_panel_name

    @property
    def panel_code(self) -> str:
        return self._study_panel_code

    @property
    def results(self) -> Sequence[MockDischargeStudy]:
        return self._studies


class TestHospitalDischargeStudiesSummarySection:
    """Tests for HospitalDischargeStudiesSummarySection builder."""

    def test_discharge_studies_section_basic(self):
        """Test basic HospitalDischargeStudiesSummarySection creation."""
        studies = [MockDischargeStudy()]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_discharge_studies_section_has_template_id_r21(self):
        """Test HospitalDischargeStudiesSummarySection includes R2.1 template ID."""
        studies = [MockDischargeStudy()]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection(
            [organizer], version=CDAVersion.R2_1
        )
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.16"
        # This section does not have an extension
        assert template.get("extension") is None

    def test_discharge_studies_section_has_template_id_r20(self):
        """Test HospitalDischargeStudiesSummarySection includes R2.0 template ID."""
        studies = [MockDischargeStudy()]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection(
            [organizer], version=CDAVersion.R2_0
        )
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.16"

    def test_discharge_studies_section_has_code(self):
        """Test HospitalDischargeStudiesSummarySection includes section code."""
        studies = [MockDischargeStudy()]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "11493-4"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Hospital Discharge Studies Summary"

    def test_discharge_studies_section_has_title(self):
        """Test HospitalDischargeStudiesSummarySection includes title."""
        studies = [MockDischargeStudy()]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection(
            [organizer], title="Discharge Studies"
        )
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Discharge Studies"

    def test_discharge_studies_section_default_title(self):
        """Test HospitalDischargeStudiesSummarySection uses default title."""
        studies = [MockDischargeStudy()]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Hospital Discharge Studies Summary"

    def test_discharge_studies_section_has_narrative(self):
        """Test HospitalDischargeStudiesSummarySection includes narrative text."""
        studies = [MockDischargeStudy()]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_discharge_studies_section_narrative_has_table(self):
        """Test HospitalDischargeStudiesSummarySection narrative includes table."""
        studies = [MockDischargeStudy()]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        table = elem.find(f".//{{{NS}}}table")
        assert table is not None
        assert table.get("border") == "1"
        assert table.get("width") == "100%"

    def test_discharge_studies_section_narrative_table_headers(self):
        """Test HospitalDischargeStudiesSummarySection narrative table has correct headers."""
        studies = [MockDischargeStudy()]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        thead = elem.find(f".//{{{NS}}}thead")
        assert thead is not None

        headers = thead.findall(f".//{{{NS}}}th")
        header_texts = [h.text for h in headers]
        expected_headers = [
            "Study Panel",
            "Study",
            "Value",
            "Unit",
            "Interpretation",
            "Reference Range",
            "Date",
        ]
        assert header_texts == expected_headers

    def test_discharge_studies_section_narrative_with_single_study(self):
        """Test HospitalDischargeStudiesSummarySection narrative with a single study."""
        studies = [
            MockDischargeStudy(
                study_name="Chest X-Ray",
                value="Normal lung fields",
                unit=None,
                interpretation="Normal",
            )
        ]
        organizer = MockDischargeStudyOrganizer(
            study_panel_name="Imaging Studies",
            effective_time=datetime(2023, 10, 15, 10, 30),
            studies=studies,
        )
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        rows = tbody.findall(f"{{{NS}}}tr")
        assert len(rows) == 1

        # Check panel name
        panel_content = rows[0].find(
            f".//{{{NS}}}content[@ID='discharge-study-panel-1']"
        )
        assert panel_content is not None
        assert panel_content.text == "Imaging Studies"

        # Check study name
        study_content = rows[0].find(f".//{{{NS}}}content[@ID='discharge-study-1-1']")
        assert study_content is not None
        assert study_content.text == "Chest X-Ray"

    def test_discharge_studies_section_narrative_with_multiple_studies_in_panel(self):
        """Test HospitalDischargeStudiesSummarySection narrative with multiple studies in one panel."""
        studies = [
            MockDischargeStudy(study_name="Chest X-Ray", value="Normal", unit=None),
            MockDischargeStudy(
                study_name="CT Chest",
                value="No acute findings",
                unit=None,
            ),
        ]
        organizer = MockDischargeStudyOrganizer(
            study_panel_name="Imaging Studies",
            studies=studies,
        )
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        rows = tbody.findall(f"{{{NS}}}tr")
        assert len(rows) == 2

        # First row should have panel name
        panel_td = rows[0].findall(f"{{{NS}}}td")[0]
        assert panel_td.find(f"{{{NS}}}content") is not None

        # Second row should have empty panel cell
        panel_td_2 = rows[1].findall(f"{{{NS}}}td")[0]
        assert panel_td_2.text == ""

    def test_discharge_studies_section_narrative_with_multiple_panels(self):
        """Test HospitalDischargeStudiesSummarySection narrative with multiple panels."""
        organizer1 = MockDischargeStudyOrganizer(
            study_panel_name="Imaging Studies",
            studies=[
                MockDischargeStudy(study_name="Chest X-Ray", value="Normal", unit=None)
            ],
        )
        organizer2 = MockDischargeStudyOrganizer(
            study_panel_name="Laboratory Studies",
            studies=[
                MockDischargeStudy(
                    study_name="Hemoglobin", value="14.5", unit="g/dL"
                )
            ],
        )
        section = HospitalDischargeStudiesSummarySection([organizer1, organizer2])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        rows = tbody.findall(f"{{{NS}}}tr")
        assert len(rows) == 2

        # Check panel names
        panel1_content = rows[0].find(
            f".//{{{NS}}}content[@ID='discharge-study-panel-1']"
        )
        assert panel1_content.text == "Imaging Studies"

        panel2_content = rows[1].find(
            f".//{{{NS}}}content[@ID='discharge-study-panel-2']"
        )
        assert panel2_content.text == "Laboratory Studies"

    def test_discharge_studies_section_narrative_with_interpretation(self):
        """Test HospitalDischargeStudiesSummarySection narrative includes interpretation."""
        studies = [
            MockDischargeStudy(
                study_name="Echocardiogram",
                value="55%",
                unit="%",
                interpretation="Normal",
            )
        ]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        # Interpretation is the 5th column (index 4)
        interpretation_cell = cells[4]
        assert interpretation_cell.text == "Normal"

    def test_discharge_studies_section_narrative_without_interpretation(self):
        """Test HospitalDischargeStudiesSummarySection narrative with no interpretation shows dash."""
        studies = [
            MockDischargeStudy(
                study_name="Chest X-Ray",
                value="Normal",
                unit=None,
                interpretation=None,
            )
        ]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        interpretation_cell = cells[4]
        assert interpretation_cell.text == "-"

    def test_discharge_studies_section_narrative_with_reference_range(self):
        """Test HospitalDischargeStudiesSummarySection narrative includes reference range."""
        studies = [
            MockDischargeStudy(
                study_name="LVEF",
                study_code="10230-1",
                value="55",
                unit="%",
                reference_range_low="50",
                reference_range_high="70",
                reference_range_unit="%",
            )
        ]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        # Reference range is the 6th column (index 5)
        range_cell = cells[5]
        assert "50" in range_cell.text
        assert "70" in range_cell.text
        assert "%" in range_cell.text

    def test_discharge_studies_section_narrative_without_reference_range(self):
        """Test HospitalDischargeStudiesSummarySection narrative with no reference range shows dash."""
        studies = [
            MockDischargeStudy(
                study_name="Chest X-Ray",
                value="Normal",
                unit=None,
                reference_range_low=None,
                reference_range_high=None,
            )
        ]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        range_cell = cells[5]
        assert range_cell.text == "-"

    def test_discharge_studies_section_narrative_without_unit(self):
        """Test HospitalDischargeStudiesSummarySection narrative with no unit shows dash."""
        studies = [
            MockDischargeStudy(
                study_name="Chest X-Ray",
                value="Normal lung fields",
                unit=None,
            )
        ]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        # Unit is the 4th column (index 3)
        unit_cell = cells[3]
        assert unit_cell.text == "-"

    def test_discharge_studies_section_narrative_date_format(self):
        """Test HospitalDischargeStudiesSummarySection narrative displays date correctly."""
        test_date = datetime(2023, 10, 15, 10, 30)
        studies = [MockDischargeStudy()]
        organizer = MockDischargeStudyOrganizer(effective_time=test_date, studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        # Date is the 7th column (index 6)
        date_cell = cells[6]
        assert date_cell.text == "2023-10-15"

    def test_discharge_studies_section_empty_studies(self):
        """Test HospitalDischargeStudiesSummarySection with no studies."""
        section = HospitalDischargeStudiesSummarySection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No discharge studies available"

        # Should not have a table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_discharge_studies_section_has_entries(self):
        """Test HospitalDischargeStudiesSummarySection includes entry elements."""
        studies = [MockDischargeStudy()]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_discharge_studies_section_entry_has_organizer(self):
        """Test HospitalDischargeStudiesSummarySection entry contains organizer."""
        studies = [MockDischargeStudy()]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        assert entry is not None
        assert entry.get("typeCode") == "DRIV"

        organizer_elem = entry.find(f"{{{NS}}}organizer")
        assert organizer_elem is not None

    def test_discharge_studies_section_multiple_organizers(self):
        """Test HospitalDischargeStudiesSummarySection with multiple organizers."""
        organizer1 = MockDischargeStudyOrganizer(
            study_panel_name="Imaging Panel 1",
            studies=[MockDischargeStudy()],
        )
        organizer2 = MockDischargeStudyOrganizer(
            study_panel_name="Lab Panel 2",
            studies=[MockDischargeStudy()],
        )
        section = HospitalDischargeStudiesSummarySection([organizer1, organizer2])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_discharge_studies_section_imaging_study(self):
        """Test HospitalDischargeStudiesSummarySection with imaging study."""
        studies = [
            MockDischargeStudy(
                study_name="Chest X-Ray (2 views)",
                study_code="36643-5",
                value="No acute cardiopulmonary process. Normal heart size.",
                unit=None,
                status="final",
                effective_time=date(2023, 10, 15),
                interpretation="Normal",
            ),
        ]
        organizer = MockDischargeStudyOrganizer(
            study_panel_name="Chest Imaging",
            study_panel_code="72170-4",
            status="completed",
            effective_time=datetime(2023, 10, 15, 14, 30),
            studies=studies,
        )
        section = HospitalDischargeStudiesSummarySection(
            [organizer], title="Discharge Studies"
        )
        elem = section.to_element()

        # Verify section structure
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title").text == "Discharge Studies"
        assert elem.find(f"{{{NS}}}text") is not None
        assert elem.find(f"{{{NS}}}entry") is not None

        # Verify narrative
        tbody = elem.find(f".//{{{NS}}}tbody")
        rows = tbody.findall(f"{{{NS}}}tr")
        assert len(rows) == 1

        # Verify entry/organizer structure
        organizer_elem = elem.find(f".//{{{NS}}}organizer")
        assert organizer_elem is not None

        components = organizer_elem.findall(f"{{{NS}}}component")
        assert len(components) == 1

    def test_discharge_studies_section_lab_study(self):
        """Test HospitalDischargeStudiesSummarySection with laboratory study."""
        studies = [
            MockDischargeStudy(
                study_name="Hemoglobin A1c",
                study_code="4548-4",
                value="6.5",
                unit="%",
                status="final",
                effective_time=date(2023, 10, 15),
                interpretation="Normal",
                reference_range_low="4.0",
                reference_range_high="5.6",
                reference_range_unit="%",
            ),
        ]
        organizer = MockDischargeStudyOrganizer(
            study_panel_name="Discharge Labs",
            study_panel_code="58410-2",
            status="completed",
            effective_time=datetime(2023, 10, 15, 8, 0),
            studies=studies,
        )
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        # Verify narrative
        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        # Check value
        assert cells[2].text == "6.5"

        # Check unit
        assert cells[3].text == "%"

        # Check reference range
        range_text = cells[5].text
        assert "4.0" in range_text
        assert "5.6" in range_text
        assert "%" in range_text

    def test_discharge_studies_section_procedure_study(self):
        """Test HospitalDischargeStudiesSummarySection with procedure observation."""
        studies = [
            MockDischargeStudy(
                study_name="Echocardiogram - Left ventricular ejection fraction",
                study_code="10230-1",
                value="55",
                unit="%",
                status="final",
                effective_time=date(2023, 10, 15),
                interpretation="Normal",
                reference_range_low="50",
                reference_range_high="70",
                reference_range_unit="%",
            ),
        ]
        organizer = MockDischargeStudyOrganizer(
            study_panel_name="Cardiac Studies",
            study_panel_code="34752-6",
            status="completed",
            effective_time=datetime(2023, 10, 15, 11, 15),
            studies=studies,
        )
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        # Verify narrative
        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")

        study_content = row.find(f".//{{{NS}}}content[@ID='discharge-study-1-1']")
        assert (
            study_content.text == "Echocardiogram - Left ventricular ejection fraction"
        )

    def test_discharge_studies_section_complete(self):
        """Test HospitalDischargeStudiesSummarySection with complete data."""
        studies = [
            MockDischargeStudy(
                study_name="Chest X-Ray",
                study_code="36643-5",
                value="Normal heart size",
                unit=None,
                status="final",
                effective_time=date(2023, 10, 15),
                interpretation="Normal",
            ),
            MockDischargeStudy(
                study_name="Hemoglobin",
                study_code="718-7",
                value="14.5",
                unit="g/dL",
                status="final",
                effective_time=date(2023, 10, 15),
                interpretation="Normal",
                reference_range_low="12",
                reference_range_high="16",
                reference_range_unit="g/dL",
            ),
        ]
        organizer = MockDischargeStudyOrganizer(
            study_panel_name="Discharge Studies Panel",
            study_panel_code="11493-4",
            status="completed",
            effective_time=datetime(2023, 10, 15, 10, 30),
            studies=studies,
        )
        section = HospitalDischargeStudiesSummarySection(
            [organizer], title="Discharge Studies"
        )
        elem = section.to_element()

        # Verify section structure
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title").text == "Discharge Studies"
        assert elem.find(f"{{{NS}}}text") is not None
        assert elem.find(f"{{{NS}}}entry") is not None

        # Verify narrative
        tbody = elem.find(f".//{{{NS}}}tbody")
        rows = tbody.findall(f"{{{NS}}}tr")
        assert len(rows) == 2

        # Verify entry/organizer structure
        organizer_elem = elem.find(f".//{{{NS}}}organizer")
        assert organizer_elem is not None

        components = organizer_elem.findall(f"{{{NS}}}component")
        assert len(components) == 2

    def test_discharge_studies_section_narrative_with_only_high_reference(self):
        """Test HospitalDischargeStudiesSummarySection narrative with only high reference range."""
        studies = [
            MockDischargeStudy(
                study_name="Creatinine",
                study_code="2160-0",
                value="1.5",
                unit="mg/dL",
                reference_range_low=None,
                reference_range_high="1.2",
                reference_range_unit="mg/dL",
            )
        ]
        organizer = MockDischargeStudyOrganizer(studies=studies)
        section = HospitalDischargeStudiesSummarySection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        # Reference range should show "< high" format (index 5)
        range_cell = cells[5]
        assert "< 1.2" in range_cell.text
        assert "mg/dL" in range_cell.text
