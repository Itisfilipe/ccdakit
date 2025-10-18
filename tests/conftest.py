"""Shared pytest fixtures for ccdakit tests."""

import pytest

from ccdakit.core.base import CDAVersion
from ccdakit.core.config import CDAConfig, OrganizationInfo, configure, reset_config


@pytest.fixture(autouse=True)
def reset_global_config():
    """Reset global config before each test to avoid test pollution."""
    reset_config()
    yield
    reset_config()


@pytest.fixture
def sample_organization():
    """Provide a sample organization for testing."""
    return OrganizationInfo(
        name="Test Medical Center",
        npi="1234567890",
        oid_root="2.16.840.1.113883.3.TEST",
        address={
            "street": "123 Main St",
            "city": "Boston",
            "state": "MA",
            "zip": "02101",
        },
        phone="555-1234",
        email="info@test.example.com",
    )


@pytest.fixture
def sample_config(sample_organization):
    """Provide a sample CDA configuration for testing."""
    return CDAConfig(
        organization=sample_organization,
        version=CDAVersion.R2_1,
        validate_on_build=False,  # Disable validation in tests by default
    )


@pytest.fixture
def configured_app(sample_config):
    """Configure the application with sample config."""
    configure(sample_config)
    return sample_config
