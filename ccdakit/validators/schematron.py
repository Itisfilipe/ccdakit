"""Schematron validator for C-CDA documents."""

import warnings
from pathlib import Path
from typing import List, Optional, Union

from lxml import etree, isoschematron

from ..core.validation import ValidationIssue, ValidationLevel, ValidationResult
from .base import BaseValidator
from .schematron_downloader import SchematronDownloader


class SchematronValidator(BaseValidator):
    """
    Schematron validator for C-CDA documents.

    Validates C-CDA documents using ISO Schematron rules for business logic,
    template conformance, and ONC certification requirements.

    Usage:
        >>> # Use default HL7 C-CDA R2.1 Schematron
        >>> validator = SchematronValidator()
        >>> result = validator.validate(document)
        >>> if result.is_valid:
        ...     print("Document passes Schematron validation!")
        >>> else:
        ...     print("Validation errors:")
        ...     for error in result.errors:
        ...         print(f"  - {error}")

        >>> # Use custom Schematron file
        >>> validator = SchematronValidator("/path/to/custom.sch")
        >>> result = validator.validate(document)

    Note:
        Schematron validation requires both the .sch file and voc.xml vocabulary file.
        These are automatically included in the schemas/schematron/ directory.
    """

    # SVRL namespace for validation report
    SVRL_NS = "http://purl.oclc.org/dsdl/svrl"

    def __init__(
        self,
        schematron_path: Optional[Union[str, Path]] = None,
        phase: Optional[str] = None,
        auto_download: bool = True,
    ):
        """
        Initialize Schematron validator.

        Args:
            schematron_path: Path to Schematron file (.sch).
                If None, uses default HL7 C-CDA R2.1 Schematron.
            phase: Schematron phase to use (e.g., "errors", "warnings").
                If None, validates all phases.
            auto_download: Automatically download Schematron files if missing.
                Default: True. Set to False to disable automatic downloads.

        Raises:
            FileNotFoundError: If schematron file doesn't exist and auto_download=False
            etree.SchematronParseError: If schematron is invalid

        Note:
            On first use, Schematron files (~63MB) will be automatically downloaded
            from HL7's official GitHub repository. This may take a few moments.
        """
        self.schematron_path = self._resolve_schematron_path(schematron_path)
        self.phase = phase
        self.auto_download = auto_download

        # Attempt auto-download if file doesn't exist
        if not self.schematron_path.exists() and self.auto_download:
            self._attempt_auto_download()

        # Check if file exists after download attempt
        if not self.schematron_path.exists():
            raise FileNotFoundError(
                f"Schematron file not found: {self.schematron_path}\n"
                "Expected file: schemas/schematron/HL7_CCDA_R2.1.sch\n\n"
                "Options:\n"
                "1. Allow automatic download (default): SchematronValidator(auto_download=True)\n"
                "2. Download manually from: https://github.com/HL7/CDA-ccda-2.1\n"
                "3. Provide your own file: SchematronValidator(schematron_path='/path/to/file.sch')"
            )

        self.schematron = self._load_schematron()

    def _resolve_schematron_path(self, path: Optional[Union[str, Path]]) -> Path:
        """
        Resolve Schematron file path.

        Args:
            path: User-provided path or None for default

        Returns:
            Resolved Path object
        """
        if path is not None:
            return Path(path)

        # Default to HL7 C-CDA R2.1 Schematron in package
        # Try to find schemas directory relative to this file
        current_dir = Path(__file__).parent
        package_root = current_dir.parent.parent

        # Check common locations
        locations = [
            package_root / "schemas" / "schematron" / "HL7_CCDA_R2.1.sch",
            Path("schemas") / "schematron" / "HL7_CCDA_R2.1.sch",
            Path.cwd() / "schemas" / "schematron" / "HL7_CCDA_R2.1.sch",
        ]

        for location in locations:
            if location.exists():
                return location

        # Return default expected location (may not exist yet)
        return package_root / "schemas" / "schematron" / "HL7_CCDA_R2.1.sch"

    def _attempt_auto_download(self) -> None:
        """
        Attempt to automatically download Schematron files.

        This method tries to download the official HL7 C-CDA R2.1 Schematron
        files if they're not present. Downloads are only attempted once.
        """
        try:
            print("Schematron files not found. Attempting automatic download...")
            print("This is a one-time download (~63MB). Please wait...")

            downloader = SchematronDownloader()
            success, message = downloader.download_all(force=False)

            if success:
                print(message)
                print("✓ Schematron files ready for validation!")
            else:
                warnings.warn(
                    f"Automatic download failed:\n{message}\n"
                    "You can provide your own Schematron file or download manually.",
                    UserWarning,
                    stacklevel=2,
                )

        except Exception as e:
            warnings.warn(
                f"Automatic download failed: {e}\n"
                "You can provide your own Schematron file using: "
                "SchematronValidator(schematron_path='/path/to/file.sch')",
                UserWarning,
                stacklevel=2,
            )

    def _load_schematron(self) -> isoschematron.Schematron:
        """
        Load and compile Schematron rules.

        Returns:
            Compiled Schematron object

        Raises:
            etree.SchematronParseError: If schematron is invalid
        """
        try:
            # Parse Schematron document
            with open(self.schematron_path, "rb") as f:
                schematron_doc = etree.parse(f)

            # Create Schematron validator
            # store_schematron=True keeps the compiled schematron for inspection
            # store_report=True keeps validation reports for error extraction
            kwargs = {
                "store_schematron": True,
                "store_report": True,
            }

            if self.phase is not None:
                kwargs["phase"] = self.phase

            return isoschematron.Schematron(schematron_doc, **kwargs)

        except etree.XMLSyntaxError as e:
            raise etree.SchematronParseError(
                f"Failed to parse Schematron file at {self.schematron_path}: {e}"
            ) from e
        except Exception as e:
            raise etree.SchematronParseError(
                f"Failed to load Schematron at {self.schematron_path}: {e}"
            ) from e

    def validate(self, document: Union[etree._Element, str, bytes, Path]) -> ValidationResult:
        """
        Validate a C-CDA document against Schematron rules.

        Args:
            document: Document to validate. Can be:
                - etree._Element: Parsed XML element
                - str: XML string or file path
                - bytes: XML bytes
                - Path: Path to XML file

        Returns:
            ValidationResult with Schematron validation findings

        Raises:
            FileNotFoundError: If file path doesn't exist
            etree.XMLSyntaxError: If document is not well-formed XML
        """
        result = ValidationResult()

        try:
            # Parse document
            doc_element = self._parse_document(document)

            # Run Schematron validation
            is_valid = self.schematron.validate(doc_element)

            if not is_valid:
                # Extract validation messages from SVRL report
                report = self.schematron.validation_report
                issues = self._extract_issues_from_report(report)

                # Categorize issues by level (schematron reports as failed-assert or successful-report)
                for issue in issues:
                    if issue.level == ValidationLevel.ERROR:
                        result.errors.append(issue)
                    elif issue.level == ValidationLevel.WARNING:
                        result.warnings.append(issue)
                    else:
                        result.infos.append(issue)

        except etree.XMLSyntaxError as e:
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
            result.errors.append(
                ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Schematron validation error: {e}",
                    code="SCHEMATRON_ERROR",
                )
            )

        return result

    def _extract_issues_from_report(self, report: etree._Element) -> List[ValidationIssue]:
        """
        Extract validation issues from SVRL report.

        Args:
            report: SVRL validation report element

        Returns:
            List of ValidationIssue objects
        """
        issues = []

        # Extract failed assertions (errors)
        for element in report.findall(f".//{{{self.SVRL_NS}}}failed-assert"):
            issue = self._parse_failed_assert(element)
            if issue:
                issues.append(issue)

        # Extract successful reports (warnings/info)
        for element in report.findall(f".//{{{self.SVRL_NS}}}successful-report"):
            issue = self._parse_successful_report(element)
            if issue:
                issues.append(issue)

        return issues

    def _parse_failed_assert(self, element: etree._Element) -> Optional[ValidationIssue]:
        """
        Parse failed-assert element from SVRL report.

        Args:
            element: failed-assert element

        Returns:
            ValidationIssue or None
        """
        # Extract message text
        text_elem = element.find(f"{{{self.SVRL_NS}}}text")
        if text_elem is None:
            return None

        message = self._extract_text_content(text_elem)
        if not message:
            return None

        # Extract location (XPath where assertion failed)
        location = element.get("location")

        # Extract rule ID (CONF ID or template ID)
        rule_id = element.get("id")

        # Build error code from rule ID
        code = f"SCHEMATRON_{rule_id}" if rule_id else "SCHEMATRON_ERROR"

        return ValidationIssue(
            level=ValidationLevel.ERROR,
            message=message,
            location=location,
            code=code,
        )

    def _parse_successful_report(self, element: etree._Element) -> Optional[ValidationIssue]:
        """
        Parse successful-report element from SVRL report.

        Successful reports are typically warnings or informational messages.

        Args:
            element: successful-report element

        Returns:
            ValidationIssue or None
        """
        # Extract message text
        text_elem = element.find(f"{{{self.SVRL_NS}}}text")
        if text_elem is None:
            return None

        message = self._extract_text_content(text_elem)
        if not message:
            return None

        # Extract location
        location = element.get("location")

        # Extract rule ID
        rule_id = element.get("id")

        # Determine level based on rule ID or message content
        # C-CDA Schematron typically uses role="warning" or role="info"
        role = element.get("role", "").lower()
        if "warning" in role or "warn" in message.lower():
            level = ValidationLevel.WARNING
        else:
            level = ValidationLevel.INFO

        code = f"SCHEMATRON_{rule_id}" if rule_id else "SCHEMATRON_INFO"

        return ValidationIssue(
            level=level,
            message=message,
            location=location,
            code=code,
        )

    def _extract_text_content(self, element: etree._Element) -> str:
        """
        Extract text content from element, handling nested elements.

        Args:
            element: Element containing text

        Returns:
            Concatenated text content
        """
        # Get all text including from nested elements
        text_parts = []

        # Get element's direct text
        if element.text:
            text_parts.append(element.text.strip())

        # Get text from all descendants
        for child in element:
            if child.text:
                text_parts.append(child.text.strip())
            if child.tail:
                text_parts.append(child.tail.strip())

        # Join and clean up
        full_text = " ".join(text_parts)
        # Remove extra whitespace
        return " ".join(full_text.split())

    def validate_file(self, file_path: Union[str, Path]) -> ValidationResult:
        """
        Convenience method to validate a file.

        Args:
            file_path: Path to XML file

        Returns:
            ValidationResult with Schematron validation findings

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
            ValidationResult with Schematron validation findings
        """
        return self.validate(xml_string)

    def validate_bytes(self, xml_bytes: bytes) -> ValidationResult:
        """
        Convenience method to validate XML bytes.

        Args:
            xml_bytes: XML document as bytes

        Returns:
            ValidationResult with Schematron validation findings
        """
        return self.validate(xml_bytes)

    @property
    def schematron_location(self) -> Path:
        """Get the Schematron file location."""
        return self.schematron_path

    @property
    def validation_phase(self) -> Optional[str]:
        """Get the validation phase being used."""
        return self.phase
