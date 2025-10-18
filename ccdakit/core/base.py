"""Core base classes for C-CDA builders."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from lxml import etree


if TYPE_CHECKING:
    from ccdakit.validators.xsd import XSDValidator


class CDAVersion(Enum):
    """Supported C-CDA versions."""

    R1_1 = "1.1"
    R2_0 = "2.0"
    R2_1 = "2.1"
    R3_0 = "3.0"  # Planned


class TemplateConfig:
    """Template identifier configuration."""

    # CDA namespace for element creation
    NS = "urn:hl7-org:v3"

    def __init__(
        self,
        root: str,
        extension: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        """
        Initialize template configuration.

        Args:
            root: Template OID
            extension: Version extension (e.g., '2015-08-01')
            description: Human-readable description
        """
        self.root = root
        self.extension = extension
        self.description = description

    def to_element(self) -> etree._Element:
        """
        Convert to templateId XML element.

        Returns:
            lxml Element for templateId
        """
        elem = etree.Element(f"{{{self.NS}}}templateId", root=self.root)
        if self.extension:
            elem.set("extension", self.extension)
        return elem


class CDAElement(ABC):
    """
    Base class for all CDA elements.

    All builders inherit from this class and implement the build() method.
    """

    # Subclasses override with version-specific templates
    TEMPLATES: "dict[CDAVersion, List[TemplateConfig]]" = {}

    def __init__(
        self,
        version: CDAVersion = CDAVersion.R2_1,
        schema: Optional["XSDValidator"] = None,
    ) -> None:
        """
        Initialize CDA element.

        Args:
            version: C-CDA version to generate
            schema: Optional XSD validator
        """
        self.version = version
        self.schema = schema

    @abstractmethod
    def build(self) -> etree._Element:
        """
        Build and return the XML element.

        This method must be implemented by subclasses.

        Returns:
            lxml Element representing this CDA component
        """
        pass

    def to_element(self) -> etree._Element:
        """
        Build element with optional validation.

        Returns:
            lxml Element representing this CDA component

        Raises:
            etree.DocumentInvalid: If validation fails
        """
        element = self.build()

        if self.schema:
            self.schema.assert_valid(element)

        return element

    def to_string(self, pretty: bool = True, encoding: str = "unicode") -> str:
        """
        Convert to XML string.

        Args:
            pretty: Whether to pretty-print XML
            encoding: Output encoding ('unicode' or 'utf-8')

        Returns:
            XML string representation
        """
        return etree.tostring(
            self.to_element(),
            pretty_print=pretty,
            encoding=encoding,  # type: ignore
        )

    def get_templates(self) -> List[TemplateConfig]:
        """
        Get templateIds for current version.

        Returns:
            List of TemplateConfig for this version

        Raises:
            ValueError: If version not supported
        """
        if self.version not in self.TEMPLATES:
            raise ValueError(
                f"Version {self.version.value} not supported for {self.__class__.__name__}"
            )
        return self.TEMPLATES[self.version]

    def add_template_ids(self, parent: etree._Element) -> None:
        """
        Add all templateIds for current version to parent element.

        Args:
            parent: Parent element to add templateIds to
        """
        for template in self.get_templates():
            parent.append(template.to_element())
