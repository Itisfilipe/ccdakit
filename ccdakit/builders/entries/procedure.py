"""Procedure Activity entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.procedure import ProcedureProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class ProcedureActivity(CDAElement):
    """
    Builder for C-CDA Procedure Activity Procedure entry.

    Represents surgical, diagnostic, or therapeutic procedures.
    This is the most common procedure template, used for procedures that alter
    the physical condition of a patient (e.g., appendectomy, hip replacement).

    Supports V3 (2022-06-01) and V2 (2014-06-09) versions.
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
    CPT_OID = "2.16.840.1.113883.6.12"  # CPT-4
    LOINC_OID = "2.16.840.1.113883.6.1"  # LOINC
    ICD10_PCS_OID = "2.16.840.1.113883.6.4"  # ICD-10 PCS

    # Code system name mapping
    CODE_SYSTEM_NAMES = {
        "SNOMED": "SNOMED CT",
        "SNOMED CT": "SNOMED CT",
        "CPT": "CPT-4",
        "CPT-4": "CPT-4",
        "CPT4": "CPT-4",
        "LOINC": "LOINC",
        "ICD10 PCS": "ICD-10 PCS",
        "ICD10PCS": "ICD-10 PCS",
    }

    # Code system OID mapping
    CODE_SYSTEM_OIDS = {
        "SNOMED": SNOMED_OID,
        "SNOMED CT": SNOMED_OID,
        "CPT": CPT_OID,
        "CPT-4": CPT_OID,
        "CPT4": CPT_OID,
        "LOINC": LOINC_OID,
        "ICD10 PCS": ICD10_PCS_OID,
        "ICD10PCS": ICD10_PCS_OID,
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
        procedure: ProcedureProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ProcedureActivity builder.

        Args:
            procedure: Procedure data satisfying ProcedureProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.procedure = procedure

    def build(self) -> etree.Element:
        """
        Build Procedure Activity XML element.

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

        # Add code
        self._add_code(proc)

        # Add status code
        status = self._map_status(self.procedure.status)
        status_elem = StatusCode(status).to_element()
        proc.append(status_elem)

        # Add effective time (procedure date) if available
        if self.procedure.date:
            self._add_effective_time(proc)

        # Add target site code if available
        if self.procedure.target_site_code or self.procedure.target_site:
            self._add_target_site(proc)

        # Add performer if available
        if self.procedure.performer_name:
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
        Add code element for the procedure.

        Args:
            proc: procedure element
        """
        # Map code system to OID if needed
        # The Code class accepts either a system name (for lookup) or an OID
        system = self.CODE_SYSTEM_OIDS.get(
            self.procedure.code_system,
            self.procedure.code_system,  # Use as-is if not found
        )

        code_elem = Code(
            code=self.procedure.code,
            system=system,
            display_name=self.procedure.name,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        proc.append(code_elem)

    def _add_effective_time(self, proc: etree._Element) -> None:
        """
        Add effectiveTime for when the procedure was performed.

        Args:
            proc: procedure element
        """
        time_elem = EffectiveTime(value=self.procedure.date).to_element()
        proc.append(time_elem)

    def _add_target_site(self, proc: etree._Element) -> None:
        """
        Add targetSiteCode element for body site.

        Args:
            proc: procedure element
        """
        target_site_elem = etree.SubElement(proc, f"{{{NS}}}targetSiteCode")

        if self.procedure.target_site_code:
            # Use coded target site
            target_site_elem.set("code", self.procedure.target_site_code)
            target_site_elem.set("codeSystem", self.SNOMED_OID)
            target_site_elem.set("codeSystemName", "SNOMED CT")
            if self.procedure.target_site:
                target_site_elem.set("displayName", self.procedure.target_site)
        else:
            # Use originalText only
            target_site_elem.set("nullFlavor", "OTH")
            text_elem = etree.SubElement(target_site_elem, f"{{{NS}}}originalText")
            text_elem.text = self.procedure.target_site

    def _add_performer(self, proc: etree._Element) -> None:
        """
        Add performer element for the person who performed the procedure.

        Args:
            proc: procedure element
        """
        import uuid

        assert self.procedure.performer_name is not None
        performer_elem = etree.SubElement(proc, f"{{{NS}}}performer")

        assigned_entity = etree.SubElement(performer_elem, f"{{{NS}}}assignedEntity")

        # Add ID
        id_elem = etree.SubElement(assigned_entity, f"{{{NS}}}id")
        id_elem.set("root", "2.16.840.1.113883.19")
        id_elem.set("extension", str(uuid.uuid4()))

        # Add assigned person with name
        assigned_person = etree.SubElement(assigned_entity, f"{{{NS}}}assignedPerson")
        name_elem = etree.SubElement(assigned_person, f"{{{NS}}}name")

        # Try to parse name (assuming "FirstName LastName" format)
        name_parts = self.procedure.performer_name.strip().split(maxsplit=1)
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
            family_elem.text = self.procedure.performer_name

    def _map_status(self, status: str) -> str:
        """
        Map procedure status to procedure status code.

        Args:
            status: Procedure status

        Returns:
            procedure status code
        """
        return self.STATUS_CODES.get(status.lower(), "completed")
