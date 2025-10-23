"""Advance Directive Observation entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.advance_directive import AdvanceDirectiveProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class AdvanceDirectiveObservation(CDAElement):
    """
    Builder for C-CDA Advance Directive Observation entry.

    Represents advance directive findings (e.g., 'resuscitation status is Full Code').
    Not a legal document substitute - references actual documents via externalDocument.
    Supports both R2.1 (2015-08-01) and R2.0 (2015-08-01) versions.

    Template ID: 2.16.840.1.113883.10.20.22.4.48
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.48",
                extension="2015-08-01",
                description="Advance Directive Observation R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.48",
                extension="2015-08-01",
                description="Advance Directive Observation R2.0",
            ),
        ],
    }

    # Code system OIDs
    SNOMED_OID = "2.16.840.1.113883.6.96"
    LOINC_OID = "2.16.840.1.113883.6.1"

    def __init__(
        self,
        directive: AdvanceDirectiveProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize AdvanceDirectiveObservation builder.

        Args:
            directive: Advance directive data satisfying AdvanceDirectiveProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.directive = directive

    def build(self) -> etree.Element:
        """
        Build Advance Directive Observation XML element.

        Conformance rules implemented:
        - CONF:1198-8648: classCode="OBS"
        - CONF:1198-8649: moodCode="EVN"
        - CONF:1198-8655: templateId with root and extension
        - CONF:1198-8654: at least one id
        - CONF:1198-8651: code from Advance Directive Type Code value set
        - CONF:1198-32842-32844: code/translation with LOINC 75320-2
        - CONF:1198-8652: statusCode="completed"
        - CONF:1198-8656: effectiveTime with low and high
        - CONF:1198-30804: value element
        - CONF:1198-32493: if CD, use SNOMED-CT
        - CONF:1198-8662-8673: participant VRF (verifier)
        - CONF:1198-8667-8673: participant CST (custodian)
        - CONF:1198-8692-8699: reference to externalDocument

        Returns:
            lxml Element for observation
        """
        # Create observation element with required attributes (CONF:1198-8648, 8649)
        obs = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template IDs (CONF:1198-8655, 10485, 32496)
        self.add_template_ids(obs)

        # Add at least one ID (CONF:1198-8654)
        self._add_id(obs)

        # Add code for advance directive type (CONF:1198-8651, 32842-32844)
        self._add_directive_type_code(obs)

        # Add status code = "completed" (CONF:1198-8652, 19082)
        status_elem = StatusCode("completed").to_element()
        obs.append(status_elem)

        # Add effective time with low and high (CONF:1198-8656, 28719, 15521, 32449)
        self._add_effective_time(obs)

        # Add value for directive (CONF:1198-30804, 32493)
        self._add_value(obs)

        # Add verifier participant if available (CONF:1198-8662-8666)
        if self.directive.verifier_name or self.directive.verification_date:
            self._add_verifier_participant(obs)

        # Add custodian participant if available (CONF:1198-8667-8673)
        if self.directive.custodian_name:
            self._add_custodian_participant(obs)

        # Add reference to external document if available (CONF:1198-8692-8699)
        if self.directive.document_id or self.directive.document_url:
            self._add_document_reference(obs)

        return obs

    def _add_id(self, obs: etree._Element) -> None:
        """
        Add ID element to observation.

        Args:
            obs: observation element
        """
        import uuid

        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=str(uuid.uuid4()),
        ).to_element()
        obs.append(id_elem)

    def _add_directive_type_code(self, obs: etree._Element) -> None:
        """
        Add code element for advance directive type.

        CONF:1198-8651: code from Advance Directive Type Code value set
        CONF:1198-32842: SHALL contain translation
        CONF:1198-32843: translation/@code="75320-2"
        CONF:1198-32844: translation/@codeSystem=LOINC

        Args:
            obs: observation element
        """
        code_elem = etree.SubElement(obs, f"{{{NS}}}code")

        # If we have a coded directive type, use it
        if self.directive.directive_type_code and self.directive.directive_type_code_system:
            code_elem.set("code", self.directive.directive_type_code)
            code_system_oid = self._get_code_system_oid(self.directive.directive_type_code_system)
            code_elem.set("codeSystem", code_system_oid)
            code_elem.set("displayName", self.directive.directive_type)
        else:
            # Use nullFlavor with originalText if no code available
            code_elem.set("nullFlavor", "OTH")
            text_elem = etree.SubElement(code_elem, f"{{{NS}}}originalText")
            text_elem.text = self.directive.directive_type

        # Add required translation (CONF:1198-32842-32844)
        translation = etree.SubElement(code_elem, f"{{{NS}}}translation")
        translation.set("code", "75320-2")
        translation.set("codeSystem", self.LOINC_OID)
        translation.set("displayName", "Advance directive")

    def _add_effective_time(self, obs: etree._Element) -> None:
        """
        Add effectiveTime with low and high elements.

        CONF:1198-8656: SHALL contain effectiveTime
        CONF:1198-28719: effectiveTime SHALL contain low
        CONF:1198-15521: effectiveTime SHALL contain high
        CONF:1198-32449: If no ending time, high SHALL have nullFlavor="NA"

        Args:
            obs: observation element
        """
        time_elem = etree.SubElement(obs, f"{{{NS}}}effectiveTime")

        # Add low element (start date)
        low_elem = etree.SubElement(time_elem, f"{{{NS}}}low")
        if self.directive.start_date:
            low_elem.set("value", self.directive.start_date.strftime("%Y%m%d"))
        else:
            low_elem.set("nullFlavor", "UNK")

        # Add high element (end date or NA if no specified ending)
        high_elem = etree.SubElement(time_elem, f"{{{NS}}}high")
        if self.directive.end_date:
            high_elem.set("value", self.directive.end_date.strftime("%Y%m%d"))
        else:
            # No specified ending time (CONF:1198-32449)
            high_elem.set("nullFlavor", "NA")

    def _add_value(self, obs: etree._Element) -> None:
        """
        Add value element for the directive.

        CONF:1198-30804: SHALL contain value
        CONF:1198-32493: If type CD, use SNOMED-CT

        Args:
            obs: observation element
        """
        value_elem = etree.SubElement(obs, f"{{{NS}}}value")
        value_elem.set(f"{{{NS}}}type", "CD")

        # If we have a coded value, use it (preferably SNOMED-CT per CONF:1198-32493)
        if self.directive.directive_value_code and self.directive.directive_value_code_system:
            code_system_oid = self._get_code_system_oid(self.directive.directive_value_code_system)
            value_elem.set("code", self.directive.directive_value_code)
            value_elem.set("codeSystem", code_system_oid)
            value_elem.set("displayName", self.directive.directive_value)
        else:
            # Use originalText if no code available
            value_elem.set("nullFlavor", "OTH")
            text_elem = etree.SubElement(value_elem, f"{{{NS}}}originalText")
            text_elem.text = self.directive.directive_value

    def _add_verifier_participant(self, obs: etree._Element) -> None:
        """
        Add verifier participant (VRF).

        CONF:1198-8662: SHOULD contain participant
        CONF:1198-8663: participant/@typeCode="VRF"
        CONF:1198-8664: templateId root="2.16.840.1.113883.10.20.1.58"
        CONF:1198-8665: SHOULD contain time
        CONF:1198-8666: time data type SHALL be TS

        Args:
            obs: observation element
        """
        participant = etree.SubElement(
            obs,
            f"{{{NS}}}participant",
            typeCode="VRF",
        )

        # Add template ID (CONF:1198-8664, 10486)
        template_id = etree.SubElement(participant, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.1.58")

        # Add time if verification date available (CONF:1198-8665, 8666)
        if self.directive.verification_date:
            time_elem = etree.SubElement(participant, f"{{{NS}}}time")
            time_elem.set("value", self.directive.verification_date.strftime("%Y%m%d"))

        # Add participantRole (CONF:1198-8825)
        participant_role = etree.SubElement(participant, f"{{{NS}}}participantRole")

        # Add playingEntity with name if available (CONF:1198-28428)
        if self.directive.verifier_name:
            playing_entity = etree.SubElement(participant_role, f"{{{NS}}}playingEntity")
            name_elem = etree.SubElement(playing_entity, f"{{{NS}}}name")
            name_elem.text = self.directive.verifier_name

    def _add_custodian_participant(self, obs: etree._Element) -> None:
        """
        Add custodian participant (CST) - healthcare agent/proxy.

        CONF:1198-8667: SHOULD contain participant
        CONF:1198-8668: participant/@typeCode="CST"
        CONF:1198-8669: participantRole
        CONF:1198-8670: participantRole/@classCode="AGNT"
        CONF:1198-28440: participantRole/code from Personal And Legal Relationship
        CONF:1198-8671: SHOULD contain address
        CONF:1198-8672: SHOULD contain telecom
        CONF:1198-8673: playingEntity SHALL contain name

        Args:
            obs: observation element
        """
        participant = etree.SubElement(
            obs,
            f"{{{NS}}}participant",
            typeCode="CST",
        )

        # Add participantRole (CONF:1198-8669, 8670)
        participant_role = etree.SubElement(
            participant,
            f"{{{NS}}}participantRole",
            classCode="AGNT",
        )

        # Add relationship code if available (CONF:1198-28440)
        if self.directive.custodian_relationship_code:
            code_elem = etree.SubElement(participant_role, f"{{{NS}}}code")
            code_elem.set("code", self.directive.custodian_relationship_code)
            code_elem.set("codeSystem", "2.16.840.1.113883.11.20.12.1")
            if self.directive.custodian_relationship:
                code_elem.set("displayName", self.directive.custodian_relationship)
        elif self.directive.custodian_relationship:
            code_elem = etree.SubElement(participant_role, f"{{{NS}}}code")
            code_elem.set("nullFlavor", "OTH")
            text_elem = etree.SubElement(code_elem, f"{{{NS}}}originalText")
            text_elem.text = self.directive.custodian_relationship

        # Add address if available (CONF:1198-8671)
        if self.directive.custodian_address:
            addr_elem = etree.SubElement(participant_role, f"{{{NS}}}addr")
            street = etree.SubElement(addr_elem, f"{{{NS}}}streetAddressLine")
            street.text = self.directive.custodian_address

        # Add telecom if available (CONF:1198-8672)
        if self.directive.custodian_phone:
            telecom = etree.SubElement(participant_role, f"{{{NS}}}telecom")
            telecom.set("value", f"tel:{self.directive.custodian_phone}")
            telecom.set("use", "HP")

        # Add playingEntity with name (CONF:1198-8824, 8673)
        playing_entity = etree.SubElement(participant_role, f"{{{NS}}}playingEntity")
        name_elem = etree.SubElement(playing_entity, f"{{{NS}}}name")
        name_elem.text = self.directive.custodian_name

    def _add_document_reference(self, obs: etree._Element) -> None:
        """
        Add reference to external advance directive document.

        CONF:1198-8692: SHOULD contain reference
        CONF:1198-8694: reference/@typeCode="REFR"
        CONF:1198-8693: reference SHALL contain externalDocument
        CONF:1198-8695: externalDocument SHALL contain id
        CONF:1198-8696: externalDocument MAY contain text
        CONF:1198-8697: text MAY contain reference
        CONF:1198-8698: URL SHALL be in text/reference
        CONF:1198-8699: URL SHOULD have corresponding linkHTML in narrative

        Args:
            obs: observation element
        """
        reference = etree.SubElement(
            obs,
            f"{{{NS}}}reference",
            typeCode="REFR",
        )

        # Add externalDocument (CONF:1198-8693)
        ext_doc = etree.SubElement(reference, f"{{{NS}}}externalDocument")

        # Add document ID (CONF:1198-8695)
        if self.directive.document_id:
            id_elem = etree.SubElement(ext_doc, f"{{{NS}}}id")
            id_elem.set("root", self.directive.document_id)
        else:
            # Generate a UUID if no ID provided
            import uuid

            id_elem = etree.SubElement(ext_doc, f"{{{NS}}}id")
            id_elem.set("root", str(uuid.uuid4()))

        # Add text with URL or description (CONF:1198-8696, 8697, 8698)
        if self.directive.document_url or self.directive.document_description:
            text_elem = etree.SubElement(ext_doc, f"{{{NS}}}text")

            if self.directive.document_url:
                # Add reference element with URL
                ref_elem = etree.SubElement(text_elem, f"{{{NS}}}reference")
                ref_elem.set("value", self.directive.document_url)
            elif self.directive.document_description:
                # Just use text content
                text_elem.text = self.directive.document_description

    def _get_code_system_oid(self, code_system: str) -> str:
        """
        Map code system name to OID.

        Args:
            code_system: Code system name or OID

        Returns:
            Code system OID
        """
        # If already an OID (starts with number), return as-is
        if code_system and code_system[0].isdigit():
            return code_system

        code_system_map = {
            "snomed ct": self.SNOMED_OID,
            "snomed": self.SNOMED_OID,
            "loinc": self.LOINC_OID,
        }
        return code_system_map.get(code_system.lower(), code_system)
