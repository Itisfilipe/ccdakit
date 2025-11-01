"""Allergy Observation entry builder for C-CDA documents.

This module implements the C-CDA R2.1 Allergy - Intolerance Observation template
(2.16.840.1.113883.10.20.22.4.7:2014-06-09) exactly as specified in the standard.

Key conformance points:
- SHALL contain statusCode="completed" (observation is complete, not allergy status)
- SHALL contain effectiveTime with low (onset date)
- MAY contain effectiveTime/high (resolution date) if allergy is resolved
- MAY contain Allergy Status Observation (clinical status)
- SHOULD contain Reaction Observation(s) for manifestations
- SHOULD NOT contain Severity Observation (deprecated - use Criticality instead)
- SHOULD contain Criticality Observation
- SHOULD contain Author Participation(s)
"""

from datetime import date
from lxml import etree
from typing import Optional

from ccdakit.builders.common import EffectiveTime, Identifier, StatusCode, create_default_author_participation
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
        Build Allergy Intolerance Observation XML element per C-CDA R2.1 spec.

        Returns:
            lxml Element for observation conforming to template 2.16.840.1.113883.10.20.22.4.7:2014-06-09
        """
        # Create observation element with required attributes (CONF:1098-7379, CONF:1098-7380)
        obs = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # MAY contain negationInd (CONF:1098-31526)
        # Use to indicate allergy was not observed
        negation = getattr(self.allergy, 'negation_ind', None)
        if negation is not None:
            obs.set("negationInd", "true" if negation else "false")

        # Add template IDs (CONF:1098-7381)
        self.add_template_ids(obs)

        # SHALL contain at least one [1..*] id (CONF:1098-7382)
        self._add_id(obs)

        # SHALL contain exactly one [1..1] code (CONF:1098-15947)
        self._add_observation_code(obs)

        # SHALL contain exactly one [1..1] statusCode="completed" (CONF:1098-19084, CONF:1098-19085)
        # This represents that the observation has been completed, NOT the status of the allergy
        # The allergy clinical status is tracked in the Allergy Status Observation
        status_elem = StatusCode("completed").to_element()
        obs.append(status_elem)

        # SHALL contain exactly one [1..1] effectiveTime (CONF:1098-7387)
        # SHALL contain exactly one [1..1] low (CONF:1098-31538)
        # MAY contain zero or one [0..1] high (CONF:1098-31539)
        self._add_effective_time(obs)

        # SHALL contain exactly one [1..1] value with @xsi:type="CD" (CONF:1098-7390)
        # from ValueSet Allergy and Intolerance Type
        self._add_value(obs)

        # SHOULD contain zero or more [0..*] Author Participation (CONF:1098-31143)
        self._add_author_participation(obs)

        # SHALL contain exactly one [1..1] participant (CONF:1098-7402)
        self._add_allergen_participant(obs)

        # MAY contain zero or one [0..1] Allergy Status Observation (CONF:1098-32939)
        # Note: This is the clinical status (active/resolved), distinct from statusCode
        status = getattr(self.allergy, 'clinical_status', None)
        if status:
            self._add_allergy_status(obs, status)

        # SHOULD NOT contain Severity Observation (CONF:1098-9961)
        # Note: Severity is DEPRECATED for allergy observation
        # Kept only for backwards compatibility - will not be added to new implementations

        # SHOULD contain zero or more [0..*] Reaction Observation (CONF:1098-7447)
        # Add reaction manifestations
        if self.allergy.reaction:
            self._add_reaction(obs)

        # SHOULD contain zero or one [0..1] Criticality Observation (CONF:1098-32910)
        # Criticality is the preferred way to characterize allergy risk
        criticality = getattr(self.allergy, 'criticality', None)
        if criticality or self.allergy.severity:
            # Add criticality if explicitly provided, or infer from severity
            self._add_criticality(obs, criticality)

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
        Add effectiveTime with onset and optional resolution date.

        Per C-CDA spec (CONF:1098-7387):
        - SHALL contain exactly one [1..1] effectiveTime
        - SHALL contain exactly one [1..1] low (CONF:1098-31538) - onset date
        - MAY contain zero or one [0..1] high (CONF:1098-31539) - resolution date

        If allergy is resolved but resolution date unknown, high SHALL have nullFlavor="UNK".

        Args:
            obs: observation element
        """
        # Create effectiveTime with low/high interval format
        # MUST have xsi:type="IVL_TS" when using low/high children per XSD schema
        time_elem = etree.Element(f"{{{NS}}}effectiveTime")
        time_elem.set("{http://www.w3.org/2001/XMLSchema-instance}type", "IVL_TS")

        # SHALL contain low (onset date)
        low_elem = etree.SubElement(time_elem, f"{{{NS}}}low")
        if self.allergy.onset_date:
            low_elem.set("value", self.allergy.onset_date.strftime("%Y%m%d"))
        else:
            low_elem.set("nullFlavor", "UNK")

        # MAY contain high (resolution date) if allergy is resolved
        resolution_date = getattr(self.allergy, 'resolution_date', None)
        if resolution_date:
            high_elem = etree.SubElement(time_elem, f"{{{NS}}}high")
            if isinstance(resolution_date, date):
                high_elem.set("value", resolution_date.strftime("%Y%m%d"))
            else:
                # Resolved but date unknown
                high_elem.set("nullFlavor", "UNK")

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
        value_elem.set("{http://www.w3.org/2001/XMLSchema-instance}type", "CD")

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

    def _add_author_participation(self, obs: etree._Element) -> None:
        """
        Add Author Participation to the observation (CONF:1098-31143).

        Per C-CDA spec:
        - Allergy Observation SHOULD contain zero or more [0..*] Author Participation

        Args:
            obs: observation element
        """
        # Add default author participation using onset date as authoring time
        author_elem = create_default_author_participation(self.allergy.onset_date)
        obs.append(author_elem)

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

        # Add ID for reaction observation
        import uuid
        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=str(uuid.uuid4()),
        ).to_element()
        reaction_obs.append(id_elem)

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

        # Add effectiveTime for reaction (SHOULD per CONF:1098-7332)
        # SHOULD contain low (CONF:1098-7333) and high (CONF:1098-7334)
        # Use interval format (low/high) to satisfy CONF requirements
        time_elem = etree.SubElement(reaction_obs, f"{{{NS}}}effectiveTime")

        # Add low element for reaction onset
        low_elem = etree.SubElement(time_elem, f"{{{NS}}}low")
        if self.allergy.onset_date:
            low_elem.set("value", self.allergy.onset_date.strftime("%Y%m%d"))
        else:
            low_elem.set("nullFlavor", "UNK")

        # Add high element (use current time or null if reaction is ongoing)
        high_elem = etree.SubElement(time_elem, f"{{{NS}}}high")
        high_elem.set("nullFlavor", "UNK")  # Reaction end time typically unknown

        # Add value (use SNOMED CT if we want to be more specific)
        value_elem = etree.SubElement(reaction_obs, f"{{{NS}}}value")
        value_elem.set("{http://www.w3.org/2001/XMLSchema-instance}type", "CD")
        value_elem.set("nullFlavor", "OTH")
        orig_text = etree.SubElement(value_elem, f"{{{NS}}}originalText")
        orig_text.text = self.allergy.reaction

        # Add author participation (SHOULD per CONF:1198-31145)
        # Reaction Observation SHOULD contain zero or more [0..*] Author Participation
        author_elem = create_default_author_participation(self.allergy.onset_date)
        reaction_obs.append(author_elem)

    def _add_allergy_status(self, obs: etree._Element, clinical_status: str) -> None:
        """
        Add Allergy Status Observation as entryRelationship (CONF:1098-32939).

        This represents the clinical status of the allergy (active, inactive, resolved).
        This is DISTINCT from the observation statusCode which is always "completed".

        Args:
            obs: observation element
            clinical_status: Clinical status (active, inactive, resolved)
        """
        # MAY contain zero or one [0..1] entryRelationship (CONF:1098-32939)
        entry_rel = etree.SubElement(
            obs,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",  # CONF:1098-32940
            inversionInd="true",  # CONF:1098-32941
        )

        # SHALL contain Allergy Status Observation (CONF:1098-32942)
        status_obs = etree.SubElement(
            entry_rel,
            f"{{{NS}}}observation",
            classCode="OBS",  # CONF:1198-7318
            moodCode="EVN",  # CONF:1198-7319
        )

        # Template ID (CONF:1198-7317)
        template_id = etree.SubElement(status_obs, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.28")
        template_id.set("extension", "2019-06-20")  # CONF:1198-32962

        # Code (CONF:1198-7320)
        code_elem = etree.SubElement(status_obs, f"{{{NS}}}code")
        code_elem.set("code", "33999-4")  # CONF:1198-19131
        code_elem.set("codeSystem", "2.16.840.1.113883.6.1")  # LOINC (CONF:1198-32155)
        code_elem.set("codeSystemName", "LOINC")
        code_elem.set("displayName", "Status")

        # StatusCode (CONF:1198-7321)
        status_code_elem = etree.SubElement(status_obs, f"{{{NS}}}statusCode")
        status_code_elem.set("code", "completed")  # CONF:1198-19087

        # Value from Allergy Clinical Status value set (CONF:1198-7322)
        # Value set: 2.16.840.1.113762.1.4.1099.29
        value_elem = etree.SubElement(status_obs, f"{{{NS}}}value")
        value_elem.set("{http://www.w3.org/2001/XMLSchema-instance}type", "CE")

        # Map status to appropriate codes
        status_map = {
            "active": ("55561003", "Active"),
            "inactive": ("73425007", "Inactive"),
            "resolved": ("413322009", "Resolved"),
        }

        status_lower = clinical_status.lower()
        if status_lower in status_map:
            code, display = status_map[status_lower]
            value_elem.set("code", code)
            value_elem.set("codeSystem", "2.16.840.1.113883.6.96")  # SNOMED CT
            value_elem.set("codeSystemName", "SNOMED CT")
            value_elem.set("displayName", display)
        else:
            # Use originalText if status not in map
            value_elem.set("nullFlavor", "OTH")
            text_elem = etree.SubElement(value_elem, f"{{{NS}}}originalText")
            text_elem.text = clinical_status

    def _add_criticality(self, obs: etree._Element, criticality: Optional[str] = None) -> None:
        """
        Add Criticality Observation as entryRelationship (CONF:1098-32910).

        Per spec: SHOULD contain zero or one [0..1] Criticality Observation.
        Criticality indicates the potential for a more serious or life-threatening reaction.
        This is the PREFERRED way to characterize allergy risk (not Severity Observation).

        Args:
            obs: observation element
            criticality: Explicit criticality value, or None to infer from severity
        """
        # SHOULD contain zero or one [0..1] entryRelationship (CONF:1098-32910)
        entry_rel = etree.SubElement(
            obs,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",  # CONF:1098-32911
            inversionInd="true",  # CONF:1098-32912
        )

        # SHALL contain Criticality Observation (CONF:1098-32913)
        criticality_obs = etree.SubElement(
            entry_rel,
            f"{{{NS}}}observation",
            classCode="OBS",  # CONF:81-32921
            moodCode="EVN",  # CONF:81-32922
        )

        # Template ID (CONF:81-32918)
        # NOTE: Per spec, Criticality Observation has NO extension!
        template_id = etree.SubElement(criticality_obs, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.145")  # CONF:81-32923
        # NO extension per spec!

        # Code (CONF:81-32919)
        code_elem = etree.SubElement(criticality_obs, f"{{{NS}}}code")
        code_elem.set("code", "82606-5")  # CONF:81-32925
        code_elem.set("codeSystem", "2.16.840.1.113883.6.1")  # LOINC (CONF:81-32926)
        code_elem.set("codeSystemName", "LOINC")
        code_elem.set("displayName", "Criticality")

        # StatusCode (CONF:81-32920)
        status_elem = etree.SubElement(criticality_obs, f"{{{NS}}}statusCode")
        status_elem.set("code", "completed")  # CONF:81-32927

        # Value from Criticality Observation value set (CONF:81-32928)
        # Value set: 2.16.840.1.113883.1.11.20549
        value_elem = etree.SubElement(criticality_obs, f"{{{NS}}}value")
        value_elem.set("{http://www.w3.org/2001/XMLSchema-instance}type", "CD")

        # Use explicit criticality if provided, otherwise infer from severity
        if criticality:
            crit_lower = criticality.lower()
            if crit_lower in ["high", "crith"]:
                value_elem.set("code", "CRITH")
                value_elem.set("displayName", "High Criticality")
            elif crit_lower in ["low", "critl"]:
                value_elem.set("code", "CRITL")
                value_elem.set("displayName", "Low Criticality")
            else:
                value_elem.set("code", "CRITU")
                value_elem.set("displayName", "Unable to assess")
        elif self.allergy.severity:
            # Infer from severity
            sev_lower = self.allergy.severity.lower()
            if sev_lower in ["severe", "fatal"]:
                value_elem.set("code", "CRITH")
                value_elem.set("displayName", "High Criticality")
            else:
                value_elem.set("code", "CRITL")
                value_elem.set("displayName", "Low Criticality")
        else:
            # Default to unable to assess
            value_elem.set("code", "CRITU")
            value_elem.set("displayName", "Unable to assess")

        value_elem.set("codeSystem", "2.16.840.1.113883.5.1063")  # ObservationValue
        value_elem.set("codeSystemName", "ObservationValue")

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
