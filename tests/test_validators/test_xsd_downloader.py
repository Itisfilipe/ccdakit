"""Comprehensive tests for XSD downloader."""

import shutil
import urllib.error
import zipfile
from unittest.mock import patch

import pytest

from ccdakit.validators.xsd_downloader import XSDDownloader


class TestXSDDownloader:
    """Test suite for XSDDownloader."""

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create a temporary directory for testing."""
        test_dir = tmp_path / "test_schemas"
        test_dir.mkdir(exist_ok=True)
        return test_dir

    @pytest.fixture
    def downloader(self, temp_dir):
        """Create downloader with temporary directory."""
        return XSDDownloader(target_dir=temp_dir)

    @pytest.fixture
    def mock_xsd_zip(self, temp_dir):
        """Create a mock XSD zip file with realistic structure."""
        # Create temporary directory structure like actual HL7 repo
        repo_dir = temp_dir / "mock_repo" / "CDA-core-sd-master"
        repo_dir.mkdir(parents=True, exist_ok=True)

        # Create mock XSD files
        xsd_files = [
            "CDA.xsd",
            "datatypes.xsd",
            "datatypes-base.xsd",
            "NarrativeBlock.xsd",
            "voc.xsd",
        ]

        for xsd_file in xsd_files:
            xsd_path = repo_dir / xsd_file
            xsd_content = f'<?xml version="1.0"?><schema name="{xsd_file}"/>'
            xsd_path.write_text(xsd_content)

        # Create zip file
        zip_path = temp_dir / "test_schemas.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            for xsd_file in xsd_files:
                xsd_path = repo_dir / xsd_file
                arcname = f"CDA-core-sd-master/{xsd_file}"
                zf.write(xsd_path, arcname=arcname)

        return zip_path

    def test_init_default_directory(self):
        """Test initializing with default directory."""
        downloader = XSDDownloader()
        assert downloader.target_dir.exists()
        assert downloader.target_dir.name == "schemas"

    def test_init_custom_directory(self, temp_dir):
        """Test initializing with custom directory."""
        downloader = XSDDownloader(target_dir=temp_dir)
        assert downloader.target_dir == temp_dir
        assert temp_dir.exists()

    def test_init_creates_directory(self, tmp_path):
        """Test that initialization creates target directory if it doesn't exist."""
        new_dir = tmp_path / "new" / "nested" / "dir"
        assert not new_dir.exists()

        downloader = XSDDownloader(target_dir=new_dir)
        assert new_dir.exists()
        assert downloader.target_dir == new_dir

    def test_is_installed_when_not_installed(self, downloader):
        """Test is_installed returns False when CDA.xsd doesn't exist."""
        assert not downloader.is_installed()

    def test_is_installed_when_installed(self, downloader, temp_dir):
        """Test is_installed returns True when CDA.xsd exists."""
        cda_path = temp_dir / "CDA.xsd"
        cda_path.write_text('<?xml version="1.0"?><schema/>')

        assert downloader.is_installed()

    def test_download_schemas_already_installed(self, downloader, temp_dir):
        """Test download returns success when schemas already installed."""
        # Create CDA.xsd to simulate installed schemas
        cda_path = temp_dir / "CDA.xsd"
        cda_path.write_text('<?xml version="1.0"?><schema/>')

        success, message = downloader.download_schemas(force=False)

        assert success is True
        assert "already installed" in message

    def test_download_schemas_force_redownload(self, downloader, temp_dir, mock_xsd_zip):
        """Test force download even when schemas exist."""
        # Create existing CDA.xsd
        cda_path = temp_dir / "CDA.xsd"
        cda_path.write_text('<?xml version="1.0"?><old schema/>')

        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = lambda url, path: shutil.copy(mock_xsd_zip, path)

            success, message = downloader.download_schemas(force=True)

            assert success is True
            assert "successfully" in message
            assert mock_retrieve.called

    def test_download_schemas_success(self, downloader, mock_xsd_zip):
        """Test successful schema download and extraction."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = lambda url, path: shutil.copy(mock_xsd_zip, path)

            success, message = downloader.download_schemas()

            assert success is True
            assert "successfully" in message
            assert downloader.is_installed()
            assert (downloader.target_dir / "CDA.xsd").exists()
            assert (downloader.target_dir / "datatypes.xsd").exists()

    def test_download_schemas_network_error(self, downloader):
        """Test handling of network errors during download."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = urllib.error.URLError("Network error")

            success, message = downloader.download_schemas()

            assert success is False
            assert "Failed to download" in message
            assert "Network error" in message

    def test_download_schemas_http_404_error(self, downloader):
        """Test handling of HTTP 404 errors."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = urllib.error.HTTPError(
                "http://test.com", 404, "Not Found", {}, None
            )

            success, message = downloader.download_schemas()

            assert success is False
            assert "Failed to download" in message

    def test_download_schemas_http_500_error(self, downloader):
        """Test handling of HTTP 500 server errors."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = urllib.error.HTTPError(
                "http://test.com", 500, "Server Error", {}, None
            )

            success, message = downloader.download_schemas()

            assert success is False
            assert "Failed to download" in message

    def test_download_schemas_timeout_error(self, downloader):
        """Test handling of timeout errors."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            import socket

            mock_retrieve.side_effect = socket.timeout("Connection timeout")

            success, message = downloader.download_schemas()

            assert success is False
            assert "Failed to download" in message

    def test_download_schemas_corrupted_zip(self, downloader, temp_dir):
        """Test handling of corrupted ZIP file."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            # Create corrupted zip file
            corrupted_zip = temp_dir / "corrupted.zip"
            corrupted_zip.write_text("This is not a valid zip file")

            mock_retrieve.side_effect = lambda url, path: shutil.copy(corrupted_zip, path)

            success, message = downloader.download_schemas()

            assert success is False
            assert "Failed to extract" in message

    def test_download_schemas_missing_extracted_directory(self, downloader, temp_dir):
        """Test handling when extracted directory structure is unexpected."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            # Create zip with wrong structure (no CDA-core-sd-master directory)
            wrong_zip = temp_dir / "wrong.zip"
            with zipfile.ZipFile(wrong_zip, "w") as zf:
                zf.writestr("some_other_dir/file.txt", "content")

            mock_retrieve.side_effect = lambda url, path: shutil.copy(wrong_zip, path)

            success, message = downloader.download_schemas()

            assert success is False
            assert "Failed to find extracted schema files" in message

    def test_download_schemas_missing_cda_xsd(self, downloader, temp_dir):
        """Test handling when CDA.xsd is not in the extracted files."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            # Create zip without CDA.xsd
            incomplete_zip = temp_dir / "incomplete.zip"
            repo_dir = temp_dir / "incomplete_repo" / "CDA-core-sd-master"
            repo_dir.mkdir(parents=True, exist_ok=True)

            # Create only one XSD file (not CDA.xsd)
            (repo_dir / "datatypes.xsd").write_text('<?xml version="1.0"?><schema/>')

            with zipfile.ZipFile(incomplete_zip, "w") as zf:
                zf.write(repo_dir / "datatypes.xsd", arcname="CDA-core-sd-master/datatypes.xsd")

            mock_retrieve.side_effect = lambda url, path: shutil.copy(incomplete_zip, path)

            success, message = downloader.download_schemas()

            assert success is False
            assert "CDA.xsd not found" in message

    def test_download_schemas_cleans_up_temp_on_success(self, downloader, mock_xsd_zip):
        """Test that temporary files are cleaned up after successful download."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = lambda url, path: shutil.copy(mock_xsd_zip, path)

            success, message = downloader.download_schemas()

            assert success is True
            # Temp directory should be cleaned up
            assert not (downloader.target_dir / "temp").exists()
            # Temp zip should be cleaned up
            assert not (downloader.target_dir / "schemas_temp.zip").exists()

    def test_download_schemas_cleans_up_temp_on_error(self, downloader, temp_dir):
        """Test that temporary files are cleaned up after extraction error."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            # Create corrupted zip
            corrupted_zip = temp_dir / "corrupted.zip"
            corrupted_zip.write_text("corrupted")

            mock_retrieve.side_effect = lambda url, path: shutil.copy(corrupted_zip, path)

            success, message = downloader.download_schemas()

            assert success is False
            # Temp files should still be cleaned up
            assert not (downloader.target_dir / "schemas_temp.zip").exists()

    def test_download_schemas_disk_full_error(self, downloader):
        """Test handling of disk full errors during download."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = OSError("No space left on device")

            success, message = downloader.download_schemas()

            assert success is False
            assert "Failed to download" in message

    def test_download_schemas_permission_error(self, downloader):
        """Test handling of permission errors during file operations."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = PermissionError("Permission denied")

            success, message = downloader.download_schemas()

            assert success is False
            assert "Failed to download" in message

    def test_cleanup_temp_dir_nonexistent(self, downloader, temp_dir):
        """Test cleanup of non-existent temp directory."""
        temp_dir_path = temp_dir / "nonexistent"
        assert not temp_dir_path.exists()

        # Should not raise error
        downloader._cleanup_temp_dir(temp_dir_path)

    def test_cleanup_temp_dir_success(self, downloader, temp_dir):
        """Test successful cleanup of temp directory."""
        temp_subdir = temp_dir / "temp_cleanup_test"
        temp_subdir.mkdir()
        (temp_subdir / "file.txt").write_text("content")
        (temp_subdir / "nested").mkdir()
        (temp_subdir / "nested" / "file2.txt").write_text("content2")

        assert temp_subdir.exists()

        downloader._cleanup_temp_dir(temp_subdir)

        assert not temp_subdir.exists()

    def test_cleanup_temp_dir_permission_error(self, downloader, temp_dir, caplog):
        """Test cleanup handles permission errors gracefully."""
        temp_subdir = temp_dir / "temp_permission_test"
        temp_subdir.mkdir()

        with patch("shutil.rmtree") as mock_rmtree:
            mock_rmtree.side_effect = PermissionError("Permission denied")

            # Should not raise, just log warning
            downloader._cleanup_temp_dir(temp_subdir)

            assert mock_rmtree.called

    def test_get_schema_info_not_installed(self, downloader):
        """Test get_schema_info when schemas not installed."""
        info = downloader.get_schema_info()

        assert info["installed"] is False
        assert info["cda_exists"] is False
        assert info["schema_count"] == 0
        assert len(info["files"]) == 0
        assert "schema_dir" in info
        assert "cda_schema" in info

    def test_get_schema_info_installed(self, downloader, temp_dir):
        """Test get_schema_info when schemas are installed."""
        # Create mock XSD files
        (temp_dir / "CDA.xsd").write_text("schema1")
        (temp_dir / "datatypes.xsd").write_text("schema2")
        (temp_dir / "voc.xsd").write_text("schema3")

        info = downloader.get_schema_info()

        assert info["installed"] is True
        assert info["cda_exists"] is True
        assert info["schema_count"] == 3
        assert "CDA.xsd" in info["files"]
        assert "datatypes.xsd" in info["files"]
        assert "voc.xsd" in info["files"]

    def test_get_schema_info_partial_installation(self, downloader, temp_dir):
        """Test get_schema_info with only some schemas installed."""
        # Create only datatypes.xsd (no CDA.xsd)
        (temp_dir / "datatypes.xsd").write_text("schema")

        info = downloader.get_schema_info()

        assert info["installed"] is False  # CDA.xsd is missing
        assert info["cda_exists"] is False
        assert info["schema_count"] == 1

    def test_print_installation_instructions(self, downloader, caplog):
        """Test print_installation_instructions outputs helpful text."""
        import logging

        caplog.set_level(logging.INFO)

        downloader.print_installation_instructions()

        # Check that instructions were logged
        assert any("Installation Instructions" in record.message for record in caplog.records)
        assert any("CDA.xsd" in record.message for record in caplog.records)
        assert any("github.com" in record.message for record in caplog.records)

    def test_schema_url_constant(self):
        """Test that schema URL constants are properly set."""
        assert XSDDownloader.BASE_URL.startswith("https://")
        assert "github.com" in XSDDownloader.BASE_URL
        assert "HL7" in XSDDownloader.SCHEMA_ZIP_URL

    def test_concurrent_download_attempts(self, downloader, mock_xsd_zip):
        """Test handling of concurrent download attempts."""
        import threading

        results = []

        def download_thread():
            with patch("urllib.request.urlretrieve") as mock_retrieve:
                mock_retrieve.side_effect = lambda url, path: shutil.copy(mock_xsd_zip, path)
                success, message = downloader.download_schemas()
                results.append((success, message))

        # Start multiple threads
        threads = [threading.Thread(target=download_thread) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # At least one should succeed
        assert any(success for success, _ in results)

    def test_download_with_nested_xsd_files(self, downloader, temp_dir):
        """Test extraction of XSD files from nested directories."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            # Create zip with nested structure
            nested_zip = temp_dir / "nested.zip"
            repo_dir = temp_dir / "nested_repo" / "CDA-core-sd-master"
            repo_dir.mkdir(parents=True, exist_ok=True)

            # Create XSD in subdirectory
            subdir = repo_dir / "schemas" / "nested"
            subdir.mkdir(parents=True, exist_ok=True)
            (subdir / "CDA.xsd").write_text('<?xml version="1.0"?><schema/>')
            (subdir / "datatypes.xsd").write_text('<?xml version="1.0"?><schema/>')

            with zipfile.ZipFile(nested_zip, "w") as zf:
                zf.write(subdir / "CDA.xsd", arcname="CDA-core-sd-master/schemas/nested/CDA.xsd")
                zf.write(
                    subdir / "datatypes.xsd",
                    arcname="CDA-core-sd-master/schemas/nested/datatypes.xsd",
                )

            mock_retrieve.side_effect = lambda url, path: shutil.copy(nested_zip, path)

            success, message = downloader.download_schemas()

            # Should successfully extract nested XSD files
            assert success is True
            assert downloader.is_installed()

    def test_download_schemas_exception_in_outer_try(self, downloader):
        """Test exception handling in outer try block."""
        with patch.object(downloader, "is_installed") as mock_is_installed:
            mock_is_installed.side_effect = RuntimeError("Unexpected error")

            success, message = downloader.download_schemas()

            assert success is False
            assert "Failed to download" in message

    def test_download_empty_zip_file(self, downloader, temp_dir):
        """Test handling of empty ZIP file."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            # Create empty zip
            empty_zip = temp_dir / "empty.zip"
            with zipfile.ZipFile(empty_zip, "w"):
                pass  # Empty zip

            mock_retrieve.side_effect = lambda url, path: shutil.copy(empty_zip, path)

            success, message = downloader.download_schemas()

            assert success is False
            assert "Failed to find extracted schema files" in message

    def test_partial_extraction_cleanup(self, downloader, temp_dir):
        """Test cleanup when extraction partially succeeds then fails."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            # Create a zip that will extract but won't have the right structure
            partial_zip = temp_dir / "partial.zip"
            with zipfile.ZipFile(partial_zip, "w") as zf:
                zf.writestr("CDA-core-sd-master/some_file.txt", "content")

            mock_retrieve.side_effect = lambda url, path: shutil.copy(partial_zip, path)

            success, message = downloader.download_schemas()

            assert success is False
            # Verify cleanup happened
            assert not (downloader.target_dir / "schemas_temp.zip").exists()
            assert not (downloader.target_dir / "temp").exists()

    def test_download_with_special_characters_in_path(self, tmp_path):
        """Test download with special characters in target path."""
        special_dir = tmp_path / "test dir with spaces & special-chars"
        downloader = XSDDownloader(target_dir=special_dir)

        assert downloader.target_dir.exists()
        assert downloader.target_dir == special_dir
