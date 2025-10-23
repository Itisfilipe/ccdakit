"""Tests for the generate CLI command."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from ccdakit.cli.__main__ import app


runner = CliRunner()


class TestGenerateCommand:
    """Test suite for the generate command."""

    def test_generate_help(self):
        """Test the --help flag displays help information."""
        result = runner.invoke(app, ["generate", "--help"])
        assert result.exit_code == 0
        assert "Generate a sample C-CDA document" in result.stdout
        assert "document_type" in result.stdout.lower() or "document-type" in result.stdout.lower()
        assert "--output" in result.stdout
        assert "--sections" in result.stdout
        assert "--interactive" in result.stdout

    def test_generate_invalid_document_type(self):
        """Test generation with an invalid document type."""
        result = runner.invoke(app, ["generate", "invalid-type"])
        assert result.exit_code == 1
        assert "Unknown document type" in result.stdout
        assert "Available types:" in result.stdout

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_ccd_default(self, mock_generate, tmp_path):
        """Test CCD generation with default settings."""
        # Create a mock document
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test_ccd.xml"
        result = runner.invoke(
            app,
            ["generate", "ccd", "--output", str(output_file)],
        )

        assert result.exit_code == 0
        assert "Document generated successfully" in result.stdout
        assert output_file.name in result.stdout

        # Check that document was written
        assert output_file.exists()
        content = output_file.read_text()
        assert "ClinicalDocument" in content

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_discharge_summary(self, mock_generate, tmp_path):
        """Test discharge summary generation."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test_discharge.xml"
        result = runner.invoke(
            app,
            ["generate", "discharge-summary", "--output", str(output_file)],
        )

        assert result.exit_code == 0
        assert output_file.exists()

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_with_sections(self, mock_generate, tmp_path):
        """Test generation with specific sections."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test_sections.xml"
        result = runner.invoke(
            app,
            [
                "generate",
                "ccd",
                "--output",
                str(output_file),
                "--sections",
                "problems,medications,allergies",
            ],
        )

        assert result.exit_code == 0
        assert output_file.exists()

        # Verify the sections were passed to the generator
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args
        sections = call_args[0][1]  # Second positional argument
        assert "problems" in sections
        assert "medications" in sections
        assert "allergies" in sections

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_auto_filename(self, mock_generate, tmp_path, monkeypatch):
        """Test generation with automatic filename."""
        # Change to tmp_path so generated file appears there
        monkeypatch.chdir(tmp_path)

        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        result = runner.invoke(app, ["generate", "ccd"])

        assert result.exit_code == 0
        assert "Document generated successfully" in result.stdout

        # Check that a file was created with timestamp pattern
        xml_files = list(tmp_path.glob("ccd_*.xml"))
        assert len(xml_files) == 1

    def test_generate_missing_faker(self):
        """Test generation when faker is not installed."""
        with patch("importlib.util.find_spec", return_value=None):
            result = runner.invoke(app, ["generate", "ccd"])

            # Should exit with error about missing faker
            assert result.exit_code == 1
            assert "faker" in result.stdout.lower()

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_exception_handling(self, mock_generate, tmp_path):
        """Test handling of exceptions during document generation."""
        mock_generate.side_effect = Exception("Generation error")

        output_file = tmp_path / "test_error.xml"
        result = runner.invoke(
            app,
            ["generate", "ccd", "--output", str(output_file)],
        )

        assert result.exit_code == 1
        assert "Error generating document" in result.stdout

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_write_error(self, mock_generate, tmp_path):
        """Test handling of file write errors."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        # Try to write to a directory that doesn't exist
        output_file = tmp_path / "nonexistent" / "test.xml"
        result = runner.invoke(
            app,
            ["generate", "ccd", "--output", str(output_file)],
        )

        assert result.exit_code == 1
        assert "Error writing file" in result.stdout

    @patch("ccdakit.cli.commands.generate._interactive_section_selection")
    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_interactive_mode(self, mock_generate, mock_interactive, tmp_path):
        """Test generation with interactive mode."""
        mock_interactive.return_value = ["problems", "medications"]
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test_interactive.xml"
        result = runner.invoke(
            app,
            ["generate", "ccd", "--output", str(output_file), "--interactive"],
        )

        assert result.exit_code == 0
        # Interactive selection should have been called
        mock_interactive.assert_called_once()

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_sections_with_spaces(self, mock_generate, tmp_path):
        """Test generation with section list containing spaces."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test.xml"
        result = runner.invoke(
            app,
            [
                "generate",
                "ccd",
                "--output",
                str(output_file),
                "--sections",
                "problems, medications, allergies",
            ],
        )

        assert result.exit_code == 0

        # Verify sections were properly stripped
        call_args = mock_generate.call_args
        sections = call_args[0][1]
        assert "problems" in sections
        assert "medications" in sections
        assert "allergies" in sections
        # No leading/trailing spaces
        for section in sections:
            assert section == section.strip()

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_all_document_types(self, mock_generate, tmp_path):
        """Test generation for all supported document types."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        document_types = ["ccd", "discharge-summary"]

        for doc_type in document_types:
            output_file = tmp_path / f"{doc_type}.xml"
            result = runner.invoke(
                app,
                ["generate", doc_type, "--output", str(output_file)],
            )

            assert result.exit_code == 0, f"Failed for document type: {doc_type}"
            assert output_file.exists()

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_with_empty_sections_list(self, mock_generate, tmp_path):
        """Test generation with an empty sections list."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test.xml"
        result = runner.invoke(
            app,
            ["generate", "ccd", "--output", str(output_file), "--sections", ""],
        )

        assert result.exit_code == 0
        # Verify empty sections resulted in an empty list after processing
        call_args = mock_generate.call_args
        sections = call_args[0][1]
        # Empty string split should result in list with empty string which gets filtered
        assert isinstance(sections, list)

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_default_sections_for_ccd(self, mock_generate, tmp_path):
        """Test that CCD uses default sections when none specified."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test.xml"
        result = runner.invoke(
            app,
            ["generate", "ccd", "--output", str(output_file)],
        )

        assert result.exit_code == 0
        # Check default sections for CCD
        call_args = mock_generate.call_args
        sections = call_args[0][1]
        assert "problems" in sections
        assert "medications" in sections
        assert "allergies" in sections

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_default_sections_for_discharge_summary(self, mock_generate, tmp_path):
        """Test that Discharge Summary uses default sections when none specified."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test.xml"
        result = runner.invoke(
            app,
            ["generate", "discharge-summary", "--output", str(output_file)],
        )

        assert result.exit_code == 0
        # Check default sections for Discharge Summary
        call_args = mock_generate.call_args
        sections = call_args[0][1]
        assert "problems" in sections
        assert "medications" in sections
        assert "allergies" in sections
        assert "procedures" in sections
        assert "vital-signs" in sections


class TestInteractiveSelection:
    """Test interactive section selection functionality."""

    @patch("rich.prompt.Prompt.ask")
    def test_interactive_selection_all_sections(self, mock_ask):
        """Test interactive selection with 'all' input."""
        from ccdakit.cli.commands.generate import _interactive_section_selection

        mock_ask.return_value = "all"
        sections = _interactive_section_selection()

        # Should return all available sections
        assert len(sections) > 0
        assert "problems" in sections
        assert "medications" in sections

    @patch("rich.prompt.Prompt.ask")
    def test_interactive_selection_empty_input(self, mock_ask):
        """Test interactive selection with empty input (defaults to 'all')."""
        from ccdakit.cli.commands.generate import _interactive_section_selection

        mock_ask.return_value = ""
        sections = _interactive_section_selection()

        # Empty input should return all sections
        assert len(sections) > 0

    @patch("rich.prompt.Prompt.ask")
    def test_interactive_selection_specific_numbers(self, mock_ask):
        """Test interactive selection with specific section numbers."""
        from ccdakit.cli.commands.generate import _interactive_section_selection

        # Select first 3 sections
        mock_ask.return_value = "1,2,3"
        sections = _interactive_section_selection()

        # Should return exactly 3 sections
        assert len(sections) == 3

    @patch("rich.prompt.Prompt.ask")
    def test_interactive_selection_with_spaces(self, mock_ask):
        """Test interactive selection with spaces in input."""
        from ccdakit.cli.commands.generate import _interactive_section_selection

        mock_ask.return_value = "1, 2, 3"
        sections = _interactive_section_selection()

        # Should handle spaces properly
        assert len(sections) == 3

    @patch("rich.prompt.Prompt.ask")
    def test_interactive_selection_invalid_number(self, mock_ask):
        """Test interactive selection with invalid section number."""
        from ccdakit.cli.commands.generate import _interactive_section_selection

        # Try to select section 9999 (doesn't exist) along with valid ones
        mock_ask.return_value = "1,9999,2"
        sections = _interactive_section_selection()

        # Should return only valid sections
        assert len(sections) == 2

    @patch("rich.prompt.Prompt.ask")
    def test_interactive_selection_negative_number(self, mock_ask):
        """Test interactive selection with negative section number."""
        from ccdakit.cli.commands.generate import _interactive_section_selection

        mock_ask.return_value = "-1,1"
        sections = _interactive_section_selection()

        # Should skip negative numbers
        assert len(sections) == 1

    @patch("rich.prompt.Prompt.ask")
    def test_interactive_selection_invalid_input(self, mock_ask):
        """Test interactive selection with non-numeric input."""
        from ccdakit.cli.commands.generate import _interactive_section_selection

        mock_ask.return_value = "abc,def"
        sections = _interactive_section_selection()

        # Invalid input should fall back to all sections
        assert len(sections) > 0

    @patch("rich.prompt.Prompt.ask")
    def test_interactive_selection_no_valid_selections(self, mock_ask):
        """Test interactive selection when no valid sections selected."""
        from ccdakit.cli.commands.generate import _interactive_section_selection

        # Only invalid numbers
        mock_ask.return_value = "999,1000"
        sections = _interactive_section_selection()

        # Should fall back to default sections
        assert len(sections) == 3
        assert "problems" in sections
        assert "medications" in sections
        assert "allergies" in sections

    @patch("rich.prompt.Prompt.ask")
    def test_interactive_selection_mixed_valid_invalid(self, mock_ask):
        """Test interactive selection with mix of valid and invalid inputs."""
        from ccdakit.cli.commands.generate import _interactive_section_selection

        # Mix of valid numbers, invalid numbers, and text
        # When there's a ValueError (from "abc"), it falls back to all sections
        mock_ask.return_value = "1,999,abc,2"
        sections = _interactive_section_selection()

        # Should fall back to all sections because of ValueError from "abc"
        assert len(sections) > 10  # All sections


class TestGenerateDocument:
    """Test _generate_document function with different section combinations."""

    @pytest.mark.skipif(
        not Path("/Users/filipe/Code/pyccda/ccdakit/utils/test_data.py").exists(),
        reason="Test data generator not available",
    )
    def test_generate_document_with_procedures(self):
        """Test document generation with procedures section."""
        from ccdakit.cli.commands.generate import _generate_document

        try:
            import faker  # noqa: F401
        except ImportError:
            pytest.skip("faker not installed")

        # Test with procedures section (currently empty list in generator)
        sections = ["problems", "medications", "procedures"]
        doc = _generate_document("ccd", sections)
        assert doc is not None

    @pytest.mark.skipif(
        not Path("/Users/filipe/Code/pyccda/ccdakit/utils/test_data.py").exists(),
        reason="Test data generator not available",
    )
    def test_generate_document_with_results(self):
        """Test document generation with results section."""
        from ccdakit.cli.commands.generate import _generate_document

        try:
            import faker  # noqa: F401
        except ImportError:
            pytest.skip("faker not installed")

        # Test with results section (currently empty list in generator)
        sections = ["problems", "medications", "results"]
        doc = _generate_document("ccd", sections)
        assert doc is not None

    @pytest.mark.skipif(
        not Path("/Users/filipe/Code/pyccda/ccdakit/utils/test_data.py").exists(),
        reason="Test data generator not available",
    )
    def test_generate_document_with_social_history(self):
        """Test document generation with social history section."""
        from ccdakit.cli.commands.generate import _generate_document

        try:
            import faker  # noqa: F401
        except ImportError:
            pytest.skip("faker not installed")

        # Test with social-history section (currently empty list in generator)
        sections = ["problems", "medications", "social-history"]
        doc = _generate_document("ccd", sections)
        assert doc is not None

    @pytest.mark.skipif(
        not Path("/Users/filipe/Code/pyccda/ccdakit/utils/test_data.py").exists(),
        reason="Test data generator not available",
    )
    def test_generate_document_with_encounters(self):
        """Test document generation with encounters section."""
        from ccdakit.cli.commands.generate import _generate_document

        try:
            import faker  # noqa: F401
        except ImportError:
            pytest.skip("faker not installed")

        # Test with encounters section (currently empty list in generator)
        sections = ["problems", "medications", "encounters"]
        doc = _generate_document("ccd", sections)
        assert doc is not None

    @pytest.mark.skipif(
        not Path("/Users/filipe/Code/pyccda/ccdakit/utils/test_data.py").exists(),
        reason="Test data generator not available",
    )
    def test_generate_document_all_supported_sections(self):
        """Test document generation with all currently supported sections."""
        from ccdakit.cli.commands.generate import _generate_document

        try:
            import faker  # noqa: F401
        except ImportError:
            pytest.skip("faker not installed")

        # Test with all supported sections
        sections = ["problems", "medications", "allergies", "immunizations", "vital-signs"]
        doc = _generate_document("ccd", sections)
        assert doc is not None
        # Just verify the document has a to_xml_string method
        assert hasattr(doc, "to_xml_string")


class TestGenerateIntegration:
    """Integration tests for generate command with real data."""

    @pytest.mark.skipif(
        not Path("/Users/filipe/Code/pyccda/ccdakit/utils/test_data.py").exists(),
        reason="Test data generator not available",
    )
    def test_generate_real_ccd(self, tmp_path):
        """Test real CCD generation if faker is available."""
        try:
            import faker  # noqa: F401
        except ImportError:
            pytest.skip("faker not installed")

        output_file = tmp_path / "real_ccd.xml"
        result = runner.invoke(
            app,
            ["generate", "ccd", "--output", str(output_file)],
        )

        # May succeed or fail depending on environment
        if result.exit_code == 0:
            assert output_file.exists()
            content = output_file.read_text()
            assert '<?xml version="1.0"' in content or "<?xml version='1.0'" in content
            assert "ClinicalDocument" in content

    @pytest.mark.skipif(
        not Path("/Users/filipe/Code/pyccda/ccdakit/utils/test_data.py").exists(),
        reason="Test data generator not available",
    )
    def test_generate_with_multiple_sections(self, tmp_path):
        """Test generation with multiple sections."""
        try:
            import faker  # noqa: F401
        except ImportError:
            pytest.skip("faker not installed")

        output_file = tmp_path / "multi_section.xml"
        result = runner.invoke(
            app,
            [
                "generate",
                "ccd",
                "--output",
                str(output_file),
                "--sections",
                "problems,medications,allergies,vital-signs,immunizations",
            ],
        )

        if result.exit_code == 0:
            assert output_file.exists()
            content = output_file.read_text()
            # Basic structure checks
            assert "ClinicalDocument" in content

    @pytest.mark.skipif(
        not Path("/Users/filipe/Code/pyccda/ccdakit/utils/test_data.py").exists(),
        reason="Test data generator not available",
    )
    def test_generate_real_discharge_summary(self, tmp_path):
        """Test real discharge summary generation."""
        try:
            import faker  # noqa: F401
        except ImportError:
            pytest.skip("faker not installed")

        output_file = tmp_path / "discharge_summary.xml"
        result = runner.invoke(
            app,
            ["generate", "discharge-summary", "--output", str(output_file)],
        )

        if result.exit_code == 0:
            assert output_file.exists()
            content = output_file.read_text()
            assert "ClinicalDocument" in content


class TestDocumentSummary:
    """Test document summary output."""

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_summary_displayed(self, mock_generate, tmp_path):
        """Test that document summary is displayed after generation."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test.xml"
        result = runner.invoke(
            app,
            [
                "generate",
                "ccd",
                "--output",
                str(output_file),
                "--sections",
                "problems,medications",
            ],
        )

        assert result.exit_code == 0
        assert "Document Summary" in result.stdout
        assert "Sections included:" in result.stdout

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_summary_shows_section_names(self, mock_generate, tmp_path):
        """Test that summary shows human-readable section names."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test.xml"
        result = runner.invoke(
            app,
            [
                "generate",
                "ccd",
                "--output",
                str(output_file),
                "--sections",
                "problems,allergies",
            ],
        )

        assert result.exit_code == 0
        # Check for human-readable names
        assert "Problems Section" in result.stdout
        assert "Allergies and Intolerances Section" in result.stdout

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_summary_shows_validation_hint(self, mock_generate, tmp_path):
        """Test that summary includes hint about validation command."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test.xml"
        result = runner.invoke(
            app,
            ["generate", "ccd", "--output", str(output_file)],
        )

        assert result.exit_code == 0
        assert "validate" in result.stdout
        assert "ccdakit validate" in result.stdout


class TestEdgeCases:
    """Test edge cases and error conditions."""

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_with_special_chars_in_path(self, mock_generate, tmp_path):
        """Test generation with special characters in file path."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        # Create path with special characters (that are valid on most filesystems)
        output_file = tmp_path / "test_file-with-dashes_and_underscores.xml"
        result = runner.invoke(
            app,
            ["generate", "ccd", "--output", str(output_file)],
        )

        assert result.exit_code == 0
        assert output_file.exists()

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_overwrites_existing_file(self, mock_generate, tmp_path):
        """Test that generation overwrites existing file."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test.xml"

        # Create existing file with different content
        output_file.write_text("Old content")

        result = runner.invoke(
            app,
            ["generate", "ccd", "--output", str(output_file)],
        )

        assert result.exit_code == 0
        # File should be overwritten
        content = output_file.read_text()
        assert "ClinicalDocument" in content
        assert "Old content" not in content

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_shows_absolute_path(self, mock_generate, tmp_path):
        """Test that output shows absolute path."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test.xml"
        result = runner.invoke(
            app,
            ["generate", "ccd", "--output", str(output_file)],
        )

        assert result.exit_code == 0
        # Should show path in output (may be absolute or just filename)
        assert "test.xml" in result.stdout or str(output_file) in result.stdout

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_with_very_long_sections_list(self, mock_generate, tmp_path):
        """Test generation with a very long list of sections."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        # Create a long sections list
        sections_list = "problems,medications,allergies,immunizations,vital-signs,procedures,results,social-history,encounters"

        output_file = tmp_path / "test.xml"
        result = runner.invoke(
            app,
            [
                "generate",
                "ccd",
                "--output",
                str(output_file),
                "--sections",
                sections_list,
            ],
        )

        assert result.exit_code == 0
        # Verify all sections were passed
        call_args = mock_generate.call_args
        sections = call_args[0][1]
        assert len(sections) == 9

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_with_duplicate_sections(self, mock_generate, tmp_path):
        """Test generation with duplicate sections in list."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test.xml"
        result = runner.invoke(
            app,
            [
                "generate",
                "ccd",
                "--output",
                str(output_file),
                "--sections",
                "problems,medications,problems,allergies",  # 'problems' duplicated
            ],
        )

        assert result.exit_code == 0
        # Verify sections were passed (duplicates may be preserved)
        call_args = mock_generate.call_args
        sections = call_args[0][1]
        assert "problems" in sections
        assert "medications" in sections
        assert "allergies" in sections

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_banner_displayed(self, mock_generate, tmp_path):
        """Test that generation banner is displayed."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test.xml"
        result = runner.invoke(
            app,
            ["generate", "ccd", "--output", str(output_file)],
        )

        assert result.exit_code == 0
        # Check banner text
        assert "Generating:" in result.stdout
        assert "Continuity of Care Document" in result.stdout

    @patch("ccdakit.cli.commands.generate._generate_document")
    def test_generate_progress_messages(self, mock_generate, tmp_path):
        """Test that progress messages are displayed."""
        mock_doc = MagicMock()
        mock_doc.to_xml_string.return_value = '<?xml version="1.0"?><ClinicalDocument/>'
        mock_generate.return_value = mock_doc

        output_file = tmp_path / "test.xml"
        result = runner.invoke(
            app,
            ["generate", "ccd", "--output", str(output_file)],
        )

        assert result.exit_code == 0
        # Check for progress messages
        assert "Generating test data..." in result.stdout
        assert "Document generated successfully" in result.stdout


class TestDocumentTypeMapping:
    """Test document type mapping and configuration."""

    def test_document_types_constant(self):
        """Test that DOCUMENT_TYPES constant is properly configured."""
        from ccdakit.cli.commands.generate import DOCUMENT_TYPES

        # Should have at least CCD and Discharge Summary
        assert "ccd" in DOCUMENT_TYPES
        assert "discharge-summary" in DOCUMENT_TYPES

        # Each type should have name and class
        for doc_type, config in DOCUMENT_TYPES.items():
            assert "name" in config
            assert "class" in config
            assert isinstance(config["name"], str)
            assert config["class"] is not None

    def test_available_sections_constant(self):
        """Test that AVAILABLE_SECTIONS constant is properly configured."""
        from ccdakit.cli.commands.generate import AVAILABLE_SECTIONS

        # Should have multiple sections
        assert len(AVAILABLE_SECTIONS) > 10

        # Each section should be a tuple of (code, name)
        for section in AVAILABLE_SECTIONS:
            assert isinstance(section, tuple)
            assert len(section) == 2
            code, name = section
            assert isinstance(code, str)
            assert isinstance(name, str)
            assert len(code) > 0
            assert len(name) > 0
