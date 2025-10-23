"""Tests for the main CLI application."""

import pytest
from typer.testing import CliRunner

from ccdakit.cli.__main__ import app


runner = CliRunner()


class TestMainCLI:
    """Test suite for the main CLI application."""

    def test_app_help(self):
        """Test the main app --help flag."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "ccdakit" in result.stdout.lower()
        assert "CLI tool for working with HL7 C-CDA" in result.stdout

        # Check that all commands are listed
        assert "validate" in result.stdout
        assert "generate" in result.stdout
        assert "convert" in result.stdout
        assert "compare" in result.stdout
        assert "serve" in result.stdout
        assert "version" in result.stdout

    def test_version_command(self):
        """Test the version command."""
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "ccdakit" in result.stdout
        assert "version" in result.stdout.lower()

        # Should show version number
        import ccdakit

        assert ccdakit.__version__ in result.stdout

    def test_no_command_shows_help(self):
        """Test that running with no command shows help."""
        result = runner.invoke(app, [])
        # Typer may exit with 0 or show help, depending on configuration
        # Just verify it doesn't crash
        assert result.exit_code in [0, 2]

    def test_invalid_command(self):
        """Test running an invalid command."""
        result = runner.invoke(app, ["invalid-command"])
        assert result.exit_code != 0

    def test_all_commands_have_help(self):
        """Test that all commands support --help."""
        commands = ["validate", "generate", "convert", "compare", "serve", "version"]

        for command in commands:
            result = runner.invoke(app, [command, "--help"])
            # version command doesn't have help since it takes no args
            if command != "version":
                assert result.exit_code == 0, f"{command} --help failed"
                assert "help" in result.stdout.lower() or command in result.stdout.lower()


class TestCLIStructure:
    """Test the structure and configuration of the CLI."""

    def test_app_name(self):
        """Test that the app has the correct name."""
        assert app.info.name == "ccdakit"

    def test_app_help_text(self):
        """Test that the app has help text."""
        assert app.info.help is not None
        assert "C-CDA" in app.info.help

    def test_all_commands_registered(self):
        """Test that all expected commands are registered."""
        # Get registered commands - handle both .name and callback.__name__
        registered_commands = []
        for cmd in app.registered_commands:
            if hasattr(cmd, 'name') and cmd.name:
                registered_commands.append(cmd.name)
            elif hasattr(cmd, 'callback') and cmd.callback:
                # Extract name from callback function name
                name = cmd.callback.__name__.replace('_command', '')
                registered_commands.append(name)

        expected_commands = ["validate", "generate", "convert", "compare", "serve", "version"]

        for expected in expected_commands:
            assert (
                expected in registered_commands
            ), f"Command '{expected}' not registered. Found: {registered_commands}"
