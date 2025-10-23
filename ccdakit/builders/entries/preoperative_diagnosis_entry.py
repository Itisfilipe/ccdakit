"""Preoperative Diagnosis entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.problem import ProblemObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.preoperative_diagnosis import PreoperativeDiagnosisProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class PreoperativeDiagnosisEntry(CDAElement):
    """
    Builder for C-CDA Preoperative Diagnosis entry.

    This template represents the surgical diagnosis or diagnoses assigned to
    the patient before the surgical procedure and is the reason for the surgery.
    The preoperative diagnosis is, in the surgeon's opinion, the diagnosis that
    will be confirmed during surgery.

    The entry is an Act wrapper that contains a Problem Observation.

    Template ID: 2.16.840.1.113883.10.20.22.4.65 (V3, 2015-08-01)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.65",
                extension="2015-08-01",
                description="Preoperative Diagnosis R2.1",
            ),
        ],
    }

    def __init__(
        self,
        diagnosis: PreoperativeDiagnosisProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize PreoperativeDiagnosisEntry builder.

        Args:
            diagnosis: Preoperative diagnosis data satisfying PreoperativeDiagnosisProtocol
            version: C-CDA version (R2.1)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.diagnosis = diagnosis

    def build(self) -> etree.Element:
        """
        Build Preoperative Diagnosis Act XML element.

        Returns:
            lxml Element for act
        """
        # Create act element with required attributes (CONF:1198-10090, CONF:1198-10091)
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="EVN",
        )

        # Add template IDs (CONF:1198-16770, CONF:1198-16771, CONF:1198-32540)
        self.add_template_ids(act)

        # Add code (CONF:1198-19155, CONF:1198-19156, CONF:1198-32167)
        code_elem = Code(
            code="10219-4",
            system="LOINC",
            display_name="Preoperative Diagnosis",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        act.append(code_elem)

        # Add entryRelationship with Problem Observation (CONF:1198-10093, CONF:1198-10094, CONF:1198-15605)
        entry_rel = etree.SubElement(
            act,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",
        )

        # Create Problem Observation from diagnosis data
        # We adapt the PreoperativeDiagnosisProtocol to ProblemProtocol interface
        obs_builder = ProblemObservation(self.diagnosis, version=self.version)
        entry_rel.append(obs_builder.to_element())

        return act
