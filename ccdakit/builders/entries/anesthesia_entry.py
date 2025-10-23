"""Anesthesia Procedure entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.anesthesia import AnesthesiaProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class AnesthesiaProcedure(CDAElement):
    """
    Builder for C-CDA Procedure Activity Procedure entry for anesthesia.

    Represents anesthesia procedure type (e.g., general, local, regional anesthesia).
    This uses the Procedure Activity Procedure (V2) template to document the type of
    anesthesia administered.

    Supports V3 (2022-06-01) and V2 (2014-06-09) versions.

    Template ID: 2.16.840.1.113883.10.20.22.4.14
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.14",
                extension="2022-06-01",
                description="Procedure Activity Procedure V3",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.14",
                extension="2014-06-09",
                description="Procedure Activity Procedure V2",
            ),
        ],
    }

    # Code system OIDs
    SNOMED_OID = "2.16.840.1.113883.6.96"  # SNOMED CT
    LOINC_OID = "2.16.840.1.113883.6.1"  # LOINC

    # Code system name mapping
    CODE_SYSTEM_NAMES = {
        "SNOMED": "SNOMED CT",
        "SNOMED CT": "SNOMED CT",
        "LOINC": "LOINC",
    }

    # Code system OID mapping
    CODE_SYSTEM_OIDS = {
        "SNOMED": SNOMED_OID,
        "SNOMED CT": SNOMED_OID,
        "LOINC": LOINC_OID,
    }

    # Status codes mapping
    STATUS_CODES = {
        "completed": "completed",
        "active": "active",
        "aborted": "aborted",
        "cancelled": "cancelled",
        "new": "new",
    }

    def __init__(
        self,
        anesthesia: AnesthesiaProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize AnesthesiaProcedure builder.

        Args:
            anesthesia: Anesthesia data satisfying AnesthesiaProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.anesthesia = anesthesia

    def build(self) -> etree.Element:
        """
        Build Anesthesia Procedure Activity XML element.

        Returns:
            lxml Element for procedure
        """
        # Create procedure element with required attributes
        proc = etree.Element(
            f"{{{NS}}}procedure",
            classCode="PROC",
            moodCode="EVN",
        )

        # Add template IDs
        self.add_template_ids(proc)

        # Add ID
        self._add_id(proc)

        # Add code for anesthesia type
        self._add_code(proc)

        # Add status code
        status = self._map_status(self.anesthesia.status)
        status_elem = StatusCode(status).to_element()
        proc.append(status_elem)

        # Add effective time (start and end times) if available
        if self.anesthesia.start_time or self.anesthesia.end_time:
            self._add_effective_time(proc)

        # Add route code if available
        if self.anesthesia.route:
            self._add_route_code(proc)

        # Add performer if available
        if self.anesthesia.performer_name:
            self._add_performer(proc)

        return proc

    def _add_id(self, proc: etree._Element) -> None:
        """
        Add ID element to procedure.

        Args:
            proc: procedure element
        """
        import uuid

        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=str(uuid.uuid4()),
        ).to_element()
        proc.append(id_elem)

    def _add_code(self, proc: etree._Element) -> None:
        """
        Add code element for the anesthesia type.

        Args:
            proc: procedure element
        """
        # Map code system to OID if needed
        system = self.CODE_SYSTEM_OIDS.get(
            self.anesthesia.anesthesia_code_system,
            self.anesthesia.anesthesia_code_system,  # Use as-is if not found
        )

        code_elem = Code(
            code=self.anesthesia.anesthesia_code,
            system=system,
            display_name=self.anesthesia.anesthesia_type,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        proc.append(code_elem)

    def _add_effective_time(self, proc: etree._Element) -> None:
        """
        Add effectiveTime for when the anesthesia was administered.

        Args:
            proc: procedure element
        """
        time_elem = EffectiveTime(
            low=self.anesthesia.start_time,
            high=self.anesthesia.end_time,
        ).to_element()
        proc.append(time_elem)

    def _add_route_code(self, proc: etree._Element) -> None:
        """
        Add methodCode element for route of administration.

        Args:
            proc: procedure element
        """
        # In procedure context, route is represented as methodCode
        method_elem = etree.SubElement(proc, f"{{{NS}}}methodCode")
        method_elem.set("nullFlavor", "OTH")

        # Add original text for the route
        text_elem = etree.SubElement(method_elem, f"{{{NS}}}originalText")
        text_elem.text = self.anesthesia.route

    def _add_performer(self, proc: etree._Element) -> None:
        """
        Add performer element for the anesthesiologist/anesthetist.

        Args:
            proc: procedure element
        """
        import uuid

        assert self.anesthesia.performer_name is not None
        performer_elem = etree.SubElement(proc, f"{{{NS}}}performer")

        assigned_entity = etree.SubElement(performer_elem, f"{{{NS}}}assignedEntity")

        # Add ID
        id_elem = etree.SubElement(assigned_entity, f"{{{NS}}}id")
        id_elem.set("root", "2.16.840.1.113883.19")
        id_elem.set("extension", str(uuid.uuid4()))

        # Add assigned person with name
        assigned_person = etree.SubElement(assigned_entity, f"{{{NS}}}assignedPerson")
        name_elem = etree.SubElement(assigned_person, f"{{{NS}}}name")

        # Try to parse name (assuming "FirstName LastName" or "Dr. FirstName LastName" format)
        name_text = self.anesthesia.performer_name.strip()

        # Remove common prefixes
        for prefix in ["Dr.", "Dr", "MD", "M.D."]:
            if name_text.startswith(prefix):
                name_text = name_text[len(prefix) :].strip()
            if name_text.endswith(prefix):
                name_text = name_text[: -len(prefix)].strip()

        # Remove comma and anything after it (like ", MD")
        if "," in name_text:
            name_text = name_text.split(",")[0].strip()

        # Split into parts
        name_parts = name_text.strip().split(maxsplit=1)
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
            family_elem.text = name_text if name_text else self.anesthesia.performer_name

    def _map_status(self, status: str) -> str:
        """
        Map anesthesia status to procedure status code.

        Args:
            status: Anesthesia status

        Returns:
            procedure status code
        """
        return self.STATUS_CODES.get(status.lower(), "completed")
