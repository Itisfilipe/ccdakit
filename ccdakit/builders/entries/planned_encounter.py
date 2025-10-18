"""Planned Encounter entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.plan_of_treatment import PlannedEncounterProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class PlannedEncounter(CDAElement):
    """
    Builder for C-CDA Planned Encounter entry.

    Represents a planned encounter with codes, dates, and status.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    Template ID: 2.16.840.1.113883.10.20.22.4.40
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.40",
                extension="2014-06-09",
                description="Planned Encounter R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.40",
                extension="2014-06-09",
                description="Planned Encounter R2.0",
            ),
        ],
    }

    def __init__(
        self,
        encounter: PlannedEncounterProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PlannedEncounter builder.

        Args:
            encounter: Planned encounter data
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.encounter = encounter

    def build(self) -> etree.Element:
        """
        Build Planned Encounter XML element.

        Returns:
            lxml Element for encounter
        """
        # Create encounter element with required attributes (moodCode = INT for planned)
        encounter = etree.Element(
            f"{{{NS}}}encounter",
            classCode="ENC",
            moodCode="INT",  # Intent/Planned
        )

        # Add template IDs
        self.add_template_ids(encounter)

        # Add IDs
        self._add_ids(encounter)

        # Add code (encounter type)
        if self.encounter.code:
            code_elem = Code(
                code=self.encounter.code,
                system=self.encounter.code_system or "CPT",
                display_name=self.encounter.description,
            ).to_element()
            code_elem.tag = f"{{{NS}}}code"
            encounter.append(code_elem)
        else:
            # If no code, use nullFlavor
            code_elem = etree.SubElement(encounter, f"{{{NS}}}code")
            code_elem.set("nullFlavor", "UNK")

        # Add status code
        status = self._map_status(self.encounter.status)
        status_elem = StatusCode(status).to_element()
        encounter.append(status_elem)

        # Add effective time (planned date)
        if self.encounter.planned_date:
            time_elem = EffectiveTime(value=self.encounter.planned_date).to_element()
            encounter.append(time_elem)

        return encounter

    def _add_ids(self, encounter: etree._Element) -> None:
        """
        Add ID elements to encounter.

        Args:
            encounter: encounter element
        """
        # Add persistent ID if available
        if self.encounter.persistent_id:
            pid = self.encounter.persistent_id
            id_elem = Identifier(root=pid.root, extension=pid.extension).to_element()
            encounter.append(id_elem)
        else:
            # Add a generated ID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            encounter.append(id_elem)

    def _map_status(self, status: str) -> str:
        """
        Map activity status to encounter status code.

        Args:
            status: Activity status

        Returns:
            Encounter status code
        """
        status_map = {
            "active": "active",
            "cancelled": "cancelled",
            "completed": "completed",
            "on-hold": "suspended",
        }
        return status_map.get(status.lower(), "active")
