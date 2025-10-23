"""Tests for AnesthesiaSection builder."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.sections.anesthesia import AnesthesiaSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockMedication:
    """Mock medication for testing anesthesia agents."""

    def __init__(
        self,
        name="Propofol",
        code="8782",
        status="completed",
        route="Intravenous",
        dosage="200 mg",
        start_date=None,
        end_date=None,
        instructions=None,
    ):
        self._name = name
        self._code = code
        self._status = status
        self._route = route
        self._dosage = dosage
        self._start_date = start_date
        self._end_date = end_date
        self._instructions = instructions

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def status(self):
        return self._status

    @property
    def route(self):
        return self._route

    @property
    def dosage(self):
        return self._dosage

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def instructions(self):
        return self._instructions


class MockAnesthesia:
    """Mock anesthesia for testing."""

    def __init__(
        self,
        anesthesia_type="General anesthesia",
        anesthesia_code="50697003",
        anesthesia_code_system="SNOMED CT",
        start_time=None,
        end_time=None,
        status="completed",
        anesthesia_agents=None,
        route=None,
        performer_name=None,
        notes=None,
    ):
        self._anesthesia_type = anesthesia_type
        self._anesthesia_code = anesthesia_code
        self._anesthesia_code_system = anesthesia_code_system
        self._start_time = start_time
        self._end_time = end_time
        self._status = status
        self._anesthesia_agents = anesthesia_agents
        self._route = route
        self._performer_name = performer_name
        self._notes = notes

    @property
    def anesthesia_type(self):
        return self._anesthesia_type

    @property
    def anesthesia_code(self):
        return self._anesthesia_code

    @property
    def anesthesia_code_system(self):
        return self._anesthesia_code_system

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def status(self):
        return self._status

    @property
    def anesthesia_agents(self):
        return self._anesthesia_agents

    @property
    def route(self):
        return self._route

    @property
    def performer_name(self):
        return self._performer_name

    @property
    def notes(self):
        return self._notes


class TestAnesthesiaSection:
    """Tests for AnesthesiaSection builder."""

    def test_anesthesia_section_basic(self):
        """Test basic AnesthesiaSection creation."""
        anesthesia = MockAnesthesia()
        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_anesthesia_section_has_template_id_r21(self):
        """Test AnesthesiaSection includes R2.1 template ID."""
        anesthesia = MockAnesthesia()
        section = AnesthesiaSection([anesthesia], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.25"
        assert template.get("extension") == "2014-06-09"

    def test_anesthesia_section_has_code(self):
        """Test AnesthesiaSection includes section code."""
        anesthesia = MockAnesthesia()
        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "59774-0"  # Anesthesia
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC

    def test_anesthesia_section_has_title(self):
        """Test AnesthesiaSection includes title."""
        anesthesia = MockAnesthesia()
        section = AnesthesiaSection([anesthesia], title="Procedure Anesthesia")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "Procedure Anesthesia"

    def test_anesthesia_section_default_title(self):
        """Test AnesthesiaSection uses default title."""
        anesthesia = MockAnesthesia()
        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Anesthesia"

    def test_anesthesia_section_has_narrative(self):
        """Test AnesthesiaSection includes narrative text."""
        anesthesia = MockAnesthesia()
        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_anesthesia_section_narrative_table(self):
        """Test narrative includes HTML table."""
        anesthesia = MockAnesthesia(
            anesthesia_type="Conscious sedation",
            anesthesia_code="48598005",
        )
        section = AnesthesiaSection([anesthesia])
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
        assert len(ths) == 8  # Type, Code, Status, Start, End, Route, Agents, Performer

    def test_anesthesia_section_empty_narrative(self):
        """Test narrative when no anesthesia records."""
        section = AnesthesiaSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No anesthesia recorded"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_anesthesia_section_has_procedure_entry(self):
        """Test AnesthesiaSection includes procedure entry element."""
        anesthesia = MockAnesthesia()
        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1
        assert entries[0].get("typeCode") == "DRIV"

        # Should contain procedure element
        proc = entries[0].find(f"{{{NS}}}procedure")
        assert proc is not None
        assert proc.get("classCode") == "PROC"

    def test_anesthesia_section_with_medication_entry(self):
        """Test AnesthesiaSection includes medication entries for agents."""
        agent = MockMedication(name="Propofol", code="8782")
        anesthesia = MockAnesthesia(anesthesia_agents=[agent])
        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        # Should have 2 entries: 1 procedure + 1 medication
        assert len(entries) == 2

        # First entry should be procedure
        proc = entries[0].find(f"{{{NS}}}procedure")
        assert proc is not None

        # Second entry should be medication
        sub_admin = entries[1].find(f"{{{NS}}}substanceAdministration")
        assert sub_admin is not None
        assert sub_admin.get("classCode") == "SBADM"

    def test_anesthesia_section_multiple_agents(self):
        """Test AnesthesiaSection with multiple anesthesia agents."""
        agents = [
            MockMedication(name="Propofol", code="8782"),
            MockMedication(name="Fentanyl", code="4337"),
        ]
        anesthesia = MockAnesthesia(anesthesia_agents=agents)
        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        # Should have 3 entries: 1 procedure + 2 medications
        assert len(entries) == 3

    def test_anesthesia_section_multiple_records(self):
        """Test AnesthesiaSection with multiple anesthesia records."""
        anesthesias = [
            MockAnesthesia(anesthesia_type="General anesthesia", anesthesia_code="50697003"),
            MockAnesthesia(anesthesia_type="Local anesthesia", anesthesia_code="386761002"),
        ]
        section = AnesthesiaSection(anesthesias)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        # Should have 2 entries: 2 procedures
        assert len(entries) == 2

    def test_anesthesia_section_to_string(self):
        """Test AnesthesiaSection serialization."""
        anesthesia = MockAnesthesia()
        section = AnesthesiaSection([anesthesia])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "59774-0" in xml  # Section code

    def test_anesthesia_section_structure_order(self):
        """Test that section elements are in correct order."""
        anesthesia = MockAnesthesia()
        section = AnesthesiaSection([anesthesia])
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

    def test_anesthesia_with_datetime(self):
        """Test anesthesia with datetime values."""
        start = datetime(2023, 5, 15, 10, 30)
        end = datetime(2023, 5, 15, 12, 45)
        anesthesia = MockAnesthesia(start_time=start, end_time=end)
        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        # Verify procedure entry has effectiveTime
        entry = elem.find(f"{{{NS}}}entry")
        proc = entry.find(f"{{{NS}}}procedure")
        eff_time = proc.find(f"{{{NS}}}effectiveTime")
        assert eff_time is not None

    def test_anesthesia_with_date_only(self):
        """Test anesthesia with date-only values."""
        start = date(2023, 5, 15)
        anesthesia = MockAnesthesia(start_time=start)
        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        # Verify procedure entry exists
        entry = elem.find(f"{{{NS}}}entry")
        proc = entry.find(f"{{{NS}}}procedure")
        assert proc is not None

    def test_anesthesia_with_performer(self):
        """Test anesthesia with performer."""
        anesthesia = MockAnesthesia(performer_name="Dr. Sarah Johnson")
        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        # Verify performer in procedure entry
        entry = elem.find(f"{{{NS}}}entry")
        proc = entry.find(f"{{{NS}}}procedure")
        performer = proc.find(f"{{{NS}}}performer")
        assert performer is not None

        assigned_entity = performer.find(f"{{{NS}}}assignedEntity")
        assert assigned_entity is not None
        assigned_person = assigned_entity.find(f"{{{NS}}}assignedPerson")
        assert assigned_person is not None

    def test_anesthesia_with_route(self):
        """Test anesthesia with route of administration."""
        anesthesia = MockAnesthesia(route="Inhalation")
        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        # Verify methodCode in procedure entry
        entry = elem.find(f"{{{NS}}}entry")
        proc = entry.find(f"{{{NS}}}procedure")
        method = proc.find(f"{{{NS}}}methodCode")
        assert method is not None


class TestAnesthesiaSectionIntegration:
    """Integration tests for AnesthesiaSection."""

    def test_complete_anesthesia_section(self):
        """Test creating a complete anesthesia section with all fields."""
        agents = [
            MockMedication(
                name="Propofol",
                code="8782",
                status="completed",
                route="Intravenous",
                dosage="200 mg",
                start_date=datetime(2023, 5, 15, 10, 30),
            ),
            MockMedication(
                name="Fentanyl",
                code="4337",
                status="completed",
                route="Intravenous",
                dosage="100 mcg",
                start_date=datetime(2023, 5, 15, 10, 30),
            ),
        ]

        anesthesia = MockAnesthesia(
            anesthesia_type="Conscious sedation",
            anesthesia_code="48598005",
            anesthesia_code_system="SNOMED CT",
            start_time=datetime(2023, 5, 15, 10, 30),
            end_time=datetime(2023, 5, 15, 12, 45),
            status="completed",
            anesthesia_agents=agents,
            route="Intravenous",
            performer_name="Dr. Michael Chen, MD",
        )

        section = AnesthesiaSection([anesthesia], title="Procedure Anesthesia")
        elem = section.to_element()

        # Verify structure
        assert local_name(elem) == "section"

        # Verify title
        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Procedure Anesthesia"

        # Verify narrative table has 1 row
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 1

        # Verify entries: 1 procedure + 2 medications
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 3

    def test_general_anesthesia_scenario(self):
        """Test general anesthesia scenario for surgery."""
        agents = [
            MockMedication(name="Sevoflurane", code="203134"),
            MockMedication(name="Rocuronium", code="76155"),
        ]

        anesthesia = MockAnesthesia(
            anesthesia_type="General anesthesia",
            anesthesia_code="50697003",
            anesthesia_code_system="SNOMED CT",
            start_time=datetime(2023, 6, 10, 8, 0),
            end_time=datetime(2023, 6, 10, 11, 30),
            status="completed",
            anesthesia_agents=agents,
            route="Inhalation",
            performer_name="Dr. Lisa Martinez",
        )

        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        # Verify entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 3  # 1 procedure + 2 medications

    def test_local_anesthesia_scenario(self):
        """Test local anesthesia scenario for minor procedure."""
        agents = [
            MockMedication(
                name="Lidocaine",
                code="6387",
                dosage="20 mg",
                route="Topical",
            ),
        ]

        anesthesia = MockAnesthesia(
            anesthesia_type="Local anesthesia",
            anesthesia_code="386761002",
            anesthesia_code_system="SNOMED CT",
            start_time=datetime(2023, 7, 5, 14, 15),
            status="completed",
            anesthesia_agents=agents,
            route="Topical",
            performer_name="Dr. James Wilson",
        )

        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        # Verify entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2  # 1 procedure + 1 medication

        # Verify narrative has the agent listed
        text = elem.find(f"{{{NS}}}text")
        xml_str = etree.tostring(text, encoding="unicode")
        assert "Lidocaine" in xml_str

    def test_multiple_anesthesia_events(self):
        """Test multiple anesthesia events in operative note."""
        anesthesias = [
            MockAnesthesia(
                anesthesia_type="Epidural anesthesia",
                anesthesia_code="18946005",
                start_time=datetime(2023, 8, 20, 9, 0),
                status="completed",
            ),
            MockAnesthesia(
                anesthesia_type="General anesthesia",
                anesthesia_code="50697003",
                start_time=datetime(2023, 8, 20, 9, 30),
                end_time=datetime(2023, 8, 20, 13, 0),
                status="completed",
            ),
        ]

        section = AnesthesiaSection(anesthesias)
        elem = section.to_element()

        # Verify narrative table has 2 rows
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        trs = tbody.findall(f"{{{NS}}}tr")
        assert len(trs) == 2

        # Verify 2 procedure entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

    def test_anesthesia_without_agents(self):
        """Test anesthesia record without specific agents documented."""
        anesthesia = MockAnesthesia(
            anesthesia_type="Regional anesthesia",
            anesthesia_code="231249005",
            start_time=date(2023, 9, 15),
            status="completed",
            performer_name="Dr. Emily Brown",
        )

        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        # Should only have procedure entry, no medication entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

        # Verify it's a procedure entry
        proc = entries[0].find(f"{{{NS}}}procedure")
        assert proc is not None

    def test_anesthesia_with_end_date_only(self):
        """Test anesthesia with end time as date (not datetime)."""
        anesthesia = MockAnesthesia(
            anesthesia_type="General anesthesia",
            start_time=date(2023, 5, 15),
            end_time=date(2023, 5, 15),
        )
        section = AnesthesiaSection([anesthesia])
        elem = section.to_element()

        # Verify narrative table exists
        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # End time column should be formatted as date (index 4)
        assert tds[4].text == "2023-05-15"
