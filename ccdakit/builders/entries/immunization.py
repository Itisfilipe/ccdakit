"""Immunization Activity entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.immunization import ImmunizationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class ImmunizationActivity(CDAElement):
    """
    Builder for C-CDA Immunization Activity entry.

    Represents a single immunization with vaccine codes, dates, lot number,
    and administration details. Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.52",
                extension="2015-08-01",
                description="Immunization Activity R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.52",
                extension="2014-06-09",
                description="Immunization Activity R2.0",
            ),
        ],
    }

    # Code system OIDs
    CVX_OID = "2.16.840.1.113883.12.292"  # CVX (Vaccines Administered)
    ROUTE_OID = "2.16.840.1.113883.3.26.1.1"  # NCI Thesaurus for routes
    SITE_OID = "2.16.840.1.113883.6.96"  # SNOMED CT for body sites

    # Status codes mapping
    STATUS_CODES = {
        "completed": "completed",
        "refused": "refused",
        "not-done": "refused",
        "active": "active",
    }

    # Common route codes (NCI Thesaurus)
    ROUTE_CODES = {
        "oral": "C38288",
        "intramuscular": "C28161",
        "subcutaneous": "C38299",
        "intradermal": "C38238",
        "intranasal": "C38284",
        "intravenous": "C38276",
    }

    # Common body site codes (SNOMED CT)
    SITE_CODES = {
        "left arm": "368208006",
        "right arm": "368209003",
        "left deltoid": "723979003",
        "right deltoid": "723980000",
        "left thigh": "61396006",
        "right thigh": "11207009",
        "left gluteus": "78333006",
        "right gluteus": "78333006",
    }

    def __init__(
        self,
        immunization: ImmunizationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ImmunizationActivity builder.

        Args:
            immunization: Immunization data satisfying ImmunizationProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.immunization = immunization

    def build(self) -> etree.Element:
        """
        Build Immunization Activity XML element.

        Returns:
            lxml Element for substanceAdministration
        """
        # Create substanceAdministration element with required attributes
        sub_admin = etree.Element(
            f"{{{NS}}}substanceAdministration",
            classCode="SBADM",
            moodCode="EVN",
            negationInd="false",
        )

        # Add template IDs
        self.add_template_ids(sub_admin)

        # Add ID
        self._add_id(sub_admin)

        # Add status code
        status = self._map_status(self.immunization.status)
        status_elem = StatusCode(status).to_element()
        sub_admin.append(status_elem)

        # Add effective time (administration date)
        self._add_effective_time(sub_admin)

        # Add route code if available
        if self.immunization.route:
            self._add_route_code(sub_admin)

        # Add site code if available
        if self.immunization.site:
            self._add_site_code(sub_admin)

        # Add dose quantity if available
        if self.immunization.dose_quantity:
            self._add_dose_quantity(sub_admin)

        # Add consumable (the actual vaccine)
        self._add_consumable(sub_admin)

        return sub_admin

    def _add_id(self, sub_admin: etree._Element) -> None:
        """
        Add ID element to substanceAdministration.

        Args:
            sub_admin: substanceAdministration element
        """
        import uuid

        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=str(uuid.uuid4()),
        ).to_element()
        sub_admin.append(id_elem)

    def _add_effective_time(self, sub_admin: etree._Element) -> None:
        """
        Add effectiveTime with administration date.

        Args:
            sub_admin: substanceAdministration element
        """
        time_elem = EffectiveTime(value=self.immunization.administration_date).to_element()
        sub_admin.append(time_elem)

    def _add_route_code(self, sub_admin: etree._Element) -> None:
        """
        Add routeCode element.

        Args:
            sub_admin: substanceAdministration element
        """
        assert self.immunization.route is not None
        route_lower = self.immunization.route.lower()
        route_code = self.ROUTE_CODES.get(route_lower)

        route_elem = etree.SubElement(sub_admin, f"{{{NS}}}routeCode")

        if route_code:
            route_elem.set("code", route_code)
            route_elem.set("codeSystem", self.ROUTE_OID)
            route_elem.set("codeSystemName", "NCI Thesaurus")
            route_elem.set("displayName", self.immunization.route)
        else:
            # Use originalText if code not found
            route_elem.set("nullFlavor", "OTH")
            text_elem = etree.SubElement(route_elem, f"{{{NS}}}originalText")
            text_elem.text = self.immunization.route

    def _add_site_code(self, sub_admin: etree._Element) -> None:
        """
        Add approachSiteCode element for body location.

        Args:
            sub_admin: substanceAdministration element
        """
        assert self.immunization.site is not None
        site_lower = self.immunization.site.lower()
        site_code = self.SITE_CODES.get(site_lower)

        site_elem = etree.SubElement(sub_admin, f"{{{NS}}}approachSiteCode")

        if site_code:
            site_elem.set("code", site_code)
            site_elem.set("codeSystem", self.SITE_OID)
            site_elem.set("codeSystemName", "SNOMED CT")
            site_elem.set("displayName", self.immunization.site)
        else:
            # Use originalText if code not found
            site_elem.set("nullFlavor", "OTH")
            text_elem = etree.SubElement(site_elem, f"{{{NS}}}originalText")
            text_elem.text = self.immunization.site

    def _add_dose_quantity(self, sub_admin: etree._Element) -> None:
        """
        Add doseQuantity element.

        Args:
            sub_admin: substanceAdministration element
        """
        assert self.immunization.dose_quantity is not None
        dose_elem = etree.SubElement(sub_admin, f"{{{NS}}}doseQuantity")

        # Try to parse dosage (e.g., "0.5 mL", "1 dose")
        dosage = self.immunization.dose_quantity.strip()
        parts = dosage.split(maxsplit=1)

        if len(parts) == 2:
            value, unit = parts
            # Check if value is numeric
            try:
                # Try to convert to float to validate it's a number
                float(value)
                dose_elem.set("value", value)
                dose_elem.set("unit", unit)
            except ValueError:
                # If value is not numeric, use originalText
                text_elem = etree.SubElement(dose_elem, f"{{{NS}}}originalText")
                text_elem.text = dosage
        else:
            # Use originalText for complex dosage
            text_elem = etree.SubElement(dose_elem, f"{{{NS}}}originalText")
            text_elem.text = dosage

    def _add_consumable(self, sub_admin: etree._Element) -> None:
        """
        Add consumable element with vaccine information.

        Args:
            sub_admin: substanceAdministration element
        """
        consumable = etree.SubElement(sub_admin, f"{{{NS}}}consumable")
        manufactured_product = etree.SubElement(
            consumable, f"{{{NS}}}manufacturedProduct", classCode="MANU"
        )

        # Add template ID for manufactured product
        template_id = etree.SubElement(manufactured_product, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.54")
        if self.version == CDAVersion.R2_1:
            template_id.set("extension", "2014-06-09")

        # Add manufactured material
        manufactured_material = etree.SubElement(
            manufactured_product, f"{{{NS}}}manufacturedMaterial"
        )

        # Add vaccine code (CVX)
        code_elem = etree.SubElement(manufactured_material, f"{{{NS}}}code")
        code_elem.set("code", self.immunization.cvx_code)
        code_elem.set("codeSystem", self.CVX_OID)
        code_elem.set("codeSystemName", "CVX")
        code_elem.set("displayName", self.immunization.vaccine_name)

        # Add lot number if available
        if self.immunization.lot_number:
            lot_elem = etree.SubElement(manufactured_material, f"{{{NS}}}lotNumberText")
            lot_elem.text = self.immunization.lot_number

        # Add manufacturer organization if available
        if self.immunization.manufacturer:
            self._add_manufacturer(manufactured_product)

    def _add_manufacturer(self, manufactured_product: etree._Element) -> None:
        """
        Add manufacturer organization element.

        Args:
            manufactured_product: manufacturedProduct element
        """
        org_elem = etree.SubElement(manufactured_product, f"{{{NS}}}manufacturerOrganization")

        # Add name
        name_elem = etree.SubElement(org_elem, f"{{{NS}}}name")
        name_elem.text = self.immunization.manufacturer

    def _map_status(self, status: str) -> str:
        """
        Map immunization status to substanceAdministration status code.

        Args:
            status: Immunization status

        Returns:
            substanceAdministration status code
        """
        return self.STATUS_CODES.get(status.lower(), "completed")
