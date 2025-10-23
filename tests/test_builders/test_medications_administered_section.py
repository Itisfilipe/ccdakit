"""Tests for MedicationsAdministeredSection builder."""

from datetime import datetime
from typing import Optional

from lxml import etree

from ccdakit.builders.sections.medications_administered import (
    MedicationsAdministeredSection,
)
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockMedicationAdministered:
    """Mock medication administration for testing."""

    def __init__(
        self,
        name="Acetaminophen 325mg oral tablet",
        code="197806",
        administration_time=datetime(2023, 12, 1, 14, 30),
        administration_end_time=None,
        dose="325 mg",
        route="oral",
        rate=None,
        site=None,
        status="completed",
        performer=None,
        indication=None,
        instructions=None,
    ):
        self._name = name
        self._code = code
        self._administration_time = administration_time
        self._administration_end_time = administration_end_time
        self._dose = dose
        self._route = route
        self._rate = rate
        self._site = site
        self._status = status
        self._performer = performer
        self._indication = indication
        self._instructions = instructions

    @property
    def name(self) -> str:
        return self._name

    @property
    def code(self) -> str:
        return self._code

    @property
    def administration_time(self) -> datetime:
        return self._administration_time

    @property
    def administration_end_time(self) -> Optional[datetime]:
        return self._administration_end_time

    @property
    def dose(self) -> str:
        return self._dose

    @property
    def route(self) -> str:
        return self._route

    @property
    def rate(self) -> Optional[str]:
        return self._rate

    @property
    def site(self) -> Optional[str]:
        return self._site

    @property
    def status(self) -> str:
        return self._status

    @property
    def performer(self) -> Optional[str]:
        return self._performer

    @property
    def indication(self) -> Optional[str]:
        return self._indication

    @property
    def instructions(self) -> Optional[str]:
        return self._instructions


class TestMedicationsAdministeredSection:
    """Tests for MedicationsAdministeredSection builder."""

    def test_medications_administered_section_basic(self):
        """Test basic MedicationsAdministeredSection creation."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_medications_administered_section_has_template_id_r21(self):
        """Test MedicationsAdministeredSection includes R2.1 template ID."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication], version=CDAVersion.R2_1)
        elem = section.to_element()

        # CONF:1098-8152, CONF:1098-10405, CONF:1098-32525
        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.38"
        assert template.get("extension") == "2014-06-09"

    def test_medications_administered_section_has_template_id_r20(self):
        """Test MedicationsAdministeredSection includes R2.0 template ID."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.38"
        assert template.get("extension") == "2014-06-09"

    def test_medications_administered_section_has_code(self):
        """Test MedicationsAdministeredSection includes section code."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication])
        elem = section.to_element()

        # CONF:1098-15383, CONF:1098-15384, CONF:1098-30829
        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "29549-3"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Medications Administered"

    def test_medications_administered_section_has_title(self):
        """Test MedicationsAdministeredSection includes title."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection(
            [medication], title="Medications Given During Procedure"
        )
        elem = section.to_element()

        # CONF:1098-8154
        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Medications Given During Procedure"

    def test_medications_administered_section_default_title(self):
        """Test MedicationsAdministeredSection uses default title."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Medications Administered"

    def test_medications_administered_section_has_narrative(self):
        """Test MedicationsAdministeredSection includes narrative text."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication])
        elem = section.to_element()

        # CONF:1098-8155
        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_medications_administered_section_narrative_table(self):
        """Test narrative includes HTML table with proper headers."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication])
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
        # Medication, Dose, Route, Administration Time, Site, Rate, Performer, Status
        assert len(ths) == 8

        # Verify header text
        headers = [th.text for th in ths]
        assert "Medication" in headers
        assert "Dose" in headers
        assert "Route" in headers
        assert "Administration Time" in headers
        assert "Site" in headers
        assert "Rate" in headers
        assert "Performer" in headers
        assert "Status" in headers

    def test_medications_administered_section_narrative_content(self):
        """Test narrative contains medication administration data."""
        medication = MockMedicationAdministered(
            name="Ondansetron 4mg injection",
            code="312086",
            dose="4 mg",
            route="iv",
            administration_time=datetime(2023, 12, 1, 14, 30),
            status="completed",
            performer="Dr. Jane Smith, RN",
            site="left arm",
        )
        section = MedicationsAdministeredSection([medication])
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
        assert content.text == "Ondansetron 4mg injection"
        assert content.get("ID") == "medication-administered-1"

        # Check dose
        assert tds[1].text == "4 mg"

        # Check route
        assert tds[2].text == "Iv"

        # Check administration time
        assert tds[3].text == "2023-12-01 14:30"

        # Check site
        assert tds[4].text == "left arm"

        # Check rate (should be dash when not specified)
        assert tds[5].text == "-"

        # Check performer
        assert tds[6].text == "Dr. Jane Smith, RN"

        # Check status
        assert tds[7].text == "Completed"

    def test_medications_administered_section_narrative_with_rate(self):
        """Test narrative shows administration rate for IV infusions."""
        medication = MockMedicationAdministered(
            name="Normal Saline 0.9% IV Solution",
            code="313002",
            dose="1000 mL",
            route="intravenous",
            rate="100 mL/hr",
            administration_time=datetime(2023, 12, 1, 10, 0),
            administration_end_time=datetime(2023, 12, 1, 20, 0),
            status="completed",
        )
        section = MedicationsAdministeredSection([medication])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check rate
        assert tds[5].text == "100 mL/hr"

        # Check time range
        assert tds[3].text == "2023-12-01 10:00 - 2023-12-01 20:00"

    def test_medications_administered_section_narrative_multiple_medications(self):
        """Test narrative with multiple administered medications."""
        medications = [
            MockMedicationAdministered(
                name="Ondansetron 4mg injection", code="312086"
            ),
            MockMedicationAdministered(
                name="Acetaminophen 325mg tablet", code="197806"
            ),
            MockMedicationAdministered(
                name="Normal Saline 0.9% IV", code="313002"
            ),
        ]
        section = MedicationsAdministeredSection(medications)
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

        assert content1.get("ID") == "medication-administered-1"
        assert content2.get("ID") == "medication-administered-2"
        assert content3.get("ID") == "medication-administered-3"

    def test_medications_administered_section_empty_narrative(self):
        """Test narrative when no medications administered."""
        section = MedicationsAdministeredSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No medications administered"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_medications_administered_section_has_entries(self):
        """Test MedicationsAdministeredSection includes entry elements."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication])
        elem = section.to_element()

        # CONF:1098-8156
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_medications_administered_section_entry_type_code(self):
        """Test entry has correct typeCode."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        assert entry is not None
        assert entry.get("typeCode") == "DRIV"

    def test_medications_administered_section_entry_has_medication_activity(self):
        """Test entry contains Medication Activity."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication])
        elem = section.to_element()

        # CONF:1098-15499
        entry = elem.find(f"{{{NS}}}entry")
        sub_admin = entry.find(f"{{{NS}}}substanceAdministration")
        assert sub_admin is not None
        assert sub_admin.get("classCode") == "SBADM"
        assert sub_admin.get("moodCode") == "EVN"

    def test_medications_administered_section_medication_activity_template(self):
        """Test Medication Activity has correct template ID."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication], version=CDAVersion.R2_1)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        sub_admin = entry.find(f"{{{NS}}}substanceAdministration")

        template = sub_admin.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.16"
        assert template.get("extension") == "2014-06-09"

    def test_medications_administered_section_multiple_entries(self):
        """Test MedicationsAdministeredSection with multiple medications."""
        medications = [
            MockMedicationAdministered(name="Ondansetron 4mg", code="312086"),
            MockMedicationAdministered(name="Acetaminophen 325mg", code="197806"),
        ]
        section = MedicationsAdministeredSection(medications)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has Medication Activity
        for entry in entries:
            sub_admin = entry.find(f"{{{NS}}}substanceAdministration")
            assert sub_admin is not None

    def test_medications_administered_section_null_flavor(self):
        """Test MedicationsAdministeredSection with null flavor."""
        section = MedicationsAdministeredSection([], null_flavor="NI")
        elem = section.to_element()

        assert elem.get("nullFlavor") == "NI"

        # Should have no entries when null flavor is present
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_medications_administered_section_null_flavor_narrative(self):
        """Test narrative with null flavor."""
        section = MedicationsAdministeredSection([], null_flavor="NI")
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert "No information available" in paragraph.text

    def test_medications_administered_section_to_string(self):
        """Test MedicationsAdministeredSection serialization."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "29549-3" in xml  # Section code
        assert "Medications Administered" in xml

    def test_medications_administered_section_structure_order(self):
        """Test that section elements are in correct order."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication])
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


class TestMedicationsAdministeredSectionIntegration:
    """Integration tests for MedicationsAdministeredSection."""

    def test_complete_medications_administered_section(self):
        """Test creating a complete medications administered section."""
        medications = [
            MockMedicationAdministered(
                name="Ondansetron 4mg/2mL injection",
                code="312086",
                dose="4 mg",
                route="iv",
                administration_time=datetime(2023, 12, 1, 14, 30),
                status="completed",
                performer="Dr. Jane Smith, RN",
                site="right arm",
            ),
            MockMedicationAdministered(
                name="Normal Saline 0.9% IV Solution",
                code="313002",
                dose="1000 mL",
                route="intravenous",
                rate="100 mL/hr",
                administration_time=datetime(2023, 12, 1, 10, 0),
                administration_end_time=datetime(2023, 12, 1, 20, 0),
                status="completed",
                performer="RN Team",
            ),
            MockMedicationAdministered(
                name="Acetaminophen 325mg oral tablet",
                code="197806",
                dose="650 mg",
                route="oral",
                administration_time=datetime(2023, 12, 1, 16, 0),
                status="completed",
            ),
        ]

        section = MedicationsAdministeredSection(
            medications, title="Medications Administered During Procedure"
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

        # Verify each entry has proper Medication Activity structure
        for entry in entries:
            sub_admin = entry.find(f"{{{NS}}}substanceAdministration")
            assert sub_admin is not None

            # Check template ID
            template = sub_admin.find(f"{{{NS}}}templateId")
            assert template.get("root") == "2.16.840.1.113883.10.20.22.4.16"

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_with_various_statuses(self):
        """Test section with different medication statuses."""
        medications = [
            MockMedicationAdministered(
                name="Completed Med",
                code="123",
                status="completed",
                administration_time=datetime(2023, 12, 1, 10, 0),
            ),
            MockMedicationAdministered(
                name="Active Med",
                code="456",
                status="active",
                administration_time=datetime(2023, 12, 1, 11, 0),
            ),
            MockMedicationAdministered(
                name="Held Med",
                code="789",
                status="held",
                administration_time=datetime(2023, 12, 1, 12, 0),
            ),
        ]

        section = MedicationsAdministeredSection(medications)
        elem = section.to_element()

        # Check narrative shows different statuses correctly
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")

        # Check status column for each row
        assert trs[0].findall(f"{{{NS}}}td")[7].text == "Completed"
        assert trs[1].findall(f"{{{NS}}}td")[7].text == "Active"
        assert trs[2].findall(f"{{{NS}}}td")[7].text == "Held"

    def test_r20_version_support(self):
        """Test section works with R2.0 version."""
        medication = MockMedicationAdministered()
        section = MedicationsAdministeredSection([medication], version=CDAVersion.R2_0)
        elem = section.to_element()

        # Check section template ID
        template = elem.find(f"{{{NS}}}templateId")
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.38"
        assert template.get("extension") == "2014-06-09"

        # Check entry Medication Activity template ID
        entry = elem.find(f"{{{NS}}}entry")
        sub_admin = entry.find(f"{{{NS}}}substanceAdministration")
        activity_template = sub_admin.find(f"{{{NS}}}templateId")
        assert activity_template.get("root") == "2.16.840.1.113883.10.20.22.4.16"
        assert activity_template.get("extension") == "2014-06-09"

    def test_empty_section_without_null_flavor(self):
        """Test empty section without null flavor still has required elements."""
        section = MedicationsAdministeredSection([])
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

    def test_iv_infusion_with_site_and_rate(self):
        """Test IV infusion medication with site and rate information."""
        medication = MockMedicationAdministered(
            name="Propofol 10mg/mL emulsion",
            code="153476",
            dose="200 mg",
            route="intravenous",
            rate="20 mg/min",
            site="right antecubital fossa",
            administration_time=datetime(2023, 12, 1, 8, 0),
            administration_end_time=datetime(2023, 12, 1, 8, 10),
            status="completed",
            performer="Dr. Robert Jones, MD",
        )

        section = MedicationsAdministeredSection([medication])
        elem = section.to_element()

        # Check narrative
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Verify all details are present
        assert "Propofol" in tds[0].find(f"{{{NS}}}content").text
        assert tds[1].text == "200 mg"
        assert tds[2].text == "Intravenous"
        assert "2023-12-01 08:00 - 2023-12-01 08:10" in tds[3].text
        assert tds[4].text == "right antecubital fossa"
        assert tds[5].text == "20 mg/min"
        assert tds[6].text == "Dr. Robert Jones, MD"
        assert tds[7].text == "Completed"

    def test_oral_medication_simple(self):
        """Test simple oral medication with minimal data."""
        medication = MockMedicationAdministered(
            name="Ibuprofen 400mg oral tablet",
            code="197805",
            dose="400 mg",
            route="oral",
            administration_time=datetime(2023, 12, 1, 12, 0),
            status="completed",
        )

        section = MedicationsAdministeredSection([medication])
        elem = section.to_element()

        # Check that optional fields show dashes
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        assert tds[4].text == "-"  # Site
        assert tds[5].text == "-"  # Rate
        assert tds[6].text == "-"  # Performer

    def test_medication_with_all_optional_fields(self):
        """Test medication with all optional fields populated."""
        medication = MockMedicationAdministered(
            name="Morphine sulfate 2mg/mL injection",
            code="1190107",
            dose="2 mg",
            route="iv",
            rate="1 mg/min",
            site="left arm",
            administration_time=datetime(2023, 12, 1, 15, 30),
            administration_end_time=datetime(2023, 12, 1, 15, 32),
            status="completed",
            performer="Jane Doe, RN",
            indication="Pain management",
            instructions="Administer slowly over 2 minutes",
        )

        section = MedicationsAdministeredSection([medication])
        elem = section.to_element()

        # Verify all data is in narrative
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        assert "Morphine" in tds[0].find(f"{{{NS}}}content").text
        assert tds[1].text == "2 mg"
        assert tds[2].text == "Iv"
        assert "15:30" in tds[3].text
        assert tds[4].text == "left arm"
        assert tds[5].text == "1 mg/min"
        assert tds[6].text == "Jane Doe, RN"
        assert tds[7].text == "Completed"

        # Verify entry is created
        entry = elem.find(f"{{{NS}}}entry")
        assert entry is not None
        sub_admin = entry.find(f"{{{NS}}}substanceAdministration")
        assert sub_admin is not None
