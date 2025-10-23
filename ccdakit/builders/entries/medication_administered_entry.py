"""Medication Activity entry builder for administered medications in C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.medication_administered import MedicationAdministeredProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class MedicationAdministeredActivity(CDAElement):
    """
    Builder for C-CDA Medication Activity entry for administered medications.

    Represents a medication or fluid that was administered during a procedure,
    encounter, or other clinical activity. Uses the Medication Activity (V2)
    template (2.16.840.1.113883.10.20.22.4.16) with moodCode="EVN" for completed
    administrations.

    Template ID: 2.16.840.1.113883.10.20.22.4.16 (2014-06-09)

    Note: This differs from prescribed medications in that it documents actual
    administration events with specific timing and administration details.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.16",
                extension="2014-06-09",
                description="Medication Activity R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.16",
                extension="2014-06-09",
                description="Medication Activity R2.0",
            ),
        ],
    }

    # Code system OIDs
    RXNORM_OID = "2.16.840.1.113883.6.88"  # RxNorm
    ROUTE_OID = "2.16.840.1.113883.3.26.1.1"  # NCI Thesaurus for routes
    UCUM_OID = "2.16.840.1.113883.6.8"  # UCUM for units
    SNOMED_OID = "2.16.840.1.113883.6.96"  # SNOMED CT for body sites

    # Status codes mapping
    STATUS_CODES = {
        "active": "active",
        "completed": "completed",
        "held": "held",
        "aborted": "aborted",
        "suspended": "suspended",
    }

    # Common route codes (NCI Thesaurus)
    ROUTE_CODES = {
        "oral": "C38288",
        "iv": "C38276",
        "intravenous": "C38276",
        "topical": "C38304",
        "subcutaneous": "C38299",
        "intramuscular": "C28161",
        "inhalation": "C38216",
        "rectal": "C38295",
        "ophthalmic": "C38287",
    }

    def __init__(
        self,
        medication: MedicationAdministeredProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize MedicationAdministeredActivity builder.

        Args:
            medication: Medication administration data satisfying MedicationAdministeredProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.medication = medication

    def build(self) -> etree.Element:
        """
        Build Medication Activity XML element for administered medication.

        Returns:
            lxml Element for substanceAdministration
        """
        # Create substanceAdministration element with required attributes
        # moodCode="EVN" for actual administration events
        sub_admin = etree.Element(
            f"{{{NS}}}substanceAdministration",
            classCode="SBADM",
            moodCode="EVN",
        )

        # Add template IDs
        self.add_template_ids(sub_admin)

        # Add ID
        self._add_id(sub_admin)

        # Add status code
        status = self._map_status(self.medication.status)
        status_elem = StatusCode(status).to_element()
        sub_admin.append(status_elem)

        # Add effective time (administration time)
        self._add_effective_time(sub_admin)

        # Add route code
        self._add_route_code(sub_admin)

        # Add dose quantity
        self._add_dose_quantity(sub_admin)

        # Add rate quantity (for IV infusions)
        if self.medication.rate:
            self._add_rate_quantity(sub_admin)

        # Add approach site code (anatomical location)
        if self.medication.site:
            self._add_approach_site_code(sub_admin)

        # Add consumable (the actual medication)
        self._add_consumable(sub_admin)

        # Add performer (who administered)
        if self.medication.performer:
            self._add_performer(sub_admin)

        # Add patient instructions if available
        if self.medication.instructions:
            self._add_instructions(sub_admin)

        # Add indication if available
        if self.medication.indication:
            self._add_indication(sub_admin)

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
        Add effectiveTime with administration time(s).

        For single-dose administrations, uses a single point in time.
        For infusions, uses a time interval.

        Args:
            sub_admin: substanceAdministration element
        """
        time_elem = etree.SubElement(sub_admin, f"{{{NS}}}effectiveTime")

        if self.medication.administration_end_time:
            # Time interval for infusions
            # Set xsi:type attribute using proper namespace
            time_elem.set("{http://www.w3.org/2001/XMLSchema-instance}type", "IVL_TS")

            # Low (start time)
            low = etree.SubElement(time_elem, f"{{{NS}}}low")
            low.set("value", self.medication.administration_time.strftime("%Y%m%d%H%M"))

            # High (end time)
            high = etree.SubElement(time_elem, f"{{{NS}}}high")
            high.set("value", self.medication.administration_end_time.strftime("%Y%m%d%H%M"))
        else:
            # Point in time for single dose
            time_elem.set("value", self.medication.administration_time.strftime("%Y%m%d%H%M"))

    def _add_route_code(self, sub_admin: etree._Element) -> None:
        """
        Add routeCode element.

        Args:
            sub_admin: substanceAdministration element
        """
        route_elem = etree.SubElement(sub_admin, f"{{{NS}}}routeCode")

        if not self.medication.route:
            # No route specified, use null flavor
            route_elem.set("nullFlavor", "UNK")
            return

        route_lower = self.medication.route.lower()
        route_code = self.ROUTE_CODES.get(route_lower)

        if route_code:
            route_elem.set("code", route_code)
            route_elem.set("codeSystem", self.ROUTE_OID)
            route_elem.set("codeSystemName", "NCI Thesaurus")
            route_elem.set("displayName", self.medication.route)
        else:
            # Use originalText if code not found
            route_elem.set("nullFlavor", "OTH")
            text_elem = etree.SubElement(route_elem, f"{{{NS}}}originalText")
            text_elem.text = self.medication.route

    def _add_dose_quantity(self, sub_admin: etree._Element) -> None:
        """
        Add doseQuantity element.

        Args:
            sub_admin: substanceAdministration element
        """
        dose_elem = etree.SubElement(sub_admin, f"{{{NS}}}doseQuantity")

        if not self.medication.dose:
            # No dosage specified, use null flavor
            dose_elem.set("nullFlavor", "UNK")
            return

        # Try to parse dose (e.g., "325 mg", "2 tablets")
        dose = self.medication.dose.strip()
        parts = dose.split(maxsplit=1)

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
                text_elem.text = dose
        else:
            # Use originalText for complex dosage
            text_elem = etree.SubElement(dose_elem, f"{{{NS}}}originalText")
            text_elem.text = dose

    def _add_rate_quantity(self, sub_admin: etree._Element) -> None:
        """
        Add rateQuantity element for IV infusions.

        Args:
            sub_admin: substanceAdministration element
        """
        rate_elem = etree.SubElement(sub_admin, f"{{{NS}}}rateQuantity")

        # Try to parse rate (e.g., "100 mL/hr", "20 mg/min")
        rate = self.medication.rate.strip()
        parts = rate.split(maxsplit=1)

        if len(parts) == 2:
            value, unit = parts
            # Check if value is numeric
            try:
                float(value)
                rate_elem.set("value", value)
                rate_elem.set("unit", unit)
            except ValueError:
                # If value is not numeric, use originalText
                text_elem = etree.SubElement(rate_elem, f"{{{NS}}}originalText")
                text_elem.text = rate
        else:
            # Use originalText
            text_elem = etree.SubElement(rate_elem, f"{{{NS}}}originalText")
            text_elem.text = rate

    def _add_approach_site_code(self, sub_admin: etree._Element) -> None:
        """
        Add approachSiteCode for anatomical location.

        Args:
            sub_admin: substanceAdministration element
        """
        site_elem = etree.SubElement(sub_admin, f"{{{NS}}}approachSiteCode")

        # For simplicity, use originalText
        # In a production system, you'd want to map to SNOMED CT codes
        site_elem.set("nullFlavor", "OTH")
        text_elem = etree.SubElement(site_elem, f"{{{NS}}}originalText")
        text_elem.text = self.medication.site

    def _add_consumable(self, sub_admin: etree._Element) -> None:
        """
        Add consumable element with medication information.

        Args:
            sub_admin: substanceAdministration element
        """
        consumable = etree.SubElement(sub_admin, f"{{{NS}}}consumable")
        manufactured_product = etree.SubElement(
            consumable, f"{{{NS}}}manufacturedProduct", classCode="MANU"
        )

        # Add template ID for manufactured product
        template_id = etree.SubElement(manufactured_product, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.23")
        if self.version == CDAVersion.R2_1:
            template_id.set("extension", "2014-06-09")

        # Add manufactured material
        manufactured_material = etree.SubElement(
            manufactured_product, f"{{{NS}}}manufacturedMaterial"
        )

        # Add medication code (RxNorm)
        code_elem = etree.SubElement(manufactured_material, f"{{{NS}}}code")
        code_elem.set("code", self.medication.code)
        code_elem.set("codeSystem", self.RXNORM_OID)
        code_elem.set("codeSystemName", "RxNorm")
        code_elem.set("displayName", self.medication.name)

    def _add_performer(self, sub_admin: etree._Element) -> None:
        """
        Add performer element for who administered the medication.

        Args:
            sub_admin: substanceAdministration element
        """
        performer = etree.SubElement(sub_admin, f"{{{NS}}}performer")
        assigned_entity = etree.SubElement(performer, f"{{{NS}}}assignedEntity")

        # Add ID
        id_elem = etree.SubElement(assigned_entity, f"{{{NS}}}id")
        id_elem.set("nullFlavor", "UNK")

        # Add assigned person
        assigned_person = etree.SubElement(assigned_entity, f"{{{NS}}}assignedPerson")
        name_elem = etree.SubElement(assigned_person, f"{{{NS}}}name")
        name_elem.text = self.medication.performer

    def _add_instructions(self, sub_admin: etree._Element) -> None:
        """
        Add patient instructions as entryRelationship.

        Args:
            sub_admin: substanceAdministration element
        """
        entry_rel = etree.SubElement(
            sub_admin,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",
            inversionInd="true",
        )

        act = etree.SubElement(
            entry_rel,
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="INT",
        )

        # Add template ID for instructions
        template_id = etree.SubElement(act, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.20")
        if self.version == CDAVersion.R2_1:
            template_id.set("extension", "2014-06-09")

        # Add code for instructions
        code_elem = etree.SubElement(act, f"{{{NS}}}code")
        code_elem.set("code", "409073007")
        code_elem.set("codeSystem", "2.16.840.1.113883.6.96")
        code_elem.set("displayName", "instruction")

        # Add text with instructions
        text_elem = etree.SubElement(act, f"{{{NS}}}text")
        text_elem.text = self.medication.instructions

        # Add status code
        status_elem = etree.SubElement(act, f"{{{NS}}}statusCode")
        status_elem.set("code", "completed")

    def _add_indication(self, sub_admin: etree._Element) -> None:
        """
        Add indication (reason for administration) as entryRelationship.

        Args:
            sub_admin: substanceAdministration element
        """
        entry_rel = etree.SubElement(
            sub_admin,
            f"{{{NS}}}entryRelationship",
            typeCode="RSON",
        )

        observation = etree.SubElement(
            entry_rel,
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template ID for indication
        template_id = etree.SubElement(observation, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.19")
        if self.version == CDAVersion.R2_1:
            template_id.set("extension", "2014-06-09")

        # Add ID
        id_elem = etree.SubElement(observation, f"{{{NS}}}id")
        id_elem.set("nullFlavor", "UNK")

        # Add code
        code_elem = etree.SubElement(observation, f"{{{NS}}}code")
        code_elem.set("code", "404684003")
        code_elem.set("codeSystem", "2.16.840.1.113883.6.96")
        code_elem.set("displayName", "Clinical finding")

        # Add text
        text_elem = etree.SubElement(observation, f"{{{NS}}}text")
        text_elem.text = self.medication.indication

        # Add status code
        status_elem = etree.SubElement(observation, f"{{{NS}}}statusCode")
        status_elem.set("code", "completed")

    def _map_status(self, status: str) -> str:
        """
        Map medication status to substanceAdministration status code.

        Args:
            status: Medication status

        Returns:
            substanceAdministration status code
        """
        if not status:
            return "completed"  # Default for administered meds
        return self.STATUS_CODES.get(status.lower(), "completed")
