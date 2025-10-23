"""Tests for AdvanceDirectivesSection builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.sections.advance_directives import AdvanceDirectivesSection
from ccdakit.core.base import CDAVersion


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


class MockAdvanceDirective:
    """Mock advance directive for testing."""

    def __init__(
        self,
        directive_type="Do Not Resuscitate",
        directive_type_code="304253006",
        directive_type_code_system="SNOMED CT",
        directive_value="Full code",
        directive_value_code="304251008",
        directive_value_code_system="SNOMED CT",
        start_date=date(2020, 1, 15),
        end_date=None,
        custodian_name=None,
        custodian_relationship=None,
        custodian_relationship_code=None,
        custodian_phone=None,
        custodian_address=None,
        verifier_name=None,
        verification_date=None,
        document_id=None,
        document_url=None,
        document_description=None,
    ):
        self._directive_type = directive_type
        self._directive_type_code = directive_type_code
        self._directive_type_code_system = directive_type_code_system
        self._directive_value = directive_value
        self._directive_value_code = directive_value_code
        self._directive_value_code_system = directive_value_code_system
        self._start_date = start_date
        self._end_date = end_date
        self._custodian_name = custodian_name
        self._custodian_relationship = custodian_relationship
        self._custodian_relationship_code = custodian_relationship_code
        self._custodian_phone = custodian_phone
        self._custodian_address = custodian_address
        self._verifier_name = verifier_name
        self._verification_date = verification_date
        self._document_id = document_id
        self._document_url = document_url
        self._document_description = document_description

    @property
    def directive_type(self):
        return self._directive_type

    @property
    def directive_type_code(self):
        return self._directive_type_code

    @property
    def directive_type_code_system(self):
        return self._directive_type_code_system

    @property
    def directive_value(self):
        return self._directive_value

    @property
    def directive_value_code(self):
        return self._directive_value_code

    @property
    def directive_value_code_system(self):
        return self._directive_value_code_system

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def custodian_name(self):
        return self._custodian_name

    @property
    def custodian_relationship(self):
        return self._custodian_relationship

    @property
    def custodian_relationship_code(self):
        return self._custodian_relationship_code

    @property
    def custodian_phone(self):
        return self._custodian_phone

    @property
    def custodian_address(self):
        return self._custodian_address

    @property
    def verifier_name(self):
        return self._verifier_name

    @property
    def verification_date(self):
        return self._verification_date

    @property
    def document_id(self):
        return self._document_id

    @property
    def document_url(self):
        return self._document_url

    @property
    def document_description(self):
        return self._document_description


class TestAdvanceDirectivesSection:
    """Tests for AdvanceDirectivesSection builder."""

    def test_section_basic(self):
        """Test basic AdvanceDirectivesSection creation."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        assert local_name(elem) == "section"

    def test_section_has_template_id_r21(self):
        """Test section includes R2.1 template ID."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive], version=CDAVersion.R2_1)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.21.1"
        assert template.get("extension") == "2015-08-01"

    def test_section_has_template_id_r20(self):
        """Test section includes R2.0 template ID."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive], version=CDAVersion.R2_0)
        elem = section.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.2.21.1"
        assert template.get("extension") == "2015-08-01"

    def test_section_has_code(self):
        """Test section includes correct code."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "42348-3"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC
        assert code.get("displayName") == "Advance Directives"

    def test_section_has_title(self):
        """Test section includes title."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive], title="My Advance Directives")
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title is not None
        assert title.text == "My Advance Directives"

    def test_section_default_title(self):
        """Test section uses default title."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        title = elem.find(f"{{{NS}}}title")
        assert title.text == "Advance Directives"

    def test_section_has_narrative(self):
        """Test section includes narrative text."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

    def test_section_narrative_table(self):
        """Test narrative includes HTML table."""
        directive = MockAdvanceDirective(
            directive_type="Do Not Resuscitate",
            directive_value="Full code",
            start_date=date(2020, 1, 15),
        )
        section = AdvanceDirectivesSection([directive])
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
        assert len(ths) == 6  # Type, Directive, Start Date, End Date, Custodian, Verification

    def test_section_narrative_content(self):
        """Test narrative contains directive data."""
        directive = MockAdvanceDirective(
            directive_type="Resuscitation",
            directive_value="Full code",
            start_date=date(2020, 1, 15),
            end_date=None,
            custodian_name="John Doe",
            custodian_relationship="Spouse",
            verifier_name="Dr. Smith",
            verification_date=date(2020, 1, 16),
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")

        tds = tr.findall(f"{{{NS}}}td")
        assert len(tds) == 6

        # Check directive type with ID
        content = tds[0].find(f"{{{NS}}}content")
        assert content is not None
        assert content.text == "Resuscitation"
        assert content.get("ID") == "directive-1"

        # Check directive value
        assert tds[1].text == "Full code"

        # Check start date
        assert tds[2].text == "2020-01-15"

        # Check end date (N/A if None)
        assert tds[3].text == "N/A"

        # Check custodian
        assert "John Doe" in tds[4].text
        assert "Spouse" in tds[4].text

        # Check verification
        assert "Dr. Smith" in tds[5].text
        assert "2020-01-16" in tds[5].text

    def test_section_narrative_with_url(self):
        """Test narrative creates link when document URL available."""
        directive = MockAdvanceDirective(
            directive_type="Living Will",
            directive_value="See document",
            document_url="http://example.com/living-will.pdf",
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        # Check that directive value has a link
        link = tds[1].find(f"{{{NS}}}linkHtml")
        assert link is not None
        assert link.get("href") == "http://example.com/living-will.pdf"
        assert link.text == "See document"

    def test_section_narrative_without_custodian(self):
        """Test narrative shows 'Not specified' for missing custodian."""
        directive = MockAdvanceDirective(custodian_name=None)
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        assert tds[4].text == "Not specified"

    def test_section_narrative_without_verification(self):
        """Test narrative shows 'Not verified' when no verification."""
        directive = MockAdvanceDirective(verifier_name=None, verification_date=None)
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        assert tds[5].text == "Not verified"

    def test_section_narrative_without_start_date(self):
        """Test narrative shows 'Unknown' for missing start date."""
        directive = MockAdvanceDirective(start_date=None)
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        assert tds[2].text == "Unknown"

    def test_section_narrative_with_end_date(self):
        """Test narrative displays end date when provided."""
        directive = MockAdvanceDirective(
            start_date=date(2020, 1, 15),
            end_date=date(2025, 1, 15),
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        table = text.find(f"{{{NS}}}table")
        tbody = table.find(f"{{{NS}}}tbody")
        tr = tbody.find(f"{{{NS}}}tr")
        tds = tr.findall(f"{{{NS}}}td")

        assert tds[3].text == "2025-01-15"

    def test_section_narrative_multiple_directives(self):
        """Test narrative with multiple directives."""
        directives = [
            MockAdvanceDirective(
                directive_type="Resuscitation",
                directive_value="Full code",
            ),
            MockAdvanceDirective(
                directive_type="Intubation",
                directive_value="No intubation",
            ),
            MockAdvanceDirective(
                directive_type="Antibiotics",
                directive_value="IV antibiotics only",
            ),
        ]
        section = AdvanceDirectivesSection(directives)
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

        assert content1.get("ID") == "directive-1"
        assert content2.get("ID") == "directive-2"
        assert content3.get("ID") == "directive-3"

    def test_section_empty_narrative(self):
        """Test narrative when no directives."""
        section = AdvanceDirectivesSection([])
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        assert text is not None

        # Should have paragraph, not table
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No advance directives on file"

        # Should not have table
        table = text.find(f"{{{NS}}}table")
        assert table is None

    def test_section_null_flavor_narrative(self):
        """Test narrative with null flavor."""
        section = AdvanceDirectivesSection(null_flavor="NI")
        elem = section.to_element()

        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert paragraph.text == "No information about advance directives"

    def test_section_null_flavor_attribute(self):
        """Test section has nullFlavor attribute when specified."""
        section = AdvanceDirectivesSection(null_flavor="NI")
        elem = section.to_element()

        assert elem.get("nullFlavor") == "NI"

    def test_section_has_entries(self):
        """Test section includes entry elements."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 1

    def test_section_entry_has_observation(self):
        """Test entry contains advance directive observation."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        assert observation is not None
        assert observation.get("classCode") == "OBS"
        assert observation.get("moodCode") == "EVN"

    def test_section_observation_has_template_id(self):
        """Test observation has correct template ID."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        template = observation.find(f"{{{NS}}}templateId")

        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.48"
        assert template.get("extension") == "2015-08-01"

    def test_section_observation_has_id(self):
        """Test observation has ID element."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        id_elem = observation.find(f"{{{NS}}}id")

        assert id_elem is not None
        assert id_elem.get("root") is not None

    def test_section_observation_has_code(self):
        """Test observation has directive type code."""
        directive = MockAdvanceDirective(
            directive_type="Resuscitation",
            directive_type_code="304253006",
            directive_type_code_system="SNOMED CT",
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        assert code is not None
        assert code.get("code") == "304253006"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT

    def test_section_observation_code_has_translation(self):
        """Test observation code has required translation."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")
        translation = code.find(f"{{{NS}}}translation")

        assert translation is not None
        assert translation.get("code") == "75320-2"
        assert translation.get("codeSystem") == "2.16.840.1.113883.6.1"  # LOINC

    def test_section_observation_has_status_code(self):
        """Test observation has statusCode = completed."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        status = observation.find(f"{{{NS}}}statusCode")

        assert status is not None
        assert status.get("code") == "completed"

    def test_section_observation_has_effective_time(self):
        """Test observation has effectiveTime with low and high."""
        directive = MockAdvanceDirective(
            start_date=date(2020, 1, 15),
            end_date=None,
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        eff_time = observation.find(f"{{{NS}}}effectiveTime")

        assert eff_time is not None

        low = eff_time.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20200115"

        high = eff_time.find(f"{{{NS}}}high")
        assert high is not None
        # Should have nullFlavor="NA" if no end date
        assert high.get("nullFlavor") == "NA"

    def test_section_observation_effective_time_with_end_date(self):
        """Test effectiveTime/high with actual end date."""
        directive = MockAdvanceDirective(
            start_date=date(2020, 1, 15),
            end_date=date(2025, 1, 15),
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        eff_time = observation.find(f"{{{NS}}}effectiveTime")

        high = eff_time.find(f"{{{NS}}}high")
        assert high.get("value") == "20250115"
        assert high.get("nullFlavor") is None

    def test_section_observation_has_value(self):
        """Test observation has value element."""
        directive = MockAdvanceDirective(
            directive_value="Full code",
            directive_value_code="304251008",
            directive_value_code_system="SNOMED CT",
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value is not None
        assert value.get(f"{{{NS}}}type") == "CD"
        assert value.get("code") == "304251008"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"  # SNOMED CT

    def test_section_observation_value_without_code(self):
        """Test observation value uses originalText when no code."""
        directive = MockAdvanceDirective(
            directive_value="Custom directive text",
            directive_value_code=None,
            directive_value_code_system=None,
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        value = observation.find(f"{{{NS}}}value")

        assert value.get("nullFlavor") == "OTH"
        orig_text = value.find(f"{{{NS}}}originalText")
        assert orig_text is not None
        assert orig_text.text == "Custom directive text"

    def test_section_observation_with_verifier(self):
        """Test observation includes verifier participant."""
        directive = MockAdvanceDirective(
            verifier_name="Dr. Jane Smith",
            verification_date=date(2020, 1, 16),
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        participants = observation.findall(f"{{{NS}}}participant")

        # Find VRF participant
        vrf_participant = None
        for p in participants:
            if p.get("typeCode") == "VRF":
                vrf_participant = p
                break

        assert vrf_participant is not None

        # Check template ID
        template = vrf_participant.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.1.58"

        # Check time
        time_elem = vrf_participant.find(f"{{{NS}}}time")
        assert time_elem is not None
        assert time_elem.get("value") == "20200116"

        # Check name
        role = vrf_participant.find(f"{{{NS}}}participantRole")
        entity = role.find(f"{{{NS}}}playingEntity")
        name = entity.find(f"{{{NS}}}name")
        assert name.text == "Dr. Jane Smith"

    def test_section_observation_with_custodian(self):
        """Test observation includes custodian participant."""
        directive = MockAdvanceDirective(
            custodian_name="John Doe",
            custodian_relationship="Spouse",
            custodian_relationship_code="SPS",
            custodian_phone="555-1234",
            custodian_address="123 Main St",
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        participants = observation.findall(f"{{{NS}}}participant")

        # Find CST participant
        cst_participant = None
        for p in participants:
            if p.get("typeCode") == "CST":
                cst_participant = p
                break

        assert cst_participant is not None

        # Check participantRole
        role = cst_participant.find(f"{{{NS}}}participantRole")
        assert role is not None
        assert role.get("classCode") == "AGNT"

        # Check relationship code
        code = role.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "SPS"

        # Check address
        addr = role.find(f"{{{NS}}}addr")
        assert addr is not None
        street = addr.find(f"{{{NS}}}streetAddressLine")
        assert street.text == "123 Main St"

        # Check telecom
        telecom = role.find(f"{{{NS}}}telecom")
        assert telecom is not None
        assert telecom.get("value") == "tel:555-1234"

        # Check name
        entity = role.find(f"{{{NS}}}playingEntity")
        name = entity.find(f"{{{NS}}}name")
        assert name.text == "John Doe"

    def test_section_observation_with_document_reference(self):
        """Test observation includes reference to external document."""
        directive = MockAdvanceDirective(
            document_id="1.2.3.4.5",
            document_url="http://example.com/directive.pdf",
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        reference = observation.find(f"{{{NS}}}reference")

        assert reference is not None
        assert reference.get("typeCode") == "REFR"

        # Check externalDocument
        ext_doc = reference.find(f"{{{NS}}}externalDocument")
        assert ext_doc is not None

        # Check ID
        id_elem = ext_doc.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") == "1.2.3.4.5"

        # Check text with URL
        text_elem = ext_doc.find(f"{{{NS}}}text")
        assert text_elem is not None
        ref_elem = text_elem.find(f"{{{NS}}}reference")
        assert ref_elem is not None
        assert ref_elem.get("value") == "http://example.com/directive.pdf"

    def test_section_multiple_entries(self):
        """Test section with multiple directives."""
        directives = [
            MockAdvanceDirective(directive_type="Resuscitation"),
            MockAdvanceDirective(directive_type="Intubation"),
        ]
        section = AdvanceDirectivesSection(directives)
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 2

        # Check each entry has an observation
        for entry in entries:
            observation = entry.find(f"{{{NS}}}observation")
            assert observation is not None

    def test_section_no_entries_with_null_flavor(self):
        """Test section has no entries when nullFlavor is set."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive], null_flavor="NI")
        elem = section.to_element()

        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_section_to_string(self):
        """Test section serialization."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive])
        xml = section.to_string(pretty=False)

        assert "<section" in xml or ":section" in xml
        assert "42348-3" in xml  # Section code
        assert "Advance Directives" in xml

    def test_section_structure_order(self):
        """Test that section elements are in correct order."""
        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive])
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


class TestAdvanceDirectivesSectionIntegration:
    """Integration tests for AdvanceDirectivesSection."""

    def test_complete_section(self):
        """Test creating a complete advance directives section."""
        directives = [
            MockAdvanceDirective(
                directive_type="Resuscitation",
                directive_type_code="304253006",
                directive_type_code_system="SNOMED CT",
                directive_value="Full code",
                directive_value_code="304251008",
                directive_value_code_system="SNOMED CT",
                start_date=date(2020, 1, 15),
                end_date=None,
                custodian_name="Jane Doe",
                custodian_relationship="Spouse",
                custodian_relationship_code="SPS",
                custodian_phone="555-1234",
                custodian_address="123 Main St, Anytown, USA",
                verifier_name="Dr. Smith",
                verification_date=date(2020, 1, 16),
                document_id="1.2.3.4.5",
                document_url="http://example.com/directive.pdf",
            ),
            MockAdvanceDirective(
                directive_type="Intubation",
                directive_type_code="304252001",
                directive_type_code_system="SNOMED CT",
                directive_value="No intubation",
                directive_value_code="304253009",
                directive_value_code_system="SNOMED CT",
                start_date=date(2020, 1, 15),
                verifier_name="Dr. Jones",
                verification_date=date(2020, 1, 16),
            ),
        ]

        section = AdvanceDirectivesSection(directives, title="Patient Advance Directives")
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

        # Verify first entry has all components
        obs1 = entries[0].find(f"{{{NS}}}observation")
        assert obs1.find(f"{{{NS}}}code") is not None
        assert obs1.find(f"{{{NS}}}value") is not None
        assert obs1.find(f"{{{NS}}}effectiveTime") is not None

        # Find participants
        participants = obs1.findall(f"{{{NS}}}participant")
        assert len(participants) >= 2  # VRF and CST

    def test_section_in_document_context(self):
        """Test section can be composed in a document."""
        parent = etree.Element(f"{{{NS}}}component")

        directive = MockAdvanceDirective()
        section = AdvanceDirectivesSection([directive])

        parent.append(section.to_element())

        section_elem = parent.find(f"{{{NS}}}section")
        assert section_elem is not None
        assert section_elem.find(f"{{{NS}}}title") is not None

    def test_section_with_minimal_data(self):
        """Test section with minimal directive data."""
        directive = MockAdvanceDirective(
            directive_type="Living Will",
            directive_type_code=None,
            directive_type_code_system=None,
            directive_value="See attached document",
            directive_value_code=None,
            directive_value_code_system=None,
            start_date=None,
            end_date=None,
            custodian_name=None,
            verifier_name=None,
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        # Should still create valid structure
        assert local_name(elem) == "section"
        entry = elem.find(f"{{{NS}}}entry")
        assert entry is not None
        obs = entry.find(f"{{{NS}}}observation")
        assert obs is not None

        # Check code uses originalText
        code = obs.find(f"{{{NS}}}code")
        assert code.get("nullFlavor") == "OTH"
        orig_text = code.find(f"{{{NS}}}originalText")
        assert orig_text.text == "Living Will"

        # Check value uses originalText
        value = obs.find(f"{{{NS}}}value")
        assert value.get("nullFlavor") == "OTH"
        orig_text = value.find(f"{{{NS}}}originalText")
        assert orig_text.text == "See attached document"

    def test_section_none_directives_list(self):
        """Test section handles None directives list."""
        section = AdvanceDirectivesSection(None)
        elem = section.to_element()

        assert local_name(elem) == "section"

        # Should have narrative saying no directives
        text = elem.find(f"{{{NS}}}text")
        paragraph = text.find(f"{{{NS}}}paragraph")
        assert paragraph is not None
        assert "No advance directives" in paragraph.text

        # Should have no entries
        entries = elem.findall(f"{{{NS}}}entry")
        assert len(entries) == 0

    def test_section_observation_with_document_description_only(self):
        """Test observation with document description but no URL."""
        directive = MockAdvanceDirective(
            document_id="1.2.3.4.5",
            document_url=None,
            document_description="Living will signed 2020-01-15",
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        reference = observation.find(f"{{{NS}}}reference")
        ext_doc = reference.find(f"{{{NS}}}externalDocument")
        text_elem = ext_doc.find(f"{{{NS}}}text")

        assert text_elem is not None
        assert text_elem.text == "Living will signed 2020-01-15"
        # Should not have reference subelement when only description
        ref_elem = text_elem.find(f"{{{NS}}}reference")
        assert ref_elem is None

    def test_section_observation_with_oid_code_system(self):
        """Test observation handles OID code system directly."""
        directive = MockAdvanceDirective(
            directive_type_code="304253006",
            directive_type_code_system="2.16.840.1.113883.6.96",  # Already an OID
            directive_value_code="304251008",
            directive_value_code_system="2.16.840.1.113883.6.96",  # Already an OID
        )
        section = AdvanceDirectivesSection([directive])
        elem = section.to_element()

        entry = elem.find(f"{{{NS}}}entry")
        observation = entry.find(f"{{{NS}}}observation")
        code = observation.find(f"{{{NS}}}code")

        # Should use the OID as-is
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"

        value = observation.find(f"{{{NS}}}value")
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"
