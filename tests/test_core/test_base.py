"""Tests for core base classes."""

import pytest
from lxml import etree

from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig


# CDA namespace
NS = "urn:hl7-org:v3"


def local_name(elem):
    """Get local name of element (without namespace)."""
    return etree.QName(elem).localname


def test_cda_version_enum():
    """Test CDAVersion enum values."""
    assert CDAVersion.R2_1.value == "2.1"
    assert CDAVersion.R2_0.value == "2.0"
    assert CDAVersion.R1_1.value == "1.1"
    assert CDAVersion.R3_0.value == "3.0"


def test_template_config_basic():
    """Test TemplateConfig without extension."""
    config = TemplateConfig(root="2.16.840.1.113883.10.20.22.2.5", description="Problem Section")

    elem = config.to_element()
    assert local_name(elem) == "templateId"
    assert elem.get("root") == "2.16.840.1.113883.10.20.22.2.5"
    assert elem.get("extension") is None


def test_template_config_with_extension():
    """Test TemplateConfig with extension."""
    config = TemplateConfig(root="2.16.840.1.113883.10.20.22.2.5", extension="2015-08-01")

    elem = config.to_element()
    assert elem.get("root") == "2.16.840.1.113883.10.20.22.2.5"
    assert elem.get("extension") == "2015-08-01"


class MockElement(CDAElement):
    """Mock implementation of CDAElement for testing."""

    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(root="2.16.840.1.113883.10.20.22.1.1"),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(root="2.16.840.1.113883.10.20.22.1.1", extension="2014-06-09"),
        ],
    }

    def build(self) -> etree._Element:
        """Build test element."""
        elem = etree.Element("test")
        self.add_template_ids(elem)
        return elem


def test_cda_element_build():
    """Test CDAElement builds and adds templates."""
    elem_builder = MockElement(version=CDAVersion.R2_1)
    elem = elem_builder.to_element()

    assert elem.tag == "test"
    templates = elem.findall(f"{{{NS}}}templateId")
    assert len(templates) == 1
    assert templates[0].get("root") == "2.16.840.1.113883.10.20.22.1.1"


def test_cda_element_multiple_templates():
    """Test CDAElement with version that has multiple templates."""
    elem_builder = MockElement(version=CDAVersion.R2_0)
    elem = elem_builder.to_element()

    templates = elem.findall(f"{{{NS}}}templateId")
    assert len(templates) == 1
    assert templates[0].get("root") == "2.16.840.1.113883.10.20.22.1.1"
    assert templates[0].get("extension") == "2014-06-09"


def test_cda_element_to_string():
    """Test CDAElement conversion to string."""
    elem_builder = MockElement(version=CDAVersion.R2_1)
    xml_str = elem_builder.to_string(pretty=False)

    assert "<test>" in xml_str or ":test>" in xml_str  # May have namespace prefix
    assert ":templateId" in xml_str or "<templateId" in xml_str  # May have namespace prefix
    assert "2.16.840.1.113883.10.20.22.1.1" in xml_str


def test_cda_element_to_string_pretty():
    """Test CDAElement conversion to pretty-printed string."""
    elem_builder = MockElement(version=CDAVersion.R2_1)
    xml_str = elem_builder.to_string(pretty=True)

    assert "<test>" in xml_str
    assert "\n" in xml_str  # Should have newlines when pretty-printed


def test_cda_element_unsupported_version():
    """Test CDAElement raises error for unsupported version."""
    elem_builder = MockElement(version=CDAVersion.R1_1)

    with pytest.raises(ValueError, match="Version 1.1 not supported"):
        elem_builder.to_element()


def test_cda_element_get_templates():
    """Test getting templates for a specific version."""
    elem_builder = MockElement(version=CDAVersion.R2_1)
    templates = elem_builder.get_templates()

    assert len(templates) == 1
    assert templates[0].root == "2.16.840.1.113883.10.20.22.1.1"


def test_cda_element_add_template_ids():
    """Test adding template IDs to an element."""
    elem_builder = MockElement(version=CDAVersion.R2_1)
    parent = etree.Element("parent")

    elem_builder.add_template_ids(parent)

    templates = parent.findall(f"{{{NS}}}templateId")
    assert len(templates) == 1


def test_cda_element_with_schema_validation():
    """Test CDAElement with XSD schema validation."""
    from unittest.mock import Mock

    # Create mock schema
    mock_schema = Mock()
    mock_schema.assert_valid = Mock()

    elem_builder = MockElement(version=CDAVersion.R2_1, schema=mock_schema)
    elem = elem_builder.to_element()

    # Schema validation should have been called
    mock_schema.assert_valid.assert_called_once()
    assert elem.tag == "test"


def test_cda_element_initialization_with_schema():
    """Test CDAElement initialization with schema parameter."""
    from unittest.mock import Mock

    mock_schema = Mock()
    elem_builder = MockElement(version=CDAVersion.R2_1, schema=mock_schema)

    assert elem_builder.version == CDAVersion.R2_1
    assert elem_builder.schema == mock_schema


def test_template_config_without_extension():
    """Test TemplateConfig to_element without extension (covers both branches)."""
    config_no_ext = TemplateConfig(root="2.16.840.1.113883.10.20.22.2.5")
    elem_no_ext = config_no_ext.to_element()

    # Verify no extension attribute
    assert elem_no_ext.get("extension") is None
    assert elem_no_ext.get("root") == "2.16.840.1.113883.10.20.22.2.5"


def test_cda_element_to_string_with_encoding():
    """Test CDAElement to_string with different encoding."""
    elem_builder = MockElement(version=CDAVersion.R2_1)

    # Test with utf-8 encoding
    xml_bytes = elem_builder.to_string(encoding="utf-8")
    assert isinstance(xml_bytes, bytes)
    assert b"test" in xml_bytes

    # Test with unicode encoding (default)
    xml_str = elem_builder.to_string(encoding="unicode")
    assert isinstance(xml_str, str)
    assert "test" in xml_str
