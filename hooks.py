"""MkDocs hooks to preserve GitHub Pages configuration files."""

import shutil
from pathlib import Path


def on_post_build(config, **kwargs):
    """
    Copy GitHub Pages configuration files to the built site directory after build.

    This ensures:
    - Custom domain (docs.ccdakit.com) is preserved via CNAME
    - GitHub Pages doesn't process the site with Jekyll via .nojekyll
    """
    docs_dir = Path(config["docs_dir"])
    site_dir = Path(config["site_dir"])

    # Files to copy from docs to site directory
    files_to_copy = ["CNAME", ".nojekyll"]

    for filename in files_to_copy:
        source = docs_dir / filename
        dest = site_dir / filename

        if source.exists():
            shutil.copy2(source, dest)
            print(f"✓ Copied {filename} to {dest}")
        else:
            print(f"⚠ Warning: {filename} not found at {source}")
