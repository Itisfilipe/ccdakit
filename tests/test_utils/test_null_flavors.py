"""Tests for null flavor utilities."""

import pytest
from lxml import etree

from ccdakit.utils.null_flavors import (
    NullFlavor,
    add_null_flavor,
    create_null_code,
    create_null_id,
    create_null_time,
    create_null_time_high,
    create_null_time_low,
    create_null_value,
    get_default_null_flavor_for_element,
    should_use_null_flavor,
)


NS = "urn:hl7-org:v3"


class TestNullFlavorConstants:
    """Test null flavor constant values."""

    def test_standard_null_flavors(self):
        """Test that standard null flavor values are defined correctly."""
        assert NullFlavor.NO_INFORMATION == "NI"
        assert NullFlavor.UNKNOWN == "UNK"
        assert NullFlavor.NOT_APPLICABLE == "NA"
        assert NullFlavor.ASKED_BUT_UNKNOWN == "ASKU"
        assert NullFlavor.OTHER == "OTH"
        assert NullFlavor.NOT_ASKED == "NASK"
        assert NullFlavor.MASKED == "MSK"
        assert NullFlavor.NOT_PRESENT == "NP"

    def test_all_values(self):
        """Test that all_values returns complete list."""
        all_values = NullFlavor.all_values()
        assert len(all_values) == 10
        assert "NI" in all_values
        assert "UNK" in all_values
        assert "NA" in all_values
        assert "ASKU" in all_values
        assert "OTH" in all_values

    def test_is_valid(self):
        """Test null flavor validation."""
        assert NullFlavor.is_valid("NI")
        assert NullFlavor.is_valid("UNK")
        assert NullFlavor.is_valid("NA")
        assert NullFlavor.is_valid("unk")  # Case insensitive
        assert not NullFlavor.is_valid("INVALID")
        assert not NullFlavor.is_valid("ABC")

    def test_null_flavor_oid(self):
        """Test that null flavor OID is correct."""
        assert NullFlavor.NULL_FLAVOR_OID == "2.16.840.1.113883.5.1008"


class TestAddNullFlavor:
    """Test add_null_flavor function."""

    def test_add_valid_null_flavor(self):
        """Test adding valid null flavor to element."""
        elem = etree.Element(f"{{{NS}}}code")
        add_null_flavor(elem, "NI")
        assert elem.get("nullFlavor") == "NI"

    def test_add_null_flavor_case_insensitive(self):
        """Test that null flavor is converted to uppercase."""
        elem = etree.Element(f"{{{NS}}}code")
        add_null_flavor(elem, "unk")
        assert elem.get("nullFlavor") == "UNK"

    def test_add_invalid_null_flavor_raises(self):
        """Test that invalid null flavor raises ValueError."""
        elem = etree.Element(f"{{{NS}}}code")
        with pytest.raises(ValueError, match="Invalid null flavor"):
            add_null_flavor(elem, "INVALID")

    def test_add_null_flavor_multiple_times(self):
        """Test that null flavor can be overwritten."""
        elem = etree.Element(f"{{{NS}}}code")
        add_null_flavor(elem, "NI")
        assert elem.get("nullFlavor") == "NI"
        add_null_flavor(elem, "UNK")
        assert elem.get("nullFlavor") == "UNK"


class TestCreateNullCode:
    """Test create_null_code function."""

    def test_create_null_code_default(self):
        """Test creating null code with default values."""
        elem = create_null_code()
        assert elem.tag == f"{{{NS}}}code"
        assert elem.get("nullFlavor") == "OTH"
        assert len(elem) == 0  # No children

    def test_create_null_code_with_text(self):
        """Test creating null code with original text."""
        elem = create_null_code("OTH", "Custom medication")
        assert elem.get("nullFlavor") == "OTH"
        original_text = elem.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "Custom medication"

    def test_create_null_code_different_flavor(self):
        """Test creating null code with different null flavor."""
        elem = create_null_code("UNK")
        assert elem.get("nullFlavor") == "UNK"

    def test_create_null_code_custom_tag(self):
        """Test creating null code with custom tag name."""
        elem = create_null_code("OTH", tag_name="translation")
        assert elem.tag == f"{{{NS}}}translation"
        assert elem.get("nullFlavor") == "OTH"


class TestCreateNullValue:
    """Test create_null_value function."""

    def test_create_null_value_default(self):
        """Test creating null value with default values."""
        elem = create_null_value("CD")
        assert elem.tag == f"{{{NS}}}value"
        assert elem.get(f"{{{NS}}}type") == "CD"
        assert elem.get("nullFlavor") == "UNK"

    def test_create_null_value_with_text(self):
        """Test creating null value with original text."""
        elem = create_null_value("CD", "OTH", "Patient reported")
        assert elem.get("nullFlavor") == "OTH"
        original_text = elem.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "Patient reported"

    def test_create_null_value_different_types(self):
        """Test creating null value with different xsi:type values."""
        elem_cd = create_null_value("CD", "OTH")
        assert elem_cd.get(f"{{{NS}}}type") == "CD"

        elem_pq = create_null_value("PQ", "UNK")
        assert elem_pq.get(f"{{{NS}}}type") == "PQ"

        elem_st = create_null_value("ST", "NI")
        assert elem_st.get(f"{{{NS}}}type") == "ST"


class TestCreateNullId:
    """Test create_null_id function."""

    def test_create_null_id_default(self):
        """Test creating null id with default values."""
        elem = create_null_id()
        assert elem.tag == f"{{{NS}}}id"
        assert elem.get("nullFlavor") == "UNK"

    def test_create_null_id_custom_flavor(self):
        """Test creating null id with custom null flavor."""
        elem = create_null_id("NI")
        assert elem.get("nullFlavor") == "NI"


class TestCreateNullTime:
    """Test create_null_time function."""

    def test_create_null_time_default(self):
        """Test creating null time with default values."""
        elem = create_null_time()
        assert elem.tag == f"{{{NS}}}effectiveTime"
        assert elem.get("nullFlavor") == "UNK"

    def test_create_null_time_custom_flavor(self):
        """Test creating null time with custom null flavor."""
        elem = create_null_time("NI")
        assert elem.get("nullFlavor") == "NI"

    def test_create_null_time_custom_tag(self):
        """Test creating null time with custom tag name."""
        elem = create_null_time("UNK", tag_name="time")
        assert elem.tag == f"{{{NS}}}time"
        assert elem.get("nullFlavor") == "UNK"


class TestCreateNullTimeLow:
    """Test create_null_time_low function."""

    def test_create_null_time_low_default(self):
        """Test creating null low time with default values."""
        elem = create_null_time_low()
        assert elem.tag == f"{{{NS}}}low"
        assert elem.get("nullFlavor") == "UNK"

    def test_create_null_time_low_custom_flavor(self):
        """Test creating null low time with custom null flavor."""
        elem = create_null_time_low("NI")
        assert elem.get("nullFlavor") == "NI"


class TestCreateNullTimeHigh:
    """Test create_null_time_high function."""

    def test_create_null_time_high_default(self):
        """Test creating null high time with default values."""
        elem = create_null_time_high()
        assert elem.tag == f"{{{NS}}}high"
        assert elem.get("nullFlavor") == "UNK"

    def test_create_null_time_high_custom_flavor(self):
        """Test creating null high time with custom null flavor."""
        elem = create_null_time_high("NA")
        assert elem.get("nullFlavor") == "NA"


class TestShouldUseNullFlavor:
    """Test should_use_null_flavor function."""

    def test_should_use_null_flavor_required_with_none(self):
        """Test that null flavor should be used for required element with None."""
        assert should_use_null_flavor(None, required=True)

    def test_should_use_null_flavor_required_with_empty_string(self):
        """Test that null flavor should be used for required element with empty string."""
        assert should_use_null_flavor("", required=True)

    def test_should_not_use_null_flavor_with_value(self):
        """Test that null flavor should not be used when value exists."""
        assert not should_use_null_flavor("some value", required=True)
        assert not should_use_null_flavor("some value", required=False)

    def test_should_not_use_null_flavor_optional_with_none(self):
        """Test that null flavor should not be used for optional element with None."""
        assert not should_use_null_flavor(None, required=False)

    def test_should_not_use_null_flavor_optional_with_empty(self):
        """Test that null flavor should not be used for optional element with empty."""
        assert not should_use_null_flavor("", required=False)


class TestGetDefaultNullFlavor:
    """Test get_default_null_flavor_for_element function."""

    def test_default_for_code(self):
        """Test default null flavor for code element."""
        assert get_default_null_flavor_for_element("code") == "OTH"

    def test_default_for_value(self):
        """Test default null flavor for value element."""
        assert get_default_null_flavor_for_element("value") == "OTH"

    def test_default_for_id(self):
        """Test default null flavor for id element."""
        assert get_default_null_flavor_for_element("id") == "UNK"

    def test_default_for_time_elements(self):
        """Test default null flavor for time elements."""
        assert get_default_null_flavor_for_element("time") == "UNK"
        assert get_default_null_flavor_for_element("effectiveTime") == "UNK"
        assert get_default_null_flavor_for_element("low") == "UNK"
        assert get_default_null_flavor_for_element("high") == "UNK"

    def test_default_for_section(self):
        """Test default null flavor for section element."""
        assert get_default_null_flavor_for_element("section") == "NI"

    def test_default_for_unknown_element(self):
        """Test default null flavor for unknown element type."""
        assert get_default_null_flavor_for_element("unknown") == "NI"

    def test_case_insensitive(self):
        """Test that element type matching is case insensitive."""
        assert get_default_null_flavor_for_element("CODE") == "OTH"
        assert get_default_null_flavor_for_element("Code") == "OTH"


class TestIntegrationScenarios:
    """Test integration scenarios for null flavor usage."""

    def test_code_with_original_text_scenario(self):
        """Test creating code with nullFlavor and originalText."""
        # Scenario: Custom medication not in RxNorm
        elem = create_null_code("OTH", "Patient's home remedy tea")

        assert elem.get("nullFlavor") == "OTH"
        original_text = elem.find(f"{{{NS}}}originalText")
        assert original_text is not None
        assert original_text.text == "Patient's home remedy tea"

    def test_unknown_onset_date_scenario(self):
        """Test creating effectiveTime with unknown onset."""
        # Scenario: Patient doesn't remember when allergy started
        low_elem = create_null_time_low("UNK")

        assert low_elem.get("nullFlavor") == "UNK"

    def test_ongoing_condition_scenario(self):
        """Test creating high element for ongoing condition."""
        # Scenario: Condition is ongoing with no end date
        high_elem = create_null_time_high("UNK")

        assert high_elem.get("nullFlavor") == "UNK"

    def test_severity_not_in_value_set_scenario(self):
        """Test creating severity value not in SNOMED."""
        # Scenario: Patient reported custom severity description
        elem = create_null_value("CD", "OTH", "Somewhat uncomfortable")

        assert elem.get(f"{{{NS}}}type") == "CD"
        assert elem.get("nullFlavor") == "OTH"
        original_text = elem.find(f"{{{NS}}}originalText")
        assert original_text.text == "Somewhat uncomfortable"

    def test_no_information_section_scenario(self):
        """Test section with no information available."""
        # Scenario: No advance directives information available
        section = etree.Element(f"{{{NS}}}section")
        add_null_flavor(section, "NI")

        assert section.get("nullFlavor") == "NI"

    def test_unknown_manufacturer_id_scenario(self):
        """Test creating id for unknown manufacturer."""
        # Scenario: Medical device with unknown manufacturer
        id_elem = create_null_id("UNK")

        assert id_elem.get("nullFlavor") == "UNK"
