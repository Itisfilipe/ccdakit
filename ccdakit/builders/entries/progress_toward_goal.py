"""Progress Toward Goal Observation entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.health_status_evaluation import ProgressTowardGoalProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class ProgressTowardGoalObservation(CDAElement):
    """
    Builder for C-CDA Progress Toward Goal Observation entry.

    This template represents a patient's progress toward a goal. It can describe
    whether a goal has been achieved or not and can also describe movement a
    patient is making toward the achievement of a goal.

    Template ID: 2.16.840.1.113883.10.20.22.4.110

    Conformance Rules:
    - SHALL contain classCode="OBS" (CONF:1098-31418)
    - SHALL contain moodCode="EVN" (CONF:1098-31419)
    - SHALL contain at least one [1..*] id (CONF:1098-31422)
    - SHALL contain code="ASSERTION" (CONF:1098-31423, CONF:1098-31424, CONF:1098-31425)
    - SHALL contain statusCode="completed" (CONF:1098-31609, CONF:1098-31610)
    - SHALL contain value from Goal Achievement value set (CONF:1098-31426)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.110",
                extension=None,
                description="Progress Toward Goal Observation",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.110",
                extension=None,
                description="Progress Toward Goal Observation",
            ),
        ],
    }

    # Code system OIDs
    ACT_CODE_OID = "2.16.840.1.113883.5.4"
    SNOMED_OID = "2.16.840.1.113883.6.96"

    def __init__(
        self,
        progress: ProgressTowardGoalProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ProgressTowardGoalObservation builder.

        Args:
            progress: Progress data satisfying ProgressTowardGoalProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.progress = progress

    def build(self) -> etree.Element:
        """
        Build Progress Toward Goal Observation XML element.

        Returns:
            lxml Element for observation
        """
        # Create observation element with required attributes (CONF:1098-31418, CONF:1098-31419)
        observation = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template ID (CONF:1098-31420, CONF:1098-31421)
        self.add_template_ids(observation)

        # Add IDs (CONF:1098-31422) - SHALL contain at least one [1..*]
        self._add_ids(observation)

        # Add code (CONF:1098-31423, CONF:1098-31424, CONF:1098-31425)
        # Fixed code: ASSERTION from HL7ActCode
        code_elem = Code(
            code="ASSERTION",
            system="HL7ActCode",
            display_name="Assertion",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        observation.append(code_elem)

        # Add statusCode (CONF:1098-31609, CONF:1098-31610)
        # SHALL be "completed"
        status_elem = StatusCode("completed").to_element()
        observation.append(status_elem)

        # Add value (CONF:1098-31426)
        # SHALL be from Goal Achievement value set
        self._add_value(observation)

        return observation

    def _add_ids(self, observation: etree._Element) -> None:
        """
        Add ID elements to observation.

        Args:
            observation: observation element
        """
        # Use provided ID or generate one
        if hasattr(self.progress, "id") and self.progress.id:
            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(self.progress.id),
            ).to_element()
            observation.append(id_elem)
        else:
            # Generate a UUID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            observation.append(id_elem)

    def _add_value(self, observation: etree._Element) -> None:
        """
        Add value element with achievement code.

        Value SHALL be from Goal Achievement value set (2.16.840.1.113883.11.20.9.55).

        Common codes from SNOMED CT:
        - 385641008: Improving (finding)
        - 260388006: No status change (finding)
        - 161788003: Condition resolved (finding)
        - 162598000: Goal not achieved (finding)

        Args:
            observation: observation element
        """
        # Create value element with xsi:type="CD"
        value = etree.SubElement(observation, f"{{{NS}}}value")
        value.set("{http://www.w3.org/2001/XMLSchema-instance}type", "CD")

        # Determine code system OID
        if hasattr(self.progress, "achievement_code_system") and self.progress.achievement_code_system:
            code_system = self.progress.achievement_code_system
            # If it's a name like "SNOMED", convert to OID
            if "SNOMED" in code_system.upper():
                code_system_oid = self.SNOMED_OID
                code_system_name = "SNOMED CT"
            else:
                code_system_oid = code_system
                code_system_name = None
        else:
            # Default to SNOMED CT (most codes in Goal Achievement value set are SNOMED)
            code_system_oid = self.SNOMED_OID
            code_system_name = "SNOMED CT"

        # Add code attributes
        value.set("code", self.progress.achievement_code)
        value.set("codeSystem", code_system_oid)

        if code_system_name:
            value.set("codeSystemName", code_system_name)

        if hasattr(self.progress, "achievement_display_name") and self.progress.achievement_display_name:
            value.set("displayName", self.progress.achievement_display_name)
