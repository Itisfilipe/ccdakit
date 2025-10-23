"""Tests for null flavor utilities."""

import pytest

from ccdakit.core.null_flavor import (
    NullFlavor,
    get_null_flavor_for_missing,
    is_null_flavor,
)


def test_null_flavor_enum_values():
    """Test NullFlavor enum has expected values."""
    assert NullFlavor.NI.value == "NI"
    assert NullFlavor.UNK.value == "UNK"
    assert NullFlavor.ASKU.value == "ASKU"
    assert NullFlavor.NA.value == "NA"
    assert NullFlavor.NAV.value == "NAV"


def test_null_flavor_enum_complete():
    """Test all null flavor codes are present."""
    expected_flavors = [
        "NI",
        "INV",
        "DER",
        "OTH",
        "NINF",
        "PINF",
        "UNK",
        "ASKU",
        "NAV",
        "NASK",
        "MSK",
        "NA",
        "NAVU",
    ]

    for flavor in expected_flavors:
        assert hasattr(NullFlavor, flavor)


def test_get_null_flavor_for_missing_not_asked():
    """Test getting null flavor when data was not asked for."""
    flavor = get_null_flavor_for_missing(asked=False)
    assert flavor == NullFlavor.UNK


def test_get_null_flavor_for_missing_asked():
    """Test getting null flavor when data was asked for but not provided."""
    flavor = get_null_flavor_for_missing(asked=True)
    assert flavor == NullFlavor.ASKU


def test_get_null_flavor_for_missing_default():
    """Test default behavior of get_null_flavor_for_missing."""
    flavor = get_null_flavor_for_missing()
    assert flavor == NullFlavor.UNK


def test_is_null_flavor_valid():
    """Test is_null_flavor with valid null flavor codes."""
    assert is_null_flavor("UNK") is True
    assert is_null_flavor("NA") is True
    assert is_null_flavor("ASKU") is True
    assert is_null_flavor("NI") is True


def test_is_null_flavor_invalid():
    """Test is_null_flavor with invalid codes."""
    assert is_null_flavor("INVALID") is False
    assert is_null_flavor("") is False
    assert is_null_flavor("unk") is False  # Case sensitive


def test_is_null_flavor_none():
    """Test is_null_flavor with None."""
    assert is_null_flavor(None) is False


def test_null_flavor_usage_in_code():
    """Test using NullFlavor in code."""
    # Example of how it would be used in a builder
    value = None

    if value is None:
        null_flavor = NullFlavor.UNK.value
    else:
        null_flavor = None

    assert null_flavor == "UNK"


def test_null_flavor_enum_member_by_value():
    """Test accessing NullFlavor by value."""
    flavor = NullFlavor("UNK")
    assert flavor == NullFlavor.UNK


def test_null_flavor_invalid_value_raises():
    """Test that invalid value raises ValueError."""
    with pytest.raises(ValueError):
        NullFlavor("INVALID")


def test_get_null_flavor_for_missing_explicit_asked():
    """Test get_null_flavor_for_missing with explicit asked=True."""
    flavor = get_null_flavor_for_missing(asked=True)
    assert flavor == NullFlavor.ASKU
    assert flavor.value == "ASKU"


def test_is_null_flavor_all_valid_codes():
    """Test is_null_flavor with all valid null flavor codes."""
    valid_codes = ["NI", "INV", "DER", "OTH", "NINF", "PINF", "UNK", "ASKU", "NAV", "NASK", "MSK", "NA", "NAVU"]

    for code in valid_codes:
        assert is_null_flavor(code) is True, f"Expected {code} to be recognized as valid null flavor"


def test_is_null_flavor_exception_handling():
    """Test is_null_flavor handles ValueError gracefully."""
    # These should all return False without raising exceptions
    assert is_null_flavor("INVALID_CODE") is False
    assert is_null_flavor("xyz") is False
    assert is_null_flavor("123") is False
    assert is_null_flavor(" ") is False
