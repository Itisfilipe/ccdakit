"""Utility for downloading C-CDA Schematron validation files."""

import logging
import urllib.request
from pathlib import Path
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class SchematronDownloader:
    """
    Downloads C-CDA Schematron validation files from HL7 GitHub repository.

    The files are large (HL7_CCDA_R2.1.sch ~1MB, voc.xml ~62MB) so they are
    not included in the package. This utility downloads them on-demand.
    """

    # Official HL7 C-CDA Schematron repository
    BASE_URL = "https://raw.githubusercontent.com/HL7/CDA-ccda-2.1/master/validation"

    FILES = {
        "schematron": {
            "filename": "HL7_CCDA_R2.1.sch",
            "url": f"{BASE_URL}/Consolidated%20CDA%20Templates%20for%20Clinical%20Notes%20%28US%20Realm%29%20DSTU%20R2.1.sch",
            "size_mb": 1,
        },
        "vocabulary": {
            "filename": "voc.xml",
            "url": f"{BASE_URL}/voc.xml",
            "size_mb": 62,
        },
    }

    def __init__(self, target_dir: Optional[Path] = None):
        """
        Initialize downloader.

        Args:
            target_dir: Directory to download files to.
                If None, uses schemas/schematron/ relative to package root.
        """
        if target_dir is None:
            # Default to schemas/schematron in package
            package_root = Path(__file__).parent.parent.parent
            target_dir = package_root / "schemas" / "schematron"

        self.target_dir = Path(target_dir)
        self.target_dir.mkdir(parents=True, exist_ok=True)

    def download_schematron(self, force: bool = False) -> Tuple[bool, str]:
        """
        Download Schematron file.

        Args:
            force: Force download even if file exists

        Returns:
            Tuple of (success: bool, message: str)
        """
        return self._download_file("schematron", force)

    def download_vocabulary(self, force: bool = False) -> Tuple[bool, str]:
        """
        Download vocabulary file.

        Args:
            force: Force download even if file exists

        Returns:
            Tuple of (success: bool, message: str)
        """
        return self._download_file("vocabulary", force)

    def download_all(self, force: bool = False) -> Tuple[bool, str]:
        """
        Download both Schematron and vocabulary files.

        After downloading the Schematron file, automatically cleans it to fix
        IDREF errors that prevent lxml from loading it.

        Args:
            force: Force download even if files exist

        Returns:
            Tuple of (success: bool, message: str)
        """
        results = []

        # Download Schematron
        success_sch, msg_sch = self.download_schematron(force)
        results.append((success_sch, msg_sch))

        # Clean Schematron file if download succeeded
        if success_sch:
            try:
                clean_success, clean_msg = self._clean_schematron_file()
                results.append((clean_success, clean_msg))
            except Exception as e:
                logger.warning(f"Failed to clean Schematron file: {e}")
                results.append(
                    (
                        False,
                        f"⚠ Warning: Schematron file downloaded but cleaning failed: {e}",
                    )
                )

        # Download vocabulary
        success_voc, msg_voc = self.download_vocabulary(force)
        results.append((success_voc, msg_voc))

        # Combine results
        all_success = all(r[0] for r in results)
        messages = [r[1] for r in results]

        return all_success, "\n".join(messages)

    def are_files_present(self) -> bool:
        """
        Check if all required files are already downloaded.

        Returns:
            True if original Schematron, cleaned Schematron, and vocabulary files exist
        """
        schematron_path = self.get_schematron_path()
        cleaned_path = self.get_cleaned_schematron_path()
        vocabulary_path = self.get_vocabulary_path()

        return (
            schematron_path.exists()
            and cleaned_path.exists()
            and vocabulary_path.exists()
        )

    def _download_file(self, file_type: str, force: bool = False) -> Tuple[bool, str]:
        """
        Download a specific file.

        Args:
            file_type: Type of file ("schematron" or "vocabulary")
            force: Force download even if file exists

        Returns:
            Tuple of (success: bool, message: str)
        """
        file_info = self.FILES[file_type]
        target_path = self.target_dir / file_info["filename"]

        # Check if file already exists
        if target_path.exists() and not force:
            return True, f"✓ {file_info['filename']} already exists"

        try:
            # Download file
            print(f"Downloading {file_info['filename']} (~{file_info['size_mb']} MB)...")
            print(f"Source: {file_info['url']}")
            print(f"Target: {target_path}")

            urllib.request.urlretrieve(file_info["url"], target_path)

            file_size_mb = target_path.stat().st_size / (1024 * 1024)
            return True, f"✓ Downloaded {file_info['filename']} ({file_size_mb:.1f} MB)"

        except Exception as e:
            error_msg = (
                f"✗ Failed to download {file_info['filename']}: {e}\n"
                f"  You can download manually from:\n"
                f"  {file_info['url']}\n"
                f"  Save to: {target_path}"
            )
            return False, error_msg

    def get_schematron_path(self) -> Path:
        """Get path to Schematron file."""
        return self.target_dir / self.FILES["schematron"]["filename"]

    def get_vocabulary_path(self) -> Path:
        """Get path to vocabulary file."""
        return self.target_dir / self.FILES["vocabulary"]["filename"]

    def get_cleaned_schematron_path(self) -> Path:
        """Get path to cleaned Schematron file."""
        original_name = self.FILES["schematron"]["filename"]
        # Replace .sch with _cleaned.sch
        cleaned_name = original_name.replace(".sch", "_cleaned.sch")
        return self.target_dir / cleaned_name

    def _clean_schematron_file(self) -> Tuple[bool, str]:
        """
        Clean the Schematron file to fix IDREF errors.

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Import here to avoid circular dependency
            from .schematron_cleaner import clean_schematron_file

            schematron_path = self.get_schematron_path()
            cleaned_path = self.get_cleaned_schematron_path()

            # Clean the file
            output_path, stats = clean_schematron_file(
                schematron_path, output_path=cleaned_path, quiet=True
            )

            msg = (
                f"✓ Cleaned Schematron file: removed {stats['invalid_references']} "
                f"invalid pattern references"
            )
            return True, msg

        except Exception as e:
            return False, f"✗ Failed to clean Schematron file: {e}"


def download_schematron_files(
    target_dir: Optional[Path] = None,
    force: bool = False,
    quiet: bool = False,
) -> bool:
    """
    Convenience function to download Schematron files.

    Args:
        target_dir: Directory to download to (default: schemas/schematron/)
        force: Force download even if files exist
        quiet: Suppress output messages

    Returns:
        True if download succeeded or files already exist, False otherwise

    Example:
        >>> from ccdakit.validators import download_schematron_files
        >>> if download_schematron_files():
        ...     print("Schematron files ready!")
    """
    downloader = SchematronDownloader(target_dir)

    # Check if already present
    if downloader.are_files_present() and not force:
        if not quiet:
            print("✓ Schematron files already present")
        return True

    # Download
    success, message = downloader.download_all(force)

    if not quiet:
        print(message)

    return success
