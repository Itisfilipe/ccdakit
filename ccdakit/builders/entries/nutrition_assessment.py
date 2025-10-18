"""Nutrition Assessment entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.nutrition import NutritionAssessmentProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class NutritionAssessment(CDAElement):
    """
    Builder for C-CDA Nutrition Assessment entry.

    Represents the patient's nutrition abilities and habits including intake,
    diet requirements or diet followed.

    Template: 2.16.840.1.113883.10.20.22.4.138
    Code: 75303-8 (Nutrition assessment) from LOINC

    Conformance Rules:
    - CONF:1098-32914: SHALL contain @classCode="OBS"
    - CONF:1098-32915: SHALL contain @moodCode="EVN"
    - CONF:1098-32916: SHALL contain templateId
    - CONF:1098-32917: templateId/@root="2.16.840.1.113883.10.20.22.4.138"
    - CONF:1098-32918: SHALL contain at least one [1..*] id
    - CONF:1098-32919: SHALL contain code
    - CONF:1098-32926: code/@code="75303-8"
    - CONF:1098-32927: code/@codeSystem="2.16.840.1.113883.6.1" (LOINC)
    - CONF:1098-32920: SHALL contain statusCode
    - CONF:1098-32921: statusCode/@code="completed"
    - CONF:1098-32923: SHALL contain effectiveTime
    - CONF:1098-32922: SHALL contain value
    - CONF:1098-32925: value SHOULD contain code from SNOMED CT if xsi:type="CD"

    Supports both R2.1 and R2.0 versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.138",
                extension=None,
                description="Nutrition Assessment",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.138",
                extension=None,
                description="Nutrition Assessment",
            ),
        ],
    }

    # Code system OIDs
    LOINC_OID = "2.16.840.1.113883.6.1"  # LOINC
    SNOMED_CT_OID = "2.16.840.1.113883.6.96"  # SNOMED CT

    # Fixed LOINC code for nutrition assessment
    NUTRITION_ASSESSMENT_CODE = "75303-8"
    NUTRITION_ASSESSMENT_DISPLAY = "Nutrition assessment"

    def __init__(
        self,
        assessment: NutritionAssessmentProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize NutritionAssessment builder.

        Args:
            assessment: Nutrition assessment data satisfying NutritionAssessmentProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.assessment = assessment

    def build(self) -> etree.Element:
        """
        Build Nutrition Assessment Observation XML element.

        Returns:
            lxml Element for observation
        """
        # Create observation element (CONF:1098-32914, CONF:1098-32915)
        observation = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template IDs (CONF:1098-32916, CONF:1098-32917)
        self.add_template_ids(observation)

        # Add ID (CONF:1098-32918: SHALL contain at least one [1..*])
        self._add_id(observation)

        # Add code (CONF:1098-32919, CONF:1098-32926, CONF:1098-32927)
        code_elem = Code(
            code=self.NUTRITION_ASSESSMENT_CODE,
            system="LOINC",
            display_name=self.NUTRITION_ASSESSMENT_DISPLAY,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        observation.append(code_elem)

        # Add status code (CONF:1098-32920, CONF:1098-32921: SHALL be "completed")
        status_elem = StatusCode("completed").to_element()
        observation.append(status_elem)

        # Add effective time (CONF:1098-32923)
        time_elem = EffectiveTime(value=self.assessment.date).to_element()
        observation.append(time_elem)

        # Add value (CONF:1098-32922, CONF:1098-32925)
        self._add_value(observation)

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
        Add value element with nutrition assessment.

        The value SHALL contain the assessment value.
        If a code is provided, it SHOULD be from SNOMED CT (CONF:1098-32925).

        Args:
            observation: observation element
        """
        if self.assessment.value_code:
            # Use CD type with code (CONF:1098-32925: SHOULD be SNOMED CT)
            value_elem = etree.SubElement(
                observation,
                f"{{{NS}}}value",
                attrib={
                    "{http://www.w3.org/2001/XMLSchema-instance}type": "CD",
                },
            )
            value_elem.set("code", self.assessment.value_code)
            value_elem.set("codeSystem", self.SNOMED_CT_OID)
            value_elem.set("displayName", self.assessment.value)
        else:
            # Use ST (string) type for free text
            value_elem = etree.SubElement(
                observation,
                f"{{{NS}}}value",
                attrib={
                    "{http://www.w3.org/2001/XMLSchema-instance}type": "ST",
                },
            )
            value_elem.text = self.assessment.value
