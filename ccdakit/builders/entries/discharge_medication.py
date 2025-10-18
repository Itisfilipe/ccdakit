"""Discharge Medication entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.entries.medication import MedicationActivity
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.medication import MedicationProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class DischargeMedication(CDAElement):
    """
    Builder for C-CDA Discharge Medication entry.

    Represents medications that the patient is intended to take (or stop) after discharge.
    This is a wrapper act that contains a Medication Activity.

    Conforms to:
    - Discharge Medication (V3) template (2.16.840.1.113883.10.20.22.4.35:2016-03-01)

    Supports both R2.1 (2016-03-01) and R2.0 (2016-03-01) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.35",
                extension="2016-03-01",
                description="Discharge Medication (V3) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.35",
                extension="2016-03-01",
                description="Discharge Medication (V3) R2.0",
            ),
        ],
    }

    # LOINC code system OID
    LOINC_OID = "2.16.840.1.113883.6.1"

    def __init__(
        self,
        medication: MedicationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize DischargeMedication builder.

        Args:
            medication: Medication data satisfying MedicationProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.medication = medication

    def build(self) -> etree.Element:
        """
        Build Discharge Medication XML element.

        Returns:
            lxml Element for act
        """
        # Create act element with required attributes (CONF:1198-7689, CONF:1198-7690)
        act = etree.Element(
            f"{{{NS}}}act",
            classCode="ACT",
            moodCode="EVN",
        )

        # Add template IDs (CONF:1198-16760)
        self.add_template_ids(act)

        # Add code element (CONF:1198-7691)
        self._add_code(act)

        # Add statusCode (CONF:1198-32779)
        status_elem = etree.SubElement(act, f"{{{NS}}}statusCode")
        status_elem.set("code", "completed")  # CONF:1198-32780

        # Add entryRelationship with Medication Activity (CONF:1198-7692)
        self._add_medication_activity(act)

        return act

    def _add_code(self, act: etree._Element) -> None:
        """
        Add code element to act.

        Args:
            act: act element
        """
        # CONF:1198-7691 - SHALL contain exactly one [1..1] code
        code_elem = etree.SubElement(act, f"{{{NS}}}code")

        # CONF:1198-19161 - code SHALL be "10183-2" Hospital discharge medication
        code_elem.set("code", "10183-2")

        # CONF:1198-32159 - codeSystem SHALL be LOINC
        code_elem.set("codeSystem", self.LOINC_OID)
        code_elem.set("codeSystemName", "LOINC")
        code_elem.set("displayName", "Hospital discharge medication")

        # CONF:1198-32952 - SHALL contain exactly one [1..1] translation
        translation = etree.SubElement(code_elem, f"{{{NS}}}translation")

        # CONF:1198-32953 - translation code SHALL be "75311-1" Discharge Medication
        translation.set("code", "75311-1")

        # CONF:1198-32954 - translation codeSystem SHALL be LOINC
        translation.set("codeSystem", self.LOINC_OID)
        translation.set("codeSystemName", "LOINC")
        translation.set("displayName", "Discharge Medication")

    def _add_medication_activity(self, act: etree._Element) -> None:
        """
        Add entryRelationship with Medication Activity.

        Args:
            act: act element
        """
        # CONF:1198-7692 - SHALL contain at least one [1..*] entryRelationship
        entry_rel = etree.SubElement(
            act,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",  # CONF:1198-7693
        )

        # CONF:1198-15525 - SHALL contain Medication Activity (V2)
        med_builder = MedicationActivity(self.medication, version=self.version)
        entry_rel.append(med_builder.to_element())
