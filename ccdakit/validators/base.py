"""Base validator protocol for C-CDA documents."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from lxml import etree

from ..core.validation import ValidationResult


class BaseValidator(ABC):
    """
    Abstract base class for C-CDA validators.

    All validators should inherit from this class and implement
    the validate method.
    """

    @abstractmethod
    def validate(self, document: Union[etree._Element, str, bytes, Path]) -> ValidationResult:
        """
        Validate a C-CDA document.

        Args:
            document: Document to validate. Can be:
                - etree._Element: Parsed XML element
                - str: XML string or file path
                - bytes: XML bytes
                - Path: Path to XML file

        Returns:
            ValidationResult with errors, warnings, and info messages

        Raises:
            FileNotFoundError: If file path doesn't exist
            etree.XMLSyntaxError: If document is not well-formed XML
        """
        pass

    def _parse_document(self, document: Union[etree._Element, str, bytes, Path]) -> etree._Element:
        """
        Parse document into an lxml Element.

        Args:
            document: Document in various formats

        Returns:
            Parsed XML element

        Raises:
            FileNotFoundError: If file path doesn't exist
            etree.XMLSyntaxError: If document is not well-formed XML
        """
        if isinstance(document, etree._Element):
            return document

        if isinstance(document, Path):
            if not document.exists():
                raise FileNotFoundError(f"File not found: {document}")
            return etree.parse(str(document)).getroot()

        if isinstance(document, str):
            # Check if it looks like XML (starts with < or whitespace then <)
            stripped = document.lstrip()
            if stripped.startswith("<"):
                # Parse as XML string
                return etree.fromstring(document.encode("utf-8"))
            # Otherwise try as file path
            path = Path(document)
            if path.exists():
                return etree.parse(str(path)).getroot()
            # If not found, try parsing as XML anyway (might be malformed)
            return etree.fromstring(document.encode("utf-8"))

        if isinstance(document, bytes):
            return etree.fromstring(document)

        raise TypeError(
            f"Unsupported document type: {type(document)}. "
            "Expected etree._Element, str, bytes, or Path"
        )
