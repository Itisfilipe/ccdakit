"""XSLT utilities for C-CDA to HTML conversion.

This module provides utilities for downloading and using the official HL7 CDA
stylesheet to convert C-CDA XML documents to human-readable HTML.
"""

import logging
import urllib.request
from pathlib import Path
from typing import Optional, Union

from lxml import etree


logger = logging.getLogger(__name__)


# Official HL7 CDA Stylesheet URL from the official HL7 CDA-core-xsl repository
# Repository: https://github.com/HL7/CDA-core-xsl
CDA_STYLESHEET_URL = "https://raw.githubusercontent.com/HL7/CDA-core-xsl/master/CDA.xsl"


def get_default_xslt_path() -> Path:
    """Get the default path for XSLT stylesheets."""
    # Store in schemas directory (same location as schematron files)
    # Use the project's schemas directory
    schemas_dir = Path(__file__).parent.parent.parent / "schemas"
    xslt_dir = schemas_dir / "xslt"

    # Create directory if it doesn't exist
    xslt_dir.mkdir(parents=True, exist_ok=True)

    return xslt_dir


def download_cda_stylesheet(target_dir: Optional[Path] = None) -> Path:
    """
    Download the official HL7 CDA stylesheet and its dependencies for rendering C-CDA documents.

    The official stylesheet requires these files:
    - CDA.xsl (main stylesheet)
    - cda_narrativeblock.xml (narrative validation)
    - cda_l10n.xml (localization)

    Args:
        target_dir: Directory to save the stylesheet. If None, uses default location.

    Returns:
        Path to the downloaded stylesheet file.

    Raises:
        urllib.error.URLError: If download fails
    """
    if target_dir is None:
        target_dir = get_default_xslt_path()

    target_dir.mkdir(parents=True, exist_ok=True)

    # Define all required files
    base_url = "https://raw.githubusercontent.com/HL7/CDA-core-xsl/master"
    required_files = [
        ("CDA.xsl", "cda.xsl"),  # (remote name, local name)
        ("cda_narrativeblock.xml", "cda_narrativeblock.xml"),
        ("cda_l10n.xml", "cda_l10n.xml"),
    ]

    main_stylesheet = target_dir / "cda.xsl"

    # Check if already downloaded
    if main_stylesheet.exists():
        return main_stylesheet

    logger.info("Downloading official HL7 CDA stylesheet and dependencies...")
    logger.info("Source: https://github.com/HL7/CDA-core-xsl")

    try:
        # Download all required files
        for remote_name, local_name in required_files:
            url = f"{base_url}/{remote_name}"
            local_path = target_dir / local_name
            logger.info("  Downloading %s...", remote_name)
            urllib.request.urlretrieve(url, local_path)

        logger.info("Downloaded CDA stylesheet to %s", target_dir)
        return main_stylesheet
    except Exception as e:
        raise RuntimeError(f"Failed to download CDA stylesheet: {e}") from e


def transform_cda_to_html(
    xml_path: Union[str, Path],
    xslt_path: Optional[Union[str, Path]] = None,
) -> str:
    """
    Transform a C-CDA XML document to HTML using XSLT.

    Args:
        xml_path: Path to the C-CDA XML file
        xslt_path: Path to XSLT stylesheet. If None, uses official HL7 CDA stylesheet.

    Returns:
        HTML string

    Raises:
        FileNotFoundError: If XML file doesn't exist
        etree.XMLSyntaxError: If XML is malformed
        etree.XSLTParseError: If XSLT stylesheet is invalid
        etree.XSLTApplyError: If transformation fails
    """
    xml_path = Path(xml_path)
    if not xml_path.exists():
        raise FileNotFoundError(f"XML file not found: {xml_path}")

    # Get XSLT stylesheet
    if xslt_path is None:
        default_xslt = get_default_xslt_path() / "cda.xsl"
        if not default_xslt.exists():
            download_cda_stylesheet()
        xslt_path = default_xslt
    else:
        xslt_path = Path(xslt_path)
        if not xslt_path.exists():
            raise FileNotFoundError(f"XSLT stylesheet not found: {xslt_path}")

    # Parse XML document
    xml_doc = etree.parse(str(xml_path))

    # Parse XSLT stylesheet
    xslt_doc = etree.parse(str(xslt_path))
    transform = etree.XSLT(xslt_doc)

    # Apply transformation
    result = transform(xml_doc)

    # Return HTML as string
    return str(result)


def transform_cda_string_to_html(
    xml_string: str,
    xslt_path: Optional[Union[str, Path]] = None,
) -> str:
    """
    Transform a C-CDA XML string to HTML using XSLT.

    Args:
        xml_string: C-CDA XML as string
        xslt_path: Path to XSLT stylesheet. If None, uses official HL7 CDA stylesheet.

    Returns:
        HTML string

    Raises:
        etree.XMLSyntaxError: If XML is malformed
        etree.XSLTParseError: If XSLT stylesheet is invalid
        etree.XSLTApplyError: If transformation fails
    """
    # Get XSLT stylesheet
    if xslt_path is None:
        default_xslt = get_default_xslt_path() / "cda.xsl"
        if not default_xslt.exists():
            download_cda_stylesheet()
        xslt_path = default_xslt
    else:
        xslt_path = Path(xslt_path)
        if not xslt_path.exists():
            raise FileNotFoundError(f"XSLT stylesheet not found: {xslt_path}")

    # Parse XML string
    xml_doc = etree.fromstring(xml_string.encode("utf-8"))

    # Parse XSLT stylesheet
    xslt_doc = etree.parse(str(xslt_path))
    transform = etree.XSLT(xslt_doc)

    # Apply transformation
    result = transform(xml_doc)

    # Return HTML as string
    return str(result)
