"""Validation infrastructure for C-CDA documents."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ValidationLevel(Enum):
    """Validation severity levels."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    """A validation issue (error, warning, or info)."""

    level: ValidationLevel
    message: str
    location: str | None = None  # XPath or description
    code: str | None = None  # Error code for categorization
    parsed_data: dict[str, Any] | None = None  # Parsed error data for enhanced display

    def __str__(self) -> str:
        """String representation of issue."""
        location_str = f" at {self.location}" if self.location else ""
        code_str = f" [{self.code}]" if self.code else ""
        return f"{self.level.value.upper()}{location_str}: {self.message}{code_str}"


@dataclass
class ValidationResult:
    """Result of validation with errors, warnings, and info."""

    errors: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)
    infos: list[ValidationIssue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Check if validation passed (no errors)."""
        return len(self.errors) == 0

    @property
    def has_warnings(self) -> bool:
        """Check if there are warnings."""
        return len(self.warnings) > 0

    @property
    def all_issues(self) -> list[ValidationIssue]:
        """Get all issues in order: errors, warnings, infos."""
        return self.errors + self.warnings + self.infos

    def raise_if_invalid(self) -> None:
        """
        Raise ValidationError if validation failed.

        Raises:
            ValidationError: If there are any errors
        """
        if not self.is_valid:
            raise ValidationError(self)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""

        def issue_to_dict(issue: ValidationIssue) -> dict:
            """Convert a single issue to dict, including parsed data if available."""
            result = {
                "message": str(issue),
                "raw_message": issue.message,
            }
            # Only add parsed data if it exists (Schematron validation has it, XSD doesn't)
            if hasattr(issue, "parsed_data") and issue.parsed_data:
                result["parsed"] = issue.parsed_data
            return result

        return {
            "is_valid": self.is_valid,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "info_count": len(self.infos),
            "errors": [issue_to_dict(e) for e in self.errors],
            "warnings": [issue_to_dict(w) for w in self.warnings],
            "infos": [issue_to_dict(i) for i in self.infos],
        }

    def __str__(self) -> str:
        """String representation of validation result."""
        lines = [
            f"Validation {'PASSED' if self.is_valid else 'FAILED'}",
            f"Errors: {len(self.errors)}, Warnings: {len(self.warnings)}, Info: {len(self.infos)}",
        ]

        if self.errors:
            lines.append("\nErrors:")
            lines.extend(f"  - {e}" for e in self.errors)

        if self.warnings:
            lines.append("\nWarnings:")
            lines.extend(f"  - {w}" for w in self.warnings)

        return "\n".join(lines)


class ValidationError(Exception):
    """Exception raised when validation fails."""

    def __init__(self, result: ValidationResult) -> None:
        """
        Initialize with validation result.

        Args:
            result: ValidationResult containing errors
        """
        self.result = result
        super().__init__(str(result))
