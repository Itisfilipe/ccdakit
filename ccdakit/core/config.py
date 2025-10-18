"""Configuration system for ccdakit."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional

from ccdakit.core.base import CDAVersion


@dataclass
class OrganizationInfo:
    """Organization/custodian information."""

    name: str
    npi: Optional[str] = None
    tin: Optional[str] = None  # Tax ID Number
    oid_root: Optional[str] = None  # Organization's OID namespace
    address: Optional[Dict[str, str]] = None
    phone: Optional[str] = None
    email: Optional[str] = None


@dataclass
class CDAConfig:
    """Global configuration for C-CDA generation."""

    # Organization (custodian)
    organization: OrganizationInfo

    # Version
    version: CDAVersion = CDAVersion.R2_1

    # Validation
    validate_on_build: bool = True
    xsd_schema_path: Optional[str] = None
    schematron_path: Optional[str] = None

    # Code system preferences
    prefer_snomed_over_icd10: bool = True

    # Persistent ID strategy
    id_generator: Optional[Callable[..., Any]] = None

    # Narrative options
    include_narrative: bool = True
    narrative_style: str = "table"  # 'table', 'list', or 'paragraph'

    # Document metadata
    document_id_root: Optional[str] = None
    confidentiality_code: str = "N"  # Normal

    # Custom extensions
    custom_namespaces: Dict[str, str] = field(default_factory=dict)
    custom_template_ids: Dict[str, list] = field(default_factory=dict)


# Global config instance
_config: Optional[CDAConfig] = None


def configure(config: CDAConfig) -> None:
    """
    Set global configuration.

    Args:
        config: CDAConfig instance
    """
    global _config
    _config = config


def get_config() -> CDAConfig:
    """
    Get current configuration.

    Returns:
        Current CDAConfig instance

    Raises:
        RuntimeError: If not configured
    """
    if _config is None:
        raise RuntimeError("ccdakit not configured. Call configure() before generating documents.")
    return _config


def reset_config() -> None:
    """Reset configuration (useful for testing)."""
    global _config
    _config = None
