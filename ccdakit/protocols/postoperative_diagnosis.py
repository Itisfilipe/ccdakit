"""Postoperative Diagnosis-related protocols for C-CDA documents.

The Postoperative Diagnosis section records diagnoses discovered or confirmed
during surgery. Often it is the same as the preoperative diagnosis.

Template ID: 2.16.840.1.113883.10.20.22.2.35
Section Code: LOINC 10218-6 "Postoperative Diagnosis"

This section uses the same Problem Observation structure as the Problem Section,
so we reuse the ProblemProtocol for consistency.
"""

# Re-export the protocols from problem module for convenience
from ccdakit.protocols.problem import PersistentIDProtocol, ProblemProtocol


__all__ = ["PostoperativeDiagnosisProtocol", "PersistentIDProtocol"]

# Alias for clarity in postoperative context
PostoperativeDiagnosisProtocol = ProblemProtocol
