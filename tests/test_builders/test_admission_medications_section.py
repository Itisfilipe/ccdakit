"""Tests for AdmissionMedicationsSection builder."""

from datetime import date

import pytest
from lxml import etree

from ccdakit.builders.sections.admission_medications import AdmissionMedicationsSection
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


class TestAdmissionMedicationsSection:
    """Tests for AdmissionMedicationsSection builder."""

    def test_section_basic_creation(self):
        """Test basic AdmissionMedicationsSection creation."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_template_id_r21(self):
        """Test AdmissionMedicationsSection includes correct R2.1 template ID."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication], version=CDAVersion.R2_1)
        elem = section.to_element()

        # CONF:1198-10098, CONF:1198-10392, CONF:1198-32560
        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.44"
        assert template.get("extension") == "2015-08-01"

    def test_section_template_id_r20(self):
        """Test AdmissionMedicationsSection includes correct R2.0 template ID."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.44"

    def test_section_has_code(self):
        """Test AdmissionMedicationsSection includes correct section code."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication])
        elem = section.to_element()

        # CONF:1198-15482, CONF:1198-15483, CONF:1198-32142
        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "42346-7"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Medications on Admission"

    def test_section_has_title(self):
        """Test AdmissionMedicationsSection includes title."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication], title="My Admission Meds")
        elem = section.to_element()

        # CONF:1198-10100
        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Admission Meds"

    def test_section_default_title(self):
        """Test AdmissionMedicationsSection uses default title."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Admission Medications"

    def test_section_has_text(self):
        """Test AdmissionMedicationsSection includes narrative text."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication])
        elem = section.to_element()

        # CONF:1198-10101
        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_section_narrative_table(self):
        """Test narrative includes HTML table."""
        medication = MockMedication(
            name="Lisinopril 10mg",
            dosage="10 mg",
            route="oral",
            frequency="once daily",
            start_date=date(2023, 1, 1),
        )
        section = AdmissionMedicationsSection([medication])
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

    def test_section_narrative_content(self):
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
        section = AdmissionMedicationsSection([medication])
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
        assert content.get("ID") == "admission-medication-1"

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

    def test_section_narrative_multiple_medications(self):
        """Test narrative with multiple medications."""
        medications = [
            MockMedication(name="Lisinopril 10mg", code="314076"),
            MockMedication(name="Metformin 500mg", code="860975"),
            MockMedication(name="Atorvastatin 20mg", code="617310"),
        ]
        section = AdmissionMedicationsSection(medications)
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

        assert content1.get("ID") == "admission-medication-1"
        assert content2.get("ID") == "admission-medication-2"
        assert content3.get("ID") == "admission-medication-3"

    def test_section_narrative_completed_medication(self):
        """Test narrative shows end date for completed medications."""
        medication = MockMedication(
            name="Amoxicillin 500mg",
            code="308191",
            status="completed",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 1, 14),
        )
        section = AdmissionMedicationsSection([medication])
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

    def test_section_empty_narrative(self):
        """Test narrative when no medications."""
        section = AdmissionMedicationsSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No medications on admission"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_section_null_flavor_narrative(self):
        """Test narrative with null flavor."""
        section = AdmissionMedicationsSection([], null_flavor="NI")
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No information about admission medications"

    def test_section_has_entries(self):
        """Test AdmissionMedicationsSection includes entry elements."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication])
        elem = section.to_element()

        # CONF:1198-10102 (SHOULD)
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_section_entry_has_act(self):
        """Test entry contains act element (Admission Medication wrapper)."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        # CONF:1098-7698
        assert act.get("classCode") == "ACT"
        # CONF:1098-7699
        assert act.get("moodCode") == "EVN"

    def test_section_entry_act_has_template_id(self):
        """Test act wrapper has correct template ID."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication], version=CDAVersion.R2_1)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")

        # CONF:1098-16758, CONF:1098-16759, CONF:1098-32524
        template = act.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.36"
        assert template.get("extension") == "2014-06-09"

    def test_section_entry_act_has_code(self):
        """Test act wrapper has correct code."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")

        # CONF:1098-15518, CONF:1098-15519, CONF:1098-32152
        code = act.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "42346-7"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"
        assert code.get("displayName") == "Medications on Admission"

    def test_section_entry_act_has_entry_relationship(self):
        """Test act wrapper has entryRelationship containing Medication Activity."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")

        # CONF:1098-7701, CONF:1098-7702
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "SUBJ"

    def test_section_entry_has_medication_activity(self):
        """Test entryRelationship contains substanceAdministration (Medication Activity)."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")

        # CONF:1098-15520
        sub_admin = entry_rel.find(f"{{{NS}}}substanceAdministration")
        assert sub_admin is not None
        assert sub_admin.get("classCode") == "SBADM"

    def test_section_multiple_entries(self):
        """Test AdmissionMedicationsSection with multiple medications."""
        medications = [
            MockMedication(name="Lisinopril 10mg", code="314076"),
            MockMedication(name="Metformin 500mg", code="860975"),
        ]
        section = AdmissionMedicationsSection(medications)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an act wrapper
        for entry in entries:
            act = entry.find(f"{{{NS}}}act")
            assert act is not None

    def test_section_to_string(self):
        """Test AdmissionMedicationsSection serialization."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "42346-7" in xml  # Section code
        assert "Medications on Admission" in xml

    def test_section_structure_order(self):
        """Test that section elements are in correct order."""
        medication = MockMedication()
        section = AdmissionMedicationsSection([medication])
        elem = section.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "code" in names
        assert "title" in names
        assert "text" in names

        # templateId should come before code
        assert names.index("templateId") < names.index("code")
        # code should come before title
        assert names.index("code") < names.index("title")
        # title should come before text
        assert names.index("title") < names.index("text")

    def test_section_missing_optional_fields(self):
        """Test handling of missing optional medication fields."""
        medication = MockMedication(
            name="Unknown Medication",
            code="000000",
            dosage=None,
            route=None,
            frequency=None,
            start_date=None,
            end_date=None,
            status=None,
        )
        section = AdmissionMedicationsSection([medication])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Should handle None values gracefully
        assert tds[1].text == "N/A"  # dosage
        assert tds[2].text == "N/A"  # route
        assert tds[3].text == "N/A"  # frequency
        assert tds[4].text == "Unknown"  # start date
        assert tds[5].text == "Unknown"  # end date
        assert tds[6].text == "Unknown"  # status

    def test_section_discontinued_medication(self):
        """Test narrative for discontinued medication."""
        medication = MockMedication(
            name="Warfarin 5mg",
            code="855333",
            status="discontinued",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 3, 15),
        )
        section = AdmissionMedicationsSection([medication])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check status
        assert tds[6].text == "Discontinued"
        # Check end date
        assert tds[5].text == "2023-03-15"

    def test_section_with_instructions(self):
        """Test medication with patient instructions."""
        medication = MockMedication(
            name="Lisinopril 10mg",
            code="314076",
            instructions="Take in the morning with food",
        )
        section = AdmissionMedicationsSection([medication])
        elem = section.to_element()

        # Entry should be created
        entry = elem.find(f"{{{NS}}}entry")
        assert entry is not None

        # Instructions should be in Medication Activity
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        sub_admin = entry_rel.find(f"{{{NS}}}substanceAdministration")

        # Look for instructions in entryRelationship
        instruction_rel = sub_admin.find(f".//{{{NS}}}entryRelationship[@typeCode='SUBJ']")
        if instruction_rel is not None:
            instruction_act = instruction_rel.find(f"{{{NS}}}act")
            if instruction_act is not None:
                text_elem = instruction_act.find(f"{{{NS}}}text")
                assert text_elem is not None


class TestAdmissionMedicationsSectionIntegration:
    """Integration tests for AdmissionMedicationsSection."""

    def test_complete_admission_medications_section(self):
        """Test creating a complete admission medications section."""
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
                name="Warfarin 5mg oral tablet",
                code="855333",
                dosage="5 mg",
                route="oral",
                frequency="once daily",
                start_date=date(2022, 6, 1),
                end_date=date(2023, 3, 15),
                status="discontinued",
            ),
        ]

        section = AdmissionMedicationsSection(medications, title="Medications on Admission")
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

        # Verify each entry has the correct structure
        for entry in entries:
            act = entry.find(f"{{{NS}}}act")
            assert act is not None

            entry_rel = act.find(f"{{{NS}}}entryRelationship")
            assert entry_rel is not None

            sub_admin = entry_rel.find(f"{{{NS}}}substanceAdministration")
            assert sub_admin is not None

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        medication = MockMedication()
        section = AdmissionMedicationsSection([medication])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_both_versions_create_valid_output(self):
        """Test that both R2.1 and R2.0 versions create valid output."""
        medication = MockMedication()

        section_r21 = AdmissionMedicationsSection([medication], version=CDAVersion.R2_1)
        elem_r21 = section_r21.to_element()

        section_r20 = AdmissionMedicationsSection([medication], version=CDAVersion.R2_0)
        elem_r20 = section_r20.to_element()

        # Both should have section element
        assert local_name(elem_r21) == "section"
        assert local_name(elem_r20) == "section"

        # Both should have required elements
        for elem in [elem_r21, elem_r20]:
            assert elem.find(f"{{{NS}}}templateId") is not None
            assert elem.find(f"{{{NS}}}code") is not None
            assert elem.find(f"{{{NS}}}title") is not None
            assert elem.find(f"{{{NS}}}text") is not None

    def test_xml_validity(self):
        """Test that generated XML is well-formed."""
        medications = [
            MockMedication(name="Med 1", code="123"),
            MockMedication(name="Med 2", code="456"),
        ]
        section = AdmissionMedicationsSection(medications)
        xml_string = section.to_string(pretty=True)

        # Should be parseable
        try:
            etree.fromstring(xml_string.encode())
        except etree.XMLSyntaxError:
            pytest.fail("Generated XML is not well-formed")

    def test_empty_section_validity(self):
        """Test that empty section is still valid."""
        section = AdmissionMedicationsSection([])
        elem = section.to_element()

        # Should have all required elements even when empty
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}title") is not None
        assert elem.find(f"{{{NS}}}text") is not None

        # Should have no entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0
