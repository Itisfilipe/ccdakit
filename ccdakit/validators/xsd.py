"""XSD schema validator for C-CDA documents."""

from pathlib import Path
from typing import Union

from lxml import etree

from ..core.validation import ValidationIssue, ValidationLevel, ValidationResult
from .base import BaseValidator


class XSDValidator(BaseValidator):
    """
    XSD schema validator for C-CDA documents.

    Validates C-CDA documents against the official HL7 C-CDA XSD schemas.

    Usage:
        >>> validator = XSDValidator("/path/to/schemas/CDA.xsd")
        >>> result = validator.validate(document)
        >>> if result.is_valid:
        ...     print("Document is valid!")
        >>> else:
        ...     print("Validation errors:")
        ...     for error in result.errors:
        ...         print(f"  - {error}")

    Note:
        You must download the C-CDA XSD schemas from HL7 before using
        this validator. See schemas/README.md for instructions.
    """

    def __init__(self, schema_path: Union[str, Path]):
        """
        Initialize XSD validator with schema file.

        Args:
            schema_path: Path to the CDA.xsd schema file

        Raises:
            FileNotFoundError: If schema file doesn't exist
            etree.XMLSchemaParseError: If schema is invalid
        """
        self.schema_path = Path(schema_path)
        if not self.schema_path.exists():
            raise FileNotFoundError(
                f"Schema file not found: {self.schema_path}\n"
                "Please download C-CDA schemas from HL7. "
                "See schemas/README.md for instructions."
            )

        try:
            schema_doc = etree.parse(str(self.schema_path))
            self.schema = etree.XMLSchema(schema_doc)
        except etree.XMLSchemaParseError as e:
            raise etree.XMLSchemaParseError(
                f"Failed to parse XSD schema at {self.schema_path}: {e}"
            ) from e

    def validate(self, document: Union[etree._Element, str, bytes, Path]) -> ValidationResult:
        """
        Validate a C-CDA document against XSD schema.

        Args:
            document: Document to validate. Can be:
                - etree._Element: Parsed XML element
                - str: XML string or file path
                - bytes: XML bytes
                - Path: Path to XML file

        Returns:
            ValidationResult with errors from schema validation

        Raises:
            FileNotFoundError: If file path doesn't exist
            etree.XMLSyntaxError: If document is not well-formed XML
        """
        result = ValidationResult()

        try:
            # Parse document
            doc_element = self._parse_document(document)

            # Validate against schema
            is_valid = self.schema.validate(doc_element)

            if not is_valid:
                # Extract validation errors
                for error in self.schema.error_log:
                    issue = self._parse_schema_error(error)
                    result.errors.append(issue)

        except etree.XMLSyntaxError as e:
            # Document is not well-formed XML
            result.errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"XML syntax error: {e}",
                    location=f"Line {e.lineno}" if hasattr(e, "lineno") else None,
                    code="XML_SYNTAX_ERROR",
                )
            )
        except FileNotFoundError as e:
            result.errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=str(e),
                    code="FILE_NOT_FOUND",
                )
            )
        except Exception as e:
            # Catch any other validation errors
            result.errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Validation error: {e}",
                    code="VALIDATION_ERROR",
                )
            )

        return result

    def _parse_schema_error(self, error: etree._LogEntry) -> ValidationIssue:
        """
        Parse lxml schema error into ValidationIssue.

        Args:
            error: lxml error log entry

        Returns:
            ValidationIssue with error details
        """
        # Extract location information
        location = None
        if error.line is not None:
            location = f"Line {error.line}"
            if error.column is not None:
                location += f", Column {error.column}"

        # Extract error message
        message = error.message

        # Try to extract element path if available
        if error.path:
            location = error.path if not location else f"{location} ({error.path})"

        return ValidationIssue(
            level=ValidationLevel.ERROR,
            message=message,
            location=location,
            code="XSD_VALIDATION_ERROR",
        )

    def validate_file(self, file_path: Union[str, Path]) -> ValidationResult:
        """
        Convenience method to validate a file.

        Args:
            file_path: Path to XML file

        Returns:
            ValidationResult with errors from schema validation

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        return self.validate(Path(file_path))

    def validate_string(self, xml_string: str) -> ValidationResult:
        """
        Convenience method to validate an XML string.

        Args:
            xml_string: XML document as string

        Returns:
            ValidationResult with errors from schema validation
        """
        return self.validate(xml_string)

    def validate_bytes(self, xml_bytes: bytes) -> ValidationResult:
        """
        Convenience method to validate XML bytes.

        Args:
            xml_bytes: XML document as bytes

        Returns:
            ValidationResult with errors from schema validation
        """
        return self.validate(xml_bytes)

    @property
    def schema_location(self) -> Path:
        """Get the schema file location."""
        return self.schema_path
