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
        **kwargs,
    ):
        """
        Initialize EffectiveTime builder.

        Args:
            value: Point in time
            low: Start of interval
            high: End of interval
            null_flavor: Null flavor if time is not available
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(**kwargs)
        self.value = value
        self.low = low
        self.high = high
        self.null_flavor = null_flavor

    def build(self) -> etree.Element:
        """
        Build effectiveTime XML element.

        Returns:
            lxml Element for effectiveTime
        """
        elem = etree.Element(f"{{{NS}}}effectiveTime")

        if self.null_flavor:
            elem.set("nullFlavor", self.null_flavor)
        elif self.value:
            # Point in time
            elem.set("value", self._format_datetime(self.value))
        else:
            # Interval
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
        Format datetime to CDA format: YYYYMMDDHHMMSS.

        Args:
            dt: datetime or date object

        Returns:
            Formatted string
        """
        if isinstance(dt, date) and not isinstance(dt, datetime):
            # Date only
            return dt.strftime("%Y%m%d")
        # Full datetime with precision
        return dt.strftime("%Y%m%d%H%M%S")


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
