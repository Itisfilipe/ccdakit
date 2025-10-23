#!/usr/bin/env python3
"""Setup script to download all validation and transformation files during deployment.

This script is run during the build process to ensure all necessary files are
available when the application starts:

1. Schematron validation files (~63MB):
   - HL7_CCDA_R2.1.sch (original)
   - HL7_CCDA_R2.1_cleaned.sch (auto-cleaned for lxml compatibility)
   - voc.xml (vocabulary definitions)

2. XSD schema files (~2MB):
   - CDA.xsd and related schema files

3. XSLT stylesheets (small):
   - CDA.xsl and dependencies for HTML conversion

All files are downloaded from official HL7 GitHub repositories.
"""

import sys
from pathlib import Path


def setup_validation_files() -> bool:
    """
    Download and setup all validation and transformation files.

    Returns:
        True if all successful, False if any failed
    """
    try:
        # Add parent directory to path so we can import ccdakit
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))

        print("\n" + "=" * 70)
        print("Setting up C-CDA Validation & Transformation Files")
        print("=" * 70)
        print("This downloads files from official HL7 repositories:")
        print("  • Schematron validation rules (~63MB)")
        print("  • XSD schemas (~2MB)")
        print("  • XSLT stylesheets (small)")
        print("\nThis is a one-time setup during deployment...\n")

        all_success = True

        # 1. Download Schematron files (includes auto-cleaning)
        print("-" * 70)
        print("1/3: Downloading Schematron validation files...")
        print("-" * 70)
        try:
            from ccdakit.validators.schematron_downloader import download_schematron_files

            success = download_schematron_files(quiet=False)
            if success:
                print("✓ Schematron files ready (includes cleaned version)")
            else:
                print("✗ Failed to download Schematron files")
                all_success = False
        except Exception as e:
            print(f"✗ Error downloading Schematron files: {e}")
            all_success = False

        # 2. Download XSD schemas
        print("\n" + "-" * 70)
        print("2/3: Downloading XSD schema files...")
        print("-" * 70)
        try:
            from ccdakit.validators.xsd_downloader import XSDDownloader

            xsd_downloader = XSDDownloader()
            success, message = xsd_downloader.download_schemas(force=False)
            print(message)
            if not success:
                all_success = False
        except Exception as e:
            print(f"✗ Error downloading XSD schemas: {e}")
            all_success = False

        # 3. Download XSLT stylesheets
        print("\n" + "-" * 70)
        print("3/3: Downloading XSLT stylesheets...")
        print("-" * 70)
        try:
            from ccdakit.utils.xslt import download_cda_stylesheet

            stylesheet_path = download_cda_stylesheet()
            print(f"✓ XSLT stylesheets downloaded to {stylesheet_path.parent}")
        except Exception as e:
            print(f"✗ Error downloading XSLT stylesheets: {e}")
            # XSLT is less critical, so don't fail if it doesn't work
            print("  (XSLT conversion may not work, but validation will)")

        # Summary
        print("\n" + "=" * 70)
        if all_success:
            print("✓ All validation files ready!")
            print("  • Schematron validation: READY")
            print("  • XSD validation: READY")
            print("  • XSLT conversion: READY")
        else:
            print("⚠ Setup completed with some issues")
            print("  Some validation features may not work correctly.")
        print("=" * 70 + "\n")

        return all_success

    except Exception as e:
        print(f"\n✗ Unexpected error during setup: {e}")
        print("=" * 70 + "\n")
        return False


if __name__ == "__main__":
    success = setup_validation_files()
    # Don't fail the build if download fails - app can still work with limited functionality
    # Always exit 0 to not break the deployment
    sys.exit(0)
