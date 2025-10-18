"""Encounter Activity entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.encounter import EncounterProtocol


# CDA namespace
NS = "urn:hl7-org:v3"
# SDTC namespace (for discharge disposition)
SDTC_NS = "urn:hl7-org:sdtc"


class EncounterActivity(CDAElement):
    """
    Builder for C-CDA Encounter Activity entry.

    Represents healthcare encounters such as office visits, emergency department
    visits, hospital admissions, and other types of patient-provider interactions.

    Supports V3 (2015-08-01) and V2 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.49",
                extension="2015-08-01",
                description="Encounter Activity V3",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.49",
                extension="2014-06-09",
                description="Encounter Activity V2",
            ),
        ],
    }

    # Code system OIDs
    CPT_OID = "2.16.840.1.113883.6.12"  # CPT-4
    SNOMED_OID = "2.16.840.1.113883.6.96"  # SNOMED CT
    ACT_CODE_OID = "2.16.840.1.113883.5.4"  # HL7 ActCode

    # Code system name mapping
    CODE_SYSTEM_NAMES = {
        "CPT": "CPT-4",
        "CPT-4": "CPT-4",
        "CPT4": "CPT-4",
        "SNOMED": "SNOMED CT",
        "SNOMED CT": "SNOMED CT",
        "ActCode": "ActCode",
        "ACT": "ActCode",
    }

    # Code system OID mapping
    CODE_SYSTEM_OIDS = {
        "CPT": CPT_OID,
        "CPT-4": CPT_OID,
        "CPT4": CPT_OID,
        "SNOMED": SNOMED_OID,
        "SNOMED CT": SNOMED_OID,
        "ActCode": ACT_CODE_OID,
        "ACT": ACT_CODE_OID,
    }

    def __init__(
        self,
        encounter: EncounterProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize EncounterActivity builder.

        Args:
            encounter: Encounter data satisfying EncounterProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.encounter = encounter

    def build(self) -> etree.Element:
        """
        Build Encounter Activity XML element.

        Returns:
            lxml Element for encounter
        """
        # Create encounter element with required attributes
        enc = etree.Element(
            f"{{{NS}}}encounter",
            classCode="ENC",
            moodCode="EVN",
        )

        # Add template IDs
        self.add_template_ids(enc)

        # Add ID
        self._add_id(enc)

        # Add code
        self._add_code(enc)

        # Add effective time (encounter date) - required
        self._add_effective_time(enc)

        # Add performer if available
        if self.encounter.performer_name:
            self._add_performer(enc)

        # Add location if available
        if self.encounter.location:
            self._add_location(enc)

        # Add discharge disposition if available (SDTC extension)
        if self.encounter.discharge_disposition:
            self._add_discharge_disposition(enc)

        return enc

    def _add_id(self, enc: etree._Element) -> None:
        """
        Add ID element to encounter.

        Args:
            enc: encounter element
        """
        import uuid

        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=str(uuid.uuid4()),
        ).to_element()
        enc.append(id_elem)

    def _add_code(self, enc: etree._Element) -> None:
        """
        Add code element for the encounter type.

        Args:
            enc: encounter element
        """
        # Map code system to OID if needed
        system = self.CODE_SYSTEM_OIDS.get(
            self.encounter.code_system,
            self.encounter.code_system,  # Use as-is if not found
        )

        code_elem = Code(
            code=self.encounter.code,
            system=system,
            display_name=self.encounter.encounter_type,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        enc.append(code_elem)

    def _add_effective_time(self, enc: etree._Element) -> None:
        """
        Add effectiveTime for when the encounter occurred.

        If end_date is provided, creates a time interval (low/high).
        Otherwise, creates a point in time value.

        Args:
            enc: encounter element
        """
        if self.encounter.end_date:
            # Create time interval with low and high
            time_elem = etree.SubElement(enc, f"{{{NS}}}effectiveTime")

            # Low (start date)
            if self.encounter.date:
                low_elem = etree.SubElement(time_elem, f"{{{NS}}}low")
                if hasattr(self.encounter.date, "hour"):
                    # datetime object
                    low_elem.set("value", self.encounter.date.strftime("%Y%m%d%H%M%S"))
                else:
                    # date object
                    low_elem.set("value", self.encounter.date.strftime("%Y%m%d"))

            # High (end date)
            high_elem = etree.SubElement(time_elem, f"{{{NS}}}high")
            if hasattr(self.encounter.end_date, "hour"):
                # datetime object
                high_elem.set("value", self.encounter.end_date.strftime("%Y%m%d%H%M%S"))
            else:
                # date object
                high_elem.set("value", self.encounter.end_date.strftime("%Y%m%d"))
        elif self.encounter.date:
            # Single point in time
            time_elem = EffectiveTime(value=self.encounter.date).to_element()
            enc.append(time_elem)

    def _add_performer(self, enc: etree._Element) -> None:
        """
        Add performer element for the healthcare provider.

        Args:
            enc: encounter element
        """
        import uuid

        assert self.encounter.performer_name is not None
        performer_elem = etree.SubElement(enc, f"{{{NS}}}performer", typeCode="PRF")

        assigned_entity = etree.SubElement(performer_elem, f"{{{NS}}}assignedEntity")

        # Add ID
        id_elem = etree.SubElement(assigned_entity, f"{{{NS}}}id")
        id_elem.set("root", "2.16.840.1.113883.19")
        id_elem.set("extension", str(uuid.uuid4()))

        # Add assigned person with name
        assigned_person = etree.SubElement(assigned_entity, f"{{{NS}}}assignedPerson")
        name_elem = etree.SubElement(assigned_person, f"{{{NS}}}name")

        # Try to parse name (assuming "FirstName LastName" format)
        name_parts = self.encounter.performer_name.strip().split(maxsplit=1)
        if len(name_parts) == 2:
            # Given name (first name)
            given_elem = etree.SubElement(name_elem, f"{{{NS}}}given")
            given_elem.text = name_parts[0]

            # Family name (last name)
            family_elem = etree.SubElement(name_elem, f"{{{NS}}}family")
            family_elem.text = name_parts[1]
        else:
            # Single name - use as family name
            family_elem = etree.SubElement(name_elem, f"{{{NS}}}family")
            family_elem.text = self.encounter.performer_name

    def _add_location(self, enc: etree._Element) -> None:
        """
        Add participant element for service delivery location.

        Args:
            enc: encounter element
        """
        import uuid

        # Create participant with typeCode="LOC"
        participant_elem = etree.SubElement(enc, f"{{{NS}}}participant", typeCode="LOC")

        # Create participantRole with classCode="SDLOC"
        participant_role = etree.SubElement(
            participant_elem,
            f"{{{NS}}}participantRole",
            classCode="SDLOC",
        )

        # Add template ID for Service Delivery Location (optional, but good practice)
        template_id = etree.SubElement(participant_role, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.32")

        # Add ID for the location
        id_elem = etree.SubElement(participant_role, f"{{{NS}}}id")
        id_elem.set("root", "2.16.840.1.113883.19")
        id_elem.set("extension", str(uuid.uuid4()))

        # Add code (optional - we could add facility type code here)
        code_elem = etree.SubElement(participant_role, f"{{{NS}}}code")
        code_elem.set("nullFlavor", "UNK")  # Unknown facility type

        # Add playingEntity with the location name
        playing_entity = etree.SubElement(
            participant_role, f"{{{NS}}}playingEntity", classCode="PLC"
        )
        name_elem = etree.SubElement(playing_entity, f"{{{NS}}}name")
        name_elem.text = self.encounter.location

    def _add_discharge_disposition(self, enc: etree._Element) -> None:
        """
        Add discharge disposition code using SDTC extension.

        Args:
            enc: encounter element
        """
        # Register SDTC namespace if not already done
        # Note: This should ideally be done at the document level
        etree.register_namespace("sdtc", SDTC_NS)

        # Add discharge disposition code
        etree.SubElement(
            enc,
            f"{{{SDTC_NS}}}dischargeDispositionCode",
            code="01",  # Default code for "Home"
            codeSystem="2.16.840.1.113883.12.112",  # HL7 Discharge Disposition
            codeSystemName="HL7 Discharge Disposition",
            displayName=self.encounter.discharge_disposition,
        )
