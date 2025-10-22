"""Utility for downloading C-CDA XSD schema files."""

import logging
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional, Tuple


logger = logging.getLogger(__name__)


class XSDDownloader:
    """
    Downloads C-CDA XSD schema files from HL7 GitHub repository.

    The XSD schemas are required for structural validation of C-CDA documents.
    This utility downloads them from the official HL7 repository.
    """

    # Official HL7 CDA core schema repository
    # Note: Using codeload.github.com for direct zip downloads
    BASE_URL = "https://codeload.github.com/HL7/CDA-core-sd/zip/refs/heads"

    # Using the master branch which contains all necessary XSD files
    SCHEMA_ZIP_URL = f"{BASE_URL}/master"

    def __init__(self, target_dir: Optional[Path] = None):
        """
        Initialize downloader.

        Args:
            target_dir: Directory to download files to.
                If None, uses schemas/ relative to package root.
        """
        if target_dir is None:
            # Default to schemas in package root
            package_root = Path(__file__).parent.parent.parent
            target_dir = package_root / "schemas"

        self.target_dir = Path(target_dir)
        self.target_dir.mkdir(parents=True, exist_ok=True)

    def is_installed(self) -> bool:
        """
        Check if XSD schemas are already installed.

        Returns:
            True if CDA.xsd exists
        """
        return (self.target_dir / "CDA.xsd").exists()

    def download_schemas(self, force: bool = False) -> Tuple[bool, str]:
        """
        Download and extract XSD schema files.

        Args:
            force: Force download even if schemas exist

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if self.is_installed() and not force:
                return True, "XSD schemas already installed"

            logger.info("Downloading C-CDA XSD schemas from HL7 repository...")
            print("Downloading C-CDA XSD schemas...")
            print("This is a one-time download (~2MB). Please wait...")

            # Download zip file
            zip_path = self.target_dir / "schemas_temp.zip"

            try:
                urllib.request.urlretrieve(self.SCHEMA_ZIP_URL, zip_path)
            except Exception as e:
                return False, f"Failed to download schemas: {e}"

            # Extract schemas
            try:
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    # Extract all files
                    zip_ref.extractall(self.target_dir / "temp")

                # Move files from the extracted directory to target
                extracted_dir = self.target_dir / "temp" / "CDA-core-sd-master"

                if extracted_dir.exists():
                    # Copy XSD files to target directory
                    for xsd_file in extracted_dir.glob("**/*.xsd"):
                        target_file = self.target_dir / xsd_file.name
                        target_file.write_bytes(xsd_file.read_bytes())
                        logger.info(f"Installed: {xsd_file.name}")
                else:
                    return False, "Failed to find extracted schema files"

                # Clean up temp files
                zip_path.unlink(missing_ok=True)
                self._cleanup_temp_dir(self.target_dir / "temp")

                if self.is_installed():
                    return True, f"✓ XSD schemas installed successfully to {self.target_dir}"
                else:
                    return False, "Schema files were downloaded but CDA.xsd not found"

            except Exception as e:
                zip_path.unlink(missing_ok=True)
                self._cleanup_temp_dir(self.target_dir / "temp")
                return False, f"Failed to extract schemas: {e}"

        except Exception as e:
            logger.error(f"Error downloading schemas: {e}")
            return False, f"Failed to download schemas: {e}"

    def _cleanup_temp_dir(self, temp_dir: Path) -> None:
        """
        Recursively delete temporary directory.

        Args:
            temp_dir: Path to temporary directory
        """
        if not temp_dir.exists():
            return

        try:
            import shutil
            shutil.rmtree(temp_dir)
        except Exception as e:
            logger.warning(f"Failed to clean up temp directory: {e}")

    def get_schema_info(self) -> dict:
        """
        Get information about installed schemas.

        Returns:
            Dictionary with schema installation status
        """
        cda_path = self.target_dir / "CDA.xsd"
        schema_files = list(self.target_dir.glob("*.xsd"))

        return {
            "installed": cda_path.exists(),
            "schema_dir": str(self.target_dir),
            "cda_schema": str(cda_path),
            "cda_exists": cda_path.exists(),
            "schema_count": len(schema_files),
            "files": [f.name for f in schema_files],
        }

    def print_installation_instructions(self) -> None:
        """Print instructions for manually downloading schemas."""
        instructions = f"""
C-CDA XSD Schema Installation Instructions
==========================================

The C-CDA XSD schemas are required for structural validation.

Method 1: Automatic Download (Recommended)
------------------------------------------
Run the following command to automatically download schemas:

    ccdakit install-schemas

Or use the Python API:

    >>> from ccdakit.validators.xsd_downloader import XSDDownloader
    >>> downloader = XSDDownloader()
    >>> success, message = downloader.download_schemas()
    >>> print(message)

Method 2: Manual Download
-------------------------
1. Visit: https://github.com/HL7/CDA-core-xsd
2. Download the repository as ZIP
3. Extract all *.xsd files to: {self.target_dir}

Required Files:
--------------
- CDA.xsd (main schema file)
- datatypes.xsd
- datatypes-base.xsd
- NarrativeBlock.xsd
- voc.xsd
- And other related XSD files

Verification
------------
After installation, verify schemas are available:

    >>> downloader = XSDDownloader()
    >>> info = downloader.get_schema_info()
    >>> print(f"Installed: {{info['installed']}}")
    >>> print(f"Schema count: {{info['schema_count']}}")
"""
        print(instructions)
