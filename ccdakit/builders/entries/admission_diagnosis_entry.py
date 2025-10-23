"""Hospital Admission Diagnosis entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code
from ccdakit.builders.entries.problem import ProblemObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.admission_diagnosis import AdmissionDiagnosisProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class HospitalAdmissionDiagnosis(CDAElement):
    """
    Builder for C-CDA Hospital Admission Diagnosis (V3) entry.

    Represents problems or diagnoses identified by the clinician at the time
    of the patient's admission. This act may contain more than one Problem
    Observation to represent multiple diagnoses for a Hospital Admission.

    Template ID: 2.16.840.1.113883.10.20.22.4.34 (V3)
    Supports R2.1 (2015-08-01) version.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.34",
                extension="2015-08-01",
                description="Hospital Admission Diagnosis (V3) R2.1",
            ),
        ],
    }

    def __init__(
        self,
        diagnosis: AdmissionDiagnosisProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize HospitalAdmissionDiagnosis builder.

        Args:
            diagnosis: Admission diagnosis data satisfying AdmissionDiagnosisProtocol
            version: C-CDA version (R2.1)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.diagnosis = diagnosis

    def build(self) -> etree.Element:
        """
        Build Hospital Admission Diagnosis act XML element.

        Returns:
            lxml Element for act
        """
        # Create act element with required attributes (CONF:1198-7671, 1198-7672)
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="EVN",
        )

        # Add template ID (CONF:1198-16747, 1198-16748, 1198-32535)
        self.add_template_ids(act)

        # Add act code (CONF:1198-19145, 1198-19146, 1198-32162)
        code_elem = Code(
            code="46241-6",
            system="LOINC",
            display_name="Admission diagnosis",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        act.append(code_elem)

        # Add entryRelationship with Problem Observation (CONF:1198-7674, 1198-7675, 1198-15535)
        self._add_problem_observation(act)

        return act

    def _add_problem_observation(self, act: etree._Element) -> None:
        """
        Add entryRelationship with Problem Observation.

        Args:
            act: Hospital admission diagnosis act element
        """
        # Create entryRelationship (CONF:1198-7674, 1198-7675)
        entry_rel = etree.SubElement(
            act,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",
        )

        # Create and add Problem Observation (CONF:1198-15535)
        obs_builder = ProblemObservation(self.diagnosis, version=self.version)
        entry_rel.append(obs_builder.to_element())
