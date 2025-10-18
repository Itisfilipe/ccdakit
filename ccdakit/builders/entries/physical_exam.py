"""Physical Exam entry builders for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.physical_exam import WoundObservationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class LongitudinalCareWoundObservation(CDAElement):
    """
    Builder for C-CDA Longitudinal Care Wound Observation entry.

    Represents a wound observation including type, location, and characteristics.
    Supports both R2.1 (2015-08-01) and R2.0 (2015-08-01) versions.

    Conforms to:
    - Longitudinal Care Wound Observation (V2): 2.16.840.1.113883.10.20.22.4.114:2015-08-01
    - Problem Observation (V3): 2.16.840.1.113883.10.20.22.4.4:2015-08-01
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.114",
                extension="2015-08-01",
                description="Longitudinal Care Wound Observation (V2)",
            ),
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.4",
                extension="2015-08-01",
                description="Problem Observation (V3)",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.114",
                extension="2015-08-01",
                description="Longitudinal Care Wound Observation (V2)",
            ),
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.4",
                extension="2015-08-01",
                description="Problem Observation (V3)",
            ),
        ],
    }

    # Code system OIDs
    SNOMED_OID = "2.16.840.1.113883.6.96"  # SNOMED CT
    ACTCODE_OID = "2.16.840.1.113883.5.4"  # HL7ActCode

    def __init__(
        self,
        wound_observation: WoundObservationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize LongitudinalCareWoundObservation builder.

        Args:
            wound_observation: Wound observation data satisfying WoundObservationProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.wound_observation = wound_observation

    def build(self) -> etree.Element:
        """
        Build Longitudinal Care Wound Observation XML element.

        Returns:
            lxml Element for observation
        """
        # Create observation element
        observation = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template IDs (CONF:1198-32947, CONF:1198-29474, CONF:1198-32913)
        self.add_template_ids(observation)

        # Add ID
        self._add_id(observation)

        # Add code - ASSERTION (CONF:1198-29476, CONF:1198-29477, CONF:1198-31010)
        code_elem = etree.SubElement(observation, f"{{{NS}}}code")
        code_elem.set("code", "ASSERTION")
        code_elem.set("codeSystem", self.ACTCODE_OID)
        code_elem.set("codeSystemName", "HL7ActCode")
        code_elem.set("displayName", "Assertion")

        # Add status code (from Problem Observation template)
        status_elem = StatusCode("completed").to_element()
        observation.append(status_elem)

        # Add effective time
        time_elem = EffectiveTime(value=self.wound_observation.date).to_element()
        observation.append(time_elem)

        # Add value with wound type (CONF:1198-29485)
        self._add_value(observation)

        # Add target site code if location provided (CONF:1198-29488)
        if self.wound_observation.location and self.wound_observation.location_code:
            self._add_target_site(observation)

        return observation

    def _add_id(self, observation: etree._Element) -> None:
        """
        Add ID element to observation.

        Args:
            observation: observation element
        """
        import uuid

        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=str(uuid.uuid4()),
        ).to_element()
        observation.append(id_elem)

    def _add_value(self, observation: etree._Element) -> None:
        """
        Add value element with wound type (CONF:1198-29485).

        Args:
            observation: observation element
        """
        value_elem = etree.SubElement(
            observation,
            f"{{{NS}}}value",
            attrib={
                "{http://www.w3.org/2001/XMLSchema-instance}type": "CD",
            },
        )
        value_elem.set("code", self.wound_observation.wound_code)
        value_elem.set("codeSystem", self.SNOMED_OID)
        value_elem.set("codeSystemName", "SNOMED CT")
        value_elem.set("displayName", self.wound_observation.wound_type)

    def _add_target_site(self, observation: etree._Element) -> None:
        """
        Add targetSiteCode element with body location (CONF:1198-29488).

        Args:
            observation: observation element
        """
        target_site = etree.SubElement(observation, f"{{{NS}}}targetSiteCode")
        target_site.set("code", self.wound_observation.location_code)
        target_site.set("codeSystem", self.SNOMED_OID)
        target_site.set("codeSystemName", "SNOMED CT")
        target_site.set("displayName", self.wound_observation.location)

        # Add laterality qualifier if provided (CONF:1198-29490, CONF:1198-29491, CONF:1198-29492)
        if self.wound_observation.laterality and self.wound_observation.laterality_code:
            qualifier = etree.SubElement(target_site, f"{{{NS}}}qualifier")

            # Add name element with laterality code (CONF:1198-29491, CONF:1198-29492, CONF:1198-31524)
            name = etree.SubElement(qualifier, f"{{{NS}}}name")
            name.set("code", "272741003")  # laterality
            name.set("codeSystem", self.SNOMED_OID)
            name.set("displayName", "Laterality")

            # Add value element with specific laterality (CONF:1198-29493, CONF:1198-29494)
            value = etree.SubElement(qualifier, f"{{{NS}}}value")
            value.set("code", self.wound_observation.laterality_code)
            value.set("codeSystem", self.SNOMED_OID)
            value.set("displayName", self.wound_observation.laterality)
