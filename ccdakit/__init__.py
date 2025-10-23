"""
ccdakit: Python library for generating HL7 C-CDA clinical documents.

This library provides a type-safe, protocol-oriented approach to generating
C-CDA (Consolidated Clinical Document Architecture) documents for healthcare
interoperability.

Basic Usage:
    from ccdakit import (
        configure,
        CDAConfig,
        OrganizationInfo,
        CDAVersion,
        ClinicalDocument,
        ProblemsSection,
    )

    # Configure the library
    config = CDAConfig(
        organization=OrganizationInfo(
            name="My Clinic",
            npi="1234567890",
            oid_root="2.16.840.1.113883.3.EXAMPLE"
        ),
        version=CDAVersion.R2_1,
    )
    configure(config)

    # Generate a document
    doc = ClinicalDocument(
        patient=my_patient,
        sections=[ProblemsSection(problems)],
    )

    # Get XML string
    xml = doc.to_string()
"""

import logging

# Core exports
# Builder exports
from ccdakit.builders import ClinicalDocument

# Section exports
from ccdakit.builders.sections import (
    AllergiesSection,
    EncountersSection,
    ImmunizationsSection,
    MedicationsSection,
    ProblemsSection,
    ProceduresSection,
    ResultsSection,
    SocialHistorySection,
    VitalSignsSection,
)
from ccdakit.core import (
    CDAConfig,
    CDAVersion,
    OrganizationInfo,
    ValidationError,
    ValidationIssue,
    ValidationLevel,
    ValidationResult,
    configure,
    get_config,
    reset_config,
)

# Protocol exports
from ccdakit.protocols import (
    AddressProtocol,
    AllergyProtocol,
    AuthorProtocol,
    EncounterProtocol,
    MedicationProtocol,
    OrganizationProtocol,
    PatientProtocol,
    ProblemProtocol,
    ProcedureProtocol,
    ResultObservationProtocol,
    ResultOrganizerProtocol,
    SmokingStatusProtocol,
    TelecomProtocol,
)


__version__ = "0.1.0a1"
__author__ = "Filipe Amaral"

# Set up null handler by default (library best practice)
# Applications can configure logging as needed
logging.getLogger(__name__).addHandler(logging.NullHandler())


__all__ = [
    # Version info
    "__version__",
    "__author__",
    # Core
    "CDAConfig",
    "CDAVersion",
    "OrganizationInfo",
    "configure",
    "get_config",
    "reset_config",
    "ValidationError",
    "ValidationIssue",
    "ValidationLevel",
    "ValidationResult",
    # Document builder
    "ClinicalDocument",
    # Sections
    "ProblemsSection",
    "MedicationsSection",
    "AllergiesSection",
    "ImmunizationsSection",
    "VitalSignsSection",
    "EncountersSection",
    "ProceduresSection",
    "ResultsSection",
    "SocialHistorySection",
    # Protocols
    "PatientProtocol",
    "AddressProtocol",
    "TelecomProtocol",
    "ProblemProtocol",
    "MedicationProtocol",
    "AllergyProtocol",
    "AuthorProtocol",
    "OrganizationProtocol",
    "EncounterProtocol",
    "ProcedureProtocol",
    "ResultObservationProtocol",
    "ResultOrganizerProtocol",
    "SmokingStatusProtocol",
]
