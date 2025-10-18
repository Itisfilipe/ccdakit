"""Planned Medication Activity entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.plan_of_treatment import PlannedMedicationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class PlannedMedication(CDAElement):
    """
    Builder for C-CDA Planned Medication Activity entry.

    Represents a planned medication with codes, dates, and status.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    Template ID: 2.16.840.1.113883.10.20.22.4.42
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.42",
                extension="2014-06-09",
                description="Planned Medication Activity R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.42",
                extension="2014-06-09",
                description="Planned Medication Activity R2.0",
            ),
        ],
    }

    def __init__(
        self,
        medication: PlannedMedicationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PlannedMedication builder.

        Args:
            medication: Planned medication data
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.medication = medication

    def build(self) -> etree.Element:
        """
        Build Planned Medication Activity XML element.

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
        status = self._map_status(self.medication.status)
        status_elem = StatusCode(status).to_element()
        sub_admin.append(status_elem)

        # Add effective time (planned date)
        if self.medication.planned_date:
            time_elem = EffectiveTime(value=self.medication.planned_date).to_element()
            sub_admin.append(time_elem)

        # Add route code if specified
        if self.medication.route:
            route_elem = etree.SubElement(sub_admin, f"{{{NS}}}routeCode")
            route_elem.set("code", "C38288")  # Oral route as default
            route_elem.set("codeSystem", "2.16.840.1.113883.3.26.1.1")
            route_elem.set("codeSystemName", "NCI Thesaurus")
            route_elem.set("displayName", self.medication.route)

        # Add dose quantity if specified
        if self.medication.dose:
            dose_elem = etree.SubElement(sub_admin, f"{{{NS}}}doseQuantity")
            dose_elem.set("value", self.medication.dose)

        # Add consumable (medication information)
        self._add_consumable(sub_admin)

        return sub_admin

    def _add_ids(self, sub_admin: etree._Element) -> None:
        """
        Add ID elements to substanceAdministration.

        Args:
            sub_admin: substanceAdministration element
        """
        # Add persistent ID if available
        if self.medication.persistent_id:
            pid = self.medication.persistent_id
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
        Add consumable element with medication information.

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
        template.set("root", "2.16.840.1.113883.10.20.22.4.23")
        if self.version == CDAVersion.R2_1:
            template.set("extension", "2014-06-09")
        else:
            template.set("extension", "2014-06-09")

        # Add manufactured material
        material = etree.SubElement(
            manufactured_product,
            f"{{{NS}}}manufacturedMaterial",
        )

        # Add code (medication code)
        if self.medication.code:
            code_elem = Code(
                code=self.medication.code,
                system=self.medication.code_system or "RxNorm",
                display_name=self.medication.description,
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
