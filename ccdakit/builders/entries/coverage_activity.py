"""Coverage Activity entry builder for C-CDA documents."""

import uuid
from datetime import datetime
from typing import Optional

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.payer import PayerProtocol


# CDA namespace
NS = "urn:hl7-org:v3"
SDTC_NS = "urn:hl7-org:sdtc"


class CoverageActivity(CDAElement):
    """
    Builder for C-CDA Coverage Activity entry.

    A Coverage Activity groups policy and authorization acts within a Payers Section
    to order the payment sources. It contains one or more Policy Activities.

    Conforms to:
    - Template ID: 2.16.840.1.113883.10.20.22.4.60 (Coverage Activity V4)
    - Extension: 2023-05-01 (latest version)

    Supports both R2.1 and R2.0 versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.60",
                extension="2023-05-01",
                description="Coverage Activity V4",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.60",
                extension="2015-08-01",
                description="Coverage Activity V3",
            ),
        ],
    }

    def __init__(
        self,
        payer: PayerProtocol,
        coverage_check_date: Optional[datetime] = None,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize CoverageActivity builder.

        Args:
            payer: Payer data satisfying PayerProtocol
            coverage_check_date: Date coverage was checked (optional)
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.payer = payer
        self.coverage_check_date = coverage_check_date

    def build(self) -> etree.Element:
        """
        Build Coverage Activity XML element.

        Conforms to all CONF rules from template 2.16.840.1.113883.10.20.22.4.60:
        - CONF:1198-8872: classCode="ACT"
        - CONF:1198-8873: moodCode="EVN"
        - CONF:1198-8897/10492/32596: templateId
        - CONF:1198-8874: id [1..*]
        - CONF:1198-8876/19160/32156: code="48768-6" Payment sources
        - CONF:1198-8875/19094: statusCode="completed"
        - CONF:4537-33064/33065: effectiveTime (SHOULD)
        - CONF:1198-8878/8879/15528: entryRelationship with Policy Activity

        Returns:
            lxml Element for act
        """
        # Create act element with required attributes (CONF:1198-8872, CONF:1198-8873)
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="EVN",
        )

        # Add template IDs (CONF:1198-8897, CONF:1198-10492, CONF:1198-32596)
        self.add_template_ids(act)

        # Add ID (CONF:1198-8874) - at least one [1..*]
        self._add_id(act)

        # Add code (CONF:1198-8876, CONF:1198-19160, CONF:1198-32156)
        code_elem = Code(
            code="48768-6",
            system="LOINC",
            display_name="Payment sources",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        act.append(code_elem)

        # Add statusCode (CONF:1198-8875, CONF:1198-19094)
        status_elem = etree.SubElement(act, f"{{{NS}}}statusCode", code="completed")

        # Add effectiveTime if provided (CONF:4537-33064, CONF:4537-33065)
        # Records when coverage was checked
        if self.coverage_check_date:
            time_elem = etree.SubElement(act, f"{{{NS}}}effectiveTime")
            time_elem.set("value", self.coverage_check_date.strftime("%Y%m%d%H%M%S"))

        # Add Policy Activity as entryRelationship (CONF:1198-8878, CONF:1198-8879, CONF:1198-15528)
        self._add_policy_activity(act)

        return act

    def _add_id(self, act: etree._Element) -> None:
        """
        Add ID element to act.

        This is the ID from the patient's insurance card.

        Args:
            act: act element
        """
        # Use member ID as the coverage activity ID
        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=self.payer.member_id,
        ).to_element()
        act.append(id_elem)

    def _add_policy_activity(self, act: etree._Element) -> None:
        """
        Add Policy Activity as entryRelationship.

        Conforms to:
        - CONF:1198-8878: SHALL contain at least one [1..*] entryRelationship
        - CONF:1198-8879: SHALL contain typeCode="COMP"
        - CONF:1198-17174/17175: MAY contain sequenceNumber
        - CONF:1198-15528: SHALL contain Policy Activity

        Args:
            act: act element
        """
        entry_rel = etree.SubElement(
            act,
            f"{{{NS}}}entryRelationship",
            typeCode="COMP",  # CONF:1198-8879
        )

        # Add sequence number if provided (CONF:1198-17174, CONF:1198-17175)
        if self.payer.sequence_number is not None:
            seq_elem = etree.SubElement(entry_rel, f"{{{NS}}}sequenceNumber")
            seq_elem.set("value", str(self.payer.sequence_number))

        # Create Policy Activity (CONF:1198-15528)
        policy_builder = PolicyActivity(self.payer, version=self.version)
        entry_rel.append(policy_builder.to_element())


class PolicyActivity(CDAElement):
    """
    Builder for Policy Activity within Coverage Activity.

    A policy activity represents the policy or program providing the coverage.

    Conforms to:
    - Template ID: 2.16.840.1.113883.10.20.22.4.61 (Policy Activity V3)
    - Extension: 2015-08-01
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.61",
                extension="2015-08-01",
                description="Policy Activity V3",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.61",
                extension="2015-08-01",
                description="Policy Activity V3",
            ),
        ],
    }

    def __init__(
        self,
        payer: PayerProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PolicyActivity builder.

        Args:
            payer: Payer data satisfying PayerProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.payer = payer

    def build(self) -> etree.Element:
        """
        Build Policy Activity XML element.

        Conforms to all CONF rules from template 2.16.840.1.113883.10.20.22.4.61:
        - CONF:1198-8898: classCode="ACT"
        - CONF:1198-8899: moodCode="EVN"
        - CONF:1198-8900/10516/32595: templateId
        - CONF:1198-8901: id [1..*]
        - CONF:1198-8903: code (insurance type)
        - CONF:1198-8902/19109: statusCode="completed"
        - CONF:1198-8906: performer (payer)
        - CONF:1198-8916: participant (covered party)
        - CONF:1198-8934: participant (subscriber, SHOULD)
        - CONF:1198-8939: entryRelationship (authorization, SHALL)

        Returns:
            lxml Element for act
        """
        # Create act element (CONF:1198-8898, CONF:1198-8899)
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="EVN",
        )

        # Add template IDs (CONF:1198-8900, CONF:1198-10516, CONF:1198-32595)
        self.add_template_ids(act)

        # Add ID - unique identifier for policy (CONF:1198-8901)
        self._add_id(act)

        # Add code - insurance type (CONF:1198-8903, CONF:1198-32852)
        self._add_code(act)

        # Add statusCode (CONF:1198-8902, CONF:1198-19109)
        status_elem = etree.SubElement(act, f"{{{NS}}}statusCode", code="completed")

        # Add performer - the payer (CONF:1198-8906)
        self._add_payer_performer(act)

        # Add participant - covered party (CONF:1198-8916)
        self._add_covered_party_participant(act)

        # Add participant - subscriber if different from patient (CONF:1198-8934)
        if self.payer.subscriber_id:
            self._add_subscriber_participant(act)

        # Add entryRelationship for authorization/plan (CONF:1198-8939)
        self._add_authorization_entry(act)

        return act

    def _add_id(self, act: etree._Element) -> None:
        """Add policy ID."""
        # Use group number if available, otherwise generate
        extension = self.payer.group_number or str(uuid.uuid4())
        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=extension,
        ).to_element()
        act.append(id_elem)

    def _add_code(self, act: etree._Element) -> None:
        """
        Add code for insurance type.

        CONF:1198-8903: SHALL contain code, SHOULD be from Health Insurance Type value set
        CONF:1198-32852: SHALL contain translation from Payer value set
        """
        code_elem = etree.SubElement(act, f"{{{NS}}}code")

        # If we have a code, use it; otherwise use display name
        if self.payer.insurance_type_code:
            code_elem.set("code", self.payer.insurance_type_code)
            code_elem.set("codeSystem", "2.16.840.1.113883.3.88.12.3221.5.2")
            code_elem.set("displayName", self.payer.insurance_type)
        else:
            # Use nullFlavor with originalText
            code_elem.set("nullFlavor", "OTH")
            orig_text = etree.SubElement(code_elem, f"{{{NS}}}originalText")
            orig_text.text = self.payer.insurance_type

        # Add translation for payer (CONF:1198-32852)
        if self.payer.payer_id:
            translation = etree.SubElement(code_elem, f"{{{NS}}}translation")
            translation.set("code", self.payer.payer_id)
            translation.set("codeSystem", "2.16.840.1.114222.4.11.3591")
            translation.set("displayName", self.payer.payer_name)

    def _add_payer_performer(self, act: etree._Element) -> None:
        """
        Add payer performer.

        CONF:1198-8906: SHALL contain performer
        CONF:1198-8907: typeCode="PRF"
        CONF:1198-16808/16809: templateId for Payer Performer
        CONF:1198-8908: assignedEntity
        CONF:1198-8909: assignedEntity/id
        CONF:1198-8912/8913: representedOrganization/name
        """
        performer = etree.SubElement(act, f"{{{NS}}}performer", typeCode="PRF")

        # Add template ID (CONF:1198-16808, CONF:1198-16809)
        template = etree.SubElement(performer, f"{{{NS}}}templateId")
        template.set("root", "2.16.840.1.113883.10.20.22.4.87")

        # Add assignedEntity (CONF:1198-8908)
        assigned = etree.SubElement(performer, f"{{{NS}}}assignedEntity")

        # Add payer ID (CONF:1198-8909)
        id_elem = Identifier(
            root="2.16.840.1.113883.6.300",  # NAIC
            extension=self.payer.payer_id,
        ).to_element()
        assigned.append(id_elem)

        # Add telecom if available (CONF:1198-8911)
        if self.payer.payer_phone:
            telecom = etree.SubElement(assigned, f"{{{NS}}}telecom")
            telecom.set("use", "WP")
            telecom.set("value", f"tel:{self.payer.payer_phone}")

        # Add representedOrganization (CONF:1198-8912)
        org = etree.SubElement(assigned, f"{{{NS}}}representedOrganization")

        # Add payer name (CONF:1198-8913)
        name = etree.SubElement(org, f"{{{NS}}}name")
        name.text = self.payer.payer_name

    def _add_covered_party_participant(self, act: etree._Element) -> None:
        """
        Add covered party participant (the patient).

        CONF:1198-8916: SHALL contain participant
        CONF:1198-8917: typeCode="COV"
        CONF:1198-16812/16814: templateId for Covered Party Participant
        CONF:1198-8918: time (coverage period)
        CONF:1198-8921: participantRole
        CONF:1198-8922/8984: participantRole/id (member ID)
        CONF:1198-8923/16078: participantRole/code (coverage role)
        """
        participant = etree.SubElement(act, f"{{{NS}}}participant", typeCode="COV")

        # Add template ID (CONF:1198-16812, CONF:1198-16814)
        template = etree.SubElement(participant, f"{{{NS}}}templateId")
        template.set("root", "2.16.840.1.113883.10.20.22.4.89")

        # Add time (coverage period) (CONF:1198-8918, CONF:1198-8919, CONF:1198-8920)
        if self.payer.start_date or self.payer.end_date:
            time_elem = etree.SubElement(participant, f"{{{NS}}}time")
            if self.payer.start_date:
                low = etree.SubElement(time_elem, f"{{{NS}}}low")
                low.set("value", self.payer.start_date.strftime("%Y%m%d"))
            if self.payer.end_date:
                high = etree.SubElement(time_elem, f"{{{NS}}}high")
                high.set("value", self.payer.end_date.strftime("%Y%m%d"))

        # Add participantRole (CONF:1198-8921)
        role = etree.SubElement(participant, f"{{{NS}}}participantRole")

        # Add member ID (CONF:1198-8922, CONF:1198-8984)
        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=self.payer.member_id,
        ).to_element()
        role.append(id_elem)

        # Add code - coverage role type (CONF:1198-8923, CONF:1198-16078)
        code_elem = etree.SubElement(role, f"{{{NS}}}code")
        if self.payer.coverage_type_code:
            code_elem.set("code", self.payer.coverage_type_code)
            code_elem.set("codeSystem", "2.16.840.1.113883.1.11.18877")
            if self.payer.relationship_to_subscriber:
                code_elem.set("displayName", self.payer.relationship_to_subscriber)
        elif self.payer.relationship_to_subscriber:
            code_elem.set("nullFlavor", "OTH")
            orig_text = etree.SubElement(code_elem, f"{{{NS}}}originalText")
            orig_text.text = self.payer.relationship_to_subscriber
        else:
            # Default to "self"
            code_elem.set("nullFlavor", "UNK")

    def _add_subscriber_participant(self, act: etree._Element) -> None:
        """
        Add subscriber participant if different from patient.

        CONF:1198-8934: SHOULD contain participant
        CONF:1198-8935: typeCode="HLD"
        CONF:1198-16813/16815: templateId for Policy Holder Participant
        CONF:1198-8936: participantRole
        CONF:1198-8937/10120: participantRole/id (subscriber ID)
        CONF:1198-17139: Shall not be present if subscriber is patient
        """
        participant = etree.SubElement(act, f"{{{NS}}}participant", typeCode="HLD")

        # Add template ID (CONF:1198-16813, CONF:1198-16815)
        template = etree.SubElement(participant, f"{{{NS}}}templateId")
        template.set("root", "2.16.840.1.113883.10.20.22.4.90")

        # Add participantRole (CONF:1198-8936)
        role = etree.SubElement(participant, f"{{{NS}}}participantRole")

        # Add subscriber ID (CONF:1198-8937, CONF:1198-10120)
        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=self.payer.subscriber_id,
        ).to_element()
        role.append(id_elem)

    def _add_authorization_entry(self, act: etree._Element) -> None:
        """
        Add authorization entryRelationship.

        CONF:1198-8939: SHALL contain at least one entryRelationship
        CONF:1198-8940: typeCode="REFR"
        CONF:1198-8942/8943: Target is authorization or coverage plan description

        For simplicity, we create a basic plan description act.
        """
        entry_rel = etree.SubElement(
            act,
            f"{{{NS}}}entryRelationship",
            typeCode="REFR",
        )

        # Create a simple act for plan description (CONF:1198-8942, CONF:1198-8943)
        plan_act = etree.SubElement(
            entry_rel,
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="DEF",
        )

        # Add plan ID if we have group number (CONF:1198-8943)
        if self.payer.group_number:
            plan_id = Identifier(
                root="2.16.840.1.113883.19",
                extension=self.payer.group_number,
            ).to_element()
            plan_act.append(plan_id)

        # Add plan text/name (CONF:1198-8943)
        text_elem = etree.SubElement(plan_act, f"{{{NS}}}text")
        text_elem.text = f"{self.payer.insurance_type} - {self.payer.payer_name}"
