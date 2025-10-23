"""Tests for configuration system."""

import pytest

from ccdakit.core.base import CDAVersion
from ccdakit.core.config import (
    CDAConfig,
    OrganizationInfo,
    configure,
    get_config,
    reset_config,
)


def test_organization_info_minimal():
    """Test OrganizationInfo with minimal data."""
    org = OrganizationInfo(name="Test Clinic")
    assert org.name == "Test Clinic"
    assert org.npi is None
    assert org.tin is None
    assert org.oid_root is None


def test_organization_info_full():
    """Test OrganizationInfo with full data."""
    org = OrganizationInfo(
        name="Test Clinic",
        npi="1234567890",
        tin="12-3456789",
        oid_root="2.16.840.1.113883.3.TEST",
        address={"street": "123 Main St", "city": "Boston", "state": "MA"},
        phone="555-1234",
        email="info@test.example.com",
    )
    assert org.npi == "1234567890"
    assert org.tin == "12-3456789"
    assert org.address["city"] == "Boston"  # type: ignore
    assert org.phone == "555-1234"
    assert org.email == "info@test.example.com"


def test_cda_config_defaults():
    """Test CDAConfig default values."""
    org = OrganizationInfo(name="Test")
    config = CDAConfig(organization=org)

    assert config.version == CDAVersion.R2_1
    assert config.validate_on_build is True
    assert config.narrative_style == "table"
    assert config.prefer_snomed_over_icd10 is True
    assert config.include_narrative is True
    assert config.confidentiality_code == "N"


def test_cda_config_custom_values():
    """Test CDAConfig with custom values."""
    org = OrganizationInfo(name="Test")
    config = CDAConfig(
        organization=org,
        version=CDAVersion.R2_0,
        validate_on_build=False,
        narrative_style="list",
        confidentiality_code="R",  # Restricted
    )

    assert config.version == CDAVersion.R2_0
    assert config.validate_on_build is False
    assert config.narrative_style == "list"
    assert config.confidentiality_code == "R"


def test_configure_and_get():
    """Test configure() and get_config()."""
    reset_config()  # Clean slate

    org = OrganizationInfo(name="Test")
    config = CDAConfig(organization=org, version=CDAVersion.R2_0)

    configure(config)

    retrieved = get_config()
    assert retrieved.version == CDAVersion.R2_0
    assert retrieved.organization.name == "Test"

    reset_config()  # Clean up


def test_get_config_not_configured():
    """Test get_config() raises when not configured."""
    reset_config()

    with pytest.raises(RuntimeError, match="not configured"):
        get_config()

    reset_config()


def test_reset_config():
    """Test reset_config() clears configuration."""
    org = OrganizationInfo(name="Test")
    config = CDAConfig(organization=org)

    configure(config)
    assert get_config() is not None

    reset_config()

    with pytest.raises(RuntimeError):
        get_config()


def test_config_with_schema_paths():
    """Test CDAConfig with validation paths."""
    org = OrganizationInfo(name="Test")
    config = CDAConfig(
        organization=org,
        xsd_schema_path="/path/to/CDA.xsd",
        schematron_path="/path/to/schematron.sch",
    )

    assert config.xsd_schema_path == "/path/to/CDA.xsd"
    assert config.schematron_path == "/path/to/schematron.sch"


def test_config_with_custom_namespaces():
    """Test CDAConfig with custom namespaces."""
    org = OrganizationInfo(name="Test")
    config = CDAConfig(
        organization=org,
        custom_namespaces={"custom": "http://example.com/custom"},
    )

    assert "custom" in config.custom_namespaces
    assert config.custom_namespaces["custom"] == "http://example.com/custom"


def test_config_with_id_generator():
    """Test CDAConfig with custom ID generator."""

    def custom_id_gen(entity_type: str, entity_id: str) -> dict:
        return {"root": "custom.oid", "extension": entity_id}

    org = OrganizationInfo(name="Test")
    config = CDAConfig(organization=org, id_generator=custom_id_gen)

    assert config.id_generator is not None
    result = config.id_generator("problem", "123")
    assert result["root"] == "custom.oid"
    assert result["extension"] == "123"


def test_configure_overwrites_existing_config():
    """Test that configure() overwrites existing configuration."""
    reset_config()

    org1 = OrganizationInfo(name="First Org")
    config1 = CDAConfig(organization=org1, version=CDAVersion.R2_0)
    configure(config1)

    # Get first config
    retrieved1 = get_config()
    assert retrieved1.organization.name == "First Org"
    assert retrieved1.version == CDAVersion.R2_0

    # Configure with new config
    org2 = OrganizationInfo(name="Second Org")
    config2 = CDAConfig(organization=org2, version=CDAVersion.R2_1)
    configure(config2)

    # Get second config - should be different
    retrieved2 = get_config()
    assert retrieved2.organization.name == "Second Org"
    assert retrieved2.version == CDAVersion.R2_1

    reset_config()


def test_get_config_error_message():
    """Test get_config() error message when not configured."""
    reset_config()

    try:
        get_config()
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert "not configured" in str(e)
        assert "configure()" in str(e)

    reset_config()
