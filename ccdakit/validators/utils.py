"""Utilities for managing C-CDA XSD schemas."""

import zipfile
from pathlib import Path
from typing import Optional, Tuple
from urllib.request import urlretrieve


# Default schema directory (relative to project root)
DEFAULT_SCHEMA_DIR = Path(__file__).parent.parent.parent / "schemas"

# Schema download URLs (these may need to be updated)
SCHEMA_URLS = {
    "R2.1": "https://www.hl7.org/fhir/cda/downloads/ccda-schemas-2.1.zip",
    "R2.0": "https://www.hl7.org/fhir/cda/downloads/ccda-schemas-2.0.zip",
}


class SchemaManager:
    """
    Manager for C-CDA XSD schemas.

    Helps with schema discovery, downloading, and path management.
    """

    def __init__(self, schema_dir: Optional[Path] = None):
        """
        Initialize schema manager.

        Args:
            schema_dir: Directory containing schemas. Defaults to project's schemas/ directory.
        """
        self.schema_dir = schema_dir or DEFAULT_SCHEMA_DIR
        self.schema_dir.mkdir(parents=True, exist_ok=True)

    def is_installed(self) -> bool:
        """
        Check if C-CDA schemas are installed.

        Returns:
            True if CDA.xsd exists in schema directory
        """
        return self.get_cda_schema_path().exists()

    def get_cda_schema_path(self) -> Path:
        """
        Get path to main CDA.xsd schema file.

        Returns:
            Path to CDA.xsd (may not exist)
        """
        return self.schema_dir / "CDA.xsd"

    def get_schema_info(self) -> dict:
        """
        Get information about installed schemas.

        Returns:
            Dictionary with schema installation status and paths
        """
        cda_path = self.get_cda_schema_path()
        return {
            "installed": cda_path.exists(),
            "schema_dir": str(self.schema_dir),
            "cda_schema": str(cda_path),
            "cda_exists": cda_path.exists(),
            "files": [f.name for f in self.schema_dir.iterdir() if f.is_file()],
        }

    def download_schemas(
        self,
        version: str = "R2.1",
        url: Optional[str] = None,
        force: bool = False,
    ) -> Tuple[bool, str]:
        """
        Download C-CDA schemas from HL7.

        Note: This is a helper function, but schemas may need to be
        downloaded manually from HL7's website due to licensing.

        Args:
            version: C-CDA version (R2.1 or R2.0)
            url: Custom download URL (overrides version)
            force: Force re-download even if schemas exist

        Returns:
            Tuple of (success: bool, message: str)

        Raises:
            ValueError: If version is not supported
        """
        if self.is_installed() and not force:
            return (
                True,
                f"Schemas already installed at {self.schema_dir}. Use force=True to re-download.",
            )

        if url is None:
            if version not in SCHEMA_URLS:
                raise ValueError(
                    f"Unsupported version: {version}. "
                    f"Supported versions: {list(SCHEMA_URLS.keys())}"
                )
            url = SCHEMA_URLS[version]

        try:
            # Download zip file
            zip_path = self.schema_dir / "schemas.zip"
            urlretrieve(url, zip_path)

            # Extract schemas
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(self.schema_dir)

            # Clean up zip file
            zip_path.unlink()

            return True, f"Schemas downloaded successfully to {self.schema_dir}"

        except Exception as e:
            return False, f"Failed to download schemas: {e}"

    def print_installation_instructions(self) -> None:
        """Print instructions for manually downloading schemas."""
        instructions = f"""
C-CDA XSD Schema Installation Instructions
==========================================

The C-CDA XSD schemas must be downloaded from HL7 due to licensing restrictions.

Method 1: Download from HL7 (Recommended)
------------------------------------------
1. Visit the HL7 C-CDA download page:
   - R2.1: https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492
   - R2.0: https://www.hl7.org/implement/standards/product_brief.cfm?product_id=379

2. Download the schema package (e.g., "CCDA_R2.1_Schemas.zip")

3. Extract the following files to: {self.schema_dir}
   - CDA.xsd (main schema file)
   - POCD_MT000040_CCDA.xsd
   - datatypes.xsd
   - voc.xsd
   - NarrativeBlock.xsd
   - SDTC/ directory (if available)

Method 2: Use Schema Manager (Automated)
-----------------------------------------
>>> from ccdakit.validators.utils import SchemaManager
>>> manager = SchemaManager()
>>> success, message = manager.download_schemas(version="R2.1")
>>> print(message)

Note: Automated download may not work due to HL7's licensing requirements.
      Manual download is recommended.

Verification
------------
After installation, verify schemas are available:

>>> manager = SchemaManager()
>>> info = manager.get_schema_info()
>>> print(info)

The 'cda_exists' field should be True.
"""
        print(instructions)


def get_default_schema_path() -> Optional[Path]:
    """
    Get default CDA.xsd schema path if available.

    Returns:
        Path to CDA.xsd if installed, None otherwise
    """
    manager = SchemaManager()
    path = manager.get_cda_schema_path()
    return path if path.exists() else None


def check_schema_installed() -> bool:
    """
    Check if C-CDA schemas are installed.

    Returns:
        True if schemas are available
    """
    manager = SchemaManager()
    return manager.is_installed()


def install_schemas(version: str = "R2.1", force: bool = False) -> bool:
    """
    Install C-CDA schemas.

    Args:
        version: C-CDA version (R2.1 or R2.0)
        force: Force re-download

    Returns:
        True if installation succeeded
    """
    manager = SchemaManager()
    success, message = manager.download_schemas(version=version, force=force)
    print(message)
    return success


def print_schema_installation_help() -> None:
    """Print schema installation instructions."""
    manager = SchemaManager()
    manager.print_installation_instructions()
