"""Planned Observation entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.plan_of_treatment import PlannedObservationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class PlannedObservation(CDAElement):
    """
    Builder for C-CDA Planned Observation entry.

    Represents a planned observation with codes, dates, and status.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    Template ID: 2.16.840.1.113883.10.20.22.4.44
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.44",
                extension="2014-06-09",
                description="Planned Observation R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.44",
                extension="2014-06-09",
                description="Planned Observation R2.0",
            ),
        ],
    }

    def __init__(
        self,
        observation: PlannedObservationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PlannedObservation builder.

        Args:
            observation: Planned observation data
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.observation = observation

    def build(self) -> etree.Element:
        """
        Build Planned Observation XML element.

        Returns:
            lxml Element for observation
        """
        # Create observation element with required attributes (moodCode = INT for planned)
        observation = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="INT",  # Intent/Planned
        )

        # Add template IDs
        self.add_template_ids(observation)

        # Add IDs
        self._add_ids(observation)

        # Add code (observation type)
        if self.observation.code:
            code_elem = Code(
                code=self.observation.code,
                system=self.observation.code_system or "LOINC",
                display_name=self.observation.description,
            ).to_element()
            code_elem.tag = f"{{{NS}}}code"
            observation.append(code_elem)
        else:
            # If no code, use nullFlavor
            code_elem = etree.SubElement(observation, f"{{{NS}}}code")
            code_elem.set("nullFlavor", "UNK")

        # Add status code
        status = self._map_status(self.observation.status)
        status_elem = StatusCode(status).to_element()
        observation.append(status_elem)

        # Add effective time (planned date)
        if self.observation.planned_date:
            time_elem = EffectiveTime(value=self.observation.planned_date).to_element()
            observation.append(time_elem)

        return observation

    def _add_ids(self, observation: etree._Element) -> None:
        """
        Add ID elements to observation.

        Args:
            observation: observation element
        """
        # Add persistent ID if available
        if self.observation.persistent_id:
            pid = self.observation.persistent_id
            id_elem = Identifier(root=pid.root, extension=pid.extension).to_element()
            observation.append(id_elem)
        else:
            # Add a generated ID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            observation.append(id_elem)

    def _map_status(self, status: str) -> str:
        """
        Map activity status to observation status code.

        Args:
            status: Activity status

        Returns:
            Observation status code
        """
        status_map = {
            "active": "active",
            "cancelled": "cancelled",
            "completed": "completed",
            "on-hold": "suspended",
        }
        return status_map.get(status.lower(), "active")
