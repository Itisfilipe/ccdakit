"""Builders for demographic elements (Address, Telecom)."""

from lxml import etree

from ccdakit.core.base import CDAElement
from ccdakit.protocols.patient import AddressProtocol, TelecomProtocol


# CDA namespace for element creation
NS = "urn:hl7-org:v3"


class Address(CDAElement):
    """Builder for CDA address elements."""

    # HL7 AddressUse codes
    USE_CODES = {
        "home": "HP",  # Primary home
        "work": "WP",  # Work place
        "temp": "TMP",  # Temporary
        "old": "OLD",  # No longer in use
        "physical": "PHYS",  # Physical visit address
        "postal": "PST",  # Postal address
    }

    def __init__(self, address: AddressProtocol, use: str = None, **kwargs):
        """
        Initialize Address builder.

        Args:
            address: Address data satisfying AddressProtocol
            use: Use code ('home', 'work', etc.) or HL7 code directly
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(**kwargs)
        self.address = address
        self.use = use

    def build(self) -> etree.Element:
        """
        Build address XML element.

        Returns:
            lxml Element for addr
        """
        elem = etree.Element(f"{{{NS}}}addr")

        # Add use attribute if specified
        if self.use:
            use_code = self.USE_CODES.get(self.use, self.use)
            elem.set("use", use_code)

        # Add street lines
        for line in self.address.street_lines:
            street = etree.SubElement(elem, f"{{{NS}}}streetAddressLine")
            street.text = line

        # Add city
        city = etree.SubElement(elem, f"{{{NS}}}city")
        city.text = self.address.city

        # Add state
        state = etree.SubElement(elem, f"{{{NS}}}state")
        state.text = self.address.state

        # Add postal code
        postal = etree.SubElement(elem, f"{{{NS}}}postalCode")
        postal.text = self.address.postal_code

        # Add country
        country = etree.SubElement(elem, f"{{{NS}}}country")
        country.text = self.address.country

        return elem


class Telecom(CDAElement):
    """Builder for CDA telecom (contact) elements."""

    # HL7 TelecomUse codes
    USE_CODES = {
        "home": "HP",  # Primary home
        "work": "WP",  # Work place
        "mobile": "MC",  # Mobile contact
        "emergency": "EC",  # Emergency contact
    }

    def __init__(self, telecom: TelecomProtocol, **kwargs):
        """
        Initialize Telecom builder.

        Args:
            telecom: Telecom data satisfying TelecomProtocol
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(**kwargs)
        self.telecom = telecom

    def build(self) -> etree.Element:
        """
        Build telecom XML element.

        Returns:
            lxml Element for telecom
        """
        elem = etree.Element(f"{{{NS}}}telecom")

        # Build value based on type
        value = self._build_value()
        elem.set("value", value)

        # Add use attribute if specified
        if self.telecom.use:
            use_code = self.USE_CODES.get(self.telecom.use, self.telecom.use)
            elem.set("use", use_code)

        return elem

    def _build_value(self) -> str:
        """
        Build the value attribute based on telecom type.

        Returns:
            Formatted value string (e.g., 'tel:+1-617-555-1234', 'mailto:foo@example.com')
        """
        telecom_type = self.telecom.type.lower()
        value = self.telecom.value

        if telecom_type == "phone":
            # Format: tel:+1-555-555-5555
            return f"tel:{value}"
        elif telecom_type == "fax":
            # Format: fax:+1-555-555-5555
            return f"tel:{value}"
        elif telecom_type == "email":
            # Format: mailto:user@example.com
            return f"mailto:{value}"
        elif telecom_type == "url":
            # Format: http://example.com or https://example.com
            if not value.startswith(("http://", "https://")):
                return f"http://{value}"
            return value
        else:
            # Default: return as-is
            return value
