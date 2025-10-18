"""Planned Immunization Activity entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.plan_of_treatment import PlannedImmunizationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class PlannedImmunization(CDAElement):
    """
    Builder for C-CDA Planned Immunization Activity entry.

    Represents a planned immunization with codes, dates, and status.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    Template ID: 2.16.840.1.113883.10.20.22.4.120
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.120",
                extension="2014-06-09",
                description="Planned Immunization Activity",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.120",
                extension="2014-06-09",
                description="Planned Immunization Activity",
            ),
        ],
    }

    def __init__(
        self,
        immunization: PlannedImmunizationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PlannedImmunization builder.

        Args:
            immunization: Planned immunization data
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.immunization = immunization

    def build(self) -> etree.Element:
        """
        Build Planned Immunization Activity XML element.

        Returns:
            lxml Element for substanceAdministration
        """
        # Create substanceAdministration element (moodCode = INT for planned)
        sub_admin = etree.Element(
            f"{{{NS}}}substanceAdministration",
            classCode="SBADM",
            moodCode="INT",  # Intent/Planned
        )

        # Add template IDs
        self.add_template_ids(sub_admin)

        # Add IDs
        self._add_ids(sub_admin)

        # Add status code
        status = self._map_status(self.immunization.status)
        status_elem = StatusCode(status).to_element()
        sub_admin.append(status_elem)

        # Add effective time (planned date)
        if self.immunization.planned_date:
            time_elem = EffectiveTime(value=self.immunization.planned_date).to_element()
            sub_admin.append(time_elem)

        # Add consumable (vaccine information)
        self._add_consumable(sub_admin)

        return sub_admin

    def _add_ids(self, sub_admin: etree._Element) -> None:
        """
        Add ID elements to substanceAdministration.

        Args:
            sub_admin: substanceAdministration element
        """
        # Add persistent ID if available
        if self.immunization.persistent_id:
            pid = self.immunization.persistent_id
            id_elem = Identifier(root=pid.root, extension=pid.extension).to_element()
            sub_admin.append(id_elem)
        else:
            # Add a generated ID
            import uuid

            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            sub_admin.append(id_elem)

    def _add_consumable(self, sub_admin: etree._Element) -> None:
        """
        Add consumable element with vaccine information.

        Args:
            sub_admin: substanceAdministration element
        """
        consumable = etree.SubElement(sub_admin, f"{{{NS}}}consumable")
        manufactured_product = etree.SubElement(
            consumable,
            f"{{{NS}}}manufacturedProduct",
            classCode="MANU",
        )

        # Add template ID for manufactured product
        template = etree.SubElement(manufactured_product, f"{{{NS}}}templateId")
        template.set("root", "2.16.840.1.113883.10.20.22.4.54")
        if self.version == CDAVersion.R2_1:
            template.set("extension", "2014-06-09")
        else:
            template.set("extension", "2014-06-09")

        # Add manufactured material
        material = etree.SubElement(
            manufactured_product,
            f"{{{NS}}}manufacturedMaterial",
        )

        # Add code (CVX vaccine code)
        vaccine_code = self.immunization.vaccine_code or self.immunization.code
        if vaccine_code:
            code_elem = Code(
                code=vaccine_code,
                system="CVX",
                display_name=self.immunization.description,
            ).to_element()
            code_elem.tag = f"{{{NS}}}code"
            material.append(code_elem)
        else:
            code_elem = etree.SubElement(material, f"{{{NS}}}code")
            code_elem.set("nullFlavor", "UNK")

    def _map_status(self, status: str) -> str:
        """
        Map activity status to substanceAdministration status code.

        Args:
            status: Activity status

        Returns:
            SubstanceAdministration status code
        """
        status_map = {
            "active": "active",
            "cancelled": "cancelled",
            "completed": "completed",
            "on-hold": "suspended",
        }
        return status_map.get(status.lower(), "active")
