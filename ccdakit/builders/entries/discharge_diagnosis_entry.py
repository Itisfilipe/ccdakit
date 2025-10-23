"""Hospital Discharge Diagnosis entry builder for C-CDA documents."""

from typing import Sequence

from lxml import etree

from ccdakit.builders.entries.problem import ProblemObservation
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.discharge_diagnosis import DischargeDiagnosisProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class HospitalDischargeDiagnosis(CDAElement):
    """
    Builder for C-CDA Hospital Discharge Diagnosis entry.

    This template represents problems or diagnoses present at the time of discharge
    which occurred during hospitalization or need to be monitored after hospitalization.
    It requires at least one Problem Observation entry.

    Template ID: 2.16.840.1.113883.10.20.22.4.33
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.33",
                extension="2015-08-01",
                description="Hospital Discharge Diagnosis (V3)",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.33",
                extension="2014-06-09",
                description="Hospital Discharge Diagnosis (V2)",
            ),
        ],
    }

    def __init__(
        self,
        diagnoses: Sequence[DischargeDiagnosisProtocol],
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize HospitalDischargeDiagnosis builder.

        Args:
            diagnoses: List of discharge diagnoses satisfying DischargeDiagnosisProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.diagnoses = diagnoses

    def build(self) -> etree.Element:
        """
        Build Hospital Discharge Diagnosis XML element.

        Returns:
            lxml Element for act
        """
        # Create act element with required attributes (CONF:1198-7663, CONF:1198-7664)
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="EVN",
        )

        # Add template IDs (CONF:1198-16764, CONF:1198-16765, CONF:1198-32534)
        self.add_template_ids(act)

        # Add ID
        self._add_ids(act)

        # Add code (CONF:1198-19147, CONF:1198-19148, CONF:1198-32163)
        code_elem = etree.SubElement(act, f"{{{NS}}}code")
        code_elem.set("code", "11535-2")
        code_elem.set("codeSystem", "2.16.840.1.113883.6.1")
        code_elem.set("codeSystemName", "LOINC")
        code_elem.set("displayName", "Hospital discharge diagnosis")

        # Add entryRelationships with Problem Observations (CONF:1198-7666, CONF:1198-7667, CONF:1198-15536)
        for diagnosis in self.diagnoses:
            entry_rel = etree.SubElement(
                act,
                f"{{{NS}}}entryRelationship",
                typeCode="SUBJ",
            )

            # Create and add Problem Observation
            obs_builder = ProblemObservation(diagnosis, version=self.version)
            entry_rel.append(obs_builder.to_element())

        return act

    def _add_ids(self, act: etree._Element) -> None:
        """
        Add ID elements to act.

        Args:
            act: act element
        """
        import uuid

        # Add a generated ID
        id_elem = etree.SubElement(act, f"{{{NS}}}id")
        id_elem.set("root", "2.16.840.1.113883.19")
        id_elem.set("extension", str(uuid.uuid4()))
