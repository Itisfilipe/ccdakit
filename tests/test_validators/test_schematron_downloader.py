"""Comprehensive tests for Schematron downloader."""

import urllib.error
from pathlib import Path
from unittest.mock import patch

import pytest

from ccdakit.validators.schematron_downloader import SchematronDownloader, download_schematron_files


class TestSchematronDownloader:
    """Test suite for SchematronDownloader."""

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create a temporary directory for testing."""
        test_dir = tmp_path / "test_schematron"
        test_dir.mkdir(exist_ok=True)
        return test_dir

    @pytest.fixture
    def downloader(self, temp_dir):
        """Create downloader with temporary directory."""
        return SchematronDownloader(target_dir=temp_dir)

    @pytest.fixture
    def mock_schematron_content(self):
        """Create mock Schematron file content."""
        return """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron">
    <pattern id="p-test">
        <rule context="/">
            <assert test="true()">Test assertion</assert>
        </rule>
    </pattern>
</schema>"""

    @pytest.fixture
    def mock_vocabulary_content(self):
        """Create mock vocabulary file content."""
        return """<?xml version="1.0" encoding="UTF-8"?>
<vocabulary>
    <valueset id="test">
        <code code="123" codeSystem="2.16.840.1.113883.6.96"/>
    </valueset>
</vocabulary>"""

    def test_init_default_directory(self):
        """Test initializing with default directory."""
        downloader = SchematronDownloader()
        assert downloader.target_dir.exists()
        assert downloader.target_dir.name == "schematron"

    def test_init_custom_directory(self, temp_dir):
        """Test initializing with custom directory."""
        downloader = SchematronDownloader(target_dir=temp_dir)
        assert downloader.target_dir == temp_dir
        assert temp_dir.exists()

    def test_init_creates_directory(self, tmp_path):
        """Test that initialization creates target directory if it doesn't exist."""
        new_dir = tmp_path / "new" / "nested" / "schematron"
        assert not new_dir.exists()

        downloader = SchematronDownloader(target_dir=new_dir)
        assert new_dir.exists()
        assert downloader.target_dir == new_dir

    def test_files_configuration(self):
        """Test that FILES configuration is properly set."""
        assert "schematron" in SchematronDownloader.FILES
        assert "vocabulary" in SchematronDownloader.FILES
        assert "filename" in SchematronDownloader.FILES["schematron"]
        assert "url" in SchematronDownloader.FILES["schematron"]
        assert SchematronDownloader.FILES["schematron"]["filename"] == "HL7_CCDA_R2.1.sch"
        assert SchematronDownloader.FILES["vocabulary"]["filename"] == "voc.xml"

    def test_get_schematron_path(self, downloader):
        """Test get_schematron_path returns correct path."""
        expected_path = downloader.target_dir / "HL7_CCDA_R2.1.sch"
        assert downloader.get_schematron_path() == expected_path

    def test_get_vocabulary_path(self, downloader):
        """Test get_vocabulary_path returns correct path."""
        expected_path = downloader.target_dir / "voc.xml"
        assert downloader.get_vocabulary_path() == expected_path

    def test_get_cleaned_schematron_path(self, downloader):
        """Test get_cleaned_schematron_path returns correct path."""
        expected_path = downloader.target_dir / "HL7_CCDA_R2.1_cleaned.sch"
        assert downloader.get_cleaned_schematron_path() == expected_path

    def test_are_files_present_none_exist(self, downloader):
        """Test are_files_present when no files exist."""
        assert not downloader.are_files_present()

    def test_are_files_present_only_schematron(self, downloader, mock_schematron_content):
        """Test are_files_present when only schematron exists."""
        downloader.get_schematron_path().write_text(mock_schematron_content)
        assert not downloader.are_files_present()

    def test_are_files_present_missing_cleaned(
        self, downloader, mock_schematron_content, mock_vocabulary_content
    ):
        """Test are_files_present when cleaned file is missing."""
        downloader.get_schematron_path().write_text(mock_schematron_content)
        downloader.get_vocabulary_path().write_text(mock_vocabulary_content)
        assert not downloader.are_files_present()

    def test_are_files_present_all_exist(
        self, downloader, mock_schematron_content, mock_vocabulary_content
    ):
        """Test are_files_present when all files exist."""
        downloader.get_schematron_path().write_text(mock_schematron_content)
        downloader.get_cleaned_schematron_path().write_text(mock_schematron_content)
        downloader.get_vocabulary_path().write_text(mock_vocabulary_content)
        assert downloader.are_files_present()

    def test_download_schematron_success(self, downloader, mock_schematron_content):
        """Test successful download of Schematron file."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:

            def mock_download(url, path):
                Path(path).write_text(mock_schematron_content)

            mock_retrieve.side_effect = mock_download

            success, message = downloader.download_schematron()

            assert success is True
            assert "HL7_CCDA_R2.1.sch" in message
            assert downloader.get_schematron_path().exists()

    def test_download_schematron_already_exists(self, downloader, mock_schematron_content):
        """Test download when Schematron file already exists."""
        downloader.get_schematron_path().write_text(mock_schematron_content)

        success, message = downloader.download_schematron(force=False)

        assert success is True
        assert "already exists" in message

    def test_download_schematron_force_redownload(self, downloader, mock_schematron_content):
        """Test force download even when file exists."""
        downloader.get_schematron_path().write_text("old content")

        with patch("urllib.request.urlretrieve") as mock_retrieve:

            def mock_download(url, path):
                Path(path).write_text(mock_schematron_content)

            mock_retrieve.side_effect = mock_download

            success, message = downloader.download_schematron(force=True)

            assert success is True
            assert mock_retrieve.called

    def test_download_vocabulary_success(self, downloader, mock_vocabulary_content):
        """Test successful download of vocabulary file."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:

            def mock_download(url, path):
                Path(path).write_text(mock_vocabulary_content)

            mock_retrieve.side_effect = mock_download

            success, message = downloader.download_vocabulary()

            assert success is True
            assert "voc.xml" in message
            assert downloader.get_vocabulary_path().exists()

    def test_download_vocabulary_already_exists(self, downloader, mock_vocabulary_content):
        """Test download when vocabulary file already exists."""
        downloader.get_vocabulary_path().write_text(mock_vocabulary_content)

        success, message = downloader.download_vocabulary(force=False)

        assert success is True
        assert "already exists" in message

    def test_download_schematron_network_error(self, downloader):
        """Test handling of network errors during Schematron download."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = urllib.error.URLError("Network error")

            success, message = downloader.download_schematron()

            assert success is False
            assert "Failed to download" in message
            assert "HL7_CCDA_R2.1.sch" in message

    def test_download_vocabulary_network_error(self, downloader):
        """Test handling of network errors during vocabulary download."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = urllib.error.URLError("Network error")

            success, message = downloader.download_vocabulary()

            assert success is False
            assert "Failed to download" in message
            assert "voc.xml" in message

    def test_download_http_404_error(self, downloader):
        """Test handling of HTTP 404 errors."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = urllib.error.HTTPError(
                "http://test.com", 404, "Not Found", {}, None
            )

            success, message = downloader.download_schematron()

            assert success is False
            assert "Failed to download" in message

    def test_download_http_500_error(self, downloader):
        """Test handling of HTTP 500 server errors."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = urllib.error.HTTPError(
                "http://test.com", 500, "Server Error", {}, None
            )

            success, message = downloader.download_vocabulary()

            assert success is False
            assert "Failed to download" in message

    def test_download_timeout_error(self, downloader):
        """Test handling of timeout errors."""
        import socket

        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = socket.timeout("Connection timeout")

            success, message = downloader.download_schematron()

            assert success is False
            assert "Failed to download" in message

    def test_download_permission_error(self, downloader):
        """Test handling of permission errors during download."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = PermissionError("Permission denied")

            success, message = downloader.download_vocabulary()

            assert success is False
            assert "Failed to download" in message

    def test_download_disk_full_error(self, downloader):
        """Test handling of disk full errors."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = OSError("No space left on device")

            success, message = downloader.download_schematron()

            assert success is False
            assert "Failed to download" in message

    def test_download_all_success(
        self, downloader, mock_schematron_content, mock_vocabulary_content
    ):
        """Test successful download of all files."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:

            def mock_download(url, path):
                if "sch" in url:
                    Path(path).write_text(mock_schematron_content)
                else:
                    Path(path).write_text(mock_vocabulary_content)

            mock_retrieve.side_effect = mock_download

            # Mock the cleaner
            with patch.object(downloader, "_clean_schematron_file") as mock_clean:
                mock_clean.return_value = (True, "✓ Cleaned successfully")

                success, message = downloader.download_all()

                assert success is True
                assert "HL7_CCDA_R2.1.sch" in message
                assert "voc.xml" in message
                assert mock_clean.called

    def test_download_all_cleans_schematron(
        self, downloader, mock_schematron_content, mock_vocabulary_content
    ):
        """Test that download_all automatically cleans the Schematron file."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:

            def mock_download(url, path):
                if "sch" in url:
                    Path(path).write_text(mock_schematron_content)
                else:
                    Path(path).write_text(mock_vocabulary_content)

            mock_retrieve.side_effect = mock_download

            with patch.object(downloader, "_clean_schematron_file") as mock_clean:
                mock_clean.return_value = (True, "✓ Cleaned: removed 5 invalid references")

                success, message = downloader.download_all()

                assert success is True
                assert mock_clean.called
                assert "Cleaned" in message or "cleaned" in message.lower()

    def test_download_all_cleaning_failure(
        self, downloader, mock_schematron_content, mock_vocabulary_content
    ):
        """Test download_all when cleaning fails."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:

            def mock_download(url, path):
                if "sch" in url:
                    Path(path).write_text(mock_schematron_content)
                else:
                    Path(path).write_text(mock_vocabulary_content)

            mock_retrieve.side_effect = mock_download

            with patch.object(downloader, "_clean_schematron_file") as mock_clean:
                mock_clean.side_effect = Exception("Cleaning error")

                success, message = downloader.download_all()

                # Should still report overall success but with warning
                assert "Warning" in message or "warning" in message.lower()

    def test_download_all_schematron_fails(self, downloader):
        """Test download_all when Schematron download fails."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = urllib.error.URLError("Network error")

            success, message = downloader.download_all()

            assert success is False
            assert "Failed" in message

    def test_download_all_vocabulary_fails(self, downloader, mock_schematron_content):
        """Test download_all when vocabulary download fails."""
        call_count = [0]

        with patch("urllib.request.urlretrieve") as mock_retrieve:

            def mock_download(url, path):
                call_count[0] += 1
                if call_count[0] == 1:  # First call (schematron)
                    Path(path).write_text(mock_schematron_content)
                else:  # Second call (vocabulary)
                    raise urllib.error.URLError("Network error")

            mock_retrieve.side_effect = mock_download

            with patch.object(downloader, "_clean_schematron_file") as mock_clean:
                mock_clean.return_value = (True, "✓ Cleaned")

                success, message = downloader.download_all()

                assert success is False

    def test_clean_schematron_file_success(self, downloader, mock_schematron_content):
        """Test successful cleaning of Schematron file."""
        # Create schematron file
        downloader.get_schematron_path().write_text(mock_schematron_content)

        with patch("ccdakit.validators.schematron_cleaner.clean_schematron_file") as mock_clean:
            mock_clean.return_value = (
                downloader.get_cleaned_schematron_path(),
                {"invalid_references": 5, "total_patterns": 100},
            )

            success, message = downloader._clean_schematron_file()

            assert success is True
            assert "Cleaned" in message
            assert "5" in message
            assert mock_clean.called

    def test_clean_schematron_file_failure(self, downloader):
        """Test handling of cleaning failure."""
        with patch("ccdakit.validators.schematron_cleaner.clean_schematron_file") as mock_clean:
            mock_clean.side_effect = Exception("Cleaning failed")

            success, message = downloader._clean_schematron_file()

            assert success is False
            assert "Failed to clean" in message

    def test_error_message_includes_manual_download_url(self, downloader):
        """Test that error messages include manual download instructions."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:
            mock_retrieve.side_effect = urllib.error.URLError("Network error")

            success, message = downloader.download_schematron()

            assert success is False
            assert "download manually" in message.lower()
            assert "http" in message

    def test_download_reports_file_size(self, downloader, mock_schematron_content):
        """Test that successful download reports file size."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:

            def mock_download(url, path):
                Path(path).write_text(mock_schematron_content)

            mock_retrieve.side_effect = mock_download

            success, message = downloader.download_schematron()

            assert success is True
            assert "MB" in message

    def test_download_all_combines_messages(
        self, downloader, mock_schematron_content, mock_vocabulary_content
    ):
        """Test that download_all combines all result messages."""
        with patch("urllib.request.urlretrieve") as mock_retrieve:

            def mock_download(url, path):
                if "sch" in url:
                    Path(path).write_text(mock_schematron_content)
                else:
                    Path(path).write_text(mock_vocabulary_content)

            mock_retrieve.side_effect = mock_download

            with patch.object(downloader, "_clean_schematron_file") as mock_clean:
                mock_clean.return_value = (True, "✓ Cleaned successfully")

                success, message = downloader.download_all()

                # Message should contain information about all operations
                assert "\n" in message  # Multiple messages joined

    def test_base_url_constant(self):
        """Test that BASE_URL constant is properly set."""
        assert SchematronDownloader.BASE_URL.startswith("https://")
        assert "github" in SchematronDownloader.BASE_URL.lower()
        # Check that FILES configuration uses BASE_URL
        assert SchematronDownloader.FILES["schematron"]["url"].startswith(
            SchematronDownloader.BASE_URL
        )
        assert SchematronDownloader.FILES["vocabulary"]["url"].startswith(
            SchematronDownloader.BASE_URL
        )

    def test_concurrent_download_attempts(self, downloader, mock_schematron_content):
        """Test handling of concurrent download attempts."""
        import threading

        results = []

        def download_thread():
            with patch("urllib.request.urlretrieve") as mock_retrieve:

                def mock_download(url, path):
                    Path(path).write_text(mock_schematron_content)

                mock_retrieve.side_effect = mock_download

                success, message = downloader.download_schematron()
                results.append((success, message))

        # Start multiple threads
        threads = [threading.Thread(target=download_thread) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All should succeed (file exists or newly created)
        assert all(success for success, _ in results)


class TestDownloadSchematronFilesConvenience:
    """Test suite for download_schematron_files convenience function."""

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create a temporary directory for testing."""
        test_dir = tmp_path / "test_convenience"
        test_dir.mkdir(exist_ok=True)
        return test_dir

    def test_download_schematron_files_success(self, temp_dir):
        """Test successful download using convenience function."""
        with patch.object(SchematronDownloader, "download_all") as mock_download:
            mock_download.return_value = (True, "Success")

            result = download_schematron_files(target_dir=temp_dir, force=False)

            assert result is True
            assert mock_download.called

    def test_download_schematron_files_failure(self, temp_dir):
        """Test failed download using convenience function."""
        with patch.object(SchematronDownloader, "download_all") as mock_download:
            mock_download.return_value = (False, "Failed")

            result = download_schematron_files(target_dir=temp_dir)

            assert result is False

    def test_download_schematron_files_already_present(self, temp_dir):
        """Test when files are already present."""
        with patch.object(SchematronDownloader, "are_files_present") as mock_present:
            mock_present.return_value = True

            result = download_schematron_files(target_dir=temp_dir, force=False)

            assert result is True

    def test_download_schematron_files_force_redownload(self, temp_dir):
        """Test force redownload even when files exist."""
        with patch.object(SchematronDownloader, "are_files_present") as mock_present:
            with patch.object(SchematronDownloader, "download_all") as mock_download:
                mock_present.return_value = True
                mock_download.return_value = (True, "Success")

                result = download_schematron_files(target_dir=temp_dir, force=True)

                assert result is True
                assert mock_download.called

    def test_download_schematron_files_quiet_mode(self, temp_dir, caplog):
        """Test quiet mode suppresses logging."""
        import logging

        caplog.set_level(logging.INFO)

        with patch.object(SchematronDownloader, "are_files_present") as mock_present:
            mock_present.return_value = True

            download_schematron_files(target_dir=temp_dir, quiet=True)

            # Should not log in quiet mode
            info_logs = [r for r in caplog.records if r.levelname == "INFO"]
            assert len(info_logs) == 0

    def test_download_schematron_files_verbose_mode(self, temp_dir, caplog):
        """Test verbose mode logs messages."""
        import logging

        caplog.set_level(logging.INFO)

        with patch.object(SchematronDownloader, "are_files_present") as mock_present:
            mock_present.return_value = True

            download_schematron_files(target_dir=temp_dir, quiet=False)

            # Should log in verbose mode
            info_logs = [r for r in caplog.records if r.levelname == "INFO"]
            assert len(info_logs) > 0

    def test_download_schematron_files_default_directory(self):
        """Test using default directory."""
        with patch.object(SchematronDownloader, "are_files_present") as mock_present:
            mock_present.return_value = True

            result = download_schematron_files(target_dir=None)

            assert result is True
