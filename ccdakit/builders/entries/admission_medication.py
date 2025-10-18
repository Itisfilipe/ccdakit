"""Admission Medication entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.entries.medication import MedicationActivity
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.medication import MedicationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class AdmissionMedication(CDAElement):
    """
    Builder for C-CDA Admission Medication entry.

    This template represents medications taken by the patient prior to
    and at the time of admission to the facility.

    Wrapper act that contains a Medication Activity entry.
    Template ID: 2.16.840.1.113883.10.20.22.4.36
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.36",
                extension="2014-06-09",
                description="Admission Medication V2",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.36",
                extension="2014-06-09",
                description="Admission Medication V2",
            ),
        ],
    }

    # LOINC code for Medications on Admission
    LOINC_CODE = "42346-7"
    LOINC_OID = "2.16.840.1.113883.6.1"

    def __init__(
        self,
        medication: MedicationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize AdmissionMedication builder.

        Args:
            medication: Medication data satisfying MedicationProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.medication = medication

    def build(self) -> etree.Element:
        """
        Build Admission Medication XML element.

        Returns:
            lxml Element for act
        """
        # Create act element with required attributes
        # CONF:1098-7698, CONF:1098-7699
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="EVN",
        )

        # Add template IDs
        # CONF:1098-16758, CONF:1098-16759, CONF:1098-32524
        self.add_template_ids(act)

        # Add code element
        # CONF:1098-15518, CONF:1098-15519, CONF:1098-32152
        code_elem = etree.SubElement(act, f"{{{NS}}}code")
        code_elem.set("code", self.LOINC_CODE)
        code_elem.set("codeSystem", self.LOINC_OID)
        code_elem.set("codeSystemName", "LOINC")
        code_elem.set("displayName", "Medications on Admission")

        # Add entryRelationship containing Medication Activity
        # CONF:1098-7701, CONF:1098-7702, CONF:1098-15520
        entry_rel = etree.SubElement(
            act,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",
        )

        # Create and add Medication Activity
        med_activity = MedicationActivity(self.medication, version=self.version)
        entry_rel.append(med_activity.to_element())

        return act
