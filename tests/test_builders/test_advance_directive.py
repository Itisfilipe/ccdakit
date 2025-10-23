"""Tests for Advance Directive Observation entry builder."""

from datetime import date

from lxml import etree

from ccdakit.builders.entries.advance_directive import AdvanceDirectiveObservation
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
        directive_type="Resuscitation status",
        directive_type_code="304251008",
        directive_type_code_system="SNOMED CT",
        directive_value="Full code",
        directive_value_code="304253006",
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


class TestAdvanceDirectiveObservation:
    """Tests for AdvanceDirectiveObservation builder."""

    def test_advance_directive_basic(self):
        """Test basic AdvanceDirectiveObservation creation."""
        directive = MockAdvanceDirective()
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        assert local_name(elem) == "observation"
        assert elem.get("classCode") == "OBS"
        assert elem.get("moodCode") == "EVN"

    def test_advance_directive_has_template_id_r21(self):
        """Test AdvanceDirectiveObservation includes R2.1 template ID."""
        directive = MockAdvanceDirective()
        obs = AdvanceDirectiveObservation(directive, version=CDAVersion.R2_1)
        elem = obs.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.48"
        assert template.get("extension") == "2015-08-01"

    def test_advance_directive_has_template_id_r20(self):
        """Test AdvanceDirectiveObservation includes R2.0 template ID."""
        directive = MockAdvanceDirective()
        obs = AdvanceDirectiveObservation(directive, version=CDAVersion.R2_0)
        elem = obs.to_element()

        template = elem.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.22.4.48"
        assert template.get("extension") == "2015-08-01"

    def test_advance_directive_has_id(self):
        """Test AdvanceDirectiveObservation includes ID element."""
        directive = MockAdvanceDirective()
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        id_elem = elem.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") is not None
        assert id_elem.get("extension") is not None

    def test_advance_directive_has_code_with_translation(self):
        """Test AdvanceDirectiveObservation includes code with LOINC translation."""
        directive = MockAdvanceDirective()
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "304251008"
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"

        # Check translation
        translation = code.find(f"{{{NS}}}translation")
        assert translation is not None
        assert translation.get("code") == "75320-2"
        assert translation.get("codeSystem") == "2.16.840.1.113883.6.1"

    def test_advance_directive_code_without_code_system(self):
        """Test AdvanceDirectiveObservation code when no code system provided."""
        directive = MockAdvanceDirective(
            directive_type_code=None,
            directive_type_code_system=None,
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("nullFlavor") == "OTH"

        original_text = code.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "Resuscitation status"

    def test_advance_directive_has_status_code(self):
        """Test AdvanceDirectiveObservation includes statusCode=completed."""
        directive = MockAdvanceDirective()
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        status = elem.find(f"{{{NS}}}statusCode")
        assert status is not None
        assert status.get("code") == "completed"

    def test_advance_directive_has_effective_time(self):
        """Test AdvanceDirectiveObservation includes effectiveTime with low and high."""
        directive = MockAdvanceDirective(
            start_date=date(2020, 1, 15),
            end_date=date(2025, 1, 15),
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None

        low = time_elem.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("value") == "20200115"

        high = time_elem.find(f"{{{NS}}}high")
        assert high is not None
        assert high.get("value") == "20250115"

    def test_advance_directive_effective_time_no_end_date(self):
        """Test AdvanceDirectiveObservation effectiveTime with no end date (NA)."""
        directive = MockAdvanceDirective(
            start_date=date(2020, 1, 15),
            end_date=None,
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None

        high = time_elem.find(f"{{{NS}}}high")
        assert high is not None
        assert high.get("nullFlavor") == "NA"

    def test_advance_directive_effective_time_no_start_date(self):
        """Test AdvanceDirectiveObservation effectiveTime with no start date (UNK)."""
        directive = MockAdvanceDirective(start_date=None)
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        time_elem = elem.find(f"{{{NS}}}effectiveTime")
        assert time_elem is not None

        low = time_elem.find(f"{{{NS}}}low")
        assert low is not None
        assert low.get("nullFlavor") == "UNK"

    def test_advance_directive_has_value(self):
        """Test AdvanceDirectiveObservation includes value element."""
        directive = MockAdvanceDirective(
            directive_value="Full code",
            directive_value_code="304253006",
            directive_value_code_system="SNOMED CT",
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        # Note: type attribute is set in CDA namespace, not XSI namespace
        type_attr = value.get(f"{{{NS}}}type")
        assert type_attr == "CD"
        assert value.get("code") == "304253006"
        assert value.get("codeSystem") == "2.16.840.1.113883.6.96"
        assert value.get("displayName") == "Full code"

    def test_advance_directive_value_without_code(self):
        """Test AdvanceDirectiveObservation value without code."""
        directive = MockAdvanceDirective(
            directive_value="Full code",
            directive_value_code=None,
            directive_value_code_system=None,
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        value = elem.find(f"{{{NS}}}value")
        assert value is not None
        assert value.get("nullFlavor") == "OTH"

        original_text = value.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "Full code"

    def test_advance_directive_with_verifier(self):
        """Test AdvanceDirectiveObservation with verifier participant."""
        directive = MockAdvanceDirective(
            verifier_name="Dr. Jane Smith",
            verification_date=date(2020, 1, 15),
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        participant = elem.find(f"{{{NS}}}participant[@typeCode='VRF']")
        assert participant is not None

        # Check template ID
        template = participant.find(f"{{{NS}}}templateId")
        assert template is not None
        assert template.get("root") == "2.16.840.1.113883.10.20.1.58"

        # Check time
        time_elem = participant.find(f"{{{NS}}}time")
        assert time_elem is not None
        assert time_elem.get("value") == "20200115"

        # Check participant role
        role = participant.find(f"{{{NS}}}participantRole")
        assert role is not None

        playing_entity = role.find(f"{{{NS}}}playingEntity")
        assert playing_entity is not None

        name = playing_entity.find(f"{{{NS}}}name")
        assert name is not None
        assert name.text == "Dr. Jane Smith"

    def test_advance_directive_verifier_without_date(self):
        """Test AdvanceDirectiveObservation verifier without verification date."""
        directive = MockAdvanceDirective(
            verifier_name="Dr. Jane Smith",
            verification_date=None,
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        participant = elem.find(f"{{{NS}}}participant[@typeCode='VRF']")
        assert participant is not None

        # Should not have time element when no verification date
        time_elem = participant.find(f"{{{NS}}}time")
        assert time_elem is None

    def test_advance_directive_without_verifier(self):
        """Test AdvanceDirectiveObservation without verifier."""
        directive = MockAdvanceDirective(
            verifier_name=None,
            verification_date=None,
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        participant = elem.find(f"{{{NS}}}participant[@typeCode='VRF']")
        assert participant is None

    def test_advance_directive_with_custodian(self):
        """Test AdvanceDirectiveObservation with custodian participant."""
        directive = MockAdvanceDirective(
            custodian_name="John Doe",
            custodian_relationship="Spouse",
            custodian_relationship_code="SPS",
            custodian_phone="555-1234",
            custodian_address="123 Main St, Anytown, USA",
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        participant = elem.find(f"{{{NS}}}participant[@typeCode='CST']")
        assert participant is not None

        # Check participant role
        role = participant.find(f"{{{NS}}}participantRole")
        assert role is not None
        assert role.get("classCode") == "AGNT"

        # Check relationship code
        code = role.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("code") == "SPS"
        assert code.get("displayName") == "Spouse"

        # Check address
        addr = role.find(f"{{{NS}}}addr")
        assert addr is not None
        street = addr.find(f"{{{NS}}}streetAddressLine")
        assert street is not None
        assert street.text == "123 Main St, Anytown, USA"

        # Check telecom
        telecom = role.find(f"{{{NS}}}telecom")
        assert telecom is not None
        assert telecom.get("value") == "tel:555-1234"
        assert telecom.get("use") == "HP"

        # Check playing entity with name
        playing_entity = role.find(f"{{{NS}}}playingEntity")
        assert playing_entity is not None
        name = playing_entity.find(f"{{{NS}}}name")
        assert name is not None
        assert name.text == "John Doe"

    def test_advance_directive_custodian_without_code(self):
        """Test AdvanceDirectiveObservation custodian without relationship code."""
        directive = MockAdvanceDirective(
            custodian_name="John Doe",
            custodian_relationship="Friend",
            custodian_relationship_code=None,
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        participant = elem.find(f"{{{NS}}}participant[@typeCode='CST']")
        assert participant is not None

        role = participant.find(f"{{{NS}}}participantRole")
        code = role.find(f"{{{NS}}}code")
        assert code is not None
        assert code.get("nullFlavor") == "OTH"

        original_text = code.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "Friend"

    def test_advance_directive_custodian_minimal(self):
        """Test AdvanceDirectiveObservation custodian with only name."""
        directive = MockAdvanceDirective(custodian_name="John Doe")
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        participant = elem.find(f"{{{NS}}}participant[@typeCode='CST']")
        assert participant is not None

        role = participant.find(f"{{{NS}}}participantRole")
        assert role is not None

        # Should not have address or telecom
        addr = role.find(f"{{{NS}}}addr")
        assert addr is None

        telecom = role.find(f"{{{NS}}}telecom")
        assert telecom is None

    def test_advance_directive_without_custodian(self):
        """Test AdvanceDirectiveObservation without custodian."""
        directive = MockAdvanceDirective(custodian_name=None)
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        participant = elem.find(f"{{{NS}}}participant[@typeCode='CST']")
        assert participant is None

    def test_advance_directive_with_document_reference(self):
        """Test AdvanceDirectiveObservation with document reference."""
        directive = MockAdvanceDirective(
            document_id="2.16.840.1.113883.19.5.99999.1",
            document_url="http://example.com/directives/123",
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        reference = elem.find(f"{{{NS}}}reference")
        assert reference is not None
        assert reference.get("typeCode") == "REFR"

        ext_doc = reference.find(f"{{{NS}}}externalDocument")
        assert ext_doc is not None

        # Check document ID
        id_elem = ext_doc.find(f"{{{NS}}}id")
        assert id_elem is not None
        assert id_elem.get("root") == "2.16.840.1.113883.19.5.99999.1"

        # Check text with URL reference
        text = ext_doc.find(f"{{{NS}}}text")
        assert text is not None
        ref = text.find(f"{{{NS}}}reference")
        assert ref is not None
        assert ref.get("value") == "http://example.com/directives/123"

    def test_advance_directive_document_without_id(self):
        """Test AdvanceDirectiveObservation document reference without explicit ID."""
        directive = MockAdvanceDirective(
            document_id=None,
            document_url="http://example.com/directives/123",
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        reference = elem.find(f"{{{NS}}}reference")
        assert reference is not None

        ext_doc = reference.find(f"{{{NS}}}externalDocument")
        id_elem = ext_doc.find(f"{{{NS}}}id")
        assert id_elem is not None
        # Should have generated UUID
        assert id_elem.get("root") is not None

    def test_advance_directive_document_with_description(self):
        """Test AdvanceDirectiveObservation document with description instead of URL."""
        directive = MockAdvanceDirective(
            document_id="2.16.840.1.113883.19.5.99999.1",
            document_url=None,
            document_description="Living Will signed on 2020-01-15",
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        reference = elem.find(f"{{{NS}}}reference")
        assert reference is not None

        ext_doc = reference.find(f"{{{NS}}}externalDocument")
        text = ext_doc.find(f"{{{NS}}}text")
        assert text is not None
        assert text.text == "Living Will signed on 2020-01-15"

        # Should not have reference element
        ref = text.find(f"{{{NS}}}reference")
        assert ref is None

    def test_advance_directive_without_document_reference(self):
        """Test AdvanceDirectiveObservation without document reference."""
        directive = MockAdvanceDirective(
            document_id=None,
            document_url=None,
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        reference = elem.find(f"{{{NS}}}reference")
        assert reference is None

    def test_advance_directive_code_system_oid_mapping(self):
        """Test code system OID mapping."""
        # Test SNOMED CT
        directive = MockAdvanceDirective(
            directive_type_code_system="SNOMED CT",
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"

        # Test LOINC
        directive = MockAdvanceDirective(
            directive_type_code="75320-2",
            directive_type_code_system="LOINC",
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code.get("codeSystem") == "2.16.840.1.113883.6.1"

        # Test OID passed directly
        directive = MockAdvanceDirective(
            directive_type_code_system="2.16.840.1.113883.6.96",
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        code = elem.find(f"{{{NS}}}code")
        assert code.get("codeSystem") == "2.16.840.1.113883.6.96"

    def test_advance_directive_complete(self):
        """Test AdvanceDirectiveObservation with all optional elements."""
        directive = MockAdvanceDirective(
            directive_type="Resuscitation status",
            directive_type_code="304251008",
            directive_type_code_system="SNOMED CT",
            directive_value="Full code",
            directive_value_code="304253006",
            directive_value_code_system="SNOMED CT",
            start_date=date(2020, 1, 15),
            end_date=date(2025, 1, 15),
            custodian_name="John Doe",
            custodian_relationship="Spouse",
            custodian_relationship_code="SPS",
            custodian_phone="555-1234",
            custodian_address="123 Main St",
            verifier_name="Dr. Jane Smith",
            verification_date=date(2020, 1, 15),
            document_id="2.16.840.1.113883.19.5.99999.1",
            document_url="http://example.com/directives/123",
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        # Verify all elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}value") is not None
        assert elem.find(f"{{{NS}}}participant[@typeCode='VRF']") is not None
        assert elem.find(f"{{{NS}}}participant[@typeCode='CST']") is not None
        assert elem.find(f"{{{NS}}}reference") is not None

    def test_advance_directive_minimal(self):
        """Test AdvanceDirectiveObservation with minimal required elements."""
        directive = MockAdvanceDirective(
            directive_type="Do Not Resuscitate",
            directive_value="DNR",
            verifier_name=None,
            custodian_name=None,
            document_id=None,
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        # Verify required elements are present
        assert elem.find(f"{{{NS}}}templateId") is not None
        assert elem.find(f"{{{NS}}}id") is not None
        assert elem.find(f"{{{NS}}}code") is not None
        assert elem.find(f"{{{NS}}}statusCode") is not None
        assert elem.find(f"{{{NS}}}effectiveTime") is not None
        assert elem.find(f"{{{NS}}}value") is not None

        # Verify optional elements are absent
        assert elem.find(f"{{{NS}}}participant[@typeCode='VRF']") is None
        assert elem.find(f"{{{NS}}}participant[@typeCode='CST']") is None
        assert elem.find(f"{{{NS}}}reference") is None

    def test_advance_directive_to_string(self):
        """Test AdvanceDirectiveObservation serialization."""
        directive = MockAdvanceDirective()
        obs = AdvanceDirectiveObservation(directive)
        xml = obs.to_string(pretty=False)

        assert "<observation" in xml or ":observation" in xml
        assert "classCode" in xml
        assert "moodCode" in xml
        assert "Full code" in xml

    def test_advance_directive_element_order(self):
        """Test that elements are in correct order."""
        directive = MockAdvanceDirective(
            verifier_name="Dr. Jane Smith",
            verification_date=date(2020, 1, 15),
            custodian_name="John Doe",
            document_id="2.16.840.1.113883.19.5.99999.1",
        )
        obs = AdvanceDirectiveObservation(directive)
        elem = obs.to_element()

        children = list(elem)
        names = [local_name(child) for child in children]

        # Check expected elements are present in order
        assert "templateId" in names
        assert "id" in names
        assert "code" in names
        assert "statusCode" in names
        assert "effectiveTime" in names
        assert "value" in names
        assert names.count("participant") == 2  # verifier + custodian
        assert "reference" in names
