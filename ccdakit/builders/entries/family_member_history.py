"""Family Member History entry builders for C-CDA documents."""

import uuid

from lxml import etree

from ccdakit.builders.common import Code, EffectiveTime, Identifier, StatusCode
from ccdakit.core.base import CDAElement, CDAVersion, TemplateConfig
from ccdakit.protocols.family_history import (
    FamilyHistoryObservationProtocol,
    FamilyMemberHistoryProtocol,
)


# CDA namespace
NS = "urn:hl7-org:v3"
# SDTC namespace for extensions
SDTC_NS = "urn:hl7-org:sdtc"


class FamilyHistoryObservation(CDAElement):
    """
    Builder for C-CDA Family History Observation entry.

    Represents a condition/problem observed in a family member.
    Supports both R2.1 (2015-08-01) and R2.0 (2014-06-09) versions.

    Conformance: 2.16.840.1.113883.10.20.22.4.46 (Family History Observation V3)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.46",
                extension="2015-08-01",
                description="Family History Observation R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.46",
                extension="2015-08-01",
                description="Family History Observation R2.0",
            ),
        ],
    }

    # Code system OIDs
    SNOMED_OID = "2.16.840.1.113883.6.96"
    ICD10_OID = "2.16.840.1.113883.6.90"
    LOINC_OID = "2.16.840.1.113883.6.1"

    def __init__(
        self,
        observation: FamilyHistoryObservationProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize FamilyHistoryObservation builder.

        Args:
            observation: Observation data satisfying FamilyHistoryObservationProtocol
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.observation = observation

    def build(self) -> etree.Element:
        """
        Build Family History Observation XML element.

        Returns:
            lxml Element for observation

        Conformance Rules:
            - CONF:1198-8586: SHALL classCode="OBS"
            - CONF:1198-8587: SHALL moodCode="EVN"
            - CONF:1198-8599: SHALL contain templateId
            - CONF:1198-8592: SHALL contain at least one id
            - CONF:1198-32427: SHALL contain code (observation type)
            - CONF:1198-8590: SHALL contain statusCode="completed"
            - CONF:1198-8593: SHOULD contain effectiveTime
            - CONF:1198-8591: SHALL contain value (condition code)
        """
        # Create observation element with required attributes (CONF:1198-8586, CONF:1198-8587)
        observation = etree.Element(
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template IDs (CONF:1198-8599, CONF:1198-10496, CONF:1198-32605)
        self.add_template_ids(observation)

        # Add IDs (CONF:1198-8592)
        self._add_ids(observation)

        # Add observation type code (CONF:1198-32427)
        self._add_code(observation)

        # Add status code (CONF:1198-8590, CONF:1198-19098)
        status_elem = StatusCode("completed").to_element()
        observation.append(status_elem)

        # Add effective time (CONF:1198-8593)
        if self.observation.effective_time:
            time_elem = EffectiveTime(value=self.observation.effective_time).to_element()
            observation.append(time_elem)

        # Add value (the actual condition code) (CONF:1198-8591)
        self._add_value(observation)

        # Add age observation if present (CONF:1198-8675)
        if self.observation.age_at_onset is not None:
            self._add_age_observation(observation)

        # Add death observation if present (CONF:1198-8678)
        if self.observation.deceased_age is not None or self.observation.deceased_cause_code:
            self._add_death_observation(observation)

        return observation

    def _add_ids(self, observation: etree._Element) -> None:
        """
        Add ID elements to observation.

        Args:
            observation: observation element
        """
        # Add persistent ID if available
        if self.observation.persistent_id:
            pid = self.observation.persistent_id
            id_elem = Identifier(root=pid.root, extension=pid.extension).to_element()
            observation.append(id_elem)
        else:
            # Add a generated ID
            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            observation.append(id_elem)

    def _add_code(self, observation: etree._Element) -> None:
        """
        Add observation type code element.

        Args:
            observation: observation element

        Conformance: CONF:1198-32427, CONF:1198-32847
        """
        # Default to "Disease" if not specified
        obs_code = self.observation.observation_type_code or "64572001"
        obs_display = self.observation.observation_type_display_name or "Disease"

        # Create code element (SNOMED CT)
        code_elem = Code(
            code=obs_code,
            system="SNOMED",
            display_name=obs_display,
        ).to_element()
        code_elem.tag = f"{{{NS}}}code"

        # Add translation (LOINC) (CONF:1198-32847)
        # Common LOINC translation: 75315-2 = Family member health status
        translation = etree.SubElement(code_elem, f"{{{NS}}}translation")
        translation.set("code", "75315-2")
        translation.set("codeSystem", self.LOINC_OID)
        translation.set("codeSystemName", "LOINC")
        translation.set("displayName", "Family member health status")

        observation.append(code_elem)

    def _add_value(self, observation: etree._Element) -> None:
        """
        Add value element with condition code.

        Args:
            observation: observation element
        """
        # Determine code system OID
        code_system = self.observation.condition_code_system.upper()
        if "SNOMED" in code_system:
            system_oid = self.SNOMED_OID
            system_name = "SNOMED CT"
        elif "ICD" in code_system or "ICD-10" in code_system:
            system_oid = self.ICD10_OID
            system_name = "ICD-10-CM"
        else:
            # Default to SNOMED
            system_oid = self.SNOMED_OID
            system_name = self.observation.condition_code_system

        # Create value element as CD (Concept Descriptor)
        value = etree.SubElement(
            observation,
            f"{{{NS}}}value",
        )
        value.set("{http://www.w3.org/2001/XMLSchema-instance}type", "CD")
        value.set("code", self.observation.condition_code)
        value.set("codeSystem", system_oid)
        value.set("codeSystemName", system_name)
        value.set("displayName", self.observation.condition_name)

    def _add_age_observation(self, observation: etree._Element) -> None:
        """
        Add Age Observation entry relationship.

        Args:
            observation: observation element

        Conformance: CONF:1198-8675, CONF:1198-8676, CONF:1198-8677, CONF:1198-15526
        """
        # Create entry relationship (CONF:1198-8675, CONF:1198-8676, CONF:1198-8677)
        entry_rel = etree.SubElement(
            observation,
            f"{{{NS}}}entryRelationship",
            typeCode="SUBJ",
            inversionInd="true",
        )

        # Create Age Observation (CONF:1198-15526)
        # Template: 2.16.840.1.113883.10.20.22.4.31
        age_obs = etree.SubElement(
            entry_rel,
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template ID
        template_id = etree.SubElement(age_obs, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.31")

        # Add code (445518008 = Age At Onset)
        age_code = Code(
            code="445518008",
            system="SNOMED",
            display_name="Age At Onset",
        ).to_element()
        age_code.tag = f"{{{NS}}}code"
        age_obs.append(age_code)

        # Add status code
        status_elem = StatusCode("completed").to_element()
        age_obs.append(status_elem)

        # Add value (age in years)
        value = etree.SubElement(age_obs, f"{{{NS}}}value")
        value.set("{http://www.w3.org/2001/XMLSchema-instance}type", "PQ")
        value.set("value", str(self.observation.age_at_onset))
        value.set("unit", "a")  # years

    def _add_death_observation(self, observation: etree._Element) -> None:
        """
        Add Family History Death Observation entry relationship.

        Args:
            observation: observation element

        Conformance: CONF:1198-8678, CONF:1198-8679, CONF:1198-15527
        """
        # Create entry relationship (CONF:1198-8678, CONF:1198-8679)
        entry_rel = etree.SubElement(
            observation,
            f"{{{NS}}}entryRelationship",
            typeCode="CAUS",
        )

        # Create Family History Death Observation (CONF:1198-15527)
        # Template: 2.16.840.1.113883.10.20.22.4.47
        death_obs = etree.SubElement(
            entry_rel,
            f"{{{NS}}}observation",
            classCode="OBS",
            moodCode="EVN",
        )

        # Add template ID
        template_id = etree.SubElement(death_obs, f"{{{NS}}}templateId")
        template_id.set("root", "2.16.840.1.113883.10.20.22.4.47")

        # Add code (ASSERTION)
        death_code = Code(
            code="ASSERTION",
            system="ActCode",
            display_name="Assertion",
        ).to_element()
        death_code.tag = f"{{{NS}}}code"
        death_obs.append(death_code)

        # Add status code
        status_elem = StatusCode("completed").to_element()
        death_obs.append(status_elem)

        # Add value (cause of death if available)
        if self.observation.deceased_cause_code:
            value = etree.SubElement(death_obs, f"{{{NS}}}value")
            value.set("{http://www.w3.org/2001/XMLSchema-instance}type", "CD")
            value.set("code", self.observation.deceased_cause_code)
            value.set("codeSystem", self.SNOMED_OID)
            value.set("codeSystemName", "SNOMED CT")
            if self.observation.deceased_cause_display_name:
                value.set("displayName", self.observation.deceased_cause_display_name)

        # Add age at death if available
        if self.observation.deceased_age is not None:
            # Add entryRelationship with Age Observation
            age_entry_rel = etree.SubElement(
                death_obs,
                f"{{{NS}}}entryRelationship",
                typeCode="SUBJ",
                inversionInd="true",
            )

            age_obs = etree.SubElement(
                age_entry_rel,
                f"{{{NS}}}observation",
                classCode="OBS",
                moodCode="EVN",
            )

            # Add template ID
            age_template_id = etree.SubElement(age_obs, f"{{{NS}}}templateId")
            age_template_id.set("root", "2.16.840.1.113883.10.20.22.4.31")

            # Add code (Age)
            age_code = Code(
                code="445518008",
                system="SNOMED",
                display_name="Age",
            ).to_element()
            age_code.tag = f"{{{NS}}}code"
            age_obs.append(age_code)

            # Add status code
            age_status_elem = StatusCode("completed").to_element()
            age_obs.append(age_status_elem)

            # Add value (age in years)
            age_value = etree.SubElement(age_obs, f"{{{NS}}}value")
            age_value.set("{http://www.w3.org/2001/XMLSchema-instance}type", "PQ")
            age_value.set("value", str(self.observation.deceased_age))
            age_value.set("unit", "a")  # years


class FamilyHistoryOrganizer(CDAElement):
    """
    Builder for C-CDA Family History Organizer entry.

    Groups observations about a specific family member.
    Supports both R2.1 (2015-08-01) and R2.0 (2014-06-09) versions.

    Conformance: 2.16.840.1.113883.10.20.22.4.45 (Family History Organizer V3)
    """

    # Template IDs for different versions
    TEMPLATES = {
        CDAVersion.R2_1: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.45",
                extension="2015-08-01",
                description="Family History Organizer R2.1",
            ),
        ],
        CDAVersion.R2_0: [
            TemplateConfig(
                root="2.16.840.1.113883.10.20.22.4.45",
                extension="2015-08-01",
                description="Family History Organizer R2.0",
            ),
        ],
    }

    def __init__(
        self,
        family_member: FamilyMemberHistoryProtocol,
        version: CDAVersion = CDAVersion.R2_1,
        **kwargs,
    ):
        """
        Initialize FamilyHistoryOrganizer builder.

        Args:
            family_member: Family member history data
            version: C-CDA version (R2.1 or R2.0)
            **kwargs: Additional arguments passed to CDAElement
        """
        super().__init__(version=version, **kwargs)
        self.family_member = family_member

    def build(self) -> etree.Element:
        """
        Build Family History Organizer XML element.

        Returns:
            lxml Element for organizer

        Conformance Rules:
            - CONF:1198-8600: SHALL classCode="CLUSTER"
            - CONF:1198-8601: SHALL moodCode="EVN"
            - CONF:1198-8604: SHALL contain templateId
            - CONF:1198-32485: SHALL contain at least one id
            - CONF:1198-8602: SHALL contain statusCode="completed"
            - CONF:1198-8609: SHALL contain subject
            - CONF:1198-32428: SHALL contain component (observations)
        """
        # Create organizer element with required attributes (CONF:1198-8600, CONF:1198-8601)
        organizer = etree.Element(
            f"{{{NS}}}organizer",
            classCode="CLUSTER",
            moodCode="EVN",
        )

        # Add template IDs (CONF:1198-8604, CONF:1198-10497, CONF:1198-32606)
        self.add_template_ids(organizer)

        # Add IDs (CONF:1198-32485)
        self._add_ids(organizer)

        # Add status code (CONF:1198-8602, CONF:1198-19099)
        status_elem = StatusCode("completed").to_element()
        organizer.append(status_elem)

        # Add subject (family member relationship) (CONF:1198-8609)
        self._add_subject(organizer)

        # Add components (observations) (CONF:1198-32428, CONF:1198-32429)
        for observation in self.family_member.observations:
            self._add_component(organizer, observation)

        return organizer

    def _add_ids(self, organizer: etree._Element) -> None:
        """
        Add ID elements to organizer.

        Args:
            organizer: organizer element
        """
        # Add persistent ID if available
        if self.family_member.persistent_id:
            pid = self.family_member.persistent_id
            id_elem = Identifier(root=pid.root, extension=pid.extension).to_element()
            organizer.append(id_elem)
        else:
            # Add a generated ID
            id_elem = Identifier(
                root="2.16.840.1.113883.19",
                extension=str(uuid.uuid4()),
            ).to_element()
            organizer.append(id_elem)

    def _add_subject(self, organizer: etree._Element) -> None:
        """
        Add subject element with family member relationship.

        Args:
            organizer: organizer element

        Conformance: CONF:1198-8609, CONF:1198-15244, CONF:1198-15245,
                    CONF:1198-15246, CONF:1198-15248
        """
        # Create subject element (CONF:1198-8609)
        subject = etree.SubElement(organizer, f"{{{NS}}}subject")

        # Create relatedSubject (CONF:1198-15244, CONF:1198-15245)
        related_subject = etree.SubElement(
            subject,
            f"{{{NS}}}relatedSubject",
            classCode="PRS",
        )

        # Add relationship code (CONF:1198-15246)
        code_elem = etree.SubElement(related_subject, f"{{{NS}}}code")
        code_elem.set("code", self.family_member.relationship_code)
        code_elem.set("codeSystem", "2.16.840.1.113883.5.111")  # RoleCode
        code_elem.set("codeSystemName", "RoleCode")
        code_elem.set("displayName", self.family_member.relationship_display_name)

        # Add subject details if available (CONF:1198-15248)
        if self.family_member.subject:
            self._add_subject_details(related_subject)

    def _add_subject_details(self, related_subject: etree._Element) -> None:
        """
        Add subject details (gender, birth, deceased info).

        Args:
            related_subject: relatedSubject element

        Conformance: CONF:1198-15248, CONF:1198-15974, CONF:1198-15976,
                    CONF:1198-15249, CONF:1198-15981, CONF:1198-15982
        """
        subject_data = self.family_member.subject

        # Create subject element
        subject_elem = etree.SubElement(related_subject, f"{{{NS}}}subject")

        # Add administrative gender code (CONF:1198-15974)
        if subject_data.administrative_gender_code:
            gender_code = etree.SubElement(subject_elem, f"{{{NS}}}administrativeGenderCode")
            gender_code.set("code", subject_data.administrative_gender_code)
            gender_code.set("codeSystem", "2.16.840.1.113883.5.1")
            gender_code.set("codeSystemName", "AdministrativeGender")

        # Add birth time (CONF:1198-15976)
        if subject_data.birth_time:
            birth_time = etree.SubElement(subject_elem, f"{{{NS}}}birthTime")
            birth_time.set("value", subject_data.birth_time.strftime("%Y%m%d"))

        # Add SDTC extensions
        # Register SDTC namespace
        etree.register_namespace("sdtc", SDTC_NS)

        # Add sdtc:deceasedInd (CONF:1198-15981)
        if subject_data.deceased_ind is not None:
            deceased_ind = etree.SubElement(
                subject_elem,
                f"{{{SDTC_NS}}}deceasedInd",
            )
            deceased_ind.set("value", "true" if subject_data.deceased_ind else "false")

        # Add sdtc:deceasedTime (CONF:1198-15982)
        if subject_data.deceased_time:
            deceased_time = etree.SubElement(
                subject_elem,
                f"{{{SDTC_NS}}}deceasedTime",
            )
            deceased_time.set("value", subject_data.deceased_time.strftime("%Y%m%d"))

    def _add_component(
        self, organizer: etree._Element, observation: FamilyHistoryObservationProtocol
    ) -> None:
        """
        Add component with Family History Observation.

        Args:
            organizer: organizer element
            observation: Observation data
        """
        # Create component element
        component = etree.SubElement(organizer, f"{{{NS}}}component")

        # Create and add Family History Observation
        obs_builder = FamilyHistoryObservation(observation, version=self.version)
        component.append(obs_builder.to_element())
