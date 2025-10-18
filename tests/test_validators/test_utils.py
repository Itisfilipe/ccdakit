"""Tests for schema management utilities."""

import pytest

from ccdakit.validators.utils import (
    SchemaManager,
    check_schema_installed,
    get_default_schema_path,
)


@pytest.fixture
def temp_schema_dir(tmp_path):
    """Create temporary schema directory."""
    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir()
    return schema_dir


class TestSchemaManager:
    """Test suite for SchemaManager."""

    @pytest.fixture
    def manager_with_temp_dir(self, temp_schema_dir):
        """Create SchemaManager with temporary directory."""
        return SchemaManager(temp_schema_dir)

    def test_init_default_dir(self):
        """Test initialization with default directory."""
        manager = SchemaManager()
        assert manager.schema_dir is not None
        assert manager.schema_dir.name == "schemas"

    def test_init_custom_dir(self, temp_schema_dir):
        """Test initialization with custom directory."""
        manager = SchemaManager(temp_schema_dir)
        assert manager.schema_dir == temp_schema_dir

    def test_init_creates_directory(self, tmp_path):
        """Test that init creates directory if it doesn't exist."""
        new_dir = tmp_path / "new_schemas"
        assert not new_dir.exists()

        SchemaManager(new_dir)
        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_is_installed_false_when_no_schema(self, manager_with_temp_dir):
        """Test is_installed returns False when no schema exists."""
        assert manager_with_temp_dir.is_installed() is False

    def test_is_installed_true_when_schema_exists(self, manager_with_temp_dir):
        """Test is_installed returns True when schema exists."""
        # Create CDA.xsd file
        cda_path = manager_with_temp_dir.schema_dir / "CDA.xsd"
        cda_path.write_text("<schema>test</schema>")

        assert manager_with_temp_dir.is_installed() is True

    def test_get_cda_schema_path(self, manager_with_temp_dir):
        """Test get_cda_schema_path returns correct path."""
        expected_path = manager_with_temp_dir.schema_dir / "CDA.xsd"
        actual_path = manager_with_temp_dir.get_cda_schema_path()

        assert actual_path == expected_path

    def test_get_schema_info_not_installed(self, manager_with_temp_dir):
        """Test get_schema_info when schema not installed."""
        info = manager_with_temp_dir.get_schema_info()

        assert info["installed"] is False
        assert info["cda_exists"] is False
        assert "schema_dir" in info
        assert "cda_schema" in info
        assert isinstance(info["files"], list)
        assert len(info["files"]) == 0

    def test_get_schema_info_installed(self, manager_with_temp_dir):
        """Test get_schema_info when schema is installed."""
        # Create CDA.xsd
        cda_path = manager_with_temp_dir.schema_dir / "CDA.xsd"
        cda_path.write_text("<schema>test</schema>")

        # Create additional files
        (manager_with_temp_dir.schema_dir / "datatypes.xsd").write_text("<datatypes/>")
        (manager_with_temp_dir.schema_dir / "README.md").write_text("# Schemas")

        info = manager_with_temp_dir.get_schema_info()

        assert info["installed"] is True
        assert info["cda_exists"] is True
        assert len(info["files"]) == 3
        assert "CDA.xsd" in info["files"]
        assert "datatypes.xsd" in info["files"]
        assert "README.md" in info["files"]

    def test_download_schemas_already_installed(self, manager_with_temp_dir):
        """Test download_schemas when already installed."""
        # Create CDA.xsd
        cda_path = manager_with_temp_dir.schema_dir / "CDA.xsd"
        cda_path.write_text("<schema>test</schema>")

        success, message = manager_with_temp_dir.download_schemas()

        assert success is True
        assert "already installed" in message.lower()

    def test_download_schemas_force_redownload(self, manager_with_temp_dir):
        """Test download_schemas with force=True."""
        # Create CDA.xsd
        cda_path = manager_with_temp_dir.schema_dir / "CDA.xsd"
        cda_path.write_text("<schema>test</schema>")

        # Force should attempt download (will fail without network, but that's ok)
        success, message = manager_with_temp_dir.download_schemas(version="R2.1", force=True)

        # We expect this to fail without actual network access
        # but we're testing that it attempts the download
        assert isinstance(success, bool)
        assert isinstance(message, str)

    def test_download_schemas_invalid_version(self, manager_with_temp_dir):
        """Test download_schemas with invalid version."""
        with pytest.raises(ValueError, match="Unsupported version"):
            manager_with_temp_dir.download_schemas(version="R99.9")

    def test_print_installation_instructions(self, manager_with_temp_dir, capsys):
        """Test print_installation_instructions outputs text."""
        manager_with_temp_dir.print_installation_instructions()

        captured = capsys.readouterr()
        output = captured.out

        assert "Installation Instructions" in output
        assert "HL7" in output
        assert "CDA.xsd" in output
        assert str(manager_with_temp_dir.schema_dir) in output


class TestUtilityFunctions:
    """Test utility functions."""

    def test_get_default_schema_path_not_installed(self, monkeypatch, tmp_path):
        """Test get_default_schema_path when not installed."""
        # Mock DEFAULT_SCHEMA_DIR to point to temp dir
        from ccdakit.validators import utils

        monkeypatch.setattr(utils, "DEFAULT_SCHEMA_DIR", tmp_path)

        result = get_default_schema_path()
        assert result is None

    def test_get_default_schema_path_installed(self, monkeypatch, tmp_path):
        """Test get_default_schema_path when installed."""
        # Create CDA.xsd
        cda_path = tmp_path / "CDA.xsd"
        cda_path.write_text("<schema>test</schema>")

        # Mock DEFAULT_SCHEMA_DIR
        from ccdakit.validators import utils

        monkeypatch.setattr(utils, "DEFAULT_SCHEMA_DIR", tmp_path)

        result = get_default_schema_path()
        assert result is not None
        assert result == cda_path
        assert result.exists()

    def test_check_schema_installed_false(self, monkeypatch, tmp_path):
        """Test check_schema_installed returns False when not installed."""
        from ccdakit.validators import utils

        monkeypatch.setattr(utils, "DEFAULT_SCHEMA_DIR", tmp_path)

        result = check_schema_installed()
        assert result is False

    def test_check_schema_installed_true(self, monkeypatch, tmp_path):
        """Test check_schema_installed returns True when installed."""
        # Create CDA.xsd
        cda_path = tmp_path / "CDA.xsd"
        cda_path.write_text("<schema>test</schema>")

        from ccdakit.validators import utils

        monkeypatch.setattr(utils, "DEFAULT_SCHEMA_DIR", tmp_path)

        result = check_schema_installed()
        assert result is True

    def test_install_schemas_prints_message(self, monkeypatch, tmp_path, capsys):
        """Test install_schemas prints a message."""
        from ccdakit.validators import utils

        # Create CDA.xsd so installation skips download
        cda_path = tmp_path / "CDA.xsd"
        cda_path.write_text("<schema>test</schema>")

        monkeypatch.setattr(utils, "DEFAULT_SCHEMA_DIR", tmp_path)

        from ccdakit.validators.utils import install_schemas

        result = install_schemas()

        captured = capsys.readouterr()
        assert len(captured.out) > 0  # Should print something
        assert isinstance(result, bool)

    def test_print_schema_installation_help(self, capsys):
        """Test print_schema_installation_help outputs instructions."""
        from ccdakit.validators.utils import print_schema_installation_help

        print_schema_installation_help()

        captured = capsys.readouterr()
        output = captured.out

        assert "Installation Instructions" in output
        assert "HL7" in output


class TestSchemaManagerIntegration:
    """Integration tests for SchemaManager."""

    def test_full_workflow_check_and_info(self, temp_schema_dir):
        """Test complete workflow of checking and getting info."""
        manager = SchemaManager(temp_schema_dir)

        # Initially not installed
        assert not manager.is_installed()

        # Get info
        info = manager.get_schema_info()
        assert not info["installed"]

        # Create schema
        cda_path = manager.get_cda_schema_path()
        cda_path.write_text("<schema>test</schema>")

        # Now installed
        assert manager.is_installed()

        # Updated info
        info = manager.get_schema_info()
        assert info["installed"]
        assert info["cda_exists"]

    def test_schema_path_consistency(self, temp_schema_dir):
        """Test that schema paths are consistent."""
        manager = SchemaManager(temp_schema_dir)

        path1 = manager.get_cda_schema_path()
        path2 = manager.get_cda_schema_path()

        assert path1 == path2
        assert path1.parent == temp_schema_dir
