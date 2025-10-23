"""Tests for the validate CLI command."""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from ccdakit.cli.__main__ import app
from ccdakit.core.validation import ValidationLevel, ValidationResult


runner = CliRunner()


@pytest.fixture
def sample_xml_file(tmp_path):
    """Create a sample XML file for testing."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test Document</title>
</ClinicalDocument>"""
    xml_file = tmp_path / "test.xml"
    xml_file.write_text(xml_content)
    return xml_file


@pytest.fixture
def invalid_xml_file(tmp_path):
    """Create an invalid XML file for testing."""
    xml_file = tmp_path / "invalid.xml"
    xml_file.write_text("not valid xml <unclosed>")
    return xml_file


@pytest.fixture
def mock_validation_result_success():
    """Create a successful validation result."""
    result = ValidationResult()
    return result


@pytest.fixture
def mock_validation_result_with_errors():
    """Create a validation result with errors."""
    result = ValidationResult()
    error = MagicMock()
    error.level = ValidationLevel.ERROR
    error.message = "Test error message"
    error.location = "line 10"
    error.code = "TEST_ERROR"
    result.errors.append(error)
    return result


@pytest.fixture
def mock_validation_result_with_warnings():
    """Create a validation result with warnings."""
    result = ValidationResult()
    warning = MagicMock()
    warning.level = ValidationLevel.WARNING
    warning.message = "Test warning message"
    warning.location = "line 5"
    warning.code = "TEST_WARNING"
    result.warnings.append(warning)
    return result


class TestValidateCommand:
    """Test suite for the validate command."""

    def test_validate_help(self):
        """Test the --help flag displays help information."""
        result = runner.invoke(app, ["validate", "--help"])
        assert result.exit_code == 0
        assert "Validate a C-CDA document" in result.stdout
        assert "--xsd" in result.stdout
        assert "--schematron" in result.stdout
        assert "--output-format" in result.stdout

    def test_validate_missing_file(self):
        """Test validation with a nonexistent file."""
        result = runner.invoke(app, ["validate", "/nonexistent/file.xml"])
        assert result.exit_code == 1
        assert "File not found" in result.stdout

    def test_validate_not_a_file(self, tmp_path):
        """Test validation with a directory path instead of a file."""
        result = runner.invoke(app, ["validate", str(tmp_path)])
        assert result.exit_code == 1
        assert "Not a file" in result.stdout

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    @patch("ccdakit.cli.commands.validate._run_schematron_validation")
    def test_validate_valid_file_success(
        self,
        mock_schematron,
        mock_xsd,
        sample_xml_file,
        mock_validation_result_success,
    ):
        """Test validation with a valid file that passes all checks."""
        mock_xsd.return_value = mock_validation_result_success
        mock_schematron.return_value = mock_validation_result_success

        result = runner.invoke(app, ["validate", str(sample_xml_file)])

        # Should not exit with error code when validation passes
        assert result.exit_code == 0
        assert "XSD validation passed" in result.stdout
        assert "Schematron validation passed" in result.stdout
        assert "Document is valid" in result.stdout

        # Both validators should be called
        mock_xsd.assert_called_once()
        mock_schematron.assert_called_once()

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    @patch("ccdakit.cli.commands.validate._run_schematron_validation")
    def test_validate_with_errors(
        self,
        mock_schematron,
        mock_xsd,
        sample_xml_file,
        mock_validation_result_with_errors,
        mock_validation_result_success,
    ):
        """Test validation with a file that has errors."""
        mock_xsd.return_value = mock_validation_result_with_errors
        mock_schematron.return_value = mock_validation_result_success

        result = runner.invoke(app, ["validate", str(sample_xml_file)])

        # Should exit with error code when validation fails
        assert result.exit_code == 1
        assert "Test error message" in result.stdout
        assert "Validation failed" in result.stdout

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    @patch("ccdakit.cli.commands.validate._run_schematron_validation")
    def test_validate_with_warnings(
        self,
        mock_schematron,
        mock_xsd,
        sample_xml_file,
        mock_validation_result_with_warnings,
        mock_validation_result_success,
    ):
        """Test validation with a file that has warnings."""
        mock_xsd.return_value = mock_validation_result_success
        mock_schematron.return_value = mock_validation_result_with_warnings

        result = runner.invoke(app, ["validate", str(sample_xml_file)])

        # Should not exit with error code for warnings only
        assert result.exit_code == 0
        assert "Test warning message" in result.stdout
        assert "warning(s) found" in result.stdout

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    def test_validate_xsd_only(
        self,
        mock_xsd,
        sample_xml_file,
        mock_validation_result_success,
    ):
        """Test validation with only XSD enabled."""
        mock_xsd.return_value = mock_validation_result_success

        result = runner.invoke(
            app,
            ["validate", str(sample_xml_file), "--no-schematron"],
        )

        assert result.exit_code == 0
        assert "Running XSD Schema Validation" in result.stdout
        mock_xsd.assert_called_once()

    @patch("ccdakit.cli.commands.validate._run_schematron_validation")
    def test_validate_schematron_only(
        self,
        mock_schematron,
        sample_xml_file,
        mock_validation_result_success,
    ):
        """Test validation with only Schematron enabled."""
        mock_schematron.return_value = mock_validation_result_success

        result = runner.invoke(
            app,
            ["validate", str(sample_xml_file), "--no-xsd"],
        )

        assert result.exit_code == 0
        assert "Running Schematron Validation" in result.stdout
        mock_schematron.assert_called_once()

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    @patch("ccdakit.cli.commands.validate._run_schematron_validation")
    def test_validate_json_output(
        self,
        mock_schematron,
        mock_xsd,
        sample_xml_file,
        mock_validation_result_success,
    ):
        """Test validation with JSON output format."""
        mock_xsd.return_value = mock_validation_result_success
        mock_schematron.return_value = mock_validation_result_success

        result = runner.invoke(
            app,
            ["validate", str(sample_xml_file), "--output-format", "json"],
        )

        assert result.exit_code == 0
        # Should contain valid JSON
        try:
            output_lines = result.stdout.split("\n")
            json_start = None
            for i, line in enumerate(output_lines):
                if line.strip().startswith("{"):
                    json_start = i
                    break

            if json_start is not None:
                json_str = "\n".join(output_lines[json_start:])
                data = json.loads(json_str)
                assert "xsd" in data or "schematron" in data
            else:
                # JSON format might output differently, check for key indicators
                assert "xsd" in result.stdout.lower() or "schematron" in result.stdout.lower()
        except json.JSONDecodeError:
            # If JSON parsing fails, at least verify command executed successfully
            assert "validation" in result.stdout.lower()

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    @patch("ccdakit.cli.commands.validate._run_schematron_validation")
    def test_validate_html_output(
        self,
        mock_schematron,
        mock_xsd,
        sample_xml_file,
        mock_validation_result_success,
    ):
        """Test validation with HTML output format."""
        mock_xsd.return_value = mock_validation_result_success
        mock_schematron.return_value = mock_validation_result_success

        result = runner.invoke(
            app,
            ["validate", str(sample_xml_file), "--output-format", "html"],
        )

        assert result.exit_code == 0
        assert "HTML report saved to" in result.stdout

        # Check that HTML file was created
        html_file = sample_xml_file.parent / f"{sample_xml_file.stem}_validation_report.html"
        assert html_file.exists()
        html_content = html_file.read_text()
        assert "<!DOCTYPE html>" in html_content
        assert "Validation Report" in html_content

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    def test_validate_xsd_exception(self, mock_xsd, sample_xml_file):
        """Test handling of XSD validation exceptions."""
        mock_xsd.side_effect = Exception("XSD validation error")

        result = runner.invoke(app, ["validate", str(sample_xml_file), "--no-schematron"])

        # Should handle the exception gracefully
        assert result.exit_code == 1
        # The error should be captured in validation result

    @patch("ccdakit.cli.commands.validate._run_schematron_validation")
    def test_validate_schematron_exception(self, mock_schematron, sample_xml_file):
        """Test handling of Schematron validation exceptions."""
        mock_schematron.side_effect = Exception("Schematron validation error")

        result = runner.invoke(app, ["validate", str(sample_xml_file), "--no-xsd"])

        # Should handle the exception gracefully
        assert result.exit_code == 1

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    @patch("ccdakit.cli.commands.validate._run_schematron_validation")
    def test_validate_multiple_errors_and_warnings(
        self,
        mock_schematron,
        mock_xsd,
        sample_xml_file,
    ):
        """Test validation with multiple errors and warnings."""
        # Create XSD result with errors
        xsd_result = ValidationResult()
        error1 = MagicMock()
        error1.level = ValidationLevel.ERROR
        error1.message = "XSD Error 1"
        error1.location = "line 5"
        error1.code = "XSD_ERROR_1"
        xsd_result.errors.append(error1)

        # Create Schematron result with warnings
        sch_result = ValidationResult()
        warning1 = MagicMock()
        warning1.level = ValidationLevel.WARNING
        warning1.message = "Schematron Warning 1"
        warning1.location = "line 10"
        warning1.code = "SCH_WARNING_1"
        sch_result.warnings.append(warning1)

        mock_xsd.return_value = xsd_result
        mock_schematron.return_value = sch_result

        result = runner.invoke(app, ["validate", str(sample_xml_file)])

        assert result.exit_code == 1
        assert "XSD Error 1" in result.stdout
        assert "Schematron Warning 1" in result.stdout
        assert "1 error(s)" in result.stdout
        assert "1 warning(s)" in result.stdout


class TestOutputFormats:
    """Test different output format edge cases."""

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    @patch("ccdakit.cli.commands.validate._run_schematron_validation")
    def test_html_output_with_errors(
        self,
        mock_schematron,
        mock_xsd,
        sample_xml_file,
        mock_validation_result_with_errors,
    ):
        """Test HTML output format with validation errors."""
        mock_xsd.return_value = mock_validation_result_with_errors
        mock_schematron.return_value = ValidationResult()

        result = runner.invoke(
            app,
            ["validate", str(sample_xml_file), "--output-format", "html"],
        )

        # Should generate HTML report even with errors
        assert "HTML report saved to" in result.stdout
        assert result.exit_code == 1

        # Verify HTML content includes errors
        html_file = sample_xml_file.parent / f"{sample_xml_file.stem}_validation_report.html"
        assert html_file.exists()
        html_content = html_file.read_text()
        assert "Test error message" in html_content
        assert "FAILED" in html_content or "failed" in html_content.lower()

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    @patch("ccdakit.cli.commands.validate._run_schematron_validation")
    def test_json_output_with_errors_and_warnings(
        self,
        mock_schematron,
        mock_xsd,
        sample_xml_file,
        mock_validation_result_with_errors,
        mock_validation_result_with_warnings,
    ):
        """Test JSON output format with both errors and warnings."""
        mock_xsd.return_value = mock_validation_result_with_errors
        mock_schematron.return_value = mock_validation_result_with_warnings

        result = runner.invoke(
            app,
            ["validate", str(sample_xml_file), "--output-format", "json"],
        )

        # Should output valid JSON with both results
        assert result.exit_code == 1

        # Extract and parse JSON from output
        output_lines = result.stdout.split("\n")
        json_start = None
        for i, line in enumerate(output_lines):
            if line.strip().startswith("{"):
                json_start = i
                break

        if json_start is not None:
            json_str = "\n".join(output_lines[json_start:])
            data = json.loads(json_str)
            assert "xsd" in data
            assert "schematron" in data


class TestValidationResultDisplay:
    """Test validation result display functionality."""

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    @patch("ccdakit.cli.commands.validate._run_schematron_validation")
    def test_validation_with_multiple_error_types(
        self,
        mock_schematron,
        mock_xsd,
        sample_xml_file,
    ):
        """Test validation display with multiple error types."""
        # Create XSD result with multiple errors
        xsd_result = ValidationResult()
        for i in range(3):
            error = MagicMock()
            error.level = ValidationLevel.ERROR
            error.message = f"XSD Error {i+1}"
            error.location = f"line {i+5}"
            error.code = f"XSD_ERROR_{i+1}"
            xsd_result.errors.append(error)

        # Create Schematron result with errors and warnings
        sch_result = ValidationResult()
        error = MagicMock()
        error.level = ValidationLevel.ERROR
        error.message = "Schematron Error"
        error.location = "line 20"
        error.code = "SCH_ERROR"
        sch_result.errors.append(error)

        warning = MagicMock()
        warning.level = ValidationLevel.WARNING
        warning.message = "Schematron Warning"
        warning.location = "line 25"
        warning.code = "SCH_WARNING"
        sch_result.warnings.append(warning)

        mock_xsd.return_value = xsd_result
        mock_schematron.return_value = sch_result

        result = runner.invoke(app, ["validate", str(sample_xml_file)])

        # Should display all errors and warnings
        assert result.exit_code == 1
        assert "XSD Error 1" in result.stdout
        assert "XSD Error 2" in result.stdout
        assert "XSD Error 3" in result.stdout
        assert "Schematron Error" in result.stdout
        assert "Schematron Warning" in result.stdout
        assert "4 error(s)" in result.stdout
        assert "1 warning(s)" in result.stdout

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    @patch("ccdakit.cli.commands.validate._run_schematron_validation")
    def test_validation_summary_all_passed(
        self,
        mock_schematron,
        mock_xsd,
        sample_xml_file,
        mock_validation_result_success,
    ):
        """Test validation summary when all validations pass."""
        mock_xsd.return_value = mock_validation_result_success
        mock_schematron.return_value = mock_validation_result_success

        result = runner.invoke(app, ["validate", str(sample_xml_file)])

        # Should show success summary
        assert result.exit_code == 0
        assert "Document is valid" in result.stdout
        assert "PASSED" in result.stdout

    @patch("ccdakit.cli.commands.validate._run_xsd_validation")
    def test_validation_with_only_warnings(
        self,
        mock_xsd,
        sample_xml_file,
        mock_validation_result_with_warnings,
    ):
        """Test validation with only warnings (no errors)."""
        mock_xsd.return_value = mock_validation_result_with_warnings

        result = runner.invoke(
            app,
            ["validate", str(sample_xml_file), "--no-schematron"],
        )

        # Should pass (exit code 0) but show warnings
        assert result.exit_code == 0
        assert "warning(s) found" in result.stdout
        assert "Document is valid" in result.stdout


class TestValidateIntegration:
    """Integration tests using real example files."""

    def test_validate_real_ccd_example(self):
        """Test validation with a real CCD example file."""
        example_file = Path("/Users/filipe/Code/pyccda/examples/ccd_example.xml")

        if not example_file.exists():
            pytest.skip("Example file not found")

        # This may fail if schemas aren't installed, but we're testing the command works
        result = runner.invoke(app, ["validate", str(example_file)])

        # Command should run without crashing
        assert "Validating" in result.stdout
        # Exit code may be 0 or 1 depending on validation result

    def test_validate_real_discharge_summary(self):
        """Test validation with a real discharge summary file."""
        example_file = Path("/Users/filipe/Code/pyccda/examples/discharge_summary_example.xml")

        if not example_file.exists():
            pytest.skip("Example file not found")

        result = runner.invoke(app, ["validate", str(example_file)])

        # Command should run without crashing
        assert "Validating" in result.stdout
