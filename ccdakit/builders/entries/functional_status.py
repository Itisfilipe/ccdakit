"""Functional Status entry builders for C-CDA documents."""

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.functional_status import (
    FunctionalStatusObservationProtocol,
    FunctionalStatusOrganizerProtocol,
)


# CDA namespace
NS = "urn:hl7-org:v3"


class FunctionalStatusObservation(CDAElement):
    """
    Builder for C-CDA Functional Status Observation entry.

    Represents a patient's physical function or problems that limit function.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.

    Conformance: Template 2.16.840.1.113883.10.20.22.4.67
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.67",
                extension="2014-06-09",
                description="Functional Status Observation R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.67",
                extension="2014-06-09",
                description="Functional Status Observation R2.0",
            ),
        ],
    }

    # Code system OIDs
    LOINC_OID = "2.16.840.1.113883.6.1"  # LOINC
    SNOMED_OID = "2.16.840.1.113883.6.96"  # SNOMED CT

    # Fixed observation code per CONF:1098-13908, CONF:1098-31522
    FUNCTIONAL_STATUS_CODE = "54522-8"  # Functional status

    def __init__(
        self,
        observation: FunctionalStatusObservationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize FunctionalStatusObservation builder.

        Args:
            observation: Functional status observation data
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.observation = observation

    def build(self) -> etree.Element:
        """
        Build Functional Status Observation XML element.

        Implements conformance rules:
        - CONF:1098-13905: classCode="OBS"
        - CONF:1098-13906: moodCode="EVN"
        - CONF:1098-13889, CONF:1098-13890, CONF:1098-32568: templateId
        - CONF:1098-13907: id [1..*]
        - CONF:1098-13908, CONF:1098-31522, CONF:1098-31523: code
        - CONF:1098-13929, CONF:1098-19101: statusCode
        - CONF:1098-13930: effectiveTime
        - CONF:1098-13932, CONF:1098-14234: value

        Returns:
            lxml Element for observation
        """
        # CONF:1098-13905, CONF:1098-13906: Create observation element
        observation = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # CONF:1098-13889, CONF:1098-13890, CONF:1098-32568: Add template IDs
        self.add_template_ids(observation)

        # CONF:1098-13907: Add ID (at least one)
        self._add_id(observation)

        # CONF:1098-13908, CONF:1098-31522, CONF:1098-31523: Add fixed code
        code_elem = Code(
            code=self.FUNCTIONAL_STATUS_CODE,
            system="LOINC",
            display_name="Functional status",
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"
        observation.append(code_elem)

        # CONF:1098-13929, CONF:1098-19101: Add status code
        status_elem = StatusCode("completed").to_element()
        observation.append(status_elem)

        # CONF:1098-13930: Add effective time
        time_elem = EffectiveTime(value=self.observation.date).to_element()
        observation.append(time_elem)

        # CONF:1098-13932, CONF:1098-14234: Add value
        self._add_value(observation)

        return observation

    def _add_id(self, observation: etree._Element) -> None:
        """
        Add ID element to observation (CONF:1098-13907).

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
        Add value element with coded value.

        CONF:1098-13932: SHALL contain exactly one [1..1] value
        CONF:1098-14234: If xsi:type="CD", SHOULD contain a code from SNOMED CT

        Args:
            observation: observation element
        """
        # Default to SNOMED CT if no code system specified
        code_system = self.observation.value_code_system or self.SNOMED_OID

        value_elem = etree.SubElement(
            observation,
            f"{{{NS}}}value",
            attrib={
                "{http://www.w3.org/2001/XMLSchema-instance}type": "CD",
            },
        )
        value_elem.set("code", self.observation.value_code)
        value_elem.set("codeSystem", code_system)
        value_elem.set("displayName", self.observation.value)


class FunctionalStatusOrganizer(CDAElement):
    """
    Builder for C-CDA Functional Status Organizer.

    Groups related functional status observations into categories.
    Supports both R2.1 (2014-06-09) and R2.0 (2014-06-09) versions.

    Conformance: Template 2.16.840.1.113883.10.20.22.4.66
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.66",
                extension="2014-06-09",
                description="Functional Status Organizer R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.66",
                extension="2014-06-09",
                description="Functional Status Organizer R2.0",
            ),
        ],
    }

    # Code system OIDs
    ICF_OID = "2.16.840.1.113883.6.254"  # International Classification of Functioning
    LOINC_OID = "2.16.840.1.113883.6.1"  # LOINC

    def __init__(
        self,
        organizer: FunctionalStatusOrganizerProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize FunctionalStatusOrganizer builder.

        Args:
            organizer: Organizer data satisfying FunctionalStatusOrganizerProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.organizer = organizer

    def build(self) -> etree.Element:
        """
        Build Functional Status Organizer XML element.

        Implements conformance rules:
        - CONF:1098-14355: classCode="CLUSTER"
        - CONF:1098-14357: moodCode="EVN"
        - CONF:1098-14361, CONF:1098-14362, CONF:1098-32569: templateId
        - CONF:1098-14363: id [1..*]
        - CONF:1098-14364, CONF:1098-31417: code
        - CONF:1098-14358, CONF:1098-31434: statusCode
        - CONF:1098-14359, CONF:1098-14368: component with observations

        Returns:
            lxml Element for organizer
        """
        # CONF:1098-14355, CONF:1098-14357: Create organizer element
        organizer_elem = etree.Element(
            f"{{{NS}}}organizer",
            classCode="CLUSTER",
            moodCode="EVN",
        )

        # CONF:1098-14361, CONF:1098-14362, CONF:1098-32569: Add template IDs
        self.add_template_ids(organizer_elem)

        # CONF:1098-14363: Add ID (at least one)
        self._add_id(organizer_elem)

        # CONF:1098-14364, CONF:1098-31417: Add code
        self._add_code(organizer_elem)

        # CONF:1098-14358, CONF:1098-31434: Add status code
        status_elem = StatusCode("completed").to_element()
        organizer_elem.append(status_elem)

        # CONF:1098-14359, CONF:1098-14368: Add component entries
        for observation in self.organizer.observations:
            self._add_component(organizer_elem, observation)

        return organizer_elem

    def _add_id(self, organizer_elem: etree._Element) -> None:
        """
        Add ID element to organizer (CONF:1098-14363).

        Args:
            organizer_elem: organizer element
        """
        import uuid

        id_elem = Identifier(
            root="2.16.840.1.113883.19",
            extension=str(uuid.uuid4()),
        ).to_element()
        organizer_elem.append(id_elem)

    def _add_code(self, organizer_elem: etree._Element) -> None:
        """
        Add code element for category.

        CONF:1098-14364: SHALL contain exactly one [1..1] code
        CONF:1098-31417: SHOULD be selected from ICF or LOINC

        Args:
            organizer_elem: organizer element
        """
        # Default to ICF if no code system specified
        code_system = self.organizer.category_code_system or self.ICF_OID

        code_elem = etree.SubElement(organizer_elem, f"{{{NS}}}code")
        code_elem.set("code", self.organizer.category_code)
        code_elem.set("codeSystem", code_system)
        code_elem.set("displayName", self.organizer.category)

    def _add_component(
        self,
        organizer_elem: etree._Element,
        observation: FunctionalStatusObservationProtocol,
    ) -> None:
        """
        Add component element with functional status observation.

        CONF:1098-14359: SHALL contain at least one [1..*] component
        CONF:1098-14368: SHALL contain Functional Status Observation

        Args:
            organizer_elem: organizer element
            observation: Functional status observation data
        """
        # Create component element
        component = etree.SubElement(organizer_elem, f"{{{NS}}}component")

        # Create and add functional status observation
        obs_builder = FunctionalStatusObservation(observation, version=self.version)
        component.append(obs_builder.to_element())
