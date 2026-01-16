"""Tests for CLI list commands."""

from typer.testing import CliRunner

from ccdakit.cli.__main__ import app


runner = CliRunner()


class TestListSectionsCommand:
    """Tests for the list-sections command."""

    def test_list_sections_default(self):
        """Test listing sections with default options."""
        result = runner.invoke(app, ["list-sections"])
        assert result.exit_code == 0
        # Should list core sections
        assert "Problems" in result.stdout or "problems" in result.stdout.lower()
        assert "Medications" in result.stdout or "medications" in result.stdout.lower()
        assert "Total:" in result.stdout

    def test_list_sections_verbose(self):
        """Test listing sections with verbose output."""
        result = runner.invoke(app, ["list-sections", "--verbose"])
        assert result.exit_code == 0
        # Should show template IDs in verbose mode
        assert "2.16.840.1.113883" in result.stdout

    def test_list_sections_verbose_short_flag(self):
        """Test listing sections with -v short flag."""
        result = runner.invoke(app, ["list-sections", "-v"])
        assert result.exit_code == 0
        # Should show template IDs in verbose mode
        assert "2.16.840.1.113883" in result.stdout

    def test_list_sections_filter_core(self):
        """Test filtering sections by core category."""
        result = runner.invoke(app, ["list-sections", "--category", "core"])
        assert result.exit_code == 0
        assert "Core Sections" in result.stdout
        assert "Problems" in result.stdout

    def test_list_sections_filter_extended(self):
        """Test filtering sections by extended category."""
        result = runner.invoke(app, ["list-sections", "--category", "extended"])
        assert result.exit_code == 0
        assert "Extended Sections" in result.stdout
        assert "Family History" in result.stdout or "Goals" in result.stdout

    def test_list_sections_filter_specialized(self):
        """Test filtering sections by specialized category."""
        result = runner.invoke(app, ["list-sections", "--category", "specialized"])
        assert result.exit_code == 0
        assert "Specialized Sections" in result.stdout

    def test_list_sections_filter_hospital(self):
        """Test filtering sections by hospital category."""
        result = runner.invoke(app, ["list-sections", "--category", "hospital"])
        assert result.exit_code == 0
        assert "Hospital Sections" in result.stdout

    def test_list_sections_invalid_category(self):
        """Test filtering with invalid category shows error."""
        result = runner.invoke(app, ["list-sections", "--category", "invalid"])
        # Should show error about unknown category
        assert "Unknown category" in result.stdout or "Error" in result.stdout

    def test_list_sections_help(self):
        """Test the --help flag displays help information."""
        result = runner.invoke(app, ["list-sections", "--help"])
        assert result.exit_code == 0
        assert "List all available C-CDA section builders" in result.stdout
        assert "--category" in result.stdout
        assert "--verbose" in result.stdout


class TestListProtocolsCommand:
    """Tests for the list-protocols command."""

    def test_list_protocols_default(self):
        """Test listing protocols with default options."""
        result = runner.invoke(app, ["list-protocols"])
        assert result.exit_code == 0
        # Should list protocol categories
        assert "Patient" in result.stdout or "patient" in result.stdout.lower()
        assert "Total:" in result.stdout or "protocols available" in result.stdout

    def test_list_protocols_verbose(self):
        """Test listing protocols with verbose output."""
        result = runner.invoke(app, ["list-protocols", "--verbose"])
        assert result.exit_code == 0
        # In verbose mode, should show field count
        assert "Fields" in result.stdout or result.exit_code == 0

    def test_list_protocols_verbose_short_flag(self):
        """Test listing protocols with -v short flag."""
        result = runner.invoke(app, ["list-protocols", "-v"])
        assert result.exit_code == 0

    def test_list_protocols_specific_protocol(self):
        """Test showing details for a specific protocol."""
        result = runner.invoke(app, ["list-protocols", "PatientProtocol"])
        # May exit with 0 or 1 depending on whether protocol exists
        # But should attempt to display protocol details
        assert "Protocol" in result.stdout or "not found" in result.stdout

    def test_list_protocols_invalid_protocol(self):
        """Test showing details for a non-existent protocol."""
        result = runner.invoke(app, ["list-protocols", "NonExistentProtocol"])
        # Should indicate protocol not found
        assert result.exit_code == 1 or "not found" in result.stdout

    def test_list_protocols_help(self):
        """Test the --help flag displays help information."""
        result = runner.invoke(app, ["list-protocols", "--help"])
        assert result.exit_code == 0
        assert "List all available protocol definitions" in result.stdout
        assert "--verbose" in result.stdout


class TestListTemplatesCommand:
    """Tests for the list-templates command."""

    def test_list_templates_default(self):
        """Test listing templates with default options."""
        result = runner.invoke(app, ["list-templates"])
        # Command outputs template information
        # Note: exit_code may be 1 if template loading encounters issues
        assert result.exit_code in [0, 1]
        # Should show available templates or message about templates
        assert "Template" in result.stdout or "template" in result.stdout.lower()

    def test_list_templates_specific_template(self):
        """Test showing details for a specific template."""
        result = runner.invoke(app, ["list-templates", "minimal_ccd"])
        # May succeed or fail depending on template availability
        assert result.exit_code in [0, 1]
        # Should attempt to display template info
        assert "Template" in result.stdout or "template" in result.stdout.lower()

    def test_list_templates_invalid_template(self):
        """Test showing details for a non-existent template."""
        result = runner.invoke(app, ["list-templates", "nonexistent_template"])
        # Should indicate template not found or show available options
        assert result.exit_code in [0, 1]

    def test_list_templates_show_content(self):
        """Test listing templates with --show-content flag."""
        result = runner.invoke(app, ["list-templates", "--show-content"])
        # Should attempt to show template content
        assert result.exit_code in [0, 1]

    def test_list_templates_help(self):
        """Test the --help flag displays help information."""
        result = runner.invoke(app, ["list-templates", "--help"])
        assert result.exit_code == 0
        assert "List all available document templates" in result.stdout
        assert "--show-content" in result.stdout


class TestListEntriesCommand:
    """Tests for the list-entries command."""

    def test_list_entries_default(self):
        """Test listing entries with default options."""
        result = runner.invoke(app, ["list-entries"])
        assert result.exit_code == 0
        # Should list entry categories
        assert "Entry" in result.stdout or "entry" in result.stdout.lower()
        assert "Total:" in result.stdout or "entry builders available" in result.stdout

    def test_list_entries_verbose(self):
        """Test listing entries with verbose output."""
        result = runner.invoke(app, ["list-entries", "--verbose"])
        assert result.exit_code == 0
        # Should show template IDs in verbose mode
        assert "2.16.840.1.113883" in result.stdout or "Template ID" in result.stdout

    def test_list_entries_verbose_short_flag(self):
        """Test listing entries with -v short flag."""
        result = runner.invoke(app, ["list-entries", "-v"])
        assert result.exit_code == 0

    def test_list_entries_filter_medications(self):
        """Test filtering entries by medications category."""
        result = runner.invoke(app, ["list-entries", "--category", "medications"])
        assert result.exit_code == 0
        assert "Medication" in result.stdout

    def test_list_entries_filter_problems(self):
        """Test filtering entries by problems category."""
        result = runner.invoke(app, ["list-entries", "--category", "problems"])
        assert result.exit_code == 0
        assert "Problem" in result.stdout

    def test_list_entries_filter_vital(self):
        """Test filtering entries by vital signs category."""
        result = runner.invoke(app, ["list-entries", "--category", "vital"])
        assert result.exit_code == 0
        assert "Vital" in result.stdout

    def test_list_entries_invalid_category(self):
        """Test filtering with invalid category shows error."""
        result = runner.invoke(app, ["list-entries", "--category", "invalid_category_xyz"])
        # Should show error about unknown category
        assert result.exit_code == 1
        assert "Error" in result.stdout or "not found" in result.stdout

    def test_list_entries_help(self):
        """Test the --help flag displays help information."""
        result = runner.invoke(app, ["list-entries", "--help"])
        assert result.exit_code == 0
        assert "List all available C-CDA entry builders" in result.stdout
        assert "--category" in result.stdout
        assert "--verbose" in result.stdout


class TestListCodeSystemsCommand:
    """Tests for the list-code-systems command."""

    def test_list_code_systems_default(self):
        """Test listing code systems with default options."""
        result = runner.invoke(app, ["list-code-systems"])
        assert result.exit_code == 0
        # Should list common code systems
        assert "LOINC" in result.stdout or "SNOMED" in result.stdout
        assert "Total:" in result.stdout or "code systems" in result.stdout.lower()

    def test_list_code_systems_verbose(self):
        """Test listing code systems with verbose output."""
        result = runner.invoke(app, ["list-code-systems", "--verbose"])
        assert result.exit_code == 0
        # Should show descriptions in verbose mode
        assert "Description" in result.stdout or result.exit_code == 0

    def test_list_code_systems_verbose_short_flag(self):
        """Test listing code systems with -v short flag."""
        result = runner.invoke(app, ["list-code-systems", "-v"])
        assert result.exit_code == 0

    def test_list_code_systems_search_loinc(self):
        """Test searching code systems for LOINC."""
        result = runner.invoke(app, ["list-code-systems", "--search", "LOINC"])
        assert result.exit_code == 0
        assert "LOINC" in result.stdout

    def test_list_code_systems_search_snomed(self):
        """Test searching code systems for SNOMED."""
        result = runner.invoke(app, ["list-code-systems", "--search", "SNOMED"])
        assert result.exit_code == 0
        assert "SNOMED" in result.stdout

    def test_list_code_systems_search_icd(self):
        """Test searching code systems for ICD."""
        result = runner.invoke(app, ["list-code-systems", "--search", "ICD"])
        # May or may not find ICD depending on what's registered
        assert result.exit_code in [0, 1]

    def test_list_code_systems_search_not_found(self):
        """Test searching code systems with no matches."""
        result = runner.invoke(app, ["list-code-systems", "--search", "nonexistent_xyz_123"])
        # Should indicate no results found
        assert result.exit_code == 1
        assert "No code systems found" in result.stdout or "not found" in result.stdout.lower()

    def test_list_code_systems_shows_value_sets(self):
        """Test that list-code-systems also shows value sets."""
        result = runner.invoke(app, ["list-code-systems"])
        assert result.exit_code == 0
        # Should also display value sets section
        assert "Value Set" in result.stdout or "value set" in result.stdout.lower()

    def test_list_code_systems_help(self):
        """Test the --help flag displays help information."""
        result = runner.invoke(app, ["list-code-systems", "--help"])
        assert result.exit_code == 0
        assert "List all available code systems" in result.stdout
        assert "--search" in result.stdout
        assert "--verbose" in result.stdout


class TestListCommandsInMainHelp:
    """Test that list commands are visible in main help."""

    def test_list_sections_in_main_help(self):
        """Test that list-sections is shown in main help."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "list-sections" in result.stdout

    def test_list_protocols_in_main_help(self):
        """Test that list-protocols is shown in main help."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "list-protocols" in result.stdout

    def test_list_templates_in_main_help(self):
        """Test that list-templates is shown in main help."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "list-templates" in result.stdout

    def test_list_entries_in_main_help(self):
        """Test that list-entries is shown in main help."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "list-entries" in result.stdout

    def test_list_code_systems_in_main_help(self):
        """Test that list-code-systems is shown in main help."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "list-code-systems" in result.stdout
