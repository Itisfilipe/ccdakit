#!/usr/bin/env python3
"""Download XSD schemas during deployment build."""

import os
import sys
from pathlib import Path

# Add parent directory to path so we can import ccdakit
sys.path.insert(0, str(Path(__file__).parent.parent))

from ccdakit.validators.xsd_downloader import XSDDownloader


def main():
    """Download XSD schemas for deployment."""
    print("=" * 60, flush=True)
    print("Downloading XSD Schemas for Deployment", flush=True)
    print("=" * 60, flush=True)

    # Force download in CI/build environments
    is_build_env = os.environ.get('RENDER') or os.environ.get('CI')

    downloader = XSDDownloader()

    print(f"\nTarget directory: {downloader.target_dir}", flush=True)
    print(f"Directory exists: {downloader.target_dir.exists()}", flush=True)
    print(f"Already installed: {downloader.is_installed()}", flush=True)
    print(f"Build environment detected: {bool(is_build_env)}", flush=True)

    if downloader.is_installed() and not is_build_env:
        print("\n✓ XSD schemas already installed. Skipping download.", flush=True)
        info = downloader.get_schema_info()
        print(f"  - Schema count: {info['schema_count']}", flush=True)
        print(f"  - CDA.xsd exists: {info['cda_exists']}", flush=True)
        return 0

    if is_build_env:
        print("\n→ Build environment: Forcing fresh download...", flush=True)
    else:
        print("\n→ Downloading schemas...", flush=True)

    # Force download in build environments to ensure fresh schemas
    success, message = downloader.download_schemas(force=bool(is_build_env))

    if success:
        print(f"\n✓ {message}", flush=True)
        info = downloader.get_schema_info()
        print(f"\nInstalled schemas:", flush=True)
        print(f"  - Total files: {info['schema_count']}", flush=True)
        print(f"  - CDA.xsd: {info['cda_exists']}", flush=True)
        print(f"  - Directory: {info['schema_dir']}", flush=True)

        # List the actual files for verification
        if info['files']:
            print(f"\n  Files installed:", flush=True)
            for f in info['files']:
                print(f"    - {f}", flush=True)

        return 0
    else:
        msg = f"\n✗ Failed: {message}"
        print(msg, file=sys.stderr, flush=True)
        print(msg, flush=True)  # Also print to stdout for visibility
        return 1


if __name__ == "__main__":
    sys.exit(main())
