"""Tests for PayersSection builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.payers import PayersSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockPayer:
    """Mock payer for testing."""

    def __init__(
        self,
        payer_name="Aetna",
        payer_id="60054",
        member_id="W123456789",
        group_number="GRP12345",
        insurance_type="PPO",
        insurance_type_code="PPO",
        start_date=date(2023, 1, 1),
        end_date=None,
        sequence_number=1,
        subscriber_name=None,
        subscriber_id=None,
        relationship_to_subscriber="self",
        payer_phone="1-800-123-4567",
        coverage_type_code="SELF",
        authorization_ids=None,
    ):
        self._payer_name = payer_name
        self._payer_id = payer_id
        self._member_id = member_id
        self._group_number = group_number
        self._insurance_type = insurance_type
        self._insurance_type_code = insurance_type_code
        self._start_date = start_date
        self._end_date = end_date
        self._sequence_number = sequence_number
        self._subscriber_name = subscriber_name
        self._subscriber_id = subscriber_id
        self._relationship_to_subscriber = relationship_to_subscriber
        self._payer_phone = payer_phone
        self._coverage_type_code = coverage_type_code
        self._authorization_ids = authorization_ids

    @property
    def payer_name(self):
        return self._payer_name

    @property
    def payer_id(self):
        return self._payer_id

    @property
    def member_id(self):
        return self._member_id

    @property
    def group_number(self):
        return self._group_number

    @property
    def insurance_type(self):
        return self._insurance_type

    @property
    def insurance_type_code(self):
        return self._insurance_type_code

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def sequence_number(self):
        return self._sequence_number

    @property
    def subscriber_name(self):
        return self._subscriber_name

    @property
    def subscriber_id(self):
        return self._subscriber_id

    @property
    def relationship_to_subscriber(self):
        return self._relationship_to_subscriber

    @property
    def payer_phone(self):
        return self._payer_phone

    @property
    def coverage_type_code(self):
        return self._coverage_type_code

    @property
    def authorization_ids(self):
        return self._authorization_ids


class TestPayersSection:
    """Tests for PayersSection builder."""

    def test_payers_section_basic(self):
        """Test basic PayersSection creation."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_payers_section_has_template_id_r21(self):
        """Test PayersSection includes R2.1 template ID."""
        payer = MockPayer()
        section = PayersSection([payer], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.18"
        assert template.get("extension") == "2015-08-01"

    def test_payers_section_has_template_id_r20(self):
        """Test PayersSection includes R2.0 template ID."""
        payer = MockPayer()
        section = PayersSection([payer], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.18"
        assert template.get("extension") == "2015-08-01"

    def test_payers_section_has_code(self):
        """Test PayersSection includes section code (CONF:1198-15395, CONF:1198-15396, CONF:1198-32149)."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "48768-6"  # CONF:1198-15396
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC (CONF:1198-32149)
        assert code.get("displayName") == "Payers"

    def test_payers_section_has_title(self):
        """Test PayersSection includes title (CONF:1198-7926)."""
        payer = MockPayer()
        section = PayersSection([payer], title="My Insurance")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Insurance"

    def test_payers_section_default_title(self):
        """Test PayersSection uses default title."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Insurance Providers"

    def test_payers_section_has_narrative(self):
        """Test PayersSection includes narrative text (CONF:1198-7927)."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_payers_section_narrative_table(self):
        """Test narrative includes HTML table."""
        payer = MockPayer(
            payer_name="Blue Cross",
            insurance_type="HMO",
            member_id="BC123456",
        )
        section = PayersSection([payer])
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
        assert len(ths) == 6  # Payer, Type, Member ID, Group, Period, Priority

    def test_payers_section_narrative_content(self):
        """Test narrative contains payer data."""
        payer = MockPayer(
            payer_name="United Healthcare",
            insurance_type="PPO",
            member_id="UHC987654",
            group_number="GRP999",
            start_date=date(2023, 3, 15),
            sequence_number=1,
        )
        section = PayersSection([payer])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 6

        # Check payer name with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "United Healthcare"
        assert content.get("ID") == "payer-1"

        # Check insurance type
        assert tds[1].text == "PPO"

        # Check member ID
        assert tds[2].text == "UHC987654"

        # Check group number
        assert tds[3].text == "GRP999"

        # Check coverage period
        assert "2023-03-15" in tds[4].text
        assert "present" in tds[4].text

        # Check priority
        assert tds[5].text == "Primary"

    def test_payers_section_narrative_multiple_payers(self):
        """Test narrative with multiple payers."""
        payers = [
            MockPayer(payer_name="Aetna", member_id="A123", sequence_number=1),
            MockPayer(payer_name="Medicare", member_id="M456", sequence_number=2),
            MockPayer(payer_name="Medicaid", member_id="MC789", sequence_number=3),
        ]
        section = PayersSection(payers)
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

        assert content1.get("ID") == "payer-1"
        assert content2.get("ID") == "payer-2"
        assert content3.get("ID") == "payer-3"

        # Check priority labels
        priority1 = trs[0].findall(f"{{{NS}}}td")[5]
        priority2 = trs[1].findall(f"{{{NS}}}td")[5]
        priority3 = trs[2].findall(f"{{{NS}}}td")[5]

        assert priority1.text == "Primary"
        assert priority2.text == "Secondary"
        assert priority3.text == "Tertiary"

    def test_payers_section_narrative_ended_coverage(self):
        """Test narrative shows end date for terminated coverage."""
        payer = MockPayer(
            payer_name="Old Insurance Co",
            member_id="OLD123",
            start_date=date(2022, 1, 1),
            end_date=date(2023, 12, 31),
        )
        section = PayersSection([payer])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check coverage period shows both dates
        assert "2022-01-01" in tds[4].text
        assert "2023-12-31" in tds[4].text

    def test_payers_section_narrative_no_group_number(self):
        """Test narrative handles missing group number."""
        payer = MockPayer(group_number=None)
        section = PayersSection([payer])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Group number should show N/A
        assert tds[3].text == "N/A"

    def test_payers_section_narrative_no_sequence_number(self):
        """Test narrative handles missing sequence number."""
        payer = MockPayer(sequence_number=None)
        section = PayersSection([payer])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Priority should show "Not specified"
        assert tds[5].text == "Not specified"

    def test_payers_section_empty_narrative(self):
        """Test narrative when no payers."""
        section = PayersSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No insurance information available"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_payers_section_has_entries(self):
        """Test PayersSection includes entry elements (CONF:1198-7959)."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1
        assert entries[0].get("typeCode") == "DRIV"

    def test_payers_section_entry_has_coverage_activity(self):
        """Test entry contains Coverage Activity (CONF:1198-15501)."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        assert act is not None
        assert act.get("classCode") == "ACT"
        assert act.get("moodCode") == "EVN"

    def test_payers_section_multiple_entries(self):
        """Test PayersSection with multiple payers."""
        payers = [
            MockPayer(payer_name="Aetna", member_id="A123"),
            MockPayer(payer_name="Medicare", member_id="M456"),
        ]
        section = PayersSection(payers)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has a coverage activity
        for entry in entries:
            act = entry.find(f"{{{NS}}}act")
            assert act is not None

    def test_payers_section_structure_order(self):
        """Test that section elements are in correct order."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "code" in names
        assert "title" in names
        assert "text" in names
        assert "entry" in names

        # Check order
        assert names.index("templateId") < names.index("code")
        assert names.index("code") < names.index("title")
        assert names.index("title") < names.index("text")
        assert names.index("text") < names.index("entry")


class TestCoverageActivity:
    """Tests for Coverage Activity entry."""

    def test_coverage_activity_basic_structure(self):
        """Test Coverage Activity has correct structure (CONF:1198-8872, CONF:1198-8873)."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")

        assert act.get("classCode") == "ACT"  # CONF:1198-8872
        assert act.get("moodCode") == "EVN"  # CONF:1198-8873

    def test_coverage_activity_has_template_id(self):
        """Test Coverage Activity has template ID (CONF:1198-8897, CONF:1198-10492, CONF:1198-32596)."""
        payer = MockPayer()
        section = PayersSection([payer], version=CDAVersion.R2_1)
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        template = act.find(f"{{{NS}}}templateId")

        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.60"
        assert template.get("extension") == "2023-05-01"  # V4 for R2.1

    def test_coverage_activity_has_id(self):
        """Test Coverage Activity has ID (CONF:1198-8874)."""
        payer = MockPayer(member_id="TEST123")
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        id_elem = act.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("extension") == "TEST123"

    def test_coverage_activity_has_code(self):
        """Test Coverage Activity has correct code (CONF:1198-8876, CONF:1198-19160, CONF:1198-32156)."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        code = act.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "48768-6"  # Payment sources (CONF:1198-19160)
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC (CONF:1198-32156)

    def test_coverage_activity_has_status_code(self):
        """Test Coverage Activity has statusCode (CONF:1198-8875, CONF:1198-19094)."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        status = act.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "completed"  # CONF:1198-19094

    def test_coverage_activity_has_entry_relationship(self):
        """Test Coverage Activity has entryRelationship (CONF:1198-8878, CONF:1198-8879)."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")

        assert entry_rel is not None
        assert entry_rel.get("typeCode") == "COMP"  # CONF:1198-8879

    def test_coverage_activity_sequence_number(self):
        """Test Coverage Activity includes sequence number (CONF:1198-17174, CONF:1198-17175)."""
        payer = MockPayer(sequence_number=2)
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        act = entry.find(f"{{{NS}}}act")
        entry_rel = act.find(f"{{{NS}}}entryRelationship")
        seq = entry_rel.find(f"{{{NS}}}sequenceNumber")

        assert seq is not None
        assert seq.get("value") == "2"  # CONF:1198-17175


class TestPolicyActivity:
    """Tests for Policy Activity entry."""

    def test_policy_activity_basic_structure(self):
        """Test Policy Activity has correct structure (CONF:1198-8898, CONF:1198-8899)."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")

        assert policy_act is not None
        assert policy_act.get("classCode") == "ACT"  # CONF:1198-8898
        assert policy_act.get("moodCode") == "EVN"  # CONF:1198-8899

    def test_policy_activity_has_template_id(self):
        """Test Policy Activity has template ID (CONF:1198-8900, CONF:1198-10516, CONF:1198-32595)."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        template = policy_act.find(f"{{{NS}}}templateId")

        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.61"
        assert template.get("extension") == "2015-08-01"

    def test_policy_activity_has_id(self):
        """Test Policy Activity has ID (CONF:1198-8901)."""
        payer = MockPayer(group_number="GRP456")
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        id_elem = policy_act.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("extension") == "GRP456"

    def test_policy_activity_has_code(self):
        """Test Policy Activity has insurance type code (CONF:1198-8903)."""
        payer = MockPayer(insurance_type="HMO", insurance_type_code="HMO")
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        code = policy_act.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "HMO"

    def test_policy_activity_code_with_translation(self):
        """Test Policy Activity code has payer translation (CONF:1198-32852)."""
        payer = MockPayer(
            payer_name="Aetna",
            payer_id="60054",
            insurance_type_code="PPO",
        )
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        code = policy_act.find(f"{{{NS}}}code")
        translation = code.find(f"{{{NS}}}translation")

        assert translation is not None
        assert translation.get("code") == "60054"
        assert translation.get("displayName") == "Aetna"

    def test_policy_activity_has_status_code(self):
        """Test Policy Activity has statusCode (CONF:1198-8902, CONF:1198-19109)."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        status = policy_act.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "completed"  # CONF:1198-19109

    def test_policy_activity_has_payer_performer(self):
        """Test Policy Activity has payer performer (CONF:1198-8906, CONF:1198-8907)."""
        payer = MockPayer(payer_name="Blue Cross", payer_id="54321")
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        performers = policy_act.findall(f"{{{NS}}}performer")

        # Find payer performer (not guarantor)
        payer_performer = None
        for perf in performers:
            template = perf.find(f"{{{NS}}}templateId")
            if template is not None and template.get("root") == "2.16.840.1.113883.10.20.22.4.87":
                payer_performer = perf
                break

        assert payer_performer is not None
        assert payer_performer.get("typeCode") == "PRF"  # CONF:1198-8907

    def test_policy_activity_payer_has_organization(self):
        """Test payer performer has organization name (CONF:1198-8912, CONF:1198-8913)."""
        payer = MockPayer(payer_name="Cigna")
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        performers = policy_act.findall(f"{{{NS}}}performer")

        payer_performer = None
        for perf in performers:
            template = perf.find(f"{{{NS}}}templateId")
            if template is not None and template.get("root") == "2.16.840.1.113883.10.20.22.4.87":
                payer_performer = perf
                break

        assigned = payer_performer.find(f"{{{NS}}}assignedEntity")
        org = assigned.find(f"{{{NS}}}representedOrganization")
        name = org.find(f"{{{NS}}}name")

        assert name is not None
        assert name.text == "Cigna"

    def test_policy_activity_payer_has_telecom(self):
        """Test payer performer has telecom (CONF:1198-8911)."""
        payer = MockPayer(payer_phone="1-800-555-1234")
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        performers = policy_act.findall(f"{{{NS}}}performer")

        payer_performer = None
        for perf in performers:
            template = perf.find(f"{{{NS}}}templateId")
            if template is not None and template.get("root") == "2.16.840.1.113883.10.20.22.4.87":
                payer_performer = perf
                break

        assigned = payer_performer.find(f"{{{NS}}}assignedEntity")
        telecom = assigned.find(f"{{{NS}}}telecom")

        assert telecom is not None
        assert "1-800-555-1234" in telecom.get("value")

    def test_policy_activity_has_covered_party_participant(self):
        """Test Policy Activity has covered party participant (CONF:1198-8916, CONF:1198-8917)."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        participants = policy_act.findall(f"{{{NS}}}participant")

        # Find covered party participant
        covered_party = None
        for part in participants:
            if part.get("typeCode") == "COV":
                covered_party = part
                break

        assert covered_party is not None
        assert covered_party.get("typeCode") == "COV"  # CONF:1198-8917

    def test_policy_activity_covered_party_has_member_id(self):
        """Test covered party has member ID (CONF:1198-8922, CONF:1198-8984)."""
        payer = MockPayer(member_id="MEM999")
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        participants = policy_act.findall(f"{{{NS}}}participant")

        covered_party = None
        for part in participants:
            if part.get("typeCode") == "COV":
                covered_party = part
                break

        role = covered_party.find(f"{{{NS}}}participantRole")
        id_elem = role.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("extension") == "MEM999"

    def test_policy_activity_covered_party_has_coverage_dates(self):
        """Test covered party has coverage time period (CONF:1198-8918, CONF:1198-8919, CONF:1198-8920)."""
        payer = MockPayer(
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31),
        )
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        participants = policy_act.findall(f"{{{NS}}}participant")

        covered_party = None
        for part in participants:
            if part.get("typeCode") == "COV":
                covered_party = part
                break

        time_elem = covered_party.find(f"{{{NS}}}time")
        low = time_elem.find(f"{{{NS}}}low")
        high = time_elem.find(f"{{{NS}}}high")

        assert low is not None
        assert low.get("value") == "20230101"
        assert high is not None
        assert high.get("value") == "20231231"

    def test_policy_activity_subscriber_participant(self):
        """Test Policy Activity has subscriber participant when subscriber differs from patient (CONF:1198-8934)."""
        payer = MockPayer(
            subscriber_id="SUB123",
            subscriber_name="John Doe",
        )
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        participants = policy_act.findall(f"{{{NS}}}participant")

        # Find subscriber participant
        subscriber = None
        for part in participants:
            if part.get("typeCode") == "HLD":
                subscriber = part
                break

        assert subscriber is not None
        assert subscriber.get("typeCode") == "HLD"  # CONF:1198-8935

    def test_policy_activity_subscriber_has_id(self):
        """Test subscriber participant has ID (CONF:1198-8937, CONF:1198-10120)."""
        payer = MockPayer(subscriber_id="SUB456")
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        participants = policy_act.findall(f"{{{NS}}}participant")

        subscriber = None
        for part in participants:
            if part.get("typeCode") == "HLD":
                subscriber = part
                break

        role = subscriber.find(f"{{{NS}}}participantRole")
        id_elem = role.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("extension") == "SUB456"

    def test_policy_activity_has_authorization_entry(self):
        """Test Policy Activity has authorization entryRelationship (CONF:1198-8939, CONF:1198-8940)."""
        payer = MockPayer()
        section = PayersSection([payer])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        coverage_act = entry.find(f"{{{NS}}}act")
        entry_rel = coverage_act.find(f"{{{NS}}}entryRelationship")
        policy_act = entry_rel.find(f"{{{NS}}}act")
        auth_entry_rel = policy_act.find(f"{{{NS}}}entryRelationship")

        assert auth_entry_rel is not None
        assert auth_entry_rel.get("typeCode") == "REFR"  # CONF:1198-8940


class TestPayersSectionIntegration:
    """Integration tests for PayersSection."""

    def test_complete_payers_section(self):
        """Test creating a complete payers section with multiple insurances."""
        payers = [
            MockPayer(
                payer_name="Blue Cross Blue Shield",
                payer_id="BCBS001",
                member_id="BC123456789",
                group_number="GRP001",
                insurance_type="PPO",
                insurance_type_code="PPO",
                start_date=date(2023, 1, 1),
                sequence_number=1,
                payer_phone="1-800-555-0001",
            ),
            MockPayer(
                payer_name="Medicare Part B",
                payer_id="MCARE",
                member_id="MCARE987654",
                group_number=None,
                insurance_type="Medicare",
                insurance_type_code="MEDICARE",
                start_date=date(2022, 6, 1),
                sequence_number=2,
                payer_phone="1-800-MEDICARE",
            ),
        ]

        section = PayersSection(payers, title="Patient Insurance Coverage")
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

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        payer = MockPayer()
        section = PayersSection([payer])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_payers_section_to_string(self):
        """Test PayersSection serialization."""
        payer = MockPayer()
        section = PayersSection([payer])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "48768-6" in xml  # Section code
        assert "Aetna" in xml  # Payer name

    def test_missing_optional_fields(self):
        """Test handling of missing optional fields."""
        payer = MockPayer(
            group_number=None,
            start_date=None,
            end_date=None,
            sequence_number=None,
            subscriber_id=None,
            payer_phone=None,
        )
        section = PayersSection([payer])
        elem = section.to_element()

        # Should still build successfully
        assert elem is not None
        assert local_name(elem) == "section"

        # Check narrative handles missing data
        text = elem.find(f"{{{NS}}}text")
        assert text is not None
