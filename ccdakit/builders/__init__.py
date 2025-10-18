"""Builders for C-CDA XML elements."""

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.builders.demographics import Address, Telecom
from ccdakit.builders.document import ClinicalDocument

# Document-level builders for specific document types
from ccdakit.builders.documents import ContinuityOfCareDocument, DischargeSummary


__all__ = [
    # Common builders
    "Code",
    "EffectiveTime",
    "Identifier",
    "StatusCode",
    # Demographic builders
    "Address",
    "Telecom",
    # Document builders
    "ClinicalDocument",
    "ContinuityOfCareDocument",
    "DischargeSummary",
]
