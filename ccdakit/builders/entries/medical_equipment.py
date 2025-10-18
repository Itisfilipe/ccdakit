"""Medical Equipment entry builders for C-CDA documents."""

from typing import Optional, Sequence
from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.medical_equipment import MedicalEquipmentProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class NonMedicinalSupplyActivity(CDAElement):
    """
    Builder for C-CDA Non-Medicinal Supply Activity entry.

    Represents equipment supplied to the patient (e.g., pumps, inhalers, wheelchairs).
    Devices applied to or placed in the patient should use Procedure Activity Procedure.

    Supports V2 (2014-06-09) version.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.50",
                extension="2014-06-09",
                description="Non-Medicinal Supply Activity V2",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.50",
                extension="2014-06-09",
                description="Non-Medicinal Supply Activity V2",
            ),
        ],
    }

    # Code system OIDs
    SNOMED_OID = "2.16.840.1.113883.6.96"  # SNOMED CT
    HCPCS_OID = "2.16.840.1.113883.6.285"  # HCPCS
    CPT_OID = "2.16.840.1.113883.6.12"  # CPT-4
    FDA_UDI_OID = "2.16.840.1.113883.3.3719"  # FDA UDI

    # Code system name mapping
    CODE_SYSTEM_NAMES = {
        "SNOMED": "SNOMED CT",
        "SNOMED CT": "SNOMED CT",
        "HCPCS": "HCPCS",
        "CPT": "CPT-4",
        "CPT-4": "CPT-4",
        "CPT4": "CPT-4",
    }

    # Code system OID mapping
    CODE_SYSTEM_OIDS = {
        "SNOMED": SNOMED_OID,
        "SNOMED CT": SNOMED_OID,
        "HCPCS": HCPCS_OID,
        "CPT": CPT_OID,
        "CPT-4": CPT_OID,
        "CPT4": CPT_OID,
    }

    # Status codes mapping (ActStatus value set)
    STATUS_CODES = {
        "completed": "completed",
        "active": "active",
        "aborted": "aborted",
        "cancelled": "cancelled",
        "new": "new",
        "suspended": "suspended",
        "nullified": "nullified",
    }

    def __init__(
        self,
        equipment: MedicalEquipmentProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize NonMedicinalSupplyActivity builder.

        Args:
            equipment: Medical equipment data satisfying MedicalEquipmentProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.equipment = equipment

    def build(self) -> etree.Element:
        """
        Build Non-Medicinal Supply Activity XML element.

        Returns:
            lxml Element for supply
        """
        # Create supply element with required attributes (CONF:1098-8745, CONF:1098-8746)
        supply = etree.Element(
            f"{{{NS}}}supply",
            classCode="SPLY",  # CONF:1098-8745
            moodCode=self._get_mood_code(),  # CONF:1098-8746
        )

        # Add template IDs (CONF:1098-8747)
        self.add_template_ids(supply)

        # Add ID (CONF:1098-8748)
        self._add_id(supply)

        # Add status code (CONF:1098-8749, CONF:1098-32363)
        status = self._map_status(self.equipment.status)
        status_elem = StatusCode(status).to_element()
        supply.append(status_elem)

        # Add effective time if available (CONF:1098-15498)
        if self.equipment.date_supplied or self.equipment.date_end:
            self._add_effective_time(supply)

        # Add quantity if available (CONF:1098-8751)
        if self.equipment.quantity is not None:
            self._add_quantity(supply)

        # Add product instance participant if device details available (CONF:1098-8752)
        if self._has_product_instance_data():
            self._add_product_instance(supply)

        # Add instruction if available (CONF:1098-30277)
        if self.equipment.instructions:
            self._add_instruction(supply)

        return supply

    def _get_mood_code(self) -> str:
        """
        Get moodCode based on status (from MoodCodeEvnInt value set).

        Returns:
            Mood code (EVN or INT)
        """
        # MoodCodeEvnInt value set includes EVN (event) and INT (intent)
        # Use INT for planned/ordered supplies, EVN for completed/active
        intent_statuses = ["new", "ordered", "planned"]
        if self.equipment.status.lower() in intent_statuses:
            return "INT"
        return "EVN"

    def _add_id(self, supply: etree._Element) -> None:
        """
        Add ID element to supply (CONF:1098-8748).

        Args:
            supply: supply element
        """
        import uuid

        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=str(uuid.uuid4()),
        ).to_element()
        supply.append(id_elem)

    def _add_effective_time(self, supply: etree._Element) -> None:
        """
        Add effectiveTime element (CONF:1098-15498).

        Args:
            supply: supply element
        """
        if self.equipment.date_supplied and self.equipment.date_end:
            # Create IVL_TS with low and high (CONF:1098-16867)
            time_elem = etree.SubElement(supply, f"{{{NS}}}effectiveTime")
            time_elem.set("{http://www.w3.org/2001/XMLSchema-instance}type", "IVL_TS")

            # Low (start date)
            low_elem = etree.SubElement(time_elem, f"{{{NS}}}low")
            if hasattr(self.equipment.date_supplied, "hour"):
                low_elem.set("value", self.equipment.date_supplied.strftime("%Y%m%d%H%M%S"))
            else:
                low_elem.set("value", self.equipment.date_supplied.strftime("%Y%m%d"))

            # High (end date) (CONF:1098-16867)
            high_elem = etree.SubElement(time_elem, f"{{{NS}}}high")
            if hasattr(self.equipment.date_end, "hour"):
                high_elem.set("value", self.equipment.date_end.strftime("%Y%m%d%H%M%S"))
            else:
                high_elem.set("value", self.equipment.date_end.strftime("%Y%m%d"))

        elif self.equipment.date_supplied:
            # Single time point
            time_elem = EffectiveTime(value=self.equipment.date_supplied).to_element()
            supply.append(time_elem)

    def _add_quantity(self, supply: etree._Element) -> None:
        """
        Add quantity element (CONF:1098-8751).

        Args:
            supply: supply element
        """
        assert self.equipment.quantity is not None
        quantity_elem = etree.SubElement(supply, f"{{{NS}}}quantity")
        quantity_elem.set("value", str(self.equipment.quantity))

    def _has_product_instance_data(self) -> bool:
        """
        Check if we have data for Product Instance participant.

        Returns:
            True if we have product instance data
        """
        return bool(
            self.equipment.manufacturer
            or self.equipment.model_number
            or self.equipment.serial_number
            or self.equipment.code
        )

    def _add_product_instance(self, supply: etree._Element) -> None:
        """
        Add participant with Product Instance (CONF:1098-8752, CONF:1098-15900).

        Args:
            supply: supply element
        """
        # Create participant element (CONF:1098-8752)
        participant = etree.SubElement(
            supply,
            f"{{{NS}}}participant",
            typeCode="PRD",  # CONF:1098-8754
        )

        # Create participantRole (Product Instance template)
        # (CONF:1098-15900)
        participant_role = etree.SubElement(
            participant,
            f"{{{NS}}}participantRole",
            classCode="MANU",  # CONF:81-7900
        )

        # Add Product Instance template ID (CONF:81-7901)
        template_id = etree.SubElement(participant_role, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.37")

        # Add ID (CONF:81-7902)
        # Use serial number/UDI if available
        if self.equipment.serial_number:
            id_elem = etree.SubElement(participant_role, f"{{{NS}}}id")
            # Check if it looks like a UDI (contains parentheses)
            if "(" in self.equipment.serial_number:
                # Full UDI - use FDA OID
                id_elem.set("root", self.FDA_UDI_OID)
                id_elem.set("extension", self.equipment.serial_number)
            else:
                # Simple serial number
                id_elem.set("root", "2.16.840.1.113883.19")
                id_elem.set("extension", self.equipment.serial_number)
        else:
            # Generate a generic ID
            import uuid

            id_elem = etree.SubElement(participant_role, f"{{{NS}}}id")
            id_elem.set("root", "2.16.840.1.113883.19")
            id_elem.set("extension", str(uuid.uuid4()))

        # Add playingDevice (CONF:81-7903)
        playing_device = etree.SubElement(participant_role, f"{{{NS}}}playingDevice")

        # Add device code if available (CONF:81-16837)
        if self.equipment.code and self.equipment.code_system:
            system = self.CODE_SYSTEM_OIDS.get(
                self.equipment.code_system,
                self.equipment.code_system,
            )
            code_elem = Code(
                code=self.equipment.code,
                system=system,
                display_name=self.equipment.name,
            ).to_element()
            code_elem.tag = f"{{{NS}}}code"
            playing_device.append(code_elem)

        # Add scopingEntity (CONF:81-7905)
        scoping_entity = etree.SubElement(participant_role, f"{{{NS}}}scopingEntity")

        # Add manufacturer ID (CONF:81-7908)
        scoping_id = etree.SubElement(scoping_entity, f"{{{NS}}}id")
        if self.equipment.manufacturer:
            scoping_id.set("root", "2.16.840.1.113883.19")
            # Use manufacturer name as extension
            scoping_id.set("extension", self.equipment.manufacturer)
        else:
            # Use nullFlavor if no manufacturer
            scoping_id.set("nullFlavor", "UNK")

    def _add_instruction(self, supply: etree._Element) -> None:
        """
        Add entryRelationship with Instruction (CONF:1098-30277).

        Args:
            supply: supply element
        """
        assert self.equipment.instructions is not None

        # Create entryRelationship (CONF:1098-30277)
        entry_rel = etree.SubElement(
            supply,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",  # CONF:1098-30278
            inversionInd="true",  # CONF:1098-30279
        )

        # Create act element for Instruction (CONF:1098-31393)
        act = etree.SubElement(
            entry_rel,
            f"{{{NS}}}act",
            classCode="ACT",  # CONF:1098-7391
            moodCode="INT",  # CONF:1098-7392
        )

        # Add Instruction template ID (CONF:1098-7393)
        template_id = etree.SubElement(act, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.20")  # CONF:1098-10503
        template_id.set("extension", "2014-06-09")  # CONF:1098-32598

        # Add code (CONF:1098-16884)
        # Using Patient Education value set - use generic instruction code
        code_elem = etree.SubElement(act, f"{{{NS}}}code")
        code_elem.set("code", "409073007")  # SNOMED: Instruction
        code_elem.set("codeSystem", self.SNOMED_OID)
        code_elem.set("codeSystemName", "SNOMED CT")
        code_elem.set("displayName", "Instruction")

        # Add text with instruction content
        text_elem = etree.SubElement(act, f"{{{NS}}}text")
        text_elem.text = self.equipment.instructions

        # Add status code (CONF:1098-7396, CONF:1098-19106)
        status_elem = etree.SubElement(act, f"{{{NS}}}statusCode")
        status_elem.set("code", "completed")

    def _map_status(self, status: str) -> str:
        """
        Map equipment status to ActStatus code.

        Args:
            status: Equipment status

        Returns:
            ActStatus code
        """
        return self.STATUS_CODES.get(status.lower(), "completed")


class MedicalEquipmentOrganizer(CDAElement):
    """
    Builder for C-CDA Medical Equipment Organizer.

    Groups multiple medical supplies/equipment together.
    Represents a set of current or historical medical devices, supplies,
    aids and equipment used by the patient.

    No version specified in template (no extension attribute).
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.135",
                extension=None,  # No extension for this template
                description="Medical Equipment Organizer",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.135",
                extension=None,
                description="Medical Equipment Organizer",
            ),
        ],
    }

    # Status codes from Result Status value set
    STATUS_CODES = {
        "completed": "completed",
        "active": "active",
        "aborted": "aborted",
        "cancelled": "cancelled",
    }

    def __init__(
        self,
        equipment_list: Sequence[MedicalEquipmentProtocol],
        status: str = "completed",
        date_start: Optional[object] = None,
        date_end: Optional[object] = None,
        organizer_code: Optional[str] = None,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize MedicalEquipmentOrganizer builder.

        Args:
            equipment_list: List of medical equipment items
            status: Organizer status (default: "completed")
            date_start: Start date for the equipment set
            date_end: End date for the equipment set
            organizer_code: Optional code for the organizer
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.equipment_list = equipment_list
        self.status = status
        self.date_start = date_start
        self.date_end = date_end
        self.organizer_code = organizer_code

    def build(self) -> etree.Element:
        """
        Build Medical Equipment Organizer XML element.

        Returns:
            lxml Element for organizer
        """
        # Create organizer element (CONF:1098-31020, CONF:1098-31021)
        organizer = etree.Element(
            f"{{{NS}}}organizer",
            classCode="CLUSTER",  # CONF:1098-31020
            moodCode="EVN",  # CONF:1098-31021
        )

        # Add template IDs (CONF:1098-31022)
        self.add_template_ids(organizer)

        # Add ID (CONF:1098-31024)
        self._add_id(organizer)

        # Add code if provided (CONF:1098-31025)
        if self.organizer_code:
            code_elem = etree.SubElement(organizer, f"{{{NS}}}code")
            code_elem.set("code", self.organizer_code)

        # Add status code (CONF:1098-31026, CONF:1098-31029)
        status_code = self._map_status(self.status)
        status_elem = StatusCode(status_code).to_element()
        organizer.append(status_elem)

        # Add effective time (CONF:1098-32136, CONF:1098-32378, CONF:1098-32379)
        self._add_effective_time(organizer)

        # Add components (CONF:1098-31027, CONF:1098-31887, CONF:1098-32380)
        if not self.equipment_list:
            raise ValueError(
                "Medical Equipment Organizer must contain at least one supply or procedure (CONF:1098-32380)"
            )

        for equipment in self.equipment_list:
            self._add_component(organizer, equipment)

        return organizer

    def _add_id(self, organizer: etree._Element) -> None:
        """
        Add ID element (CONF:1098-31024).

        Args:
            organizer: organizer element
        """
        import uuid

        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=str(uuid.uuid4()),
        ).to_element()
        organizer.append(id_elem)

    def _add_effective_time(self, organizer: etree._Element) -> None:
        """
        Add effectiveTime with low and high (CONF:1098-32136).

        Args:
            organizer: organizer element
        """
        time_elem = etree.SubElement(organizer, f"{{{NS}}}effectiveTime")

        # Add low (CONF:1098-32378)
        low_elem = etree.SubElement(time_elem, f"{{{NS}}}low")
        if self.date_start:
            if hasattr(self.date_start, "hour"):
                low_elem.set("value", self.date_start.strftime("%Y%m%d%H%M%S"))
            else:
                low_elem.set("value", self.date_start.strftime("%Y%m%d"))
        else:
            # Use nullFlavor if no start date
            low_elem.set("nullFlavor", "UNK")

        # Add high (CONF:1098-32379)
        high_elem = etree.SubElement(time_elem, f"{{{NS}}}high")
        if self.date_end:
            if hasattr(self.date_end, "hour"):
                high_elem.set("value", self.date_end.strftime("%Y%m%d%H%M%S"))
            else:
                high_elem.set("value", self.date_end.strftime("%Y%m%d"))
        else:
            # Use nullFlavor if no end date
            high_elem.set("nullFlavor", "UNK")

    def _add_component(
        self, organizer: etree._Element, equipment: MedicalEquipmentProtocol
    ) -> None:
        """
        Add component with Non-Medicinal Supply Activity (CONF:1098-31027, CONF:1098-31862).

        Args:
            organizer: organizer element
            equipment: Medical equipment data
        """
        # Create component element
        component = etree.SubElement(organizer, f"{{{NS}}}component")

        # Create and add Non-Medicinal Supply Activity (CONF:1098-31862)
        supply_builder = NonMedicinalSupplyActivity(equipment, version=self.version)
        component.append(supply_builder.to_element())

    def _map_status(self, status: str) -> str:
        """
        Map status to Result Status value set code.

        Args:
            status: Organizer status

        Returns:
            Status code
        """
        return self.STATUS_CODES.get(status.lower(), "completed")
