"""Planned Procedure entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.plan_of_treatment import PlannedProcedureProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class PlannedProcedure(CDAElement):
    """
    Builder for C-CDA Planned Procedure entry.

    Represents a planned procedure with codes, dates, and status.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    Template ID: 2.16.840.1.113883.10.20.22.4.41
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.41",
                extension="2014-06-09",
                description="Planned Procedure R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.41",
                extension="2014-06-09",
                description="Planned Procedure R2.0",
            ),
        ],
    }

    def __init__(
        self,
        procedure: PlannedProcedureProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PlannedProcedure builder.

        Args:
            procedure: Planned procedure data
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.procedure = procedure

    def build(self) -> etree.Element:
        """
        Build Planned Procedure XML element.

        Returns:
            lxml Element for procedure
        """
        # Create procedure element with required attributes (moodCode = INT for planned)
        procedure = etree.Element(
            f"{{{NS}}}procedure",
            classCode="PROC",
            moodCode="INT",  # Intent/Planned
        )

        # Add template IDs
        self.add_template_ids(procedure)

        # Add IDs
        self._add_ids(procedure)

        # Add code (procedure type)
        if self.procedure.code:
            code_elem = Code(
                code=self.procedure.code,
                system=self.procedure.code_system or "SNOMED",
                display_name=self.procedure.description,
            ).to_element()
            code_elem.tag = f"{{{NS}}}code"
            procedure.append(code_elem)
        else:
            # If no code, use nullFlavor
            code_elem = etree.SubElement(procedure, f"{{{NS}}}code")
            code_elem.set("nullFlavor", "UNK")

        # Add status code
        status = self._map_status(self.procedure.status)
        status_elem = StatusCode(status).to_element()
        procedure.append(status_elem)

        # Add effective time (planned date)
        if self.procedure.planned_date:
            time_elem = EffectiveTime(value=self.procedure.planned_date).to_element()
            procedure.append(time_elem)

        # Add target site code if body site specified
        if self.procedure.body_site:
            target_site = etree.SubElement(
                procedure,
                f"{{{NS}}}targetSiteCode",
            )
            target_site.set("code", "123037004")  # Body structure
            target_site.set("codeSystem", "2.16.840.1.113883.6.96")
            target_site.set("codeSystemName", "SNOMED CT")
            target_site.set("displayName", self.procedure.body_site)

        return procedure

    def _add_ids(self, procedure: etree._Element) -> None:
        """
        Add ID elements to procedure.

        Args:
            procedure: procedure element
        """
        # Add persistent ID if available
        if self.procedure.persistent_id:
            pid = self.procedure.persistent_id
            id_elem = Identifier(root=pid.root, extension=pid.extension).to_element()
            procedure.append(id_elem)
        else:
            # Add a generated ID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            procedure.append(id_elem)

    def _map_status(self, status: str) -> str:
        """
        Map activity status to procedure status code.

        Args:
            status: Activity status

        Returns:
            Procedure status code
        """
        status_map = {
            "active": "active",
            "cancelled": "cancelled",
            "completed": "completed",
            "on-hold": "suspended",
        }
        return status_map.get(status.lower(), "active")
