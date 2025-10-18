"""Past Medical History-related protocols for C-CDA documents.

Past Medical History section uses the same Problem Observation structure
as the Problem Section, so we reuse the ProblemProtocol.
"""

# Re-export the protocols from problem module for convenience
from ccdakit.protocols.problem import PersistentIDProtocol, ProblemProtocol

__all__ = ["ProblemProtocol", "PersistentIDProtocol"]
