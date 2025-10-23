"""Tests for Results Section builder."""

from datetime import date, datetime
from typing import Sequence

from lxml import etree

from ccdakit.builders.sections.results import ResultsSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockResult:
    """Mock result observation for testing."""

    def __init__(
        self,
        test_name="Glucose",
        test_code="2345-7",
        value="95",
        unit="mg/dL",
        status="completed",
        effective_time=date(2023, 10, 1),
        value_type=None,
        interpretation=None,
        reference_range_low=None,
        reference_range_high=None,
        reference_range_unit=None,
    ):
        self._test_name = test_name
        self._test_code = test_code
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
    def test_name(self):
        return self._test_name

    @property
    def test_code(self):
        return self._test_code

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


class MockResultOrganizer:
    """Mock result organizer for testing."""

    def __init__(
        self,
        panel_name="Complete Blood Count",
        panel_code="58410-2",
        status="completed",
        effective_time=datetime(2023, 10, 1, 10, 30),
        results=None,
    ):
        self._panel_name = panel_name
        self._panel_code = panel_code
        self._status = status
        self._effective_time = effective_time
        self._results = results or []

    @property
    def panel_name(self) -> str:
        return self._panel_name

    @property
    def panel_code(self) -> str:
        return self._panel_code

    @property
    def status(self) -> str:
        return self._status

    @property
    def effective_time(self) -> datetime:
        return self._effective_time

    @property
    def results(self) -> Sequence[MockResult]:
        return self._results


class TestResultsSection:
    """Tests for ResultsSection builder."""

    def test_results_section_basic(self):
        """Test basic ResultsSection creation."""
        results = [MockResult()]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_results_section_has_template_id_r21(self):
        """Test ResultsSection includes R2.1 template ID."""
        results = [MockResult()]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.3.1"
        assert template.get("extension") == "2015-08-01"

    def test_results_section_has_template_id_r20(self):
        """Test ResultsSection includes R2.0 template ID."""
        results = [MockResult()]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.3.1"
        assert template.get("extension") == "2015-08-01"

    def test_results_section_has_code(self):
        """Test ResultsSection includes section code."""
        results = [MockResult()]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "30954-2"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Relevant diagnostic tests and/or laboratory data"

    def test_results_section_has_title(self):
        """Test ResultsSection includes title."""
        results = [MockResult()]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer], title="Lab Results")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Lab Results"

    def test_results_section_default_title(self):
        """Test ResultsSection uses default title."""
        results = [MockResult()]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Results"

    def test_results_section_has_narrative(self):
        """Test ResultsSection includes narrative text."""
        results = [MockResult()]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_results_section_narrative_has_table(self):
        """Test ResultsSection narrative includes table."""
        results = [MockResult()]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        table = elem.find(f".//{{{NS}}}table")
        assert table is not None
        assert table.get("border") == "1"
        assert table.get("width") == "100%"

    def test_results_section_narrative_table_headers(self):
        """Test ResultsSection narrative table has correct headers."""
        results = [MockResult()]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        thead = elem.find(f".//{{{NS}}}thead")
        assert thead is not None

        headers = thead.findall(f".//{{{NS}}}th")
        header_texts = [h.text for h in headers]
        expected_headers = [
            "Panel",
            "Test",
            "Value",
            "Unit",
            "Interpretation",
            "Reference Range",
            "Date",
        ]
        assert header_texts == expected_headers

    def test_results_section_narrative_with_single_result(self):
        """Test ResultsSection narrative with a single result."""
        results = [
            MockResult(
                test_name="Glucose",
                value="95",
                unit="mg/dL",
                interpretation="Normal",
            )
        ]
        organizer = MockResultOrganizer(
            panel_name="Metabolic Panel",
            effective_time=datetime(2023, 10, 15, 10, 30),
            results=results,
        )
        section = ResultsSection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        rows = tbody.findall(f"{{{NS}}}tr")
        assert len(rows) == 1

        # Check panel name
        panel_content = rows[0].find(f".//{{{NS}}}content[@ID='result-panel-1']")
        assert panel_content is not None
        assert panel_content.text == "Metabolic Panel"

        # Check test name
        test_content = rows[0].find(f".//{{{NS}}}content[@ID='result-1-1']")
        assert test_content is not None
        assert test_content.text == "Glucose"

    def test_results_section_narrative_with_multiple_results_in_panel(self):
        """Test ResultsSection narrative with multiple results in one panel."""
        results = [
            MockResult(test_name="Glucose", value="95", unit="mg/dL"),
            MockResult(test_name="Hemoglobin", value="14.5", unit="g/dL"),
        ]
        organizer = MockResultOrganizer(
            panel_name="Complete Blood Count",
            results=results,
        )
        section = ResultsSection([organizer])
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

    def test_results_section_narrative_with_multiple_panels(self):
        """Test ResultsSection narrative with multiple panels."""
        organizer1 = MockResultOrganizer(
            panel_name="Metabolic Panel",
            results=[MockResult(test_name="Glucose", value="95", unit="mg/dL")],
        )
        organizer2 = MockResultOrganizer(
            panel_name="Lipid Panel",
            results=[MockResult(test_name="Cholesterol", value="180", unit="mg/dL")],
        )
        section = ResultsSection([organizer1, organizer2])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        rows = tbody.findall(f"{{{NS}}}tr")
        assert len(rows) == 2

        # Check panel names
        panel1_content = rows[0].find(f".//{{{NS}}}content[@ID='result-panel-1']")
        assert panel1_content.text == "Metabolic Panel"

        panel2_content = rows[1].find(f".//{{{NS}}}content[@ID='result-panel-2']")
        assert panel2_content.text == "Lipid Panel"

    def test_results_section_narrative_with_interpretation(self):
        """Test ResultsSection narrative includes interpretation."""
        results = [
            MockResult(
                test_name="Glucose",
                value="150",
                unit="mg/dL",
                interpretation="High",
            )
        ]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        # Interpretation is the 5th column (index 4)
        interpretation_cell = cells[4]
        assert interpretation_cell.text == "High"

    def test_results_section_narrative_without_interpretation(self):
        """Test ResultsSection narrative with no interpretation shows dash."""
        results = [
            MockResult(
                test_name="Glucose",
                value="95",
                unit="mg/dL",
                interpretation=None,
            )
        ]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        interpretation_cell = cells[4]
        assert interpretation_cell.text == "-"

    def test_results_section_narrative_with_reference_range(self):
        """Test ResultsSection narrative includes reference range."""
        results = [
            MockResult(
                test_name="Glucose",
                value="95",
                unit="mg/dL",
                reference_range_low="70",
                reference_range_high="100",
                reference_range_unit="mg/dL",
            )
        ]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        # Reference range is the 6th column (index 5)
        range_cell = cells[5]
        assert "70" in range_cell.text
        assert "100" in range_cell.text
        assert "mg/dL" in range_cell.text

    def test_results_section_narrative_without_reference_range(self):
        """Test ResultsSection narrative with no reference range shows dash."""
        results = [
            MockResult(
                test_name="Glucose",
                value="95",
                unit="mg/dL",
                reference_range_low=None,
                reference_range_high=None,
            )
        ]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        range_cell = cells[5]
        assert range_cell.text == "-"

    def test_results_section_narrative_without_unit(self):
        """Test ResultsSection narrative with no unit shows dash."""
        results = [
            MockResult(
                test_name="Blood Type",
                value="A+",
                unit=None,
            )
        ]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        # Unit is the 4th column (index 3)
        unit_cell = cells[3]
        assert unit_cell.text == "-"

    def test_results_section_narrative_date_format(self):
        """Test ResultsSection narrative displays date correctly."""
        test_date = datetime(2023, 10, 15, 10, 30)
        results = [MockResult()]
        organizer = MockResultOrganizer(effective_time=test_date, results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        # Date is the 7th column (index 6)
        date_cell = cells[6]
        assert date_cell.text == "2023-10-15"

    def test_results_section_empty_results(self):
        """Test ResultsSection with no results."""
        section = ResultsSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No lab results available"

        # Should not have a table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_results_section_has_entries(self):
        """Test ResultsSection includes entry elements."""
        results = [MockResult()]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_results_section_entry_has_organizer(self):
        """Test ResultsSection entry contains organizer."""
        results = [MockResult()]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        assert entry is not None
        assert entry.get("typeCode") == "DRIV"

        organizer_elem = entry.find(f"{{{NS}}}organizer")
        assert organizer_elem is not None

    def test_results_section_multiple_organizers(self):
        """Test ResultsSection with multiple organizers."""
        organizer1 = MockResultOrganizer(
            panel_name="Panel 1",
            results=[MockResult()],
        )
        organizer2 = MockResultOrganizer(
            panel_name="Panel 2",
            results=[MockResult()],
        )
        section = ResultsSection([organizer1, organizer2])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_results_section_complete(self):
        """Test ResultsSection with complete data."""
        results = [
            MockResult(
                test_name="Glucose",
                test_code="2345-7",
                value="95",
                unit="mg/dL",
                status="completed",
                effective_time=date(2023, 10, 15),
                interpretation="Normal",
                reference_range_low="70",
                reference_range_high="100",
                reference_range_unit="mg/dL",
            ),
            MockResult(
                test_name="Hemoglobin",
                test_code="718-7",
                value="14.5",
                unit="g/dL",
                status="completed",
                effective_time=date(2023, 10, 15),
                interpretation="Normal",
                reference_range_low="12",
                reference_range_high="16",
                reference_range_unit="g/dL",
            ),
        ]
        organizer = MockResultOrganizer(
            panel_name="Complete Blood Count",
            panel_code="58410-2",
            status="completed",
            effective_time=datetime(2023, 10, 15, 10, 30),
            results=results,
        )
        section = ResultsSection([organizer], title="Lab Results")
        elem = section.to_element()

        # Verify section structure
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title").text == "Lab Results"
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

    def test_results_section_narrative_with_only_high_reference(self):
        """Test ResultsSection narrative with only high reference range."""
        results = [
            MockResult(
                test_name="Glucose",
                test_code="2345-7",
                value="250",
                unit="mg/dL",
                reference_range_low=None,
                reference_range_high="140",
                reference_range_unit="mg/dL",
            )
        ]
        organizer = MockResultOrganizer(results=results)
        section = ResultsSection([organizer])
        elem = section.to_element()

        tbody = elem.find(f".//{{{NS}}}tbody")
        row = tbody.find(f"{{{NS}}}tr")
        cells = row.findall(f"{{{NS}}}td")

        # Reference range should show "< high" format (index 5)
        range_cell = cells[5]
        assert "< 140" in range_cell.text
        assert "mg/dL" in range_cell.text
