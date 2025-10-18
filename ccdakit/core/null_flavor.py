"""Null flavor handling for C-CDA documents."""

from enum import Enum
from typing import Optional


class NullFlavor(Enum):
    """
    Standard HL7 null flavors.

    Used when data is missing or not applicable.
    """

    # No information
    NI = "NI"  # No information
    INV = "INV"  # Invalid
    DER = "DER"  # Derived
    OTH = "OTH"  # Other
    NINF = "NINF"  # Negative infinity
    PINF = "PINF"  # Positive infinity

    # Unknown
    UNK = "UNK"  # Unknown
    ASKU = "ASKU"  # Asked but unknown
    NAV = "NAV"  # Temporarily unavailable
    NASK = "NASK"  # Not asked

    # Masked
    MSK = "MSK"  # Masked

    # Not applicable
    NA = "NA"  # Not applicable
    NAVU = "NAVU"  # Not available


def get_null_flavor_for_missing(asked: bool = False) -> NullFlavor:
    """
    Get appropriate null flavor for missing data.

    Args:
        asked: Whether the data was asked for but not provided

    Returns:
        Appropriate NullFlavor
    """
    return NullFlavor.ASKU if asked else NullFlavor.UNK


def is_null_flavor(value: Optional[str]) -> bool:
    """
    Check if a string is a valid null flavor code.

    Args:
        value: String to check

    Returns:
        True if value is a null flavor code
    """
    if value is None:
        return False
    try:
        NullFlavor(value)
        return True
    except ValueError:
        return False
