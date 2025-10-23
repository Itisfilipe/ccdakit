"""Health Concern Act entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.health_concern import HealthConcernProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class HealthConcernAct(CDAElement):
    """
    Builder for C-CDA Health Concern Act entry.

    Represents a health concern which may wrap various observations
    like problems, allergies, social history, etc.
    Supports both R2.1 (2015-08-01) and R2.0 (2015-08-01) versions.

    Per spec (2.16.840.1.113883.10.20.22.4.132):
    - classCode="ACT" (CONF:4515-30750)
    - moodCode="EVN" (CONF:4515-30751)
    - code="75310-3" Health Concern from LOINC (CONF:4515-32310)
    - statusCode from ProblemAct statusCode value set (CONF:4515-32313)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.132",
                extension="2022-06-01",
                description="Health Concern Act V3",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.132",
                extension="2015-08-01",
                description="Health Concern Act V2",
            ),
        ],
    }

    # Code system OIDs
    LOINC_OID = "2.16.840.1.113883.6.1"
    SNOMED_OID = "2.16.840.1.113883.6.96"

    # Status codes mapping (from ProblemAct statusCode value set)
    STATUS_CODES = {
        "active": "active",
        "suspended": "suspended",
        "aborted": "aborted",
        "completed": "completed",
    }

    def __init__(
        self,
        health_concern: HealthConcernProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize HealthConcernAct builder.

        Args:
            health_concern: Health concern data satisfying HealthConcernProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.health_concern = health_concern

    def build(self) -> etree.Element:
        """
        Build Health Concern Act XML element.

        Returns:
            lxml Element for act
        """
        # Create act element with required attributes (CONF:4515-30750, 4515-30751)
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="EVN",
        )

        # Add template IDs (CONF:4515-30752)
        self.add_template_ids(act)

        # Add IDs (CONF:4515-30754)
        self._add_ids(act)

        # Add code (75310-3 = Health Concern) (CONF:4515-32310)
        code_elem = Code(
            code="75310-3",
            system="LOINC",
            display_name="Health Concern",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        act.append(code_elem)

        # Add status code (CONF:4515-30758)
        status = self._map_status(self.health_concern.status)
        status_elem = StatusCode(status).to_element()
        act.append(status_elem)

        # Add effective time (CONF:4515-30759)
        self._add_effective_time(act)

        # Add entry relationships for observations (CONF:4515-30761 and others)
        self._add_observations(act)

        return act

    def _add_ids(self, act: etree._Element) -> None:
        """
        Add ID elements to act.

        Per CONF:4515-30754, SHALL contain at least one [1..*] id.

        Args:
            act: act element
        """
        # Add persistent ID if available
        if self.health_concern.persistent_id:
            pid = self.health_concern.persistent_id
            id_elem = Identifier(root=pid.root, extension=pid.extension).to_element()
            act.append(id_elem)
        else:
            # Add a generated ID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            act.append(id_elem)

    def _add_effective_time(self, act: etree._Element) -> None:
        """
        Add effectiveTime with low and optionally high dates.

        Per CONF:4515-30759, MAY contain zero or one [0..1] effectiveTime.
        The effectiveTime reflects when the condition was felt to be a concern.

        Args:
            act: act element
        """
        if self.health_concern.effective_time_low or self.health_concern.effective_time_high:
            time_elem = EffectiveTime(
                low=self.health_concern.effective_time_low,
                high=self.health_concern.effective_time_high,
            ).to_element()
            act.append(time_elem)

    def _add_observations(self, act: etree._Element) -> None:
        """
        Add entryRelationship elements for related observations.

        Per spec, Health Concern Act MAY contain:
        - Problem Observation (CONF:4515-30761)
        - Allergy Observation (CONF:4515-31007)
        - Social History Observation (CONF:4515-31253)
        - And many others...

        For simplicity, this implementation creates a basic observation structure
        that can be extended based on the observation_type.

        Args:
            act: act element
        """
        for observation in self.health_concern.observations:
            # Create entryRelationship with typeCode="REFR" (Refers to)
            entry_rel = etree.SubElement(
                act,
                f"{{{NS}}}entryRelationship",
                typeCode="REFR",
            )

            # Create observation element
            obs = etree.SubElement(
                entry_rel,
                f"{{{NS}}}observation",
                classCode="OBS",
                moodCode="EVN",
            )

            # Add template ID based on observation type
            self._add_observation_template(obs, observation.observation_type)

            # Add ID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            obs.append(id_elem)

            # Add code
            code_elem = etree.SubElement(obs, f"{{{NS}}}code")
            code_elem.set("code", observation.code)

            # Determine code system OID
            if observation.code_system.upper() in ["SNOMED", "SNOMED CT"]:
                code_elem.set("codeSystem", self.SNOMED_OID)
                code_elem.set("codeSystemName", "SNOMED CT")
            elif observation.code_system.upper() == "LOINC":
                code_elem.set("codeSystem", self.LOINC_OID)
                code_elem.set("codeSystemName", "LOINC")
            else:
                code_elem.set("codeSystem", observation.code_system)

            if observation.display_name:
                code_elem.set("displayName", observation.display_name)

            # Add status code
            status_elem = StatusCode("completed").to_element()
            obs.append(status_elem)

    def _add_observation_template(self, observation: etree._Element, obs_type: str) -> None:
        """
        Add appropriate template ID based on observation type.

        Args:
            observation: observation element
            obs_type: Type of observation
        """
        # Template ID mappings for common observation types
        template_mappings = {
            "problem": "2.16.840.1.113883.10.20.22.4.4",
            "allergy": "2.16.840.1.113883.10.20.22.4.7",
            "social_history": "2.16.840.1.113883.10.20.22.4.38",
            "vital_sign": "2.16.840.1.113883.10.20.22.4.27",
            "result": "2.16.840.1.113883.10.20.22.4.2",
            "smoking_status": "2.16.840.1.113883.10.20.22.4.78",
        }

        template_root = template_mappings.get(obs_type.lower())
        if template_root:
            template = etree.SubElement(observation, f"{{{NS}}}templateId")
            template.set("root", template_root)

    def _map_status(self, status: str) -> str:
        """
        Map health concern status to act status code.

        Args:
            status: Health concern status

        Returns:
            Act status code
        """
        return self.STATUS_CODES.get(status.lower(), "active")
