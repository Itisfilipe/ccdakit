"""Tests for base validator functionality."""

from pathlib import Path

import pytest
from lxml import etree

from ccdakit.core.validation import ValidationResult
from ccdakit.validators.base import BaseValidator


class MockValidator(BaseValidator):
    """Mock validator for testing base functionality."""

    def validate(self, document) -> ValidationResult:
        """Simple validation that always passes."""
        self._parse_document(document)  # Test parsing
        return ValidationResult()


class TestBaseValidator:
    """Test suite for BaseValidator."""

    @pytest.fixture
    def validator(self):
        """Create mock validator instance."""
        return MockValidator()

    @pytest.fixture
    def sample_xml_string(self):
        """Sample XML string."""
        return '<?xml version="1.0"?><root><child>test</child></root>'

    @pytest.fixture
    def sample_xml_bytes(self, sample_xml_string):
        """Sample XML as bytes."""
        return sample_xml_string.encode("utf-8")

    @pytest.fixture
    def sample_xml_element(self, sample_xml_string):
        """Sample XML as lxml Element."""
        return etree.fromstring(sample_xml_string.encode("utf-8"))

    @pytest.fixture
    def temp_xml_file(self, sample_xml_string, tmp_path):
        """Create temporary XML file."""
        file_path = tmp_path / "test.xml"
        file_path.write_text(sample_xml_string)
        return file_path

    def test_parse_document_from_element(self, validator, sample_xml_element):
        """Test parsing document from lxml Element."""
        result = validator._parse_document(sample_xml_element)
        assert isinstance(result, etree._Element)
        assert result.tag == "root"

    def test_parse_document_from_string(self, validator, sample_xml_string):
        """Test parsing document from XML string."""
        result = validator._parse_document(sample_xml_string)
        assert isinstance(result, etree._Element)
        assert result.tag == "root"

    def test_parse_document_from_bytes(self, validator, sample_xml_bytes):
        """Test parsing document from bytes."""
        result = validator._parse_document(sample_xml_bytes)
        assert isinstance(result, etree._Element)
        assert result.tag == "root"

    def test_parse_document_from_path_object(self, validator, temp_xml_file):
        """Test parsing document from Path object."""
        result = validator._parse_document(temp_xml_file)
        assert isinstance(result, etree._Element)
        assert result.tag == "root"

    def test_parse_document_from_path_string(self, validator, temp_xml_file):
        """Test parsing document from path string."""
        result = validator._parse_document(str(temp_xml_file))
        assert isinstance(result, etree._Element)
        assert result.tag == "root"

    def test_parse_document_invalid_xml_string(self, validator):
        """Test parsing invalid XML string raises error."""
        with pytest.raises(etree.XMLSyntaxError):
            validator._parse_document("<invalid>xml")

    def test_parse_document_invalid_xml_bytes(self, validator):
        """Test parsing invalid XML bytes raises error."""
        with pytest.raises(etree.XMLSyntaxError):
            validator._parse_document(b"<invalid>xml")

    def test_parse_document_nonexistent_file(self, validator):
        """Test parsing nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            validator._parse_document(Path("/nonexistent/file.xml"))

    def test_parse_document_invalid_type(self, validator):
        """Test parsing unsupported type raises TypeError."""
        with pytest.raises(TypeError, match="Unsupported document type"):
            validator._parse_document(12345)

    def test_parse_document_invalid_type_list(self, validator):
        """Test parsing list raises TypeError."""
        with pytest.raises(TypeError, match="Unsupported document type"):
            validator._parse_document([])

    def test_validate_method_must_be_implemented(self):
        """Test that validate method must be implemented by subclasses."""
        # BaseValidator is abstract, so instantiation should fail
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            BaseValidator()

    def test_mock_validator_validate(self, validator, sample_xml_string):
        """Test mock validator's validate method."""
        result = validator.validate(sample_xml_string)
        assert isinstance(result, ValidationResult)
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_with_element(self, validator, sample_xml_element):
        """Test validating with Element input."""
        result = validator.validate(sample_xml_element)
        assert result.is_valid is True

    def test_validate_with_bytes(self, validator, sample_xml_bytes):
        """Test validating with bytes input."""
        result = validator.validate(sample_xml_bytes)
        assert result.is_valid is True

    def test_validate_with_path(self, validator, temp_xml_file):
        """Test validating with Path input."""
        result = validator.validate(temp_xml_file)
        assert result.is_valid is True
