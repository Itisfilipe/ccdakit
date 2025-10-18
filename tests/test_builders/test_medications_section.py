"""Tests for MedicationsSection builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.medications import MedicationsSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockMedication:
    """Mock medication for testing."""

    def __init__(
        self,
        name="Lisinopril 10mg oral tablet",
        code="314076",
        dosage="10 mg",
        route="oral",
        frequency="once daily",
        start_date=date(2023, 1, 1),
        end_date=None,
        status="active",
        instructions=None,
    ):
        self._name = name
        self._code = code
        self._dosage = dosage
        self._route = route
        self._frequency = frequency
        self._start_date = start_date
        self._end_date = end_date
        self._status = status
        self._instructions = instructions

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def dosage(self):
        return self._dosage

    @property
    def route(self):
        return self._route

    @property
    def frequency(self):
        return self._frequency

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def status(self):
        return self._status

    @property
    def instructions(self):
        return self._instructions


class TestMedicationsSection:
    """Tests for MedicationsSection builder."""

    def test_medications_section_basic(self):
        """Test basic MedicationsSection creation."""
        medication = MockMedication()
        section = MedicationsSection([medication])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_medications_section_has_template_id_r21(self):
        """Test MedicationsSection includes R2.1 template ID."""
        medication = MockMedication()
        section = MedicationsSection([medication], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.1.1"
        assert template.get("extension") == "2014-06-09"

    def test_medications_section_has_template_id_r20(self):
        """Test MedicationsSection includes R2.0 template ID."""
        medication = MockMedication()
        section = MedicationsSection([medication], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.1.1"
        assert template.get("extension") == "2014-06-09"

    def test_medications_section_has_code(self):
        """Test MedicationsSection includes section code."""
        medication = MockMedication()
        section = MedicationsSection([medication])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "10160-0"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "History of Medication use Narrative"

    def test_medications_section_has_title(self):
        """Test MedicationsSection includes title."""
        medication = MockMedication()
        section = MedicationsSection([medication], title="My Medications")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Medications"

    def test_medications_section_default_title(self):
        """Test MedicationsSection uses default title."""
        medication = MockMedication()
        section = MedicationsSection([medication])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Medications"

    def test_medications_section_has_narrative(self):
        """Test MedicationsSection includes narrative text."""
        medication = MockMedication()
        section = MedicationsSection([medication])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_medications_section_narrative_table(self):
        """Test narrative includes HTML table."""
        medication = MockMedication(
            name="Lisinopril 10mg",
            dosage="10 mg",
            route="oral",
            frequency="once daily",
            start_date=date(2023, 1, 1),
        )
        section = MedicationsSection([medication])
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
        assert len(ths) == 7  # Medication, Dosage, Route, Frequency, Start, End, Status

    def test_medications_section_narrative_content(self):
        """Test narrative contains medication data."""
        medication = MockMedication(
            name="Metformin 500mg",
            code="860975",
            dosage="500 mg",
            route="oral",
            frequency="twice daily",
            start_date=date(2023, 1, 15),
            status="active",
        )
        section = MedicationsSection([medication])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 7

        # Check medication name with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Metformin 500mg"
        assert content.get("ID") == "medication-1"

        # Check dosage
        assert tds[1].text == "500 mg"

        # Check route
        assert tds[2].text == "Oral"

        # Check frequency
        assert tds[3].text == "twice daily"

        # Check start date
        assert tds[4].text == "2023-01-15"

        # Check end date (should show "Ongoing" for active)
        assert tds[5].text == "Ongoing"

        # Check status
        assert tds[6].text == "Active"

    def test_medications_section_narrative_multiple_medications(self):
        """Test narrative with multiple medications."""
        medications = [
            MockMedication(name="Lisinopril 10mg", code="314076"),
            MockMedication(name="Metformin 500mg", code="860975"),
            MockMedication(name="Atorvastatin 20mg", code="617310"),
        ]
        section = MedicationsSection(medications)
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

        assert content1.get("ID") == "medication-1"
        assert content2.get("ID") == "medication-2"
        assert content3.get("ID") == "medication-3"

    def test_medications_section_narrative_completed_medication(self):
        """Test narrative shows end date for completed medications."""
        medication = MockMedication(
            name="Amoxicillin 500mg",
            code="308191",
            status="completed",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 1, 14),
        )
        section = MedicationsSection([medication])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check status
        assert tds[6].text == "Completed"

        # Check end date
        assert tds[5].text == "2023-01-14"

    def test_medications_section_empty_narrative(self):
        """Test narrative when no medications."""
        section = MedicationsSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No known medications"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_medications_section_has_entries(self):
        """Test MedicationsSection includes entry elements."""
        medication = MockMedication()
        section = MedicationsSection([medication])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1
        assert entries[0].get("typeCode") == "DRIV"

    def test_medications_section_entry_has_substance_administration(self):
        """Test entry contains substanceAdministration element."""
        medication = MockMedication()
        section = MedicationsSection([medication])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        sub_admin = entry.find(f"{{{NS}}}substanceAdministration")
        assert sub_admin is not None
        assert sub_admin.get("classCode") == "SBADM"

    def test_medications_section_multiple_entries(self):
        """Test MedicationsSection with multiple medications."""
        medications = [
            MockMedication(name="Lisinopril 10mg", code="314076"),
            MockMedication(name="Metformin 500mg", code="860975"),
        ]
        section = MedicationsSection(medications)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has a substanceAdministration
        for entry in entries:
            sub_admin = entry.find(f"{{{NS}}}substanceAdministration")
            assert sub_admin is not None

    def test_medications_section_to_string(self):
        """Test MedicationsSection serialization."""
        medication = MockMedication()
        section = MedicationsSection([medication])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "10160-0" in xml  # Section code
        assert "Medication" in xml

    def test_medications_section_structure_order(self):
        """Test that section elements are in correct order."""
        medication = MockMedication()
        section = MedicationsSection([medication])
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


class TestMedicationsSectionIntegration:
    """Integration tests for MedicationsSection."""

    def test_complete_medications_section(self):
        """Test creating a complete medications section."""
        medications = [
            MockMedication(
                name="Lisinopril 10mg oral tablet",
                code="314076",
                dosage="10 mg",
                route="oral",
                frequency="once daily",
                start_date=date(2023, 1, 1),
                status="active",
            ),
            MockMedication(
                name="Metformin 500mg oral tablet",
                code="860975",
                dosage="500 mg",
                route="oral",
                frequency="twice daily",
                start_date=date(2023, 2, 15),
                status="active",
            ),
            MockMedication(
                name="Amoxicillin 500mg oral capsule",
                code="308191",
                dosage="500 mg",
                route="oral",
                frequency="three times daily",
                start_date=date(2023, 11, 1),
                end_date=date(2023, 11, 14),
                status="completed",
            ),
        ]

        section = MedicationsSection(medications, title="Current Medications")
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

        medication = MockMedication()
        section = MedicationsSection([medication])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None
