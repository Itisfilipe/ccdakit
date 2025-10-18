"""Planned Supply entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.plan_of_treatment import PlannedSupplyProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class PlannedSupply(CDAElement):
    """
    Builder for C-CDA Planned Supply entry.

    Represents a planned supply with codes, dates, and status.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    Template ID: 2.16.840.1.113883.10.20.22.4.43
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.43",
                extension="2014-06-09",
                description="Planned Supply R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.43",
                extension="2014-06-09",
                description="Planned Supply R2.0",
            ),
        ],
    }

    def __init__(
        self,
        supply: PlannedSupplyProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PlannedSupply builder.

        Args:
            supply: Planned supply data
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.supply = supply

    def build(self) -> etree.Element:
        """
        Build Planned Supply XML element.

        Returns:
            lxml Element for supply
        """
        # Create supply element with required attributes (moodCode = INT for planned)
        supply = etree.Element(
            f"{{{NS}}}supply",
            classCode="SPLY",
            moodCode="INT",  # Intent/Planned
        )

        # Add template IDs
        self.add_template_ids(supply)

        # Add IDs
        self._add_ids(supply)

        # Add code (supply type)
        if self.supply.code:
            code_elem = Code(
                code=self.supply.code,
                system=self.supply.code_system or "SNOMED",
                display_name=self.supply.description,
            ).to_element()
            code_elem.tag = f"{{{NS}}}code"
            supply.append(code_elem)
        else:
            # If no code, use nullFlavor
            code_elem = etree.SubElement(supply, f"{{{NS}}}code")
            code_elem.set("nullFlavor", "UNK")

        # Add status code
        status = self._map_status(self.supply.status)
        status_elem = StatusCode(status).to_element()
        supply.append(status_elem)

        # Add effective time (planned date)
        if self.supply.planned_date:
            time_elem = EffectiveTime(value=self.supply.planned_date).to_element()
            supply.append(time_elem)

        # Add quantity if specified
        if self.supply.quantity:
            quantity_elem = etree.SubElement(supply, f"{{{NS}}}quantity")
            quantity_elem.set("value", str(self.supply.quantity))

        return supply

    def _add_ids(self, supply: etree._Element) -> None:
        """
        Add ID elements to supply.

        Args:
            supply: supply element
        """
        # Add persistent ID if available
        if self.supply.persistent_id:
            pid = self.supply.persistent_id
            id_elem = Identifier(root=pid.root, extension=pid.extension).to_element()
            supply.append(id_elem)
        else:
            # Add a generated ID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            supply.append(id_elem)

    def _map_status(self, status: str) -> str:
        """
        Map activity status to supply status code.

        Args:
            status: Activity status

        Returns:
            Supply status code
        """
        status_map = {
            "active": "active",
            "cancelled": "cancelled",
            "completed": "completed",
            "on-hold": "suspended",
        }
        return status_map.get(status.lower(), "active")
