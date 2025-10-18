"""Lab result entry builders for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.result import ResultObservationProtocol, ResultOrganizerProtocol


# CDA namespace
NS = "urn:hl7-org:v3"


class ResultObservation(CDAElement):
    """
    Builder for C-CDA Result Observation entry.

    Represents a single lab test result observation (e.g., glucose, hemoglobin).
    Implements Result Observation V4 (template 2.16.840.1.113883.10.20.22.4.2:2023-05-01).

    Key features:
    - Support for multiple value types (PQ, CD, ST)
    - LOINC codes for test identification
    - Interpretation codes (normal/high/low)
    - Reference ranges
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.2",
                extension="2023-05-01",
                description="Result Observation V4",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.2",
                extension="2023-05-01",
                description="Result Observation V4",
            ),
        ],
    }

    # Code system OIDs
    LOINC_OID = "2.16.840.1.113883.6.1"  # LOINC
    SNOMED_CT_OID = "2.16.840.1.113883.6.96"  # SNOMED CT
    HL7_INTERPRETATION_OID = "2.16.840.1.113883.5.83"  # HL7 ObservationInterpretation

    # Status code mapping
    STATUS_CODES = {
        "completed": "completed",
        "final": "completed",
        "preliminary": "active",
        "active": "active",
        "cancelled": "cancelled",
        "aborted": "aborted",
    }

    # Interpretation codes (HL7 ObservationInterpretation)
    INTERPRETATION_CODES = {
        "normal": "N",
        "high": "H",
        "low": "L",
        "critical": "A",
        "critically high": "HH",
        "critically low": "LL",
        "abnormal": "A",
        "n": "N",
        "h": "H",
        "l": "L",
        "a": "A",
        "hh": "HH",
        "ll": "LL",
    }

    def __init__(
        self,
        result: ResultObservationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ResultObservation builder.

        Args:
            result: Result data satisfying ResultObservationProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.result = result

    def build(self) -> etree.Element:
        """
        Build Result Observation XML element.

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

        # Add code (LOINC code for the test)
        code_elem = Code(
            code=self.result.test_code,
            system="LOINC",
            display_name=self.result.test_name,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        observation.append(code_elem)

        # Add status code
        status = self._map_status(self.result.status)
        status_elem = StatusCode(status).to_element()
        observation.append(status_elem)

        # Add effective time
        time_elem = EffectiveTime(value=self.result.effective_time).to_element()
        observation.append(time_elem)

        # Add value (PQ, CD, or ST type)
        self._add_value(observation)

        # Add interpretation code if available
        if self.result.interpretation:
            self._add_interpretation(observation)

        # Add reference range if available
        if self.result.reference_range_low or self.result.reference_range_high:
            self._add_reference_range(observation)

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

    def _map_status(self, status: str) -> str:
        """
        Map result status to C-CDA status code.

        Args:
            status: Status from protocol

        Returns:
            Mapped status code
        """
        return self.STATUS_CODES.get(status.lower(), "completed")

    def _add_value(self, observation: etree._Element) -> None:
        """
        Add value element with appropriate type (PQ, CD, or ST).

        Args:
            observation: observation element
        """
        # Determine value type
        value_type = self._determine_value_type()

        if value_type == "PQ":
            self._add_pq_value(observation)
        elif value_type == "CD":
            self._add_cd_value(observation)
        else:  # ST
            self._add_st_value(observation)

    def _determine_value_type(self) -> str:
        """
        Determine the appropriate value type based on protocol data.

        Returns:
            Value type: "PQ", "CD", or "ST"
        """
        # Use explicit value_type if provided
        if self.result.value_type:
            return self.result.value_type.upper()

        # Otherwise infer from data
        if self.result.unit:
            return "PQ"  # Physical quantity if unit is present
        else:
            return "ST"  # String type by default

    def _add_pq_value(self, observation: etree._Element) -> None:
        """
        Add Physical Quantity (PQ) value.

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
        value_elem.set("value", self.result.value)
        if self.result.unit:
            value_elem.set("unit", self.result.unit)

    def _add_cd_value(self, observation: etree._Element) -> None:
        """
        Add Coded (CD) value.

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
        # For CD values, assume the value is a code
        value_elem.set("code", self.result.value)
        value_elem.set("codeSystem", self.SNOMED_CT_OID)
        value_elem.set("displayName", self.result.test_name)

    def _add_st_value(self, observation: etree._Element) -> None:
        """
        Add String (ST) value.

        Args:
            observation: observation element
        """
        value_elem = etree.SubElement(
            observation,
            f"{{{NS}}}value",
            attrib={
                "{http://www.w3.org/2001/XMLSchema-instance}type": "ST",
            },
        )
        value_elem.text = self.result.value

    def _add_interpretation(self, observation: etree._Element) -> None:
        """
        Add interpretationCode element.

        Args:
            observation: observation element
        """
        assert self.result.interpretation is not None
        # Map interpretation to HL7 code
        code = self.INTERPRETATION_CODES.get(
            self.result.interpretation.lower(), self.result.interpretation.upper()
        )

        interp_elem = etree.SubElement(observation, f"{{{NS}}}interpretationCode")
        interp_elem.set("code", code)
        interp_elem.set("codeSystem", self.HL7_INTERPRETATION_OID)

    def _add_reference_range(self, observation: etree._Element) -> None:
        """
        Add referenceRange element with observationRange.

        Args:
            observation: observation element
        """
        ref_range_elem = etree.SubElement(observation, f"{{{NS}}}referenceRange")
        obs_range_elem = etree.SubElement(ref_range_elem, f"{{{NS}}}observationRange")

        # Add value with IVL_PQ type (interval of physical quantity)
        value_elem = etree.SubElement(
            obs_range_elem,
            f"{{{NS}}}value",
            attrib={
                "{http://www.w3.org/2001/XMLSchema-instance}type": "IVL_PQ",
            },
        )

        # Add low and high bounds
        if self.result.reference_range_low:
            low_elem = etree.SubElement(value_elem, f"{{{NS}}}low")
            low_elem.set("value", self.result.reference_range_low)
            if self.result.reference_range_unit:
                low_elem.set("unit", self.result.reference_range_unit)

        if self.result.reference_range_high:
            high_elem = etree.SubElement(value_elem, f"{{{NS}}}high")
            high_elem.set("value", self.result.reference_range_high)
            if self.result.reference_range_unit:
                high_elem.set("unit", self.result.reference_range_unit)


class ResultOrganizer(CDAElement):
    """
    Builder for C-CDA Result Organizer.

    Groups multiple lab result observations into a panel (e.g., Complete Blood Count).
    Implements Result Organizer V4 (template 2.16.840.1.113883.10.20.22.4.1:2023-05-01).

    Key features:
    - Groups related test results
    - LOINC codes for panel identification
    - Contains multiple Result Observations
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.1",
                extension="2023-05-01",
                description="Result Organizer V4",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.1",
                extension="2023-05-01",
                description="Result Organizer V4",
            ),
        ],
    }

    # Status code mapping (same as observation)
    STATUS_CODES = {
        "completed": "completed",
        "final": "completed",
        "preliminary": "active",
        "active": "active",
        "cancelled": "cancelled",
        "aborted": "aborted",
    }

    def __init__(
        self,
        organizer: ResultOrganizerProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize ResultOrganizer builder.

        Args:
            organizer: Organizer data satisfying ResultOrganizerProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.organizer = organizer

    def build(self) -> etree.Element:
        """
        Build Result Organizer XML element.

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

        # Add code (LOINC code for the panel)
        code_elem = Code(
            code=self.organizer.panel_code,
            system="LOINC",
            display_name=self.organizer.panel_name,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        organizer_elem.append(code_elem)

        # Add status code
        status = self._map_status(self.organizer.status)
        status_elem = StatusCode(status).to_element()
        organizer_elem.append(status_elem)

        # Add effective time
        time_elem = EffectiveTime(value=self.organizer.effective_time).to_element()
        organizer_elem.append(time_elem)

        # Add component entries for each result observation
        for result in self.organizer.results:
            self._add_component(organizer_elem, result)

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

    def _map_status(self, status: str) -> str:
        """
        Map result status to C-CDA status code.

        Args:
            status: Status from protocol

        Returns:
            Mapped status code
        """
        return self.STATUS_CODES.get(status.lower(), "completed")

    def _add_component(
        self, organizer_elem: etree._Element, result: ResultObservationProtocol
    ) -> None:
        """
        Add component element with result observation.

        Args:
            organizer_elem: organizer element
            result: Result observation data
        """
        # Create component element
        component = etree.SubElement(organizer_elem, f"{{{NS}}}component")

        # Create and add result observation
        obs_builder = ResultObservation(result, version=self.version)
        component.append(obs_builder.to_element())
