"""Complication entry builder for C-CDA documents.

Complications are represented using Problem Observation entries as specified
in the Complications Section (Template ID: 2.16.840.1.113883.10.20.22.2.37).
"""

from lxml import etree

from ccdakit.builders.entries.problem import ProblemObservation
from ccdakit.core.base import CDAElement, CDAVersion
from ccdakit.protocols.complication import ComplicationProtocol


class ComplicationObservation(CDAElement):
    """
    Builder for C-CDA Complication Observation entry.

    Complications are represented using the Problem Observation template
    (2.16.840.1.113883.10.20.22.4.4) as specified in the C-CDA standard.

    This class is a wrapper around ProblemObservation that provides
    semantic clarity when working with complications specifically.
    """

    def __init__(
        self,
        complication: ComplicationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ComplicationObservation builder.

        Args:
            complication: Complication data satisfying ComplicationProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.complication = complication
        # Delegate to ProblemObservation for actual implementation
        self._problem_obs = ProblemObservation(complication, version=version, **kwargs)

    def build(self) -> etree.Element:
        """
        Build Complication Observation XML element.

        Returns:
            lxml Element for observation (delegates to ProblemObservation)
        """
        return self._problem_obs.build()
