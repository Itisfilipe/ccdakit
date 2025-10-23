"""Comprehensive tests for Schematron cleaner."""

from pathlib import Path

import pytest
from lxml import etree

from ccdakit.validators.schematron_cleaner import SchematronCleaner, clean_schematron_file


class TestSchematronCleaner:
    """Test suite for SchematronCleaner."""

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create a temporary directory for testing."""
        test_dir = tmp_path / "test_cleaner"
        test_dir.mkdir(exist_ok=True)
        return test_dir

    @pytest.fixture
    def valid_schematron_content(self):
        """Create valid Schematron file content with valid references."""
        return """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron">
    <pattern id="p-valid-1">
        <rule context="/">
            <assert test="true()">Test assertion 1</assert>
        </rule>
    </pattern>
    <pattern id="p-valid-2">
        <rule context="/root">
            <assert test="true()">Test assertion 2</assert>
        </rule>
    </pattern>
    <phase id="errors">
        <active pattern="p-valid-1"/>
        <active pattern="p-valid-2"/>
    </phase>
</schema>"""

    @pytest.fixture
    def schematron_with_invalid_refs(self):
        """Create Schematron with invalid pattern references."""
        return """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron">
    <pattern id="p-exists-1">
        <rule context="/">
            <assert test="true()">Assertion 1</assert>
        </rule>
    </pattern>
    <pattern id="p-exists-2">
        <rule context="/root">
            <assert test="true()">Assertion 2</assert>
        </rule>
    </pattern>
    <phase id="errors">
        <active pattern="p-exists-1"/>
        <active pattern="p-exists-2"/>
        <active pattern="p-missing-1"/>
        <active pattern="p-missing-2"/>
    </phase>
    <phase id="warnings">
        <active pattern="p-exists-1"/>
        <active pattern="p-missing-3"/>
    </phase>
</schema>"""

    @pytest.fixture
    def valid_schematron_file(self, temp_dir, valid_schematron_content):
        """Create a valid Schematron file."""
        file_path = temp_dir / "valid.sch"
        file_path.write_text(valid_schematron_content)
        return file_path

    @pytest.fixture
    def invalid_refs_file(self, temp_dir, schematron_with_invalid_refs):
        """Create a Schematron file with invalid references."""
        file_path = temp_dir / "invalid_refs.sch"
        file_path.write_text(schematron_with_invalid_refs)
        return file_path

    def test_init_with_valid_file(self, valid_schematron_file):
        """Test initializing cleaner with valid file."""
        cleaner = SchematronCleaner(valid_schematron_file)
        assert cleaner.schematron_path == valid_schematron_file

    def test_init_with_nonexistent_file(self, temp_dir):
        """Test initializing with nonexistent file raises FileNotFoundError."""
        nonexistent = temp_dir / "nonexistent.sch"
        with pytest.raises(FileNotFoundError, match="Schematron file not found"):
            SchematronCleaner(nonexistent)

    def test_init_converts_path_to_pathlib(self, valid_schematron_file):
        """Test that string paths are converted to Path objects."""
        cleaner = SchematronCleaner(str(valid_schematron_file))
        assert isinstance(cleaner.schematron_path, Path)

    def test_clean_valid_schematron(self, valid_schematron_file):
        """Test cleaning a valid Schematron file with no invalid references."""
        cleaner = SchematronCleaner(valid_schematron_file)
        output_path, stats = cleaner.clean(quiet=True)

        assert output_path.exists()
        assert stats["invalid_references"] == 0
        assert stats["total_patterns"] == 2
        assert stats["total_references"] == 2

    def test_clean_removes_invalid_references(self, invalid_refs_file):
        """Test that invalid pattern references are removed."""
        cleaner = SchematronCleaner(invalid_refs_file)
        output_path, stats = cleaner.clean(quiet=True)

        assert output_path.exists()
        assert stats["invalid_references"] == 3  # 2 in errors phase + 1 in warnings
        assert stats["errors_phase_cleaned"] == 2
        assert stats["warnings_phase_cleaned"] == 1
        assert stats["total_patterns"] == 2  # Only actual patterns

    def test_clean_preserves_valid_references(self, invalid_refs_file):
        """Test that valid references are preserved during cleaning."""
        cleaner = SchematronCleaner(invalid_refs_file)
        output_path, stats = cleaner.clean(quiet=True)

        # Parse cleaned file
        tree = etree.parse(str(output_path))
        root = tree.getroot()

        # Find all active elements
        sch_ns = "http://purl.oclc.org/dsdl/schematron"
        active_elements = root.findall(f".//{{{sch_ns}}}active")

        # Should have 3 valid references (2 in errors, 1 in warnings)
        assert len(active_elements) == 3
        assert stats["total_references"] == 3

    def test_clean_custom_output_path(self, valid_schematron_file, temp_dir):
        """Test cleaning with custom output path."""
        custom_output = temp_dir / "custom_output.sch"
        cleaner = SchematronCleaner(valid_schematron_file)
        output_path, stats = cleaner.clean(output_path=custom_output, quiet=True)

        assert output_path == custom_output
        assert custom_output.exists()

    def test_clean_default_output_path(self, valid_schematron_file):
        """Test that default output path has '_cleaned' suffix."""
        cleaner = SchematronCleaner(valid_schematron_file)
        output_path, stats = cleaner.clean(quiet=True)

        assert "_cleaned" in output_path.name
        assert output_path.suffix == ".sch"
        assert output_path.parent == valid_schematron_file.parent

    def test_clean_adds_comment(self, valid_schematron_file):
        """Test that cleaning adds explanatory comment to document."""
        cleaner = SchematronCleaner(valid_schematron_file)
        output_path, stats = cleaner.clean(quiet=True)

        # Read cleaned file
        content = output_path.read_text()

        # Should contain comment about cleaning
        assert "automatically processed" in content
        assert "IDREF errors" in content
        assert "ccdakit" in content

    def test_clean_logging_quiet_mode(self, valid_schematron_file, caplog):
        """Test that quiet mode suppresses logging."""
        import logging

        caplog.set_level(logging.INFO)

        cleaner = SchematronCleaner(valid_schematron_file)
        cleaner.clean(quiet=True)

        # Should not log in quiet mode
        info_logs = [r for r in caplog.records if r.levelname == "INFO"]
        assert len(info_logs) == 0

    def test_clean_logging_verbose_mode(self, valid_schematron_file, caplog):
        """Test that verbose mode logs information."""
        import logging

        caplog.set_level(logging.INFO)

        cleaner = SchematronCleaner(valid_schematron_file)
        cleaner.clean(quiet=False)

        # Should log in verbose mode
        info_logs = [r for r in caplog.records if r.levelname == "INFO"]
        assert len(info_logs) > 0

    def test_clean_logs_removed_references(self, invalid_refs_file, caplog):
        """Test that cleaning logs number of removed references."""
        import logging

        caplog.set_level(logging.INFO)

        cleaner = SchematronCleaner(invalid_refs_file)
        cleaner.clean(quiet=False)

        # Should log removed references
        log_messages = [r.message for r in caplog.records if r.levelname == "INFO"]
        assert any("Removed" in msg for msg in log_messages)

    def test_find_actual_patterns(self, valid_schematron_file):
        """Test finding actual pattern IDs."""
        cleaner = SchematronCleaner(valid_schematron_file)
        tree = etree.parse(str(valid_schematron_file))
        root = tree.getroot()

        patterns = cleaner._find_actual_patterns(root)

        assert "p-valid-1" in patterns
        assert "p-valid-2" in patterns
        assert len(patterns) == 2

    def test_find_actual_patterns_empty(self, temp_dir):
        """Test finding patterns in Schematron with no patterns."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron">
</schema>"""
        file_path = temp_dir / "no_patterns.sch"
        file_path.write_text(content)

        cleaner = SchematronCleaner(file_path)
        tree = etree.parse(str(file_path))
        root = tree.getroot()

        patterns = cleaner._find_actual_patterns(root)

        assert len(patterns) == 0

    def test_clean_phase(self, invalid_refs_file):
        """Test cleaning a single phase."""
        cleaner = SchematronCleaner(invalid_refs_file)
        tree = etree.parse(str(invalid_refs_file))
        root = tree.getroot()

        # Find actual patterns
        actual_patterns = cleaner._find_actual_patterns(root)

        # Find errors phase
        sch_ns = "http://purl.oclc.org/dsdl/schematron"
        errors_phase = root.find(f".//{{{sch_ns}}}phase[@id='errors']")

        # Get initial count of active elements
        initial_count = len(errors_phase.findall(f"{{{sch_ns}}}active"))

        # Clean the phase
        removed = cleaner._clean_phase(errors_phase, actual_patterns)

        # Check that invalid references were removed
        assert removed == 2
        final_count = len(errors_phase.findall(f"{{{sch_ns}}}active"))
        assert final_count == initial_count - removed

    def test_clean_phase_no_invalid_refs(self, valid_schematron_file):
        """Test cleaning phase with all valid references."""
        cleaner = SchematronCleaner(valid_schematron_file)
        tree = etree.parse(str(valid_schematron_file))
        root = tree.getroot()

        actual_patterns = cleaner._find_actual_patterns(root)

        sch_ns = "http://purl.oclc.org/dsdl/schematron"
        errors_phase = root.find(f".//{{{sch_ns}}}phase[@id='errors']")

        removed = cleaner._clean_phase(errors_phase, actual_patterns)

        assert removed == 0

    def test_add_cleaning_comment(self, valid_schematron_file):
        """Test adding cleaning comment to root element."""
        cleaner = SchematronCleaner(valid_schematron_file)
        tree = etree.parse(str(valid_schematron_file))
        root = tree.getroot()

        # Initially no comments
        initial_comment_count = len([child for child in root if isinstance(child, etree._Comment)])

        cleaner._add_cleaning_comment(root)

        # Should have one comment now
        comments = [child for child in root if isinstance(child, etree._Comment)]
        assert len(comments) == initial_comment_count + 1

        # Check comment content
        comment_text = str(comments[0])
        assert "automatically processed" in comment_text
        assert "ccdakit" in comment_text

    def test_clean_malformed_xml(self, temp_dir):
        """Test handling of malformed XML."""
        malformed = temp_dir / "malformed.sch"
        malformed.write_text("<schema><unclosed>")

        with pytest.raises(etree.XMLSyntaxError):
            cleaner = SchematronCleaner(malformed)
            cleaner.clean()

    def test_clean_preserves_xml_declaration(self, valid_schematron_file):
        """Test that cleaned file has XML declaration."""
        cleaner = SchematronCleaner(valid_schematron_file)
        output_path, stats = cleaner.clean(quiet=True)

        content = output_path.read_text()
        assert content.startswith("<?xml version=")
        assert "1.0" in content[:50]  # Version should be in first line

    def test_clean_preserves_encoding(self, valid_schematron_file):
        """Test that cleaned file preserves UTF-8 encoding."""
        cleaner = SchematronCleaner(valid_schematron_file)
        output_path, stats = cleaner.clean(quiet=True)

        content = output_path.read_text()
        # Check for encoding (can use single or double quotes)
        assert "encoding=" in content[:100]
        assert "UTF-8" in content[:100].upper()

    def test_clean_pretty_print(self, valid_schematron_file):
        """Test that cleaned file is pretty-printed."""
        cleaner = SchematronCleaner(valid_schematron_file)
        output_path, stats = cleaner.clean(quiet=True)

        content = output_path.read_text()
        # Pretty-printed XML should have indentation
        lines = content.split("\n")
        indented_lines = [line for line in lines if line.startswith("  ")]
        assert len(indented_lines) > 0

    def test_clean_multiple_phases(self, temp_dir):
        """Test cleaning with multiple phases."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron">
    <pattern id="p-1">
        <rule context="/"><assert test="true()">Test</assert></rule>
    </pattern>
    <phase id="errors">
        <active pattern="p-1"/>
        <active pattern="p-missing-1"/>
    </phase>
    <phase id="warnings">
        <active pattern="p-1"/>
        <active pattern="p-missing-2"/>
    </phase>
    <phase id="info">
        <active pattern="p-1"/>
        <active pattern="p-missing-3"/>
    </phase>
</schema>"""
        file_path = temp_dir / "multi_phase.sch"
        file_path.write_text(content)

        cleaner = SchematronCleaner(file_path)
        output_path, stats = cleaner.clean(quiet=True)

        # Should remove one invalid ref from each phase
        assert stats["invalid_references"] == 3
        assert stats["total_references"] == 3  # One valid ref per phase

    def test_clean_pattern_without_id(self, temp_dir):
        """Test handling of patterns without id attribute."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron">
    <pattern>
        <rule context="/"><assert test="true()">Test</assert></rule>
    </pattern>
    <pattern id="p-1">
        <rule context="/root"><assert test="true()">Test</assert></rule>
    </pattern>
    <phase id="errors">
        <active pattern="p-1"/>
        <active pattern="p-missing"/>
    </phase>
</schema>"""
        file_path = temp_dir / "no_id.sch"
        file_path.write_text(content)

        cleaner = SchematronCleaner(file_path)
        output_path, stats = cleaner.clean(quiet=True)

        # Should only find the one pattern with an ID
        assert stats["total_patterns"] == 1
        assert stats["invalid_references"] == 1

    def test_clean_active_without_pattern_attribute(self, temp_dir):
        """Test handling of active elements without pattern attribute."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron">
    <pattern id="p-1">
        <rule context="/"><assert test="true()">Test</assert></rule>
    </pattern>
    <phase id="errors">
        <active pattern="p-1"/>
        <active/>
    </phase>
</schema>"""
        file_path = temp_dir / "no_pattern_attr.sch"
        file_path.write_text(content)

        cleaner = SchematronCleaner(file_path)
        output_path, stats = cleaner.clean(quiet=True)

        # Active element without pattern attribute shouldn't cause errors
        # It will be skipped (not removed, not counted)
        assert stats["total_patterns"] == 1

    def test_clean_stats_dictionary_complete(self, invalid_refs_file):
        """Test that stats dictionary contains all expected keys."""
        cleaner = SchematronCleaner(invalid_refs_file)
        output_path, stats = cleaner.clean(quiet=True)

        expected_keys = [
            "total_patterns",
            "total_references",
            "invalid_references",
            "errors_phase_cleaned",
            "warnings_phase_cleaned",
        ]

        for key in expected_keys:
            assert key in stats
            assert isinstance(stats[key], int)

    def test_clean_file_io_error(self, valid_schematron_file, temp_dir):
        """Test handling of file I/O errors during write."""

        cleaner = SchematronCleaner(valid_schematron_file)

        # Create read-only directory to force write error
        readonly_dir = temp_dir / "readonly"
        readonly_dir.mkdir()
        output_path = readonly_dir / "output.sch"

        # Make directory read-only (no write permission)
        import os
        import stat

        try:
            # Remove write permissions
            os.chmod(readonly_dir, stat.S_IRUSR | stat.S_IXUSR)

            # Attempt to write should fail
            with pytest.raises((IOError, OSError, PermissionError)):
                cleaner.clean(output_path=output_path, quiet=True)
        finally:
            # Restore permissions for cleanup
            try:
                os.chmod(readonly_dir, stat.S_IRWXU)
            except (OSError, PermissionError):
                # Unable to restore permissions, will be cleaned up by pytest
                pass

    def test_sch_namespace_constant(self):
        """Test that SCH_NS constant is correctly defined."""
        assert SchematronCleaner.SCH_NS == "http://purl.oclc.org/dsdl/schematron"


class TestCleanSchematronFileConvenience:
    """Test suite for clean_schematron_file convenience function."""

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Create a temporary directory for testing."""
        test_dir = tmp_path / "test_convenience"
        test_dir.mkdir(exist_ok=True)
        return test_dir

    @pytest.fixture
    def test_file(self, temp_dir):
        """Create a test Schematron file."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron">
    <pattern id="p-1">
        <rule context="/"><assert test="true()">Test</assert></rule>
    </pattern>
    <phase id="errors">
        <active pattern="p-1"/>
        <active pattern="p-missing"/>
    </phase>
</schema>"""
        file_path = temp_dir / "test.sch"
        file_path.write_text(content)
        return file_path

    def test_clean_schematron_file_success(self, test_file):
        """Test successful cleaning using convenience function."""
        output_path, stats = clean_schematron_file(test_file, quiet=True)

        assert output_path.exists()
        assert stats["invalid_references"] == 1
        assert "_cleaned" in output_path.name

    def test_clean_schematron_file_custom_output(self, test_file, temp_dir):
        """Test cleaning with custom output path."""
        custom_output = temp_dir / "custom.sch"
        output_path, stats = clean_schematron_file(test_file, output_path=custom_output, quiet=True)

        assert output_path == custom_output
        assert custom_output.exists()

    def test_clean_schematron_file_quiet_mode(self, test_file, caplog):
        """Test quiet mode suppresses logging."""
        import logging

        caplog.set_level(logging.INFO)

        clean_schematron_file(test_file, quiet=True)

        info_logs = [r for r in caplog.records if r.levelname == "INFO"]
        assert len(info_logs) == 0

    def test_clean_schematron_file_verbose_mode(self, test_file, caplog):
        """Test verbose mode logs information."""
        import logging

        caplog.set_level(logging.INFO)

        clean_schematron_file(test_file, quiet=False)

        info_logs = [r for r in caplog.records if r.levelname == "INFO"]
        assert len(info_logs) > 0

    def test_clean_schematron_file_nonexistent(self, temp_dir):
        """Test cleaning nonexistent file raises error."""
        nonexistent = temp_dir / "nonexistent.sch"

        with pytest.raises(FileNotFoundError):
            clean_schematron_file(nonexistent)

    def test_clean_schematron_file_returns_stats(self, test_file):
        """Test that convenience function returns statistics."""
        output_path, stats = clean_schematron_file(test_file, quiet=True)

        assert isinstance(stats, dict)
        assert "total_patterns" in stats
        assert "invalid_references" in stats

    def test_clean_schematron_file_string_path(self, test_file):
        """Test that convenience function accepts string paths."""
        output_path, stats = clean_schematron_file(str(test_file), quiet=True)

        assert output_path.exists()
        assert isinstance(output_path, Path)
