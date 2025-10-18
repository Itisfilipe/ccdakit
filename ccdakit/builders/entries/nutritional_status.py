"""Nutritional Status Observation entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.builders.entries.nutrition_assessment import NutritionAssessment
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.nutrition import NutritionalStatusProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class NutritionalStatusObservation(CDAElement):
    """
    Builder for C-CDA Nutritional Status Observation entry.

    Describes the overall nutritional status of the patient including findings
    related to nutritional status.

    Template: 2.16.840.1.113883.10.20.22.4.124
    Code: 75305-3 (Nutrition status) from LOINC

    Conformance Rules:
    - CONF:1098-29841: SHALL contain @classCode="OBS"
    - CONF:1098-29842: SHALL contain @moodCode="EVN"
    - CONF:1098-29843: SHALL contain templateId
    - CONF:1098-29844: templateId/@root="2.16.840.1.113883.10.20.22.4.124"
    - CONF:1098-29845: SHALL contain at least one [1..*] id
    - CONF:1098-29846: SHALL contain code
    - CONF:1098-29897: code/@code="75305-3"
    - CONF:1098-29898: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
    - CONF:1098-29852: SHALL contain statusCode
    - CONF:1098-29853: statusCode/@code="completed"
    - CONF:1098-31867: SHALL contain effectiveTime
    - CONF:1098-29854: SHALL contain value from Nutritional Status value set
    - CONF:1098-30323: SHALL contain at least one [1..*] entryRelationship
    - CONF:1098-30335: entryRelationship/@typeCode="SUBJ"
    - CONF:1098-30336: entryRelationship SHALL contain Nutrition Assessment

    Supports both R2.1 and R2.0 versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.124",
                extension=None,
                description="Nutritional Status Observation",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.124",
                extension=None,
                description="Nutritional Status Observation",
            ),
        ],
    }

    # Code system OIDs
    LOINC_OID = "2.16.840.1.113883.6.1"  # LOINC
    SNOMED_CT_OID = "2.16.840.1.113883.6.96"  # SNOMED CT

    # Fixed LOINC code for nutritional status
    NUTRITIONAL_STATUS_CODE = "75305-3"
    NUTRITIONAL_STATUS_DISPLAY = "Nutrition status"

    def __init__(
        self,
        nutritional_status: NutritionalStatusProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize NutritionalStatusObservation builder.

        Args:
            nutritional_status: Nutritional status data satisfying NutritionalStatusProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.nutritional_status = nutritional_status

    def build(self) -> etree.Element:
        """
        Build Nutritional Status Observation XML element.

        Returns:
            lxml Element for observation
        """
        # Create observation element (CONF:1098-29841, CONF:1098-29842)
        observation = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template IDs (CONF:1098-29843, CONF:1098-29844)
        self.add_template_ids(observation)

        # Add ID (CONF:1098-29845: SHALL contain at least one [1..*])
        self._add_id(observation)

        # Add code (CONF:1098-29846, CONF:1098-29897, CONF:1098-29898)
        code_elem = Code(
            code=self.NUTRITIONAL_STATUS_CODE,
            system="LOINC",
            display_name=self.NUTRITIONAL_STATUS_DISPLAY,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        observation.append(code_elem)

        # Add status code (CONF:1098-29852, CONF:1098-29853: SHALL be "completed")
        status_elem = StatusCode("completed").to_element()
        observation.append(status_elem)

        # Add effective time (CONF:1098-31867)
        time_elem = EffectiveTime(value=self.nutritional_status.date).to_element()
        observation.append(time_elem)

        # Add value (CONF:1098-29854: SHALL contain value from Nutritional Status value set)
        self._add_value(observation)

        # Add entry relationships with Nutrition Assessments
        # (CONF:1098-30323, CONF:1098-30335, CONF:1098-30336)
        self._add_assessments(observation)

        return observation

    def _add_id(self, observation: etree._Element) -> None:
        """
        Add ID element to observation.

        Args:
            observation: observation element
        """
        import uuid

        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=str(uuid.uuid4()),
        ).to_element()
        observation.append(id_elem)

    def _add_value(self, observation: etree._Element) -> None:
        """
        Add value element with nutritional status.

        The value SHALL contain a code from Nutritional Status value set
        (2.16.840.1.113883.1.11.20.2.7) (CONF:1098-29854).

        Args:
            observation: observation element
        """
        value_elem = etree.SubElement(
            observation,
            f"{{{NS}}}value",
            attrib={
                "{http://www.w3.org/2001/XMLSchema-instance}type": "CD",
            },
        )
        value_elem.set("code", self.nutritional_status.status_code)
        value_elem.set("codeSystem", self.SNOMED_CT_OID)
        value_elem.set("displayName", self.nutritional_status.status)

    def _add_assessments(self, observation: etree._Element) -> None:
        """
        Add entryRelationship elements with Nutrition Assessments.

        CONF:1098-30323: SHALL contain at least one [1..*] entryRelationship
        CONF:1098-30335: entryRelationship/@typeCode="SUBJ"
        CONF:1098-30336: entryRelationship SHALL contain Nutrition Assessment

        Args:
            observation: observation element
        """
        for assessment in self.nutritional_status.assessments:
            # Create entryRelationship element (CONF:1098-30335)
            entry_rel = etree.SubElement(
                observation,
                f"{{{NS}}}entryRelationship",
                typeCode="SUBJ",
            )

            # Add Nutrition Assessment (CONF:1098-30336)
            assessment_builder = NutritionAssessment(assessment, version=self.version)
            entry_rel.append(assessment_builder.to_element())
