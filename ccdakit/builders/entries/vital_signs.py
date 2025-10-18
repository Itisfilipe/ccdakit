"""Vital Signs entry builders for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.vital_signs import VitalSignProtocol, VitalSignsOrganizerProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class VitalSignObservation(CDAElement):
    """
    Builder for C-CDA Vital Sign Observation entry.

    Represents a single vital sign measurement (e.g., blood pressure, heart rate).
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.27",
                extension="2014-06-09",
                description="Vital Sign Observation R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.27",
                extension="2014-06-09",
                description="Vital Sign Observation R2.0",
            ),
        ],
    }

    # Code system OIDs
    LOINC_OID = "2.16.840.1.113883.6.1"  # LOINC
    UCUM_OID = "2.16.840.1.113883.6.8"  # UCUM (Unified Code for Units of Measure)

    # Common vital sign LOINC codes
    VITAL_SIGN_CODES = {
        "blood pressure": "85354-9",
        "systolic blood pressure": "8480-6",
        "diastolic blood pressure": "8462-4",
        "heart rate": "8867-4",
        "respiratory rate": "9279-1",
        "body temperature": "8310-5",
        "oxygen saturation": "59408-5",
        "body height": "8302-2",
        "body weight": "29463-7",
        "bmi": "39156-5",
    }

    def __init__(
        self,
        vital_sign: VitalSignProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize VitalSignObservation builder.

        Args:
            vital_sign: Vital sign data satisfying VitalSignProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.vital_sign = vital_sign

    def build(self) -> etree.Element:
        """
        Build Vital Sign Observation XML element.

        Returns:
            lxml Element for observation
        """
        # Create observation element
        observation = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template IDs
        self.add_template_ids(observation)

        # Add ID
        self._add_id(observation)

        # Add code (LOINC code for the vital sign type)
        code_elem = Code(
            code=self.vital_sign.code,
            system="LOINC",
            display_name=self.vital_sign.type,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        observation.append(code_elem)

        # Add status code
        status_elem = StatusCode("completed").to_element()
        observation.append(status_elem)

        # Add effective time
        time_elem = EffectiveTime(value=self.vital_sign.date).to_element()
        observation.append(time_elem)

        # Add value with unit
        self._add_value(observation)

        # Add interpretation code if available
        if self.vital_sign.interpretation:
            self._add_interpretation(observation)

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
        Add value element with measurement and unit.

        Args:
            observation: observation element
        """
        value_elem = etree.SubElement(
            observation,
            f"{{{NS}}}value",
            attrib={
                "{http://www.w3.org/2001/XMLSchema-instance}type": "PQ",
            },
        )
        value_elem.set("value", self.vital_sign.value)
        value_elem.set("unit", self.vital_sign.unit)

    def _add_interpretation(self, observation: etree._Element) -> None:
        """
        Add interpretationCode element.

        Args:
            observation: observation element
        """
        assert self.vital_sign.interpretation is not None
        # Interpretation codes (HL7 ObservationInterpretation)
        interpretation_codes = {
            "normal": "N",
            "high": "H",
            "low": "L",
            "critical high": "HH",
            "critical low": "LL",
        }

        code = interpretation_codes.get(self.vital_sign.interpretation.lower(), "N")

        interp_elem = etree.SubElement(observation, f"{{{NS}}}interpretationCode")
        interp_elem.set("code", code)
        interp_elem.set("codeSystem", "2.16.840.1.113883.5.83")
        interp_elem.set("displayName", self.vital_sign.interpretation)


class VitalSignsOrganizer(CDAElement):
    """
    Builder for C-CDA Vital Signs Organizer.

    Groups multiple vital sign observations taken at the same time.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.26",
                extension="2015-08-01",
                description="Vital Signs Organizer R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.26",
                extension="2014-06-09",
                description="Vital Signs Organizer R2.0",
            ),
        ],
    }

    # LOINC code for vital signs panel
    VITAL_SIGNS_PANEL_CODE = "46680005"  # Vital signs (SNOMED CT) - alternate: 74728-7 (LOINC)

    def __init__(
        self,
        organizer: VitalSignsOrganizerProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize VitalSignsOrganizer builder.

        Args:
            organizer: Organizer data satisfying VitalSignsOrganizerProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.organizer = organizer

    def build(self) -> etree.Element:
        """
        Build Vital Signs Organizer XML element.

        Returns:
            lxml Element for organizer
        """
        # Create organizer element
        organizer_elem = etree.Element(
            f"{{{NS}}}organizer",
            classCode="CLUSTER",
            moodCode="EVN",
        )

        # Add template IDs
        self.add_template_ids(organizer_elem)

        # Add ID
        self._add_id(organizer_elem)

        # Add code (vital signs panel)
        code_elem = etree.SubElement(organizer_elem, f"{{{NS}}}code")
        code_elem.set("code", self.VITAL_SIGNS_PANEL_CODE)
        code_elem.set("codeSystem", "2.16.840.1.113883.6.96")
        code_elem.set("codeSystemName", "SNOMED CT")
        code_elem.set("displayName", "Vital signs")

        # Add status code
        status_elem = StatusCode("completed").to_element()
        organizer_elem.append(status_elem)

        # Add effective time
        time_elem = EffectiveTime(value=self.organizer.date).to_element()
        organizer_elem.append(time_elem)

        # Add component entries for each vital sign observation
        for vital_sign in self.organizer.vital_signs:
            self._add_component(organizer_elem, vital_sign)

        return organizer_elem

    def _add_id(self, organizer_elem: etree._Element) -> None:
        """
        Add ID element to organizer.

        Args:
            organizer_elem: organizer element
        """
        import uuid

        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=str(uuid.uuid4()),
        ).to_element()
        organizer_elem.append(id_elem)

    def _add_component(self, organizer_elem: etree._Element, vital_sign: VitalSignProtocol) -> None:
        """
        Add component element with vital sign observation.

        Args:
            organizer_elem: organizer element
            vital_sign: Vital sign data
        """
        # Create component element
        component = etree.SubElement(organizer_elem, f"{{{NS}}}component")

        # Create and add vital sign observation
        obs_builder = VitalSignObservation(vital_sign, version=self.version)
        component.append(obs_builder.to_element())
