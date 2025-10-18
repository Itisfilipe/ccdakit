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
