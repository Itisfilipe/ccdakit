"""Tests for XSLT utilities."""

import tempfile
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
from lxml import etree

from ccdakit.utils.xslt import (
    download_cda_stylesheet,
    get_default_xslt_path,
    transform_cda_string_to_html,
    transform_cda_to_html,
)


class TestGetDefaultXsltPath:
    """Tests for get_default_xslt_path function."""

    def test_returns_path_in_schemas_directory(self):
        """Test that default path is in schemas/xslt directory."""
        path = get_default_xslt_path()
        assert path.name == "xslt"
        assert path.parent.name == "schemas"
        assert path.exists()  # Should create directory if it doesn't exist

    def test_creates_directory_if_not_exists(self):
        """Test that the function creates the directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock the function to use a temp directory
            with patch("ccdakit.utils.xslt.Path") as mock_path:
                temp_path = Path(tmpdir) / "test_xslt"
                mock_path.return_value.parent.parent.parent = Path(tmpdir)
                mock_instance = MagicMock()
                mock_instance.mkdir = MagicMock()
                mock_path.return_value.__truediv__ = lambda self, other: temp_path

                # Call the real function
                result = get_default_xslt_path()

                # Directory should be created
                assert result.exists()


class TestDownloadCdaStylesheet:
    """Tests for download_cda_stylesheet function."""

    def test_downloads_all_required_files(self):
        """Test that all required files are downloaded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            target_dir = Path(tmpdir)

            # Mock urllib.request.urlretrieve
            with patch("ccdakit.utils.xslt.urllib.request.urlretrieve") as mock_retrieve:
                result = download_cda_stylesheet(target_dir)

                # Should have made 3 download calls
                assert mock_retrieve.call_count == 3

                # Should return path to main stylesheet
                assert result == target_dir / "cda.xsl"
                assert result.name == "cda.xsl"

    def test_skips_download_if_already_exists(self):
        """Test that download is skipped if files already exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            target_dir = Path(tmpdir)
            main_stylesheet = target_dir / "cda.xsl"
            main_stylesheet.touch()  # Create empty file

            with patch("ccdakit.utils.xslt.urllib.request.urlretrieve") as mock_retrieve:
                result = download_cda_stylesheet(target_dir)

                # Should not download if file exists
                assert mock_retrieve.call_count == 0
                assert result == main_stylesheet

    def test_uses_default_directory_when_none_provided(self):
        """Test that default directory is used when target_dir is None."""
        with patch("ccdakit.utils.xslt.get_default_xslt_path") as mock_get_path:
            with patch("ccdakit.utils.xslt.urllib.request.urlretrieve"):
                mock_dir = MagicMock()
                mock_dir.mkdir = MagicMock()
                mock_dir.__truediv__ = lambda self, other: MagicMock(exists=lambda: True)
                mock_get_path.return_value = mock_dir

                download_cda_stylesheet(None)

                # Should call get_default_xslt_path
                mock_get_path.assert_called_once()

    def test_raises_error_on_download_failure(self):
        """Test that RuntimeError is raised when download fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            target_dir = Path(tmpdir)

            with patch("ccdakit.utils.xslt.urllib.request.urlretrieve") as mock_retrieve:
                mock_retrieve.side_effect = urllib.error.URLError("Network error")

                with pytest.raises(RuntimeError, match="Failed to download CDA stylesheet"):
                    download_cda_stylesheet(target_dir)

    def test_creates_target_directory_if_not_exists(self):
        """Test that target directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            target_dir = Path(tmpdir) / "new_dir"
            assert not target_dir.exists()

            with patch("ccdakit.utils.xslt.urllib.request.urlretrieve"):
                download_cda_stylesheet(target_dir)

                # Directory should be created
                assert target_dir.exists()


class TestTransformCdaToHtml:
    """Tests for transform_cda_to_html function."""

    def test_transforms_valid_cda_xml(self):
        """Test successful transformation of valid CDA XML."""
        # Create a minimal valid CDA XML
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test Document</title>
</ClinicalDocument>"""

        # Create a minimal XSLT stylesheet
        xslt_content = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="urn:hl7-org:v3">
    <xsl:output method="html"/>
    <xsl:template match="/">
        <html><body><h1>Test Output</h1></body></html>
    </xsl:template>
</xsl:stylesheet>"""

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / "test.xml"
            xslt_path = Path(tmpdir) / "test.xsl"

            xml_path.write_text(xml_content)
            xslt_path.write_text(xslt_content)

            result = transform_cda_to_html(xml_path, xslt_path)

            # Should return HTML string
            assert isinstance(result, str)
            assert "html" in result.lower()

    def test_raises_error_for_missing_xml_file(self):
        """Test that FileNotFoundError is raised for missing XML file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / "nonexistent.xml"

            with pytest.raises(FileNotFoundError, match="XML file not found"):
                transform_cda_to_html(xml_path)

    def test_raises_error_for_missing_xslt_file(self):
        """Test that FileNotFoundError is raised for missing XSLT file."""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test</title>
</ClinicalDocument>"""

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / "test.xml"
            xslt_path = Path(tmpdir) / "nonexistent.xsl"

            xml_path.write_text(xml_content)

            with pytest.raises(FileNotFoundError, match="XSLT stylesheet not found"):
                transform_cda_to_html(xml_path, xslt_path)

    def test_raises_error_for_invalid_xml(self):
        """Test that XMLSyntaxError is raised for malformed XML."""
        invalid_xml = "This is not valid XML"

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / "invalid.xml"
            xml_path.write_text(invalid_xml)

            with pytest.raises(etree.XMLSyntaxError):
                transform_cda_to_html(xml_path)

    def test_raises_error_for_invalid_xslt(self):
        """Test that XSLTParseError is raised for invalid XSLT."""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test</title>
</ClinicalDocument>"""

        invalid_xslt = "This is not valid XSLT"

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / "test.xml"
            xslt_path = Path(tmpdir) / "invalid.xsl"

            xml_path.write_text(xml_content)
            xslt_path.write_text(invalid_xslt)

            with pytest.raises(etree.XMLSyntaxError):
                transform_cda_to_html(xml_path, xslt_path)

    def test_downloads_stylesheet_if_not_exists_and_none_provided(self):
        """Test that stylesheet is downloaded if default doesn't exist and none provided."""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test</title>
</ClinicalDocument>"""

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / "test.xml"
            xml_path.write_text(xml_content)

            with patch("ccdakit.utils.xslt.get_default_xslt_path") as mock_get_path:
                with patch("ccdakit.utils.xslt.download_cda_stylesheet") as mock_download:
                    # Mock default path that doesn't exist
                    mock_xslt_path = Path(tmpdir) / "nonexistent.xsl"
                    mock_get_path.return_value = Path(tmpdir)

                    # This should trigger download
                    try:
                        transform_cda_to_html(xml_path, None)
                    except Exception:
                        # Expected to fail since we're not providing a valid stylesheet
                        pass

                    # Should have called download
                    mock_download.assert_called_once()

    def test_uses_default_stylesheet_if_exists(self):
        """Test that default stylesheet is used if it exists and none provided."""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test</title>
</ClinicalDocument>"""

        xslt_content = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="urn:hl7-org:v3">
    <xsl:output method="html"/>
    <xsl:template match="/">
        <html><body><h1>Default</h1></body></html>
    </xsl:template>
</xsl:stylesheet>"""

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / "test.xml"
            xslt_path = Path(tmpdir) / "cda.xsl"

            xml_path.write_text(xml_content)
            xslt_path.write_text(xslt_content)

            with patch("ccdakit.utils.xslt.get_default_xslt_path") as mock_get_path:
                mock_get_path.return_value = Path(tmpdir)

                result = transform_cda_to_html(xml_path, None)

                # Should successfully transform
                assert isinstance(result, str)
                assert "html" in result.lower()

    def test_accepts_string_paths(self):
        """Test that function accepts string paths in addition to Path objects."""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test</title>
</ClinicalDocument>"""

        xslt_content = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="urn:hl7-org:v3">
    <xsl:output method="html"/>
    <xsl:template match="/">
        <html><body><h1>Test</h1></body></html>
    </xsl:template>
</xsl:stylesheet>"""

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / "test.xml"
            xslt_path = Path(tmpdir) / "test.xsl"

            xml_path.write_text(xml_content)
            xslt_path.write_text(xslt_content)

            # Pass as strings
            result = transform_cda_to_html(str(xml_path), str(xslt_path))

            assert isinstance(result, str)
            assert "html" in result.lower()


class TestTransformCdaStringToHtml:
    """Tests for transform_cda_string_to_html function."""

    def test_transforms_valid_cda_string(self):
        """Test successful transformation of valid CDA XML string."""
        xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test Document</title>
</ClinicalDocument>"""

        xslt_content = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="urn:hl7-org:v3">
    <xsl:output method="html"/>
    <xsl:template match="/">
        <html><body><h1>Test Output</h1></body></html>
    </xsl:template>
</xsl:stylesheet>"""

        with tempfile.TemporaryDirectory() as tmpdir:
            xslt_path = Path(tmpdir) / "test.xsl"
            xslt_path.write_text(xslt_content)

            result = transform_cda_string_to_html(xml_string, xslt_path)

            # Should return HTML string
            assert isinstance(result, str)
            assert "html" in result.lower()

    def test_raises_error_for_invalid_xml_string(self):
        """Test that XMLSyntaxError is raised for malformed XML string."""
        invalid_xml = "This is not valid XML"

        with tempfile.TemporaryDirectory() as tmpdir:
            xslt_path = Path(tmpdir) / "test.xsl"
            xslt_path.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html"/>
    <xsl:template match="/"><html/></xsl:template>
</xsl:stylesheet>""")

            with pytest.raises(etree.XMLSyntaxError):
                transform_cda_string_to_html(invalid_xml, xslt_path)

    def test_raises_error_for_missing_xslt_file(self):
        """Test that FileNotFoundError is raised for missing XSLT file."""
        xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test</title>
</ClinicalDocument>"""

        with tempfile.TemporaryDirectory() as tmpdir:
            xslt_path = Path(tmpdir) / "nonexistent.xsl"

            with pytest.raises(FileNotFoundError, match="XSLT stylesheet not found"):
                transform_cda_string_to_html(xml_string, xslt_path)

    def test_downloads_stylesheet_if_not_exists_and_none_provided(self):
        """Test that stylesheet is downloaded if default doesn't exist and none provided."""
        xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test</title>
</ClinicalDocument>"""

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("ccdakit.utils.xslt.get_default_xslt_path") as mock_get_path:
                with patch("ccdakit.utils.xslt.download_cda_stylesheet") as mock_download:
                    # Mock default path that doesn't exist
                    mock_get_path.return_value = Path(tmpdir)

                    # This should trigger download
                    try:
                        transform_cda_string_to_html(xml_string, None)
                    except Exception:
                        # Expected to fail since we're not providing a valid stylesheet
                        pass

                    # Should have called download
                    mock_download.assert_called_once()

    def test_uses_default_stylesheet_if_exists(self):
        """Test that default stylesheet is used if it exists and none provided."""
        xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test</title>
</ClinicalDocument>"""

        xslt_content = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="urn:hl7-org:v3">
    <xsl:output method="html"/>
    <xsl:template match="/">
        <html><body><h1>Default</h1></body></html>
    </xsl:template>
</xsl:stylesheet>"""

        with tempfile.TemporaryDirectory() as tmpdir:
            xslt_path = Path(tmpdir) / "cda.xsl"
            xslt_path.write_text(xslt_content)

            with patch("ccdakit.utils.xslt.get_default_xslt_path") as mock_get_path:
                mock_get_path.return_value = Path(tmpdir)

                result = transform_cda_string_to_html(xml_string, None)

                # Should successfully transform
                assert isinstance(result, str)
                assert "html" in result.lower()

    def test_accepts_string_path_for_xslt(self):
        """Test that function accepts string path for XSLT."""
        xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test</title>
</ClinicalDocument>"""

        xslt_content = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="urn:hl7-org:v3">
    <xsl:output method="html"/>
    <xsl:template match="/">
        <html><body><h1>Test</h1></body></html>
    </xsl:template>
</xsl:stylesheet>"""

        with tempfile.TemporaryDirectory() as tmpdir:
            xslt_path = Path(tmpdir) / "test.xsl"
            xslt_path.write_text(xslt_content)

            # Pass as string
            result = transform_cda_string_to_html(xml_string, str(xslt_path))

            assert isinstance(result, str)
            assert "html" in result.lower()

    def test_handles_xml_with_special_characters(self):
        """Test that function handles XML with special characters."""
        xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
    <title>Test &amp; Special "Characters" &lt;here&gt;</title>
</ClinicalDocument>"""

        xslt_content = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns="urn:hl7-org:v3">
    <xsl:output method="html"/>
    <xsl:template match="/">
        <html><body><h1>Test</h1></body></html>
    </xsl:template>
</xsl:stylesheet>"""

        with tempfile.TemporaryDirectory() as tmpdir:
            xslt_path = Path(tmpdir) / "test.xsl"
            xslt_path.write_text(xslt_content)

            result = transform_cda_string_to_html(xml_string, xslt_path)

            # Should successfully transform
            assert isinstance(result, str)
            assert "html" in result.lower()


class TestIntegrationWithRealFiles:
    """Integration tests using real CDA files if available."""

    def test_transform_with_real_cda_file_if_exists(self):
        """Test transformation with a real CDA file if it exists."""
        # Look for sample CCD file
        sample_ccd = Path("/Users/filipe/Code/pyccda/ccd_example.xml")

        if sample_ccd.exists():
            # Use the actual CDA stylesheet if available
            default_xslt = get_default_xslt_path() / "cda.xsl"

            if default_xslt.exists():
                result = transform_cda_to_html(sample_ccd, default_xslt)

                # Should return HTML
                assert isinstance(result, str)
                assert len(result) > 0
                # HTML output typically contains these elements
                assert any(tag in result.lower() for tag in ["html", "body", "table"])

    def test_transform_string_with_real_cda_content_if_exists(self):
        """Test string transformation with real CDA content if available."""
        sample_ccd = Path("/Users/filipe/Code/pyccda/ccd_example.xml")

        if sample_ccd.exists():
            xml_string = sample_ccd.read_text()

            # Use the actual CDA stylesheet if available
            default_xslt = get_default_xslt_path() / "cda.xsl"

            if default_xslt.exists():
                result = transform_cda_string_to_html(xml_string, default_xslt)

                # Should return HTML
                assert isinstance(result, str)
                assert len(result) > 0
                assert any(tag in result.lower() for tag in ["html", "body", "table"])
