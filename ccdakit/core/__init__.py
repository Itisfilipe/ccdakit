"""Core infrastructure for pyccda."""

from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.core.config import CDAConfig, OrganizationInfo, configure, get_config, reset_config
from ccdakit.core.null_flavor import NullFlavor, get_null_flavor_for_missing, is_null_flavor
from ccdakit.core.validation import (
    ValidationError,
    ValidationIssue,
    ValidationLevel,
    ValidationResult,
)


__all__ = [
    # Base classes
    "CDAElement",
    "CDAVersion",
    "TemplateConfig",
    # Configuration
    "CDAConfig",
    "OrganizationInfo",
    "configure",
    "get_config",
    "reset_config",
    # Validation
    "ValidationLevel",
    "ValidationIssue",
    "ValidationResult",
    "ValidationError",
    # Null flavors
    "NullFlavor",
    "get_null_flavor_for_missing",
    "is_null_flavor",
]
