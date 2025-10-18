"""Allergy Observation entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.allergy import AllergyProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class AllergyObservation(CDAElement):
    """
    Builder for C-CDA Allergy Intolerance Observation entry.

    Represents a single allergy or intolerance with allergen, reaction, and severity.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.7",
                extension="2014-06-09",
                description="Allergy Intolerance Observation R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.7",
                extension="2014-06-09",
                description="Allergy Intolerance Observation R2.0",
            ),
        ],
    }

    # Code system OIDs
    SNOMED_OID = "2.16.840.1.113883.6.96"  # SNOMED CT
    RXNORM_OID = "2.16.840.1.113883.6.88"  # RxNorm (for medications)
    UNII_OID = "2.16.840.1.113883.4.9"  # UNII (for substances)

    # Allergy type codes (SNOMED CT)
    ALLERGY_TYPE_CODES = {
        "allergy": ("419199007", "Allergy to substance"),
        "intolerance": ("420134006", "Propensity to adverse reactions"),
    }

    # Severity codes (SNOMED CT)
    SEVERITY_CODES = {
        "mild": ("255604002", "Mild"),
        "moderate": ("6736007", "Moderate"),
        "severe": ("24484000", "Severe"),
        "fatal": ("399166001", "Fatal"),
    }

    # Status codes mapping
    STATUS_CODES = {
        "active": "active",
        "resolved": "completed",
        "inactive": "completed",
    }

    def __init__(
        self,
        allergy: AllergyProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize AllergyObservation builder.

        Args:
            allergy: Allergy data satisfying AllergyProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.allergy = allergy

    def build(self) -> etree.Element:
        """
        Build Allergy Intolerance Observation XML element.

        Returns:
            lxml Element for observation
        """
        # Create observation element with required attributes
        obs = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template IDs
        self.add_template_ids(obs)

        # Add ID
        self._add_id(obs)

        # Add code for allergy observation type
        self._add_observation_code(obs)

        # Add status code
        status = self._map_status(self.allergy.status)
        status_elem = StatusCode(status).to_element()
        obs.append(status_elem)

        # Add effective time (onset date) if available
        if self.allergy.onset_date:
            self._add_effective_time(obs)

        # Add value for allergy/intolerance type
        self._add_value(obs)

        # Add participant for allergen
        self._add_allergen_participant(obs)

        # Add reaction if available
        if self.allergy.reaction:
            self._add_reaction(obs)

        # Add severity if available
        if self.allergy.severity:
            self._add_severity(obs)

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

    def _add_observation_code(self, obs: etree._Element) -> None:
        """
        Add code element for allergy observation type.

        Args:
            obs: observation element
        """
        code_elem = etree.SubElement(obs, f"{{{NS}}}code")
        code_elem.set("code", "ASSERTION")
        code_elem.set("codeSystem", "2.16.840.1.113883.5.4")
        code_elem.set("codeSystemName", "ActCode")
        code_elem.set("displayName", "Assertion")

    def _add_effective_time(self, obs: etree._Element) -> None:
        """
        Add effectiveTime with onset date.

        Args:
            obs: observation element
        """
        time_elem = EffectiveTime(value=self.allergy.onset_date).to_element()
        obs.append(time_elem)

    def _add_value(self, obs: etree._Element) -> None:
        """
        Add value element for allergy/intolerance type.

        Args:
            obs: observation element
        """
        allergy_type = self.allergy.allergy_type.lower()
        type_info = self.ALLERGY_TYPE_CODES.get(allergy_type)

        value_elem = etree.SubElement(obs, f"{{{NS}}}value")
        value_elem.set(f"{{{NS}}}type", "CD")

        if type_info:
            code, display = type_info
            value_elem.set("code", code)
            value_elem.set("codeSystem", self.SNOMED_OID)
            value_elem.set("codeSystemName", "SNOMED CT")
            value_elem.set("displayName", display)
        else:
            # Use originalText if type not found
            value_elem.set("nullFlavor", "OTH")
            text_elem = etree.SubElement(value_elem, f"{{{NS}}}originalText")
            text_elem.text = self.allergy.allergy_type

    def _add_allergen_participant(self, obs: etree._Element) -> None:
        """
        Add participant element for the allergen.

        Args:
            obs: observation element
        """
        participant = etree.SubElement(
            obs,
            f"{{{NS}}}participant",
            typeCode="CSM",
        )

        participant_role = etree.SubElement(
            participant,
            f"{{{NS}}}participantRole",
            classCode="MANU",
        )

        playing_entity = etree.SubElement(
            participant_role,
            f"{{{NS}}}playingEntity",
            classCode="MMAT",
        )

        # Add allergen code
        code_elem = etree.SubElement(playing_entity, f"{{{NS}}}code")

        if self.allergy.allergen_code and self.allergy.allergen_code_system:
            code_elem.set("code", self.allergy.allergen_code)

            # Map code system to OID
            code_system_oid = self._get_code_system_oid(self.allergy.allergen_code_system)
            code_elem.set("codeSystem", code_system_oid)
            code_elem.set("codeSystemName", self.allergy.allergen_code_system)
            code_elem.set("displayName", self.allergy.allergen)
        else:
            # Use originalText if no code available
            code_elem.set("nullFlavor", "OTH")
            text_elem = etree.SubElement(code_elem, f"{{{NS}}}originalText")
            text_elem.text = self.allergy.allergen

    def _add_reaction(self, obs: etree._Element) -> None:
        """
        Add reaction as entryRelationship.

        Args:
            obs: observation element
        """
        entry_rel = etree.SubElement(
            obs,
            f"{{{NS}}}entryRelationship",
            typeCode="MFST",
            inversionInd="true",
        )

        reaction_obs = etree.SubElement(
            entry_rel,
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template ID for reaction observation
        template_id = etree.SubElement(reaction_obs, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.9")
        if self.version == CDAVersion.R2_1:
            template_id.set("extension", "2014-06-09")

        # Add code for reaction
        code_elem = etree.SubElement(reaction_obs, f"{{{NS}}}code")
        code_elem.set("code", "ASSERTION")
        code_elem.set("codeSystem", "2.16.840.1.113883.5.4")

        # Add text with reaction
        text_elem = etree.SubElement(reaction_obs, f"{{{NS}}}text")
        text_elem.text = self.allergy.reaction

        # Add status code
        status_elem = etree.SubElement(reaction_obs, f"{{{NS}}}statusCode")
        status_elem.set("code", "completed")

        # Add value (use SNOMED CT if we want to be more specific)
        value_elem = etree.SubElement(reaction_obs, f"{{{NS}}}value")
        value_elem.set(f"{{{NS}}}type", "CD")
        value_elem.set("nullFlavor", "OTH")
        orig_text = etree.SubElement(value_elem, f"{{{NS}}}originalText")
        orig_text.text = self.allergy.reaction

    def _add_severity(self, obs: etree._Element) -> None:
        """
        Add severity as entryRelationship.

        Args:
            obs: observation element
        """
        # This method is only called when severity is not None (guarded by caller)
        assert self.allergy.severity is not None

        entry_rel = etree.SubElement(
            obs,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",
            inversionInd="true",
        )

        severity_obs = etree.SubElement(
            entry_rel,
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template ID for severity observation
        template_id = etree.SubElement(severity_obs, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.8")
        if self.version == CDAVersion.R2_1:
            template_id.set("extension", "2014-06-09")

        # Add code for severity
        code_elem = etree.SubElement(severity_obs, f"{{{NS}}}code")
        code_elem.set("code", "SEV")
        code_elem.set("codeSystem", "2.16.840.1.113883.5.4")
        code_elem.set("displayName", "Severity Observation")

        # Add text with severity
        text_elem = etree.SubElement(severity_obs, f"{{{NS}}}text")
        text_elem.text = self.allergy.severity

        # Add status code
        status_elem = etree.SubElement(severity_obs, f"{{{NS}}}statusCode")
        status_elem.set("code", "completed")

        # Add value with severity code
        severity_lower = self.allergy.severity.lower()
        severity_info = self.SEVERITY_CODES.get(severity_lower)

        value_elem = etree.SubElement(severity_obs, f"{{{NS}}}value")
        value_elem.set(f"{{{NS}}}type", "CD")

        if severity_info:
            code, display = severity_info
            value_elem.set("code", code)
            value_elem.set("codeSystem", self.SNOMED_OID)
            value_elem.set("codeSystemName", "SNOMED CT")
            value_elem.set("displayName", display)
        else:
            # Use originalText if severity not in predefined list
            value_elem.set("nullFlavor", "OTH")
            orig_text = etree.SubElement(value_elem, f"{{{NS}}}originalText")
            orig_text.text = self.allergy.severity

    def _get_code_system_oid(self, code_system: str) -> str:
        """
        Map code system name to OID.

        Args:
            code_system: Code system name

        Returns:
            Code system OID
        """
        code_system_map = {
            "rxnorm": self.RXNORM_OID,
            "unii": self.UNII_OID,
            "snomed ct": self.SNOMED_OID,
            "snomed": self.SNOMED_OID,
        }
        return code_system_map.get(code_system.lower(), self.UNII_OID)

    def _map_status(self, status: str) -> str:
        """
        Map allergy status to observation status code.

        Args:
            status: Allergy status

        Returns:
            observation status code
        """
        return self.STATUS_CODES.get(status.lower(), "active")
