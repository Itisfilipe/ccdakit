"""XSD schema validator for C-CDA documents."""

from pathlib import Path
from typing import Optional, Union

from lxml import etree

from ..core.validation import ValidationIssue, ValidationLevel, ValidationResult
from .base import BaseValidator


class XSDValidator(BaseValidator):
    """
    XSD schema validator for C-CDA documents.

    Validates C-CDA documents against the official HL7 C-CDA XSD schemas.

    Usage:
        >>> # Use default schemas (auto-downloads if needed)
        >>> validator = XSDValidator()
        >>> result = validator.validate(document)
        >>> if result.is_valid:
        ...     print("Document is valid!")
        >>> else:
        ...     print("Validation errors:")
        ...     for error in result.errors:
        ...         print(f"  - {error}")

        >>> # Or provide custom schema path
        >>> validator = XSDValidator("/path/to/schemas/CDA.xsd")
        >>> result = validator.validate(document)

    Note:
        XSD schemas are automatically downloaded on first use if not present.
        Set auto_download=False to disable automatic downloads.
    """

    def __init__(
        self,
        schema_path: Optional[Union[str, Path]] = None,
        auto_download: bool = True,
    ):
        """
        Initialize XSD validator with schema file.

        Args:
            schema_path: Path to the CDA.xsd schema file.
                If None, uses default location and auto-downloads if needed.
            auto_download: Automatically download schemas if missing.
                Default: True. Set to False to disable automatic downloads.

        Raises:
            FileNotFoundError: If schema file doesn't exist and auto_download=False
            etree.XMLSchemaParseError: If schema is invalid

        Note:
            On first use, XSD schemas (~2MB) will be automatically downloaded
            from HL7's official repository. This may take a few moments.
        """
        self.auto_download = auto_download
        self.schema_path = self._resolve_schema_path(schema_path)

        # Attempt auto-download if file doesn't exist
        if not self.schema_path.exists() and self.auto_download:
            self._attempt_auto_download()

        # Check if file exists after download attempt
        if not self.schema_path.exists():
            raise FileNotFoundError(
                f"Schema file not found: {self.schema_path}\n"
                "Expected file: schemas/CDA.xsd\n\n"
                "Options:\n"
                "1. Allow automatic download (default): XSDValidator(auto_download=True)\n"
                "2. Download manually from: https://github.com/HL7/CDA-core-xsd\n"
                "3. Provide your own file: XSDValidator(schema_path='/path/to/CDA.xsd')"
            )

        try:
            schema_doc = etree.parse(str(self.schema_path))
            self.schema = etree.XMLSchema(schema_doc)
        except etree.XMLSchemaParseError as e:
            raise etree.XMLSchemaParseError(
                f"Failed to parse XSD schema at {self.schema_path}: {e}"
            ) from e

    def _resolve_schema_path(self, path: Optional[Union[str, Path]]) -> Path:
        """
        Resolve XSD schema path.

        Args:
            path: User-provided path or None for default

        Returns:
            Resolved Path object
        """
        if path is not None:
            return Path(path)

        # Default to CDA.xsd in package schemas directory
        current_dir = Path(__file__).parent
        package_root = current_dir.parent.parent

        # Check common locations
        locations = [
            package_root / "schemas" / "CDA.xsd",
            Path("schemas") / "CDA.xsd",
            Path.cwd() / "schemas" / "CDA.xsd",
        ]

        for location in locations:
            if location.exists():
                return location

        # Return default expected location (may not exist yet)
        return package_root / "schemas" / "CDA.xsd"

    def _attempt_auto_download(self) -> None:
        """
        Attempt to automatically download XSD schema files.

        This method tries to download the official HL7 C-CDA XSD schemas
        if they're not present. Downloads are only attempted once.
        """
        try:
            from .xsd_downloader import XSDDownloader

            print("XSD schemas not found. Attempting automatic download...")
            print("This is a one-time download (~2MB). Please wait...")

            downloader = XSDDownloader()
            success, message = downloader.download_schemas(force=False)

            if success:
                print(message)
                print("✓ XSD schemas ready for validation!")
            else:
                import warnings

                warnings.warn(
                    f"Automatic download failed:\n{message}\n"
                    "You can provide your own schema file or download manually.",
                    UserWarning,
                    stacklevel=2,
                )

        except Exception as e:
            import warnings

            warnings.warn(
                f"Automatic download failed: {e}\n"
                "You can provide your own schema file using: "
                "XSDValidator(schema_path='/path/to/CDA.xsd')",
                UserWarning,
                stacklevel=2,
            )

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
