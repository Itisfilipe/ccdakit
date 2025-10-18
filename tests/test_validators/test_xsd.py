"""Tests for XSD validator."""

from pathlib import Path

import pytest
from lxml import etree

from ccdakit.core.validation import ValidationLevel, ValidationResult
from ccdakit.validators.xsd import XSDValidator


class TestXSDValidator:
    """Test suite for XSDValidator."""

    @pytest.fixture
    def simple_xsd_schema(self, tmp_path):
        """Create a simple XSD schema for testing."""
        schema_content = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="root">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="child" type="xs:string"/>
      </xs:sequence>
      <xs:attribute name="id" type="xs:string" use="required"/>
    </xs:complexType>
  </xs:element>
</xs:schema>"""
        schema_path = tmp_path / "test_schema.xsd"
        schema_path.write_text(schema_content)
        return schema_path

    @pytest.fixture
    def valid_xml_string(self):
        """Valid XML string matching simple schema."""
        return '<?xml version="1.0"?><root id="1"><child>test</child></root>'

    @pytest.fixture
    def invalid_xml_missing_attr(self):
        """Invalid XML missing required attribute."""
        return '<?xml version="1.0"?><root><child>test</child></root>'

    @pytest.fixture
    def invalid_xml_wrong_element(self):
        """Invalid XML with wrong element."""
        return '<?xml version="1.0"?><root id="1"><wrong>test</wrong></root>'

    @pytest.fixture
    def malformed_xml(self):
        """Malformed XML string."""
        return "<root><unclosed>"

    def test_init_with_valid_schema(self, simple_xsd_schema):
        """Test initializing validator with valid schema."""
        validator = XSDValidator(simple_xsd_schema)
        assert validator.schema_path == simple_xsd_schema
        assert validator.schema is not None

    def test_init_with_nonexistent_schema(self):
        """Test initializing with nonexistent schema raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Schema file not found"):
            XSDValidator("/nonexistent/schema.xsd")

    def test_init_with_invalid_schema(self, tmp_path):
        """Test initializing with invalid XSD raises XMLSchemaParseError."""
        invalid_schema = tmp_path / "invalid.xsd"
        invalid_schema.write_text("<invalid>schema</invalid>")

        with pytest.raises(etree.XMLSchemaParseError):
            XSDValidator(invalid_schema)

    def test_validate_valid_xml_string(self, simple_xsd_schema, valid_xml_string):
        """Test validating valid XML string."""
        validator = XSDValidator(simple_xsd_schema)
        result = validator.validate(valid_xml_string)

        assert isinstance(result, ValidationResult)
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_valid_xml_bytes(self, simple_xsd_schema, valid_xml_string):
        """Test validating valid XML bytes."""
        validator = XSDValidator(simple_xsd_schema)
        result = validator.validate(valid_xml_string.encode("utf-8"))

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_valid_xml_element(self, simple_xsd_schema, valid_xml_string):
        """Test validating valid XML element."""
        validator = XSDValidator(simple_xsd_schema)
        element = etree.fromstring(valid_xml_string.encode("utf-8"))
        result = validator.validate(element)

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_valid_xml_file(self, simple_xsd_schema, valid_xml_string, tmp_path):
        """Test validating valid XML file."""
        validator = XSDValidator(simple_xsd_schema)
        xml_file = tmp_path / "test.xml"
        xml_file.write_text(valid_xml_string)

        result = validator.validate(xml_file)

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_invalid_xml_missing_attr(self, simple_xsd_schema, invalid_xml_missing_attr):
        """Test validating XML with missing required attribute."""
        validator = XSDValidator(simple_xsd_schema)
        result = validator.validate(invalid_xml_missing_attr)

        assert result.is_valid is False
        assert len(result.errors) == 1
        assert result.errors[0].level == ValidationLevel.ERROR
        assert result.errors[0].code == "XSD_VALIDATION_ERROR"
        assert "attribute" in result.errors[0].message.lower()

    def test_validate_invalid_xml_wrong_element(self, simple_xsd_schema, invalid_xml_wrong_element):
        """Test validating XML with wrong element."""
        validator = XSDValidator(simple_xsd_schema)
        result = validator.validate(invalid_xml_wrong_element)

        assert result.is_valid is False
        assert len(result.errors) >= 1
        assert result.errors[0].level == ValidationLevel.ERROR

    def test_validate_malformed_xml(self, simple_xsd_schema, malformed_xml):
        """Test validating malformed XML."""
        validator = XSDValidator(simple_xsd_schema)
        result = validator.validate(malformed_xml)

        assert result.is_valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "XML_SYNTAX_ERROR"
        assert "syntax error" in result.errors[0].message.lower()

    def test_validate_nonexistent_file(self, simple_xsd_schema):
        """Test validating nonexistent file."""
        validator = XSDValidator(simple_xsd_schema)
        result = validator.validate(Path("/nonexistent/file.xml"))

        assert result.is_valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "FILE_NOT_FOUND"

    def test_validate_file_convenience_method(self, simple_xsd_schema, valid_xml_string, tmp_path):
        """Test validate_file convenience method."""
        validator = XSDValidator(simple_xsd_schema)
        xml_file = tmp_path / "test.xml"
        xml_file.write_text(valid_xml_string)

        result = validator.validate_file(xml_file)

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_string_convenience_method(self, simple_xsd_schema, valid_xml_string):
        """Test validate_string convenience method."""
        validator = XSDValidator(simple_xsd_schema)
        result = validator.validate_string(valid_xml_string)

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_bytes_convenience_method(self, simple_xsd_schema, valid_xml_string):
        """Test validate_bytes convenience method."""
        validator = XSDValidator(simple_xsd_schema)
        result = validator.validate_bytes(valid_xml_string.encode("utf-8"))

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_schema_location_property(self, simple_xsd_schema):
        """Test schema_location property."""
        validator = XSDValidator(simple_xsd_schema)
        assert validator.schema_location == simple_xsd_schema

    def test_parse_schema_error_with_location(self, simple_xsd_schema, invalid_xml_missing_attr):
        """Test error parsing includes location information."""
        validator = XSDValidator(simple_xsd_schema)
        result = validator.validate(invalid_xml_missing_attr)

        assert result.is_valid is False
        # Location should be present
        assert result.errors[0].location is not None

    def test_multiple_validation_errors(self, tmp_path):
        """Test handling multiple validation errors."""
        # Create schema requiring multiple elements
        schema_content = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="root">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="required1" type="xs:string"/>
        <xs:element name="required2" type="xs:string"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>"""
        schema_path = tmp_path / "multi.xsd"
        schema_path.write_text(schema_content)

        # XML missing both required elements
        invalid_xml = '<?xml version="1.0"?><root></root>'

        validator = XSDValidator(schema_path)
        result = validator.validate(invalid_xml)

        assert result.is_valid is False
        # Should have at least one error
        assert len(result.errors) >= 1

    def test_init_with_string_path(self, simple_xsd_schema):
        """Test initializing with string path."""
        validator = XSDValidator(str(simple_xsd_schema))
        assert validator.schema_path == Path(simple_xsd_schema)

    def test_validate_with_path_string(self, simple_xsd_schema, valid_xml_string, tmp_path):
        """Test validating with path as string."""
        validator = XSDValidator(simple_xsd_schema)
        xml_file = tmp_path / "test.xml"
        xml_file.write_text(valid_xml_string)

        result = validator.validate(str(xml_file))

        assert result.is_valid is True
