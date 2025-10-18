"""Tests for validation infrastructure."""

import pytest

from ccdakit.core.validation import (
    ValidationError,
    ValidationIssue,
    ValidationLevel,
    ValidationResult,
)


def test_validation_issue_creation():
    """Test creating a validation issue."""
    issue = ValidationIssue(
        level=ValidationLevel.ERROR,
        message="Test error",
        location="/ClinicalDocument/component",
        code="ERR001",
    )

    assert issue.level == ValidationLevel.ERROR
    assert issue.message == "Test error"
    assert issue.location == "/ClinicalDocument/component"
    assert issue.code == "ERR001"


def test_validation_issue_str():
    """Test string representation of validation issue."""
    issue = ValidationIssue(
        level=ValidationLevel.ERROR,
        message="Test error",
        location="/path/to/element",
        code="ERR001",
    )

    str_repr = str(issue)
    assert "ERROR" in str_repr
    assert "Test error" in str_repr
    assert "/path/to/element" in str_repr
    assert "[ERR001]" in str_repr


def test_validation_issue_str_no_location():
    """Test string representation without location."""
    issue = ValidationIssue(level=ValidationLevel.WARNING, message="Test warning")

    str_repr = str(issue)
    assert "WARNING" in str_repr
    assert "Test warning" in str_repr


def test_validation_result_empty():
    """Test empty validation result."""
    result = ValidationResult()

    assert result.is_valid
    assert not result.has_warnings
    assert len(result.all_issues) == 0


def test_validation_result_with_errors():
    """Test validation result with errors."""
    error = ValidationIssue(level=ValidationLevel.ERROR, message="Error 1")
    result = ValidationResult(errors=[error])

    assert not result.is_valid
    assert len(result.errors) == 1
    assert len(result.all_issues) == 1


def test_validation_result_with_warnings():
    """Test validation result with warnings."""
    warning = ValidationIssue(level=ValidationLevel.WARNING, message="Warning 1")
    result = ValidationResult(warnings=[warning])

    assert result.is_valid  # Warnings don't fail validation
    assert result.has_warnings
    assert len(result.warnings) == 1


def test_validation_result_with_mixed_issues():
    """Test validation result with errors, warnings, and info."""
    error = ValidationIssue(level=ValidationLevel.ERROR, message="Error")
    warning = ValidationIssue(level=ValidationLevel.WARNING, message="Warning")
    info = ValidationIssue(level=ValidationLevel.INFO, message="Info")

    result = ValidationResult(errors=[error], warnings=[warning], infos=[info])

    assert not result.is_valid
    assert result.has_warnings
    assert len(result.all_issues) == 3
    assert result.all_issues[0].level == ValidationLevel.ERROR
    assert result.all_issues[1].level == ValidationLevel.WARNING
    assert result.all_issues[2].level == ValidationLevel.INFO


def test_validation_result_raise_if_invalid():
    """Test raise_if_invalid raises for errors."""
    error = ValidationIssue(level=ValidationLevel.ERROR, message="Error")
    result = ValidationResult(errors=[error])

    with pytest.raises(ValidationError) as exc_info:
        result.raise_if_invalid()

    assert exc_info.value.result == result


def test_validation_result_raise_if_invalid_no_error():
    """Test raise_if_invalid does not raise when valid."""
    result = ValidationResult()

    # Should not raise
    result.raise_if_invalid()


def test_validation_result_to_dict():
    """Test converting validation result to dictionary."""
    error = ValidationIssue(level=ValidationLevel.ERROR, message="Error 1")
    warning = ValidationIssue(level=ValidationLevel.WARNING, message="Warning 1")

    result = ValidationResult(errors=[error], warnings=[warning])
    result_dict = result.to_dict()

    assert result_dict["is_valid"] is False
    assert result_dict["error_count"] == 1
    assert result_dict["warning_count"] == 1
    assert len(result_dict["errors"]) == 1
    assert len(result_dict["warnings"]) == 1


def test_validation_result_str():
    """Test string representation of validation result."""
    error = ValidationIssue(level=ValidationLevel.ERROR, message="Test error")
    warning = ValidationIssue(level=ValidationLevel.WARNING, message="Test warning")

    result = ValidationResult(errors=[error], warnings=[warning])
    str_repr = str(result)

    assert "FAILED" in str_repr
    assert "Errors: 1" in str_repr
    assert "Warnings: 1" in str_repr
    assert "Test error" in str_repr
    assert "Test warning" in str_repr


def test_validation_result_str_passed():
    """Test string representation of passed validation."""
    result = ValidationResult()
    str_repr = str(result)

    assert "PASSED" in str_repr
    assert "Errors: 0" in str_repr


def test_validation_error_creation():
    """Test creating a ValidationError."""
    error = ValidationIssue(level=ValidationLevel.ERROR, message="Test error")
    result = ValidationResult(errors=[error])

    exc = ValidationError(result)

    assert exc.result == result
    assert "FAILED" in str(exc)


def test_validation_levels():
    """Test all validation level enum values."""
    assert ValidationLevel.ERROR.value == "error"
    assert ValidationLevel.WARNING.value == "warning"
    assert ValidationLevel.INFO.value == "info"
