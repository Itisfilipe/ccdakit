"""Tests for DischargeMedicationsSection builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.discharge_medications import DischargeMedicationsSection
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


class TestDischargeMedicationsSection:
    """Tests for DischargeMedicationsSection builder."""

    def test_discharge_medications_section_basic(self):
        """Test basic DischargeMedicationsSection creation."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_discharge_medications_section_has_template_id_r21(self):
        """Test DischargeMedicationsSection includes R2.1 template ID."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication], version=CDAVersion.R2_1)
        elem = section.to_element()

        # CONF:1198-7822, CONF:1198-10397, CONF:1198-32562
        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.11.1"
        assert template.get("extension") == "2015-08-01"

    def test_discharge_medications_section_has_template_id_r20(self):
        """Test DischargeMedicationsSection includes R2.0 template ID."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.11.1"
        assert template.get("extension") == "2015-08-01"

    def test_discharge_medications_section_has_code(self):
        """Test DischargeMedicationsSection includes section code."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        # CONF:1198-15361, CONF:1198-15362, CONF:1198-32145
        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "10183-2"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Hospital Discharge Medications"

    def test_discharge_medications_section_code_has_translation(self):
        """Test section code includes required translation."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        # CONF:1198-32857, CONF:1198-32858, CONF:1198-32859
        code = elem.find(f"{{{NS}}}code")
        translation = code.find(f"{{{NS}}}translation")
        assert translation is not None
        assert translation.get("code") == "75311-1"
        assert translation.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert translation.get("displayName") == "Discharge Medications"

    def test_discharge_medications_section_has_title(self):
        """Test DischargeMedicationsSection includes title."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication], title="My Discharge Meds")
        elem = section.to_element()

        # CONF:1198-7824
        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Discharge Meds"

    def test_discharge_medications_section_default_title(self):
        """Test DischargeMedicationsSection uses default title."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Discharge Medications"

    def test_discharge_medications_section_has_narrative(self):
        """Test DischargeMedicationsSection includes narrative text."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        # CONF:1198-7825
        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_discharge_medications_section_narrative_table(self):
        """Test narrative includes HTML table."""
        medication = MockMedication(
            name="Lisinopril 10mg",
            dosage="10 mg",
            route="oral",
            frequency="once daily",
            start_date=date(2023, 1, 1),
        )
        section = DischargeMedicationsSection([medication])
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
        # Medication, Dosage, Route, Frequency, Start Date, End Date, Status, Instructions
        assert len(ths) == 8

    def test_discharge_medications_section_narrative_content(self):
        """Test narrative contains medication data."""
        medication = MockMedication(
            name="Metformin 500mg",
            code="860975",
            dosage="500 mg",
            route="oral",
            frequency="twice daily",
            start_date=date(2023, 1, 15),
            status="active",
            instructions="Take with food",
        )
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 8

        # Check medication name with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Metformin 500mg"
        assert content.get("ID") == "discharge-medication-1"

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

        # Check instructions
        assert tds[7].text == "Take with food"

    def test_discharge_medications_section_narrative_no_instructions(self):
        """Test narrative shows dash when no instructions."""
        medication = MockMedication(instructions=None)
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check instructions column shows dash
        assert tds[7].text == "-"

    def test_discharge_medications_section_narrative_multiple_medications(self):
        """Test narrative with multiple medications."""
        medications = [
            MockMedication(name="Lisinopril 10mg", code="314076"),
            MockMedication(name="Metformin 500mg", code="860975"),
            MockMedication(name="Atorvastatin 20mg", code="617310"),
        ]
        section = DischargeMedicationsSection(medications)
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

        assert content1.get("ID") == "discharge-medication-1"
        assert content2.get("ID") == "discharge-medication-2"
        assert content3.get("ID") == "discharge-medication-3"

    def test_discharge_medications_section_narrative_completed_medication(self):
        """Test narrative shows end date for completed medications."""
        medication = MockMedication(
            name="Amoxicillin 500mg",
            code="308191",
            status="completed",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 1, 14),
        )
        section = DischargeMedicationsSection([medication])
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

    def test_discharge_medications_section_empty_narrative(self):
        """Test narrative when no medications."""
        section = DischargeMedicationsSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No discharge medications"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_discharge_medications_section_has_entries(self):
        """Test DischargeMedicationsSection includes entry elements."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        # CONF:1198-7826
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_discharge_medications_section_entry_has_act(self):
        """Test entry contains act element."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        # CONF:1198-15491
        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"
        assert act.get("moodCode") == "EVN"

    def test_discharge_medications_section_entry_has_medication_activity(self):
        """Test entry contains Medication Activity."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is not None

        sub_admin = entry_rel.find(f"{{{NS}}}substanceAdministration")
        assert sub_admin is not None
        assert sub_admin.get("classCode") == "SBADM"

    def test_discharge_medications_section_multiple_entries(self):
        """Test DischargeMedicationsSection with multiple medications."""
        medications = [
            MockMedication(name="Lisinopril 10mg", code="314076"),
            MockMedication(name="Metformin 500mg", code="860975"),
        ]
        section = DischargeMedicationsSection(medications)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an act with Discharge Medication structure
        for entry in entries:
            act = entry.find(f"{{{NS}}}act")
            assert act is not None

            # Check for code element
            code = act.find(f"{{{NS}}}code")
            assert code is not None
            assert code.get("code") == "10183-2"

            # Check for statusCode
            status = act.find(f"{{{NS}}}statusCode")
            assert status is not None
            assert status.get("code") == "completed"

    def test_discharge_medications_section_null_flavor(self):
        """Test DischargeMedicationsSection with null flavor."""
        section = DischargeMedicationsSection([], null_flavor="NI")
        elem = section.to_element()

        # CONF:1198-32812
        assert elem.get("nullFlavor") == "NI"

        # Should have no entries when null flavor is present
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_discharge_medications_section_null_flavor_narrative(self):
        """Test narrative with null flavor."""
        section = DischargeMedicationsSection([], null_flavor="NI")
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert "No information available" in paragraph.text

    def test_discharge_medications_section_to_string(self):
        """Test DischargeMedicationsSection serialization."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "10183-2" in xml  # Section code
        assert "75311-1" in xml  # Translation code
        assert "Discharge Medication" in xml

    def test_discharge_medications_section_structure_order(self):
        """Test that section elements are in correct order."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
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

    def test_discharge_medication_act_code(self):
        """Test Discharge Medication act has correct code."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")

        # CONF:1198-7691, CONF:1198-19161, CONF:1198-32159
        code = act.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "10183-2"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert code.get("displayName") == "Hospital discharge medication"

    def test_discharge_medication_act_code_translation(self):
        """Test Discharge Medication act code has required translation."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        code = act.find(f"{{{NS}}}code")

        # CONF:1198-32952, CONF:1198-32953, CONF:1198-32954
        translation = code.find(f"{{{NS}}}translation")
        assert translation is not None
        assert translation.get("code") == "75311-1"
        assert translation.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert translation.get("displayName") == "Discharge Medication"

    def test_discharge_medication_act_status_code(self):
        """Test Discharge Medication act has completed status."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")

        # CONF:1198-32779, CONF:1198-32780
        status = act.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_discharge_medication_act_entry_relationship(self):
        """Test Discharge Medication act has entryRelationship."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")

        # CONF:1198-7692, CONF:1198-7693
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "SUBJ"

    def test_discharge_medication_template_id(self):
        """Test Discharge Medication has correct template ID."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication], version=CDAVersion.R2_1)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")

        # CONF:1198-16760, CONF:1198-16761, CONF:1198-32513
        template = act.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.35"
        assert template.get("extension") == "2016-03-01"


class TestDischargeMedicationsSectionIntegration:
    """Integration tests for DischargeMedicationsSection."""

    def test_complete_discharge_medications_section(self):
        """Test creating a complete discharge medications section."""
        medications = [
            MockMedication(
                name="Lisinopril 10mg oral tablet",
                code="314076",
                dosage="10 mg",
                route="oral",
                frequency="once daily",
                start_date=date(2023, 12, 1),
                status="active",
                instructions="Take in the morning",
            ),
            MockMedication(
                name="Metformin 500mg oral tablet",
                code="860975",
                dosage="500 mg",
                route="oral",
                frequency="twice daily",
                start_date=date(2023, 12, 1),
                status="active",
                instructions="Take with meals",
            ),
            MockMedication(
                name="Amoxicillin 500mg oral capsule",
                code="308191",
                dosage="500 mg",
                route="oral",
                frequency="three times daily",
                start_date=date(2023, 12, 1),
                end_date=date(2023, 12, 10),
                status="completed",
                instructions="Complete full course",
            ),
        ]

        section = DischargeMedicationsSection(
            medications, title="Discharge Medications"
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

        # Verify each entry has proper Discharge Medication structure
        for entry in entries:
            act = entry.find(f"{{{NS}}}act")
            assert act is not None

            # Check template ID
            template = act.find(f"{{{NS}}}templateId")
            assert template.get("root") == "2.16.840.1.113883.10.20.22.4.35"

            # Check code
            code = act.find(f"{{{NS}}}code")
            assert code.get("code") == "10183-2"

            # Check translation
            translation = code.find(f"{{{NS}}}translation")
            assert translation.get("code") == "75311-1"

            # Check status
            status = act.find(f"{{{NS}}}statusCode")
            assert status.get("code") == "completed"

            # Check entryRelationship with Medication Activity
            entry_rel = act.find(f"{{{NS}}}entryRelationship")
            assert entry_rel.get("typeCode") == "SUBJ"

            sub_admin = entry_rel.find(f"{{{NS}}}substanceAdministration")
            assert sub_admin is not None

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        medication = MockMedication()
        section = DischargeMedicationsSection([medication])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_with_various_medication_statuses(self):
        """Test section with different medication statuses."""
        medications = [
            MockMedication(
                name="Active Med",
                code="123",
                status="active",
                end_date=None,
            ),
            MockMedication(
                name="Completed Med",
                code="456",
                status="completed",
                end_date=date(2023, 12, 1),
            ),
            MockMedication(
                name="Discontinued Med",
                code="789",
                status="discontinued",
                end_date=date(2023, 11, 15),
            ),
        ]

        section = DischargeMedicationsSection(medications)
        elem = section.to_element()

        # Check narrative shows different statuses correctly
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        # Check status column for each row
        assert trs[0].findall(f"{{{NS}}}td")[6].text == "Active"
        assert trs[1].findall(f"{{{NS}}}td")[6].text == "Completed"
        assert trs[2].findall(f"{{{NS}}}td")[6].text == "Discontinued"

        # Check end date column
        assert trs[0].findall(f"{{{NS}}}td")[5].text == "Ongoing"
        assert trs[1].findall(f"{{{NS}}}td")[5].text == "2023-12-01"
        assert trs[2].findall(f"{{{NS}}}td")[5].text == "2023-11-15"

    def test_r20_version_support(self):
        """Test section works with R2.0 version."""
        medication = MockMedication()
        section = DischargeMedicationsSection([medication], version=CDAVersion.R2_0)
        elem = section.to_element()

        # Check section template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.11.1"
        assert template.get("extension") == "2015-08-01"

        # Check entry act template ID
        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        act_template = act.find(f"{{{NS}}}templateId")
        assert act_template.get("root") == "2.16.840.1.113883.10.20.22.4.35"
        assert act_template.get("extension") == "2016-03-01"

    def test_empty_section_without_null_flavor(self):
        """Test empty section without null flavor still has required elements."""
        section = DischargeMedicationsSection([])
        elem = section.to_element()

        # Should have all required elements
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Should have no entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

        # Narrative should explain no medications
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
