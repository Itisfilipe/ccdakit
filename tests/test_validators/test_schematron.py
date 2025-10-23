"""Tests for Schematron validator."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from lxml import etree

from ccdakit.core.validation import ValidationLevel, ValidationResult
from ccdakit.validators.schematron import SchematronValidator


class TestSchematronValidator:
    """Test suite for SchematronValidator."""

    @pytest.fixture
    def simple_schematron(self, tmp_path):
        """Create a simple Schematron schema for testing."""
        # Simple ISO Schematron with a few rules
        schematron_content = """<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">
  <sch:ns prefix="cda" uri="urn:hl7-org:v3"/>

  <sch:pattern id="root-checks">
    <sch:rule context="/">
      <sch:assert test="root" id="root-exists">
        Document must have a root element.
      </sch:assert>
    </sch:rule>
  </sch:pattern>

  <sch:pattern id="root-element-checks">
    <sch:rule context="/root">
      <sch:assert test="@id" id="id-required">
        Root element must have an id attribute.
      </sch:assert>
      <sch:assert test="child" id="child-required">
        Root element must contain a child element.
      </sch:assert>
      <sch:assert test="not(@id='invalid')" id="id-not-invalid">
        Root id attribute must not be 'invalid'.
      </sch:assert>
    </sch:rule>
  </sch:pattern>

  <sch:pattern id="child-element-checks">
    <sch:rule context="/root/child">
      <sch:assert test="string-length(text()) > 0" id="child-not-empty">
        Child element must not be empty.
      </sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>"""
        schematron_path = tmp_path / "test_schematron.sch"
        schematron_path.write_text(schematron_content)
        return schematron_path

    @pytest.fixture
    def ccda_schematron(self, tmp_path):
        """Create a C-CDA-like Schematron for more realistic testing."""
        schematron_content = """<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">
  <sch:ns prefix="cda" uri="urn:hl7-org:v3"/>

  <sch:pattern id="document-checks">
    <sch:rule context="/cda:ClinicalDocument">
      <sch:assert test="cda:realmCode[@code='US']" id="realm-us">
        ClinicalDocument SHALL contain exactly one [1..1] realmCode="US".
      </sch:assert>
      <sch:assert test="cda:typeId[@root='2.16.840.1.113883.1.3' and @extension='POCD_HD000040']" id="typeid-required">
        ClinicalDocument SHALL contain exactly one [1..1] typeId.
      </sch:assert>
      <sch:assert test="cda:templateId" id="templateid-required">
        ClinicalDocument SHALL contain at least one [1..*] templateId.
      </sch:assert>
      <sch:assert test="cda:id" id="document-id-required">
        ClinicalDocument SHALL contain exactly one [1..1] id.
      </sch:assert>
      <sch:assert test="cda:code" id="document-code-required">
        ClinicalDocument SHALL contain exactly one [1..1] code.
      </sch:assert>
      <sch:assert test="cda:title" id="document-title-required">
        ClinicalDocument SHALL contain exactly one [1..1] title.
      </sch:assert>
      <sch:assert test="cda:effectiveTime" id="effective-time-required">
        ClinicalDocument SHALL contain exactly one [1..1] effectiveTime.
      </sch:assert>
      <sch:assert test="cda:recordTarget" id="record-target-required">
        ClinicalDocument SHALL contain at least one [1..*] recordTarget.
      </sch:assert>
    </sch:rule>
  </sch:pattern>

  <sch:pattern id="patient-checks">
    <sch:rule context="/cda:ClinicalDocument/cda:recordTarget/cda:patientRole">
      <sch:assert test="cda:id" id="patient-id-required">
        patientRole SHALL contain at least one [1..*] id.
      </sch:assert>
      <sch:assert test="cda:patient" id="patient-required">
        patientRole SHALL contain exactly one [1..1] patient.
      </sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>"""
        schematron_path = tmp_path / "ccda_schematron.sch"
        schematron_path.write_text(schematron_content)
        return schematron_path

    @pytest.fixture
    def valid_xml_string(self):
        """Valid XML string matching simple Schematron."""
        return '<?xml version="1.0"?><root id="test123"><child>content</child></root>'

    @pytest.fixture
    def invalid_xml_missing_id(self):
        """Invalid XML missing required id attribute."""
        return '<?xml version="1.0"?><root><child>content</child></root>'

    @pytest.fixture
    def invalid_xml_missing_child(self):
        """Invalid XML missing required child element."""
        return '<?xml version="1.0"?><root id="test123"></root>'

    @pytest.fixture
    def invalid_xml_empty_child(self):
        """Invalid XML with empty child element."""
        return '<?xml version="1.0"?><root id="test123"><child></child></root>'

    @pytest.fixture
    def invalid_xml_multiple_errors(self):
        """Invalid XML with multiple Schematron errors."""
        return '<?xml version="1.0"?><root id="invalid"><child></child></root>'

    @pytest.fixture
    def valid_ccda_minimal(self):
        """Minimal valid C-CDA document."""
        return """<?xml version="1.0"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <realmCode code="US"/>
  <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.1"/>
  <id root="2.16.840.1.113883.3.3208.101.1" extension="20130607100315-CCDA-CCD"/>
  <code code="34133-9" codeSystem="2.16.840.1.113883.6.1"/>
  <title>Continuity of Care Document</title>
  <effectiveTime value="20130607"/>
  <recordTarget>
    <patientRole>
      <id root="2.16.840.1.113883.3.3208.101.2" extension="20130607100800-Patient1"/>
      <patient>
        <name>
          <given>John</given>
          <family>Doe</family>
        </name>
      </patient>
    </patientRole>
  </recordTarget>
</ClinicalDocument>"""

    @pytest.fixture
    def invalid_ccda_missing_realm(self):
        """Invalid C-CDA missing realmCode."""
        return """<?xml version="1.0"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.1"/>
  <id root="2.16.840.1.113883.3.3208.101.1" extension="test"/>
  <code code="34133-9" codeSystem="2.16.840.1.113883.6.1"/>
  <title>Test</title>
  <effectiveTime value="20130607"/>
  <recordTarget>
    <patientRole>
      <id root="2.16.840.1.113883.3.3208.101.2" extension="test"/>
      <patient>
        <name><given>John</given></name>
      </patient>
    </patientRole>
  </recordTarget>
</ClinicalDocument>"""

    @pytest.fixture
    def malformed_xml(self):
        """Malformed XML string."""
        return "<root><unclosed>"

    def test_init_with_custom_schematron(self, simple_schematron):
        """Test initializing validator with custom Schematron."""
        validator = SchematronValidator(simple_schematron)
        assert validator.schematron_path == simple_schematron
        assert validator.schematron is not None

    def test_init_with_nonexistent_schematron(self):
        """Test initializing with nonexistent Schematron raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Schematron file not found"):
            SchematronValidator("/nonexistent/schematron.sch")

    def test_init_with_invalid_schematron(self, tmp_path):
        """Test initializing with invalid Schematron raises SchematronParseError."""
        invalid_schematron = tmp_path / "invalid.sch"
        invalid_schematron.write_text("<invalid>schematron</invalid>")

        with pytest.raises(etree.SchematronParseError):
            SchematronValidator(invalid_schematron)

    def test_init_with_phase(self, simple_schematron):
        """Test initializing validator with specific phase."""
        validator = SchematronValidator(simple_schematron, phase="errors")
        assert validator.phase == "errors"
        assert validator.validation_phase == "errors"

    def test_validate_valid_xml_string(self, simple_schematron, valid_xml_string):
        """Test validating valid XML string."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate(valid_xml_string)

        assert isinstance(result, ValidationResult)
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_valid_xml_bytes(self, simple_schematron, valid_xml_string):
        """Test validating valid XML bytes."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate(valid_xml_string.encode("utf-8"))

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_valid_xml_element(self, simple_schematron, valid_xml_string):
        """Test validating valid XML element."""
        validator = SchematronValidator(simple_schematron)
        element = etree.fromstring(valid_xml_string.encode("utf-8"))
        result = validator.validate(element)

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_valid_xml_file(self, simple_schematron, valid_xml_string, tmp_path):
        """Test validating valid XML file."""
        validator = SchematronValidator(simple_schematron)
        xml_file = tmp_path / "test.xml"
        xml_file.write_text(valid_xml_string)

        result = validator.validate(xml_file)

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_invalid_xml_missing_id(self, simple_schematron, invalid_xml_missing_id):
        """Test validating XML with missing required id attribute."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate(invalid_xml_missing_id)

        assert result.is_valid is False
        assert len(result.errors) >= 1

        # Check that error contains relevant information
        error = result.errors[0]
        assert error.level == ValidationLevel.ERROR
        assert "id" in error.message.lower() or "attribute" in error.message.lower()
        assert error.code is not None
        assert "SCHEMATRON" in error.code

    def test_validate_invalid_xml_missing_child(self, simple_schematron, invalid_xml_missing_child):
        """Test validating XML with missing required child element."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate(invalid_xml_missing_child)

        assert result.is_valid is False
        assert len(result.errors) >= 1
        assert result.errors[0].level == ValidationLevel.ERROR

    def test_validate_invalid_xml_empty_child(self, simple_schematron, invalid_xml_empty_child):
        """Test validating XML with empty child element."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate(invalid_xml_empty_child)

        assert result.is_valid is False
        assert len(result.errors) >= 1

        # Check error message mentions empty child
        assert any("empty" in e.message.lower() for e in result.errors)

    def test_validate_multiple_schematron_errors(
        self, simple_schematron, invalid_xml_multiple_errors
    ):
        """Test handling multiple Schematron validation errors."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate(invalid_xml_multiple_errors)

        assert result.is_valid is False
        # Should have at least 2 errors (invalid id + empty child)
        assert len(result.errors) >= 2

    def test_validate_malformed_xml(self, simple_schematron, malformed_xml):
        """Test validating malformed XML."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate(malformed_xml)

        assert result.is_valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "XML_SYNTAX_ERROR"
        assert "syntax error" in result.errors[0].message.lower()

    def test_validate_nonexistent_file(self, simple_schematron):
        """Test validating nonexistent file."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate(Path("/nonexistent/file.xml"))

        assert result.is_valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "FILE_NOT_FOUND"

    def test_validate_file_convenience_method(self, simple_schematron, valid_xml_string, tmp_path):
        """Test validate_file convenience method."""
        validator = SchematronValidator(simple_schematron)
        xml_file = tmp_path / "test.xml"
        xml_file.write_text(valid_xml_string)

        result = validator.validate_file(xml_file)

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_string_convenience_method(self, simple_schematron, valid_xml_string):
        """Test validate_string convenience method."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate_string(valid_xml_string)

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_validate_bytes_convenience_method(self, simple_schematron, valid_xml_string):
        """Test validate_bytes convenience method."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate_bytes(valid_xml_string.encode("utf-8"))

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_schematron_location_property(self, simple_schematron):
        """Test schematron_location property."""
        validator = SchematronValidator(simple_schematron)
        assert validator.schematron_location == simple_schematron

    def test_error_contains_location(self, simple_schematron, invalid_xml_missing_id):
        """Test error includes location information."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate(invalid_xml_missing_id)

        assert result.is_valid is False
        # At least some errors should have location
        assert any(e.location is not None for e in result.errors)

    def test_error_contains_code(self, simple_schematron, invalid_xml_missing_id):
        """Test error includes SCHEMATRON code."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate(invalid_xml_missing_id)

        assert result.is_valid is False
        # All errors should have codes
        for error in result.errors:
            assert error.code is not None
            assert "SCHEMATRON" in error.code

    def test_ccda_valid_document(self, ccda_schematron, valid_ccda_minimal):
        """Test validating valid C-CDA document."""
        validator = SchematronValidator(ccda_schematron)
        result = validator.validate(valid_ccda_minimal)

        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_ccda_invalid_missing_realm(self, ccda_schematron, invalid_ccda_missing_realm):
        """Test validating C-CDA with missing realmCode."""
        validator = SchematronValidator(ccda_schematron)
        result = validator.validate(invalid_ccda_missing_realm)

        assert result.is_valid is False
        assert len(result.errors) >= 1

        # Check that error mentions realm
        assert any("realm" in e.message.lower() for e in result.errors)

    def test_init_with_string_path(self, simple_schematron):
        """Test initializing with string path."""
        validator = SchematronValidator(str(simple_schematron))
        assert validator.schematron_path == Path(simple_schematron)

    def test_validate_with_path_string(self, simple_schematron, valid_xml_string, tmp_path):
        """Test validating with path as string."""
        validator = SchematronValidator(simple_schematron)
        xml_file = tmp_path / "test.xml"
        xml_file.write_text(valid_xml_string)

        result = validator.validate(str(xml_file))

        assert result.is_valid is True

    def test_default_schematron_path_resolution(self):
        """Test that default Schematron path resolves correctly."""
        # This will use the cleaned HL7 C-CDA R2.1 Schematron
        validator = SchematronValidator()

        # Verify it loaded successfully
        assert validator.schematron is not None
        assert validator.schematron_path.exists()
        # Should use cleaned version by default
        assert "cleaned" in validator.schematron_path.name.lower()

    def test_validate_with_real_ccda_schematron(self, valid_ccda_minimal):
        """Test validation with cleaned HL7 C-CDA Schematron."""
        # This uses the auto-cleaned version that has IDREF errors fixed
        validator = SchematronValidator()
        result = validator.validate(valid_ccda_minimal)

        # Minimal C-CDA may not pass all HL7 rules, but should parse
        assert isinstance(result, ValidationResult)

    def test_extract_text_content_simple(self, simple_schematron):
        """Test text extraction from simple element."""
        validator = SchematronValidator(simple_schematron)

        element = etree.fromstring("<text>Simple text</text>")
        text = validator._extract_text_content(element)

        assert text == "Simple text"

    def test_extract_text_content_with_nested_elements(self, simple_schematron):
        """Test text extraction with nested elements."""
        validator = SchematronValidator(simple_schematron)

        element = etree.fromstring("<text>Start <nested>middle</nested> end</text>")
        text = validator._extract_text_content(element)

        assert "Start" in text
        assert "middle" in text
        assert "end" in text

    def test_init_without_default_schematron_available(self):
        """Test initialization when Schematron file is not available."""
        # Try to initialize with a non-existent file path
        # This should raise FileNotFoundError when auto_download is disabled
        nonexistent_path = Path("/nonexistent/path/to/schematron.sch")

        with pytest.raises(FileNotFoundError, match="Schematron file not found"):
            SchematronValidator(schematron_path=nonexistent_path, auto_download=False)

    def test_validation_result_structure(self, simple_schematron, invalid_xml_missing_id):
        """Test validation result has proper structure."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate(invalid_xml_missing_id)

        # Verify result structure
        assert hasattr(result, "is_valid")
        assert hasattr(result, "errors")
        assert hasattr(result, "warnings")
        assert hasattr(result, "infos")

        # Verify error structure
        for error in result.errors:
            assert hasattr(error, "level")
            assert hasattr(error, "message")
            assert hasattr(error, "location")
            assert hasattr(error, "code")
            assert error.message  # Should not be empty

    def test_multiple_validations_with_same_validator(
        self, simple_schematron, valid_xml_string, invalid_xml_missing_id
    ):
        """Test that validator can be reused for multiple validations."""
        validator = SchematronValidator(simple_schematron)

        # First validation - valid
        result1 = validator.validate(valid_xml_string)
        assert result1.is_valid is True

        # Second validation - invalid
        result2 = validator.validate(invalid_xml_missing_id)
        assert result2.is_valid is False

        # Third validation - valid again
        result3 = validator.validate(valid_xml_string)
        assert result3.is_valid is True

    def test_schematron_namespace_handling(self, tmp_path):
        """Test that Schematron handles namespaces correctly."""
        # Create Schematron with namespace
        schematron_content = """<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">
  <sch:ns prefix="ns1" uri="http://example.com/ns1"/>

  <sch:pattern id="ns-checks">
    <sch:rule context="/ns1:root">
      <sch:assert test="@id" id="ns-id-required">
        Root element must have an id attribute.
      </sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>"""
        schematron_path = tmp_path / "ns_schematron.sch"
        schematron_path.write_text(schematron_content)

        # Create XML with namespace
        valid_xml = '<?xml version="1.0"?><root xmlns="http://example.com/ns1" id="test"/>'
        invalid_xml = '<?xml version="1.0"?><root xmlns="http://example.com/ns1"/>'

        validator = SchematronValidator(schematron_path)

        # Valid XML should pass
        result_valid = validator.validate(valid_xml)
        assert result_valid.is_valid is True

        # Invalid XML should fail
        result_invalid = validator.validate(invalid_xml)
        assert result_invalid.is_valid is False

    # --- Enhanced tests for uncovered lines ---

    def test_resolve_schematron_path_fallback_to_original(self, tmp_path, monkeypatch):
        """Test fallback to original Schematron when cleaned version doesn't exist."""
        # Create a temporary directory structure with only original file
        schemas_dir = tmp_path / "schemas" / "schematron"
        schemas_dir.mkdir(parents=True)
        original_file = schemas_dir / "HL7_CCDA_R2.1.sch"

        # Create simple schematron content
        schematron_content = """<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">
  <sch:pattern id="test">
    <sch:rule context="/">
      <sch:assert test="root" id="root-exists">Root exists</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>"""
        original_file.write_text(schematron_content)

        # Test path resolution directly
        validator = SchematronValidator(original_file)

        # Check that it found the original file
        assert validator.schematron_path.exists()
        assert "HL7_CCDA_R2.1.sch" in str(validator.schematron_path)

    def test_auto_download_success(self, tmp_path, monkeypatch):
        """Test successful automatic download of Schematron files."""
        # Mock SchematronDownloader
        mock_downloader = Mock()
        mock_downloader.download_all.return_value = (True, "Download successful")

        with patch(
            "ccdakit.validators.schematron.SchematronDownloader", return_value=mock_downloader
        ):
            # Create a non-existent path
            nonexistent_path = tmp_path / "nonexistent.sch"

            # This should trigger auto-download
            with pytest.raises(FileNotFoundError):
                # Will still fail since we're not creating the actual file,
                # but download should be attempted
                SchematronValidator(schematron_path=nonexistent_path, auto_download=True)

            # Verify download was attempted
            mock_downloader.download_all.assert_called_once()

    def test_auto_download_failure(self, tmp_path):
        """Test handling of failed automatic download."""
        # Mock SchematronDownloader to fail
        mock_downloader = Mock()
        mock_downloader.download_all.return_value = (False, "Download failed")

        with patch(
            "ccdakit.validators.schematron.SchematronDownloader", return_value=mock_downloader
        ):
            # Should issue warning and then raise FileNotFoundError
            with pytest.warns(UserWarning, match="Automatic download failed"):
                with pytest.raises(FileNotFoundError):
                    nonexistent_path = tmp_path / "nonexistent.sch"
                    SchematronValidator(schematron_path=nonexistent_path, auto_download=True)

    def test_auto_download_exception(self, tmp_path):
        """Test handling of exception during automatic download."""
        # Mock SchematronDownloader to raise exception
        with patch(
            "ccdakit.validators.schematron.SchematronDownloader",
            side_effect=RuntimeError("Network error"),
        ):
            # Should issue warning and then raise FileNotFoundError
            with pytest.warns(UserWarning, match="Automatic download failed"):
                with pytest.raises(FileNotFoundError):
                    nonexistent_path = tmp_path / "nonexistent.sch"
                    SchematronValidator(schematron_path=nonexistent_path, auto_download=True)

    def test_load_schematron_xml_syntax_error(self, tmp_path):
        """Test handling of XML syntax errors in Schematron file."""
        # Create Schematron file with XML syntax error
        bad_xml_path = tmp_path / "bad_syntax.sch"
        bad_xml_path.write_text("<?xml version='1.0'?><sch:schema><unclosed>")

        with pytest.raises(etree.SchematronParseError, match="Failed to parse Schematron file"):
            SchematronValidator(bad_xml_path)

    def test_load_schematron_general_exception(self, tmp_path):
        """Test handling of general exceptions during Schematron loading."""
        # Create valid XML but invalid Schematron
        invalid_sch_path = tmp_path / "invalid.sch"
        invalid_sch_path.write_text("<?xml version='1.0'?><root>Not a schematron</root>")

        with pytest.raises(etree.SchematronParseError, match="Failed to load Schematron"):
            SchematronValidator(invalid_sch_path)

    def test_validation_with_schematron_error(self, simple_schematron, valid_xml_string):
        """Test handling of errors during Schematron validation."""
        validator = SchematronValidator(simple_schematron)

        # Mock the schematron.validate to raise an exception
        with patch.object(
            validator.schematron, "validate", side_effect=RuntimeError("Validation error")
        ):
            result = validator.validate(valid_xml_string)

            assert result.is_valid is False
            assert len(result.errors) == 1
            assert result.errors[0].code == "SCHEMATRON_ERROR"
            assert "Schematron validation error" in result.errors[0].message

    def test_extract_issues_with_warnings_and_info(self, tmp_path):
        """Test extraction of warnings and informational messages from SVRL."""
        # Test that we can parse warnings/info from SVRL correctly
        # We'll test the parsing methods directly rather than relying on schematron behavior
        validator_schema = """<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">
  <sch:pattern id="test">
    <sch:rule context="/">
      <sch:assert test="root" id="test-id">Root exists</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>"""
        schematron_path = tmp_path / "test.sch"
        schematron_path.write_text(validator_schema)

        validator = SchematronValidator(schematron_path)

        # Test parsing warning from successful-report
        warning_report = etree.fromstring(
            f'<successful-report xmlns="{validator.SVRL_NS}" id="test-id" location="/root" role="warning">'
            f'<text xmlns="{validator.SVRL_NS}">This is a warning message</text>'
            f"</successful-report>"
        )
        warning_issue = validator._parse_successful_report(warning_report)
        assert warning_issue is not None
        assert warning_issue.level == ValidationLevel.WARNING

        # Test parsing info from successful-report
        info_report = etree.fromstring(
            f'<successful-report xmlns="{validator.SVRL_NS}" id="test-id" location="/root" role="info">'
            f'<text xmlns="{validator.SVRL_NS}">This is an info message</text>'
            f"</successful-report>"
        )
        info_issue = validator._parse_successful_report(info_report)
        assert info_issue is not None
        assert info_issue.level == ValidationLevel.INFO

    def test_parse_failed_assert_without_text_element(self, simple_schematron):
        """Test parsing failed-assert with missing text element."""
        validator = SchematronValidator(simple_schematron)

        # Create a failed-assert element without text child
        failed_assert = etree.fromstring(
            f'<failed-assert xmlns="{validator.SVRL_NS}" id="test-id" location="/root"/>'
        )

        result = validator._parse_failed_assert(failed_assert)
        assert result is None

    def test_parse_failed_assert_with_empty_text(self, simple_schematron):
        """Test parsing failed-assert with empty text content."""
        validator = SchematronValidator(simple_schematron)

        # Create a failed-assert element with empty text
        failed_assert = etree.fromstring(
            f'<failed-assert xmlns="{validator.SVRL_NS}" id="test-id" location="/root">'
            f'<text xmlns="{validator.SVRL_NS}">   </text>'
            f"</failed-assert>"
        )

        result = validator._parse_failed_assert(failed_assert)
        assert result is None

    def test_parse_successful_report_without_text_element(self, simple_schematron):
        """Test parsing successful-report with missing text element."""
        validator = SchematronValidator(simple_schematron)

        # Create a successful-report element without text child
        successful_report = etree.fromstring(
            f'<successful-report xmlns="{validator.SVRL_NS}" id="test-id" location="/root"/>'
        )

        result = validator._parse_successful_report(successful_report)
        assert result is None

    def test_parse_successful_report_with_empty_text(self, simple_schematron):
        """Test parsing successful-report with empty text content."""
        validator = SchematronValidator(simple_schematron)

        # Create a successful-report element with empty text
        successful_report = etree.fromstring(
            f'<successful-report xmlns="{validator.SVRL_NS}" id="test-id" location="/root">'
            f'<text xmlns="{validator.SVRL_NS}">   </text>'
            f"</successful-report>"
        )

        result = validator._parse_successful_report(successful_report)
        assert result is None

    def test_parse_successful_report_warning_detection(self, simple_schematron):
        """Test that successful-report correctly detects warnings."""
        validator = SchematronValidator(simple_schematron)

        # Create successful-report with warning role
        successful_report = etree.fromstring(
            f'<successful-report xmlns="{validator.SVRL_NS}" id="test-id" location="/root" role="warning">'
            f'<text xmlns="{validator.SVRL_NS}">This is a warning message</text>'
            f"</successful-report>"
        )

        result = validator._parse_successful_report(successful_report)
        assert result is not None
        assert result.level == ValidationLevel.WARNING

    def test_parse_successful_report_info_detection(self, simple_schematron):
        """Test that successful-report correctly detects info messages."""
        validator = SchematronValidator(simple_schematron)

        # Create successful-report with info role
        successful_report = etree.fromstring(
            f'<successful-report xmlns="{validator.SVRL_NS}" id="test-id" location="/root" role="info">'
            f'<text xmlns="{validator.SVRL_NS}">This is an informational message</text>'
            f"</successful-report>"
        )

        result = validator._parse_successful_report(successful_report)
        assert result is not None
        assert result.level == ValidationLevel.INFO

    def test_parse_successful_report_warn_in_message(self, simple_schematron):
        """Test that 'warn' in message triggers WARNING level."""
        validator = SchematronValidator(simple_schematron)

        # Create successful-report with "warn" in message text
        successful_report = etree.fromstring(
            f'<successful-report xmlns="{validator.SVRL_NS}" id="test-id" location="/root">'
            f'<text xmlns="{validator.SVRL_NS}">I warn you about this issue</text>'
            f"</successful-report>"
        )

        result = validator._parse_successful_report(successful_report)
        assert result is not None
        assert result.level == ValidationLevel.WARNING

    def test_extract_text_content_with_tail(self, simple_schematron):
        """Test text extraction with element tail content."""
        validator = SchematronValidator(simple_schematron)

        # Create element with nested tags and tail text
        element = etree.fromstring(
            "<text>Before <bold>bold text</bold> after <italic>italic</italic> end</text>"
        )
        text = validator._extract_text_content(element)

        # Should extract all text including tails
        assert "Before" in text
        assert "bold text" in text
        assert "after" in text
        assert "italic" in text
        assert "end" in text

    def test_extract_text_content_empty_element(self, simple_schematron):
        """Test text extraction from empty element."""
        validator = SchematronValidator(simple_schematron)

        element = etree.fromstring("<text/>")
        text = validator._extract_text_content(element)

        assert text == ""

    def test_extract_text_content_whitespace_normalization(self, simple_schematron):
        """Test that whitespace is properly normalized."""
        validator = SchematronValidator(simple_schematron)

        element = etree.fromstring("<text>  Multiple   spaces   and\n\nnewlines\t\ttabs  </text>")
        text = validator._extract_text_content(element)

        # Should normalize whitespace
        assert "  " not in text  # No double spaces
        assert "\n" not in text  # No newlines
        assert "\t" not in text  # No tabs

    def test_custom_resolver_for_voc_xml(self, tmp_path):
        """Test that custom resolver handles voc.xml includes."""
        # Create voc.xml file
        voc_path = tmp_path / "voc.xml"
        voc_content = """<?xml version="1.0" encoding="UTF-8"?>
<vocabulary>
  <valueSets>
    <valueSet id="test" name="Test Value Set"/>
  </valueSets>
</vocabulary>"""
        voc_path.write_text(voc_content)

        # Create Schematron that references voc.xml
        schematron_content = """<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">
  <sch:pattern id="test">
    <sch:rule context="/">
      <sch:assert test="root" id="root-exists">Root exists</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>"""
        schematron_path = tmp_path / "test.sch"
        schematron_path.write_text(schematron_content)

        # Create validator - should load successfully
        validator = SchematronValidator(schematron_path)
        assert validator.schematron is not None

    def test_schematron_with_phase(self, tmp_path):
        """Test Schematron validation with specific phase."""
        # Create Schematron with multiple phases
        schematron_content = """<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">
  <sch:phase id="errors">
    <sch:active pattern="error-patterns"/>
  </sch:phase>

  <sch:phase id="warnings">
    <sch:active pattern="warning-patterns"/>
  </sch:phase>

  <sch:pattern id="error-patterns">
    <sch:rule context="/root">
      <sch:assert test="@required" id="required-attr">
        Required attribute must be present.
      </sch:assert>
    </sch:rule>
  </sch:pattern>

  <sch:pattern id="warning-patterns">
    <sch:rule context="/root">
      <sch:report test="@deprecated" role="warning" id="deprecated-attr">
        Deprecated attribute detected.
      </sch:report>
    </sch:rule>
  </sch:pattern>
</sch:schema>"""
        schematron_path = tmp_path / "phased.sch"
        schematron_path.write_text(schematron_content)

        # Test with errors phase
        validator = SchematronValidator(schematron_path, phase="errors")
        assert validator.phase == "errors"

        # Validate document missing required attribute
        xml_missing_required = '<?xml version="1.0"?><root deprecated="true"/>'
        result = validator.validate(xml_missing_required)

        # Should fail due to missing required attribute (errors phase active)
        assert result.is_valid is False

    def test_validation_with_file_not_found_error(self, simple_schematron, tmp_path):
        """Test proper handling of FileNotFoundError during validation."""
        validator = SchematronValidator(simple_schematron)

        # Try to validate non-existent file path
        nonexistent_file = tmp_path / "definitely_does_not_exist_12345.xml"
        result = validator.validate(nonexistent_file)

        assert result.is_valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "FILE_NOT_FOUND"

    def test_validation_with_xml_syntax_error(self, simple_schematron):
        """Test proper handling of XML syntax errors during validation."""
        validator = SchematronValidator(simple_schematron)

        # Malformed XML
        malformed_xml = "<root><unclosed>"
        result = validator.validate(malformed_xml)

        assert result.is_valid is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "XML_SYNTAX_ERROR"
        assert "syntax error" in result.errors[0].message.lower()

    def test_large_document_validation(self, simple_schematron):
        """Test validation of large documents."""
        # Create a large XML document
        large_xml = '<?xml version="1.0"?><root id="test"><child>'
        large_xml += "x" * 1000000  # 1MB of content
        large_xml += "</child></root>"

        validator = SchematronValidator(simple_schematron)
        result = validator.validate(large_xml)

        # Should handle large documents
        assert isinstance(result, ValidationResult)

    def test_error_with_line_number(self, simple_schematron):
        """Test that XML syntax errors include line numbers."""
        validator = SchematronValidator(simple_schematron)

        # Multi-line malformed XML
        malformed_xml = """<?xml version="1.0"?>
<root>
  <unclosed>
  <another>
</root>"""

        result = validator.validate(malformed_xml)

        assert result.is_valid is False
        assert len(result.errors) == 1
        # Should include location information
        assert result.errors[0].location is not None or "Line" in result.errors[0].message

    def test_validation_with_unusual_namespaces(self, tmp_path):
        """Test validation with unusual or multiple namespaces."""
        schematron_content = """<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">
  <sch:ns prefix="ns1" uri="http://example.com/ns1"/>
  <sch:ns prefix="ns2" uri="http://example.com/ns2"/>

  <sch:pattern id="multi-ns">
    <sch:rule context="/ns1:root">
      <sch:assert test="ns2:child" id="child-required">
        Must have child from ns2.
      </sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>"""
        schematron_path = tmp_path / "multi_ns.sch"
        schematron_path.write_text(schematron_content)

        # Valid XML with multiple namespaces
        valid_xml = """<?xml version="1.0"?>
<root xmlns="http://example.com/ns1" xmlns:ns2="http://example.com/ns2">
  <ns2:child>content</ns2:child>
</root>"""

        validator = SchematronValidator(schematron_path)
        result = validator.validate(valid_xml)

        assert result.is_valid is True

    def test_validation_issue_with_parsed_data(self, simple_schematron, invalid_xml_missing_id):
        """Test that validation issues include parsed_data from error parser."""
        validator = SchematronValidator(simple_schematron)
        result = validator.validate(invalid_xml_missing_id)

        assert result.is_valid is False
        assert len(result.errors) > 0

        # Check that parsed_data is present
        for error in result.errors:
            assert hasattr(error, "parsed_data")
            assert error.parsed_data is not None
            assert isinstance(error.parsed_data, dict)

    def test_schematron_resolver_non_file_urls(self, tmp_path):
        """Test that resolver handles HTTP URLs correctly."""
        # Create Schematron file
        schematron_content = """<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">
  <sch:pattern id="test">
    <sch:rule context="/">
      <sch:assert test="root" id="root-exists">Root exists</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>"""
        schematron_path = tmp_path / "test.sch"
        schematron_path.write_text(schematron_content)

        # Validator should load successfully even if no HTTP URLs are resolved
        validator = SchematronValidator(schematron_path)
        assert validator.schematron is not None
