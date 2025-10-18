"""Smoking Status entry builder for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.social_history import SmokingStatusProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class SmokingStatusObservation(CDAElement):
    """
    Builder for C-CDA Smoking Status - Meaningful Use entry.

    Represents a snapshot observation of the patient's current smoking status
    as specified in Meaningful Use Stage 2 requirements.

    Template: 2.16.840.1.113883.10.20.22.4.78 (V2: 2014-06-09)
    Code: 72166-2 (Tobacco smoking status NHIS) from LOINC

    This represents a "snapshot in time" observation, simply reflecting what the
    patient's current smoking status is at the time of the observation.

    Supports both R2.1 and R2.0 versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.78",
                extension="2014-06-09",
                description="Smoking Status - Meaningful Use (V2) R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.78",
                extension="2014-06-09",
                description="Smoking Status - Meaningful Use (V2) R2.0",
            ),
        ],
    }

    # Code system OIDs
    LOINC_OID = "2.16.840.1.113883.6.1"  # LOINC
    SNOMED_CT_OID = "2.16.840.1.113883.6.96"  # SNOMED CT

    # Fixed LOINC code for smoking status
    SMOKING_STATUS_CODE = "72166-2"  # Tobacco smoking status NHIS
    SMOKING_STATUS_DISPLAY = "Tobacco smoking status"

    # Common smoking status codes from Smoking Status Value Set (2.16.840.1.113883.11.20.9.38)
    SMOKING_STATUS_CODES = {
        "current every day smoker": "449868002",
        "current some day smoker": "428041000124106",
        "former smoker": "8517006",
        "never smoker": "266919005",
        "smoker, current status unknown": "77176002",
        "unknown if ever smoked": "266927001",
        "heavy tobacco smoker": "428071000124103",
        "light tobacco smoker": "428061000124105",
    }

    def __init__(
        self,
        smoking_status: SmokingStatusProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize SmokingStatusObservation builder.

        Args:
            smoking_status: Smoking status data satisfying SmokingStatusProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.smoking_status = smoking_status

    def build(self) -> etree.Element:
        """
        Build Smoking Status Observation XML element.

        Returns:
            lxml Element for observation

        Note:
            This template represents a "snapshot in time" observation with a timestamp
            effectiveTime (NOT an interval). The value SHALL contain a code from the
            Smoking Status Value Set and SHALL NOT have a nullFlavor.
        """
        # Create observation element
        observation = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template IDs
        self.add_template_ids(observation)

        # Add ID (SHALL contain at least one [1..*])
        self._add_id(observation)

        # Add code (72166-2 - Tobacco smoking status NHIS)
        code_elem = Code(
            code=self.SMOKING_STATUS_CODE,
            system="LOINC",
            display_name=self.SMOKING_STATUS_DISPLAY,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        observation.append(code_elem)

        # Add status code (SHALL be "completed")
        status_elem = StatusCode("completed").to_element()
        observation.append(status_elem)

        # Add effective time (timestamp only, NOT an interval)
        time_elem = EffectiveTime(value=self.smoking_status.date).to_element()
        observation.append(time_elem)

        # Add value (SHALL be CD type with code from Smoking Status Value Set)
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
        Add value element with smoking status code.

        The value SHALL:
        - Have @xsi:type="CD"
        - Contain a code from Smoking Status Value Set (2.16.840.1.113883.11.20.9.38)
        - NOT have a nullFlavor

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
        value_elem.set("code", self.smoking_status.code)
        value_elem.set("codeSystem", self.SNOMED_CT_OID)
        value_elem.set("displayName", self.smoking_status.smoking_status)
