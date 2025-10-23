"""Mental Status entry builders for C-CDA documents."""

from datetime import date, datetime

from lxml import etree

from ccdakit.builders.common import EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.mental_status import (
    MentalStatusObservationProtocol,
    MentalStatusOrganizerProtocol,
)


# CDA namespace
NS = "urn:hl7-org:v3"


class MentalStatusObservation(CDAElement):
    """
    Builder for C-CDA Mental Status Observation entry (V3).

    Represents an observation about mental status from subjective/objective information.
    Template ID: 2.16.840.1.113883.10.20.22.4.74
    Supports R2.1 (2015-08-01) version.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.74",
                extension="2015-08-01",
                description="Mental Status Observation (V3) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.74",
                extension="2015-08-01",
                description="Mental Status Observation (V3) R2.0",
            ),
        ],
    }

    # Code system OIDs
    SNOMED_OID = "2.16.840.1.113883.6.96"
    LOINC_OID = "2.16.840.1.113883.6.1"

    def __init__(
        self,
        observation: MentalStatusObservationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize MentalStatusObservation builder.

        Args:
            observation: Mental status observation data
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.observation = observation

    def build(self) -> etree.Element:
        """
        Build Mental Status Observation XML element.

        Returns:
            lxml Element for observation

        CONF Rules Implemented:
            - CONF:1198-14249: classCode="OBS"
            - CONF:1198-14250: moodCode="EVN"
            - CONF:1198-14255, CONF:1198-14256, CONF:1198-32565: templateId
            - CONF:1198-14257: id [1..*]
            - CONF:1198-14591, CONF:1198-32788, CONF:1198-32789: code=373930000 (Cognitive function)
            - CONF:1198-32790, CONF:1198-32791, CONF:1198-32792: translation with LOINC
            - CONF:1198-14254, CONF:1198-19092: statusCode="completed"
            - CONF:1198-14261: effectiveTime [1..1]
            - CONF:1198-14263, CONF:1198-14271: value (CD, SHOULD be SNOMED)
        """
        # CONF:1198-14249, CONF:1198-14250
        obs = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # CONF:1198-14255, CONF:1198-14256, CONF:1198-32565: Add template IDs
        self.add_template_ids(obs)

        # CONF:1198-14257: Add IDs [1..*]
        self._add_ids(obs)

        # CONF:1198-14591, CONF:1198-32788, CONF:1198-32789: Add observation code
        # Code: 373930000 (Cognitive function) from SNOMED CT
        code_elem = etree.SubElement(obs, f"{{{NS}}}code")
        code_elem.set("code", "373930000")
        code_elem.set("codeSystem", self.SNOMED_OID)
        code_elem.set("codeSystemName", "SNOMED CT")
        code_elem.set("displayName", "Cognitive function")

        # CONF:1198-32790, CONF:1198-32791, CONF:1198-32792: Add translation
        translation = etree.SubElement(code_elem, f"{{{NS}}}translation")
        translation.set("code", "75275-8")
        translation.set("codeSystem", self.LOINC_OID)
        translation.set("codeSystemName", "LOINC")
        translation.set("displayName", "Cognitive Function")

        # CONF:1198-14254, CONF:1198-19092: Add status code
        status_elem = StatusCode("completed").to_element()
        obs.append(status_elem)

        # CONF:1198-14261: Add effectiveTime [1..1]
        self._add_effective_time(obs)

        # CONF:1198-14263, CONF:1198-14271: Add value (CD type, SHOULD be SNOMED)
        self._add_value(obs)

        return obs

    def _add_ids(self, obs: etree._Element) -> None:
        """
        Add ID elements to observation.

        Args:
            obs: observation element
        """
        # Add persistent ID if available
        if self.observation.persistent_id:
            pid = self.observation.persistent_id
            id_elem = Identifier(root=pid.root, extension=pid.extension).to_element()
            obs.append(id_elem)
        else:
            # Add a generated ID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            obs.append(id_elem)

    def _add_effective_time(self, obs: etree._Element) -> None:
        """
        Add effectiveTime element.

        Args:
            obs: observation element
        """
        obs_date = self.observation.observation_date

        # Convert date to datetime if needed
        if isinstance(obs_date, date) and not isinstance(obs_date, datetime):
            # For date only, use EffectiveTime with value
            time_elem = etree.SubElement(obs, f"{{{NS}}}effectiveTime")
            time_elem.set("value", obs_date.strftime("%Y%m%d"))
        else:
            # For datetime
            time_elem = EffectiveTime(value=obs_date).to_element()
            obs.append(time_elem)

    def _add_value(self, obs: etree._Element) -> None:
        """
        Add value element with mental status finding.

        Args:
            obs: observation element
        """
        value_elem = etree.SubElement(obs, f"{{{NS}}}value")
        value_elem.set("{http://www.w3.org/2001/XMLSchema-instance}type", "CD")

        # CONF:1198-14271: SHOULD contain SNOMED CT code
        if self.observation.value_code:
            value_elem.set("code", self.observation.value_code)
            value_elem.set("codeSystem", self.SNOMED_OID)
            value_elem.set("codeSystemName", "SNOMED CT")
            value_elem.set("displayName", self.observation.value)
        else:
            # If no code provided, use nullFlavor
            value_elem.set("nullFlavor", "OTH")
            # Add originalText
            orig_text = etree.SubElement(value_elem, f"{{{NS}}}originalText")
            orig_text.text = self.observation.value


class MentalStatusOrganizer(CDAElement):
    """
    Builder for C-CDA Mental Status Organizer entry (V3).

    Groups related mental status observations by category.
    Template ID: 2.16.840.1.113883.10.20.22.4.75
    Supports R2.1 (2015-08-01) version.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.75",
                extension="2015-08-01",
                description="Mental Status Organizer (V3) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.75",
                extension="2015-08-01",
                description="Mental Status Organizer (V3) R2.0",
            ),
        ],
    }

    # Code system OIDs
    ICF_OID = "2.16.840.1.113883.6.254"
    LOINC_OID = "2.16.840.1.113883.6.1"

    def __init__(
        self,
        organizer: MentalStatusOrganizerProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize MentalStatusOrganizer builder.

        Args:
            organizer: Mental status organizer data
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.organizer = organizer

    def build(self) -> etree.Element:
        """
        Build Mental Status Organizer XML element.

        Returns:
            lxml Element for organizer

        CONF Rules Implemented:
            - CONF:1198-14369: classCode="CLUSTER"
            - CONF:1198-14371: moodCode="EVN"
            - CONF:1198-14375, CONF:1198-14376, CONF:1198-32566: templateId
            - CONF:1198-14377: id [1..*]
            - CONF:1198-14378, CONF:1198-14697, CONF:1198-14698: code (SHOULD be ICF or LOINC)
            - CONF:1198-14372, CONF:1198-19093: statusCode="completed"
            - CONF:1198-32424: effectiveTime [0..1] (SHOULD)
            - CONF:1198-14373, CONF:1198-14381: component with Mental Status Observation [1..*]
        """
        # CONF:1198-14369, CONF:1198-14371
        org = etree.Element(
            f"{{{NS}}}organizer",
            classCode="CLUSTER",
            moodCode="EVN",
        )

        # CONF:1198-14375, CONF:1198-14376, CONF:1198-32566: Add template IDs
        self.add_template_ids(org)

        # CONF:1198-14377: Add IDs [1..*]
        self._add_ids(org)

        # CONF:1198-14378, CONF:1198-14697, CONF:1198-14698: Add code
        self._add_code(org)

        # CONF:1198-14372, CONF:1198-19093: Add status code
        status_elem = StatusCode("completed").to_element()
        org.append(status_elem)

        # CONF:1198-32424: Add effectiveTime if available (SHOULD)
        self._add_effective_time(org)

        # CONF:1198-14373, CONF:1198-14381: Add components with observations [1..*]
        for obs_data in self.organizer.observations:
            component = etree.SubElement(org, f"{{{NS}}}component")
            obs_builder = MentalStatusObservation(obs_data, version=self.version)
            component.append(obs_builder.to_element())

        return org

    def _add_ids(self, org: etree._Element) -> None:
        """
        Add ID elements to organizer.

        Args:
            org: organizer element
        """
        # Add persistent ID if available
        if self.organizer.persistent_id:
            pid = self.organizer.persistent_id
            id_elem = Identifier(root=pid.root, extension=pid.extension).to_element()
            org.append(id_elem)
        else:
            # Add a generated ID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            org.append(id_elem)

    def _add_code(self, org: etree._Element) -> None:
        """
        Add code element for organizer category.

        Args:
            org: organizer element
        """
        code_elem = etree.SubElement(org, f"{{{NS}}}code")
        code_elem.set("code", self.organizer.category_code)

        # CONF:1198-14698: SHOULD be ICF or LOINC
        code_system = self.organizer.category_code_system.upper()
        if "ICF" in code_system:
            code_elem.set("codeSystem", self.ICF_OID)
            code_elem.set("codeSystemName", "ICF")
        elif "LOINC" in code_system:
            code_elem.set("codeSystem", self.LOINC_OID)
            code_elem.set("codeSystemName", "LOINC")
        else:
            # Use as-is if OID provided
            code_elem.set("codeSystem", self.organizer.category_code_system)

        code_elem.set("displayName", self.organizer.category)

    def _add_effective_time(self, org: etree._Element) -> None:
        """
        Add effectiveTime element if available (optional).

        Args:
            org: organizer element
        """
        # CONF:1198-32424: SHOULD contain effectiveTime
        if self.organizer.effective_time_low or self.organizer.effective_time_high:
            time_elem = EffectiveTime(
                low=self.organizer.effective_time_low,
                high=self.organizer.effective_time_high,
            ).to_element()
            org.append(time_elem)
