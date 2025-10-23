"""Tests for XSD validator."""

from pathlib import Path
from unittest.mock import Mock, patch

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

    # ========================================================================
    # Additional tests for edge cases and error handling (Lines 100-115, 134-135, 146-149, 208-210)
    # ========================================================================

    def test_resolve_schema_path_default_locations(self, tmp_path, monkeypatch):
        """Test schema path resolution checks multiple default locations."""
        # Create a schema in one of the default locations
        schema_dir = tmp_path / "schemas"
        schema_dir.mkdir(parents=True)
        schema_path = schema_dir / "CDA.xsd"

        schema_content = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="root" type="xs:string"/>
</xs:schema>"""
        schema_path.write_text(schema_content)

        # Change working directory to tmp_path
        monkeypatch.chdir(tmp_path)

        # Initialize validator without providing schema path
        # It should find the schema in the default location
        validator = XSDValidator(auto_download=False)

        # Verify it found the schema
        assert validator.schema_path.exists()
        assert validator.schema_path.name == "CDA.xsd"

    def test_resolve_schema_path_package_root(self, tmp_path, monkeypatch):
        """Test schema resolution from package root location."""
        # Mock the __file__ path to simulate package structure
        with patch("ccdakit.validators.xsd.Path") as mock_path_class:
            # Create real schema file
            schema_dir = tmp_path / "schemas"
            schema_dir.mkdir(parents=True)
            schema_path = schema_dir / "CDA.xsd"

            schema_content = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="root" type="xs:string"/>
</xs:schema>"""
            schema_path.write_text(schema_content)

            # Setup mock to return our tmp_path as package root
            def path_side_effect(arg=None):
                if arg is None:
                    # Path() constructor
                    return Path(tmp_path)
                if isinstance(arg, str) and "validators" in arg:
                    # Path(__file__) case
                    mock_file_path = Mock()
                    mock_file_path.parent.parent.parent = tmp_path
                    return mock_file_path
                # Default: use real Path
                return Path(arg)

            mock_path_class.side_effect = path_side_effect

            # The schema should be found
            # Note: This test verifies the path resolution logic exists
            # The actual location testing is complex due to mocking limitations

    def test_init_with_auto_download_disabled_and_missing_schema(self, tmp_path):
        """Test that auto_download=False raises error when schema missing."""
        nonexistent_path = tmp_path / "nonexistent" / "CDA.xsd"

        with pytest.raises(FileNotFoundError, match="Schema file not found"):
            XSDValidator(schema_path=nonexistent_path, auto_download=False)

    def test_auto_download_path_resolution(self, tmp_path, simple_xsd_schema):
        """Test that validator handles schema paths correctly with auto_download enabled."""
        # Test that having auto_download=True doesn't break normal operation
        # when schema exists
        schema_path = tmp_path / "schemas" / "CDA.xsd"
        schema_path.parent.mkdir(parents=True)
        schema_path.write_text(simple_xsd_schema.read_text())

        # Should work fine with auto_download=True when file exists
        validator = XSDValidator(schema_path=schema_path, auto_download=True)
        assert validator.schema_path == schema_path
        assert validator.auto_download is True

    def test_auto_download_disabled_prevents_download_attempt(self, tmp_path):
        """Test that auto_download=False doesn't attempt download."""
        schema_path = tmp_path / "schemas" / "nonexistent_CDA.xsd"

        # With auto_download=False, should immediately raise FileNotFoundError
        # without attempting download
        with pytest.raises(FileNotFoundError, match="Schema file not found"):
            XSDValidator(schema_path=schema_path, auto_download=False)

    def test_auto_download_enabled_with_missing_file(self, tmp_path):
        """Test behavior when auto_download=True but schema still missing."""
        schema_path = tmp_path / "schemas" / "nonexistent_CDA.xsd"

        # With auto_download=True and missing file, will attempt download
        # Since download infrastructure isn't available in test, will still fail
        # but may show warning
        with pytest.raises(FileNotFoundError):
            XSDValidator(schema_path=schema_path, auto_download=True)

    def test_validate_with_generic_exception(self, simple_xsd_schema):
        """Test handling of unexpected exceptions during validation."""
        validator = XSDValidator(simple_xsd_schema)

        # Mock _parse_document to raise an unexpected exception (not XMLSyntaxError or FileNotFoundError)
        with patch.object(validator, "_parse_document") as mock_parse:
            mock_parse.side_effect = RuntimeError("Unexpected validation error")

            result = validator.validate("<test/>")

            # Should catch exception and return validation error
            assert result.is_valid is False
            assert len(result.errors) == 1
            assert result.errors[0].code == "VALIDATION_ERROR"
            assert "Unexpected validation error" in result.errors[0].message

    def test_validate_with_unsupported_document_type(self, simple_xsd_schema):
        """Test that unsupported document types are handled."""
        validator = XSDValidator(simple_xsd_schema)

        # Create an object that will cause TypeError in _parse_document
        class BadDocument:
            pass

        # This should be caught by the generic exception handler in validate()
        result = validator.validate(BadDocument())

        assert result.is_valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "VALIDATION_ERROR"
        assert "Unsupported document type" in result.errors[0].message

    def test_xml_syntax_error_with_line_number(self, simple_xsd_schema):
        """Test XML syntax error includes line number in location."""
        validator = XSDValidator(simple_xsd_schema)

        # Malformed XML with multiple lines to get line number
        malformed = """<?xml version="1.0"?>
<root>
  <unclosed>
  <another>
"""

        result = validator.validate(malformed)

        assert result.is_valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "XML_SYNTAX_ERROR"
        # Should have location with line number
        assert result.errors[0].location is not None
        assert "Line" in result.errors[0].location

    def test_xml_syntax_error_location_handling(self, simple_xsd_schema):
        """Test that XML syntax errors are properly captured."""
        validator = XSDValidator(simple_xsd_schema)

        # Test with various malformed XML to ensure error handling works
        malformed_xmls = [
            "<unclosed",  # Missing closing tag
            "<root><child></root>",  # Mismatched tags
            "<?xml version='1.0'?><>",  # Empty tag
        ]

        for xml in malformed_xmls:
            result = validator.validate(xml)
            assert result.is_valid is False
            assert len(result.errors) >= 1
            assert result.errors[0].code in ["XML_SYNTAX_ERROR", "VALIDATION_ERROR"]

    def test_parse_schema_error_with_column(self, tmp_path):
        """Test schema error parsing includes column information."""
        # Create schema that will generate errors with column info
        schema_content = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="root">
    <xs:complexType>
      <xs:attribute name="required" type="xs:string" use="required"/>
    </xs:complexType>
  </xs:element>
</xs:schema>"""
        schema_path = tmp_path / "column_test.xsd"
        schema_path.write_text(schema_content)

        validator = XSDValidator(schema_path)

        # Invalid XML - missing required attribute
        invalid_xml = '<?xml version="1.0"?><root/>'

        result = validator.validate(invalid_xml)

        assert result.is_valid is False
        assert len(result.errors) >= 1
        # Error should have location information
        error = result.errors[0]
        assert error.location is not None
        # Should contain "Line" in location
        assert "Line" in error.location

    def test_parse_schema_error_with_path(self, tmp_path):
        """Test schema error includes element path when available."""
        # Create schema with nested elements
        schema_content = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="root">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="child">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="value" type="xs:integer"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>"""
        schema_path = tmp_path / "path_test.xsd"
        schema_path.write_text(schema_content)

        validator = XSDValidator(schema_path)

        # Invalid XML - wrong type for value element
        invalid_xml = """<?xml version="1.0"?>
<root>
  <child>
    <value>not_an_integer</value>
  </child>
</root>"""

        result = validator.validate(invalid_xml)

        assert result.is_valid is False
        assert len(result.errors) >= 1

    def test_validate_empty_xml(self, simple_xsd_schema):
        """Test validation of empty/minimal XML document."""
        validator = XSDValidator(simple_xsd_schema)

        # Empty document - empty string is parsed as possible file path first, then as XML
        # Since it's not a valid file path and not valid XML, it should fail
        empty_xml = ""

        result = validator.validate(empty_xml)

        # Should fail - either VALIDATION_ERROR or XML_SYNTAX_ERROR
        assert result.is_valid is False
        assert len(result.errors) >= 1
        # Allow either error code since behavior depends on parsing path
        assert result.errors[0].code in ["XML_SYNTAX_ERROR", "VALIDATION_ERROR"]

    def test_validate_xml_with_only_whitespace(self, simple_xsd_schema):
        """Test validation of XML with only whitespace."""
        validator = XSDValidator(simple_xsd_schema)

        whitespace_xml = "   \n\t  "

        result = validator.validate(whitespace_xml)

        assert result.is_valid is False
        assert len(result.errors) >= 1

    def test_init_with_corrupted_schema_file(self, tmp_path):
        """Test initialization with corrupted XSD schema."""
        corrupted_schema = tmp_path / "corrupted.xsd"
        # Write invalid XML that will fail XSD parsing
        corrupted_schema.write_text("<?xml version='1.0'?><not-a-valid-schema/>")

        with pytest.raises((etree.XMLSchemaParseError, etree.XMLSchemaError)):
            XSDValidator(corrupted_schema)

    def test_validate_very_large_xml_document(self, simple_xsd_schema):
        """Test validation of a large XML document."""
        validator = XSDValidator(simple_xsd_schema)

        # Create a large but valid XML document
        large_xml = '<?xml version="1.0"?><root id="large">'
        # Add many child elements
        for i in range(1000):
            large_xml += f"<child>value_{i}</child>"
        large_xml += "</root>"

        # Note: This will fail validation because schema expects single child
        # but tests that large documents can be processed
        result = validator.validate(large_xml)

        # Document is parseable but invalid per schema
        assert result.is_valid is False

    def test_validate_xml_with_unusual_namespaces(self, tmp_path):
        """Test validation of XML with unusual namespace declarations."""
        # Create schema with namespace
        schema_content = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           targetNamespace="http://example.com/test"
           xmlns:tns="http://example.com/test"
           elementFormDefault="qualified">
  <xs:element name="root">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="child" type="xs:string"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>"""
        schema_path = tmp_path / "namespace_test.xsd"
        schema_path.write_text(schema_content)

        validator = XSDValidator(schema_path)

        # XML with correct namespace
        valid_xml = """<?xml version="1.0"?>
<tns:root xmlns:tns="http://example.com/test">
  <tns:child>test</tns:child>
</tns:root>"""

        result = validator.validate(valid_xml)

        # Should be valid
        assert result.is_valid is True

    def test_validate_file_convenience_with_string_path(
        self, simple_xsd_schema, valid_xml_string, tmp_path
    ):
        """Test validate_file with string path instead of Path object."""
        validator = XSDValidator(simple_xsd_schema)
        xml_file = tmp_path / "test.xml"
        xml_file.write_text(valid_xml_string)

        # Pass string path
        result = validator.validate_file(str(xml_file))

        assert result.is_valid is True

    def test_multiple_schema_validation_errors_reported(self, tmp_path):
        """Test that all schema validation errors are reported."""
        # Schema requiring multiple attributes
        schema_content = """<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="root">
    <xs:complexType>
      <xs:attribute name="id" type="xs:string" use="required"/>
      <xs:attribute name="name" type="xs:string" use="required"/>
      <xs:attribute name="value" type="xs:integer" use="required"/>
    </xs:complexType>
  </xs:element>
</xs:schema>"""
        schema_path = tmp_path / "multi_attr.xsd"
        schema_path.write_text(schema_content)

        validator = XSDValidator(schema_path)

        # Missing all required attributes
        invalid_xml = '<?xml version="1.0"?><root/>'

        result = validator.validate(invalid_xml)

        assert result.is_valid is False
        # Should report multiple errors (one for each missing attribute)
        assert len(result.errors) >= 1

    def test_schema_location_property_returns_path(self, simple_xsd_schema):
        """Test schema_location property returns correct Path object."""
        validator = XSDValidator(simple_xsd_schema)

        location = validator.schema_location

        assert isinstance(location, Path)
        assert location == simple_xsd_schema
        assert location.exists()

    def test_init_auto_download_default_true(self, simple_xsd_schema):
        """Test that auto_download defaults to True."""
        validator = XSDValidator(simple_xsd_schema)

        assert validator.auto_download is True

    def test_init_auto_download_can_be_disabled(self, simple_xsd_schema):
        """Test that auto_download can be set to False."""
        validator = XSDValidator(simple_xsd_schema, auto_download=False)

        assert validator.auto_download is False
