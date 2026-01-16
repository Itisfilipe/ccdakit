"""Common reusable builders for C-CDA elements."""

from datetime import date, datetime
from typing import Optional

from lxml import etree

from ccdakit.core.base import CDAElement


# CDA namespace for element creation
NS = "urn:hl7-org:v3"


class Code(CDAElement):
    """Reusable code element builder."""

    # Standard code system OIDs
    # NOTE: This dictionary duplicates CodeSystemRegistry.SYSTEMS to avoid circular imports.
    # The Code class is a core builder used throughout the codebase, and importing
    # CodeSystemRegistry here would create circular dependencies with modules that
    # depend on both builders and utils. Consider consolidating in future refactoring.
    SYSTEM_OIDS = {
        # Clinical terminology systems
        "LOINC": "2.16.840.1.113883.6.1",
        "SNOMED": "2.16.840.1.113883.6.96",
        "RxNorm": "2.16.840.1.113883.6.88",
        "ICD-10": "2.16.840.1.113883.6.90",
        "ICD-10-CM": "2.16.840.1.113883.6.90",
        "ICD-10-PCS": "2.16.840.1.113883.6.4",
        "ICD-9-CM": "2.16.840.1.113883.6.103",
        "ICD-9-PCS": "2.16.840.1.113883.6.104",
        "CPT": "2.16.840.1.113883.6.12",
        "CVX": "2.16.840.1.113883.12.292",
        "NDC": "2.16.840.1.113883.6.69",
        "HCPCS": "2.16.840.1.113883.6.285",
        "NCI": "2.16.840.1.113883.3.26.1.1",
        "UNII": "2.16.840.1.113883.4.9",
        # Units of measure
        "UCUM": "2.16.840.1.113883.6.8",
        # HL7 vocabulary systems
        "HL7": "2.16.840.1.113883.5.1",
        "ActClass": "2.16.840.1.113883.5.6",
        "ActCode": "2.16.840.1.113883.5.4",
        "ActMood": "2.16.840.1.113883.5.1001",
        "ActStatus": "2.16.840.1.113883.5.14",
        "ObservationInterpretation": "2.16.840.1.113883.5.83",
        "ParticipationType": "2.16.840.1.113883.5.90",
        "RoleClass": "2.16.840.1.113883.5.110",
        "EntityNameUse": "2.16.840.1.113883.5.45",
        "PostalAddressUse": "2.16.840.1.113883.5.1119",
        "TelecomAddressUse": "2.16.840.1.113883.5.1119",
        "MaritalStatus": "2.16.840.1.113883.5.2",
        "ReligiousAffiliation": "2.16.840.1.113883.5.1076",
        "AdministrativeGender": "2.16.840.1.113883.5.1",
        "NullFlavor": "2.16.840.1.113883.5.1008",
        # CDC and demographic systems
        "Race": "2.16.840.1.113883.6.238",
        "Ethnicity": "2.16.840.1.113883.6.238",
        # International standards
        "Language": "2.16.840.1.113883.6.121",
        "ISO3166": "1.0.3166.1.2.2",
        # Healthcare facility and billing
        "NUBC": "2.16.840.1.113883.6.301",
        "DischargeDisposition": "2.16.840.1.113883.12.112",
        "AdmitSource": "2.16.840.1.113883.12.23",
        "ProcedureCode": "2.16.840.1.113883.6.96",
        # Additional HL7 vocabulary
        "RouteOfAdministration": "2.16.840.1.113883.5.112",
        "DoseForm": "2.16.840.1.113883.3.26.1.1",
        "BodySite": "2.16.840.1.113883.6.96",
        "Confidentiality": "2.16.840.1.113883.5.25",
        "EncounterType": "2.16.840.1.113883.5.4",
        "ProblemType": "2.16.840.1.113883.3.88.12.3221.7.2",
        "AllergyCategory": "2.16.840.1.113883.3.88.12.3221.6.2",
        "AllergySeverity": "2.16.840.1.113883.6.96",
        "ReactionSeverity": "2.16.840.1.113883.6.96",
        "MedicationStatus": "2.16.840.1.113883.3.88.12.80.20",
        "VitalSignResult": "2.16.840.1.113883.6.1",
        "LabResultStatus": "2.16.840.1.113883.5.14",
        "ResultInterpretation": "2.16.840.1.113883.5.83",
        "SpecimenType": "2.16.840.1.113883.6.96",
    }

    def __init__(
        self,
        code: Optional[str] = None,
        system: Optional[str] = None,
        display_name: Optional[str] = None,
        null_flavor: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize Code builder.

        Args:
            code: Code value
            system: Code system (name or OID)
            display_name: Human-readable display name
            null_flavor: Null flavor if code is not available
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(**kwargs)
        self.code = code
        self.system = system
        self.display_name = display_name
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        """
        Build code XML element.

        Returns:
            lxml Element for code

        Raises:
            ValueError: If both code and null_flavor are missing
        """
        elem = etree.Element(f"{{{NS}}}code")

        if self.null_flavor:
            elem.set("nullFlavor", self.null_flavor)
        else:
            if not self.code or not self.system:
                raise ValueError("code and system required when null_flavor not provided")

            elem.set("code", self.code)

            # Handle system OID lookup
            if self.system in self.SYSTEM_OIDS:
                elem.set("codeSystem", self.SYSTEM_OIDS[self.system])
                elem.set("codeSystemName", self.system)
            else:
                elem.set("codeSystem", self.system)

            if self.display_name:
                elem.set("displayName", self.display_name)

        return elem


class EffectiveTime(CDAElement):
    """Reusable effectiveTime element with support for points and intervals."""

    def __init__(
        self,
        value: Optional[datetime] = None,
        low: Optional[datetime] = None,
        high: Optional[datetime] = None,
        null_flavor: Optional[str] = None,
        include_both_value_and_low: bool = False,
        **kwargs,
    ):
        """
        Initialize EffectiveTime builder.

        Args:
            value: Point in time
            low: Start of interval
            high: End of interval
            null_flavor: Null flavor if time is not available
            include_both_value_and_low: If True, include both @value attribute and <low> child (for CONF:1098-32775/32776)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(**kwargs)
        self.value = value
        self.low = low
        self.high = high
        self.null_flavor = null_flavor
        self.include_both_value_and_low = include_both_value_and_low

    def build(self) -> etree.Element:
        """
        Build effectiveTime XML element.

        Returns:
            lxml Element for effectiveTime
        """
        elem = etree.Element(f"{{{NS}}}effectiveTime")

        if self.null_flavor:
            elem.set("nullFlavor", self.null_flavor)
        elif self.include_both_value_and_low and self.value:
            # Special case for CONF:1098-32775/32776: include both @value and <low>
            elem.set("value", self._format_datetime(self.value))
            low = etree.SubElement(elem, f"{{{NS}}}low")
            low.set("value", self._format_datetime(self.value))
        elif self.value:
            # Point in time
            elem.set("value", self._format_datetime(self.value))
        else:
            # Interval - MUST have xsi:type="IVL_TS" when using low/high children
            # This is required by XSD schema for proper type validation
            if self.low or self.high:
                elem.set("{http://www.w3.org/2001/XMLSchema-instance}type", "IVL_TS")

            if self.low:
                low = etree.SubElement(elem, f"{{{NS}}}low")
                low.set("value", self._format_datetime(self.low))

            if self.high:
                high = etree.SubElement(elem, f"{{{NS}}}high")
                high.set("value", self._format_datetime(self.high))
            elif self.low and not self.high:
                # Ongoing - use nullFlavor for high
                high = etree.SubElement(elem, f"{{{NS}}}high")
                high.set("nullFlavor", "UNK")

        return elem

    @staticmethod
    def _format_datetime(dt: datetime) -> str:
        """
        Format datetime to CDA format with timezone for precise times.

        Per C-CDA spec (CONF:81-10130):
        If more precise than day, SHOULD include time-zone offset.

        Format:
        - Date only: YYYYMMDD
        - DateTime: YYYYMMDDHHMMSS-0500 (with timezone)

        Args:
            dt: datetime or date object

        Returns:
            Formatted string with timezone if datetime
        """
        if isinstance(dt, date) and not isinstance(dt, datetime):
            # Date only - no timezone needed
            return dt.strftime("%Y%m%d")
        # Full datetime with timezone offset
        # Format: YYYYMMDDHHMMSS+/-HHMM
        base_time = dt.strftime("%Y%m%d%H%M%S")

        # Add timezone offset
        if dt.tzinfo is not None:
            # Use actual timezone from datetime
            offset = dt.strftime("%z")  # Format: +HHMM or -HHMM
            return f"{base_time}{offset}"
        else:
            # No timezone info - assume local time and add offset
            # For consistency, use UTC-5 (EST) as default
            import time
            if time.daylight:
                # Daylight saving time
                offset_seconds = -time.altzone
            else:
                # Standard time
                offset_seconds = -time.timezone

            # Convert to +/-HHMM format
            offset_hours = offset_seconds // 3600
            offset_minutes = abs(offset_seconds % 3600) // 60
            offset_str = f"{offset_hours:+03d}{offset_minutes:02d}"
            return f"{base_time}{offset_str}"


class Identifier(CDAElement):
    """Reusable ID element builder."""

    def __init__(
        self,
        root: str,
        extension: Optional[str] = None,
        null_flavor: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize Identifier builder.

        Args:
            root: OID or UUID root
            extension: Extension within the root namespace
            null_flavor: Null flavor if ID is not available
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(**kwargs)
        self.root = root
        self.extension = extension
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        """
        Build id XML element.

        Returns:
            lxml Element for id
        """
        elem = etree.Element(f"{{{NS}}}id")

        if self.null_flavor:
            elem.set("nullFlavor", self.null_flavor)
        else:
            elem.set("root", self.root)
            if self.extension:
                elem.set("extension", self.extension)

        return elem


class StatusCode(CDAElement):
    """Reusable statusCode element builder."""

    def __init__(self, code: str, **kwargs):
        """
        Initialize StatusCode builder.

        Args:
            code: Status code value (e.g., 'completed', 'active')
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(**kwargs)
        self.code = code

    def build(self) -> etree.Element:
        """
        Build statusCode XML element.

        Returns:
            lxml Element for statusCode
        """
        elem = etree.Element(f"{{{NS}}}statusCode")
        elem.set("code", self.code)
        return elem


def create_default_author_participation(time: Optional[datetime] = None) -> etree.Element:
    """
    Create a default Author Participation element.

    Per C-CDA spec (2.16.840.1.113883.10.20.22.4.119):
    SHOULD contain Author Participation for clinical statements.

    This creates a minimal compliant author participation with:
    - Template ID for Author Participation
    - Time (when authored)
    - AssignedAuthor with minimal required elements

    Args:
        time: Time of authorship (defaults to current time if not provided)

    Returns:
        lxml Element for author participation
    """
    from datetime import datetime

    if time is None:
        time = datetime.now()

    # Create author element
    author_elem = etree.Element(f"{{{NS}}}author")

    # Add template ID for Author Participation (CONF:81-32888)
    template_id = etree.SubElement(author_elem, f"{{{NS}}}templateId")
    template_id.set("root", "2.16.840.1.113883.10.20.22.4.119")

    # Add time (when authored) - REQUIRED
    time_elem = etree.SubElement(author_elem, f"{{{NS}}}time")
    time_elem.set("value", EffectiveTime._format_datetime(time))

    # Add assignedAuthor - REQUIRED
    assigned_author = etree.SubElement(author_elem, f"{{{NS}}}assignedAuthor")

    # Add author ID - REQUIRED
    # Use nullFlavor since we don't have specific author information
    id_elem = etree.SubElement(assigned_author, f"{{{NS}}}id")
    id_elem.set("nullFlavor", "NI")

    # Add NPI id (SHOULD per CONF:1198-32882)
    # This assignedAuthor SHOULD contain zero or one [0..1] id with @root="2.16.840.1.113883.4.6" (NPI)
    npi_id_elem = etree.SubElement(assigned_author, f"{{{NS}}}id")
    npi_id_elem.set("root", "2.16.840.1.113883.4.6")  # National Provider Identifier
    npi_id_elem.set("extension", "1234567890")  # Sample NPI

    # Add code (SHOULD per CONF:1098-31671)
    # Default to general physician code
    code_elem = etree.SubElement(assigned_author, f"{{{NS}}}code")
    code_elem.set("code", "200000000X")  # Allopathic & Osteopathic Physicians
    code_elem.set("codeSystem", "2.16.840.1.113883.6.101")  # NUCC Provider Taxonomy
    code_elem.set("codeSystemName", "NUCC Provider Taxonomy")
    code_elem.set("displayName", "Physician")

    return author_elem
