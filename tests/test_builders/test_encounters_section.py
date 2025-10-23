"""Tests for EncountersSection builder."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.sections.encounters import EncountersSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockEncounter:
    """Mock encounter for testing."""

    def __init__(
        self,
        encounter_type="Office Visit",
        code="99213",
        code_system="CPT-4",
        date=date(2023, 5, 15),
        end_date=None,
        location=None,
        performer_name=None,
        discharge_disposition=None,
    ):
        self._encounter_type = encounter_type
        self._code = code
        self._code_system = code_system
        self._date = date
        self._end_date = end_date
        self._location = location
        self._performer_name = performer_name
        self._discharge_disposition = discharge_disposition

    @property
    def encounter_type(self):
        return self._encounter_type

    @property
    def code(self):
        return self._code

    @property
    def code_system(self):
        return self._code_system

    @property
    def date(self):
        return self._date

    @property
    def end_date(self):
        return self._end_date

    @property
    def location(self):
        return self._location

    @property
    def performer_name(self):
        return self._performer_name

    @property
    def discharge_disposition(self):
        return self._discharge_disposition


class TestEncountersSection:
    """Tests for EncountersSection builder."""

    def test_encounters_section_basic(self):
        """Test basic EncountersSection creation."""
        encounter = MockEncounter()
        section = EncountersSection([encounter])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_encounters_section_has_template_id_r21(self):
        """Test EncountersSection includes R2.1 template ID."""
        encounter = MockEncounter()
        section = EncountersSection([encounter], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.22.1"
        assert template.get("extension") == "2015-08-01"

    def test_encounters_section_has_template_id_r20(self):
        """Test EncountersSection includes R2.0 template ID."""
        encounter = MockEncounter()
        section = EncountersSection([encounter], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.22.1"
        assert template.get("extension") == "2014-06-09"

    def test_encounters_section_has_code(self):
        """Test EncountersSection includes section code."""
        encounter = MockEncounter()
        section = EncountersSection([encounter])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "46240-8"  # Encounters
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC

    def test_encounters_section_has_title(self):
        """Test EncountersSection includes title."""
        encounter = MockEncounter()
        section = EncountersSection([encounter], title="My Encounters")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Encounters"

    def test_encounters_section_default_title(self):
        """Test EncountersSection uses default title."""
        encounter = MockEncounter()
        section = EncountersSection([encounter])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Encounters"

    def test_encounters_section_has_narrative(self):
        """Test EncountersSection includes narrative text."""
        encounter = MockEncounter()
        section = EncountersSection([encounter])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_encounters_section_narrative_table(self):
        """Test narrative includes HTML table."""
        encounter = MockEncounter(
            encounter_type="Emergency Department Visit",
            code="99285",
        )
        section = EncountersSection([encounter])
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
        assert (
            len(ths) == 6
        )  # Encounter Type, Code, Date, Location, Performer, Discharge Disposition

    def test_encounters_section_empty_narrative(self):
        """Test narrative when no encounters."""
        section = EncountersSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No encounters recorded"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_encounters_section_has_entries(self):
        """Test EncountersSection includes entry elements."""
        encounter = MockEncounter()
        section = EncountersSection([encounter])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1
        assert entries[0].get("typeCode") == "DRIV"

    def test_encounters_section_entry_has_encounter(self):
        """Test entry contains encounter element."""
        encounter = MockEncounter()
        section = EncountersSection([encounter])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        enc = entry.find(f"{{{NS}}}encounter")
        assert enc is not None
        assert enc.get("classCode") == "ENC"

    def test_encounters_section_multiple_entries(self):
        """Test EncountersSection with multiple encounters."""
        encounters = [
            MockEncounter(encounter_type="Office Visit", code="99213"),
            MockEncounter(encounter_type="Emergency Visit", code="99285"),
        ]
        section = EncountersSection(encounters)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_encounters_section_narrative_with_location(self):
        """Test narrative includes location information."""
        encounter = MockEncounter(
            encounter_type="Hospital Visit",
            location="Memorial Hospital",
        )
        section = EncountersSection([encounter])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Location should be in the 4th column (index 3)
        assert tds[3].text == "Memorial Hospital"

    def test_encounters_section_narrative_with_performer(self):
        """Test narrative includes performer information."""
        encounter = MockEncounter(
            encounter_type="Office Visit",
            performer_name="Dr. John Smith",
        )
        section = EncountersSection([encounter])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Performer should be in the 5th column (index 4)
        assert tds[4].text == "Dr. John Smith"

    def test_encounters_section_narrative_with_discharge(self):
        """Test narrative includes discharge disposition."""
        encounter = MockEncounter(
            encounter_type="Inpatient Admission",
            discharge_disposition="Home",
        )
        section = EncountersSection([encounter])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Discharge disposition should be in the 6th column (index 5)
        assert tds[5].text == "Home"

    def test_encounters_section_narrative_date_formatting(self):
        """Test date formatting in narrative."""
        encounter = MockEncounter(
            encounter_type="Office Visit",
            date=date(2023, 5, 15),
        )
        section = EncountersSection([encounter])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Date should be in the 3rd column (index 2)
        assert tds[2].text == "2023-05-15"

    def test_encounters_section_narrative_datetime_formatting(self):
        """Test datetime formatting in narrative."""
        encounter = MockEncounter(
            encounter_type="Emergency Visit",
            date=datetime(2023, 5, 15, 14, 30),
        )
        section = EncountersSection([encounter])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # DateTime should include time
        assert tds[2].text == "2023-05-15 14:30"

    def test_encounters_section_narrative_date_range(self):
        """Test date range formatting in narrative."""
        encounter = MockEncounter(
            encounter_type="Inpatient Admission",
            date=date(2023, 5, 15),
            end_date=date(2023, 5, 18),
        )
        section = EncountersSection([encounter])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Should show date range
        assert tds[2].text == "2023-05-15 to 2023-05-18"

    def test_encounters_section_to_string(self):
        """Test EncountersSection serialization."""
        encounter = MockEncounter()
        section = EncountersSection([encounter])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "46240-8" in xml  # Section code

    def test_encounters_section_structure_order(self):
        """Test that section elements are in correct order."""
        encounter = MockEncounter()
        section = EncountersSection([encounter])
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


class TestEncountersSectionIntegration:
    """Integration tests for EncountersSection."""

    def test_complete_encounters_section(self):
        """Test creating a complete encounters section."""
        encounters = [
            MockEncounter(
                encounter_type="Office Visit",
                code="99213",
                code_system="CPT-4",
                date=date(2023, 3, 10),
                location="Primary Care Clinic",
                performer_name="Dr. Jane Smith",
            ),
            MockEncounter(
                encounter_type="Inpatient Hospital Admission",
                code="32485007",
                code_system="SNOMED CT",
                date=datetime(2023, 5, 15, 9, 0),
                end_date=datetime(2023, 5, 18, 11, 30),
                location="Memorial Hospital",
                performer_name="Dr. John Surgeon",
                discharge_disposition="Home",
            ),
        ]

        section = EncountersSection(encounters, title="Patient Encounter History")
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify narrative table has 2 rows
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 2

        # Verify 2 entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_outpatient_encounters_section(self):
        """Test section with only outpatient encounters."""
        encounters = [
            MockEncounter(
                encounter_type="Office Visit",
                code="99213",
                code_system="CPT-4",
                date=date(2023, 1, 15),
                location="Primary Care",
                performer_name="Dr. Smith",
            ),
            MockEncounter(
                encounter_type="Outpatient Consultation",
                code="99245",
                code_system="CPT-4",
                date=date(2023, 3, 20),
                location="Specialist Clinic",
                performer_name="Dr. Jones",
            ),
        ]

        section = EncountersSection(encounters)
        elem = section.to_element()

        # Verify all entries are present
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Verify no discharge dispositions (outpatient only)
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")

        for tr in tbody.findall(f"{{{NS}}}tr"):
            tds = tr.findall(f"{{{NS}}}td")
            # Discharge disposition column should be "-"
            assert tds[5].text == "-"

    def test_mixed_encounter_types_section(self):
        """Test section with mixed encounter types."""
        encounters = [
            MockEncounter(
                encounter_type="Emergency Department Visit",
                code="99285",
                code_system="CPT-4",
                date=datetime(2023, 2, 10, 3, 45),
                end_date=datetime(2023, 2, 10, 8, 20),
                location="County General ER",
                performer_name="Dr. Wilson",
            ),
            MockEncounter(
                encounter_type="Office Visit",
                code="99213",
                code_system="CPT-4",
                date=date(2023, 3, 15),
                location="Primary Care",
                performer_name="Dr. Smith",
            ),
            MockEncounter(
                encounter_type="Hospital Inpatient",
                code="32485007",
                code_system="SNOMED CT",
                date=date(2023, 4, 1),
                end_date=date(2023, 4, 5),
                location="Memorial Hospital",
                performer_name="Dr. Johnson",
                discharge_disposition="Skilled Nursing Facility",
            ),
        ]

        section = EncountersSection(encounters)
        elem = section.to_element()

        # Verify all 3 encounters
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 3

        # Verify narrative has all 3 rows
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 3

    def test_minimal_encounters_section(self):
        """Test section with minimal encounter data."""
        encounters = [
            MockEncounter(
                encounter_type="Office Visit",
                code="99213",
                code_system="CPT-4",
                date=date(2023, 5, 15),
            ),
        ]

        section = EncountersSection(encounters)
        elem = section.to_element()

        # Verify required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None
        assert elem.find(f"{{{NS}}}entry") is not None

        # Verify narrative shows "-" for missing optional fields
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        assert tds[3].text == "-"  # No location
        assert tds[4].text == "-"  # No performer
        assert tds[5].text == "-"  # No discharge disposition

    def test_encounters_section_narrative_no_date(self):
        """Test narrative with no encounter date."""
        encounter = MockEncounter(
            encounter_type="Office Visit",
            code="99213",
            code_system="CPT-4",
            date=None,
        )
        section = EncountersSection([encounter])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Date column should show "Unknown" when date is None
        assert tds[2].text == "Unknown"
