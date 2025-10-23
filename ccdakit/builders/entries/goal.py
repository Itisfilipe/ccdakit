"""Goal Observation entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.goal import GoalProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class GoalObservation(CDAElement):
    """
    Builder for C-CDA Goal Observation entry (V2).

    Represents a patient health goal with status, dates, and values.
    Supports R2.1 version (2022-06-01).

    Template ID: 2.16.840.1.113883.10.20.22.4.121
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.121",
                extension="2022-06-01",
                description="Goal Observation V2",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.121",
                extension="2022-06-01",
                description="Goal Observation V2",
            ),
        ],
    }

    # Code system OIDs
    LOINC_OID = "2.16.840.1.113883.6.1"
    SNOMED_OID = "2.16.840.1.113883.6.96"
    UCUM_OID = "2.16.840.1.113883.6.8"

    # Status codes mapping (ActStatus value set)
    STATUS_CODES = {
        "active": "active",
        "cancelled": "cancelled",
        "completed": "completed",
        "on-hold": "on-hold",
        "suspended": "suspended",
        "aborted": "aborted",
        "new": "new",
    }

    def __init__(
        self,
        goal: GoalProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize GoalObservation builder.

        Args:
            goal: Goal data satisfying GoalProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.goal = goal

    def build(self) -> etree.Element:
        """
        Build Goal Observation XML element.

        Returns:
            lxml Element for observation
        """
        # Create observation element with required attributes (CONF:4515-30418, CONF:4515-30419)
        observation = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="GOL",  # GOL = Goal mood
        )

        # Add template IDs (CONF:4515-8583, CONF:4515-10512, CONF:4515-32886)
        self.add_template_ids(observation)

        # Add IDs (CONF:4515-32332)
        self._add_ids(observation)

        # Add code (CONF:4515-30784)
        self._add_code(observation)

        # Add status code (CONF:4515-32333, CONF:4515-32334)
        status = self._map_status(self.goal.status)
        status_elem = StatusCode(status).to_element()
        observation.append(status_elem)

        # Add effective time (CONF:4515-32335)
        self._add_effective_time(observation)

        # Add value if present (CONF:4515-32743)
        self._add_value(observation)

        return observation

    def _add_ids(self, observation: etree._Element) -> None:
        """
        Add ID elements to observation.

        Args:
            observation: observation element
        """
        # Add a generated ID (required: at least one [1..*])
        import uuid

        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=str(uuid.uuid4()),
        ).to_element()
        observation.append(id_elem)

    def _add_code(self, observation: etree._Element) -> None:
        """
        Add code element for goal type.

        Args:
            observation: observation element
        """
        # Use provided code or default to generic goal code
        if self.goal.code and self.goal.code_system:
            # Determine code system OID
            code_system = self.goal.code_system.upper()
            if "LOINC" in code_system:
                system_oid = self.LOINC_OID
                system_name = "LOINC"
            elif "SNOMED" in code_system:
                system_oid = self.SNOMED_OID
                system_name = "SNOMED CT"
            else:
                system_oid = self.goal.code_system
                system_name = self.goal.code_system

            code_elem = etree.SubElement(observation, f"{{{NS}}}code")
            code_elem.set("code", self.goal.code)
            code_elem.set("codeSystem", system_oid)
            if system_name:
                code_elem.set("codeSystemName", system_name)
            if self.goal.display_name:
                code_elem.set("displayName", self.goal.display_name)
        else:
            # Default: use a generic goal code from LOINC
            # Note: Per spec, code SHOULD be from LOINC (CONF:4515-30784)
            code_elem = etree.SubElement(observation, f"{{{NS}}}code")
            code_elem.set("code", "ASSERTION")
            code_elem.set("codeSystem", "2.16.840.1.113883.5.4")
            code_elem.set("displayName", "Assertion")

    def _add_effective_time(self, observation: etree._Element) -> None:
        """
        Add effectiveTime with start and optionally target dates.

        Args:
            observation: observation element
        """
        # SHOULD contain effectiveTime (CONF:4515-32335)
        if self.goal.start_date or self.goal.target_date:
            time_elem = EffectiveTime(
                low=self.goal.start_date,
                high=self.goal.target_date,
            ).to_element()
            observation.append(time_elem)

    def _add_value(self, observation: etree._Element) -> None:
        """
        Add value element with goal value.

        Args:
            observation: observation element
        """
        # MAY contain value (CONF:4515-32743)
        if self.goal.value:
            if self.goal.value_unit:
                # Physical Quantity (PQ) with unit
                value = etree.SubElement(observation, f"{{{NS}}}value")
                value.set("{http://www.w3.org/2001/XMLSchema-instance}type", "PQ")
                value.set("value", str(self.goal.value))
                value.set("unit", self.goal.value_unit)
            else:
                # String or coded value
                value = etree.SubElement(observation, f"{{{NS}}}value")
                value.set("{http://www.w3.org/2001/XMLSchema-instance}type", "ST")
                value.text = str(self.goal.value)
        elif self.goal.description:
            # If no coded value, use description as text value
            value = etree.SubElement(observation, f"{{{NS}}}value")
            value.set("{http://www.w3.org/2001/XMLSchema-instance}type", "ST")
            value.text = self.goal.description

    def _map_status(self, status: str) -> str:
        """
        Map goal status to observation status code.

        Args:
            status: Goal status

        Returns:
            Observation status code from ActStatus value set
        """
        normalized = status.lower().replace("_", "-")
        return self.STATUS_CODES.get(normalized, "active")
