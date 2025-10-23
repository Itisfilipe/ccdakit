"""Null flavor utilities for C-CDA documents.

This module provides standardized null flavor handling according to HL7 C-CDA specification.
Null flavors are used to indicate why data is missing or unknown in SHALL elements.

Null Flavor Values:
    NI: No Information - The value is not available because it was not sought
    UNK: Unknown - A proper value is applicable but is not known
    NA: Not Applicable - No proper value is applicable in this context
    ASKU: Asked but Unknown - Information was sought but not found
    OTH: Other - The actual value is not a member of the set of permitted values
    NASK: Not Asked - This information has not been sought
    MSK: Masked - There is information but it has been masked for security/privacy
    NP: Not Present - The value is exceptional and should be referenced elsewhere
    NINF: Negative Infinity - The value is negative infinity
    PINF: Positive Infinity - The value is positive infinity

Common Usage Patterns:
    - SHALL element with no data: Use "NI" (No Information)
    - Date/time unknown: Use "UNK" (Unknown)
    - Code not in value set: Use "OTH" (Other) with originalText
    - High element for ongoing status: Use "UNK" (Unknown)
    - Not applicable in context: Use "NA" (Not Applicable)
"""

from typing import Optional

from lxml import etree

# CDA namespace
NS = "urn:hl7-org:v3"


class NullFlavor:
    """Standard null flavor values per HL7 V3 specification."""

    # Common null flavors (from HL7 NullFlavor vocabulary)
    NO_INFORMATION = "NI"  # No information (value not sought)
    UNKNOWN = "UNK"  # Unknown (proper value applicable but not known)
    NOT_APPLICABLE = "NA"  # Not applicable in this context
    ASKED_BUT_UNKNOWN = "ASKU"  # Asked but unknown
    OTHER = "OTH"  # Other (actual value not in permitted set)
    NOT_ASKED = "NASK"  # Not asked
    MASKED = "MSK"  # Masked for security/privacy
    NOT_PRESENT = "NP"  # Not present (exceptional, referenced elsewhere)
    NEGATIVE_INFINITY = "NINF"  # Negative infinity
    POSITIVE_INFINITY = "PINF"  # Positive infinity

    # Null flavor code system OID
    NULL_FLAVOR_OID = "2.16.840.1.113883.5.1008"

    @classmethod
    def all_values(cls) -> list[str]:
        """Get all valid null flavor values.

        Returns:
            List of all null flavor codes
        """
        return [
            cls.NO_INFORMATION,
            cls.UNKNOWN,
            cls.NOT_APPLICABLE,
            cls.ASKED_BUT_UNKNOWN,
            cls.OTHER,
            cls.NOT_ASKED,
            cls.MASKED,
            cls.NOT_PRESENT,
            cls.NEGATIVE_INFINITY,
            cls.POSITIVE_INFINITY,
        ]

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Check if a value is a valid null flavor.

        Args:
            value: Null flavor value to check

        Returns:
            True if valid null flavor, False otherwise
        """
        return value.upper() in cls.all_values()


def add_null_flavor(element: etree._Element, null_flavor: str) -> None:
    """Add nullFlavor attribute to an element.

    Args:
        element: XML element to add null flavor to
        null_flavor: Null flavor code (e.g., "NI", "UNK", "NA")

    Raises:
        ValueError: If null_flavor is not a valid null flavor code
    """
    if not NullFlavor.is_valid(null_flavor):
        raise ValueError(
            f"Invalid null flavor: {null_flavor}. "
            f"Must be one of: {', '.join(NullFlavor.all_values())}"
        )
    element.set("nullFlavor", null_flavor.upper())


def create_null_code(
    null_flavor: str = NullFlavor.OTHER,
    original_text: Optional[str] = None,
    tag_name: str = "code",
) -> etree._Element:
    """Create a code element with null flavor.

    Used when a coded value is required but not available or not in value set.

    Args:
        null_flavor: Null flavor to use (default: "OTH")
        original_text: Optional text description to include
        tag_name: Tag name for the element (default: "code")

    Returns:
        XML element with nullFlavor attribute

    Example:
        >>> code_elem = create_null_code("OTH", "Custom medication")
        >>> # <code nullFlavor="OTH"><originalText>Custom medication</originalText></code>
    """
    elem = etree.Element(f"{{{NS}}}{tag_name}")
    add_null_flavor(elem, null_flavor)

    if original_text:
        text_elem = etree.SubElement(elem, f"{{{NS}}}originalText")
        text_elem.text = original_text

    return elem


def create_null_value(
    xsi_type: str,
    null_flavor: str = NullFlavor.UNKNOWN,
    original_text: Optional[str] = None,
) -> etree._Element:
    """Create a value element with null flavor.

    Used when an observation value is required but not available.

    Args:
        xsi_type: xsi:type attribute value (e.g., "CD", "PQ", "ST")
        null_flavor: Null flavor to use (default: "UNK")
        original_text: Optional text description to include

    Returns:
        XML element with nullFlavor and xsi:type attributes

    Example:
        >>> value_elem = create_null_value("CD", "OTH", "Patient reported severity")
        >>> # <value xsi:type="CD" nullFlavor="OTH">
        >>> #   <originalText>Patient reported severity</originalText>
        >>> # </value>
    """
    elem = etree.Element(f"{{{NS}}}value")
    elem.set(f"{{{NS}}}type", xsi_type)
    add_null_flavor(elem, null_flavor)

    if original_text:
        text_elem = etree.SubElement(elem, f"{{{NS}}}originalText")
        text_elem.text = original_text

    return elem


def create_null_id(
    null_flavor: str = NullFlavor.UNKNOWN,
) -> etree._Element:
    """Create an id element with null flavor.

    Used when an identifier is required but not available.

    Args:
        null_flavor: Null flavor to use (default: "UNK")

    Returns:
        XML id element with nullFlavor attribute

    Example:
        >>> id_elem = create_null_id("UNK")
        >>> # <id nullFlavor="UNK"/>
    """
    elem = etree.Element(f"{{{NS}}}id")
    add_null_flavor(elem, null_flavor)
    return elem


def create_null_time(
    null_flavor: str = NullFlavor.UNKNOWN,
    tag_name: str = "effectiveTime",
) -> etree._Element:
    """Create a time element with null flavor.

    Used when a time value is required but not available.

    Args:
        null_flavor: Null flavor to use (default: "UNK")
        tag_name: Tag name for the element (default: "effectiveTime")

    Returns:
        XML time element with nullFlavor attribute

    Example:
        >>> time_elem = create_null_time("UNK")
        >>> # <effectiveTime nullFlavor="UNK"/>
    """
    elem = etree.Element(f"{{{NS}}}{tag_name}")
    add_null_flavor(elem, null_flavor)
    return elem


def create_null_time_low(
    null_flavor: str = NullFlavor.UNKNOWN,
) -> etree._Element:
    """Create a low time element with null flavor.

    Used in effectiveTime intervals when start date is unknown.

    Args:
        null_flavor: Null flavor to use (default: "UNK")

    Returns:
        XML low element with nullFlavor attribute

    Example:
        >>> low_elem = create_null_time_low("UNK")
        >>> # <low nullFlavor="UNK"/>
    """
    elem = etree.Element(f"{{{NS}}}low")
    add_null_flavor(elem, null_flavor)
    return elem


def create_null_time_high(
    null_flavor: str = NullFlavor.UNKNOWN,
) -> etree._Element:
    """Create a high time element with null flavor.

    Used in effectiveTime intervals when end date is unknown or ongoing.
    Use "UNK" for unknown end date, "NA" for not applicable (no end date).

    Args:
        null_flavor: Null flavor to use (default: "UNK")

    Returns:
        XML high element with nullFlavor attribute

    Example:
        >>> high_elem = create_null_time_high("UNK")
        >>> # <high nullFlavor="UNK"/>
    """
    elem = etree.Element(f"{{{NS}}}high")
    add_null_flavor(elem, null_flavor)
    return elem


def should_use_null_flavor(value: Optional[str], required: bool = True) -> bool:
    """Determine if null flavor should be used for a value.

    Args:
        value: The value to check
        required: Whether the element is required (SHALL)

    Returns:
        True if null flavor should be used, False otherwise

    Example:
        >>> should_use_null_flavor(None, required=True)
        True
        >>> should_use_null_flavor("some value", required=True)
        False
        >>> should_use_null_flavor(None, required=False)
        False
    """
    # If value exists, don't use null flavor
    if value is not None and value != "":
        return False

    # If required (SHALL) and no value, use null flavor
    if required:
        return True

    # If not required (MAY/SHOULD) and no value, omit element
    return False


def get_default_null_flavor_for_element(element_type: str) -> str:
    """Get the recommended default null flavor for common element types.

    Args:
        element_type: Type of element (e.g., "code", "value", "id", "time", "high", "low")

    Returns:
        Recommended null flavor code

    Example:
        >>> get_default_null_flavor_for_element("code")
        'OTH'
        >>> get_default_null_flavor_for_element("id")
        'UNK'
    """
    defaults = {
        "code": NullFlavor.OTHER,  # Code not in value set
        "value": NullFlavor.OTHER,  # Value not in permitted set
        "id": NullFlavor.UNKNOWN,  # ID not available
        "time": NullFlavor.UNKNOWN,  # Time not known
        "effectivetime": NullFlavor.UNKNOWN,  # Time not known
        "low": NullFlavor.UNKNOWN,  # Start time not known
        "high": NullFlavor.UNKNOWN,  # End time not known (or use NA for ongoing)
        "section": NullFlavor.NO_INFORMATION,  # No information available for section
    }
    return defaults.get(element_type.lower(), NullFlavor.NO_INFORMATION)
